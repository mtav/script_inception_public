#!/usr/bin/env python3
# -*- coding: utf-8 -*-

bl_info = {
    "name": "Rod Connected Diamond (RCD) crystal",
    "author": "mtav",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > RCD",
    "description": "Adds a new Rod Connected Diamond (RCD) crystal",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh"}

import bpy
import os
import pathlib
import numpy

from io_mesh_stl import stl_utils
from io_mesh_stl import blender_utils

from mathutils import Matrix
from mathutils import Vector

from bpy.types import Operator
from bpy.props import FloatVectorProperty, BoolProperty, FloatProperty, IntProperty, EnumProperty, IntVectorProperty

from bpy_extras.io_utils import axis_conversion
from bpy_extras.object_utils import AddObjectHelper, object_data_add

from blender_scripts.modules.blender_utilities import setOrigin, selectObjects, add_array_modifier
from blender_scripts.modules.GeometryObjects import add_cylinder, add_tetra, add_lattice_cell, add_block

import bfdtd.RCD

class OBJECT_OT_add_RCD(Operator, AddObjectHelper):
    """Create a new RCD object"""
    # .. todo:: add array creation + duplicate vertex removal
    # .. todo:: inverse RCD creation?
    # .. todo:: RCD111 direct+inverse creation?
    # .. todo:: standardize shift_cell/shift_origin to make it consistent between RCD and RCD111
    # .. todo:: finish implementing FRD properly, bot 111 and normal
    # .. todo:: implement automatic crystal limitation to cell, as done for FreeCAD. Integrate/merge all related code.
    # .. todo:: make nicer, more centered RCD111 shifted cells
    # .. todo:: load inverse RCD111 STL files? (or generate, but might be problematic, cf FreeCAD for that. Use FreeCAD without calling it? also in future super-app?)
    
    bl_idname = "mesh.add_rcd"
    bl_label = "Add Rod Connected Diamond (RCD) crystal"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}
    
    size : FloatProperty(name="size", default=1, min=0)
    shift_cell : BoolProperty(name="shift cell", default=False)
    shift_origin : BoolProperty(name="shift origin", default=False)
    radius : FloatProperty(name="radius", default=0.05, min=0)
    
    add_unit_cell_BB : BoolProperty(name="Add unit-cell bounding box", default=True)
    
    create_array : BoolProperty(name="Create an array", default=False)
    array_size_X : IntProperty(name="number of periods in X", default = 2, min=1)
    array_size_Y : IntProperty(name="number of periods in Y", default = 3, min=1)
    array_size_Z : IntProperty(name="number of periods in Z", default = 4, min=1)
    
    cell_type : EnumProperty(items = (("RCD","RCD","RCD"),
                                      ("RCD111_v1","RCD111 type 1","RCD111 with 3 tetras"),
                                      ("RCD111_v2","RCD111 type 2","RCD111 with 6 tetras"),
                                      ("RCD111_inverse","RCD111_inverse","Add a pre-made inverse RCD111 unit-cell"),
                                      ("FRD111_v1","FRD111 type 1","FRD111 with 3 tetras"),
                                      ("FRD111_v2","FRD111 type 2","FRD111 with 6 tetras"),
                                      ), default='RCD111_v2', name = "Cell type:")
    #sub_cell_type = EnumProperty(items = (("cell_type_1","cell type 1","3 tetras"), ("cell_type_2","cell type 2","6 tetras")), default='cell_type_2', name = "RCD111 cell type:")

    RCD111_v2_advanced : BoolProperty(name="Create array filling a box", default=False)
    RCD111_v2_location : FloatVectorProperty(name="location", default = (0,0,0))
    RCD111_v2_size : FloatVectorProperty(name="size", default = (numpy.sqrt(2)/2, numpy.sqrt(6)/2, numpy.sqrt(3)), min=0)
    # RCD111_v2_size = IntVectorProperty(name="size", default = (1,1,1))
    
    # RCD111_v2_Nx = IntProperty(name="number of periods in X", default = 1, min=1)
    # RCD111_v2_Nx = IntProperty(name="number of periods in X", default = 1, min=1)
    # RCD111_v2_Ny = IntProperty(name="number of periods in Y", default = 1, min=1)
    # RCD111_v2_Nz = IntProperty(name="number of periods in Z", default = 1, min=1)
    # RCD111_v2_Sx = IntProperty(name="size in X", default = 2)
    # RCD111_v2_Sy = IntProperty(name="size in Y", default = 3)
    # RCD111_v2_Sz = IntProperty(name="size in Z", default = 4)
    
    def draw(self, context):
      layout = self.layout
      box = layout.box()
      box.prop(self, 'location')
      box.prop(self, 'cell_type')
      box.prop(self, 'size')
      box.prop(self, 'shift_cell')
      box.prop(self, 'shift_origin')
      box.prop(self, 'radius')
      box.prop(self, 'add_unit_cell_BB')
      box.prop(self, 'create_array')
      if self.create_array:
        box.prop(self, 'array_size_X')
        box.prop(self, 'array_size_Y')
        box.prop(self, 'array_size_Z')
      box.prop(self, 'RCD111_v2_advanced')
      if self.RCD111_v2_advanced:
        box1 = layout.box()
        box1.label(text='Advanced RCD111 options:')
        box1.prop(self, 'RCD111_v2_location')
        box1.prop(self, 'RCD111_v2_size')
        # box1.prop(self, 'RCD111_v2_Nx')
        # box1.prop(self, 'RCD111_v2_Ny')
        # box1.prop(self, 'RCD111_v2_Nz')
        # box1.prop(self, 'RCD111_v2_Sx')
        # box1.prop(self, 'RCD111_v2_Sy')
        # box1.prop(self, 'RCD111_v2_Sz')
      return
    
    def execute(self, context):
      
      # .. todo:: Support rotation as usual in object addons?
      # crystal axes
      e1 = [1,0,0]
      e2 = [0,1,0]
      e3 = [0,0,1]
      
      if self.cell_type == 'RCD':
        # .. todo:: set to cursor location (check how addCube & co initialize it -> It is set when object_data_add(context, mesh, operator=self) is called, which means ideally a mesh should be created and then passed to that function. It should take care of rotation&co too.)
        ## get cursor location for placement
        #cursor_location3 = numpy.array(bpy.context.scene.cursor.location)
        #self.setLocation(cursor_location3)
      
        location = Vector(self.location)
        
        obj_list = []
        if self.shift_cell:
          obj_list.extend( add_tetra(self, location=location+self.size*Vector([3/4, 1/4, 1/4]), size=self.size/2, name='Tetra', cylinder_radius=self.radius) )
          obj_list.extend( add_tetra(self, location=location+self.size*Vector([1/4, 3/4, 1/4]), size=self.size/2, name='Tetra', cylinder_radius=self.radius) )
          obj_list.extend( add_tetra(self, location=location+self.size*Vector([1/4, 1/4, 3/4]), size=self.size/2, name='Tetra', cylinder_radius=self.radius) )
          obj_list.extend( add_tetra(self, location=location+self.size*Vector([3/4, 3/4, 3/4]), size=self.size/2, name='Tetra', cylinder_radius=self.radius) )
        else:
          obj_list.extend( add_tetra(self, location=location+self.size*Vector([1/4, 1/4, 1/4]), size=self.size/2, name='Tetra', cylinder_radius=self.radius) )
          obj_list.extend( add_tetra(self, location=location+self.size*Vector([3/4, 3/4, 1/4]), size=self.size/2, name='Tetra', cylinder_radius=self.radius) )
          obj_list.extend( add_tetra(self, location=location+self.size*Vector([3/4, 1/4, 3/4]), size=self.size/2, name='Tetra', cylinder_radius=self.radius) )
          obj_list.extend( add_tetra(self, location=location+self.size*Vector([1/4, 3/4, 3/4]), size=self.size/2, name='Tetra', cylinder_radius=self.radius) )
        
        common_mesh = obj_list[0].data
        for obj in obj_list[1:]:
          obj.data = common_mesh
          
        selectObjects(obj_list)
        bpy.ops.object.join()
        obj_blender = context.active_object
        obj_blender.name='RCD'
        setOrigin(obj_blender, self.location)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        
        e1 = self.size*Vector([1,0,0])
        e2 = self.size*Vector([0,1,0])
        e3 = self.size*Vector([0,0,1])
      elif self.cell_type == 'RCD111_inverse':
        if self.shift_cell:
          STLfile = os.path.join(pathlib.Path.home(), 'Development/script_inception_public/src/blender_scripts/STL-files/RCD111_inverse_shifted_centred.stl')
        else:
          STLfile = os.path.join(pathlib.Path.home(), 'Development/script_inception_public/src/blender_scripts/STL-files/RCD111_inverse.stl')
        objName = bpy.path.display_name(os.path.basename(STLfile))
        tris, tri_nors, pts = stl_utils.read_stl(STLfile)
        tri_nors = None
        axis_forward='Y'
        axis_up='Z'
        global_scale = self.size
        global_matrix = axis_conversion(from_forward=axis_forward, from_up=axis_up).to_4x4() @ Matrix.Scale(global_scale, 4)
        blender_utils.create_and_link_mesh(objName, tris, tri_nors, pts, global_matrix)
        obj_blender = context.active_object
        
        # get cursor location for placement
        if obj_blender:
          obj_blender.location = numpy.array(context.scene.cursor.location)
        else:
          raise Exception('obj_blender is None')
        
        obj_bfdtd = bfdtd.RCD.RCD_HexagonalLattice()
        obj_bfdtd.setOuterRadius(self.radius)
        obj_bfdtd.setCubicUnitCellSize(self.size)
        obj_bfdtd.setShifted(self.shift_cell)
        obj_bfdtd.setUnitCellType(2)
        e1, e2, e3 = obj_bfdtd.getLatticeVectors()
        
      else:
        if 'RCD111' in self.cell_type:
          obj_bfdtd = bfdtd.RCD.RCD_HexagonalLattice()
        else:
          obj_bfdtd = bfdtd.RCD.FRD_HexagonalLattice()
        obj_bfdtd.setOuterRadius(self.radius)
        obj_bfdtd.setCubicUnitCellSize(self.size)
        obj_bfdtd.setShifted(self.shift_cell)
        if 'v1' in self.cell_type:
          obj_bfdtd.setUnitCellType(1)
        else:
          obj_bfdtd.setUnitCellType(2)

        if self.RCD111_v2_advanced:
          obj_bfdtd.fillBox(self.RCD111_v2_location, self.RCD111_v2_size)
          # obj_bfdtd.fillBox([self.RCD111_v2_Nx, self.RCD111_v2_Ny, self.RCD111_v2_Nz], [self.RCD111_v2_Nx, self.RCD111_v2_Ny, self.RCD111_v2_Nz])
          # obj_bfdtd.createRectangularArraySymmetrical(self.RCD111_v2_Nx, self.RCD111_v2_Ny, self.RCD111_v2_Nz)
          add_block(self, location3 = self.RCD111_v2_location, size3 = self.RCD111_v2_size, name='box_to_fill', wiremode=True)
        
        obj_blender = obj_bfdtd.createBlenderObject(self, context)
        e1, e2, e3 = obj_bfdtd.getLatticeVectors()
        
      obj_blender.name = self.cell_type
      if self.create_array:
        add_array_modifier(obj_blender, 'array-modifier-X', self.array_size_X, e1)
        add_array_modifier(obj_blender, 'array-modifier-Y', self.array_size_Y, e2)
        add_array_modifier(obj_blender, 'array-modifier-Z', self.array_size_Z, e3)

      # add unit-cell bounding box
      if self.add_unit_cell_BB:
        obj_lattice_cell = add_lattice_cell(self, e1, e2, e3, name='lattice_cell', shift_origin=self.shift_origin, wiremode=True)
        selectObjects([obj_blender, obj_lattice_cell], active_object=obj_lattice_cell, context = context)
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)

      return {'FINISHED'}

# Registration
def add_RCD_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_RCD.bl_idname,
        text="Add RCD",
        icon='MESH_CUBE')

def register():
    bpy.utils.register_class(OBJECT_OT_add_RCD)
    bpy.types.VIEW3D_MT_mesh_add.append(add_RCD_button)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_RCD)
    bpy.types.VIEW3D_MT_mesh_add.remove(add_RCD_button)

if __name__ == "__main__":
    register()
