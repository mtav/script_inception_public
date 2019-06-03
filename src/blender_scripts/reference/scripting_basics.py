# To make Blender happy:
bl_info = {"name":"scripting_basics", "category": "User"}

import bpy
import bmesh
from bpy_extras import object_utils

# simple "pyData" creation function
def getPyDataSquare():
    verts_loc = [[0,0,0],[1,0,0],[1,1,0],[0,1,0]]
    edges = [[0,1],[1,2],[2,3],[3,0]]
    faces = []
    return (verts_loc, edges, faces)

# simple "pyData" creation function
def getPyDataTriangle():
    verts_loc = [[0,0,0],[1,0,0],[0,1,0]]
    edges = []
    faces = [[0,1,2]]
    return (verts_loc, edges, faces)

# create a simple mesh
def createMesh(pyDataGenerator, mesh_name='mesh'):
    mesh = bpy.data.meshes.new(mesh_name)
    
    (verts_loc, edges, faces) = pyDataGenerator()
        
    bm = bmesh.new()
    
    for v_co in verts_loc:
        bm.verts.new(v_co)
    
    for e_idx in edges:
        bm.edges.new([bm.verts[i] for i in e_idx])
    
    for f_idx in faces:
        bm.faces.new([bm.verts[i] for i in f_idx])
    
    bm.to_mesh(mesh)
    mesh.update()
    return mesh

# create a simple object from a mesh
def createObjectFromMesh(mesh, object_name='object'):
    object_utils.object_data_add(bpy.context, mesh, operator=None)
    
    obj = bpy.context.scene.objects.active
    obj.name = object_name
    
    return (obj,mesh)

# add a simple object
def addSimpleObject(pyDataGenerator, object_name='object', mesh_name='mesh'):
    mesh = createMesh(pyDataGenerator, mesh_name)
    (obj,mesh) = createObjectFromMesh(mesh, object_name)
    return (obj,mesh)

if __name__ == '__main__':

  #(obj1,mesh1) = addSimpleObject('foo.object','foo.mesh');
  #(obj2,mesh2) = addSimpleObject('toto.object','toto.mesh');

  #shared_mesh = createMesh(getPyDataSquare, 'shared_mesh')
  shared_mesh = createMesh(getPyDataTriangle, 'shared_mesh')
  (obj1, mesh1) = createObjectFromMesh(shared_mesh,'obj1')
  (obj2, mesh2) = createObjectFromMesh(shared_mesh,'obj2')

  obj1.location = [0,0,0]
  obj2.location = [1,1,1]

  bpy.ops.object.select_all(action = 'DESELECT')

  obj1.select = True
  obj2.select = True

  scene = bpy.context.scene
  scene.objects.active = obj1

  # parenting objects
  bpy.ops.object.parent_set()

  # joining objects
  #bpy.ops.object.join()

  # create a group
  bpy.ops.group.create(name='myLittleGroup')

  # grouping objects
  bpy.ops.object.group_link(group='myLittleGroup')

  # moving selected objects to a specific layer
  bpy.ops.object.move_to_layer(layers=(False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True))

  # setting layers which are on
  bpy.context.scene.layers=(False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True)
