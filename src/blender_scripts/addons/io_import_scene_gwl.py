#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
.. todo:: Documentation
.. todo:: Cleanup
.. todo:: import options
.. todo:: Compare class vs module, different ways of creating addons, choose best
.. todo:: Figure out how to enable the addon directly after installation
"""

# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    'name': 'Import GWL Format (.gwl)',
    'author': 'mtav',
    'version': (2022, 8, 3),
    'blender': (3, 2, 0),
    'location': 'File > Import > GWL (.gwl)',
    'description': 'Import files in the GWL format (.gwl)',
    'warning': '',
    'wiki_url': '',
    'tracker_url': '',
    'category': 'Import-Export',
    }

import os
import codecs
import math
from math import sin, cos, radians
import bpy
from mathutils import Vector, Matrix
from blender_scripts.modules.GWL_import import *

# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator

class ImportGWL(Operator, ImportHelper):
    '''This appears in the tooltip of the operator and in the generated docs'''
    bl_idname = "import_gwl.gwl"  # important since its how bpy.ops.import_gwl.gwl is constructed
    bl_label = "Import GWL"

    # ImportHelper mixin class uses this
    filter_glob = StringProperty(default="*.gwl", options={'HIDDEN'})

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    use_setting = BoolProperty(
            name="Example Boolean",
            description="Example Tooltip",
            default=True,
            )

    type = EnumProperty(
            name="Example Enum",
            description="Choose between two items",
            items=(('OPT_A', "First Option", "Description one"),
                   ('OPT_B', "Second Option", "Description two")),
            default='OPT_A',
            )

    def execute(self, context):
        #return test(context, self.filepath, self.use_setting)
        importGWL(self.filepath)
        return {'FINISHED'}

# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
    self.layout.operator(ImportGWL.bl_idname, text="GWL (.gwl)")

def register():
    print('registering ', os.path.basename(__file__))
    bpy.utils.register_class(ImportGWL)
    if bpy.app.version >= (2, 80, 0):
      bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    else:
      bpy.types.INFO_MT_file_import.append(menu_func_import)
      raise

def unregister():
    print('unregistering ', os.path.basename(__file__))
    bpy.utils.unregister_class(ImportGWL)
    if bpy.app.version >= (2, 80, 0):
      bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    else:
      bpy.types.INFO_MT_file_import.remove(menu_func_import)
      raise

if __name__ == "__main__":
    print('main:', os.path.basename(__file__))
    register()
    # test call
    bpy.ops.import_gwl.gwl('INVOKE_DEFAULT')
