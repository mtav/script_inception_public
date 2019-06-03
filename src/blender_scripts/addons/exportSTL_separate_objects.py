#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# <pep8-80 compliant>

bl_info = {
    "name": "Export to STL format (with optionally one file per object)",
    "author": "mtav",
    "version": (1, 0),
    "blender": (2, 57, 0),
    "location": "File > Export > Stl",
    "description": "Export each selected object to its own .stl file",
    "warning": "",
    "category": "Import-Export",
}

if "bpy" in locals():
    import imp
    if "stl_utils" in locals():
        imp.reload(stl_utils)
    if "blender_utils" in locals():
        imp.reload(blender_utils)

import os

import bpy
from bpy.props import (StringProperty,
                       BoolProperty,
                       CollectionProperty,
                       EnumProperty,
                       FloatProperty,
                       )
from bpy_extras.io_utils import (ImportHelper,
                                 ExportHelper,
                                 axis_conversion,
                                 )
from bpy.types import Operator, OperatorFileListElement

from io_mesh_stl import stl_utils
from io_mesh_stl import blender_utils
import itertools
from mathutils import Matrix

class ExportSTLseparateObjects(Operator, ExportHelper):
    """Save STL triangle mesh data from the active object"""
    bl_idname = "export_mesh.stl_multiple"
    bl_label = "Export STL (multiple files)"

    filename_ext = ".stl"
    filter_glob = StringProperty(default="*.stl", options={'HIDDEN'})

    ascii = BoolProperty(
            name="Ascii",
            description="Save the file in ASCII file format",
            default=False,
            )

    one_file_per_object = BoolProperty(
            name="one_file_per_object",
            description="one file per object",
            default=True,
            )

    use_mesh_modifiers = BoolProperty(
            name="Apply Modifiers",
            description="Apply the modifiers before saving",
            default=True,
            )

    axis_forward = EnumProperty(
            name="Forward",
            items=(('X', "X Forward", ""),
                   ('Y', "Y Forward", ""),
                   ('Z', "Z Forward", ""),
                   ('-X', "-X Forward", ""),
                   ('-Y', "-Y Forward", ""),
                   ('-Z', "-Z Forward", ""),
                   ),
            default='Y',
            )
    axis_up = EnumProperty(
            name="Up",
            items=(('X', "X Up", ""),
                   ('Y', "Y Up", ""),
                   ('Z', "Z Up", ""),
                   ('-X', "-X Up", ""),
                   ('-Y', "-Y Up", ""),
                   ('-Z', "-Z Up", ""),
                   ),
            default='Z',
            )
    global_scale = FloatProperty(
            name="Scale",
            min=0.01, max=1000.0,
            default=1.0,
            )

    def execute(self, context):
        keywords = self.as_keywords(ignore=("axis_forward",
                                            "axis_up",
                                            "global_scale",
                                            "check_existing",
                                            "filter_glob",
                                            "use_mesh_modifiers",
                                            ))

        global_matrix = axis_conversion(to_forward=self.axis_forward,
                                        to_up=self.axis_up,
                                        ).to_4x4() * Matrix.Scale(self.global_scale, 4)

        if self.one_file_per_object:
          basepath = os.path.splitext(self.filepath)[0]
          os.mkdir(basepath)
          print('Exporting multiple .stl files into {}'.format(basepath))
          for ob in context.selected_objects:
            stlfile = basepath + os.sep + ob.name + '.stl'
            print(stlfile)
            keywords = {'filepath': stlfile, 'ascii': self.ascii}
            faces = itertools.chain.from_iterable( blender_utils.faces_from_mesh(ob, global_matrix, self.use_mesh_modifiers) for ob in [ob])
            stl_utils.write_stl(faces=faces, **keywords)
        else:
          faces = itertools.chain.from_iterable( blender_utils.faces_from_mesh(ob, global_matrix, self.use_mesh_modifiers) for ob in context.selected_objects)
          stl_utils.write_stl(faces=faces, **keywords)

        return {'FINISHED'}

def menu_export(self, context):
    default_path = os.path.splitext(bpy.data.filepath)[0]
    self.layout.operator(ExportSTLseparateObjects.bl_idname, text="Stl (.stl) (multiple files)")

def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_file_export.append(menu_export)

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_file_export.remove(menu_export)


if __name__ == "__main__":
    register()
