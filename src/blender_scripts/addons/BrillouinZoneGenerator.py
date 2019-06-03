#!/usr/bin/env python3
# -*- coding: utf-8 -*-

bl_info = {
    "name": "Brillouin zone generator",
    "author": "mtav",
    "version": (1, 0),
    "blender": (2, 76, 0),
    "location": "View3D > Add > Mesh > Add Brillouin zone",
    "description": "Adds a Brillouin zone mesh",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Add Mesh"}

import bpy
import bmesh
import math
from bpy.props import FloatProperty, BoolProperty, FloatVectorProperty, IntVectorProperty, IntProperty, EnumProperty
from mathutils import Vector, Matrix
#from bpy_extras import object_utils
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from bpy.types import Operator

from blender_scripts.modules.blender_utilities import faceCoordsToIndices, getPyDataTetraHedron, addToBmesh, createObjectFromBmesh

def reciprocal_conversion(a1, a2, a3, b1, b2, b3):
  a1 = Vector(a1)
  a2 = Vector(a2)
  a3 = Vector(a3)
  vol = a1.dot(a2.cross(a3))
  if vol != 0:
    b1[:] = a2.cross(a3)/vol
    b2[:] = a3.cross(a1)/vol
    b3[:] = a1.cross(a2)/vol
  return vol

def BrillouinZoneFCT(self, context):
  mesh = bpy.data.meshes.new("BrillouinZone-FCT")

  bm = bmesh.new()

  # compute lattice vectors
  a, b, c = self.unit_cube_size
  a1 = 0.5*Vector((0,b,c))
  a2 = 0.5*Vector((a,0,c))
  a3 = 0.5*Vector((a,b,0))

  b1 = Vector()
  b2 = Vector()
  b3 = Vector()
  reciprocal_conversion(a1, a2, a3, b1, b2, b3)
  
  # update attributes
  self.a1 = a1
  self.a2 = a2
  self.a3 = a3

  self.b1 = b1
  self.b2 = b2
  self.b3 = b3
  
  # define vertices
  Gamma = bm.verts.new((0, 0, 0))
  #A1 = bm.verts.new(a1)
  #A2 = bm.verts.new(a2)
  #A3 = bm.verts.new(a3)
  B1 = bm.verts.new(b1)
  B2 = bm.verts.new(b2)
  B3 = bm.verts.new(b3)
  
  #bm.edges.new((Gamma, A1))
  #bm.edges.new((Gamma, A2))
  #bm.edges.new((Gamma, A3))

  bm.edges.new((Gamma, B1))
  bm.edges.new((Gamma, B2))
  bm.edges.new((Gamma, B3))

  X_p00 = bm.verts.new(1/2*(b2+b3))
  X_m00 = bm.verts.new(-1/2*(b2+b3))
  X_0p0 = bm.verts.new(1/2*(b3+b1))
  X_0m0 = bm.verts.new(-1/2*(b3+b1))
  X_00p = bm.verts.new(1/2*(b1+b2))
  X_00m = bm.verts.new(-1/2*(b1+b2))

  #bm.edges.new((X_m00, X_p00))
  #bm.edges.new((X_0m0, X_0p0))
  #bm.edges.new((X_00m, X_00p))

  L_ppp = bm.verts.new(1/2*(b1+b2+b3))
  L_mmm = bm.verts.new(-1/2*(b1+b2+b3))
  L_mpp = bm.verts.new(1/2*b1)
  L_pmm = bm.verts.new(-1/2*b1)
  L_pmp = bm.verts.new(1/2*b2)
  L_mpm = bm.verts.new(-1/2*b2)
  L_ppm = bm.verts.new(1/2*b3)
  L_mmp = bm.verts.new(-1/2*b3)

  #bm.edges.new((L_mmm, L_ppp))
  #bm.edges.new((L_mpp, L_pmm))
  #bm.edges.new((L_pmp, L_mpm))
  #bm.edges.new((L_ppm, L_mmp))

  s_x = (-1/a**2 + 1/b**2 + 1/c**2)
  s_y = (1/a**2 - 1/b**2 + 1/c**2)
  s_z = (1/a**2 + 1/b**2 - 1/c**2)

  #bmesh_square_Xplus = bmesh.new()
  #W_px_py = bmesh_square_Xplus.verts.new( (1/a,  b/2*s_x,  0) )
  #W_px_my = bmesh_square_Xplus.verts.new( (1/a, -b/2*s_x,  0) )
  #W_px_pz = bmesh_square_Xplus.verts.new( (1/a,  0      ,  c/2*s_x) )
  #W_px_mz = bmesh_square_Xplus.verts.new( (1/a,  0      , -c/2*s_x) )
  #bmesh_square_Xplus.faces.new((W_px_py, W_px_pz, W_px_my, W_px_mz))
  
  #bmesh_square_Xminus = bmesh_square_Xplus.copy()
  #bmesh.ops.rotate(bmesh_square_Xminus, verts=bmesh_square_Xminus.verts, cent=(0.0, 0.0, 0.0), matrix=Matrix.Rotation(math.radians(180.0), 3, 'Z'))

  #bmesh_square_Yplus = bmesh_square_Xplus.copy()
  #bmesh.ops.rotate(bmesh_square_Yplus, verts=bmesh_square_Yplus.verts, cent=(0.0, 0.0, 0.0), matrix=Matrix.Rotation(math.radians(90.0), 3, 'Z'))

  #bmesh_square_Yminus = bmesh_square_Xplus.copy()
  #bmesh.ops.rotate(bmesh_square_Yminus, verts=bmesh_square_Yminus.verts, cent=(0.0, 0.0, 0.0), matrix=Matrix.Rotation(math.radians(-90.0), 3, 'Z'))

  #bmesh_square_Zplus = bmesh_square_Xplus.copy()
  #bmesh.ops.rotate(bmesh_square_Zplus, verts=bmesh_square_Zplus.verts, cent=(0.0, 0.0, 0.0), matrix=Matrix.Rotation(math.radians(-90.0), 3, 'Y'))

  #bmesh_square_Zminus = bmesh_square_Xplus.copy()
  #bmesh.ops.rotate(bmesh_square_Zminus, verts=bmesh_square_Zminus.verts, cent=(0.0, 0.0, 0.0), matrix=Matrix.Rotation(math.radians(90.0), 3, 'Y'))

  #bmesh_hexagon_px_py_pz = bmesh.new()
  #W_px_py = bmesh_hexagon_px_py_pz.verts.new( (1/a     , b/2*s_x, 0) )
  #W_px_pz = bmesh_hexagon_px_py_pz.verts.new( (1/a     , 0      , c/2*s_x) )
  #W_py_px = bmesh_hexagon_px_py_pz.verts.new( ( a/2*s_y, 1/b    , 0) )
  #W_py_pz = bmesh_hexagon_px_py_pz.verts.new( ( 0      , 1/b    , c/2*s_y) )
  #W_pz_px = bmesh_hexagon_px_py_pz.verts.new( ( a/2*s_z, 0      , 1/c) )
  #W_pz_py = bmesh_hexagon_px_py_pz.verts.new( ( 0      , b/2*s_z, 1/c) )
  #bmesh_hexagon_px_py_pz.faces.new((W_px_py, W_py_px, W_py_pz, W_pz_py, W_pz_px, W_px_pz))

  #bmesh_hexagon_mx_py_pz = bmesh_hexagon_px_py_pz.copy()
  #bmesh.ops.rotate(bmesh_hexagon_mx_py_pz, verts=bmesh_hexagon_mx_py_pz.verts, cent=(0.0, 0.0, 0.0), matrix=Matrix.Rotation(math.radians(1*90.0), 3, 'Z'))
  #bmesh_hexagon_mx_my_pz = bmesh_hexagon_px_py_pz.copy()
  #bmesh.ops.rotate(bmesh_hexagon_mx_my_pz, verts=bmesh_hexagon_mx_my_pz.verts, cent=(0.0, 0.0, 0.0), matrix=Matrix.Rotation(math.radians(2*90.0), 3, 'Z'))
  #bmesh_hexagon_px_my_pz = bmesh_hexagon_px_py_pz.copy()
  #bmesh.ops.rotate(bmesh_hexagon_px_my_pz, verts=bmesh_hexagon_px_my_pz.verts, cent=(0.0, 0.0, 0.0), matrix=Matrix.Rotation(math.radians(3*90.0), 3, 'Z'))

  #bmesh_hexagon_px_py_mz = bmesh_hexagon_px_py_pz.copy()
  #bmesh.ops.rotate(bmesh_hexagon_px_py_mz, verts=bmesh_hexagon_px_py_mz.verts, cent=(0.0, 0.0, 0.0), matrix=Matrix.Rotation(math.radians(-90.0), 3, 'X'))

  #bmesh_hexagon_mx_py_mz = bmesh_hexagon_px_py_mz.copy()
  #bmesh.ops.rotate(bmesh_hexagon_mx_py_mz, verts=bmesh_hexagon_mx_py_mz.verts, cent=(0.0, 0.0, 0.0), matrix=Matrix.Rotation(math.radians(1*90.0), 3, 'Z'))
  #bmesh_hexagon_mx_my_mz = bmesh_hexagon_px_py_mz.copy()
  #bmesh.ops.rotate(bmesh_hexagon_mx_my_mz, verts=bmesh_hexagon_mx_my_mz.verts, cent=(0.0, 0.0, 0.0), matrix=Matrix.Rotation(math.radians(2*90.0), 3, 'Z'))
  #bmesh_hexagon_px_my_mz = bmesh_hexagon_px_py_mz.copy()
  #bmesh.ops.rotate(bmesh_hexagon_px_my_mz, verts=bmesh_hexagon_px_my_mz.verts, cent=(0.0, 0.0, 0.0), matrix=Matrix.Rotation(math.radians(3*90.0), 3, 'Z'))

  #addToBmesh(bm, bmesh_square_Xplus)
  #addToBmesh(bm, bmesh_square_Xminus)
  #addToBmesh(bm, bmesh_square_Yplus)
  #addToBmesh(bm, bmesh_square_Yminus)
  #addToBmesh(bm, bmesh_square_Zplus)
  #addToBmesh(bm, bmesh_square_Zminus)

  #addToBmesh(bm, bmesh_hexagon_px_py_pz)
  #addToBmesh(bm, bmesh_hexagon_mx_py_pz)
  #addToBmesh(bm, bmesh_hexagon_mx_my_pz)
  #addToBmesh(bm, bmesh_hexagon_px_my_pz)

  #addToBmesh(bm, bmesh_hexagon_px_py_mz)
  #addToBmesh(bm, bmesh_hexagon_mx_py_mz)
  #addToBmesh(bm, bmesh_hexagon_mx_my_mz)
  #addToBmesh(bm, bmesh_hexagon_px_my_mz)

  W_px_py = bm.verts.new( (1/a,  b/2*s_x,  0) )
  W_px_my = bm.verts.new( (1/a, -b/2*s_x,  0) )
  W_px_pz = bm.verts.new( (1/a,  0    ,  c/2*s_x) )
  W_px_mz = bm.verts.new( (1/a,  0    , -c/2*s_x) )

  W_mx_py = bm.verts.new( (-1/a,  b/2*s_x,  0) )
  W_mx_my = bm.verts.new( (-1/a, -b/2*s_x,  0) )
  W_mx_pz = bm.verts.new( (-1/a,  0    ,  c/2*s_x) )
  W_mx_mz = bm.verts.new( (-1/a,  0    , -c/2*s_x) )

  W_py_px = bm.verts.new( ( a/2*s_y, 1/b,  0) )
  W_py_mx = bm.verts.new( (-a/2*s_y, 1/b,  0) )
  W_py_pz = bm.verts.new( ( 0    , 1/b,  c/2*s_y) )
  W_py_mz = bm.verts.new( ( 0    , 1/b, -c/2*s_y) )

  W_my_px = bm.verts.new( ( a/2*s_y, -1/b,  0) )
  W_my_mx = bm.verts.new( (-a/2*s_y, -1/b,  0) )
  W_my_pz = bm.verts.new( ( 0    , -1/b,  c/2*s_y) )
  W_my_mz = bm.verts.new( ( 0    , -1/b, -c/2*s_y) )

  W_pz_px = bm.verts.new( ( a/2*s_z, 0    , 1/c) )
  W_pz_mx = bm.verts.new( (-a/2*s_z, 0    , 1/c) )
  W_pz_py = bm.verts.new( ( 0,     b/2*s_z, 1/c) )
  W_pz_my = bm.verts.new( ( 0,    -b/2*s_z, 1/c) )

  W_mz_px = bm.verts.new( ( a/2*s_z, 0    , -1/c) )
  W_mz_mx = bm.verts.new( (-a/2*s_z, 0    , -1/c) )
  W_mz_py = bm.verts.new( ( 0,     b/2*s_z, -1/c) )
  W_mz_my = bm.verts.new( ( 0,    -b/2*s_z, -1/c) )

  bm.faces.new((W_px_py, W_px_pz, W_px_my, W_px_mz))
  bm.faces.new((W_mx_py, W_mx_mz, W_mx_my, W_mx_pz))
  bm.faces.new((W_py_pz, W_py_px, W_py_mz, W_py_mx))
  bm.faces.new((W_my_pz, W_my_mx, W_my_mz, W_my_px))
  bm.faces.new((W_pz_px, W_pz_py, W_pz_mx, W_pz_my))
  bm.faces.new((W_mz_px, W_mz_my, W_mz_mx, W_mz_py))

  bm.faces.new((W_px_py, W_py_px, W_py_pz, W_pz_py, W_pz_px, W_px_pz)) # px py pz
  bm.faces.new((W_px_py, W_py_px, W_py_mz, W_mz_py, W_mz_px, W_px_mz)) # px py mz
  bm.faces.new((W_px_my, W_my_px, W_my_pz, W_pz_my, W_pz_px, W_px_pz)) # px my pz
  bm.faces.new((W_px_my, W_my_px, W_my_mz, W_mz_my, W_mz_px, W_px_mz)) # px my mz
  bm.faces.new((W_mx_py, W_py_mx, W_py_pz, W_pz_py, W_pz_mx, W_mx_pz)) # mx py pz
  bm.faces.new((W_mx_py, W_py_mx, W_py_mz, W_mz_py, W_mz_mx, W_mx_mz)) # mx py mz
  bm.faces.new((W_mx_my, W_my_mx, W_my_pz, W_pz_my, W_pz_mx, W_mx_pz)) # mx my pz
  bm.faces.new((W_mx_my, W_my_mx, W_my_mz, W_mz_my, W_mz_mx, W_mx_mz)) # mx my mz

  U_px_py_pz = bm.verts.new( (W_px_py.co + W_px_pz.co)/2 )
  U_px_py_mz = bm.verts.new( (W_px_py.co + W_px_mz.co)/2 )
  U_px_my_pz = bm.verts.new( (W_px_my.co + W_px_pz.co)/2 )
  U_px_my_mz = bm.verts.new( (W_px_my.co + W_px_mz.co)/2 )
  U_mx_py_pz = bm.verts.new( (W_mx_py.co + W_mx_pz.co)/2 )
  U_mx_py_mz = bm.verts.new( (W_mx_py.co + W_mx_mz.co)/2 )
  U_mx_my_pz = bm.verts.new( (W_mx_my.co + W_mx_pz.co)/2 )
  U_mx_my_mz = bm.verts.new( (W_mx_my.co + W_mx_mz.co)/2 )

  U_py_px_pz = bm.verts.new( (W_py_px.co + W_py_pz.co)/2 )
  U_py_px_mz = bm.verts.new( (W_py_px.co + W_py_mz.co)/2 )
  U_py_mx_pz = bm.verts.new( (W_py_mx.co + W_py_pz.co)/2 )
  U_py_mx_mz = bm.verts.new( (W_py_mx.co + W_py_mz.co)/2 )
  U_my_px_pz = bm.verts.new( (W_my_px.co + W_my_pz.co)/2 )
  U_my_px_mz = bm.verts.new( (W_my_px.co + W_my_mz.co)/2 )
  U_my_mx_pz = bm.verts.new( (W_my_mx.co + W_my_pz.co)/2 )
  U_my_mx_mz = bm.verts.new( (W_my_mx.co + W_my_mz.co)/2 )

  U_pz_px_py = bm.verts.new( (W_pz_px.co + W_pz_py.co)/2 )
  U_pz_px_my = bm.verts.new( (W_pz_px.co + W_pz_my.co)/2 )
  U_pz_mx_py = bm.verts.new( (W_pz_mx.co + W_pz_py.co)/2 )
  U_pz_mx_my = bm.verts.new( (W_pz_mx.co + W_pz_my.co)/2 )
  U_mz_px_py = bm.verts.new( (W_mz_px.co + W_mz_py.co)/2 )
  U_mz_px_my = bm.verts.new( (W_mz_px.co + W_mz_my.co)/2 )
  U_mz_mx_py = bm.verts.new( (W_mz_mx.co + W_mz_py.co)/2 )
  U_mz_mx_my = bm.verts.new( (W_mz_mx.co + W_mz_my.co)/2 )

  K_px_py = bm.verts.new( (W_px_py.co + W_py_px.co)/2 )
  K_px_my = bm.verts.new( (W_px_my.co + W_my_px.co)/2 )
  K_px_pz = bm.verts.new( (W_px_pz.co + W_pz_px.co)/2 )
  K_px_mz = bm.verts.new( (W_px_mz.co + W_mz_px.co)/2 )

  K_mx_py = bm.verts.new( (W_mx_py.co + W_py_mx.co)/2 )
  K_mx_my = bm.verts.new( (W_mx_my.co + W_my_mx.co)/2 )
  K_mx_pz = bm.verts.new( (W_mx_pz.co + W_pz_mx.co)/2 )
  K_mx_mz = bm.verts.new( (W_mx_mz.co + W_mz_mx.co)/2 )

  K_pz_py = bm.verts.new( (W_pz_py.co + W_py_pz.co)/2 )
  K_pz_my = bm.verts.new( (W_pz_my.co + W_my_pz.co)/2 )
  K_mz_py = bm.verts.new( (W_mz_py.co + W_py_mz.co)/2 )
  K_mz_my = bm.verts.new( (W_mz_my.co + W_my_mz.co)/2 )

  bm.to_mesh(mesh)
  mesh.update()

  # add the mesh as an object into the scene with this utility module
  object_data_add(context, mesh, operator=self)

  # remove doubles and fix normals
  bpy.ops.object.mode_set(mode='EDIT')
  bpy.ops.mesh.select_mode(type='VERT', action='ENABLE')
  bpy.ops.mesh.select_all(action='SELECT')
  bpy.ops.mesh.remove_doubles()
  bpy.ops.mesh.normals_make_consistent(inside=False)
  bpy.ops.object.mode_set(mode='OBJECT')  

  return

class AddBrillouinZone(Operator, AddObjectHelper):
    """Add a first Brillouin zone mesh"""
    bl_idname = "mesh.brillouin_zone_add"
    bl_label = "Add Brillouin zone"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    lattice = EnumProperty(
      items = (
      ("CS","Cubic simple",""),
      ("H","Hexagonal",""),
      ("BCC","Body-Centered Cubic",""),
      ("FCT","Face-Centered Tetragonal",""),
      ("FCC","Face-Centered Cubic",""),
      ("Custom","Custom",""),
      ),
      name = "Lattice", default="FCT")

    updating = BoolProperty(name="updating", default=False)

    def update_direct_lattice(self, context):
      if not self.updating:
        #print(self.__class__.__name__ + '.update_direct_lattice')
        self.updating = True
        vol = reciprocal_conversion(self.a1, self.a2, self.a3, self.b1, self.b2, self.b3)
        self.updating = False
        #print(self.a1, self.a2, self.a3)
        #print(self.b1, self.b2, self.b3)

    def update_reciprocal_lattice(self, context):
      if not self.updating:
        #print(self.__class__.__name__ + '.update_reciprocal_lattice')
        self.updating = True
        vol = reciprocal_conversion(self.b1, self.b2, self.b3, self.a1, self.a2, self.a3)
        self.updating = False
        #print(self.a1, self.a2, self.a3)
        #print(self.b1, self.b2, self.b3)

    a1 = FloatVectorProperty(name="a1", default=Vector((1,0,0)), update = update_direct_lattice)
    a2 = FloatVectorProperty(name="a2", default=Vector((0,1,0)), update = update_direct_lattice)
    a3 = FloatVectorProperty(name="a3", default=Vector((0,0,1)), update = update_direct_lattice)

    b1 = FloatVectorProperty(name="b1", default=Vector((1,0,0)), update = update_reciprocal_lattice)
    b2 = FloatVectorProperty(name="b2", default=Vector((0,1,0)), update = update_reciprocal_lattice)
    b3 = FloatVectorProperty(name="b3", default=Vector((0,0,1)), update = update_reciprocal_lattice)

    unit_cube_size = FloatVectorProperty(name="unit cube size", default=Vector((1,1,0.8)))

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'lattice')
        
        if self.lattice == "Custom":
          box1 = layout.box()
          box1.label('Lattice vectors:')
          box1.prop(self, 'a1')
          box1.prop(self, 'a2')
          box1.prop(self, 'a3')
          box2 = layout.box()
          box2.label('Reciprocal lattice vectors (/ 2 pi):')
          box2.prop(self, 'b1')
          box2.prop(self, 'b2')
          box2.prop(self, 'b3')
        elif self.lattice == "FCT":
          layout.prop(self, 'unit_cube_size')
          box1 = layout.box()
          box1.label('Lattice vectors:')
          col1 = box1.column(align=False)
          col1.label('a1 = {}'.format(self.a1[:]))
          col1.label('a2 = {}'.format(self.a2[:]))
          col1.label('a3 = {}'.format(self.a3[:]))
          box2 = layout.box()
          box2.label('Reciprocal lattice vectors (/ 2 pi):')
          col2 = box2.column(align=False)
          col2.label('b1 = {}'.format(self.b1[:]))
          col2.label('b2 = {}'.format(self.b2[:]))
          col2.label('b3 = {}'.format(self.b3[:]))
        
    def execute(self, context):
        if self.lattice == "FCT":
          BrillouinZoneFCT(self, context)          
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(AddBrillouinZone.bl_idname, icon='MESH_CUBE')

def register():
    bpy.utils.register_class(AddBrillouinZone)
    bpy.types.INFO_MT_mesh_add.append(menu_func)

def unregister():
    bpy.utils.unregister_class(AddBrillouinZone)
    bpy.types.INFO_MT_mesh_add.remove(menu_func)

if __name__ == '__main__':
    register()
    bpy.ops.mesh.brillouin_zone_add()
