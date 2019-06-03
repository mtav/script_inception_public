#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''Script to import .str files (for the Focused Ion Beam for example).

.. todo:: We could add weight paint corresponding to the beam intensity via weights as follows::

            obj=bpy.context.object
            d=obj.data
            v=d.vertices
            v[0].groups[0].weight = N
          
          However, switching to VTK is better in the long term... (and Blender does not show weights as colors if there are no faces...)
'''

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
    'name': 'Import STR Format (.str)',
    'author': 'mtav',
    'version': (0, 0, 1),
    'blender': (2, 63, 0),
    'location': 'File > Import > STR (.str)',
    'description': 'Import files in the STR format (.str)',
    'warning': '',
    'wiki_url': '',
    'tracker_url': '',
    'category': 'Import-Export',
    }

import os
import codecs
import math
import sys
import glob
from math import sin, cos, radians
from mathutils import Vector, Matrix

# ImportHelper is a helper class, defines filename and invoke() function which calls the file selector.
import bpy
import bmesh
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty, FloatVectorProperty
from bpy.types import Operator

from FIB.FIB import readStrFile

def importSTR(filename):
    ''' import STR geometry from .str file and create corresponding structure in Blender '''
    print('----->Importing STR geometry: '+filename)
    
    Xscaling = 1
    Yscaling = 1
    Zscaling = 1

    (repetitions, pointlist) = readStrFile(filename)
    
    [(Zmin,Zmax),(Xmin,Xmax),(Ymin,Ymax)] = [(min(i),max(i)) for i in list(zip(*pointlist))]
    
    if Xmax-Xmin>10 or Ymax-Ymin>10:
        Xscaling = Yscaling = min(Xscaling, 10/max(Xmax-Xmin,Ymax-Ymin))
    
    print([(Zmin,Zmax),(Xmin,Xmax),(Ymin,Ymax)])
    Zscaling = min(Zscaling, 1/(max(Zmax,Zmin)))
    
    print('Xscaling = {}, Yscaling = {}, Zscaling = {}'.format(Xscaling,Yscaling,Zscaling))
    
    mesh = bpy.data.meshes.new(os.path.basename(filename))
    
    bm = bmesh.new()
    
    last = None
    for idx, (dwell,x,y) in enumerate(pointlist):
        A = bm.verts.new((x, y, 0))
        B = bm.verts.new((x, y, -dwell))
        #bm.edges.new((A,B))
        if last is not None:
            bm.edges.new((last,B))
        last = B
    
    bm.to_mesh(mesh)
    mesh.update()
    
    # add the mesh as an object into the scene with this utility module
    from bpy_extras import object_utils
    object_utils.object_data_add(bpy.context, mesh)
    bpy.context.object.scale = (Xscaling, Yscaling, Zscaling)
    
    print('...done')
    return

class ImportSTR(Operator, ImportHelper):
    '''This appears in the tooltip of the operator and in the generated docs'''
    bl_idname = "import_str.str"  # important since its how bpy.ops.import_str.str is constructed
    bl_label = "Import STR"

    # ImportHelper mixing class uses this
    filter_glob = StringProperty(default="*.str")

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.

    def execute(self, context):
        importSTR(self.filepath)
        return {'FINISHED'}

# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
    self.layout.operator(ImportSTR.bl_idname, text="STR (.str)")

def register():
    bpy.utils.register_class(ImportSTR)
    bpy.types.INFO_MT_file_import.append(menu_func_import)

def unregister():
    bpy.utils.unregister_class(ImportSTR)
    bpy.types.INFO_MT_file_import.remove(menu_func_import)

if __name__ == "__main__":
  if len(sys.argv)>4: # CLI call with args
      for i in range(len(sys.argv)- 4):
          print('Importing ' + sys.argv[4+i])
          importSTR(sys.argv[4+i]);
