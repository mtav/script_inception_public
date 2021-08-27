#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
    'name': 'Import BristolFDTD Format (.geo,.inp,.in)',
    'author': 'mtav',
    'version': (0, 0, 2),
    'blender': (2, 83, 0),
    'location': 'File > Import > BristolFDTD (.geo,.inp,.in)',
    'description': 'Import files in the BristolFDTD format (.geo,.inp,.in)',
    'wiki_url': '',
    'tracker_url': '',
    'category': 'Import-Export',
    }

"""
TODO: Documentation
TODO: Cleanup
TODO: import options
TODO: Compare class vs module, different ways of creating addons, choose best
TODO: Figure out how to enable the addon directly after installation
TODO: Implement progress bar! (cf: 2.68/scripts/addons/ui_translate/update_svn.py, progress_begin(min, max), progress_update(value), progress_end())
"""

import os
import codecs
import math
from math import sin, cos, radians
import bpy
from mathutils import Vector, Matrix
from blender_scripts.modules.bfdtd_import import addObjectsByDuplication, BristolFDTDimporter
from blender_scripts.modules import blender_utilities

# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy.props import (StringProperty,
                       BoolProperty,
                       CollectionProperty,
                       EnumProperty,
                       FloatProperty,
                       IntProperty
                       )
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator, OperatorFileListElement

