#!/usr/bin/env python3
# -*- coding: utf-8 -*-

bl_info = {
    "name": "New GWL X Block",
    "author": "mtav",
    "version": (1, 0),
    "blender": (2, 65, 0),
    "location": "View3D > Add > Mesh > Add GWL X Block",
    "description": "Adds a new GWL X Block",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Add Mesh"}

# TODO: Update using external GWLobject based class.

import bpy
from bpy.types import Operator
import bmesh
from bpy.props import FloatProperty, BoolProperty, FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
import numpy
import math
from blender_scripts.modules import blender_utilities

def add_XBlock(width, height, depth, LineDistance_Horizontal, LineDistance_Vertical):

    LineNumber_Horizontal = math.floor( (depth/LineDistance_Horizontal) + 1 )
    LineNumber_Vertical = math.floor( (height/LineDistance_Vertical) + 1 )

    verts = []
    edges = []
    faces = []

    ylist = []
    L = (LineNumber_Horizontal-1)*LineDistance_Horizontal
    ylist = numpy.linspace(-0.5*L, 0.5*L, LineNumber_Horizontal)

    zlist = []
    L = (LineNumber_Vertical-1)*LineDistance_Vertical
    zlist = numpy.linspace(-0.5*L, 0.5*L, LineNumber_Vertical)

    for z in zlist:
      for y in ylist:
        A = [-0.5*width,y,z]
        B = [0.5*width,y,z]
        verts.append(A)
        verts.append(B)
        edges.append((len(verts)-2,len(verts)-1))
    
    return verts, edges, faces

# TODO: unused: could be removed
def add_object(self, context):
    scale_x = self.scale.x
    scale_y = self.scale.y

    verts = [Vector((-1 * scale_x, 1 * scale_y, 0)),
             Vector((1 * scale_x, 1 * scale_y, 0)),
             Vector((1 * scale_x, -1 * scale_y, 0)),
             Vector((-1 * scale_x, -1 * scale_y, 0)),
            ]

    edges = []
    faces = [[0, 1, 2, 3]]

    mesh = bpy.data.meshes.new(name="GWL X Block")
    mesh.from_pydata(verts, edges, faces)
    # useful for development when the mesh may be invalid.
    # mesh.validate(verbose=True)
    object_data_add(context, mesh, operator=self)


class OBJECT_OT_add_xblock(Operator, AddObjectHelper):
    """Add a simple X Block"""
    bl_idname = "mesh.xblock_add"
    bl_label = "Add GWL X Block"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    width = FloatProperty(
            name="Width",
            description="Box Width",
            min=0.01, max=100.0,
            default=2.0,
            )
    height = FloatProperty(
            name="Height",
            description="Box Height",
            min=0.01, max=100.0,
            default=2.0,
            )
    depth = FloatProperty(
            name="Depth",
            description="Box Depth",
            min=0.01, max=100.0,
            default=2.0,
            )

    LineDistance_Horizontal = FloatProperty(
            name="LineDistance_Horizontal",
            description="LineDistance_Horizontal",
            min=0.001, max=5,
            default=0.100,
            )
          
    LineDistance_Vertical = FloatProperty(
            name="LineDistance_Vertical",
            description="LineDistance_Vertical",
            min=0.001, max=5,
            default=0.200,
            )

    # generic transform props
    view_align = BoolProperty(
            name="Align to View",
            default=False,
            )
    location = FloatVectorProperty(
            name="Location",
            subtype='TRANSLATION',
            )
    rotation = FloatVectorProperty(
            name="Rotation",
            subtype='EULER',
            )

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.prop(self, 'width')
        box.prop(self, 'height')
        box.prop(self, 'depth')

        box.prop(self, 'LineDistance_Horizontal')
        box.prop(self, 'LineDistance_Vertical')

        box.prop(self, 'view_align')
        box.prop(self, 'location')
        box.prop(self, 'rotation')

    def execute(self, context):

#        add_object(self, context)

        verts_loc, edges, faces = add_XBlock(self.width, self.height, self.depth, self.LineDistance_Horizontal, self.LineDistance_Vertical)

        mesh = bpy.data.meshes.new(name="GWL X Block")
        mesh.from_pydata(verts_loc, edges, faces)
        # useful for development when the mesh may be invalid.
        # mesh.validate(verbose=True)
        object_data_add(context, mesh, operator=self)

        ## bmesh method:
        # mesh = bpy.data.meshes.new(name = meshname)
        # mesh.from_pydata(verts_loc, edges, faces)
        # #useful for development when the mesh may be invalid.
        # #mesh.validate(verbose=True)
        #
        ## add the mesh as an object into the scene with this utility module
        # from bpy_extras import object_utils
        # object_utils.object_data_add(context, mesh, operator=self)

        return {'FINISHED'}

# def menu_func(self, context):
#     self.layout.operator(Add_GWL_XBlock.bl_idname, icon='MESH_CUBE')

# Registration

def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_xblock.bl_idname,
        text="Add new GWL X Block",
        icon='PLUGIN')


# This allows you to right click on a button and link to the manual
def add_object_manual_map():
    url_manual_prefix = "http://wiki.blender.org/index.php/Doc:2.6/Manual/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_xblock", "Modeling/Objects"),
        )
    return url_manual_prefix, url_manual_mapping


def register():
    bpy.utils.register_class(OBJECT_OT_add_xblock)
    bpy.utils.register_manual_map(add_object_manual_map)
    bpy.types.INFO_MT_mesh_add.append(add_object_button)
    # bpy.types.INFO_MT_mesh_add.append(menu_func)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_xblock)
    bpy.utils.unregister_manual_map(add_object_manual_map)
    bpy.types.INFO_MT_mesh_add.remove(add_object_button)
    # bpy.types.INFO_MT_mesh_add.remove(menu_func)

if __name__ == "__main__":
    register()

    # test call
    #bpy.ops.mesh.xblock_add()
