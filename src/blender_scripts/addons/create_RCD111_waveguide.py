#!/usr/bin/env python3
# -*- coding: utf-8 -*-

bl_info = {
    "name": "Create RCD111 waveguide",
    "author": "mtav",
    "version": (1, 0),
    "blender": (3, 4, 0),
    "location": "View3D > SIP menu -> Create RCD111 waveguide",
    "description": "Create RCD111 waveguide",
    "warning": "UNFINISHED",
    "wiki_url": "",
    "category": "Object"}

import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty, BoolProperty, FloatProperty, IntProperty, EnumProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
from blender_scripts.modules.blender_utilities import setOrigin, selectObjects, add_array_modifier
from blender_scripts.modules.GeometryObjects import add_cylinder, add_tetra

import bfdtd.RCD

#class CreateRCD111WaveguidePanel(bpy.types.Panel):
  #bl_space_type = "VIEW_3D"
  #bl_region_type = "TOOLS"
  #bl_context = "objectmode"
  #bl_category = "SIP"
  #bl_label = "Create RCD111 waveguide"

  #def draw(self, context):
    #TheCol = self.layout.column(align=True)
    #TheCol.operator("object.create_rcd111_waveguide", text="Create RCD111 waveguide")
    
class CreateRCD111Waveguide(bpy.types.Operator):
  bl_idname = "object.create_rcd111_waveguide"
  bl_label = "Create RCD111 waveguide"
  bl_options = {'REGISTER', 'UNDO', 'PRESET'}
  
  (preset_vectors , preset_vectors_groups) = bfdtd.RCD.RCD111_waveguide_vector_dictionary()
  direction : EnumProperty(items = (("three_arrays","Use 3 arrays","Avoids overlapping objects, but the origin and location of the original are modified. Uses less memory."), ("six_arrays","Use 6 arrays","Can lead to overlapping objects. Preserves origin and location of the original. Easy to change periods later. Memory intensive.")), default='three_arrays', name = "Method:")

  method : EnumProperty(items = (("three_arrays","Use 3 arrays","Avoids overlapping objects, but the origin and location of the original are modified. Uses less memory."), ("six_arrays","Use 6 arrays","Can lead to overlapping objects. Preserves origin and location of the original. Easy to change periods later. Memory intensive.")), default='three_arrays', name = "Method:")

  array_X_positive : BoolProperty(name="Array along +X", default=True)
  array_X_positive_size : IntProperty(name="number of periods in +X", default = 2, min=1)
  array_Y_positive : BoolProperty(name="Array along +Y", default=True)
  array_Y_positive_size : IntProperty(name="number of periods in +Y", default = 3, min=1)
  array_Z_positive : BoolProperty(name="Array along +Z", default=True)
  array_Z_positive_size : IntProperty(name="number of periods in +Z", default = 4, min=1)
  
  array_X_negative : BoolProperty(name="Array along -X", default=False)
  array_X_negative_size : IntProperty(name="number of periods in -X", default = 2, min=1)
  array_Y_negative : BoolProperty(name="Array along -Y", default=False)
  array_Y_negative_size : IntProperty(name="number of periods in -Y", default = 3, min=1)
  array_Z_negative : BoolProperty(name="Array along -Z", default=False)
  array_Z_negative_size : IntProperty(name="number of periods in -Z", default = 4, min=1)
  
  e1_vec3 : FloatVectorProperty(name="e1_vec3", default=Vector((1,0,0)))
  e2_vec3 : FloatVectorProperty(name="e2_vec3", default=Vector((0,1,0)))
  e3_vec3 : FloatVectorProperty(name="e3_vec3", default=Vector((0,0,1)))
  
  use_scale : BoolProperty(name="Use object scale", default=False) # TODO: Take scale into account?
  apply_scale : BoolProperty(name="Apply scale first", default=False) # TODO: Take scale into account?
  
  def draw(self, context):
    layout = self.layout
    box = layout.box()
    box.prop(self, 'method')
    
    if self.method == 'three_arrays':
      box.prop(self, 'array_X_positive')
      if self.array_X_positive:
        box.prop(self, 'array_X_positive_size')
        box.prop(self, 'array_X_negative_size')
      box.prop(self, 'array_Y_positive')
      if self.array_Y_positive:
        box.prop(self, 'array_Y_positive_size')
        box.prop(self, 'array_Y_negative_size')
      box.prop(self, 'array_Z_positive')
      if self.array_Z_positive:
        box.prop(self, 'array_Z_positive_size')
        box.prop(self, 'array_Z_negative_size')
      
    else:
      box.prop(self, 'array_X_positive')
      if self.array_X_positive:
        box.prop(self, 'array_X_positive_size')
      box.prop(self, 'array_Y_positive')
      if self.array_Y_positive:
        box.prop(self, 'array_Y_positive_size')
      box.prop(self, 'array_Z_positive')
      if self.array_Z_positive:
        box.prop(self, 'array_Z_positive_size')
      
      box.prop(self, 'array_X_negative')
      if self.array_X_negative:
        box.prop(self, 'array_X_negative_size')
      box.prop(self, 'array_Y_negative')
      if self.array_Y_negative:
        box.prop(self, 'array_Y_negative_size')
      box.prop(self, 'array_Z_negative')
      if self.array_Z_negative:
        box.prop(self, 'array_Z_negative_size')
    
    box.prop(self, 'e1_vec3')
    box.prop(self, 'e2_vec3')
    box.prop(self, 'e3_vec3')
    
    box.prop(self, 'use_scale')
    box.prop(self, 'apply_scale')

  def execute(self, context):
    return {'FINISHED'}
    
    obj = context.active_object
    obj_location_original = obj.location.copy()
    
    if self.apply_scale:
      bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    if self.use_scale:
      e1_vec3 = Vector(self.e1_vec3)
      e2_vec3 = Vector(self.e2_vec3)
      e3_vec3 = Vector(self.e3_vec3)
    else:
      e1_vec3 = scale_vector_divide(obj.scale, self.e1_vec3)
      e2_vec3 = scale_vector_divide(obj.scale, self.e2_vec3)
      e3_vec3 = scale_vector_divide(obj.scale, self.e3_vec3)
        
    if self.method == 'three_arrays':
      if self.use_scale:
        if self.array_X_positive:
          obj.location = obj.location - (self.array_X_negative_size - 1) * scale_vector_multiply(obj.scale, self.e1_vec3)
        if self.array_Y_positive:
          obj.location = obj.location - (self.array_Y_negative_size - 1) * scale_vector_multiply(obj.scale, self.e2_vec3)
        if self.array_Z_positive:
          obj.location = obj.location - (self.array_Z_negative_size - 1) * scale_vector_multiply(obj.scale, self.e3_vec3)
      else:
        if self.array_X_positive:
          obj.location = obj.location - (self.array_X_negative_size - 1) * Vector(self.e1_vec3)
        if self.array_Y_positive:
          obj.location = obj.location - (self.array_Y_negative_size - 1) * Vector(self.e2_vec3)
        if self.array_Z_positive:
          obj.location = obj.location - (self.array_Z_negative_size - 1) * Vector(self.e3_vec3)
      
      setOrigin(obj, obj_location_original)
      
      if self.array_X_positive:
        add_array_modifier(obj, 'array X', self.array_X_positive_size + self.array_X_negative_size - 1, e1_vec3)
      if self.array_Y_positive:
        add_array_modifier(obj, 'array Y', self.array_Y_positive_size + self.array_Y_negative_size - 1, e2_vec3)
      if self.array_Z_positive:
        add_array_modifier(obj, 'array Z', self.array_Z_positive_size + self.array_Z_negative_size - 1, e3_vec3)
      
    else:
      if self.array_X_positive:
        add_array_modifier(obj, 'array +X', self.array_X_positive_size, e1_vec3)
      if self.array_Y_positive:
        add_array_modifier(obj, 'array +Y', self.array_Y_positive_size, e2_vec3)
      if self.array_Z_positive:
        add_array_modifier(obj, 'array +Z', self.array_Z_positive_size, e3_vec3)
      if self.array_X_negative:
        add_array_modifier(obj, 'array -X', self.array_X_negative_size, -e1_vec3)
      if self.array_Y_negative:
        add_array_modifier(obj, 'array -Y', self.array_Y_negative_size, -e2_vec3)
      if self.array_Z_negative:
        add_array_modifier(obj, 'array -Z', self.array_Z_negative_size, -e3_vec3)
    
    return {'FINISHED'}

def register():
  bpy.utils.register_class(CreateRCD111Waveguide)
  #bpy.utils.register_class(CreateRCD111WaveguidePanel)

def unregister():
  bpy.utils.unregister_class(CreateRCD111Waveguide)
  #bpy.utils.unregister_class(CreateRCD111WaveguidePanel)

if __name__ == "__main__":
  register()
