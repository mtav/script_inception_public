#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Basic example script to add a tab to the tool shelf on the left in the view3D window. (press T to make it appear)
For Blender 2.79.
'''

bl_info = {
    "name": "SIP panel for Blender 2.79",
    "author": "mtav",
    "version": (1, 0),
    "blender": (2, 79, 0),
    "location": "View3D > Tool shelf -> SIP", # Add a tab to the tool shelf on the left in the view3D window. (press T to make it appear)
    "description": "Blender 2.79 specific. Adds a new SIP tab for easy access to some operators.",
    "warning": "Not compatible with Blender >2.79",
    "wiki_url": "",
    "category": "Object"}

import bpy

class Create_SIP_Panel(bpy.types.Panel):
  bl_space_type = "VIEW_3D"
  bl_region_type = "TOOLS"
  bl_context = "objectmode"
  bl_category = "SIP"
  bl_label = "SIP"

  def draw(self, context):
    TheCol = self.layout.column(align=True)
    TheCol.operator("mesh.primitive_plane_add", text='My secret operator.')
    
def register():
  bpy.utils.register_class(Create_SIP_Panel)

def unregister():
  bpy.utils.unregister_class(Create_SIP_Panel)

if __name__ == "__main__":
  register()
