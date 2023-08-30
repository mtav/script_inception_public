#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###############################
# UTILITY FUNCTIONS
###############################
# TODO: Function to align an object with an axis
# TODO: Make sure rotation matrix is correct
# TODO: Should not be added to blender dir by setup scripts.

bl_info = {"name":"blender_utilities", "category": "User"}

# Utility functions for Blender scripts

import bpy
import math
import bmesh
import warnings
import bpy_types
import collections
from bpy_extras import object_utils
from numpy import pi, cos, sin
from mathutils import Vector, Matrix, Color
import warnings

###################
def createBmeshFrompyData(verts_loc, edges, faces):
    '''
    Create a simple **bmesh** based on verts_loc, edges, faces lists, i.e. so called *pyData*.
    
    If you have a variable of the form pyData = (verts_loc, edges, faces), you can call the function using Python's argument unpacking functionality as follows::
    
      createBmeshFrompyData(*pyData)
    '''

    bm = bmesh.new()
    
    for v_co in verts_loc:
        bm.verts.new(v_co)

    # blender 2.73+ fix
    if bpy.app.version >= (2, 73, 0):
        bm.verts.ensure_lookup_table()
    else:
        bm.verts.index_update()
    
    for e_idx in edges:
        bm.edges.new([bm.verts[i] for i in e_idx])
    
    for f_idx in faces:
        bm.faces.new([bm.verts[i] for i in f_idx])
    
    return(bm)

def createMeshFrompyData(pyData, mesh_name='mesh'):
    '''
    Create a simple mesh using pyData directly.
    
    .. note:: Instead of using this function, you can just use the Blender built-in function **from_pydata**.
    
      Example::
      
        mesh = bpy.data.meshes.new(name="New Object Mesh")
        mesh.from_pydata(verts, edges, faces)
        # useful for development when the mesh may be invalid.
        # mesh.validate(verbose=True)
        object_data_add(context, mesh, operator=self)
    '''
    
    warnings.warn('DEPRECATED: This function is deprecated. Please use the Blender built-in function **from_pydata** instead.', DeprecationWarning)
    
    mesh = bpy.data.meshes.new(mesh_name)
    bm = createBmeshFrompyData(*pyData)
    bm.to_mesh(mesh)
    mesh.update()
    return mesh

def createMesh(pyDataGenerator, mesh_name='mesh'):
    '''
    create a simple mesh using a pyData generator function (seems a bit pointless now... ^^)
    '''
    warnings.warn('DEPRECATED: This function is deprecated. Please use the Blender built-in function **from_pydata** instead.', DeprecationWarning)
    return createMeshFrompyData(pyDataGenerator(), mesh_name)

def createObjectFromMesh(mesh, object_name='object', operator=None, context=bpy.context):
    '''
    create a simple object from a mesh
    '''
    
    object_utils.object_data_add(context, mesh, operator=operator)
    #object_utils.object_data_add(context, mesh)
    if bpy.app.version >= (2, 80, 0):
      obj = bpy.context.object
    else:
      obj = context.scene.objects.active
    #print(obj)
    obj.name = object_name
    return (obj,mesh)

def createMeshFromBmesh(bm, mesh_name='mesh'):
    mesh = bpy.data.meshes.new(mesh_name)
    bm.to_mesh(mesh)
    mesh.update()
    return mesh

def createObjectFromBmesh(bm, object_name='object', mesh_name='mesh', operator=None, context=bpy.context):
    mesh = createMeshFromBmesh(bm, mesh_name)
    (obj,mesh) = createObjectFromMesh(mesh, object_name, operator=operator, context=context)
    return (obj,mesh)

def addSimpleObject(pyDataGenerator, object_name='object', mesh_name='mesh', context=bpy.context, operator=None):
    '''
    add a simple object
    '''
    mesh = createMesh(pyDataGenerator, mesh_name)
    (obj,mesh) = createObjectFromMesh(mesh, object_name, context=context, operator=operator)
    return (obj,mesh)

###################
def addToBmesh(bm_dst, bm_src):
    '''
    Utility function to add one bmesh **bm_src** to another bmesh **bm_dst**.
    
    :param bmesh bm_dst: the destination bmesh to add to
    :param bmesh bm_src: the source bmesh to add
    
    :return: (verts, edges, faces), lists of the vertices, edges and faces added to **bm_dst**. The items in the lists are of type *bmesh.types.BMVert*, *bmesh.types.BMEdge*, *bmesh.types.BMFace*.
    '''

    # update indices
    for idx,v in enumerate(bm_src.verts):
        v.index = idx + len(bm_dst.verts)
    
    verts = []
    edges = []
    faces = []
    # add pyData from bmesh
    for v in bm_src.verts:
        verts.append(bm_dst.verts.new(v.co))

    # blender 2.73+ fix
    if bpy.app.version >= (2, 73, 0):
        bm_dst.verts.ensure_lookup_table()
    else:
        bm_dst.verts.index_update()

    for e in bm_src.edges:
        edges.append(bm_dst.edges.new([bm_dst.verts[i] for i in [i.index for i in e.verts] ]))

    for f in bm_src.faces:
        faces.append(bm_dst.faces.new([bm_dst.verts[i] for i in [i.index for i in f.verts] ]))

    return verts, edges, faces

