#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ..todo:: Add vectors+unit-cell for lattice+reciprocal lattice (with centered/non-centered origin option?)
# ..todo:: multi-file import? (need better grouping first)

bl_info = {
    'name': 'Import MPB output (.out)',
    'author': 'mtav',
    'version': (0, 0, 1),
    'blender': (3, 4, 1),
    'location': 'File > Import > MPB (.out)',
    'description': 'Import k-points from MPB output files (.out)',
    'warning': '',
    'wiki_url': '',
    'tracker_url': '',
    'category': 'Import-Export',
    }

import os
import sys
import numpy
import argparse
from MPB.MPB_parser import parse_MPB
from blender_scripts.modules.blender_utilities import selectObjects, createGroup, make_collection

import bpy
import bmesh
# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty, CollectionProperty
from bpy.types import Operator
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from blender_scripts.modules.GeometryObjects import add_arrow, add_lattice_vectors, add_lattice_cell, add_lattice_objects

class Import_MPB_data(Operator, ImportHelper, AddObjectHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "import_mpb.mpb"  # important since its how bpy.ops.import_mpb.mpb is constructed
    bl_label = "Import MPB data"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    # ImportHelper mixin class uses this
    filename_ext = ".out"

    filter_glob : StringProperty(
            default="*.out;*.dat",
            options={'HIDDEN'},
            )

    # necessary to support multi-file import
    # https://stackoverflow.com/questions/63299327/importing-multiple-files-in-blender-import-plugin
    files: CollectionProperty(
        type=bpy.types.OperatorFileListElement,
        options={'HIDDEN', 'SKIP_SAVE'},
    )

    directory: StringProperty(
        subtype='DIR_PATH',
    )

    bool_cone_length_automatic  : BoolProperty(name="Automatic cone length", default=True)
    cone_length : FloatProperty(
            name="cone_length",
            default=1/5.0,
            description="cone length",
            )

    bool_cone_radius_automatic : BoolProperty(name="Automatic cone radius", default=True)
    cone_radius : FloatProperty(
            name="cone_radius",
            default=1/20.0,
            description="cone radius",
            )

    bool_cylinder_radius_automatic : BoolProperty(name="Automatic cylinder radius", default=True)
    cylinder_radius : FloatProperty(
            name="cylinder_radius",
            default=1/40.0,
            description="cylinder radius",
            )

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.prop(self, 'bool_cone_length_automatic')
        if not self.bool_cone_length_automatic:
          box.prop(self, 'cone_length')
        
        box.prop(self, 'bool_cone_radius_automatic')
        if not self.bool_cone_radius_automatic:
          box.prop(self, 'cone_radius')
        
        box.prop(self, 'bool_cylinder_radius_automatic')
        if not self.bool_cylinder_radius_automatic:
          box.prop(self, 'cylinder_radius')

    def execute(self, context):

      # loop through selected files
      for current_file in self.files:
          filepath = os.path.join(self.directory, current_file.name)
          print('Importing MPB .out file:', filepath)

          # create importer instance and set parameters
          importer = Importer()
          importer.filepath = filepath
          importer.context = context
          importer.operator = self

          # set arrow parameters
          if self.bool_cone_length_automatic:
            importer.cone_length = None
          else:
            importer.cone_length = self.cone_length

          if self.bool_cone_radius_automatic:
            importer.cone_radius = None
          else:
            importer.cone_radius = self.cone_radius

          if self.bool_cylinder_radius_automatic:
            importer.cylinder_radius = None
          else:
            importer.cylinder_radius = self.cylinder_radius

          # execute importer instance
          importer.execute()

      # return importer.execute()
      return {'FINISHED'}

# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
    self.layout.operator(Import_MPB_data.bl_idname, text="MPB (.out)")

def register():
    bpy.utils.register_class(Import_MPB_data)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister():
    bpy.utils.unregister_class(Import_MPB_data)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

# TODO: Try to integrate this into MPB_parser.py somehow if possible (import bpy&co only when needed)
class Importer():
  filepath = None
  cone_length = None # 1/5.0
  cone_radius = None # 1/20.0
  cylinder_radius = None # 1/40.0
  context = bpy.context
  operator = None
  
  def __init__(self):
    return
  
  def execute(self):
    print("running read_mpb...")
    filepath_basename = os.path.basename(self.filepath)
    
    (root, ext) = os.path.splitext(self.filepath)
    if ext == '.dat':
      print('==> .dat file detected')
      # hack
      return {'FINISHED'}
    
    with open(self.filepath) as infile:
      MPB_data_list = parse_MPB(infile)

      # Create a new collection to which all new things will be added.
      collection = make_collection(filepath_basename, parent_collection=None, checkExisting=False, make_active=True)
      # layer_collection = bpy.context.view_layer.layer_collection.children[collection.name]
      # bpy.context.view_layer.active_layer_collection = layer_collection

      for idx, MPB_data_object in enumerate(MPB_data_list):
        print('=== dataset {} ==='.format(idx))
        
        name = 'k-points-{}-{}'.format(filepath_basename, idx)
        
        # add lattice+reciprocal lattice basis vectors+cells
        (a0,a1,a2) = MPB_data_object.getLatticeVectors()
        (b0,b1,b2) = MPB_data_object.getReciprocalLatticeVectors()

        ##### Add lattice cells + vectors
        lattice_objects = add_lattice_objects(self, a0, a1, a2, b0, b1, b2, name = name+'-lattice_objects',
                                                cone_length=self.cone_length,
                                                cone_radius=self.cone_radius,
                                                cylinder_radius=self.cylinder_radius)

        ##### List of objects that will be grouped together by parenting it to an empty
        obj_list = lattice_objects

        # add k-point path and sphere following it
        L = MPB_data_object.get_kpoints_in_cartesian_coordinates()
        if len(L)>0:
          for i in L:
            print(i)
          
          mesh = bpy.data.meshes.new(name)

          bm = bmesh.new()

          for v_co in L:
            bm.verts.new(v_co)

          bm.verts.ensure_lookup_table()
          for i in range(len(L)-1):
            bm.edges.new([bm.verts[i], bm.verts[i+1]])

          bm.to_mesh(mesh)
          mesh.update()

          object_data_add(self.context, mesh, operator=self.operator)
          bpy.ops.object.convert(target='CURVE')
          
          k_points_path_object = self.context.active_object
          k_points_path_object.name = name+'-path'

          print('Adding animation...')
          k_points_path_object.data.use_path = True
          scene = self.context.scene
          k_points_path_object.data.path_duration = scene.frame_end - scene.frame_start

          bpy.ops.mesh.primitive_uv_sphere_add()
          S = self.context.active_object
          S.name = name+'-sphere'
          L = numpy.power(MPB_data_object.getReciprocalCellVolume(), 1/3)
          S.scale = 3*[L/20]

          # add a constraint to it
          constraint = S.constraints.new('FOLLOW_PATH')
          constraint.target = k_points_path_object
          bpy.ops.constraint.followpath_path_animate(constraint=constraint.name)

          #bpy.ops.object.constraint_add(type='FOLLOW_PATH')
          #C = S.constraints[-1]
          #C.target = k_points_path_object
          #selectObjects([S], active_object=S, context=self.context)
          #bpy.ops.constraint.followpath_path_animate(constraint="Follow Path", owner='OBJECT')

          # https://devtalk.blender.org/t/deprecationwarning-passing-in-context-overrides-is-deprecated-in-favor-of-context-temp-override/27870
          # https://docs.blender.org/api/current/bpy.ops.constraint.html
          # https://blender.stackexchange.com/questions/285851/use-followpath-path-animate-in-python-script
          # with bpy.context.temp_override(**kwargs):
          # with bpy.context.temp_override(constraint=constraint):
          #     bpy.ops.constraint.followpath_path_animate(override, constraint='Follow Path')

          # override = {'constraint':constraint}
          # bpy.ops.constraint.followpath_path_animate(override, constraint='Follow Path')

          selectObjects([k_points_path_object], active_object=k_points_path_object, context=self.context)

          obj_list.extend([k_points_path_object]) # The sphere is already constrained by the "follow path" constraint.

        else:
          print('no k-points found')

      ##### group objects together by parenting them to an empty

      # L = selectObjects(obj_list, active_object=None, context=bpy.context, include_children=True)
      # for idx, obj in L:
      #     print(idx, obj)

      hide_settings = [obj.hide_get() for obj in obj_list]
      for obj in obj_list:
          obj.hide_set(False)

      bpy.ops.object.add(type='EMPTY')
      obj_empty = bpy.context.active_object
      obj_empty.name = filepath_basename
      selectObjects(obj_list, active_object=obj_empty, context=bpy.context)
      bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

      # myCol = createGroup(obj_list, active_object=None, context=bpy.context, group_name=filepath_basename)

      for h, obj in zip(hide_settings, obj_list):
          obj.hide_set(h)

    print('FINISHED')
    return {'FINISHED'}

    ## create the empty
    #newempty = bpy.data.objects.new('empty_'+curve.name, None)
    #newempty.empty_draw_type = 'ARROWS'
    ## link it to the current scene
    #bpy.context.scene.objects.link(newempty)

    # TODO: path animation with arrow :) + maybe auto-BZ add?
    # TODO: use k-points from pre-run output, i.e. in (x,y,z) format (that way, no need to wait for run to finish)

    # path building:
    #>>> print(d.splines[0].points[0])
    #<bpy_struct, SplinePoint at 0x7f37627a0b88>

    #>>> print(d.splines[0].points[0].co)
    #<Vector (-2.0000, 0.0000, 0.0000, 1.0000)>

    #>>> print(d.splines[0].points[1].co)
    #<Vector (-1.0000, 0.0000, 0.0000, 1.0000)>

    #>>> print(d.splines[0].points[2].co)
    #<Vector (0.0000, 0.0000, 0.0000, 1.0000)>

    #>>> print(d.splines[0].points[3].co)
    #<Vector (1.0000, 0.0000, 0.0000, 1.0000)>

    #>>> print(d.splines[0].points[4].co)
    #<Vector (2.0000, 0.0000, 0.0000, 1.0000)>

    #>>> print(d.splines[0].points[5].co)
    #Traceback (most recent call last):
      #File "<blender_console>", line 1, in <module>
    #IndexError: bpy_prop_collection[index]: index 5 out of range, size 5

    #>>> d
    #bpy.data.curves['NurbsPath']

def main():
  print('sys.argv=' + str(sys.argv))
  print('len(sys.argv)=' + str(len(sys.argv)))

  parser = argparse.ArgumentParser()
  parser.add_argument('filename', nargs='+')
  args = parser.parse_args(sys.argv[4:])
  print(sys.argv[4:])
  print(args)
  
  for i in args.filename:
    importer = Importer()
    importer.filepath = i
    importer.execute()

  return

if __name__ == "__main__":
    main()
    #register()

    ## test call
    #bpy.ops.import_mpb.mpb('INVOKE_DEFAULT')
