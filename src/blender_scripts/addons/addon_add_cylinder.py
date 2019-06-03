bl_info = {
    "name": "Cylinder + AABB bounding box",
    "author": "mtav",
    "version": (1, 0),
    "blender": (2, 75, 0),
    "location": "View3D > Add > Mesh > Cylinder + AABB Bounding Box",
    "description": "Adds a new cylinder defined by centre+direction and the corresponding Axis-Aligned Bounding Box.",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
    }

# .. todo:: Make FDTD cylinder & co (from FDTDMenu.py) subclasses of such basic CAD addons.

import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty, FloatProperty, BoolProperty, StringProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector

import numpy
from utilities.geometry import getAABBCylinder
from blender_scripts.modules.GeometryObjects import add_cylinder

def add_object(self, context):
    u = self.direction/numpy.linalg.norm(self.direction)
    A = numpy.array(self.location) - self.length/2 * u
    B = numpy.array(self.location) + self.length/2 * u
    add_cylinder(self, A, B, name=self.name, cylinder_radius=self.radius)
    
    if self.AABB:
      (minBB, maxBB) = getAABBCylinder(A, B, self.radius)
      
      ##    bpy.ops.mesh.primitive_cylinder_add(radius=self.radius, depth=self.length, location=self.centre)
      ##   https://www.gamedev.net/forums/topic/338522-bounding-box-for-a-cylinder/?PageSpeed=noscript
      ## .. todo:: Figure out why this formula is correct.
      ## .. todo:: Create shared function to get AABB bounding box (maybe there is some library?)
      ## .. todo:: Create new operator to create box using lower+upper
      #D = B - A
      #kx = numpy.sqrt((D[1]**2+D[2]**2)/(self.length**2))
      #ky = numpy.sqrt((D[0]**2+D[2]**2)/(self.length**2))
      #kz = numpy.sqrt((D[0]**2+D[1]**2)/(self.length**2))
      
      #minBB = numpy.minimum(A,B)
      #maxBB = numpy.maximum(A,B)
      
      #minBB -= Vector([kx*self.radius, ky*self.radius, kz*self.radius])
      #maxBB += Vector([kx*self.radius, ky*self.radius, kz*self.radius])
      
      #S = numpy.abs(maxBB-minBB)
      #print('S',S)
      
      #bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2, view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
      #    bpy.ops.mesh.primitive_cube_add(radius=1, location=(0, 0, 0))
      
      bpy.ops.mesh.primitive_cube_add(location=(0,0,0),rotation=(0,0,0))
      bpy.context.object.draw_type = 'WIRE'
      obj = bpy.context.active_object
      obj.name = '{}.AABB'.format(self.name) # 'AABB_bounding_box'
      
      pos = 0.5*(minBB + maxBB)
      diag = maxBB-minBB
      obj.scale = 0.5*diag
      obj.location = pos
    
    return

class OBJECT_OT_add_object(Operator, AddObjectHelper):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_object"
    bl_label = "Add Cylinder + AABB bounding box"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}
  
    name = StringProperty(
            name="name",
            default='Cylinder',
            )
  
    #centre = FloatVectorProperty(
            #name="centre",
            #default=(1.0, 1.0, 1.0),
            #)
    location = FloatVectorProperty(
            name="Location",
            subtype='TRANSLATION',
            )
            
    direction = FloatVectorProperty(
            name="direction",
            default=(1.0, 1.0, 1.0),
            )

    radius = FloatProperty(
            name="radius",
            default=0.5,
            min=0,
            )
    
    length = FloatProperty(
            name="length",
            default=10,
            min=0,
            )
    
    AABB = BoolProperty(
            name="Axis-Aligned Bounding Box (AABB)",
            default=True,
            )
    
    def invoke(self, context, event):
      self.location = bpy.context.scene.cursor_location
      return self.execute(context)
    
    def draw(self, context):
      layout = self.layout
      box = layout.box()
      box.prop(self, 'name')
      box.prop(self, 'location')
      box.prop(self, 'direction')
      box.prop(self, 'radius')
      box.prop(self, 'length')
      box.prop(self, 'AABB')
      return

    def execute(self, context):

        add_object(self, context)

        return {'FINISHED'}


# Registration

def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_object.bl_idname,
        text="Add Cylinder + AABB bounding box",
        icon='PLUGIN')

# This allows you to right click on a button and link to the manual
def add_object_manual_map():
    url_manual_prefix = "http://wiki.blender.org/index.php/Doc:2.6/Manual/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_object", "Modeling/Objects"),
        )
    return url_manual_prefix, url_manual_mapping

def register():
    bpy.utils.register_class(OBJECT_OT_add_object)
    bpy.utils.register_manual_map(add_object_manual_map)
    bpy.types.INFO_MT_mesh_add.append(add_object_button)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_object)
    bpy.utils.unregister_manual_map(add_object_manual_map)
    bpy.types.INFO_MT_mesh_add.remove(add_object_button)

if __name__ == "__main__":
    register()
