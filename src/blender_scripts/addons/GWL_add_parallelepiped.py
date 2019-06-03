#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
.. todo:: Finish implementing option to get the size arguments from the e1,e2,e3 vectors.
.. todo:: Finish implementing start-end point method (unless it was meant to be the same as above?)
'''

bl_info = {
    "name": "parallelepiped",
    "author": "mtav",
    "version": (1, 0),
    "blender": (2, 65, 0),
    "location": "View3D > Add > Mesh > parallelepiped",
    "description": "Adds a new parallelepiped",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Add Mesh"}

# name your mesh
meshname = "parallelepiped"

import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty, IntVectorProperty, IntProperty, FloatProperty, BoolProperty, StringProperty, EnumProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
import bmesh

# Import necessary class here
from GWL.parallelepiped import Parallelepiped

class OBJECT_OT_add_parallelepiped_idname(Operator, AddObjectHelper):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_parallelepiped"
    bl_label = "Add parallelepiped Object"
    bl_description = "Add a new parallelepiped"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    # Add properties here
    
    # to help with the use of related properties
    updating = BoolProperty(name="updating", default=False)
    
    def updateSize(self, context):
      if not self.updating:
        if self.size_from_vectors:
          self.updating = True
          
          e1_vec3 = Vector(self.e1_vec3)
          e2_vec3 = Vector(self.e2_vec3)
          e3_vec3 = Vector(self.e3_vec3)
          
          e1_vec3.length = self.size_vec3[0]
          e2_vec3.length = self.size_vec3[1]
          e3_vec3.length = self.size_vec3[2]
          
          self.e1_vec3 = Vector(e1_vec3)
          self.e2_vec3 = Vector(e2_vec3)
          self.e3_vec3 = Vector(e3_vec3)
          
          self.updating = False

    def updateDirections(self, context):
      if not self.updating:
        if self.size_from_vectors:
          self.updating = True
          self.size_vec3[0] = Vector(self.e1_vec3).length
          self.size_vec3[1] = Vector(self.e2_vec3).length
          self.size_vec3[2] = Vector(self.e3_vec3).length
          self.updating = False

    method = EnumProperty(items = (("e1,e2,e3","e1,e2,e3","define the parallelepiped by specifying the edge vectors e1,e2,e3"),
                                   ("start-end point","start-end point","define the parallelepiped by specifying a start and end point")),
                          default='e1,e2,e3',
                          name = "method",
                          description = "method")

    e1_vec3 = FloatVectorProperty(name="e1", description="e1", default=Vector((1,0,0)), precision=3, update=updateDirections)
    e2_vec3 = FloatVectorProperty(name="e2", description="e2", default=Vector((0,1,0)), precision=3, update=updateDirections)
    e3_vec3 = FloatVectorProperty(name="e3", description="e3", default=Vector((0,0,1)), precision=3, update=updateDirections)

    size_vec3 = FloatVectorProperty(name="size", description="size", default=Vector((1,1,1)), precision=3, min=0, update=updateSize)
    
    size_from_vectors = BoolProperty(name="Sync size from/to e1,e2,e3 vectors", description="Sync size from/to e1,e2,e3 vectors", default=True)

    LineNumber_method = EnumProperty(items = (("use_line_number","use line number","use line number"),
                                              ("use_voxelsize_and_linedistance","use voxelsize and linedistance","use voxelsize and linedistance")),
                          default = 'use_line_number',
                          name = "line number method",
                          description = "line number method")

    voxelsize_vec3 = FloatVectorProperty(name="voxelsize", description="voxelsize", default=Vector([0.150,0.150,0.450]), min=0, step=0.001, precision=3)
    overlap_vec3 = FloatVectorProperty(name="overlap", description="overlap", default=Vector([0,0,0.5]), min=0, max=0.999, step=0.001, precision=3)

    LineNumber_vec3 = IntVectorProperty(name="Line number", description="Line number", default=Vector(Parallelepiped.LineNumber_vec3), min=0)

    connected = BoolProperty(name="connected", description="connected", default=True)

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.prop(self, 'e1_vec3')
        box.prop(self, 'e2_vec3')
        box.prop(self, 'e3_vec3')
        box.prop(self, 'size_vec3')
        box.prop(self, 'size_from_vectors')

        box.prop(self, 'connected')

        box.prop(self, 'LineNumber_method')
        if self.LineNumber_method == 'use_voxelsize_and_linedistance':
          box.prop(self, 'voxelsize_vec3')
          box.prop(self, 'overlap_vec3')
        else:
          box.prop(self, 'LineNumber_vec3')
          
        box_common = layout.box()
        box_common.prop(self, 'location')
        box_common.prop(self, 'rotation')
        box_common.prop(self, 'view_align')

    def execute(self, context):

      # Create object here
      obj = Parallelepiped()
      
      obj.size_vec3 = self.size_vec3
      obj.e1_vec3 = self.e1_vec3
      obj.e2_vec3 = self.e2_vec3
      obj.e3_vec3 = self.e3_vec3
      
      #if self.
      obj.voxelsize_vec3 = self.voxelsize_vec3
      obj.overlap_vec3 = self.overlap_vec3
      obj.LineNumber_vec3 = self.LineNumber_vec3
      
      obj.connected = self.connected
      
      verts_loc, edges, faces = obj.getMeshData()

      mesh = bpy.data.meshes.new(name = meshname)
      mesh.from_pydata(verts_loc, edges, faces)
      # useful for development when the mesh may be invalid.
      # mesh.validate(verbose=True)

      # add the mesh as an object into the scene with this utility module
      from bpy_extras import object_utils
      object_utils.object_data_add(context, mesh, operator=self)

      return {'FINISHED'}

# Registration

def add_parallelepiped_idname_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_parallelepiped_idname.bl_idname,
        text="Add parallelepiped",
        icon='PLUGIN')


# This allows you to right click on a button and link to the manual
def add_parallelepiped_idname_manual_map():
    url_manual_prefix = "http://wiki.blender.org/index.php/Doc:2.6/Manual/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_parallelepiped", "Modeling/Objects"),
        )
    return url_manual_prefix, url_manual_mapping


def register():
    bpy.utils.register_class(OBJECT_OT_add_parallelepiped_idname)
    bpy.utils.register_manual_map(add_parallelepiped_idname_manual_map)
    bpy.types.INFO_MT_mesh_add.append(add_parallelepiped_idname_button)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_parallelepiped_idname)
    bpy.utils.unregister_manual_map(add_parallelepiped_idname_manual_map)
    bpy.types.INFO_MT_mesh_add.remove(add_parallelepiped_idname_button)


if __name__ == "__main__":
    register()