###################
# Converts a faceCoords list of the form [(vec3, vec3, ...), (vec3, vec3, ...), ...] into a list of vertex indices of the form [(i,j,...),(k,l,...),...] based on a list of vertices verts of the form [vec3, vec3, ...]
def faceCoordsToIndices(faceCoords, verts):
    faceIndices = []
    for f in faceCoords:
        faceIndices.append( list((verts.index(p) for p in f)) )
    return faceIndices
###################
def getTetraHedron(P0,P1,P2,P3):
    verts=[P0,P1,P2,P3]
    facesCoords_tetra = [(P2, P1, P0),
             (P0, P1, P3),
             (P1, P2, P3),
             (P2, P0, P3)]

    faceIndices = faceCoordsToIndices(facesCoords_tetra, verts)

    return verts, faceIndices

def getPyDataHexagon(noFaces=False):
    verts_loc = []
    edges = []
    faces = []
    
    N = 6
    for i in range(N):
        theta = i*(2*pi/N)
        verts_loc.append([cos(theta), sin(theta),0])
        if noFaces:
            edges.append((i,(i+1)%N))
        
    if not noFaces:
        faces.append(range(N))
        
    return (verts_loc, edges, faces)

def getPyDataTetraHedron():
    edges = []
    verts_loc, faces = getTetraHedron((1,0,0),(0,1,0),(0,0,1),(1,1,1))
    return (verts_loc, edges, faces)

###########
def duplicateObject(obj, linked=True, translation_vector = (0,0,0), context=bpy.context):
  ''' Duplicate an object and return the created duplicate. '''
  bpy.ops.object.select_all(action = 'DESELECT')
  obj.select = True
  context.scene.objects.active = obj
  if linked:
    bpy.ops.object.duplicate_move_linked(TRANSFORM_OT_translate={"value":translation_vector})
  else:
    bpy.ops.object.duplicate_move(TRANSFORM_OT_translate={"value":translation_vector})
  duplicate = context.object
  return duplicate

def createGroup(obj_list, active_object=None, context = bpy.context, group_name='Collection', include_children=True, parent_collection = None):
  '''
  Creates a group containing objects from *obj_list*.
  active_object : Object to make active if specified.
  context : bpy.context
  group_name : optional group name
  
  For Blender >=2.8, Collections are created instead of groups.

  TODO: Get rid of support for older Blender versions.
  TODO: Refactor to createCollection. cf make_collection, etc functions.
  '''

  # warnings.simplefilter('always', DeprecationWarning)
  # warnings.warn("createGroup is deprecated. Please use createCollection() instead.", DeprecationWarning)

  # Select objects:
  obj_list = selectObjects(obj_list, active_object=active_object, context = bpy.context, include_children=include_children)

  if bpy.app.version >= (2, 80, 0):

        # Remove selected objects from all collections:
        bpy.ops.collection.objects_remove_all()

        # Create collection:
        # myCol = bpy.data.collections.new(group_name)
        # Add to scene
        # bpy.context.scene.collection.children.link(myCol)
        myCol = make_collection(group_name, parent_collection=parent_collection, checkExisting=False)

        # Add objects to collection:
        for obj in obj_list:
            myCol.objects.link(obj)

        return myCol
  else:
    if group_name:
      bpy.ops.group.create(name=group_name)
    else:
      bpy.ops.group.create()
  return

def selectObjects(obj_list, active_object=None, context = bpy.context, include_children=False):
  '''
  Select objects in *obj_list* and return selected objects.

  Unhiding and rehiding objects to select all objects, including hidden ones is not possible, because unhiding them deselects them too.
  '''
  if not isinstance(obj_list, collections.abc.Iterable):
    obj_list = [obj_list]

  ##### recursively include children
  if include_children:
      children = []
      for obj in obj_list:
        children.extend(obj.children_recursive)
      obj_list.extend(children)

  ##### Check for any hidden objects
  for obj in obj_list:
      if obj.hide_get():
          raise Exception(f'{obj} is hidden. Selection will fail.')

  bpy.ops.object.select_all(action = 'DESELECT')
  for obj in obj_list:
    if bpy.app.version >= (2, 80, 0):
      obj.select_set(True)
    else:
      obj.select = True

  if active_object:
    if bpy.app.version >= (2, 80, 0):
      context.view_layer.objects.active = active_object
    else:
      context.scene.objects.active = active_object

  return bpy.context.selected_objects