class ImportBristolFDTD(Operator, ImportHelper):
    '''
    Import BristolFDTD geometry from .in, .geo or .inp and create corresponding structure in Blender
    .. note:: Blender does not like descriptions ending with a dot ('.').
              cf: http://www.letworyinteractive.com/blendercode/dc/d7e/rna__define_8c_source.html
              00058 /* pedantic check for '.', do this since its a hassle for translators */
    '''
    bl_idname = "import_bfdtd.bfdtd"  # important since its how bpy.ops.import_bfdtd.bfdtd is constructed
    bl_label = "Import BristolFDTD"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    # ImportHelper mixin class uses this
    filter_glob = StringProperty(default="*.geo;*.inp;*.in", options={'HIDDEN'})

    # to enable multi-file import
    files = CollectionProperty(
            name="File Path",
            type=OperatorFileListElement,
            )

    directory = StringProperty(
            subtype='DIR_PATH',
            )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    use_placeholder = BoolProperty(
            name="Use placeholder",
            description="Use a placeholder for objects to increase import speed",
            default=False,
            )
    
    cylinder_to_line_mesh = BoolProperty(
            name="cylinders->line-mesh",
            description="Create a single line mesh from cylinders",
            default=True,
            )
    
    create_vertex_mesh = BoolProperty(
            name="Objects -> vertex mesh",
            description="Import all objects into single vertex-based mesh, where vertex position = object position",
            default=False,
            )
    
    placeholder_type = EnumProperty(
            name="Placeholder type",
            description="Choose between two items",
            items=(
                    ('first_imported_object', "first imported object", "first imported object"),
                    ('oriented', "Oriented placeholder", "Oriented placeholder (base vectors)"),
                    ('sphere', "Non-oriented placeholder", "Non-oriented placeholder (Sphere)"),
                  ),
            default='first_imported_object',
            )

    restrict_import_volume = BoolProperty(name="Restrict import volume", description="Restrict import volume to increase import speed", default=False)

    volume_specification_style = EnumProperty(items = (
      ("min-max-relative", "min-max-relative", "min-max-relative"),
      ("centre-size-relative","centre-size-relative","centre-size-relative"),
      ("min-max-absolute", "min-max-absolute", "min-max-absolute"),
      ("centre-size-absolute","centre-size-absolute","centre-size-absolute"),
      ),
      default='centre-size-relative', name = "volume_specification_style")

    xmin = FloatProperty(name="xmin", default=0)
    xmax = FloatProperty(name="xmax", default=1)
    ymin = FloatProperty(name="ymin", default=0)
    ymax = FloatProperty(name="ymax", default=1)
    zmin = FloatProperty(name="zmin", default=0)
    zmax = FloatProperty(name="zmax", default=1)

    centre_x = FloatProperty(name="centre_x", default=0.5)
    centre_y = FloatProperty(name="centre_y", default=0.5)
    centre_z = FloatProperty(name="centre_z", default=0.5)
    size_x = FloatProperty(name="size_x", default=1/10)
    size_y = FloatProperty(name="size_y", default=1/10)
    size_z = FloatProperty(name="size_z", default=1/10)
    
    pre_2008_BFDTD_version = BoolProperty(name="BFDTD version < 2008", description="Use the old snapshot indexing system", default=False)

    import_cylinders = BoolProperty(name="Import cylinders", description="Import cylinders", default=True)
    import_blocks = BoolProperty(name="Import blocks", description="Import blocks", default=True)

    numbered_prefixes = BoolProperty(name="Numbered prefixes", description="Use numbered prefixes in case of multiple files", default=True)
    
    use_Nmax_objects = BoolProperty(name="Limit number of imported objects", description="Limit number of imported objects", default=True)
    Nmax_objects = IntProperty(name="Maximum number of objects", default=500)

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        
        box.prop(self, 'pre_2008_BFDTD_version')
        
        box.prop(self, 'create_vertex_mesh')
        
        box.prop(self, 'use_placeholder')
        if self.use_placeholder:
          box.prop(self, 'placeholder_type')

        box.prop(self, 'cylinder_to_line_mesh')

        box.prop(self, 'use_Nmax_objects')
        if self.use_Nmax_objects:
          box.prop(self, 'Nmax_objects')
        
        box.prop(self, 'restrict_import_volume')
        if self.restrict_import_volume:
          box.prop(self, 'volume_specification_style')
          if self.volume_specification_style == 'min-max-relative':
            box.prop(self, 'xmin')
            box.prop(self, 'xmax')
            box.prop(self, 'ymin')
            box.prop(self, 'ymax')
            box.prop(self, 'zmin')
            box.prop(self, 'zmax')
          elif self.volume_specification_style == 'centre-size-relative':
            box.prop(self, 'centre_x')
            box.prop(self, 'centre_y')
            box.prop(self, 'centre_z')
            box.prop(self, 'size_x')
            box.prop(self, 'size_y')
            box.prop(self, 'size_z')
          elif self.volume_specification_style == 'min-max-absolute':
            box.prop(self, 'xmin')
            box.prop(self, 'xmax')
            box.prop(self, 'ymin')
            box.prop(self, 'ymax')
            box.prop(self, 'zmin')
            box.prop(self, 'zmax')
          elif self.volume_specification_style == 'centre-size-absolute':
            box.prop(self, 'centre_x')
            box.prop(self, 'centre_y')
            box.prop(self, 'centre_z')
            box.prop(self, 'size_x')
            box.prop(self, 'size_y')
            box.prop(self, 'size_z')
          else:
            raise
        
        box.prop(self, 'import_cylinders')
        box.prop(self, 'import_blocks')
        box.prop(self, 'numbered_prefixes')

    def execute(self, context):
        paths = [os.path.join(self.directory, name.name)
                 for name in self.files]

        importer = BristolFDTDimporter()
        
        importer.use_placeholder = self.use_placeholder
        importer.placeholder_type = self.placeholder_type
        importer.restrict_import_volume = self.restrict_import_volume
        importer.cylinder_to_line_mesh = self.cylinder_to_line_mesh
        
        if 'min-max' in self.volume_specification_style:
          importer.xmin = self.xmin
          importer.xmax = self.xmax
          importer.ymin = self.ymin
          importer.ymax = self.ymax
          importer.zmin = self.zmin
          importer.zmax = self.zmax
        else:
          importer.xmin = self.centre_x - self.size_x/2
          importer.xmax = self.centre_x + self.size_x/2
          importer.ymin = self.centre_y - self.size_y/2
          importer.ymax = self.centre_y + self.size_y/2
          importer.zmin = self.centre_z - self.size_z/2
          importer.zmax = self.centre_z + self.size_z/2
        
        if 'relative' in self.volume_specification_style:
          importer.volume_specification_style = 'relative'
        else:
          importer.volume_specification_style = 'absolute'
        
        importer.pre_2008_BFDTD_version = self.pre_2008_BFDTD_version        
        importer.import_cylinders = self.import_cylinders
        importer.import_blocks = self.import_blocks
        importer.GUI_loaded = True
        importer.numbered_prefixes = self.numbered_prefixes
        importer.use_Nmax_objects = self.use_Nmax_objects
        importer.Nmax_objects = self.Nmax_objects
        importer.create_vertex_mesh = self.create_vertex_mesh
        
        importer.importBristolFDTD(paths)
        
        return {'FINISHED'}

# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
    self.layout.operator(ImportBristolFDTD.bl_idname, text="BristolFDTD (.geo,.inp,.in)")

def register():
    bpy.utils.register_class(ImportBristolFDTD)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister():
    bpy.utils.unregister_class(ImportBristolFDTD)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

if __name__ == "__main__":
    register()
    # test call
    bpy.ops.import_bfdtd.bfdtd('INVOKE_DEFAULT')
