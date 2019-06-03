#!/usr/bin/env python3
# -*- coding: utf-8 -*-

bl_info = {
    "name": "SpiralPhasePlate",
    "author": "mtav",
    "version": (1, 0),
    "blender": (2, 65, 0),
    "location": "View3D > Add > Mesh > SpiralPhasePlate",
    "description": "Adds a new SpiralPhasePlate",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Add Mesh"}

# name your mesh
meshname = "SpiralPhasePlate"

import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty, IntProperty, FloatProperty, BoolProperty, StringProperty, EnumProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
import bmesh
from blender_scripts.modules import blender_utilities

# Import necessary class here
from GWL.SpiralPhasePlate import SpiralPhasePlate

class OBJECT_OT_add_spiral_phase_plate(Operator, AddObjectHelper, SpiralPhasePlate):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_spiral_phase_plate"
    bl_label = "Add SpiralPhasePlate Object"
    bl_description = "Add a new SpiralPhasePlate"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    ### Option to disable automatic 3D view updates
    #update_view = BoolProperty(name="truncateBottom", description="truncateBottom", default=SpiralPhasePlate().truncateBottom)

    ### Add properties here
    maxHeight = FloatProperty(name="maxHeight", description="maxHeight", default=SpiralPhasePlate().maxHeight)
    radius = FloatProperty(name="radius", description="radius", default=SpiralPhasePlate().radius, min=0)
    N_Discontinuities = IntProperty(name="N_Discontinuities", description="N_Discontinuities", default=SpiralPhasePlate().N_Discontinuities, min=0)
    phiStep = FloatProperty(name="phiStep", description="phiStep", default=SpiralPhasePlate().phiStep)
    radialStep = FloatProperty(name="radialStep", description="radialStep", default=SpiralPhasePlate().radialStep)
    heightStep = FloatProperty(name="heightStep", description="heightStep", default=SpiralPhasePlate().heightStep)
    N_HeightSteps = IntProperty(name="N_HeightSteps", description="N_HeightSteps", default=SpiralPhasePlate().N_HeightSteps, min=0)
    truncateBottom = BoolProperty(name="truncateBottom", description="truncateBottom", default=SpiralPhasePlate().truncateBottom)
    minZ = FloatProperty(name="minZ", description="minZ", default=SpiralPhasePlate().minZ)

    def execute(self, context):

        # compute points
        self.computePoints()
        
        # create blender mesh
        verts_loc, edges, faces = self.getMeshData()

        mesh = bpy.data.meshes.new(name = meshname)
        mesh.from_pydata(verts_loc, edges, faces)
        # useful for development when the mesh may be invalid.
        # mesh.validate(verbose=True)

        # add the mesh as an object into the scene with this utility module
        from bpy_extras import object_utils
        object_utils.object_data_add(context, mesh, operator=self)

        return {'FINISHED'}

# Registration

def add_spiral_phase_plate_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_spiral_phase_plate.bl_idname,
        text="Add SpiralPhasePlate",
        icon='PLUGIN')


# This allows you to right click on a button and link to the manual
def add_spiral_phase_plate_manual_map():
    url_manual_prefix = "http://wiki.blender.org/index.php/Doc:2.6/Manual/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_spiral_phase_plate", "Modeling/Objects"),
        )
    return url_manual_prefix, url_manual_mapping


def register():
    bpy.utils.register_class(OBJECT_OT_add_spiral_phase_plate)
    bpy.utils.register_manual_map(add_spiral_phase_plate_manual_map)
    bpy.types.INFO_MT_mesh_add.append(add_spiral_phase_plate_button)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_spiral_phase_plate)
    bpy.utils.unregister_manual_map(add_spiral_phase_plate_manual_map)
    bpy.types.INFO_MT_mesh_add.remove(add_spiral_phase_plate_button)


if __name__ == "__main__":
    register()
