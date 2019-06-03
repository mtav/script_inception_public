#!/usr/bin/env python3
# -*- coding: utf-8 -*-

bl_info = {
    "name": "tube",
    "author": "mtav",
    "version": (1, 0),
    "blender": (2, 65, 0),
    "location": "View3D > Add > Mesh > tube",
    "description": "Adds a new tube",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Add Mesh"}

# name your mesh
meshname = "tube"

import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty, IntProperty, FloatProperty, BoolProperty, StringProperty, EnumProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
import bmesh
from blender_scripts.modules import blender_utilities

# Import necessary class here
from GWL.tube import Tube

class OBJECT_OT_add_tube_idname(Operator, AddObjectHelper):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_tube"
    bl_label = "Add tube Object"
    bl_description = "Add a new tube"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    # Add properties here
    inner_radius = FloatProperty(name="inner_radius", description="inner_radius", default=1, min=0)
    outer_radius = FloatProperty(name="outer_radius", description="outer_radius", default=2, min=0)
    height = FloatProperty(name="height", description="height", default=3, min=0)
    method = EnumProperty(items = (("spiral","spiral","spiral bla bla"),
                                   ("vertical lines","vertical lines","vertical lines bla bla"),
                                   ("circles","circles","circles bla bla")), default='circles',
                          name = "method",
                          description = "method")

    PointDistance = FloatVectorProperty(name="PointDistance", description="PointDistance (r, theta, z)", default=Vector([0.150,0.150,0.450]), min=0, step=0.001, precision=3)
    
    downwardWriting = BoolProperty(name="downwardWriting", description="downwardWriting", default=True)
    zigzag = BoolProperty(name="zigzag", description="zigzag", default=True)
    rotateSpirals = BoolProperty(name="rotateSpirals", description="rotateSpirals", default=False)
    add_flat_ends = BoolProperty(name="add_flat_ends", description="add flat ends", default=False)
    closed_loop = BoolProperty(name="closed_loop", description="close circles", default=False)

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.prop(self, 'location')
        box.prop(self, 'inner_radius')
        box.prop(self, 'outer_radius')
        box.prop(self, 'height')
        box.prop(self, 'method')
        box.prop(self, 'PointDistance')
        box.prop(self, 'downwardWriting')
        box.prop(self, 'closed_loop')
        if self.method == 'vertical lines':
          box.prop(self, 'zigzag')
        if self.method == 'spiral':
          box.prop(self, 'rotateSpirals')
          box.prop(self, 'add_flat_ends')
        
    def execute(self, context):

        # Create object here
        obj = Tube()
        #obj.centro = self.location # not passed, since blender already takes care of the relative mesh location
        obj.inner_radius = self.inner_radius
        obj.outer_radius = self.outer_radius
        obj.height = self.height
        obj.method = self.method
        obj.PointDistance_r = self.PointDistance[0]
        obj.PointDistance_theta = self.PointDistance[1]
        obj.PointDistance_z = self.PointDistance[2]
        obj.downwardWriting = self.downwardWriting
        obj.zigzag = self.zigzag
        obj.rotateSpirals = self.rotateSpirals
        obj.add_flat_ends = self.add_flat_ends
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

def add_tube_idname_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_tube_idname.bl_idname,
        text="Add tube",
        icon='PLUGIN')


# This allows you to right click on a button and link to the manual
def add_tube_idname_manual_map():
    url_manual_prefix = "http://wiki.blender.org/index.php/Doc:2.6/Manual/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_tube", "Modeling/Objects"),
        )
    return url_manual_prefix, url_manual_mapping


def register():
    bpy.utils.register_class(OBJECT_OT_add_tube_idname)
    bpy.utils.register_manual_map(add_tube_idname_manual_map)
    bpy.types.INFO_MT_mesh_add.append(add_tube_idname_button)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_tube_idname)
    bpy.utils.unregister_manual_map(add_tube_idname_manual_map)
    bpy.types.INFO_MT_mesh_add.remove(add_tube_idname_button)


if __name__ == "__main__":
    register()
