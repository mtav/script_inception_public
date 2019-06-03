bl_info = {
    "name": "Polygon",
    "author": "Mike Taverne",
    "version": (1, 0),
    "blender": (2, 75, 0),
    "location": "View3D > Add > Mesh > Add Polygon Object",
    "description": "Adds a new Polygon Object",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
    }

import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty, FloatProperty, IntProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector

import utilities.polygon_info

def add_polygon(self, context):

    bpy.ops.mesh.primitive_cylinder_add(vertices=self.p.getN(), radius=self.p.getRadius(), depth=self.depth)
                                    
#    scale_x = self.scale.x
#    scale_y = self.scale.y
#
#    verts = [Vector((-1 * scale_x, 1 * scale_y, 0)),
#             Vector((1 * scale_x, 1 * scale_y, 0)),
#             Vector((1 * scale_x, -1 * scale_y, 0)),
#             Vector((-1 * scale_x, -1 * scale_y, 0)),
#            ]
#
#    edges = []
#    faces = [[0, 1, 2, 3]]
#
#    mesh = bpy.data.meshes.new(name="New Object Mesh")
#    mesh.from_pydata(verts, edges, faces)
#    # useful for development when the mesh may be invalid.
#    # mesh.validate(verbose=True)
#    object_data_add(context, mesh, operator=self)


class OBJECT_OT_add_polygon(Operator, AddObjectHelper):
    """Create a new Polygon Object"""
    bl_idname = "mesh.add_polygon"
    bl_label = "Add Polygon Object"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    depth = FloatProperty(
            name="Depth",
            default=1.0,
            description="Depth",
            min=0,
            )

    N = IntProperty(
            name="Vertices",
            default=3,
            description="Number of vertices",
            min=3,
            )

    Rv = FloatProperty(
            name="Rv",
            default=1.0,
            description="Radius to vertices",
            min=0,
            )
    
    S = FloatProperty(
            name="S",
            default=1.0,
            description="Side length",
            min=0,
            )

#    cornerCutRatio = FloatProperty(
#            name="cornerCutRatio",
#            description="cornerCutRatio (alpha=2*dist(P2,I23)/dist(P2,P3))",
#            min=0, max=6./5.,
#            default = 0.7,
#            update = update_cornerCutRatio
#            )
#
#    FillFactor_percent = FloatProperty(
#            name="Fill factor (%)",
#            description="Fill factor (%)",
#            default = 100*TapsteriteFillFactor(0.7),
#            min = 100*1/24,
#            max = 100*23/24,
#            update = update_FillFactor_percent
#            )

    area = FloatProperty(
            name="area",
            default=1.0,
            description="area",
            min=0,
            )

    p = utilities.polygon_info.polygon()
#    p.setRadius(self.radius)
#    p.setN(self.N)

    def draw(self, context):
      layout = self.layout
      box = layout.box()
      box.prop(self, 'N')
      box.prop(self, 'Rv')
      box.prop(self, 'depth')
      box.prop(self, 'area')
      box.prop(self, 'S')
#      box.prop(self, 'view_align')
#      box.prop(self, 'location')
#      box.prop(self, 'rotation')
#      box.prop(self, 'scale')
      return

    def execute(self, context):
        self.p.setN(self.N)
#        self.p.setArea(self.area)
        self.p.setSideLength(self.S)
        add_polygon(self, context)

        return {'FINISHED'}


# Registration

def add_polygon_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_polygon.bl_idname,
        text="Add Polygon",
        icon='PLUGIN')


# This allows you to right click on a button and link to the manual
def add_polygon_manual_map():
    url_manual_prefix = "http://wiki.blender.org/index.php/Doc:2.6/Manual/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_polygon", "Modeling/Objects"),
        )
    return url_manual_prefix, url_manual_mapping


def register():
    bpy.utils.register_class(OBJECT_OT_add_polygon)
    bpy.utils.register_manual_map(add_polygon_manual_map)
    bpy.types.INFO_MT_mesh_add.append(add_polygon_button)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_polygon)
    bpy.utils.unregister_manual_map(add_polygon_manual_map)
    bpy.types.INFO_MT_mesh_add.remove(add_polygon_button)

if __name__ == "__main__":
    register()
