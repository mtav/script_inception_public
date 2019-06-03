# based on code from: http://blenderartists.org/forum/showthread.php?200311-Creating-a-Object-Selection-Box-in-Panel-UI-of-Blender-2-5

bl_info = {
    "name": "New Object",
    "author": "Your Name Here",
    "version": (1, 0),
    "blender": (2, 65, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Adds a new Mesh Object",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Add Mesh"}


import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector


def add_object(self, context):
    
    print('self.obj_000 = ', self.obj_000)
    print('self.obj_111 = ', self.obj_111)
    
    if self.obj_000 in bpy.data.objects.keys():
        vec0 = bpy.data.objects[self.obj_000].location
    else:
        vec0 = Vector((0,0,0))

    if self.obj_111 in bpy.data.objects.keys():
        vec1 = bpy.data.objects[self.obj_111].location
    else:
        vec1 = Vector((1,1,1))
        
#    obj_000 = bpy.data.objects[self.obj_000]
#    obj_111 = bpy.data.objects[self.obj_111]
    
#    print((obj_000,obj_111))
#    scale_x = self.scale.x
#    scale_y = self.scale.y

    verts = [Vector(), vec1-vec0]

    edges = [[0,1]]
    faces = []

    mesh = bpy.data.meshes.new(name="New Object Mesh")
    mesh.from_pydata(verts, edges, faces)
    # useful for development when the mesh may be invalid.
    # mesh.validate(verbose=True)
    new_object_base = object_data_add(context, mesh, operator=self)
    print('new_object_base = ', new_object_base)
    new_object_base.object.location = vec0


class OBJECT_OT_add_object(Operator, AddObjectHelper):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_object"
    bl_label = "Add Mesh Object"
    bl_options = {'REGISTER', 'UNDO'}

    scale = FloatVectorProperty(
            name="scale",
            default=(1.0, 1.0, 1.0),
            subtype='TRANSLATION',
            description="scaling",
            )

    obj_000 = bpy.props.StringProperty()
    obj_111 = bpy.props.StringProperty()
        
    def draw(self, context):
        obj = context.object
        layout = self.layout
        layout.label(text=" Simple Row:")
        layout.prop_search(self, "obj_000",  context.scene, "objects")
        layout.prop_search(self, "obj_111",  context.scene, "objects")

    def execute(self, context):

        add_object(self, context)

        return {'FINISHED'}


# Registration

def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_object.bl_idname,
        text="Add Object",
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
