#!/usr/bin/env python3
# -*- coding: utf-8 -*-

bl_info = {
    "name": "SpiralParabola",
    "author": "mtav",
    "version": (1, 0),
    "blender": (2, 65, 0),
    "location": "View3D > Add > Mesh > SpiralParabola",
    "description": "Adds a new SpiralParabola",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Add Mesh"}

# name your mesh
meshname = "SpiralParabola"

import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty, IntProperty, FloatProperty, BoolProperty, StringProperty, EnumProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
import bmesh
from blender_scripts.modules import blender_utilities

# Import necessary class here
from GWL.SpiralParabola import SpiralSphere, SpiralParabola, StarParabola

class OBJECT_OT_add_foobar_idname(Operator, AddObjectHelper):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_spiral_parabola"
    bl_label = "Add SpiralParabola Object"
    bl_description = "Add a new SpiralParabola"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    # Add properties here

    method = EnumProperty(items = (("SpiralSphere", "SpiralSphere", "SpiralSphere"),
      ("SpiralParabola","SpiralParabola","SpiralParabola"),
      ("StarParabola","StarParabola", 'StarParabola'),
      ('GeodesicParabola', 'GeodesicParabola', 'GeodesicParabola'),
      ('MathFunctionParabola', 'MathFunctionParabola', 'MathFunctionParabola'),
      ),
      default='StarParabola', name = "method")

    a = FloatProperty(name="a", description="y = a*x^2", default=1, min=0)
    b = FloatProperty(name="b", description="y = b*x^2", default=1, min=0)
    #rstart = FloatProperty(name="rstart", description="rstart", default=5, min=0)
    #thickness = FloatProperty(name="thickness", description="thickness", default=3, min=0)
    #hole_radius = FloatProperty(name="hole_radius", description="hole_radius", default=2.5, min=0)
    #ZtoX_radius_ratio = FloatProperty(name="ZtoX_radius_ratio", description="ZtoX_radius_ratio", default=0.6, min=0)
    #deltaR = FloatProperty(name="deltaR", description="deltaR", default=0.2, min=0)
    #deltaP = FloatProperty(name="deltaP", description="deltaP", default=6, min=0)
    #phi_start = FloatProperty(name="phi_start", description="phi_start", default=0, min=0)
    #voxelX = FloatProperty(name="voxelX", description="voxelX", default=0.3, min=0)
    #overlap = FloatProperty(name="overlap", description="overlap", default=0.5, min=0)
    #deltaR_increasing = BoolProperty(name="deltaR_increasing", description="deltaR_increasing", default=True)
    #theta_increasing = BoolProperty(name="theta_increasing", description="theta_increasing", default=True)
    #TopHemiparabola = BoolProperty(name="TopHemiparabola", description="TopHemiparabola", default=True)

    def draw(self, context):
      layout = self.layout
      box = layout.box()
      box.prop(self, 'method')
      if self.method == "SpiralSphere":
        box.prop(self, 'a')
      else:
        box.prop(self, 'b')
    
    def execute(self, context):
        
        if self.method == 'SpiralSphere':
          obj = SpiralSphere()
          pass
        elif self.method == 'SpiralParabola':
          pass
        elif self.method == 'StarParabola':
          # Create object here
          obj = StarParabola()
          obj.a = self.a
        elif self.method == 'GeodesicParabola':
          pass
        elif self.method == 'MathFunctionParabola':
          pass
          
        #return {'FINISHED'}
        
        ## Create object here
        #obj = SpiralParabola()
        #obj.radius = self.radius
        #obj.rstart = self.rstart
        #obj.thickness = self.thickness
        #obj.hole_radius = self.hole_radius
        #obj.ZtoX_radius_ratio = self.ZtoX_radius_ratio
        #obj.deltaR = self.deltaR
        #obj.deltaP = self.deltaP
        #obj.phi_start = self.phi_start
        #obj.voxelX = self.voxelX
        #obj.overlap = self.overlap
        #obj.TopHemiparabola = self.TopHemiparabola
        #if self.deltaR_increasing:
          #obj.deltaR_direction = 1
        #else:
          #obj.deltaR_direction = -1
        #if self.theta_increasing:
          #obj.theta_direction = 1
        #else:
          #obj.theta_direction = -1
        
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
        text="Add SpiralParabola",
        icon='PLUGIN')


# This allows you to right click on a button and link to the manual
def add_foobar_idname_manual_map():
    url_manual_prefix = "http://wiki.blender.org/index.php/Doc:2.6/Manual/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_spiral_parabola", "Modeling/Objects"),
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
