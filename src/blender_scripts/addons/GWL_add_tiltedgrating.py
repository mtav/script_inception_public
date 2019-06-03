#!/usr/bin/env python3
# -*- coding: utf-8 -*-

bl_info = {
    "name": "tiltedGrating",
    "author": "mtav",
    "version": (1, 0),
    "blender": (2, 65, 0),
    "location": "View3D > Add > Mesh > tiltedGrating",
    "description": "Adds a new tiltedGrating",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Add Mesh"}

# name your mesh
meshname = "tiltedGrating"

import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty, IntProperty, FloatProperty, BoolProperty, StringProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
import bmesh
from blender_scripts.modules import blender_utilities

# Import necessary class here
from GWL.tilted_grating import TiltedGrating

class OBJECT_OT_add_TiltedGrating_idname(Operator, AddObjectHelper):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_tiltedgrating"
    bl_label = "Add tiltedGrating Object"
    bl_description = "Add a new tiltedGrating"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    # Add properties here
    Nlines = IntProperty(name="Nlines", description="Number of lines", default=11, min=1, step=1)
    angle_deg = FloatProperty(name="angle_deg", description="Angle in degrees", default=60, min=0, max=360, step=1)
    line_width = FloatProperty(name="line_width", default=1)
    line_height = FloatProperty(name="line_height", default=2)
    line_length = FloatProperty(name="line_length", default=10)
    period = FloatProperty(name="period", default=2)

    connected = BoolProperty(name="connected", description="connected", default=True)

    def execute(self, context):

        # Create object here
        obj = TiltedGrating()
        obj.Nlines = self.Nlines
        obj.angle_deg = self.angle_deg
        obj.line_width = self.line_width
        obj.line_height = self.line_height
        obj.line_length = self.line_length
        obj.period = self.period
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

def add_tiltedgrating_idname_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_TiltedGrating_idname.bl_idname,
        text="Add tiltedGrating",
        icon='PLUGIN')


# This allows you to right click on a button and link to the manual
def add_tiltedgrating_idname_manual_map():
    url_manual_prefix = "http://wiki.blender.org/index.php/Doc:2.6/Manual/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_tiltedgrating", "Modeling/Objects"),
        )
    return url_manual_prefix, url_manual_mapping


def register():
    bpy.utils.register_class(OBJECT_OT_add_TiltedGrating_idname)
    bpy.utils.register_manual_map(add_tiltedgrating_idname_manual_map)
    bpy.types.INFO_MT_mesh_add.append(add_tiltedgrating_idname_button)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_TiltedGrating_idname)
    bpy.utils.unregister_manual_map(add_tiltedgrating_idname_manual_map)
    bpy.types.INFO_MT_mesh_add.remove(add_tiltedgrating_idname_button)


if __name__ == "__main__":
    register()
