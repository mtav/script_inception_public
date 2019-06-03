bl_info = {
    "name": "Add elliptical rod",
    "author": "mtav",
    "version": (1, 0),
    "blender": (2, 75, 0),
    "location": "View3D > Add > Mesh > Add elliptical rod",
    "description": "Add elliptical rod",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
    }

# .. todo:: Make FDTD cylinder & co (from FDTDMenu.py) subclasses of such basic CAD addons.

import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty, FloatProperty, BoolProperty, StringProperty, IntProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector

import numpy
from utilities.geometry import getAABBCylinder
from blender_scripts.modules.GeometryObjects import add_cylinder, addEllipsoid, add_arrow
import utilities.ellipse

def EllipticalRodMesh(context, location, direction, width, transverse_height, smooth_start, smooth_end, N):
  rod_info = utilities.ellipse.EllipticalRod()
  rod_info.setEllipsoidWidth(width)
  rod_info.setCylinderDiameterBig(transverse_height)
  
  (minor_diameter, major_diameter, alpha_rad) = rod_info.getTiltedEllipseInfo()
  r1 = 0.5*minor_diameter
  r2 = 0.5*major_diameter
  
  location = numpy.array(location)
  direction = numpy.array(direction)
  # minor_axis = numpy.cross(numpy.array([0,0,1]), direction)
  # print(minor_axis)
  minor_axis = numpy.array([direction[1]*direction[2], -direction[0]*direction[2], 0])
  # print(minor_axis)
  
  # major_axis = z axis rotated by alpha_rad around minor_axis
  major_axis = numpy.dot(utilities.common.rotation_matrix3(minor_axis, alpha_rad), numpy.array([0,0,direction[2]]))
  
  minor_axis = minor_axis/numpy.linalg.norm(minor_axis)
  major_axis = major_axis/numpy.linalg.norm(major_axis)
  u = -minor_axis
  v = major_axis
  w = direction
  
  verts = []
  edges = []
  faces = []
  for i in range(N):
    theta = i*2*numpy.pi/N
    P = r1*numpy.cos(theta)*u + r2*numpy.sin(theta)*v
    verts.append(Vector(P))
    verts.append(Vector(P+direction))
    if i < N-1:
      faces.append([2*i, 2*(i+1), 2*(i+1)+1, 2*i+1])
    else:
      faces.append([2*i, 0, 1, 2*i+1])
      
  faces.append([2*(N-1-i) for i in range(N)])
  faces.append([2*i+1 for i in range(N)])
  
  if smooth_start:
    addEllipsoid(context, location, [minor_diameter, minor_diameter, rod_info.getEllipsoidHeightZ()], e0=[1,0,0], e1=[0,1,0], e2=[0,0,1])
  if smooth_end:
    addEllipsoid(context, location+direction, [minor_diameter, minor_diameter, rod_info.getEllipsoidHeightZ()], e0=[1,0,0], e1=[0,1,0], e2=[0,0,1])
  
  # add_arrow(context, location, location+u, name='u', color=[1,0,0])
  # add_arrow(context, location, location+v, name='v', color=[0,1,0])
  # add_arrow(context, location, location+w, name='w', color=[0,0,1])
  
  return verts, edges, faces

class OBJECT_OT_add_object(Operator, AddObjectHelper):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_object"
    bl_label = "Add elliptical rod"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}
  
    name = StringProperty(
            name="name",
            default='EllipticalRod',
            )
  
    #centre = FloatVectorProperty(
            #name="centre",
            #default=(1.0, 1.0, 1.0),
            #)
    location = FloatVectorProperty(
            name="Location",
            subtype='TRANSLATION',
            )
  
    # direction = EnumProperty(items = (("1,1,1","1,1,1","define the parallelepiped by specifying the edge vectors e1,e2,e3"),

    direction = FloatVectorProperty(
            name="direction",
            default=(1.0, 1.0, 1.0),
            )

    Nvertices = IntProperty(
            name="Nvertices",
            default=32,
            min=0)
            
    width = FloatProperty(
            name="width",
            default=0.4,
            min=0,
            )
    
    transverse_height = FloatProperty(
            name="transverse height",
            default=0.5,
            min=0,
            )
    
    # length = FloatProperty(
            # name="length",
            # default=10,
            # min=0,
            # )
    
    smooth_start = BoolProperty(
            name="Smooth start",
            default=False,
            )
    smooth_end = BoolProperty(
            name="Smooth end",
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
      box.prop(self, 'width')
      box.prop(self, 'transverse_height')
      box.prop(self, 'smooth_start')
      box.prop(self, 'smooth_end')
      box.prop(self, 'Nvertices')
      return

    def execute(self, context):
      verts, edges, faces = EllipticalRodMesh(context, self.location, self.direction, self.width, self.transverse_height, self.smooth_start, self.smooth_end, self.Nvertices)
      mesh = bpy.data.meshes.new(name="EllipticalRod")
      mesh.from_pydata(verts, edges, faces)
      # useful for development when the mesh may be invalid.
      # mesh.validate(verbose=True)
      object_data_add(context, mesh, operator=self)
      return {'FINISHED'}


# Registration

def add_object_button(self, context):
  self.layout.operator(
      OBJECT_OT_add_object.bl_idname,
      text="Add elliptical rod",
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
