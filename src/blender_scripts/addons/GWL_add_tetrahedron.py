#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
.. todo:: Update using external GWLobject based class.
'''

bl_info = {
    "name": "ice-tetrahedron",
    "author": "mtav",
    "version": (1, 0),
    "blender": (2, 65, 0),
    "location": "View3D > Add > Mesh > ice-tetrahedron",
    "description": "Adds an ice-tetrahedron mesh",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Add Mesh"}

import bpy
import bmesh

from bpy.props import FloatProperty, BoolProperty, FloatVectorProperty
from numpy import sqrt,pi,cos,sin
from mathutils import *
from GWL.tube import Tube
from blender_scripts.modules import blender_utilities

class AddIceTetrahedron(bpy.types.Operator):
    """Adds an ice-tetrahedron mesh"""
    bl_idname = "mesh.ice_tetrahedron_add"
    bl_label = "Add ice-tetrahedron"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    #width = FloatProperty(
            #name="Width",
            #description="Box Width",
            #min=0.01, max=100.0,
            #default=1.0,
            #)
    #height = FloatProperty(
            #name="Height",
            #description="Box Height",
            #min=0.01, max=100.0,
            #default=1.0,
            #)
    #depth = FloatProperty(
            #name="Depth",
            #description="Box Depth",
            #min=0.01, max=100.0,
            #default=1.0,
            #)

    length_top = FloatProperty(
            name="length_top",
            description="length_top",
            min=0.01, max=100.0,
            default=2,
            )

    length_bottom = FloatProperty(
            name="length_bottom",
            description="length_bottom",
            min=0.01, max=100.0,
            default=5,
            )

    delta = FloatProperty(
            name="delta",
            description="delta",
            min=0.01, max=100.0,
            default=0.1,
            )

    radius = FloatProperty(
            name="radius",
            description="radius",
            min=0.01, max=100.0,
            default=0.05,
            )

    BottomToTop = BoolProperty(
            name="BottomToTop writing",
            default=False,
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

    def execute(self, context):

        mesh = bpy.data.meshes.new("Ice-tetrahedron")

        delta = self.delta

        bm = bmesh.new()

        D = Vector((1/2, sqrt(3)/2, 5/4))

        centre = bm.verts.new(Vector((1/2, sqrt(3)/2, 1/4)))

        A = bm.verts.new((0, 0, 0))

        B = bm.verts.new((0,sqrt(3),0))

        C = bm.verts.new((3/2,sqrt(3)/2,0))

        D = bm.verts.new(D)

        r = self.radius

        alpha = 0*2*pi/3
        D0 = D.co + Vector((r*cos(alpha),r*sin(alpha),0))
        centre_D0 = centre.co + Vector((r*cos(alpha),r*sin(alpha),0))

        alpha = 1*2*pi/3
        D1 = D.co + Vector((r*cos(alpha),r*sin(alpha),0))
        centre_D1 = centre.co + Vector((r*cos(alpha),r*sin(alpha),0))

        alpha = 2*2*pi/3
        D2 = D.co + Vector((r*cos(alpha),r*sin(alpha),0))
        centre_D2 = centre.co + Vector((r*cos(alpha),r*sin(alpha),0))
        
        D0 = bm.verts.new(D0)
        D1 = bm.verts.new(D1)
        D2 = bm.verts.new(D2)
        
        centre_D0 = bm.verts.new(centre_D0)
        centre_D1 = bm.verts.new(centre_D1)
        centre_D2 = bm.verts.new(centre_D2)
        
        C0 = bm.verts.new(C.co + delta*Vector((0,1,0)))
        C1 = bm.verts.new(C.co - delta*Vector((0,1,0)))
        centre_C0 = bm.verts.new(centre.co + delta*Vector((0,1,0)))
        centre_C1 = bm.verts.new(centre.co - delta*Vector((0,1,0)))


        u = A.co - centre.co
        z = Vector((0,0,1))
        v = u.cross(z)
        v.normalize()
        
        A0 = bm.verts.new(A.co + delta*v)
        A1 = bm.verts.new(A.co - delta*v)
        centre_A0 = bm.verts.new(centre.co + delta*v)
        centre_A1 = bm.verts.new(centre.co - delta*v)
        

        u = B.co - centre.co
        z = Vector((0,0,1))
        v = u.cross(z)
        v.normalize()
        
        B0 = bm.verts.new(B.co + delta*v)
        B1 = bm.verts.new(B.co - delta*v)
        centre_B0 = bm.verts.new(centre.co + delta*v)
        centre_B1 = bm.verts.new(centre.co - delta*v)
        
        if self.BottomToTop:
          bm.edges.new((A, centre))
          bm.edges.new((A0, centre_A0))
          bm.edges.new((A1, centre_A1))
          
          bm.edges.new((B, centre))
          bm.edges.new((B0, centre_B0))
          bm.edges.new((B1, centre_B1))
          
          bm.edges.new((C, centre))
          bm.edges.new((C0, centre_C0))
          bm.edges.new((C1, centre_C1))
          
          bm.edges.new((centre_D0,D0))
          bm.edges.new((centre_D1,D1))
          bm.edges.new((centre_D2,D2))
          
        else:
          bm.edges.new((D0, centre_D0))
          bm.edges.new((D1, centre_D1))
          bm.edges.new((D2, centre_D2))

          bm.edges.new((centre, A))
          bm.edges.new((centre_A0, A0))
          bm.edges.new((centre_A1, A1))
          
          bm.edges.new((centre, B))
          bm.edges.new((centre_B0, B0))
          bm.edges.new((centre_B1, B1))
          
          bm.edges.new((centre, C))
          bm.edges.new((centre_C0, C0))
          bm.edges.new((centre_C1, C1))
          
        D0.co = centre_D0.co + (D0.co-centre_D0.co).normalized()*self.length_top
        D1.co = centre_D1.co + (D1.co-centre_D1.co).normalized()*self.length_top
        D2.co = centre_D2.co + (D2.co-centre_D2.co).normalized()*self.length_top

        offset = Vector(centre.co)
        for v in bm.verts:
          v.co -= offset

        A.co = centre.co + (A.co-centre.co).normalized()*self.length_bottom
        A0.co = centre_A0.co + (A0.co-centre_A0.co).normalized()*self.length_bottom
        A1.co = centre_A1.co + (A1.co-centre_A1.co).normalized()*self.length_bottom

        B.co = centre.co + (B.co-centre.co).normalized()*self.length_bottom
        B0.co = centre_B0.co + (B0.co-centre_B0.co).normalized()*self.length_bottom
        B1.co = centre_B1.co + (B1.co-centre_B1.co).normalized()*self.length_bottom

        C.co = centre.co + (C.co-centre.co).normalized()*self.length_bottom
        C0.co = centre_C0.co + (C0.co-centre_C0.co).normalized()*self.length_bottom
        C1.co = centre_C1.co + (C1.co-centre_C1.co).normalized()*self.length_bottom

        #centre.co = A.co + (centre.co-A.co).normalized()*self.length_bottom
        #centre_A0.co = A0.co + (centre_A0.co-A0.co).normalized()*self.length_bottom
        #centre_A1.co = A1.co + (centre_A1.co-A1.co).normalized()*self.length_bottom

        #B.co = centre.co + (B.co-centre.co).normalized()*self.length_bottom


        bm.to_mesh(mesh)
        mesh.update()

        # add the mesh as an object into the scene with this utility module
        from bpy_extras import object_utils
        object_utils.object_data_add(context, mesh, operator=self)

        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(AddIceTetrahedron.bl_idname, icon='PLUGIN')

def register():
    bpy.utils.register_class(AddIceTetrahedron)
    bpy.types.INFO_MT_mesh_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(AddIceTetrahedron)
    bpy.types.INFO_MT_mesh_add.remove(menu_func)

if __name__ == "__main__":
    print('=== start ===')
    register()
    #bpy.utils.register_class(AddIceTetrahedron)
    # test call
    #bpy.ops.mesh.ice_tetrahedron_add()
    print('=== end ===')
