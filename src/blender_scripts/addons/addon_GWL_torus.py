#!/usr/bin/env python3
# -*- coding: utf-8 -*-

bl_info = {
    "name": "Photonic torus",
    "author": "mtav",
    "version": (1, 0),
    "blender": (2, 75, 0),
    "location": "View3D > Add > Mesh > New photonic torus",
    "description": "Adds a new photonic torus GWL object. Depends on the mesh extra objects addon.",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
    }
    
# .. todo:: add dependency to "mesh extra objects addon" somehow and handle case when missing (for bpy.ops.object.parent_to_empty() operator)
# .. todo:: change "scar position" (open part of bend)
# .. todo:: make interface usable by other addons using bends like the photonic wire one?
# .. todo:: open-describe with python-based language to create structures?

import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty, FloatProperty, BoolProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from math import radians
from mathutils import Vector, Matrix
import blender_scripts.modules.GeometryObjects as GeometryObjects
from blender_scripts.modules.blender_utilities import setOrigin, selectObjects

def add_photonic_torus(self, context):
  
  blender_object_list = []
  if self.show_design:
    b = GeometryObjects.add_bend(centre=[0,0,0], bend_radius=self.bend_radius, tube_radius=0.5*self.wire_diametre, name='bend_design', angle_start_deg=self.angle_start_deg, angle_end_deg=self.angle_end_deg)
    
    blender_object_list.extend([b])
    
  if self.show_gwl:
    b = GeometryObjects.add_gwl_bend(centre=[0,0,0], bend_radius=self.bend_radius, tube_radius=0.5*self.wire_diametre, name='bend_GWL', angle_start_deg=self.angle_start_deg, angle_end_deg=self.angle_end_deg,
      cross_section_r0=self.cross_section_r0, cross_section_delta_r=self.cross_section_delta_r, cross_section_delta_theta=self.cross_section_delta_theta, longitudinal_delta=self.bend_delta)
    
    blender_object_list.extend([b])
    
  if blender_object_list:
    selectObjects(blender_object_list)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.object.parent_to_empty()
    obj = bpy.context.active_object
    obj.matrix_world = Matrix.Rotation(radians(self.rotation), 4, 'Z')
    obj.location = self.location
    
  return

class AddPhotonicTorus(Operator, AddObjectHelper):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_photonic_torus"
    bl_label = "Add photonic torus"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}
    
    #################################
    location = FloatVectorProperty(
            name="location",
            default=[0,0,0]
            )
    rotation = FloatProperty(
            name="rotation",
            default=0,
            description='rotation around Z in degrees',
            step=100,
            )
    #################################
    angle_start_deg = FloatProperty(
            name="start angle (degrees)",
            default=-30,
            step=100,
            )
    angle_end_deg = FloatProperty(
            name="end angle (degrees)",
            default=60,
            step=100,
            )
    #################################
    bend_radius = FloatProperty(
            name="bend_radius",
            default=60/50,
            min=0.01,
            )
    wire_diametre = FloatProperty(
            name="wire_diametre",
            default=5/50,
            min=0.01,
            )
    show_design = BoolProperty(
            name="show design",
            default=True,
            )
    #################################
    show_gwl = BoolProperty(
            name="show GWL",
            default=True,
            )
    #################################
    cross_section_delta_sync = BoolProperty(
            name="Sync cross-section steps",
            default=False,
            )
    cross_section_r0 = FloatProperty(
            name="r0",
            description='size of inner circle',
            default=0.05,
            min=0.01,
            )
    cross_section_delta_r = FloatProperty(
            name="delta_r",
            description='step between circles',
            default=0.1,
            min=0.01,
            )
    cross_section_delta_theta = FloatProperty(
            name="delta_theta",
            description='step along a circle',
            default=0.1,
            min=0.01,
            )
    #################################
    bend_delta = FloatProperty(
            name="bend_delta",
            description='step along the bends',
            default=0.1,
            min=0.01,
            )
    #################################
    
    def draw(self, context):
      layout = self.layout
      box = layout.box()
      box.label('Design:')
      box.prop(self, 'bend_radius')
      box.prop(self, 'wire_diametre')
      box.prop(self, 'angle_start_deg')
      box.prop(self, 'angle_end_deg')
      box.prop(self, 'show_design')
      box_gwl = layout.box()
      box_gwl.label('GWL parameters:')
      box_gwl.prop(self, 'show_gwl')
      b = box_gwl.box()
      b.label('Cross-section parameters:')
      b.prop(self, 'cross_section_delta_sync')
      b.prop(self, 'cross_section_r0')
      b.prop(self, 'cross_section_delta_r')
      if not self.cross_section_delta_sync:
        b.prop(self, 'cross_section_delta_theta')
      else:
        self.cross_section_delta_theta = self.cross_section_delta_r
      b = box_gwl.box()
      b.label('Longitudinal parameters')
      b.prop(self, 'bend_delta')
      b = box_gwl.box()
      b.label('Placement')
      b.prop(self, 'location')
      b.prop(self, 'rotation')

    def execute(self, context):
        add_photonic_torus(self, context)
        return {'FINISHED'}

# Registration
def addPhotonicTorusButton(self, context):
    self.layout.operator(
        AddPhotonicTorus.bl_idname,
        text="Add photonic torus",
        icon='PLUGIN')

def register():
    bpy.utils.register_class(AddPhotonicTorus)
    bpy.types.INFO_MT_mesh_add.append(addPhotonicTorusButton)

def unregister():
    bpy.utils.unregister_class(AddPhotonicTorus)
    bpy.types.INFO_MT_mesh_add.remove(addPhotonicTorusButton)

if __name__ == "__main__":
    register()
