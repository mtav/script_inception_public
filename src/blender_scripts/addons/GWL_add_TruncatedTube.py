#!/usr/bin/env python3
# -*- coding: utf-8 -*-

bl_info = {
    "name": "TruncatedTube",
    "author": "mtav",
    "version": (1, 0),
    "blender": (2, 65, 0),
    "location": "View3D > Add > Mesh > TruncatedTube",
    "description": "Adds a new TruncatedTube",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Add Mesh"}

# name your mesh
meshname = "TruncatedTube"

import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty, IntProperty, FloatProperty, BoolProperty, StringProperty, EnumProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
import bmesh
from blender_scripts.modules import blender_utilities

# Import necessary class here
from GWL.tube import TruncatedTube

class OBJECT_OT_add_truncated_tube(Operator, AddObjectHelper):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_truncated_tube"
    bl_label = "Add TruncatedTube Object"
    bl_description = "Add a new TruncatedTube"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    # Add properties here
    #N = IntProperty(name="N", description="Number of lines", default=5, min=0, max=10, step=1)
    #PointDistance = FloatVectorProperty(name="PointDistance", description="PointDistance (r, theta, z)", default=Vector([0.150,0.150,0.450]), min=0, step=0.001, precision=3)
    
    voxel_width = FloatProperty(name="voxel_width", description="voxel_width", default=0.100, min=0)
    voxel_height = FloatProperty(name="voxel_height", description="voxel_height", default=0.200, min=0)
    inner_radius = FloatProperty(name="inner_radius", description="inner_radius", default=0.5, min=0)
    outer_radius = FloatProperty(name="outer_radius", description="outer_radius", default=1, min=0)
    height = FloatProperty(name="height", description="height", default=1, min=0)
    truncationDistanceFromCentro = FloatProperty(name="truncationDistanceFromCentro", description="truncationDistanceFromCentro", default=0.7)
    closed_loop = BoolProperty(name="closed_loop", description="close circles", default=False)

    def execute(self, context):

        # Create object here
        obj = TruncatedTube()
        #obj.centro = self.centro
        obj.voxel_width = self.voxel_width
        obj.voxel_height = self.voxel_height
        obj.inner_radius = self.inner_radius
        obj.outer_radius = self.outer_radius
        obj.height = self.height
        obj.truncationDistanceFromCentro = self.truncationDistanceFromCentro
        obj.closed_loop = self.closed_loop
        
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

def add_truncated_tube_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_truncated_tube.bl_idname,
        text="Add TruncatedTube",
        icon='PLUGIN')


# This allows you to right click on a button and link to the manual
def add_truncated_tube_manual_map():
    url_manual_prefix = "http://wiki.blender.org/index.php/Doc:2.6/Manual/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_truncated_tube", "Modeling/Objects"),
        )
    return url_manual_prefix, url_manual_mapping


def register():
    bpy.utils.register_class(OBJECT_OT_add_truncated_tube)
    bpy.utils.register_manual_map(add_truncated_tube_manual_map)
    bpy.types.INFO_MT_mesh_add.append(add_truncated_tube_button)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_truncated_tube)
    bpy.utils.unregister_manual_map(add_truncated_tube_manual_map)
    bpy.types.INFO_MT_mesh_add.remove(add_truncated_tube_button)


if __name__ == "__main__":
    register()
