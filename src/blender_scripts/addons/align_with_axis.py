#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import bpy
import math
from math import atan, radians, sqrt
import mathutils
from mathutils import Vector, Matrix
from bpy.props import FloatVectorProperty, IntProperty, FloatProperty, BoolProperty, StringProperty, EnumProperty

bl_info = {
    "name": "align_with_axis",
    "author": "mtav",
    "version": (1, 0),
    "blender": (3, 4, 0),
    "location": "View3D > Tool shelf -> SIP -> Align with axis",
    "description": "Allows you to align an object along a specific axis, including with a specific rotation around that axis and specific dimensions.",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"}

#class AlignWithAxisPanel(bpy.types.Panel):
  #bl_space_type = "VIEW_3D"
  #bl_region_type = "TOOLS"
  #bl_context = "objectmode"
  ##bl_category = "Tools"
  #bl_category = "SIP"
  #bl_label = "Align with axis"

  #def draw(self, context):
    #TheCol = self.layout.column(align=True)
    #TheCol.operator("object.align_with_axis", text="Align with axis")
    
class AlignWithAxis(bpy.types.Operator):
  bl_idname = "object.align_with_axis"
  bl_label = "Align with axis"
  bl_options = {'REGISTER', 'UNDO', 'PRESET'}

  origin : FloatVectorProperty(name="origin", default=Vector((0,0,0)))

  direction_specification_style : EnumProperty(items = (("vector","vector","vector"),("endpoint","endpoint","endpoint")), default='endpoint', name = "direction_specification_style")
  e3_vec3 : FloatVectorProperty(name="e3_vec3", default=Vector((0,0,1)))
  e1_vec3 : FloatVectorProperty(name="e1_vec3", default=Vector((1,0,0)))
  
  norm_specification_style : EnumProperty(items = (("normalized","normalized","normalized"),("specific_norm","specific norm","specific norm"),("norm_from_vectors","norm from vectors","norm from vectors")), default='specific_norm', name = "norm_specification_style")

  e1_norm : FloatProperty(name="e1_norm", default=1)
  e2_norm : FloatProperty(name="e2_norm", default=1)
  e3_norm : FloatProperty(name="e3_norm", default=1)

  bool_inverse : BoolProperty(name="inverse", description="Use inverse transformation", default=False)

  a_raw = Vector()
  b_raw = Vector()
  c_raw = Vector()

  a_normalized = Vector()
  b_normalized = Vector()
  c_normalized = Vector()

  def draw(self, context):
    layout = self.layout
    box = layout.box()
    box.prop(self, 'origin')
    box.prop(self, 'direction_specification_style')
    box.prop(self, 'e3_vec3')
    box.prop(self, 'e1_vec3')
    box.prop(self, 'norm_specification_style')
    if self.norm_specification_style == "specific_norm":
        box.prop(self, 'e1_norm')
        box.prop(self, 'e2_norm')
        box.prop(self, 'e3_norm')
    box.prop(self, 'bool_inverse')
    
    # display information about resulting basis vectors
    layout.label(text="Information:")
    box = layout.box()
    
    col = box.column(align=False)
    col.label(text='non-normalized:')
    col.label(text='a = [{}, {}, {}]'.format(*self.a_raw))
    col.label(text='b = [{}, {}, {}]'.format(*self.b_raw))
    col.label(text='c = [{}, {}, {}]'.format(*self.c_raw))
    col.label(text='normalized:')
    col.label(text='a/norm(a) = [{}, {}, {}]'.format(*self.a_normalized))
    col.label(text='b/norm(b) = [{}, {}, {}]'.format(*self.b_normalized))
    col.label(text='c/norm(c) = [{}, {}, {}]'.format(*self.c_normalized))

  def execute(self, context):
    
    # define origin and axis
    start = Vector(self.origin)
    
    #print(start)
    #print(Vector(start))
    #print(start[0])
    #print(start[1])
    #print(start[2])

    if self.direction_specification_style == "endpoint":
        end = Vector(self.e3_vec3)
        axis = end - start
    else:
        end = Vector(self.origin) + Vector(self.e3_vec3)
        axis = Vector(self.e3_vec3)
    
    # set up x,y,z vectors for convenience
    x = Vector((1,0,0))
    y = Vector((0,1,0))
    z = Vector((0,0,1))

    # create un-normalized basis vectors
    c = axis.copy()
    b = axis.cross(Vector(self.e1_vec3))
    a = b.cross(c)

    self.a_raw = a.copy()
    self.b_raw = b.copy()
    self.c_raw = c.copy()
    self.a_normalized = a.copy()
    self.b_normalized = b.copy()
    self.c_normalized = c.copy()
    self.a_normalized.normalize()
    self.b_normalized.normalize()
    self.c_normalized.normalize()

    if self.norm_specification_style == "normalized":
        xdim = 1
        ydim = 1
        zdim = 1
    elif self.norm_specification_style == "norm_from_vectors":
        xdim = a.length
        ydim = b.length
        zdim = c.length
    else:
        xdim = self.e1_norm
        ydim = self.e2_norm
        zdim = self.e3_norm

    # normalize the basis
    a.normalize()
    b.normalize()
    c.normalize()

    # create a,b,c,d vectors for the final transformation matrix
    a = a.resized(4)
    b = b.resized(4)
    c = c.resized(4)
    d = Vector((0,0,0,1))

    # create scaling+translation matrices
    Sx = Matrix.Scale(xdim, 4, Vector((1,0,0)))
    Sy = Matrix.Scale(ydim, 4, Vector((0,1,0)))
    Sz = Matrix.Scale(zdim, 4, Vector((0,0,1)))
    T = Matrix.Translation(start)

    # create the final transformation matrix
    Mfinal = T @ Matrix((a,b,c,d)).transposed() @ Sx @ Sy @ Sz

    # apply the final transformation matrix
    obj = context.object
    
    if obj is None:
      self.report({'ERROR'}, "No object selected!")
      return {'FINISHED'}
    
    # TODO: Fix inverse transformation. Does not seem to work properly when translation+rotation+scaling are used.
    if not self.bool_inverse:
      obj.matrix_local = Mfinal
    else:
      obj.matrix_local = Mfinal.inverted()
    
    print('obj.matrix_local = ',obj.matrix_local)
    #print('FINISHED')

    return {'FINISHED'}

def register():
  bpy.utils.register_class(AlignWithAxis)
  #bpy.utils.register_class(AlignWithAxisPanel)

def unregister():
  bpy.utils.unregister_class(AlignWithAxis)
  #bpy.utils.unregister_class(AlignWithAxisPanel)

if __name__ == "__main__":
  register()
