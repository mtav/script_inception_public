#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# How to add a menu and more: https://blender.stackexchange.com/questions/292694/how-can-i-add-a-custom-menu-entry-to-the-topbar-of-the-3d-viewport

bl_info = {
    "name": "SIP menu",
    "author": "mtav",
    "version": (1, 0),
    "blender": (3, 4, 0),
    "location": "View3D -> SIP menu",
    "description": "Adds a new SIP menu for easy access to some operators.",
    "warning": "",
    "wiki_url": "",
    "category": "Object"}

import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty, BoolProperty, FloatProperty, IntProperty, EnumProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
from blender_scripts.modules.blender_utilities import setOrigin, selectObjects, add_array_modifier
from blender_scripts.modules.GeometryObjects import add_cylinder, add_tetra

#from import OBJECT_OT_add_arrow
import addon_add_arrow

class Create_SIP_Menu(bpy.types.Menu):
  bl_label = "SIP"
  bl_idname = "VIEW3D_MT_SIP"

  bl_space_type = "VIEW_3D"
  # bl_region_type = "TOOLS"
  bl_context = "objectmode"
  bl_category = "SIP"

  def draw(self, context):
    TheCol = self.layout.column(align=True)
    TheCol.operator("object.align_with_axis", text="Align with axis")
    TheCol.operator("object.create_3d_array", text="Create 3D array")
    TheCol.operator("object.create_rcd111_waveguide", text="Create RCD111 waveguide")
    TheCol.operator(addon_add_arrow.OBJECT_OT_add_arrow.bl_idname, text=addon_add_arrow.OBJECT_OT_add_arrow.bl_label)
    TheCol.operator("object.set_weights_to_vertex_indices", text="Set weights to vertex index")

def draw_item(self, context):
    layout = self.layout
    layout.menu(Create_SIP_Menu.bl_idname)

def register():
    bpy.utils.register_class(Create_SIP_Menu)
    bpy.types.VIEW3D_MT_editor_menus.append(draw_item)

def unregister():
    bpy.utils.unregister_class(Create_SIP_Menu)
    bpy.types.VIEW3D_MT_editor_menus.remove(draw_item)

if __name__ == "__main__":
  register()