def setOrigin(obj, loc):
    # store cursor location
    if bpy.app.version >= (2, 80, 0):
      orig_cursor = bpy.context.scene.cursor.location.copy()
    else:
      orig_cursor = bpy.context.scene.cursor_location.copy()
    # move cursor
    if bpy.app.version >= (2, 80, 0):
      bpy.context.scene.cursor.location = loc
    else:
      bpy.context.scene.cursor_location = loc
    # select object
    selectObjects([obj])
    # change origin
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    # restore cursor location
    if bpy.app.version >= (2, 80, 0):
      bpy.context.scene.cursor.location = orig_cursor
    else:
      bpy.context.scene.cursor_location = orig_cursor

def grid_index(Nx, Ny, Nz, i, j, k):
    return (Ny*Nz*i + Nz*j + k)

def Orthogonal(vec):
    # ..todo:: create Blender independent version and just use Vector() for input/output conversion when calling the function...
    vec = Vector(vec)
    xx = abs(vec.x)
    yy = abs(vec.y)
    zz = abs(vec.z)
    if (xx < yy):
        if xx < zz:
            return Vector([0,vec.z,-vec.y])
        else:
            return Vector([vec.y,-vec.x,0])
    else:
        if yy < zz:
            return Vector([-vec.z,0,vec.x])
        else:
            return Vector([vec.y,-vec.x,0])

def rotationMatrix(axis_point, axis_direction, angle_degrees):
  ''' return a rotation matrix for a rotation around an arbitrary axis '''
  axis = Vector([axis_direction[0],axis_direction[1],axis_direction[2]])
  C = Vector([axis_point[0],axis_point[1],axis_point[2]])
  T = Matrix.Translation(C)
  Tinv = Matrix.Translation(-C)
  R = Matrix.Rotation(math.radians(angle_degrees), 4, axis)
  return T*R*Tinv

def loadBasicMaterials():
  '''
  Define some basic materials for easy "coloring".
  '''
  if 'red' not in [i.name for i in bpy.data.materials]:
    material = bpy.data.materials.new('red')
    setDiffuseColor(material, Color((1, 0, 0)))
  if 'green' not in [i.name for i in bpy.data.materials]:
    material = bpy.data.materials.new('green')
    setDiffuseColor(material, Color((0, 1, 0)))
  if 'blue' not in [i.name for i in bpy.data.materials]:
    material = bpy.data.materials.new('blue')
    setDiffuseColor(material, Color((0, 0, 1)))

  if 'cyan' not in [i.name for i in bpy.data.materials]:
    material = bpy.data.materials.new('cyan')
    setDiffuseColor(material, Color((0, 1, 1)))
  if 'magenta' not in [i.name for i in bpy.data.materials]:
    material = bpy.data.materials.new('magenta')
    setDiffuseColor(material, Color((1, 0, 1)))
  if 'yellow' not in [i.name for i in bpy.data.materials]:
    material = bpy.data.materials.new('yellow')
    setDiffuseColor(material, Color((1, 1, 0)))

  if 'black' not in [i.name for i in bpy.data.materials]:
    material = bpy.data.materials.new('black')
    setDiffuseColor(material, Color((0, 0, 0)))
  if 'white' not in [i.name for i in bpy.data.materials]:
    material = bpy.data.materials.new('white')
    setDiffuseColor(material, Color((1, 1, 1)))

def setDiffuseColor(material, color_object, alpha=1):
  '''Extra function to simplify backward compatibility. color_object should be a Color object and can be defined as follows: color_object=Color((R,G,B)).'''
  if bpy.app.version >= (2, 80, 0):
    material.diffuse_color[0] = color_object[0] # red
    material.diffuse_color[1] = color_object[1] # green
    material.diffuse_color[2] = color_object[2] # blue
    material.diffuse_color[3] = alpha            # alpha
  else:
    material.diffuse_color = color_object
    material.alpha = alpha

def joinObjects(obj_list, origin=None, name=None, context = bpy.context):
  ''' Joins the objects from *obj_list* into a single object, sets the origin to *origin*, names the new object *name* and returns it.'''
  
  selectObjects(obj_list, active_object=None, context = context)
  bpy.ops.object.join()
  
  obj = context.active_object
  if name:
    obj.name = name
  if origin is not None:
    setOrigin(obj, origin)
  return(obj)

