#!/usr/bin/env python3
# -*- coding: utf-8 -*-

bl_info = {
    "name": "Unit cube",
    "author": "mtav",
    "version": (1, 0),
    "blender": (3, 4, 0),
    "location": "View3D > Add > Mesh > Unit Cube",
    "description": "Adds a new unit cube",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh"}

import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty, BoolProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
import blender_scripts.modules.mesh
from blender_scripts.modules.blender_utilities import setOrigin

class OBJECT_OT_add_unit_cube(Operator, AddObjectHelper):
    """Create a new unit cube"""
    bl_idname = "mesh.add_unit_cube"
    bl_label = "Add unit cube"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    scale : FloatVectorProperty(
            name="scale",
            default=(1.0, 1.0, 1.0),
            subtype='TRANSLATION',
            description="scaling",
            )
            
    origin : FloatVectorProperty(name="origin", default=(0, 0, 0))
    wiremode : BoolProperty(name="wiremode", default=True)
    origin_is_lower : BoolProperty(name="Origin is lower corner", default=True)

    def draw(self, context):
      layout = self.layout
      box = layout.box()
      box.prop(self, 'origin')
      box.prop(self, 'origin_is_lower')
      box.prop(self, 'wiremode')
      
      #box.prop(self, 'view_align') # blender <=2.79
      box.prop(self, 'align') # blender >=2.8
      box.prop(self, 'location')
      box.prop(self, 'rotation')
      box.prop(self, 'scale')

      return

    def execute(self, context):
      
      # manual creation
      scale_x = self.scale.x
      scale_y = self.scale.y
      scale_z = self.scale.z

      origin = Vector(self.origin)

      #verts = [
               #origin + Vector((0*scale_x, 0*scale_y, 1*scale_z)),
               #origin + Vector((0*scale_x, 1*scale_y, 1*scale_z)),
               #origin + Vector((1*scale_x, 1*scale_y, 1*scale_z)),
               #origin + Vector((1*scale_x, 0*scale_y, 1*scale_z)),
               #origin + Vector((1*scale_x, 0*scale_y, 0*scale_z)),
               #origin + Vector((1*scale_x, 1*scale_y, 0*scale_z)),
               #origin + Vector((0*scale_x, 1*scale_y, 0*scale_z)),
               #origin + Vector((0*scale_x, 0*scale_y, 0*scale_z)),
              #]

      #edges = []

      #faces = []
      #faces.append([3,2,1,0])
      #faces.append([7,6,5,4])
      #faces.append([0,1,6,7])
      #faces.append([1,2,5,6])
      #faces.append([2,3,4,5])
      #faces.append([3,0,7,4])

      if self.origin_is_lower:
        verts, edges, faces = blender_scripts.modules.mesh.block(origin+0.5*self.scale, self.scale)
      else:
        verts, edges, faces = blender_scripts.modules.mesh.block(origin, self.scale)

      mesh = bpy.data.meshes.new(name="UnitCube")
      mesh.from_pydata(verts, edges, faces)
      # useful for development when the mesh may be invalid.
      # mesh.validate(verbose=True)
      object_data_add(context, mesh, operator=self)

      ## creation using primitive_cube_add() (does not work properly if 3D cursor is not at origin)
      #bpy.ops.mesh.primitive_cube_add()
      #obj = bpy.context.active_object
      #setOrigin(obj,[-1,-1,-1])
      #obj.dimensions = [1,1,1]
      #obj.location = [0,0,0]
      #obj.name = 'UnitCube'
      #obj.data.name = 'UnitCube'
      #bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
      
      if self.wiremode:
        context.object.display_type = 'WIRE'
      
      return {'FINISHED'}

# Registration
def add_unit_cube_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_unit_cube.bl_idname,
        text="Add unit cube",
        icon='MESH_CUBE')

def register():
    bpy.utils.register_class(OBJECT_OT_add_unit_cube)
    bpy.types.VIEW3D_MT_mesh_add.append(add_unit_cube_button)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_unit_cube)
    bpy.types.VIEW3D_MT_mesh_add.remove(add_unit_cube_button)

if __name__ == "__main__":
    register()
