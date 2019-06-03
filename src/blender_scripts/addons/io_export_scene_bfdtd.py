#!/usr/bin/env python3
# -*- coding: utf-8 -*-

bl_info = {
    'name': 'Export BristolFDTD Format (.geo,.inp,.in) - EXPERIMENTAL',
    'author': 'mtav',
    'version': (0, 0, 1),
    'blender': (2, 63, 0),
    'location': 'File > Export > BristolFDTD (.geo,.inp,.in)',
    'description': 'Export files to the BristolFDTD format (.geo,.inp,.in)',
    'warning': 'Under construction!',
    'wiki_url': '',
    'tracker_url': '',
    'category': 'Import-Export',
    }

import os
import bpy
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator
from bfdtd.BFDTDobject import BFDTDobject
from bfdtd.GeometryObjects import Block, Cylinder, Sphere
from blender_scripts.modules import blender_utilities

# .. todo:: fix export order

class dialog_files_exist(bpy.types.Operator):
    bl_idname = "wm.dialog_files_exist"
    bl_label = "Files exist. Refusing to overwrite."
    def execute(self, context):
        return {'FINISHED'}
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
class ExportBristolFDTD(Operator, ExportHelper):
    """ Blender operator for exporting to the BFDTD format """
    bl_idname = "export_bfdtd.bfdtd"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Export BristolFDTD"
    bl_options = {'REGISTER', 'PRESET'}

    # ExportHelper mixin class uses this
    filename_ext = ""
    #filename_ext = ".txt"

    filter_glob = StringProperty(default="*.geo;*.inp;*.in", options={'HIDDEN'})

    filename = StringProperty(
            name="filename",
            description="filename used for exporting the file",
            maxlen=1024,
            )

    directory = StringProperty(
            name="directory",
            description="directory used for exporting the file",
            maxlen=1024,
            )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    write_geo = BoolProperty(name="write .geo", description="write .geo", default=True)
    write_inp = BoolProperty(name="write .inp", description="write .inp", default=True)
    write_in = BoolProperty(name="write .in", description="write .in", default=True)
    write_sh = BoolProperty(name="write .sh", description="write .sh", default=True)

    overwrite = BoolProperty(name="overwrite if files exist", description="overwrite if files exist", default=False)

    def execute(self, context):
      # .. todo:: Add option to write out box or not... (and maybe always put box in separate file?)
      print('---> Exporting to {}'.format(self.filepath))
      print('filepath = {}'.format(self.filepath))
      print('filename = {}'.format(self.filename))
      print('directory = {}'.format(self.directory))

      geofile = self.filepath + '.geo'
      inpfile = self.filepath + '.inp'
      infile = self.filepath + '.in'
      shfile = self.filepath + '.sh'

      files_exist = False
      if self.write_geo and os.path.exists(geofile): files_exist = True
      if self.write_inp and os.path.exists(inpfile): files_exist = True
      if self.write_in and os.path.exists(infile): files_exist = True
      if self.write_sh and os.path.exists(shfile): files_exist = True
      
      if files_exist and not self.overwrite:
        bpy.ops.wm.dialog_files_exist('INVOKE_DEFAULT')
        return {'CANCELLED'}
      else:

        obj_list = list(context.selected_objects)

        bfdtd_obj = BFDTDobject()
        bfdtd_obj.setFileBaseName(self.filename)

        for blender_obj in obj_list:
            if 'bfdtd_type' in blender_obj.keys():
              object_function = eval(blender_obj['bfdtd_type'])
              b = object_function()
              b.setName(blender_obj.name)
              
              #if 'location' in blender_obj.keys():
                #b.setLocation(blender_obj['location'])
              #else:
                #b.setLocation(list(blender_obj.location))
              
              b.setLocation(list(blender_obj.location)) # using the location seen in blender is closer to what the user expects... (should be an option)
              
              #if blender_obj['bfdtd_type'] == 'Sphere' and 'outer_radius' in blender_obj.keys():
              # .. todo:: link size in blender to outer_radius variable...
              if isinstance(b, Sphere) and 'outer_radius' in blender_obj.keys():
                b.setOuterRadius(blender_obj['outer_radius'])
              else:
                b.setSize(list(blender_obj.dimensions))
              
              blender_obj.rotation_mode = 'AXIS_ANGLE'
              b.setRotationAxisAngle(list(blender_obj.rotation_axis_angle))
              
              if 'relative_permittivity' in blender_obj.keys():
                b.setRelativePermittivity(blender_obj['relative_permittivity'])
                
              if 'relative_conductivity' in blender_obj.keys():            
                b.setRelativeConductivity(blender_obj['relative_conductivity'])
              
              bfdtd_obj.appendGeometryObject(b)
              result = 'OK'
            else:
              result = 'FAIL: bfdtd_type not defined.'
            print('Adding {}: {}'.format(blender_obj.name, result))
        
        if self.write_geo:
          bfdtd_obj.writeGeoFile(geofile, overwrite=self.overwrite, withBox=False)
        if self.write_inp:
          bfdtd_obj.writeInpFile(inpfile, overwrite=self.overwrite)
        if self.write_in:
          bfdtd_obj.writeFileList(infile, overwrite=self.overwrite)
        if self.write_sh:
          bfdtd_obj.writeShellScript(shfile, overwrite=self.overwrite)

      print('DONE')      
      return {'FINISHED'}

# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(ExportBristolFDTD.bl_idname, text="BristolFDTD (.geo,.inp,.in)")

def register():
    bpy.utils.register_class(dialog_files_exist)
    bpy.utils.register_class(ExportBristolFDTD)
    bpy.types.INFO_MT_file_export.append(menu_func_export)

def unregister():
    bpy.utils.unregister_class(dialog_files_exist)
    bpy.utils.unregister_class(ExportBristolFDTD)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)

if __name__ == "__main__":
    register()
