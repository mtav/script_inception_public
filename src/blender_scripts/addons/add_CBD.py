#!/usr/bin/env python3
# -*- coding: utf-8 -*-

object_name = 'Cracked Brazilian Disk (CBD)'

bl_info = {
    "name": 'Cracked Brazilian Disk (CBD)',
    "author": "mtav",
    "version": (1, 0),
    "blender": (2, 69, 0),
    "location": "View3D > Add > Mesh > Cracked Brazilian Disk (CBD)",
    "description": "Adds a new Cracked Brazilian Disk (CBD)",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh"}

import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty, BoolProperty, FloatProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
from blender_scripts.modules.blender_utilities import setOrigin, selectObjects
from blender_scripts.modules.GeometryObjects import add_cylinder, add_tetra, add_block
from blender_scripts.modules.CrackedBrazilianDisk import CrackedBrazilianDisk

class OBJECT_OT_add_CBD(Operator, AddObjectHelper):
  """Create a new CBD"""
  
  bl_idname = "mesh.add_cbd"
  bl_label = "Add " + object_name
  bl_options = {'REGISTER', 'UNDO', 'PRESET'}
  
  disk_diametro = FloatProperty(name="disk diametre", default=15, min=0)
  disk_height = FloatProperty(name="disk height", default=5, min=0)
  
  hole_width = FloatProperty(name="hole width", default=1, min=0)
  hole_length = FloatProperty(name="hole length", default=5, min=0)
  
  wall_width = FloatProperty(name="wall width", default=2, min=0)
  wall_length_extra = FloatProperty(name="additional wall length", description='length to add/remove to/from the disk diametre on each side', default=0, min=0)
  wall_height_extra = FloatProperty(name="additional wall height", description='length to add/remove to/from the disk height on each side', default=0, min=0)
  
  def draw(self, context):
    layout = self.layout
    box = layout.box()
    box.prop(self, 'disk_diametro')
    box.prop(self, 'disk_height')
    box.prop(self, 'hole_width')
    box.prop(self, 'hole_length')
    box.prop(self, 'wall_width')
    box.prop(self, 'wall_length_extra')
    box.prop(self, 'wall_height_extra')
    return
  
  def execute(self, context):
    obj = CrackedBrazilianDisk()
    obj.setDiskDiametre(self.disk_diametro)
    obj.setDiskHeight(self.disk_height)
    obj.setHoleWidth(self.hole_width)
    obj.setHoleLength(self.hole_length)
    obj.setWallWidth(self.wall_width)
    obj.setWallLengthExtra(self.wall_length_extra)
    obj.setWallHeightExtra(self.wall_height_extra)
    obj.createBlenderObject(self, context)
    return {'FINISHED'}

# Registration
def add_CBD_button(self, context):
  self.layout.operator(
      OBJECT_OT_add_CBD.bl_idname,
      text = "Add " + object_name,
      icon = 'MESH_CUBE')

def register():
  bpy.utils.register_class(OBJECT_OT_add_CBD)
  bpy.types.INFO_MT_mesh_add.append(add_CBD_button)

def unregister():
  bpy.utils.unregister_class(OBJECT_OT_add_CBD)
  bpy.types.INFO_MT_mesh_add.remove(add_CBD_button)

if __name__ == "__main__":
  register()
