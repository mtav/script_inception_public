#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Module for use by Blender addons
'''

# To make Blender happy:
bl_info = {"name":"FDTDGeometryObjects - MODULE - NOT ADDON", "category": "Module", 'warning': 'MODULE - NOT ADDON'}

#import Blender
#~ from bpy import *
import math
import bpy
#import BPyAddMesh
import os
import sys
import re
import array
import numpy

import utilities

# define Vector+Matrix
#~ from bpy.Mathutils import Vector
#~ from bpy.Mathutils import Matrix
#from Blender.Mathutils import Vector
#from Blender.Mathutils import Matrix
#from mathutils import Color
import bmesh
from math import radians
from mathutils import *
from bpy_extras import object_utils #Blender 2.63
from blender_scripts.modules.blender_utilities import setOrigin, grid_index, Orthogonal, rotationMatrix
import bfdtd
import blender_scripts.modules.GeometryObjects as GeometryObjects
import blender_scripts.modules.bfdtd_import
# from blender_scripts.modules.bfdtd_import import createLineMeshFromCylinders
import blender_scripts.modules.blender_utilities as blender_utilities

from bpy_extras.object_utils import AddObjectHelper, object_data_add

def GEOmesh1D(name, coords, location=[0,0,0]):
  '''Creates a "1D mesh" from a given list of coordinates.'''
  verts = 2*len(coords)*[0]
  edges = len(coords)*[0]
  faces = []
  
  vert_idx = 0
  edge_idx = 0

  for x in coords:
    A = vert_idx
    verts[vert_idx] = Vector([x, 0, 0]); vert_idx+=1
    B = vert_idx
    verts[vert_idx] = Vector([x, 1, 0]); vert_idx+=1
    edges[edge_idx] = [A, B]; edge_idx+=1
  
  mesh_new = bpy.data.meshes.new(name=name)
  mesh_new.from_pydata(verts, edges, faces)
  object_utils.object_data_add(bpy.context, mesh_new)

  obj = bpy.context.active_object
  obj.name = name
  obj.location = Vector(location)

  return(blender_utilities.getActiveObject(bpy.context))

def GEOmesh1D_bmesh(name, coords, location=[0,0,0]):
  '''Creates a "1D mesh" from a given list of coordinates. (bmesh using version)'''
  mesh = bpy.data.meshes.new(name)
  bm = bmesh.new()
  for (idx, x) in enumerate(coords):
    bm.verts.new([x, 0, 0])
    bm.verts.new([x, 1, 0])
    bm.edges.new([bm.verts[2*idx], bm.verts[2*idx+1]])
  bm.to_mesh(mesh)
  mesh.update()
  object_utils.object_data_add(bpy.context, mesh)
  
  obj = bpy.context.active_object
  obj.name = name
  obj.location = Vector(location)
  return(obj)

def renderXMesh1D(name, coords, location=[0,0,0]):
  '''Creates a "1D mesh" from a given list of coordinates. (bmesh using version)'''
  mesh = bpy.data.meshes.new(name)
  bm = bmesh.new()
  for (idx, x) in enumerate(coords):
    bm.verts.new([x, 0, 0])
    bm.verts.new([x, 1, 0])
    bm.verts.new([x, 0, 1])
    bm.edges.new([bm.verts[3*idx], bm.verts[3*idx+1]])
    bm.edges.new([bm.verts[3*idx], bm.verts[3*idx+2]])
  bm.to_mesh(mesh)
  mesh.update()
  object_utils.object_data_add(bpy.context, mesh)
  
  obj = bpy.context.active_object
  obj.name = name
  obj.location = Vector(location)
  return(obj)

def renderYMesh1D(name, coords, location=[0,0,0]):
  '''Creates a "1D mesh" from a given list of coordinates. (bmesh using version)'''
  mesh = bpy.data.meshes.new(name)
  bm = bmesh.new()
  for (idx, y) in enumerate(coords):
    bm.verts.new([0, y, 0])
    bm.verts.new([1, y, 0])
    bm.verts.new([0, y, 1])
    bm.edges.new([bm.verts[3*idx], bm.verts[3*idx+1]])
    bm.edges.new([bm.verts[3*idx], bm.verts[3*idx+2]])
  bm.to_mesh(mesh)
  mesh.update()
  object_utils.object_data_add(bpy.context, mesh)
  
  obj = bpy.context.active_object
  obj.name = name
  obj.location = Vector(location)
  return(obj)


def renderZMesh1D(name, coords, location=[0,0,0]):
  '''Creates a "1D mesh" from a given list of coordinates. (bmesh using version)'''
  mesh = bpy.data.meshes.new(name)
  bm = bmesh.new()
  for (idx, z) in enumerate(coords):
    bm.verts.new([0, 0, z])
    bm.verts.new([1, 0, z])
    bm.verts.new([0, 1, z])
    bm.edges.new([bm.verts[3*idx], bm.verts[3*idx+1]])
    bm.edges.new([bm.verts[3*idx], bm.verts[3*idx+2]])
  bm.to_mesh(mesh)
  mesh.update()
  object_utils.object_data_add(bpy.context, mesh)
  
  obj = bpy.context.active_object
  obj.name = name
  obj.location = Vector(location)
  return(obj)

class FDTDGeometryObjects(object):
    def __init__(self):
      # prepare base materials
      self.material_dict = dict()
      self.updateMaterialDictionary()

      self.verbosity = 0

      # .. todo:: finish implementing this?
      #self.transparency_method='MASK'
      #self.transparency_method='RAYTRACE'
      #self.transparency_method='Z_TRANSPARENCY'
      
      self.frequency_snapshot_material = self.getCustomMaterial('frequency_snapshot', Color((0.5, 0, 0)), 0.5)
      self.time_snapshot_material      = self.getCustomMaterial('time_snapshot'     , Color((0.5, 1, 0)), 0.5)
      self.eps_snapshot_material       = self.getCustomMaterial('eps_snapshot'      , Color((0.5, 0, 1)), 0.5)
      self.excitation_material         = self.getCustomMaterial('excitation'        , Color((1.0, 0, 0)), 0.5)
      
      self.snapshot_materials = [ self.frequency_snapshot_material, self.time_snapshot_material, self.eps_snapshot_material ]
      
      self.probe_scalefactor_box = 0.0218
      self.probe_scalefactor_mesh = 0.5
      self.mesh_min = 0
      self.mesh_max = 0
      self.box_SizeX = 0
      self.box_SizeY = 0
      self.box_SizeZ = 0

      self.cylinders_as_single_line_mesh = True

    def addGeometryObjects(self, geo_list):
      print('--- addGeometryObjects ---')

      if self.cylinders_as_single_line_mesh:
        cylinder_list = []
        geo_list_without_cylinder = []
        for idx, obj in enumerate(geo_list):
          if isinstance(obj, bfdtd.Cylinder) and not isinstance(obj, bfdtd.Cone):
            cylinder_list.append(obj)
          else:
            geo_list_without_cylinder.append(obj)

        geo_list = geo_list_without_cylinder

        # self.addCylindersAsSingleLineMesh(cylinder_list)
        BFDTDobject_obj = bfdtd.BFDTDobject()
        print('len(cylinder_list) = {}'.format(len(cylinder_list)))
        # raise
        BFDTDobject_obj.setGeometryObjects(cylinder_list)
        blender_scripts.modules.bfdtd_import.createLineMeshFromCylinders(BFDTDobject_obj)

      for idx, obj in enumerate(geo_list):
        if self.verbosity > 0:
          print('====================')
          print('idx = {}'.format(idx))
          print('--------------------')
          print(obj)
          print('====================')
        
        if isinstance(obj, bfdtd.Sphere):
          self.GEOsphere(obj.getName(), obj.getLocation(), obj.getOuterRadius(), obj.getInnerRadius(), obj.getRelativePermittivity(), obj.getRelativeConductivity())
        elif isinstance(obj, bfdtd.Cylinder):
          if not isinstance(obj, bfdtd.Cone):
            start_point = obj.getLocation() - obj.getHeight()/2 * obj.getAxis()
            end_point = obj.getLocation() + obj.getHeight()/2 * obj.getAxis()
            print(numpy.linalg.norm(obj.getAxis()))
            print(start_point)
            print(end_point)
            print(type(obj.getOuterRadius()))
            GeometryObjects.add_cylinder(self, start_point, end_point, name=obj.getName(), cylinder_radius=obj.getOuterRadius())
          else:
            self.addCone(obj)
        elif isinstance(obj, bfdtd.Parallelepiped):
          if not isinstance(obj, bfdtd.Ellipsoid):
          #self.addParallelepiped(obj)
            self.GEOdistorted(obj)
          else:
            self.addEllipsoid(obj)
      
      return

    # def addCylindersAsSingleLineMesh(self, cylinder_list):
      # for idx, obj in enumerate(cylinder_list):
        # print('====================')
        # print('idx = {}'.format(idx))
        # print('--------------------')
        # print(obj)
        # print('====================')
        # a,b = obj.getStartEndPoints()
        # print(a,b)
        # raise
        
      # return
    
    def addEllipsoid(self, obj):
      # .. todo:: use UV sphere to make axes easier to see?
      self.GEOsphere(obj.getName(), obj.getLocation(), 1, 0, obj.getRelativePermittivity(), obj.getRelativeConductivity(), UVsphere=True)
      blender_obj = bpy.context.active_object
      
      e0, e1, e2 = obj.getAxes()
      s0, s1, s2 = obj.getSize()
      print(e0, e1, e2)
      print(s0, s1, s2)
      
      e0 = s0/2*utilities.common.unitVector(e0)
      e1 = s1/2*utilities.common.unitVector(e1)
      e2 = s2/2*utilities.common.unitVector(e2)
      
      for v in blender_obj.data.vertices:
        p = v.co.x*e0 + v.co.y*e1 + v.co.z*e2
        v.co = p
      #return
      
      #verts = []
      #edges = []
      #faces = []
      #segments = 32
      #rings = 16
      ##segments = 3
      ##rings = 3
      #for theta in numpy.linspace(0, numpy.pi, rings+1):
        #for phi_index in range(segments):
          #phi = phi_index*(2*numpy.pi/segments)
          ##numpy.linspace(0, 2*numpy.pi, segments):
          #xl = numpy.sin(theta)*numpy.cos(phi)
          #yl = numpy.sin(theta)*numpy.sin(phi)
          #zl = numpy.cos(theta)
          #v = xl*e0 + yl*e1 + zl*e2
          #verts.append(Vector(v))
      
      #mesh = bpy.data.meshes.new(name=obj.getName())
      #mesh.from_pydata(verts, edges, faces)
      ## useful for development when the mesh may be invalid.
      ##mesh.validate(verbose=True)
      ##object_data_add(bpy.context, mesh, operator=self)
      #object_data_add(bpy.context, mesh)
      
      ## set location
      #blender_obj = bpy.context.active_object
      #blender_obj.location = obj.getLocation()
      
      ## name object and mesh
      #blender_obj.name = obj.getName()
      #blender_obj.data.name = obj.getName() + '.mesh'
      
      ## remove doubles
      #bpy.ops.object.mode_set(mode='EDIT')
      #bpy.ops.mesh.select_mode(type='VERT', action='ENABLE')
      #bpy.ops.mesh.select_all(action='SELECT')
      #bpy.ops.mesh.remove_doubles()
      #bpy.ops.object.mode_set(mode='OBJECT')
      
      return
    
    def setCommonProperties(self, fdtd_obj, blender_obj):
      # define name and material
      blender_obj.name = fdtd_obj.getName()
      blender_obj.active_material = self.getMaterial(fdtd_obj.getRelativePermittivity(), fdtd_obj.getRelativeConductivity())
      blender_obj.show_transparent = True
      blender_obj.show_wire = True
      
      # define custom properties for future export
      #blender_obj['bfdtd_type'] = "{0}.{1}".format(fdtd_obj.__class__.__module__, fdtd_obj.__class__.__name__)
      blender_obj['bfdtd_type'] = type(fdtd_obj).__name__
      blender_obj['relative_permittivity'] = fdtd_obj.getRelativePermittivity()
      blender_obj['relative_conductivity'] = fdtd_obj.getRelativeConductivity()
      return
    
    def addCylinder(self, fdtd_cylinder):
      start_point, end_point = fdtd_cylinder.getStartEndPoints()
      blender_cylinder = GeometryObjects.add_cylinder(self, start_point, end_point, name=fdtd_cylinder.getName(), cylinder_radius=fdtd_cylinder.getOuterRadius())
      self.setCommonProperties(fdtd_cylinder, blender_cylinder)
      #self.GEOcylinder_matrix2(obj, name, rotation_matrix, inner_radius, outer_radius, height, permittivity, conductivity)
      return

    def addCone(self, obj):
      h = obj.getHeight()
      r1 = obj.getOuterRadius1()
      r2 = obj.getOuterRadius2()
      print(type(r1), r1)
      print(type(r2), r2)
      N = 32
      verts = []
      edges = []
      faces = []
      for i in range(N):
        theta = i*2*numpy.pi/N
        print(type(theta))
        print(theta)
        x1 = r1*numpy.cos(theta)
        y1 = r1*numpy.sin(theta)
        z1 = -h/2
        x2 = r2*numpy.cos(theta)
        y2 = r2*numpy.sin(theta)
        z2 = h/2
        verts.append(Vector((x1,y1,z1)))
        verts.append(Vector((x2,y2,z2)))
        if i < N-1:
          faces.append([2*i, 2*(i+1), 2*(i+1)+1, 2*i+1])
        else:
          faces.append([2*i, 0, 1, 2*i+1])
          
      faces.append([2*(N-1-i) for i in range(N)])
      faces.append([2*i+1 for i in range(N)])
      
      mesh = bpy.data.meshes.new(name=obj.getName())
      mesh.from_pydata(verts, edges, faces)
      # useful for development when the mesh may be invalid.
      mesh.validate(verbose=True)
      #object_data_add(bpy.context, mesh, operator=self)
      object_data_add(bpy.context, mesh)
      
      rotmat = GeometryObjects.getRotationMatrixFromAxis(obj.getAxis())
      
      # add cylinder
      #bpy.ops.mesh.primitive_cylinder_add(location = Vector(cylinder_center), radius=cylinder_radius, depth=cylinder_length, rotation=(0,0,0))
      blender_obj = bpy.context.active_object
      blender_obj.matrix_world = rotmat
      blender_obj.location = obj.getLocation()
      
      # name object and mesh
      blender_obj.name = obj.getName()
      blender_obj.data.name = obj.getName() + '.mesh'
      
      return

    #def addParallelepiped(self, obj):
      #verts = [Vector(i) for i in p.getVerticesRelative()]
      
      #scale_x = self.scale.x
      #scale_y = self.scale.y

      #verts = [Vector((-1 * scale_x, 1 * scale_y, 0)),
               #Vector((1 * scale_x, 1 * scale_y, 0)),
               #Vector((1 * scale_x, -1 * scale_y, 0)),
               #Vector((-1 * scale_x, -1 * scale_y, 0)),
              #]

      #edges = []
      #faces = [[0, 1, 2, 3]]

      #mesh = bpy.data.meshes.new(name="New Object Mesh")
      #mesh.from_pydata(verts, edges, faces)
      ## useful for development when the mesh may be invalid.
      ## mesh.validate(verbose=True)
      #object_data_add(context, mesh, operator=self)
      #pass

    def getCustomMaterial(self, name, diffuse_color, alpha):
      '''
      Creates a new material named "name", if it does not yet exist. Otherwise, it returns the already existing material.
      
      *diffuse_color* and *alpha* are set to the given values.
      '''
      if name in bpy.data.materials.keys():
        material = bpy.data.materials[name]
      else:
        material = bpy.data.materials.new(name)
        if bpy.app.version >= (2, 80, 0):
          material.diffuse_color[0] = diffuse_color[0] # red
          material.diffuse_color[1] = diffuse_color[1] # green
          material.diffuse_color[2] = diffuse_color[2] # blue
          material.diffuse_color[3] = alpha            # alpha
        else:
          material.diffuse_color = diffuse_color
          material.alpha = alpha
      return(material)
      
    def updateMaterialDictionary(self):
      '''Update the material dictionary, which is of the form {(permittivity, conductivity):bpy.types.Material}.'''
      self.material_dict.clear()
      for mat in bpy.data.materials:
        if 'permittivity' in mat.keys() and 'conductivity' in mat.keys():
          self.material_dict[ (mat['permittivity'], mat['conductivity']) ] = mat
      return(self.material_dict)

    def getMaterialColor(self, permittivity, conductivity, max_permittivity = 25.0):
      '''
      Return a Color based on the given permittivity and conductivity values.
      
      .. note:: Conductivity is currently ignored and permittivity capped to the [0, 25] range.
      '''
      p = permittivity
      if p < 0:
        p = 0
      if p > max_permittivity:
        p = max_permittivity
      return Color((0, p/max_permittivity, 1.0 - p/max_permittivity))

    def getMaterial(self, permittivity, conductivity):
      '''
      Return a material corresponding to the  (permittivity, conductivity) pair.
      If no corresponding material exists, it will be created first.
      
      .. todo:: We could add multiple materials to an object. One for permittivity and one for conductivity for example. This could make it easier to switch between a permittivity and a conductivity "view" for example.
      '''
      
      # This is just a simple hack to support non-isotropic permittivities.
      # .. todo:: support non-isotropic permittivities properly.
      if isinstance(permittivity, list):
        permittivity = numpy.mean(permittivity)
      
      if (permittivity, conductivity) not in self.material_dict.keys():
        mat_name = 'n_{:.2f}_p_{:.2f}_c{:.2f}'.format(numpy.sqrt(permittivity), permittivity, conductivity)
        diffuse_color = self.getMaterialColor(permittivity, conductivity)
        alpha = 0.5
        permittivity_material = self.getCustomMaterial(mat_name, diffuse_color, alpha)
        # permittivity_material = bpy.data.materials.new(mat_name)
        permittivity_material['permittivity'] = permittivity
        permittivity_material['conductivity'] = conductivity
        self.material_dict[(permittivity, conductivity)] = permittivity_material
    
      return self.material_dict[ (permittivity, conductivity) ]

    ###############################
    # OBJECT CREATION FUNCTIONS
    ###############################
    def GEOblock(self, name, lower, upper, permittivity, conductivity):

      lower = numpy.array(lower)
      upper = numpy.array(upper)

      # add cube
      bpy.ops.mesh.primitive_cube_add(location=(0,0,0),rotation=(0,0,0))
      
      # get added object
      obj = bpy.context.active_object
      
      #print(obj)
      #for obj in bpy.data.objects:
        #print(obj.name)
        
      #bpy.data.objects[-1].name = 'testkubo2'
      obj.name = name
      
      pos = 0.5*(lower+upper)
      diag = upper-lower
      obj.scale = 0.5*diag
      obj.location = pos
      
      # deleting faces fails when in object mode, so change.
      #bpy.ops.object.mode_set(mode = 'EDIT') 
      #bpy.ops.mesh.delete(type='ONLY_FACE')
      #bpy.ops.object.mode_set(mode = 'OBJECT')

      obj.show_transparent = True; obj.show_wire = True

      ######################################
      #Assign first material on all the mesh
      ######################################
      #Add a material slot
      bpy.ops.object.material_slot_add()
       
      #Assign a material to the last slot
      obj.material_slots[obj.material_slots.__len__() - 1].material = self.getMaterial(permittivity, conductivity)
       
      #Go to Edit mode
      bpy.ops.object.mode_set(mode='EDIT')
       
      #Select all the vertices
      bpy.ops.mesh.select_all(action='SELECT') 
       
      #Assign the material on all the vertices
      bpy.ops.object.material_slot_assign() 
       
      #Return to Object Mode
      bpy.ops.object.mode_set(mode='OBJECT')

      return(obj)

        #scene = Blender.Scene.GetCurrent()
        #mesh = Blender.Mesh.Primitives.Cube(1.0)
        #mesh.materials = self.getMaterial(permittivity, conductivity)
        #for f in mesh.faces:
            #f.mat = 0
    
        #obj = scene.objects.new(mesh, name)
        #pos = 0.5*(lower+upper)
        #diag = upper-lower
        #obj.SizeX = abs(diag[0])
        #obj.SizeY = abs(diag[1])
        #obj.SizeZ = abs(diag[2])
        #obj.setLocation(pos[0], pos[1], pos[2])
        #obj.transp = True; obj.wireMode = True
        #return
    
    def GEOblock_matrix(self, name, rotation_matrix, permittivity, conductivity):
      # add cube
      #bpy.ops.mesh.primitive_cube_add(location=(0,0,0),rotation=(45,45,0))
      bpy.ops.mesh.primitive_cube_add(location=(0,0,0),rotation=(0,0,0))
      
      # get added object
      obj = bpy.context.active_object
      
      #print(obj)
      #for obj in bpy.data.objects:
        #print(obj.name)
        
      #bpy.data.objects[-1].name = 'testkubo2'
      obj.name = name
      
      #pos = 0.5*(lower+upper)
      #diag = upper-lower
      #obj.scale = 0.5*diag
      #obj.location = pos
      
      # deleting faces fails when in object mode, so change.
      #bpy.ops.object.mode_set(mode = 'EDIT') 
      #bpy.ops.mesh.delete(type='ONLY_FACE')
      #bpy.ops.object.mode_set(mode = 'OBJECT')
      
      obj.show_transparent = True; obj.show_wire = True
      
      ######################################
      #Assign first material on all the mesh
      ######################################
      #Add a material slot
      bpy.ops.object.material_slot_add()
       
      #Assign a material to the last slot
      obj.material_slots[obj.material_slots.__len__() - 1].material = self.getMaterial(permittivity, conductivity)
       
      #Go to Edit mode
      bpy.ops.object.mode_set(mode='EDIT')
       
      #Select all the vertices
      bpy.ops.mesh.select_all(action='SELECT') 
       
      #Assign the material on all the vertices
      bpy.ops.object.material_slot_assign() 
       
      #Return to Object Mode
      bpy.ops.object.mode_set(mode='OBJECT')
      
      obj.matrix_world = rotation_matrix
      
      # define custom properties for future export
      obj['bfdtd_type'] = 'Block'
      obj['relative_permittivity'] = permittivity
      obj['relative_conductivity'] = conductivity
      
      return(obj)

        ##~ Blender.Window.SetActiveLayer(1<<8)
        #scene = Blender.Scene.GetCurrent()

        #~ Blender.Window.SetActiveLayer(1<<8)
        #scene = Blender.Scene.GetCurrent()
        #mesh = Blender.Mesh.Primitives.Cube(1.0)
        #mesh.materials = self.getMaterial(permittivity, conductivity)
        #for f in mesh.faces:
            #f.mat = 0
    
        #obj = scene.objects.new(mesh, name)
        #obj.setMatrix(rotation_matrix)
        #obj.transp = True; obj.wireMode = True
        ##~ obj.layers = [ 8 ]
        #return

    def GEOdistorted(self, obj):
        #scene = Blender.Scene.GetCurrent()
        
        #mesh = Blender.Mesh.Primitives.Cube(1.0)
        #mesh.materials = self.getMaterial(permittivity, conductivity)
        #for f in mesh.faces:
            #f.mat = 0
    
        #obj = scene.objects.new(mesh, name)

        #obj.setMatrix(rotation_matrix)
        #obj.transp = True; obj.wireMode = True
        ##~ obj.layers = [ 8 ]
        #return

        #pos = 0.5*(lower+upper)
        #diag = upper-lower
        #obj.SizeX = abs(diag[0])
        #obj.SizeY = abs(diag[1])
        #obj.SizeZ = abs(diag[2])
        #obj.setLocation(pos[0], pos[1], pos[2])
        #obj.transp = True; obj.wireMode = True

######################################################################################

        # variables
        #for i in range(8):
          #vertices[i] = Vector(distorted.vertices[i])
    
        #offset = 0
        #for i_object in range(0, Nobjects):
          #line = in_file.readline()
          #words = line.split()
          #Nverts = int(words[0])
          #Nfaces = int(words[1])
          #print "Nverts=",Nverts
          #print "Nfaces=",Nfaces
          
        vertices = obj.getVerticesRelative()
        local_verts = []
        for i_vert in range(len(vertices)):
          local_verts.append( Vector(vertices[i_vert]) )
          
        #print(local_verts)
        faces = []
        faces.append([3,2,1,0])
        faces.append([7,6,5,4])
        faces.append([0,1,6,7])
        faces.append([1,2,5,6])
        faces.append([2,3,4,5])
        faces.append([3,0,7,4])

          #for i_face in range(0, Nfaces):
                #line = in_file.readline()
                #words = line.split()
                #if len(words) < 3:
                  #Blender.Draw.PupMenu('Error%t|File format error 4')
                  #return
                #Nverts_in_face = int(words[0])
                #if len(words) != 1 + Nverts_in_face:
                  #Blender.Draw.PupMenu('Error%t|File format error 5')
                  #return
                #face_verts = []
                #for i_face_vert in range(0, Nverts_in_face):
                  #idx = int(words[i_face_vert + 1]) - offset
                  #face_verts.append(idx)
                ##print "face_verts=",face_verts
                #faces.append(face_verts)
          
        #print "Adding object ",object_names[i_object]
        
        edges = []
        
        #print('=========> adding mesh with name = '+str(name))
        mesh_data = bpy.data.meshes.new(obj.getName())
        mesh_data.from_pydata(local_verts, edges, faces)

        mesh_data.materials.append(self.getMaterial(obj.getRelativePermittivity(), obj.getRelativeConductivity() ))

        mesh_data.update() # (calc_edges=True) not needed here
        
        new_object = bpy.data.objects.new(obj.getName(), mesh_data)
        new_object.show_transparent = True; new_object.show_wire = True
        new_object.location = obj.getLocation()

        scene = bpy.context.scene
        scene.objects.link(new_object)
        
        #cube_object.select = True
        
        #BPyAddMesh.add_mesh_simple(name, , [], faces)

        #obj = Blender.Object.GetSelected()[0]
        #obj.transp = True; obj.wireMode = True
        #objmesh = obj.getData(mesh=True)
        #objmesh.materials = self.getMaterial(permittivity, conductivity)
        #for f in objmesh.faces:
          #f.mat = 0

######################################################################################


        return(new_object)
    
    def GEOcylinder(self, name, center, inner_radius, outer_radius, height, permittivity, conductivity, angle_X, angle_Y, angle_Z):
        bpy.ops.mesh.primitive_cylinder_add(location = Vector(center), radius=outer_radius, depth=height, rotation=(angle_X, angle_Y, angle_Z))
        obj = bpy.context.active_object
        obj.name = name
        #obj.scale = Vector([outer_radius])
        #obj.location = Vector(center)
        
        # deleting faces fails when in object mode, so change.
        #bpy.ops.object.mode_set(mode = 'EDIT') 
        #bpy.ops.mesh.delete(type='ONLY_FACE')
        #bpy.ops.object.mode_set(mode = 'OBJECT')
  
        obj.show_transparent = True; obj.show_wire = True
  
        ######################################
        #Assign first material on all the mesh
        ######################################
        #Add a material slot
        bpy.ops.object.material_slot_add()
        
        #Assign a material to the last slot
        obj.material_slots[obj.material_slots.__len__() - 1].material = self.getMaterial(permittivity, conductivity)
        
        #Go to Edit mode
        bpy.ops.object.mode_set(mode='EDIT')
        
        #Select all the vertices
        bpy.ops.mesh.select_all(action='SELECT') 
        
        #Assign the material on all the vertices
        bpy.ops.object.material_slot_assign() 
        
        #Return to Object Mode
        bpy.ops.object.mode_set(mode='OBJECT')

        #scene = Blender.Scene.GetCurrent()
        #mesh = Blender.Mesh.Primitives.Cylinder(32, 2*outer_radius, H)
        #mesh.materials = self.getMaterial(permittivity, conductivity)
        #for f in mesh.faces:
            #f.mat = 0
    
        #obj = scene.objects.new(mesh, name)
        #obj.setLocation(center[0], center[1], center[2])
        #obj.RotX = angle_X
        #obj.RotY = angle_Y
        #obj.RotZ = angle_Z
        #obj.transp = True; obj.wireMode = True
        return(obj)
    
    # TODO: Create a tube primitive to really support inner radius
    # TODO: sanitize rotation/import system, cleanup, etc
    def GEOcylinder_matrix(self, name, rotation_matrix, inner_radius, outer_radius, height, permittivity, conductivity):
        # passing the radius+depth directly will apply them directly, leading to an object of scale (1,1,1). So no need to add scaling to the rotation_matrix.
        
        bpy.ops.mesh.primitive_cylinder_add(location = Vector([0,0,0]), radius=outer_radius, depth=height, rotation=(radians(-90),0,0))
        bpy.ops.object.transform_apply(rotation=True) # aligning cylinder to Y axis directly and applying rotation, to follow BFDTD standard cylinder orientation.
        
        obj = bpy.context.active_object
        obj.name = name
        obj.active_material = self.getMaterial(permittivity, conductivity)
        obj.show_transparent = True; obj.show_wire = True
        obj.matrix_world = rotation_matrix
        return(obj)
    
    def GEOcylinder_matrix2(self, obj, name, rotation_matrix, inner_radius, outer_radius, height, permittivity, conductivity):
        # passing the radius+depth directly will apply them directly, leading to an object of scale (1,1,1). So no need to add scaling to the rotation_matrix.
        obj.name = name
        obj.active_material = self.getMaterial(permittivity, conductivity)
        obj.show_transparent = True; obj.show_wire = True
        obj.matrix_world = rotation_matrix
        
        scale = [outer_radius, 0.5*height, outer_radius]
        
        Sx = Matrix.Scale(scale[0],4,[1,0,0])
        Sy = Matrix.Scale(scale[1],4,[0,1,0])
        Sz = Matrix.Scale(scale[2],4,[0,0,1])
        obj.matrix_world *= Sx*Sy*Sz
        
        #rotation_matrix *= Sx*Sy*Sz;
        
        
        # TODO: Fix cylinder size!!!
        #obj.scale = [2*outer_radius,2*outer_radius,height]
        
        # define custom properties for future export
        obj['bfdtd_type'] = 'Cylinder'
        obj['relative_permittivity'] = permittivity
        obj['relative_conductivity'] = conductivity
        
        return(obj)
    
    def GEOcylinder_passedObj(self, obj, name, axis_point, axis_direction, angle_degrees, inner_radius, outer_radius, height, permittivity, conductivity):
          #scale = [cylinder.outer_radius, cylinder.outer_radius, 0.5*cylinder.height]
          
          #Sx = Matrix.Scale(scale[0],4,[1,0,0])
          #Sy = Matrix.Scale(scale[1],4,[0,1,0])
          #Sz = Matrix.Scale(scale[2],4,[0,0,1])

          ##rotation_matrix *= Sx*Sy*Sz;

          ## add rotations
          ## TODO: Check it works correctly...
          #for r in cylinder.rotation_list:
            #rotation_matrix *= rotationMatrix(r.axis_point, r.axis_direction, r.angle_degrees)*rotation_matrix

          ## position object
          #T = Matrix.Translation(Vector([cylinder.centro[0],cylinder.centro[1],cylinder.centro[2]]))
          #rotation_matrix *= T;
        return(obj)
    
    def GEOsphere(self, name, center, outer_radius, inner_radius, permittivity, conductivity, UVsphere=False):
        if UVsphere:
          bpy.ops.mesh.primitive_uv_sphere_add()
        else:
          bpy.ops.mesh.primitive_ico_sphere_add()

        obj = bpy.context.active_object
        obj.name = name
        obj.scale = Vector(3*[outer_radius])
        obj.location = Vector(list(center))
        
        # deleting faces fails when in object mode, so change.
        #bpy.ops.object.mode_set(mode = 'EDIT') 
        #bpy.ops.mesh.delete(type='ONLY_FACE')
        #bpy.ops.object.mode_set(mode = 'OBJECT')
  
        obj.show_transparent = True; obj.show_wire = True
  
        ######################################
        #Assign first material on all the mesh
        ######################################
        if self:
          #Add a material slot
          bpy.ops.object.material_slot_add()
          
          #Assign a material to the last slot
          obj.material_slots[obj.material_slots.__len__() - 1].material = self.getMaterial(permittivity, conductivity)
        
        #Go to Edit mode
        bpy.ops.object.mode_set(mode='EDIT')
        
        #Select all the vertices
        bpy.ops.mesh.select_all(action='SELECT') 
        
        #Assign the material on all the vertices
        bpy.ops.object.material_slot_assign()
        
        #Return to Object Mode
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # define custom properties for future export
        obj['bfdtd_type'] = 'Sphere'
        obj['relative_permittivity'] = permittivity
        obj['relative_conductivity'] = conductivity
        obj['outer_radius'] = outer_radius
        obj['location'] = center
        
        return(obj)
    
    def GEOsphere_matrix(self, name, rotation_matrix, outer_radius, inner_radius, permittivity, conductivity):
      # TODO?
      return
          
    def GEObox(self, name, lower, upper):
      # add cube
      bpy.ops.mesh.primitive_cube_add(location=(0,0,0),rotation=(0,0,0))
    
      # get added object
      obj = bpy.context.active_object
      #print(obj)
      #for obj in bpy.data.objects:
        #print(obj.name)
        
      #bpy.data.objects[-1].name = 'testkubo2'
      obj.name = name

      pos = 0.5*(lower+upper)
      diag = upper-lower
      obj.scale = 0.5*diag
      obj.location = pos
      
      # deleting faces fails when in object mode, so change.
      bpy.ops.object.mode_set(mode = 'EDIT') 
      bpy.ops.mesh.delete(type='ONLY_FACE')
      bpy.ops.object.mode_set(mode = 'OBJECT')

      obj.show_transparent = True; obj.show_wire = True
  
      return(obj)

        #scene = bpy.context.scene; Blender.Scene.GetCurrent()
        #bpy.ops.mesh.primitive_cube_add(location=(0,0,0),rotation=(0,0,0))
        #mesh = 
        #bpy.data
        #bpy.context
        #obj = bpy.context.active_object
        #obj.name = name
        #mesh = bpy.data.meshes[obj.name]

        #obj.location = 0.5 * (max_co + min_co) + Vector((0.0, 0.0, 1.0))
        #obj.scale = 0.5 * (max_co - min_co) + Vector((1.0, 1.0, 2.0))

        #mesh = Blender.Mesh.Primitives.Cube(1.0)
        #mesh.faces.delete(0, list(range(len(mesh.faces))))
        #bpy.ops.mesh.delete(type='ONLY_FACE')
    
        #toto = bpy.data.meshes["Cube.004"].faces[0]
    
        #obj.data.faces
    
        #obj = scene.objects.new(mesh, name)
        #pos = 0.5*(lower+upper)
        #diag = upper-lower
        
        #~ global box_SizeX
        #~ global box_SizeY
        #~ global box_SizeZ
        #self.box_SizeX = abs(diag[0])
        #self.box_SizeY = abs(diag[1])
        #self.box_SizeZ = abs(diag[2])
        #print(("box_SizeX = ", self.box_SizeX))
        #print(("box_SizeY = ", self.box_SizeY))
        #print(("box_SizeZ = ", self.box_SizeZ))
        
        #obj.SizeX = self.box_SizeX
        #obj.SizeY = self.box_SizeY
        #obj.SizeZ = self.box_SizeZ
        
        #obj.setLocation(pos[0], pos[1], pos[2])
        #obj.transp = True; obj.wireMode = True
    
        #return
        
    def GEOmesh(self, name, full_mesh, delta_X_vector, delta_Y_vector, delta_Z_vector):
        '''Creates a mesh from "delta vectors" (thickness lists).
        
        Options:
        
          * full_mesh: If true, inner lines will be added to the mesh. Otherwise, only lines on the "faces of the meshbox" will be drawn.
        '''
        if len(delta_X_vector)<=0 or len(delta_Y_vector)<=0 or len(delta_Z_vector)<=0:
          return
        
        Nx = len(delta_X_vector)+1
        Ny = len(delta_Y_vector)+1
        Nz = len(delta_Z_vector)+1
        xmax = sum(delta_X_vector)
        ymax = sum(delta_Y_vector)
        zmax = sum(delta_Z_vector)
        
        self.mesh_min = min(min(delta_X_vector), min(delta_Y_vector), min(delta_Z_vector))
        self.mesh_max = max(max(delta_X_vector), max(delta_Y_vector), max(delta_Z_vector))
        print( ('X: min = ', min(delta_X_vector), ' average = ', float(sum(delta_X_vector)) / len(delta_X_vector)) )
        print( ('Y: min = ', min(delta_Y_vector), ' average = ', float(sum(delta_Y_vector)) / len(delta_Y_vector)) )
        print( ('Z: min = ', min(delta_Z_vector), ' average = ', float(sum(delta_Z_vector)) / len(delta_Z_vector)) )
        
        # print("len(delta_X_vector) = ", len(delta_X_vector))
        # print("len(delta_Y_vector) = ", len(delta_Y_vector))
        # print("len(delta_Z_vector) = ", len(delta_Z_vector))
        # print("len(delta_vector) = ", len(delta_vector))
        #~ global mesh_min
        #~ global mesh_max
        #delta_vector = delta_X_vector + delta_Y_vector + delta_Z_vector
        #self.mesh_min = min(delta_vector)
        #self.mesh_max = max(delta_vector)
        print("self.mesh_min = ", self.mesh_min)
        print("self.mesh_max = ", self.mesh_max)
        
        # verts = array.array('d',range())
        # verts = range(Nx*Ny*Nz)
        verts = []
        edges = []
        faces = []
    
        if full_mesh:
            verts = list(range(2*(Nx*Ny + Ny*Nz + Nz*Nx)))
            edges = list(range(Nx*Ny + Ny*Nz + Nz*Nx))
            faces = []
            
            vert_idx = 0
            edge_idx = 0
            # Z edges
            x = 0
            for i in range(Nx):
                if i>0:
                    x+=delta_X_vector[i-1]
                y = 0
                for j in range(Ny):
                    if j>0:
                        y+=delta_Y_vector[j-1]
                    A = vert_idx
                    verts[vert_idx] = Vector([x, y, 0]); vert_idx+=1
                    B = vert_idx
                    verts[vert_idx] = Vector([x, y, zmax]); vert_idx+=1
                    edges[edge_idx] = [A, B]; edge_idx+=1
    
            # X edges
            y = 0
            for j in range(Ny):
                if j>0:
                    y+=delta_Y_vector[j-1]
                z = 0
                for k in range(Nz):
                    if k>0:
                        z+=delta_Z_vector[k-1]
                    A = vert_idx
                    verts[vert_idx] = Vector([0, y, z]); vert_idx+=1
                    B = vert_idx
                    verts[vert_idx] = Vector([xmax, y, z]); vert_idx+=1
                    edges[edge_idx] = [A, B]; edge_idx+=1
    
            # Y edges
            z = 0
            for k in range(Nz):
                if k>0:
                    z+=delta_Z_vector[k-1]
                x = 0
                for i in range(Nx):
                    if i>0:
                        x+=delta_X_vector[i-1]
                    A = vert_idx
                    verts[vert_idx] = Vector([x, 0, z]); vert_idx+=1
                    B = vert_idx
                    verts[vert_idx] = Vector([x, ymax, z]); vert_idx+=1
                    edges[edge_idx] = [A, B]; edge_idx+=1
        
        else:
            verts = list(range(4*(Nx + Ny + Nz)))
            edges = list(range(4*(Nx + Ny + Nz)))
            faces = []
            
            vert_idx = 0
            edge_idx = 0
            
            # X edges
            x = 0
            for i in range(Nx):
                if i>0:
                    x+=delta_X_vector[i-1]
                A = vert_idx; verts[vert_idx] = Vector([x, 0,    0   ]); vert_idx+=1
                B = vert_idx; verts[vert_idx] = Vector([x, ymax, 0   ]); vert_idx+=1
                C = vert_idx; verts[vert_idx] = Vector([x, ymax, zmax]); vert_idx+=1
                D = vert_idx; verts[vert_idx] = Vector([x, 0,    zmax]); vert_idx+=1
                edges[edge_idx] = [A, B]; edge_idx+=1
                edges[edge_idx] = [B, C]; edge_idx+=1
                edges[edge_idx] = [C, D]; edge_idx+=1
                edges[edge_idx] = [D, A]; edge_idx+=1
                
            # Y edges
            y = 0
            for j in range(Ny):
                if j>0:
                    y+=delta_Y_vector[j-1]
                A = vert_idx; verts[vert_idx] = Vector([0,    y, 0   ]); vert_idx+=1
                B = vert_idx; verts[vert_idx] = Vector([xmax, y, 0   ]); vert_idx+=1
                C = vert_idx; verts[vert_idx] = Vector([xmax, y, zmax]); vert_idx+=1
                D = vert_idx; verts[vert_idx] = Vector([0,    y, zmax]); vert_idx+=1
                edges[edge_idx] = [A, B]; edge_idx+=1
                edges[edge_idx] = [B, C]; edge_idx+=1
                edges[edge_idx] = [C, D]; edge_idx+=1
                edges[edge_idx] = [D, A]; edge_idx+=1
    
            # Z edges
            z = 0
            for k in range(Nz):
                if k>0:
                    z+=delta_Z_vector[k-1]
                A = vert_idx; verts[vert_idx] = Vector([0,    0,    z]); vert_idx+=1
                B = vert_idx; verts[vert_idx] = Vector([xmax, 0,    z]); vert_idx+=1
                C = vert_idx; verts[vert_idx] = Vector([xmax, ymax, z]); vert_idx+=1
                D = vert_idx; verts[vert_idx] = Vector([0,    ymax, z]); vert_idx+=1
                edges[edge_idx] = [A, B]; edge_idx+=1
                edges[edge_idx] = [B, C]; edge_idx+=1
                edges[edge_idx] = [C, D]; edge_idx+=1
                edges[edge_idx] = [D, A]; edge_idx+=1
                
        # print(verts)
        mesh_new = bpy.data.meshes.new(name=name)
        mesh_new.from_pydata(verts, edges, faces)
        object_utils.object_data_add(bpy.context, mesh_new)

        #BPyAddMesh.add_mesh_simple(name, verts, edges, faces)
        #~ bpy.data.meshes.new("Torus")
        
        #obj = Blender.Object.GetSelected()[0]
        # obj.layers = [ 2 ]
        # print('Nverts=', len(verts))
        # print('Nverts=', Nx*Ny*Nz)
    
        # print('Nedges=', len(edges))
        # print('Nedges=', Nx*Ny + Ny*Nz + Nz*Nx)
    
        return(blender_utilities.getActiveObject(bpy.context))
        
    #def GEOexcitation(self, name, P1, P2):
    def GEOexcitation(self, excitation):
        name = excitation.name
        P1 = Vector(excitation.P1)
        P2 = Vector(excitation.P2)
        
        if excitation.current_source != 11:
          print('template excitation')
        else:
          print('normal excitation')
      
        #scene = Blender.Scene.GetCurrent()

        # arrow dimensions:
        arrow_length = (P2-P1).length
        cone_length = arrow_length/5.0
        cylinder_length = 4*cone_length
        cone_radius = arrow_length/20.0
        cylinder_radius = cone_radius/2.0
        cylinder_center = P1+2./5.*(P2-P1)
        cone_center = P1+4.5/5.*(P2-P1)
            
        axisZ = (P2-P1); # because the default primitive cone is oriented along -Z, unlike the one imported from Blender UI...
        axisX = Orthogonal(axisZ)
        axisY = axisZ.cross(axisX)
        axisX.normalize()
        axisY.normalize()
        axisZ.normalize()
        
        axisX.resize_4d();axisX[3]=0
        axisY.resize_4d();axisX[3]=0
        axisZ.resize_4d();axisX[3]=0
        axisW=Vector((0,0,0,1))
        rotmat = Matrix((axisX,axisY,axisZ,axisW))
        rotmat.transpose()
        
        angle_X = angle_Y = angle_Z = 0
        bpy.ops.mesh.primitive_cylinder_add(location = Vector(cylinder_center), radius=cylinder_radius, depth=cylinder_length, rotation=(angle_X, angle_Y, angle_Z))
        arrow_cylinder_obj = bpy.context.active_object
        arrow_cylinder_obj.name = name

        arrow_cylinder_obj.matrix_world = rotmat
        #arrow_cylinder_obj.dimensions = (2*cylinder_radius,2*cylinder_radius,cylinder_length)
        arrow_cylinder_obj.location = cylinder_center

        bpy.ops.mesh.primitive_cone_add(radius1=cone_radius, depth=cone_length, location=Vector(cone_center), rotation=(0.0, 0.0, 0.0))
        arrow_cone_obj = bpy.context.active_object
        arrow_cone_obj.name = name

        arrow_cone_obj.matrix_world = rotmat
        #arrow_cylinder_obj.dimensions = (2*cylinder_radius,2*cylinder_radius,cylinder_length)
        arrow_cone_obj.location = cone_center

        bpy.ops.object.select_all(action = 'DESELECT')
        scene = bpy.context.scene
        scene.objects.active = arrow_cylinder_obj
        
        arrow_cylinder_obj.select = True
        arrow_cone_obj.select = True
        bpy.ops.object.join()

        
        #scene = Blender.Scene.GetCurrent()
        
        #mesh = Blender.Mesh.Primitives.Cylinder(32, 2*cylinder_radius, cylinder_length)
        #mesh.materials = [ self.excitation_material ]
        #arrow_cylinder_obj.data.materials = [self.excitation_material]
        #obj.active_material=bpy.data.materials['Red']
        arrow_cylinder_obj.active_material = self.excitation_material
        #for f in mesh.faces:
            #f.mat = 0
    
        #arrow_cylinder_obj = scene.objects.new(mesh, name)
        #arrow_cylinder_obj.setMatrix(rotmat)
        #arrow_cylinder_obj.setLocation(cylinder_center[0], cylinder_center[1], cylinder_center[2])
    
        #mesh = Blender.Mesh.Primitives.Cone(32, 2*cone_radius, cone_length)
        #mesh.materials = [ self.excitation_material ]
        #for f in mesh.faces:
            #f.mat = 0
    
        #arrow_cone_obj = scene.objects.new(mesh, name)
        #arrow_cone_obj.setMatrix(rotmat)
    
        #arrow_cone_obj.setLocation(cone_center[0], cone_center[1], cone_center[2])
    
        #arrow_cylinder_obj.join([arrow_cone_obj])
        # arrow_cylinder_obj.layers = [ 5 ]
        #arrow_cylinder_obj.transp = True; arrow_cylinder_obj.wireMode = True
    
        #scene.objects.unlink(arrow_cone_obj)
        
        # set origin of created arrow object to 0.5*(P1+P2)
        setOrigin(arrow_cylinder_obj, 0.5*(P1+P2))        
        
        return(arrow_cylinder_obj)
    
    def snapshot(self, name, plane, P1, P2, snapshot_type):
        
        P1 = Vector(P1)
        P2 = Vector(P2)
        
        centro = 0.5*(P1+P2)
        
        verts = []
        if plane.lower() == 'x':
            #X
            A = Vector([0.5*(P1[0]+P2[0]), P1[1], P1[2]]) - centro
            B = Vector([0.5*(P1[0]+P2[0]), P2[1], P1[2]]) - centro
            C = Vector([0.5*(P1[0]+P2[0]), P2[1], P2[2]]) - centro
            D = Vector([0.5*(P1[0]+P2[0]), P1[1], P2[2]]) - centro
            verts = [ A, B, C, D ]
        elif plane.lower() == 'y':
            #Y
            A = Vector([P1[0], 0.5*(P1[1]+P2[1]), P1[2]]) - centro
            B = Vector([P1[0], 0.5*(P1[1]+P2[1]), P2[2]]) - centro
            C = Vector([P2[0], 0.5*(P1[1]+P2[1]), P2[2]]) - centro
            D = Vector([P2[0], 0.5*(P1[1]+P2[1]), P1[2]]) - centro
            verts = [ A, B, C, D ]
        else:
            #Z
            A = Vector([P1[0], P1[1], 0.5*(P1[2]+P2[2])]) - centro
            B = Vector([P2[0], P1[1], 0.5*(P1[2]+P2[2])]) - centro
            C = Vector([P2[0], P2[1], 0.5*(P1[2]+P2[2])]) - centro
            D = Vector([P1[0], P2[1], 0.5*(P1[2]+P2[2])]) - centro
            verts = [ A, B, C, D ]
        
        verts = verts
        edges = []
        faces = [( 0, 1, 2, 3 )]
        #name = 'snapshot'
        #if snapshot_type == 0:
            #name = 'freq_snapshot'
        #elif snapshot_type == 1:
            #name = 'time_snapshot'
        #else:
            #name = 'eps_snapshot'
        
        # print("Adding plane at ", A, B, C, D)

        #mesh_new = bpy.data.meshes.new(name=name)
        #mesh_new.from_pydata(verts, edges, faces)
        #object_utils.object_data_add(bpy.context, mesh_new)

        mesh_data = bpy.data.meshes.new(name=name)
        mesh_data.from_pydata(verts, edges, faces)
        mesh_data.update() # (calc_edges=True) not needed here
        
        new_object = bpy.data.objects.new(name, mesh_data)
        
        scene = bpy.context.scene
        scene.objects.link(new_object)
        
        if self.verbosity > 0:
          print('==> snapshot_type = '+str(snapshot_type))
          print(self.snapshot_materials)
        new_object.active_material = self.snapshot_materials[snapshot_type]

        new_object.show_wire = True
        new_object.show_transparent = True
        
        new_object.location = centro

        #BPyAddMesh.add_mesh_simple(name, verts, edges, faces)
        #obj = Blender.Object.GetSelected()[0]
        ## obj.layers = [ 3 ]
        #obj.transp = True; obj.wireMode = True
        
        #mesh = Blender.Mesh.Get( obj.data.name )
        #mesh.materials = self.snapshot_materials
        #for f in mesh.faces:
            #f.mat = snapshot_type
        
        # set origin to geometry (would be better to set it via the mesh, but this is easier and less bug prone)
        # fails for some reason. :(
        # .. todo:: Figure out why.
        #bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        
        return(new_object)
    
    def GEOfrequency_snapshot(self, name, plane, P1, P2):
      return self.snapshot(name, plane, P1, P2, 0)
       
    def GEOtime_snapshot(self, name, plane, P1, P2):
      return self.snapshot(name, plane, P1, P2, 1)
    
    def GEOeps_snapshot(self, name, plane, P1, P2):
      return self.snapshot(name, plane, P1, P2, 2)
    
    def GEOprobe(self, name, position):
      #scene = Blender.Scene.GetCurrent()

      #~ probe_size = probe_scalefactor_box*max(box_SizeX,box_SizeY,box_SizeZ)
      probe_size = self.probe_scalefactor_mesh*self.mesh_min
      if probe_size<=0:
        probe_size = self.probe_scalefactor_box*max(self.box_SizeX,self.box_SizeY,self.box_SizeZ)
      if probe_size<=0:
        probe_size = 1
      print('self.probe_scalefactor_mesh = ' + str(self.probe_scalefactor_mesh))
      print('self.mesh_min = ' + str(self.mesh_min))
      print('probe_size = ' + str(probe_size))
      # TODO: define probe_size relative to smallest part of geometry + add way to change it in blender eventually
      # print("probe_size = ", probe_scalefactor_box,"*max(",box_SizeX,",",box_SizeY,",",box_SizeZ,")=", probe_scalefactor_box,"*",max(box_SizeX,box_SizeY,box_SizeZ),"=", probe_size)

      # add cube
      bpy.ops.mesh.primitive_cube_add(location=Vector(position),rotation=(0,0,0))

      # get added object
      obj = bpy.context.active_object

      #print(obj)
      #for obj in bpy.data.objects:
        #print(obj.name)
        
      #bpy.data.objects[-1].name = 'testkubo2'
      obj.name = name

      obj.dimensions = 3*[probe_size]

      # deleting faces fails when in object mode, so change.
      #bpy.ops.object.mode_set(mode = 'EDIT') 
      #bpy.ops.mesh.delete(type='ONLY_FACE')
      #bpy.ops.object.mode_set(mode = 'OBJECT')

      obj.show_transparent = True; obj.show_wire = True
      return(obj)

###############################
# TEST FUNCTIONS
###############################
def TestObjects():
    ''' test objects '''
    Blender.Window.SetActiveLayer(1<<0)
    GEOmesh(False, [1, 1], [1, 2, 3], [4, 3, 2, 1])
    
    Blender.Window.SetActiveLayer(1<<1)
    #GEOexcitation(Vector(0,0,0), Vector(1,0,0))
    #GEOexcitation(Vector(0,0,0), Vector(0,1,0))
    #GEOexcitation(Vector(0,0,0), Vector(0,0,1))

    #GEOexcitation(Vector(1,0,0), Vector(2,0,0))
    #GEOexcitation(Vector(0,1,0), Vector(0,2,0))
    #GEOexcitation(Vector(0,0,1), Vector(0,0,2))

    #GEOexcitation(Vector(0,0,0), Vector(1,1,1))
    #GEOexcitation(Vector(1,1,1), Vector(2,2,2))
    #GEOexcitation(Vector(2,2,2), Vector(3,3,3))

    #GEOexcitation(Vector(1,1,1), Vector(2,1,2))
    #GEOexcitation(Vector(2,1,2), Vector(2,2,3))
    #GEOexcitation(Vector(2,2,3), Vector(1,2,4))

    # The death spiral!
    # x1=0;y1=0;z1=0
    # x2=0;y2=0;z2=0
    # for i in range(10*36):
        # x2=math.cos(math.radians(10*i))
        # y2=math.sin(math.radians(10*i))
        # z2=(10.*i)/360.
        # GEOexcitation(Vector(x1,y1,z1), Vector(x2,y2,z2))
        # x1=x2;y1=y2;z1=z2

    Blender.Window.SetActiveLayer(1<<2)
    GEOfrequency_snapshot(1, Vector(-1, -1, -1), Vector(1, 1, 1))
    GEOfrequency_snapshot(2, Vector(-1, -1, -1), Vector(1, 1, 1))
    GEOfrequency_snapshot(3, Vector(-1, -1, -1), Vector(1, 1, 1))

    Blender.Window.SetActiveLayer(1<<3)
    GEOtime_snapshot(1, Vector(2, -1, -1), Vector(4, 1, 1))
    GEOtime_snapshot(2, Vector(2, -1, -1), Vector(4, 1, 1))
    GEOtime_snapshot(3, Vector(2, -1, -1), Vector(4, 1, 1))

    Blender.Window.SetActiveLayer(1<<4)
    GEOeps_snapshot(1, Vector(5, -1, -1), Vector(7, 1, 1))
    GEOeps_snapshot(2, Vector(5, -1, -1), Vector(7, 1, 1))
    GEOeps_snapshot(3, Vector(5, -1, -1), Vector(7, 1, 1))

    Blender.Window.SetActiveLayer(1<<5)
    GEOfrequency_snapshot(1, Vector(-1, -1, -1), Vector(-1, 1, 1))
    GEOfrequency_snapshot(2, Vector(-1, -1, -1), Vector(1, -1, 1))
    GEOfrequency_snapshot(3, Vector(-1, -1, -1), Vector(1, 1, -1))

    Blender.Window.SetActiveLayer(1<<6)
    GEOtime_snapshot(1, Vector(2, -1, -1), Vector(2, 1, 1))
    GEOtime_snapshot(2, Vector(2, -1, -1), Vector(4, -1, 1))
    GEOtime_snapshot(3, Vector(2, -1, -1), Vector(4, 1, -1))

    Blender.Window.SetActiveLayer(1<<7)
    GEOeps_snapshot(1, Vector(5, -1, -1), Vector(5, 1, 1))
    GEOeps_snapshot(2, Vector(5, -1, -1), Vector(7, -1, 1))
    GEOeps_snapshot(3, Vector(5, -1, -1), Vector(7, 1, -1))

    for i in range(11):
        Blender.Window.SetActiveLayer(1<<8)
        GEOblock(Vector(0, 0, i), Vector(1, 1, i+1), 10*i, 0)
        GEObox(Vector(1, 1, i), Vector(2, 2, i+1))
        GEOblock(Vector(2, 2, i), Vector(3, 3, i+1), 10*i, 100)
        GEOcylinder(Vector(3.5, 3.5, i+0.5), 0, 0.5, 1, 100-10*i, 200, 0)
        GEOcylinder(Vector(4.5, 4.5, i+0.5), 0, 0.5, 1, 10*i, 200, 45)
        GEOsphere(Vector(5.5, 5.5, i+0.5), 0.5, 0, i, 0)
        Blender.Window.SetActiveLayer(1<<9)
        GEOprobe(Vector(0, 0, i))

    Blender.Scene.GetCurrent().setLayers([1,2,3,4,5,6,7,8,9,10])

def TestMatrix():
  ''' test Blender matrix object '''
  u=Blender.Mathutils.Vector(1,2,3)
  v=Blender.Mathutils.Vector(4,5,6)
  w=Blender.Mathutils.Vector(7,8,9)
  M=Blender.Mathutils.Matrix(u,v,w)
  print('============')
  print(u)
  print(v)
  print(w)
  print('============')
  print(M)
  print('============')
  print((Blender.Mathutils.RotationMatrix(math.radians(0), 2)))
  print((Blender.Mathutils.RotationMatrix(math.radians(45), 2)))
  print((Blender.Mathutils.RotationMatrix(math.radians(90), 2)))
  print((Blender.Mathutils.RotationMatrix(0, 2)))
  print((Blender.Mathutils.RotationMatrix(45, 2)))
  print((Blender.Mathutils.RotationMatrix(90, 2)))
  M=Blender.Mathutils.RotationMatrix(45, 3, 'x' )
  print('======QUAT======')
  print(M)
  print((M.toQuat()))
  print('============')
  Q=Blender.Mathutils.RotationMatrix(45, 4, 'x' )
  print(Q)
  print('============')
  u1=Blender.Mathutils.Vector(1,2,3,4)
  u2=Blender.Mathutils.Vector(5,6,7,8)
  u3=Blender.Mathutils.Vector(9,10,11,12)
  u4=Blender.Mathutils.Vector(13,14,15,16)        
  print('============')
  Q=Blender.Mathutils.Matrix(u1,u2,u3,u4)
  print(Q)
  print('============')
  print((Q.translationPart()))
  print((Q.scalePart()))
  print((Q.rotationPart()))
  print('====Q=R*Sx*Sy*Sz*T========')
  R=Blender.Mathutils.RotationMatrix(45, 4, 'r', Blender.Mathutils.Vector(17,18,19))
  T=Blender.Mathutils.TranslationMatrix(Blender.Mathutils.Vector(14,15,16))
  Sx=Blender.Mathutils.ScaleMatrix(2,4,Blender.Mathutils.Vector(1,0,0))
  Sy=Blender.Mathutils.ScaleMatrix(3,4,Blender.Mathutils.Vector(0,1,0))
  Sz=Blender.Mathutils.ScaleMatrix(4,4,Blender.Mathutils.Vector(0,0,1))
  print(Sx)
  print(Sy)
  print(Sz)
  S=Sx*Sy*Sz
  print((S.scalePart()))
  print(T)
  print(R)
  Q=S*R*T
  #~ Q=R*T
  print('============')
  print(Q)
  print('============')
  print((Q.translationPart()))
  print((Q.scalePart()))
  print((Q.rotationPart()))
  print('============')
  
  scene = Blender.Scene.GetCurrent()
  #~ mesh = Blender.Mesh.Primitives.Cylinder(32, 2, 5)
  mesh = Blender.Mesh.Primitives.Cone(32, 2, 3)
  mesh = Blender.Mesh.Primitives.Cube(1.0)
  obj = scene.objects.new(mesh, 'test_object')
  #~ obj.setMatrix(rotmat)
  #~ obj.setLocation(cone_center[0], cone_center[1], cone_center[2])

  #~ obj.setLocation(center[0], center[1], center[2])
  #~ obj.RotX = angle_X
  #~ obj.RotY = angle_Y
  #~ obj.RotZ = angle_Z
  #~ obj.transp = True; obj.wireMode = True

  #~ pos = 0.5*(lower+upper)
  #~ diag = upper-lower
  obj.SizeX = 1
  obj.SizeY = 2
  obj.SizeZ = 3
  L=Blender.Mathutils.Vector(1,0,0)
  obj.setLocation(L)
  M=obj.getMatrix()
  C=Blender.Mathutils.Vector(-1,0,0)
  T=Blender.Mathutils.TranslationMatrix(C)
  Tinv=Blender.Mathutils.TranslationMatrix(-(C))
  R=Blender.Mathutils.RotationMatrix(45, 4, 'r', Blender.Mathutils.Vector(0,0,1))
  #~ T=Blender.Mathutils.TranslationMatrix(-2,0,0)
  print('############')
  print(M)
  print(T)
  print(Tinv)
  print((M*Tinv))
  print((M*Tinv*R*T))
  print('############')
  obj.setMatrix(M*Tinv*R*T)
  print('# EULER ###########')
  print((obj.getMatrix().toEuler()))
  print('############')
  #~ obj.RotX = 90
  #~ obj.RotY = 45
  #~ obj.RotZ = 0

  #~ sys.exit(0)

  #~ Vector object 	
  #~ ProjectVecs(vec1, vec2)
  #~ Return the projection of vec1 onto vec2. 	source code
  #~ Matrix object. 	
  #~ RotationMatrix(angle, matSize, axisFlag, axis)
  #~ Create a matrix representing a rotation. 	source code
  #~ Matrix object. 	
  #~ TranslationMatrix(vector)
  #~ Create a matrix representing a translation 	source code
  #~ Matrix object. 	
  #~ ScaleMatrix(factor, matSize, axis)
  #~ Create a matrix representing a scaling. 	source code
  #~ Matrix object. 	
  #~ OrthoProjectionMatrix(plane, matSize, axis)
  #~ Create a matrix to represent an orthographic projection

if __name__ == '__main__':
  pass
