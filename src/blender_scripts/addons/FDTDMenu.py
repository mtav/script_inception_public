#!/usr/bin/env python3
# -*- coding: utf-8 -*-

bl_info = {
    'name': 'FDTD menu - EXPERIMENTAL',
    'author': 'mtav',
    'version': (0, 0, 1),
    'blender': (2, 63, 0),
    'location': '3D View->Add->FDTD',
    'description': 'FDTD menu',
    'warning': 'Under construction!',
    'category': 'FDTD',
    }

'''
FDTD menu to add objects with FDTD properties (permittivity, conductivity, radius, etc).
.. todo:: Organize all SIP addons adding objects into submenus.
.. todo:: Create single SIP addons or groups of it. (part of bigger push to proper modules and easier installs+tests)
.. todo:: upload generic useful scripts to blender repos, after passing script standard tests (PEP80 or similar?)
'''

import bpy
import math
import mathutils

from bpy.types import Operator
from bpy_extras.object_utils import AddObjectHelper, object_data_add

from bpy.props import (StringProperty,
                       BoolProperty,
                       CollectionProperty,
                       EnumProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       IntProperty
                       )

import bfdtd
from bfdtd.GeometryObjects import Block
import blender_scripts
#import blender_scripts.modules
#import blender_scripts.modules.FDTDGeometryObjects
#import blender_scripts.modules.GeometryObjects

class FDTDMenu(bpy.types.Menu):
  bl_label = "FDTD"
  bl_idname = "OBJECT_MT_fdtd_menu"

  def draw(self, context):
    layout = self.layout
    layout.operator("fdtd.block")
    layout.operator("fdtd.distorted")
    layout.operator("fdtd.sphere")
    layout.operator("fdtd.cylinder")

def draw_item(self, context):
  layout = self.layout
  layout.menu(FDTDMenu.bl_idname)

# .. todo:: why _OT_ ?
class OBJECT_OT_block(Operator, AddObjectHelper):
  """Create a new block"""
  bl_idname = "fdtd.block"
  bl_label = "Add FDTD block"
  bl_options = {'REGISTER', 'UNDO', 'PRESET'}
  
  def execute(self, context):
    print('Adding FDTD block')
    bfdtd_obj_manager = blender_scripts.modules.FDTDGeometryObjects.FDTDGeometryObjects()
    pos = bpy.context.scene.cursor_location
    bfdtd_obj_manager.GEOblock_matrix('BFDTD-Block', mathutils.Matrix.Translation(pos), 4, 0)
    
    return {'FINISHED'}
  
  #def execute(self, context):
    #print('Adding block')
    ##GEOblock(Block())
    ##addObj(Block())
    ##b = Block
    #bpy.ops.mesh.primitive_cube_add()
    #obj = bpy.context.scene.objects.active
    #obj['LOLO'] = 'pouet'
    #for i 
    
    #b = Block()
    #GEO
    #bpy.context.scene.cursor_location
    ## create object
    #obj = FDTDGeometryObjects_obj.GEOblock_matrix(block.name, rotation_matrix, block.permittivity, block.conductivity)
    #obj['bfdtd_type'] = 'Block'
    #obj['relative_permittivity'] = block.permittivity
    #obj['relative_conductivity'] = block.conductivity
    ##FDTDGeometryObjects_obj.GEOblock(block.name, block.lower, block.upper, block.permittivity, block.conductivity)
    #bpy.context.scene.objects.active = obj
    #bpy.ops.object.group_link(group=group_name)
    #bpy.ops.object.group_link(group='blocks')

    return {'FINISHED'}

class OBJECT_OT_distorted(Operator, AddObjectHelper):
  """Create a new distorted"""
  bl_idname = "fdtd.distorted"
  bl_label = "Add FDTD distorted"
  bl_options = {'REGISTER', 'UNDO', 'PRESET'}

  def execute(self, context):
    print('Adding FDTD distorted')
    return {'FINISHED'}

class OBJECT_OT_sphere(Operator, AddObjectHelper):
  """Create a new sphere"""
  bl_idname = "fdtd.sphere"
  bl_label = "Add FDTD sphere"
  bl_options = {'REGISTER', 'UNDO', 'PRESET'}

  def execute(self, context):
    print('Adding FDTD sphere')
    bfdtd_obj_manager = blender_scripts.modules.FDTDGeometryObjects.FDTDGeometryObjects()
    bfdtd_obj_manager.GEOsphere('BFDTD-Sphere', bpy.context.scene.cursor_location, 1, 0, 4, 0)
    return {'FINISHED'}

