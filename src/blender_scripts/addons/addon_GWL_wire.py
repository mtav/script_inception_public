#!/usr/bin/env python3
# -*- coding: utf-8 -*-

bl_info = {
    "name": "Photonic wire",
    "author": "mtav",
    "version": (1, 0),
    "blender": (2, 75, 0),
    "location": "View3D > Add > Mesh > New photonic wire",
    "description": "Adds a new photonic wire GWL object. Depends on the mesh extra objects addon.",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
    }
    
# .. todo:: add dependency to "mesh extra objects addon" somehow and handle case when missing (for bpy.ops.object.parent_to_empty() operator)

import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty, FloatProperty, BoolProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from math import radians
from mathutils import Vector, Matrix
import blender_scripts.modules.GeometryObjects as GeometryObjects
from blender_scripts.modules.blender_utilities import setOrigin, selectObjects

def add_photonic_wire(self, context):
  
  blender_object_list = []
  if self.show_design:
    cyl = GeometryObjects.add_cylinder(self, [-0.5*self.length, 0, self.height + self.bend_radius], [0.5*self.length, 0, self.height + self.bend_radius], name='photonic wire', cylinder_radius=0.5*self.wire_diametre)
    cone1 = GeometryObjects.add_cone(self, [-0.5*self.length-self.bend_radius, 0, 0], [-0.5*self.length-self.bend_radius, 0, self.height], name='Cone1', radius1=0.5*self.cone_diametre, radius2=0.5*self.wire_diametre)
    cone2 = GeometryObjects.add_cone(self, [0.5*self.length+self.bend_radius, 0, 0], [0.5*self.length+self.bend_radius, 0, self.height], name='Cone2', radius1=0.5*self.cone_diametre, radius2=0.5*self.wire_diametre)
    bend1 = GeometryObjects.add_bend(centre=[0.5*self.length, 0, self.height], bend_radius=self.bend_radius, tube_radius=0.5*self.wire_diametre, name='bend2', angle_start_deg=0, angle_end_deg=90)
    bend2 = GeometryObjects.add_bend(centre=[-0.5*self.length, 0, self.height], bend_radius=self.bend_radius, tube_radius=0.5*self.wire_diametre, name='bend1', angle_start_deg=90, angle_end_deg=180)
    
    blender_object_list.extend([cyl, cone1, cone2, bend1, bend2])
    
  if self.show_gwl:
    a = GeometryObjects.add_gwl_cone(self, [-0.5*self.length-self.bend_radius, 0, 0], [-0.5*self.length-self.bend_radius, 0, self.height], name='GWL_wire0_Cone1', radius1=0.5*self.cone_diametre, radius2=0.5*self.wire_diametre,
      cross_section_r0=self.cross_section_r0, cross_section_delta_r=self.cross_section_delta_r, cross_section_delta_theta=self.cross_section_delta_theta, longitudinal_delta=self.cone_delta)
    b = GeometryObjects.add_gwl_bend(centre=[-0.5*self.length, 0, self.height], bend_radius=self.bend_radius, tube_radius=0.5*self.wire_diametre, name='GWL_wire1_bend1', angle_start_deg=180, angle_end_deg=90,
      cross_section_r0=self.cross_section_r0, cross_section_delta_r=self.cross_section_delta_r, cross_section_delta_theta=self.cross_section_delta_theta, longitudinal_delta=self.bend_delta)
    c = GeometryObjects.add_gwl_cylinder(self, [-0.5*self.length, 0, self.height + self.bend_radius], [0.5*self.length, 0, self.height + self.bend_radius], name='GWL_wire2_photonic_wire', cylinder_radius=0.5*self.wire_diametre,
      cross_section_r0=self.cross_section_r0, cross_section_delta_r=self.cross_section_delta_r, cross_section_delta_theta=self.cross_section_delta_theta, longitudinal_delta=self.wire_delta)
    d = GeometryObjects.add_gwl_bend(centre=[0.5*self.length, 0, self.height], bend_radius=self.bend_radius, tube_radius=0.5*self.wire_diametre, name='GWL_wire3_bend2', angle_start_deg=90, angle_end_deg=0,
      cross_section_r0=self.cross_section_r0, cross_section_delta_r=self.cross_section_delta_r, cross_section_delta_theta=self.cross_section_delta_theta, longitudinal_delta=self.bend_delta)
    e = GeometryObjects.add_gwl_cone(self, [0.5*self.length+self.bend_radius, 0, self.height], [0.5*self.length+self.bend_radius, 0, 0], name='GWL_wire4_Cone2', radius2=0.5*self.cone_diametre, radius1=0.5*self.wire_diametre,
      cross_section_r0=self.cross_section_r0, cross_section_delta_r=self.cross_section_delta_r, cross_section_delta_theta=self.cross_section_delta_theta, longitudinal_delta=self.cone_delta)
  
    blender_object_list.extend([a,b,c,d,e])
    
  if blender_object_list:
    selectObjects(blender_object_list)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.object.parent_to_empty()
    obj = bpy.context.active_object
    obj.matrix_world = Matrix.Rotation(radians(self.rotation), 4, 'Z')
    obj.location = self.location
  
  # for obj in blender_object_list:
    # # setOrigin(obj, [0,0,0])
    # # obj.rotation_euler = (0,0,0)  # Note that you need to use radians rather than angles here
    
    # obj.matrix_world = Matrix.Rotation(radians(self.rotation), 4, 'Z')
    # obj.location = self.location
    
  return