def add_array_modifier(obj, label, size, vec3):
  ''' Simple function to simplify creating arrays. '''
  array_mod = obj.modifiers.new(label, 'ARRAY')
  array_mod.count = size
  array_mod.use_constant_offset = True
  array_mod.use_relative_offset = False
  array_mod.constant_offset_displace = vec3

########################################################################
# new blender >=2.8 code:
# source: https://devtalk.blender.org/t/what-are-the-python-codes-related-to-collection-actions-for-blender-2-8/4479/4
def find_collection(context, item):
    '''
    Return one of the collections that item belongs to.
    '''
    collections = item.users_collection
    if len(collections) > 0:
        return collections[0]
    return context.scene.collection

def make_collection(collection_name, parent_collection = None, checkExisting=True, make_active=False):
  '''
  Create a new collection.
  '''
  if bpy.app.version >= (2, 80, 0):
    if parent_collection is None:
      parent_collection = bpy.context.scene.collection
    if checkExisting and (collection_name in bpy.data.collections): # Does the collection already exist?
        new_collection = bpy.data.collections[collection_name]
    else:
        new_collection = bpy.data.collections.new(collection_name)
        parent_collection.children.link(new_collection) # Add the new collection under a parent

    if make_active:
        # https://blender.stackexchange.com/questions/127403/change-active-collection
        layer_collection = bpy.context.view_layer.layer_collection.children[new_collection.name]
        bpy.context.view_layer.active_layer_collection = layer_collection

    return new_collection

  else:
    current_group = bpy.data.groups.new(name=collection_name) # blender<2.80
    return current_group.name

def setCollections(obj, collection_list, context=bpy.context):
  '''
  Remove obj from all collections, then add it to collections in collection_list.
  '''

  # print(f'---->setCollections({obj}, {collection_list})')
  for idx, collection in enumerate(collection_list):
    if idx==0:
      addToCollection(obj, collection, removeFromOthers=True, context=bpy.context)
    else:
      addToCollection(obj, collection, removeFromOthers=False, context=bpy.context)

def addToCollection(obj, collection, removeFromOthers=False, context=bpy.context):
  '''
  Add object *obj* to the collection *collection*.
  *collection* can be either a string or an instance of type bpy_types.Collection.

  If removeFromOthers=True, the object will be removed from all other collections.
  '''
  if bpy.app.version >= (2, 80, 0):
    if isinstance(collection, str):
      coll = bpy.data.collections[collection]
    else:
      coll = collection

    if removeFromOthers:
      bpy.ops.collection.objects_remove_all()

    if not coll in obj.users_collection:
      coll.objects.link(obj)
  else:
    setActiveObject(obj, context=context)
    bpy.ops.object.group_link(group=collection)
  return

def setActiveObject(obj, context=bpy.context):
  if bpy.app.version >= (2, 80, 0):
    context.view_layer.objects.active = obj
  else:
    context.scene.objects.active = obj

def getActiveObject(context=bpy.context):
  if bpy.app.version >= (2, 80, 0):
    return context.view_layer.objects.active
  else:
    return context.scene.objects.active

def applyModifiers(obj, context=bpy.context):
    # source: https://blenderartists.org/t/how-to-apply-all-the-modifiers-with-python/1314483/2
    ctx = context.copy()
    ctx['object'] = obj
    for _, m in enumerate(obj.modifiers):
        try:
            ctx['modifier'] = m
            bpy.ops.object.modifier_apply(ctx, modifier=m.name)
        except RuntimeError:
            print(f"Error applying {m.name} to {obj.name}, removing it instead.")
            obj.modifiers.remove(m)

    for m in obj.modifiers:
        obj.modifiers.remove(m)

def removeInteriorFaces(obj, context=bpy.context):
  setActiveObject(obj, context=context)
  
  bpy.ops.object.mode_set(mode='EDIT')

  bpy.ops.mesh.select_mode(type='VERT', action='ENABLE')
  bpy.ops.mesh.select_all(action='SELECT')
  bpy.ops.mesh.remove_doubles()

  bpy.ops.mesh.select_all(action='DESELECT')
  bpy.ops.mesh.select_mode(type='FACE', action='ENABLE')
  bpy.ops.mesh.select_interior_faces()
  bpy.ops.mesh.delete(type='ONLY_FACE')

  # extra non-manifold removal
  bpy.ops.mesh.select_all(action='DESELECT')
  bpy.ops.mesh.select_mode(type='VERT', action='ENABLE')
  bpy.ops.mesh.select_non_manifold()
  bpy.ops.mesh.delete(type='EDGE_FACE')

  bpy.ops.object.mode_set(mode='OBJECT')
  return
########################################################################

if __name__ == '__main__':
  pass
