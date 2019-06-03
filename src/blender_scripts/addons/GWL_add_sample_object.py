#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Template for creating GWL object addons.

When creating your own replace the following terms:
  foobar_file : file containing the class for your object
  foobarClass : name of the class for your object
  add_foobar_idname : operator name, must all be lower case
  foobar_name : name of your new object
'''

bl_info = {
    "name": "foobar_name - EXAMPLE ADDON",
    "author": "mtav",
    "version": (1, 0),
    "blender": (2, 65, 0),
    "location": "View3D > Add > Mesh > foobar_name",
    "description": "Adds a new foobar_name",
    "warning": "Example addon.",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Add Mesh"}

# name your mesh
meshname = "foobar_name"

import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty, IntProperty, FloatProperty, BoolProperty, StringProperty, EnumProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
import bmesh

# Import necessary class here
from GWL.foobar_file import foobarClass

class OBJECT_OT_add_foobar_idname(Operator, AddObjectHelper):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_foobar_idname"
    bl_label = "Add foobar_name Object"
    bl_description = "Add a new foobar_name"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    ### Add properties here
    
    # StringProperty
    filter_glob = StringProperty(default="*.geo;*.inp;*.in", options={'HIDDEN'})
    
    # IntProperty
    N = IntProperty(name="N", description="Number of lines", default=5, min=0, max=10, step=1)

    # FloatProperty
    angle_deg = FloatProperty(name="angle_deg", description="Angle in degrees", default=60, min=0, max=360, step=1)

    # BoolProperty
    TopDownWriting = BoolProperty(name="TopDownWriting", description="TopDownWriting", default=True)

    # FloatVectorProperty
    overlap_vec3 = FloatVectorProperty(name="overlap", description="overlap", default=Vector([0,0,0.5]), min=0, max=0.999, step=0.001, precision=3)
    
    # EnumProperty
    method = EnumProperty(items = (("spiral","spiral","spiral bla bla"),
                                   ("vertical lines","vertical lines","vertical lines bla bla"),
                                   ("circles","circles","circles bla bla")),
                                   default='circles',
                                   name = "method",
                                   description = "method")

    def execute(self, context):

        # Create object here
        obj = foobarClass()
        # set object properties to operator properties
        obj.setProperty(self.N)
        obj.N = self.N
        # compute points
        obj.computePoints()
        
        # convert GWLobject to blender mesh
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

def add_foobar_idname_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_foobar_idname.bl_idname,
        text="Add foobar_name",
        icon='PLUGIN')


# This allows you to right click on a button and link to the manual
def add_foobar_idname_manual_map():
    url_manual_prefix = "http://wiki.blender.org/index.php/Doc:2.6/Manual/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_foobar_idname", "Modeling/Objects"),
        )
    return url_manual_prefix, url_manual_mapping


def register():
    bpy.utils.register_class(OBJECT_OT_add_foobar_idname)
    bpy.utils.register_manual_map(add_foobar_idname_manual_map)
    bpy.types.INFO_MT_mesh_add.append(add_foobar_idname_button)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_foobar_idname)
    bpy.utils.unregister_manual_map(add_foobar_idname_manual_map)
    bpy.types.INFO_MT_mesh_add.remove(add_foobar_idname_button)


if __name__ == "__main__":
    register()