class AddPhotonicWire(Operator, AddObjectHelper):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_photonic_wire"
    bl_label = "Add photonic wire"
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
    
    length = FloatProperty(
            name="length",
            default=200/50,
            min=0.01,
            )
    height = FloatProperty(
            name="height",
            default=45/50,
            min=0.01,
            )
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
    cone_diametre = FloatProperty(
            name="cone_diametre",
            default=16/50,
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
    longitudinal_delta_sync = BoolProperty(
            name="Sync longitudinal steps",
            default=False,
            )
    bend_delta = FloatProperty(
            name="bend_delta",
            description='step along the bends',
            default=0.1,
            min=0.01,
            )
    cone_delta = FloatProperty(
            name="cone_delta",
            description='step along the cones',
            default=0.1,
            min=0.01,
            )
    wire_delta = FloatProperty(
            name="wire_delta",
            description='step along the straight wire',
            default=0.1,
            min=0.01,
            )
    #################################
    
    def draw(self, context):
      layout = self.layout
      box = layout.box()
      box.label('Design:')
      box.prop(self, 'length')
      box.prop(self, 'height')
      box.prop(self, 'bend_radius')
      box.prop(self, 'wire_diametre')
      box.prop(self, 'cone_diametre')
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
      b.prop(self, 'longitudinal_delta_sync')
      b.prop(self, 'cone_delta')
      if not self.longitudinal_delta_sync:
        b.prop(self, 'bend_delta')
        b.prop(self, 'wire_delta')
      else:
        self.bend_delta = self.cone_delta
        self.wire_delta = self.cone_delta
      b = box_gwl.box()
      b.label('Placement')
      b.prop(self, 'location')
      b.prop(self, 'rotation')

    def execute(self, context):
        add_photonic_wire(self, context)
        return {'FINISHED'}

# Registration
def addPhotonicWireButton(self, context):
    self.layout.operator(
        AddPhotonicWire.bl_idname,
        text="Add photonic wire",
        icon='PLUGIN')

def register():
    bpy.utils.register_class(AddPhotonicWire)
    bpy.types.INFO_MT_mesh_add.append(addPhotonicWireButton)

def unregister():
    bpy.utils.unregister_class(AddPhotonicWire)
    bpy.types.INFO_MT_mesh_add.remove(addPhotonicWireButton)

if __name__ == "__main__":
    register()
