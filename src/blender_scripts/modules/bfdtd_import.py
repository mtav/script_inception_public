#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Module for use by Blender addons

Old blender 2.49 stuff:
Name: 'Bristol FDTD (*.in,*.geo,*.inp)'
Blender: 249
Group: 'Import'
Tooltip: 'Import from Bristol FDTD'
'''

# To make Blender happy:
bl_info = {"name":"bfdtd_import - MODULE - NOT ADDON", "category": "Module", 'warning': 'MODULE - NOT ADDON'}

###############################
# IMPORTS
###############################
from bfdtd.bfdtd_parser import *
from blender_scripts.modules.FDTDGeometryObjects import *
from blender_scripts.modules.layer_manager import LayerManagerObjects
from bfdtd.bristolFDTD_generator_functions import *
from mathutils import *
import os
import pickle
#import cPickle
import utilities.brisFDTD_ID_info as brisFDTD_ID_info
import time
from blender_scripts.modules.blender_utilities import selectObjects
import blender_scripts.modules.blender_utilities as blender_utilities
import argparse

import bpy
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector

#import layer_manager
#from Blender import Draw, BGL, Text, Scene, Window, Object

# TODO: When importing multiple files, avoid re-creating already existing materials (i.e. same refractive index)
# TODO: add new "properties" like refractive index to objects if possible
# TODO: Optimize speed (quite slow when there are thousands of objects). Quick workaround: Option to import all objects as links of the same or as some simple oriented/non-oriented object.
# TODO: Option to autosave after import using bpy.ops.wm.save_as_mainfile()
# TODO: CLI tool to convert BFDTD files to .blende/.h5/.vtk/etc
# TODO: Any point in creating a second BFDTD import class?: blender_scripts/addons/io_import_scene_bfdtd.py and blender_scripts/modules/bfdtd_import.py

###############################
# INITIALIZATIONS
###############################
#cfgfile = os.path.expanduser('~')+'/BlenderImportBFDTD.txt'

# official script data location :)
# Blender >=2.5
if os.getenv('BLENDERDATADIR'):
  cfgfile = os.getenv('BLENDERDATADIR')+os.sep+'BlenderImportBFDTD.txt'
else:
  cfgfile = getuserdir()+os.sep+'BlenderImportBFDTD.txt'

# Blender <2.49b
#print('Blender.Get("datadir") = '+str(Blender.Get("datadir")))
#if Blender.Get("datadir"):
  #print('datadir defined')
  #cfgfile = Blender.Get("datadir")+'/BlenderImportBFDTD.txt'
#else:
  #print('datadir not defined or somehow broken. Make sure the directory $HOME/.blender/scripts/bpydata is present and accessible.')
  #sys.exit(0)

def addObjectsByDuplication(N=1, createObjectFunction=bpy.ops.object.empty_add, GUI_loaded=False):
  '''
  Until we figure out a way to allocate space for objects to add them faster, we work around the problem by using blender's duplicate function.
  This means the number of objects increases according to a 2^n series.
  
  .. note:: This function is currently unused...
  '''
  ## progress indicator does not work when running from CLI
  if GUI_loaded:
    bpy.context.window_manager.progress_begin(0, 100)

  # we will store added objects in a list
  L = N*[0]
  current_idx = 0

  # deselect all
  bpy.ops.object.select_all(action = 'DESELECT')

  # add first object
  createObjectFunction()
  L[current_idx] = bpy.context.object
  current_idx += 1

  # duplicate
  while 2*current_idx <= N:
      sub_start_time = time.time()

      bpy.ops.object.select_linked()

      print(( 'current_idx =', current_idx, 'selection =', len(bpy.context.selected_objects) ))

      bpy.ops.object.duplicate_move_linked()

      L[current_idx:current_idx+len(bpy.context.selected_objects)] = bpy.context.selected_objects
      current_idx += len(bpy.context.selected_objects)
      if GUI_loaded:
        bpy.context.window_manager.progress_update(current_idx/N)
      else:
        print(('progress =', current_idx/N))
      print ('Elapsed time: ',round(time.time()-sub_start_time,4),'seconds')

  print('Last duplication...')
  selectObjects( L[0 : N - current_idx] )
  bpy.ops.object.duplicate_move_linked()

  bpy.context.window_manager.progress_end()

  return(L)

###############################
# IMPORT FUNCTION
###############################
class BristolFDTDimporter(object):
  '''
  .. todo:: Importing same file twice via GUI leads to existing group error. Fix.
  .. todo:: Selecting multiple files for import does not work. Fix.
  .. todo:: move each file into a separate scene + use the 2*20 layers in blender for the different types of objects (groups will be used)
  .. todo:: option to replace previous group/scene if re-opening the same file?
  .. todo:: undo/redo support.
  .. todo:: choose group to import to. Additional importer option?
  .. todo:: skip spheres/distorted/... options?
  .. todo:: separate max number of objects for each type of objects?
  .. todo:: add "layer property" to know if object is over or under another one. + find way to visualize it.
  .. todo:: loop through global object list instead of per object type?
  .. todo:: recursive import of all .inp, .geo, or .in files in a directory (as possible via CLI, but via GUI)
  .. todo:: finish placeholder support
  .. todo:: relative/absolute coordinates for restriction box dimensions + corresponding options in CLI+GUI
  .. todo:: option to use numeric indexing for snapshots, or way to view numeric and alphabetic indexes (old and new system) via object properties
  
  refs:
  
  * blender-2.73a-linux-glibc211-x86_64/2.73/scripts/addons/io_mesh_stl/__init__.py
  * blender-2.73a-linux-glibc211-x86_64/2.73/scripts/modules/bpy_extras/io_utils.py
  '''
  def __init__(self):
    self.use_placeholder = False
    self.placeholder_type = 'first_imported_object'
    
    self.cylinder_to_line_mesh = True
    
    self.restrict_import_volume = False
    self.xmin = 0
    self.xmax = 1
    self.ymin = 0
    self.ymax = 1
    self.zmin = 0
    self.zmax = 1
    
    self.volume_specification_style = 'relative'
    
    self.pre_2008_BFDTD_version = False
    
    self.no_geometry = False
    self.import_cylinders = True
    self.import_blocks = True
    
    self.verbosity = 0
    
    self.GUI_loaded = False
    self.numbered_prefixes = True

    self.use_Nmax_objects = True
    self.Nmax_objects = 500
    
    self.create_vertex_mesh = False
    
  def __str__(self):
    '''printing function'''
    return self.PrintSelf()

  def PrintSelf(self, indent=''):
    '''printing function with indent'''
    ret = ''
    ret += indent + 'use_placeholder = {}\n'.format(self.use_placeholder)
    ret += indent + 'placeholder_type = {}\n'.format(self.placeholder_type)
    ret += indent + 'restrict_import_volume = {}\n'.format(self.restrict_import_volume)
    ret += indent + 'volume_specification_style = {}\n'.format(self.volume_specification_style)
    ret += indent + 'xmin = {}\n'.format(self.xmin)
    ret += indent + 'xmax = {}\n'.format(self.xmax)
    ret += indent + 'ymin = {}\n'.format(self.ymin)
    ret += indent + 'ymax = {}\n'.format(self.ymax)
    ret += indent + 'zmin = {}\n'.format(self.zmin)
    ret += indent + 'zmax = {}\n'.format(self.zmax)
    ret += indent + 'pre_2008_BFDTD_version = {}\n'.format(self.pre_2008_BFDTD_version)
    ret += indent + 'import_cylinders = {}\n'.format(self.import_cylinders)
    ret += indent + 'import_blocks = {}\n'.format(self.import_blocks)
    ret += indent + 'verbosity = {}\n'.format(self.verbosity)
    ret += indent + 'GUI_loaded = {}\n'.format(self.GUI_loaded)
    ret += indent + 'numbered_prefixes = {}\n'.format(self.numbered_prefixes)
    ret += indent + 'use_Nmax_objects = {}\n'.format(self.use_Nmax_objects)
    ret += indent + 'Nmax_objects = {}'.format(self.Nmax_objects)
    return(ret)

  def importBristolFDTD(self, filename_list):
    '''
    Import one or more BristolFDTD files into Blender.

    :param filename_list: single .geo, .inp or .in file, or a list of such files
    '''
    if isinstance(filename_list, str):
      filename_list = [filename_list]

    Nfiles = len(filename_list)
    prefix_zfill = len(str(Nfiles-1))
    for i in range(Nfiles):
      print('Importing {}/{} : {}'.format(i+1, Nfiles, filename_list[i]))
      if Nfiles>1 and self.numbered_prefixes:
        self.importBristolFDTD_single_file(filename_list[i], filename_idx=i, prefix_zfill=prefix_zfill)
      else:
        self.importBristolFDTD_single_file(filename_list[i])
    return
    
  def importBristolFDTD_single_file(self, filename, filename_idx=None, prefix_zfill=0):
      '''
      Import BristolFDTD geometry from .in,.geo or .inp and create corresponding structure in Blender.
      
      This function imports a single file.
      To import multiple files, use :py:func:`importBristolFDTD`
      '''

      start_time = time.time()

      print('----->Importing bristol FDTD geometry: ' + filename)
      print(self.PrintSelf('\t'))
      
      #Blender.Window.WaitCursor(1);

      # save import path
      # Blender.Set('tempdir',os.path.dirname(filename));
      #FILE = open(, 'w');
      #pickle.dump(, FILE);
      #FILE.close();

      with open(cfgfile, 'wb') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        pickle.dump(filename, f, pickle.HIGHEST_PROTOCOL)

      # create structured_entries
      structured_entries = readBristolFDTD(filename)

      ##################
      # GROUP SETUP
      ##################
      # create group corresponding to this file
      # deselect all
      bpy.ops.object.select_all(action='DESELECT')

      # Truncated to 63 characters because that seems to be the maximum string length Blender accepts for group names.
      # (allows keeping part of the path for better identification if multiple files use the same basename)
      if filename_idx is None:
        group_name = filename[-63:]
      else:
        group_name_prefix = str(filename_idx).zfill(prefix_zfill) + '-'
        group_name = group_name_prefix + filename[-(63-len(group_name_prefix)):]

      #if group_name in bpy.data.groups:
        #raise Exception('group already exists: {}\n{}'.format(group_name, bpy.data.groups))
      
      # older version
      #bpy.ops.group.create(name=group_name)
      # This version ensures that a new group name is created if necessary and stores the new group in *current_group*.
      # current_group = bpy.data.groups.new(name=group_name) # blender<2.80
      # group_name = current_group.name # blender<2.80
      collection_current_file = blender_utilities.make_collection(group_name)  # blender>=2.80

      collection_meshes = blender_utilities.make_collection('meshes', parent_collection=collection_current_file, checkExisting=False)
      collection_boxes = blender_utilities.make_collection('boxes', parent_collection=collection_current_file, checkExisting=False)
      collection_excitations = blender_utilities.make_collection('excitations', parent_collection=collection_current_file, checkExisting=False)
      collection_frequencySnapshots = blender_utilities.make_collection('frequencySnapshots', parent_collection=collection_current_file, checkExisting=False)
      collection_timeSnapshots = blender_utilities.make_collection('timeSnapshots', parent_collection=collection_current_file, checkExisting=False)
      collection_epsilonSnapshots = blender_utilities.make_collection('epsilonSnapshots', parent_collection=collection_current_file, checkExisting=False)
      collection_spheres = blender_utilities.make_collection('spheres', parent_collection=collection_current_file, checkExisting=False)
      collection_distorted = blender_utilities.make_collection('distorted', parent_collection=collection_current_file, checkExisting=False)
      collection_blocks = blender_utilities.make_collection('blocks', parent_collection=collection_current_file, checkExisting=False)
      collection_cylinders = blender_utilities.make_collection('cylinders', parent_collection=collection_current_file, checkExisting=False)
      collection_probes = blender_utilities.make_collection('probes', parent_collection=collection_current_file, checkExisting=False)
      ##################

      # we create an instance of the FDTDGeometryObjects class, which allows adding objects to the scene with shared materials (TODO: maybe find a better system?)
      FDTDGeometryObjects_obj = FDTDGeometryObjects()

      # Blender.Window.RedrawAll(); # This must be called before any SetActiveLayer calls!

      layerManager = LayerManagerObjects()
      
      # Box
      obj = FDTDGeometryObjects_obj.GEObox(structured_entries.box.name, Vector(structured_entries.box.lower), Vector(structured_entries.box.upper))
      blender_utilities.setActiveObject(obj, context=bpy.context)
      blender_utilities.setCollections(obj, [collection_boxes], context=bpy.context)
      
      # Mesh
      obj = FDTDGeometryObjects_obj.GEOmesh('mesh', False, structured_entries.mesh.getXmeshDelta(),structured_entries.mesh.getYmeshDelta(),structured_entries.mesh.getZmeshDelta());
      blender_utilities.setActiveObject(obj, context=bpy.context)
      blender_utilities.setCollections(obj, [collection_meshes], context=bpy.context)

      # Time_snapshot (time or EPS)
      Ntsnaps = 0
      for time_snapshot in structured_entries.time_snapshot_list:

        Ntsnaps += 1
        snap_plane = time_snapshot.getPlaneLetter()
        probe_ident = structured_entries.flag.id_string.replace('\"','')
        snap_time_number = 1
        TimeSnapshotFileName, alphaID, pair = brisFDTD_ID_info.numID_to_alphaID_TimeSnapshot(Ntsnaps, snap_plane, probe_ident, snap_time_number)

        if time_snapshot.eps == 0:
          obj = FDTDGeometryObjects_obj.GEOtime_snapshot(time_snapshot.name, time_snapshot.getPlaneLetter(), time_snapshot.P1, time_snapshot.P2)
          blender_utilities.setActiveObject(obj, context=bpy.context)
          blender_utilities.setCollections(obj, [collection_timeSnapshots], context=bpy.context)
        else:
          obj = FDTDGeometryObjects_obj.GEOeps_snapshot(TimeSnapshotFileName, time_snapshot.getPlaneLetter(), time_snapshot.P1, time_snapshot.P2)
          blender_utilities.setActiveObject(obj, context=bpy.context)
          blender_utilities.setCollections(obj, [collection_epsilonSnapshots], context=bpy.context)

      # Frequency_snapshot
      # TODO: Finally get a correct system for filenames/comment names/etc implemented. getfilename() or something...
      Nfsnaps = 0
      for frequency_snapshot in structured_entries.frequency_snapshot_list:
        #Blender.Window.SetActiveLayer(1<<layerManager.DefaultLayers.index('frequency_snapshots_'+planeNumberName(frequency_snapshot.plane)[1]));

        Nfsnaps += 1
        snap_plane = frequency_snapshot.getPlaneLetter()
        probe_ident = structured_entries.flag.id_string.replace('\"','')
        snap_time_number = 0
        FrequencySnapshotFileName, alphaID, pair = brisFDTD_ID_info.numID_to_alphaID_FrequencySnapshot(Nfsnaps, snap_plane, probe_ident, snap_time_number, pre_2008_BFDTD_version=self.pre_2008_BFDTD_version)

        obj = FDTDGeometryObjects_obj.GEOfrequency_snapshot(FrequencySnapshotFileName, frequency_snapshot.getPlaneLetter(), frequency_snapshot.P1, frequency_snapshot.P2)
        #obj = FDTDGeometryObjects_obj.GEOfrequency_snapshot(frequency_snapshot.name, frequency_snapshot.plane, frequency_snapshot.P1, frequency_snapshot.P2)

        blender_utilities.setActiveObject(obj, context=bpy.context)
        blender_utilities.setCollections(obj, [collection_frequencySnapshots], context=bpy.context)

      # Excitation
      #Blender.Window.SetActiveLayer(1<<layerManager.DefaultLayers.index('excitations'));
      for excitation in structured_entries.excitation_list:
          #Blender.Window.SetActiveLayer(1<<layerManager.DefaultLayers.index('excitations'));
          #print(Blender.Window.GetActiveLayer())
          #print(excitation)
          obj = FDTDGeometryObjects_obj.GEOexcitation(excitation);
          blender_utilities.setActiveObject(obj, context=bpy.context)
          blender_utilities.setCollections(obj, [collection_excitations], context=bpy.context)
          
          #FDTDGeometryObjects_obj.GEOexcitation(excitation.name, Vector(excitation.P1), Vector(excitation.P2));
      # Probe
      #Blender.Window.SetActiveLayer(1<<layerManager.DefaultLayers.index('probes'));
      Nprobes = 0
      for probe in structured_entries.probe_list:
          # print('probe = ',Vector(probe.position))
          Nprobes += 1
          ProbeFileName = 'p' + str(Nprobes).zfill(2) + structured_entries.flag.id_string.replace('\"','') + '.prn'
          #FDTDGeometryObjects_obj.GEOprobe(probe.name+' ('+ProbeFileName+')', Vector(probe.position));
          obj = FDTDGeometryObjects_obj.GEOprobe(ProbeFileName, Vector(probe.position));
          blender_utilities.setActiveObject(obj, context=bpy.context)
          blender_utilities.setCollections(obj, [collection_probes], context=bpy.context)

      ##################################################################
      ### geometry loading
      
      if not self.no_geometry:
        
        if self.create_vertex_mesh:
          
          # just create a mesh of vertices representing object locations
          # .. todo:: just as with the lines for cylinders, this should be an option for spheres (i.e. different placeholders for each type of object) (also create different vertex mesh for each "material"/.geo file)
          
          L = structured_entries.getGeometryObjects()
          N = len(L)
          print('N(objects) = {}'.format(N))
          
          verts = N*[Vector((0,0,0))]
          
          for idx, obj in enumerate(L):
              verts[idx] = Vector(obj.getLocation())
          
          edges = []
          faces = []
          
          mesh = bpy.data.meshes.new(name="Object positions")
          mesh.from_pydata(verts, edges, faces)
          #object_data_add(bpy.context, mesh, operator=self)
          object_data_add(bpy.context, mesh)
          
        else:
          # Sphere
          #Blender.Window.SetActiveLayer(1<<layerManager.DefaultLayers.index('spheres'));
          for sphere in structured_entries.sphere_list:
              # variables
              centro = Vector(sphere.getLocation())

              # initialise rotation_matrix
              rotation_matrix = Matrix()
              rotation_matrix.identity();

              # scale object
              #Sx=Blender.Mathutils.ScaleMatrix(abs(2*sphere.outer_radius),4,Blender.Mathutils.Vector(1,0,0))
              #Sy=Blender.Mathutils.ScaleMatrix(abs(2*sphere.outer_radius),4,Blender.Mathutils.Vector(0,1,0))
              #Sz=Blender.Mathutils.ScaleMatrix(abs(2*sphere.outer_radius),4,Blender.Mathutils.Vector(0,0,1))
              #rotation_matrix *= Sx*Sy*Sz;

              # position object
              #T = Blender.Mathutils.TranslationMatrix(centro)
              #rotation_matrix *= T;

              # add rotations
              #for r in sphere.rotation_list:
                #rotation_matrix *= rotationMatrix(r.axis_point, r.axis_direction, r.angle_degrees);

              # create object
              obj = FDTDGeometryObjects_obj.GEOsphere(sphere.name, sphere.getLocation(), sphere.outer_radius, sphere.inner_radius, sphere.permittivity, sphere.conductivity)
              #FDTDGeometryObjects_obj.GEOsphere_matrix(sphere.name, rotation_matrix, sphere.outer_radius, sphere.inner_radius, sphere.permittivity, sphere.conductivity);
              #FDTDGeometryObjects_obj.GEOblock_matrix(sphere.name, rotation_matrix, sphere.permittivity, sphere.conductivity);
              blender_utilities.setActiveObject(obj, context=bpy.context)
              blender_utilities.setCollections(obj, [collection_spheres], context=bpy.context)

          if self.import_blocks:
            # Block
            #Blender.Window.SetActiveLayer(1<<layerManager.DefaultLayers.index('blocks'))
            for block in structured_entries.block_list:
                # variables
                lower = Vector(block.getLowerAbsolute())
                upper = Vector(block.getUpperAbsolute())
                pos = 0.5*(lower+upper)
                diag = 0.5*(upper-lower)

                # initialise rotation_matrix
                rotation_matrix = Matrix()
                rotation_matrix.identity()

                # add rotations
                for r in block.rotation_list:
                  rotation_matrix = rotationMatrix(r.axis_point, r.axis_direction, r.angle_degrees)*rotation_matrix

                # position object
                T = Matrix.Translation(pos)
                if bpy.app.version >= (2, 80, 0):
                  rotation_matrix @= T
                else:
                  rotation_matrix *= T

                ## scale object
                Sx = Matrix.Scale(abs(diag[0]), 4, Vector((1,0,0)) )
                Sy = Matrix.Scale(abs(diag[1]), 4, Vector((0,1,0)) )
                Sz = Matrix.Scale(abs(diag[2]), 4, Vector((0,0,1)) )
                if bpy.app.version >= (2, 80, 0):
                  rotation_matrix @= Sx@Sy@Sz
                else:
                  rotation_matrix *= Sx*Sy*Sz

                # create object
                obj = FDTDGeometryObjects_obj.GEOblock_matrix(block.name, rotation_matrix, block.permittivity, block.conductivity)
                #FDTDGeometryObjects_obj.GEOblock(block.name, block.lower, block.upper, block.permittivity, block.conductivity)
                blender_utilities.setActiveObject(obj, context=bpy.context)
                blender_utilities.setCollections(obj, [collection_blocks], context=bpy.context)

          # Distorted
          for distorted in structured_entries.distorted_list:
              # create object
              #print(distorted)
              obj = FDTDGeometryObjects_obj.GEOdistorted(distorted);
              blender_utilities.setActiveObject(obj, context=bpy.context)
              blender_utilities.setCollections(obj, [collection_distorted], context=bpy.context)

          #########################
          # Cylinders
          
          if self.import_cylinders:
            
            if self.cylinder_to_line_mesh:
              obj = createLineMeshFromCylinders(structured_entries)
              blender_utilities.setCollections(obj, [collection_cylinders], context=bpy.context)
            else:
              ## progress indicator does not work when running from CLI
              if self.GUI_loaded:
                bpy.context.window_manager.progress_begin(0, 100)

              #Blender.Window.SetActiveLayer(1<<layerManager.DefaultLayers.index('cylinders'));
              
              if self.restrict_import_volume:
                if self.volume_specification_style == 'relative':
                  import_volume_xmin = self.xmin * structured_entries.getSize()[0]
                  import_volume_xmax = self.xmax * structured_entries.getSize()[0]
                  import_volume_ymin = self.ymin * structured_entries.getSize()[1]
                  import_volume_ymax = self.ymax * structured_entries.getSize()[1]
                  import_volume_zmin = self.zmin * structured_entries.getSize()[2]
                  import_volume_zmax = self.zmax * structured_entries.getSize()[2]
                else:
                  import_volume_xmin = self.xmin
                  import_volume_xmax = self.xmax
                  import_volume_ymin = self.ymin
                  import_volume_ymax = self.ymax
                  import_volume_zmin = self.zmin
                  import_volume_zmax = self.zmax
                
                truncated_cylinder_list = truncateGeoList(structured_entries.cylinder_list, import_volume_xmin, import_volume_xmax, import_volume_ymin, import_volume_ymax, import_volume_zmin, import_volume_zmax)
                if self.verbosity > 0:
                  print(self)
                  print('len(structured_entries.cylinder_list) = {}'.format(len(structured_entries.cylinder_list)))
                  print('len(truncated_cylinder_list) = {}'.format(len(truncated_cylinder_list)))
              else:
                truncated_cylinder_list = structured_entries.cylinder_list
                
              if self.use_Nmax_objects:
                truncated_cylinder_list = truncated_cylinder_list[:self.Nmax_objects]
              
              # hack to create a lot of objects quickly using duplication.
              # .. todo:: replace/improve + implement for other objects
              # .. todo:: one mesh per material & .geo file, rather than multiple objects, while respecting appearance order, i.e. group sequences of same material objects into a single mesh.
              # cf:
              #   https://blender.stackexchange.com/questions/7358/python-performance-with-blender-operators
              #   https://blender.stackexchange.com/questions/39721/how-can-i-create-many-objects-quickly
              
              N = len(truncated_cylinder_list)
              if self.verbosity > 0:
                print('len(truncated_cylinder_list) = {}'.format(N))
              if N > 0:
                N_added_max = 500
                N_added = min(N_added_max, N)
                N_duplications = (N//N_added) - 1
                N_remainder = N%N_added

                print('N',N)
                print('N_added_max',N_added_max)
                print('N_added',N_added)
                print('N_duplications',N_duplications)
                print('N_remainder',N_remainder)
                print('total = '+str(N_added + N_duplications*N_added +  N_remainder))

                Nfill =  len(str(N))

                cyl_list = N*[0]

                # add all cylinders
                print('Adding all '+str(N)+' cylinders...')

                # normal add
                if self.GUI_loaded:
                  bpy.context.window_manager.progress_update(0)
                for i in range(N_added + N_remainder):
                  bpy.ops.mesh.primitive_cylinder_add(location = Vector([0,0,0]), rotation=(radians(-90),0,0))
                  bpy.ops.object.transform_apply(rotation=True) # aligning cylinder to Y axis directly and applying rotation, to follow BFDTD standard cylinder orientation.
                  cyl_list[i] = bpy.context.object
                  if self.GUI_loaded:
                    bpy.context.window_manager.progress_update(i/(N_added + N_remainder))

                ## select items to duplicate
                selectObjects(cyl_list[0:N_added])

                ## duplicate
                if self.GUI_loaded:
                  bpy.context.window_manager.progress_update(0)
                for i in range(N_duplications):
                  #'cyl.''{:0>-{Nfill}}'.format(i,Nfill=Nfill)
                  bpy.ops.object.duplicate_move_linked()
                  start_idx = N_added + N_remainder + i*N_added
                  end_idx = start_idx + N_added
                  print((start_idx,end_idx))
                  cyl_list[start_idx:end_idx] = bpy.context.selected_objects
                  if self.GUI_loaded:
                    bpy.context.window_manager.progress_update(i/N_duplications)

                # set location/rotation/scale of cylinders
                print('Setting location/rotation/scale of all '+str(N)+' cylinders...')
                #for i, cylinder in enumerate(truncated_cylinder_list):
                  #obj = cyl_list[i]

                if self.GUI_loaded:
                  bpy.context.window_manager.progress_update(0)
                for i, cylinder in enumerate(truncated_cylinder_list):
                #for cylinder in truncated_cylinder_list:

                  # initialise rotation_matrix
                  rotation_matrix = Matrix()
                  rotation_matrix.identity()

                  scale = [cylinder.outer_radius, cylinder.outer_radius, 0.5*cylinder.height]

                  Sx = Matrix.Scale(scale[0],4,[1,0,0])
                  Sy = Matrix.Scale(scale[1],4,[0,1,0])
                  Sz = Matrix.Scale(scale[2],4,[0,0,1])

                  #rotation_matrix *= Sx*Sy*Sz;

                  # add rotations
                  # TODO: Check it works correctly...
                  for r in cylinder.rotation_list:
                    rotation_matrix *= rotationMatrix(r.axis_point, r.axis_direction, r.angle_degrees)*rotation_matrix
                    
                  #r = cylinder.rotation_list[0]

                  # position object
                  T = Matrix.Translation(Vector([cylinder.location[0], cylinder.location[1], cylinder.location[2]]))
                  rotation_matrix *= T;

                  # because FDTD cylinders are aligned with the Y axis by default
                  #rotation_matrix *= rotationMatrix(Vector([0,0,0]), Vector([1,0,0]), -90)

                  # create object
                  #obj = FDTDGeometryObjects_obj.GEOcylinder_matrix(cylinder.name, rotation_matrix, cylinder.inner_radius, cylinder.outer_radius, cylinder.height, cylinder.permittivity, cylinder.conductivity)
                  #obj = cyl_list[i]
                  #GEOcylinder_matrix2(self, obj, name, rotation_matrix, inner_radius, outer_radius, height, permittivity, conductivity)
                  obj = FDTDGeometryObjects_obj.GEOcylinder_matrix2(cyl_list[i],cylinder.name, rotation_matrix, cylinder.inner_radius, cylinder.outer_radius, cylinder.height, cylinder.permittivity, cylinder.conductivity)
                  #obj = FDTDGeometryObjects_obj.GEOcylinder_matrix(cylinder.name, rotation_matrix, cylinder.inner_radius, cylinder.outer_radius, cylinder.height, cylinder.permittivity, cylinder.conductivity)
                  #obj = FDTDGeometryObjects_obj.GEOcylinder_passedObj(cyl_list[i], cylinder.name, r.axis_point, r.axis_direction, r.angle_degrees, inner_radius, outer_radius, height, permittivity, conductivity)

                  blender_utilities.setActiveObject(obj, context=bpy.context)
                  blender_utilities.setCollections(obj, [collection_cylinders], context=bpy.context)

                  #angle_X = numpy.deg2rad(-90)
                  #angle_X = -0.5*numpy.pi
                  #angle_Y = 0
                  #angle_Z = 0
                  #FDTDGeometryObjects_obj.GEOcylinder(cylinder.name, cylinder.centro, cylinder.inner_radius, cylinder.outer_radius, cylinder.height, cylinder.permittivity, cylinder.conductivity, angle_X, angle_Y, angle_Z)

                  if self.GUI_loaded:
                    bpy.context.window_manager.progress_update(i/N)
                  else:
                    print('progress = {}'.format(i/N))

                if self.GUI_loaded:
                  bpy.context.window_manager.progress_end()
            ######################### if N > 0: end
      ##################################################################


      #########################
      # Not yet implemented:
      # Flag
      # structured_entries.flag;
      # Boundaries
      # structured_entries.boundaries;
      #########################

      # TODO: Save the layer settings somewhere for reuse
      #scene = Blender.Scene.GetCurrent()
      scene = bpy.context.scene

      layersOn = [layerManager.DefaultLayers.index('spheres')+1,layerManager.DefaultLayers.index('blocks')+1,layerManager.DefaultLayers.index('cylinders')+1]
      print(layersOn)
      #layersOn = [1,2,3]
      #print layersOn
      #Blender.Scene.GetCurrent().setLayers(layersOn)

      #scene.update(0);
      #Blender.Window.RedrawAll();
      #Blender.Window.WaitCursor(0);
      #Blender.Scene.GetCurrent().setLayers([1,3,4,5,6,7,8,9,10]);
      print('...done')
      #print Blender.Get('scriptsdir')
      #Blender.Run(Blender.Get('scriptsdir')+'/layer_manager.py')
      #layer_manager_objects = layer_manager.LayerManagerObjects()
      #Draw.Register(layer_manager_objects.gui, layer_manager_objects.event, layer_manager_objects.button_event)

      #print '=========================='
      #print Blender.Window.GetScreens()
      #print Blender.Window.GetAreaID()
      #print Blender.Window.GetAreaSize()
      #print Blender.Text.Get()
      #print '=========================='
      #~ Blender.Window.FileSelector(algosomething, "Import Bristol FDTD file...");
      #~ Blender.Run('~/.blender/scripts/bfdtd_import.py')

      print ('Elapsed time: ',round(time.time()-start_time,4),'seconds')

###############################
# MAIN FUNCTION
###############################
def main():
  ''' MAIN FUNCTION '''
  print('sys.argv=' + str(sys.argv))
  print('len(sys.argv)=' + str(len(sys.argv)))

  parser = argparse.ArgumentParser()
  parser.add_argument("--Nmax", type=int, default=500, help='Maximum number of objects to import. If set to a negative value, all objects will be imported.')
  
  parser.add_argument("--restrict-import-volume", action='store_true')
  parser.add_argument("--centre", nargs=3, type=float, default=[0.5, 0.5, 0.5])
  parser.add_argument("--size", nargs=3, type=float, default=[1/10, 1/10, 1/10])
  
  parser.add_argument("--no-geometry", action='store_true')
  parser.add_argument("--skip-cylinders", action='store_true')
  parser.add_argument("--skip-blocks", action='store_true')
  parser.add_argument("--pre_2008_BFDTD_version", action='store_true')
  parser.add_argument('filename', nargs='+')
  args = parser.parse_args(sys.argv[4:])
  print(sys.argv[4:])
  print(args)

  importer = BristolFDTDimporter()
  importer.no_geometry = args.no_geometry
  importer.import_cylinders = not args.skip_cylinders
  importer.import_blocks = not args.skip_blocks
  importer.pre_2008_BFDTD_version = args.pre_2008_BFDTD_version
  if args.Nmax < 0:
    importer.use_Nmax_objects = False
  else:
    importer.use_Nmax_objects = True
    importer.Nmax_objects = args.Nmax

  importer.restrict_import_volume = args.restrict_import_volume
  importer.xmin = args.centre[0] - args.size[0]/2
  importer.xmax = args.centre[0] + args.size[0]/2
  importer.ymin = args.centre[1] - args.size[1]/2
  importer.ymax = args.centre[1] + args.size[1]/2
  importer.zmin = args.centre[2] - args.size[2]/2
  importer.zmax = args.centre[2] + args.size[2]/2

  importer.importBristolFDTD(args.filename)

  # arg[0]='blender'
  # arg[1]='-P'
  # arg[2]='scriptname'
  # arg[3]='--'

  #if len(sys.argv) > 4:

  #else:
    #raise Exception('Oops, sorry, it seems this is still used after all. :)')
    ####################
    ## load import path
    ####################
    ## print('tempdir=',Blender.Get('tempdir'))
    ## print('soundsdir=',Blender.Get('soundsdir'))

    ## default_path = Blender.Get('tempdir');
    ## if not default_path:
        ## default_path = os.getenv('DATADIR');

    #default_path = os.getenv('DATADIR')
    #print('cfgfile = ', cfgfile)

    #if os.path.isfile(cfgfile) and os.path.getsize(cfgfile) > 0:
        ##with open(, 'r') as FILE:
             ##= pickle.load(FILE);
      #with open(cfgfile, 'rb') as f:
        ## The protocol version used is detected automatically, so we do not
        ## have to specify it.
        #default_path = pickle.load(f)
    ####################

    ####################
    ## import file
    ####################
    #Blender.Window.FileSelector(importBristolFDTD, "Import Bristol FDTD file...", default_path);
    ## TestObjects();

def createLineMeshFromCylinders(BFDTDobject_obj):
  cylinder_list = BFDTDobject_obj.getGeometryObjectsByType(bfdtd.Cylinder)

  material_set = set()
  
  for cyl in cylinder_list:
    material_set.add((cyl.getRelativePermittivity(), cyl.getRelativeConductivity()))
  
  print(material_set)
  
  verts = []
  edges = []
  faces = []

  Nverts = 0
  for cyl in cylinder_list:
    a,b = cyl.getStartEndPoints()
    verts.append(a)
    verts.append(b)
    Nverts+=2
    edges.append( (Nverts-2, Nverts-1) )
  
  mesh = bpy.data.meshes.new(name="CylinderMesh")
  mesh.from_pydata(verts, edges, faces)
  # useful for development when the mesh may be invalid.
  # mesh.validate(verbose=True)
  object_data_add(bpy.context, mesh)
  obj = bpy.context.active_object
  
  return obj

if __name__ == "__main__":
  main()