class OBJECT_OT_cylinder(Operator, AddObjectHelper):
  """Create a new cylinder"""
  bl_idname = "fdtd.cylinder"
  bl_label = "Add FDTD cylinder"
  bl_options = {'REGISTER', 'UNDO', 'PRESET'}
  
  #centre = FloatVectorProperty(
          #name="centre",
          #default=(1.0, 1.0, 1.0),
          #)

  name = StringProperty(
          name="name",
          default='BFDTD-Cylinder',
          )
  
  location = FloatVectorProperty(
          name="Location",
          subtype='TRANSLATION',
          )
  
  direction = FloatVectorProperty(
          name="direction",
          default=(1.0, 1.0, 1.0),
          )
  
  radius = FloatProperty(
          name="radius",
          default=0.5,
          min=0,
          )
  
  length = FloatProperty(
          name="length",
          default=10,
          min=0,
          )
  
  AABB = BoolProperty(
          name="Axis-Aligned Bounding Box (AABB)",
          default=True,
          )
  
  permittivity = FloatProperty(
          name="permittivity",
          default=4,
          min=0,
          )
  conductivity = FloatProperty(
          name="conductivity",
          default=0,
          min=0,
          )
  
  def invoke(self, context, event):
    self.location = bpy.context.scene.cursor_location
    return self.execute(context)
  
  def draw(self, context):
    layout = self.layout
    box = layout.box()
    #box.prop(self, 'centre')
    box.prop(self, 'name')
    box.prop(self, 'location')
    box.prop(self, 'direction')
    box.prop(self, 'radius')
    box.prop(self, 'length')
    box.prop(self, 'AABB')
    box.prop(self, 'permittivity')
    box.prop(self, 'conductivity')
    return
  
  def execute(self, context):
    fdtd_cylinder = bfdtd.Cylinder()
    fdtd_cylinder.setName(self.name)
    fdtd_cylinder.setLocation(self.location)
    fdtd_cylinder.setInnerRadius(0)
    fdtd_cylinder.setOuterRadius(self.radius)
    fdtd_cylinder.setHeight(self.length)
    fdtd_cylinder.setRelativePermittivity(self.permittivity)
    fdtd_cylinder.setRelativeConductivity(self.conductivity)
    fdtd_cylinder.setAxis(self.direction)
    
    bfdtd_obj_manager = blender_scripts.modules.FDTDGeometryObjects.FDTDGeometryObjects()
    bfdtd_obj_manager.addCylinder(fdtd_cylinder)
    
    if self.AABB:
      minBB, maxBB = fdtd_cylinder.getAABB()
      bfdtd_obj_manager.GEObox('{}.AABB'.format(self.name), minBB, maxBB)
    
    #bfdtd_obj_manager = blender_scripts.modules.FDTDGeometryObjects.FDTDGeometryObjects()
    #pos = bpy.context.scene.cursor_location
    #bpy.ops.mesh.primitive_cylinder_add(location = mathutils.Vector([0,0,0]), rotation=(math.radians(-90),0,0))
    #bpy.ops.object.transform_apply(rotation=True) # aligning cylinder to Y axis directly and applying rotation, to follow BFDTD standard cylinder orientation.
    
    #obj = bpy.context.object
    #name = 
    #rotation_matrix = mathutils.Matrix.Translation(pos)
    #inner_radius = 
    #outer_radius = 
    #height = 
    #permittivity = 
    #conductivity = 
    
    #bfdtd_obj_manager.GEOcylinder_matrix2(obj, name, rotation_matrix, inner_radius, outer_radius, height, permittivity, conductivity)
    
    return {'FINISHED'}

import bpy #needed in a script-text-window!
def fget(self):                                 # custom get function
    """Distance from origin"""                  # description of property
    loc = self.location                         # location of object
    distance = loc.length                       # distance from origin
    return distance                             # return value
 
def fset(self, value):                          # custom set function
    if self.location.length < 1E-6:             # if object is at origin
        self.location = [1, 0, 0]               # direction to move in
    self.location.length = value                # set distance from origin
 
bpy.types.Object.trolling = property(fget, fset)# assign function to property
 
#ob = bpy.context.active_object                  # get the active object
#print(ob.distance)                              # print distance to the console
#ob.distance = 2                                 # set the distance
 
class myPanel(bpy.types.Panel):                 # panel to display new property
    bl_space_type = "VIEW_3D"                   # show up in: 3d-window
    bl_region_type = "UI"                       # show up in: properties panel
    bl_label = "My Panel"                       # name of the new panel
 
    def draw(self, context):
      # display "distance" of the active object
      self.layout.label(text=str(bpy.context.active_object.trolling))

def register():
  bpy.utils.register_class(FDTDMenu)
  #bpy.types.INFO_HT_header.append(draw_item)
  #bpy.types.VIEW3D_HT_header.append(draw_item)
  bpy.types.INFO_MT_add.append(draw_item)

  bpy.utils.register_class(OBJECT_OT_block)
  bpy.utils.register_class(OBJECT_OT_distorted)
  bpy.utils.register_class(OBJECT_OT_sphere)
  bpy.utils.register_class(OBJECT_OT_cylinder)

  #bpy.utils.register_class(myPanel)               # register panel

def unregister():
  bpy.utils.unregister_class(FDTDMenu)
  bpy.types.INFO_HT_header.remove(draw_item)

  bpy.utils.unregister_class(OBJECT_OT_block)
  bpy.utils.unregister_class(OBJECT_OT_distorted)
  bpy.utils.unregister_class(OBJECT_OT_sphere)
  bpy.utils.unregister_class(OBJECT_OT_cylinder)

  #bpy.utils.unregister_class(myPanel)               # register panel

if __name__ == "__main__":
  register()
