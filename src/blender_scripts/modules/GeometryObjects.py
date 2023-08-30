#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Extra objects for Blender. Arrows, etc.

"self" should be some operator usable by bpy_extras.object_utils.object_data_add().

.. todo:: Use to create Excitation objects , unit cubes, boxes, etc.
.. todo:: figure out Blender's matrix system properly and make it easy to place new objects at cursor, etc.
.. todo:: notation consistency: use 0-indexing everywhere (a0,a1,a2)
.. todo:: addon to visualize crystal (with option to restrict to cuboid volume, etc), using sphere mesh (or user-provided) + array modifiers, with option to switch between direct and reciprocal lattice and/or show both, etc
.. todo:: 2D/3D array modifier addon
.. todo:: lattice type detector + auto-creation of first BZ and standard labels
.. todo:: make functions return a mesh for blender's add_object call (bmesh system instead of working with objects?)
'''

# To make Blender happy:
bl_info = {"name":"GeometryObjects - MODULE - NOT ADDON", "category": "Module", 'warning': 'MODULE - NOT ADDON'}

import bpy
import numpy
from mathutils import Vector, Matrix, Color
from bpy_extras.object_utils import object_data_add
from blender_scripts.modules.blender_utilities import Orthogonal, setOrigin, selectObjects, loadBasicMaterials, createGroup
import utilities.common

def add_tetra(self, location=[1/4,1/4,1/4], size=1/2, name='Tetra', cylinder_radius=None):
  
  location = Vector(location)
  
  obj_list = []
  obj_list.append(add_cylinder(self, location, location + size*Vector([-0.5, -0.5, -0.5]), cylinder_radius=cylinder_radius))
  obj_list.append(add_cylinder(self, location, location + size*Vector([ 0.5,  0.5, -0.5]), cylinder_radius=cylinder_radius))
  obj_list.append(add_cylinder(self, location, location + size*Vector([-0.5,  0.5,  0.5]), cylinder_radius=cylinder_radius))
  obj_list.append(add_cylinder(self, location, location + size*Vector([ 0.5, -0.5,  0.5]), cylinder_radius=cylinder_radius))
  
  common_mesh = obj_list[0].data
  for obj in obj_list[1:]:
    obj.data = common_mesh
  return(obj_list)

def getRotationMatrixFromAxis(axis):
  # define world rotation matrix
  axisZ = Vector(axis) # because the default primitive cone is oriented along -Z, unlike the one imported from Blender UI...
  axisX = Orthogonal(axisZ)
  axisY = axisZ.cross(axisX)
  axisX.normalize()
  axisY.normalize()
  axisZ.normalize()
  axisX.resize_4d(); axisX[3] = 0
  axisY.resize_4d(); axisY[3] = 0
  axisZ.resize_4d(); axisZ[3] = 0
  axisW = Vector((0,0,0,1))
  rotmat = Matrix((axisX,axisY,axisZ,axisW))
  rotmat.transpose()
  return(rotmat)

def add_block(blender_operator, location3 = [0, 0, 0], size3 = [1, 1, 1], name='Block', wiremode=False):
  
  # add cube
  bpy.ops.mesh.primitive_cube_add(location = location3)
  
  # get added object
  obj = bpy.context.active_object
  
  # set properties
  obj.name = name
  obj.scale = 0.5*numpy.array(size3)
  bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

  if wiremode:
    obj.display_type = 'WIRE'
  
  return(obj)

def add_cylinder(self, start_point, end_point, name='Cylinder', cylinder_radius=None):
  
    # convert start and end points to vectors
    P1 = Vector(start_point)
    P2 = Vector(end_point)
    
    # define location and size of the cylinder
    cylinder_length = (P2-P1).length
    if cylinder_length != 0:
      normalized_direction_vector = (P2-P1)/cylinder_length
    else:
      normalized_direction_vector = Vector([0,0,1])
    
    if cylinder_radius is None:
      cylinder_radius = cylinder_length/40.0
    
    cylinder_center = P1 + (0.5*cylinder_length)*normalized_direction_vector
    
    #print('cylinder_center = {}'.format(cylinder_center))
    #print('cylinder_length = {}'.format(cylinder_length))
    #print('cylinder_radius = {}'.format(cylinder_radius))
    
    ## define world rotation matrix
    #axisZ = (P2-P1) # because the default primitive cone is oriented along -Z, unlike the one imported from Blender UI...
    #axisX = Orthogonal(axisZ)
    #axisY = axisZ.cross(axisX)
    #axisX.normalize()
    #axisY.normalize()
    #axisZ.normalize()
    #axisX.resize_4d(); axisX[3] = 0
    #axisY.resize_4d(); axisY[3] = 0
    #axisZ.resize_4d(); axisZ[3] = 0
    #axisW = Vector((0,0,0,1))
    #rotmat = Matrix((axisX,axisY,axisZ,axisW))
    #rotmat.transpose()
    
    rotmat = getRotationMatrixFromAxis(P2-P1)
    
    # add cylinder
    bpy.ops.mesh.primitive_cylinder_add(location = Vector(cylinder_center), radius=cylinder_radius, depth=cylinder_length, rotation=(0,0,0))
    cylinder_obj = bpy.context.active_object
    cylinder_obj.matrix_world = rotmat
    cylinder_obj.location = cylinder_center
    
    # name object and mesh
    cylinder_obj.name = name
    cylinder_obj.data.name = name + '.mesh'
    
    return(cylinder_obj)

def add_cone(self, start_point, end_point, name='Cone', radius1=None, radius2=None):
  # convert start and end points to vectors
  P1 = Vector(start_point)
  P2 = Vector(end_point)
  
  # define location and size of the cylinder
  length = (P2-P1).length
  if length != 0:
    normalized_direction_vector = (P2-P1)/length
  else:
    normalized_direction_vector = Vector([0,0,1])
  
  if radius1 is None:
    radius1 = 2*length/40.0
  if radius2 is None:
    radius2 = length/40.0
  
  center = P1 + (0.5*length)*normalized_direction_vector
  
  N = 32
  verts = []
  edges = []
  faces = []
  for i in range(N):
    theta = i*2*numpy.pi/N
    x1 = radius1*numpy.cos(theta)
    y1 = radius1*numpy.sin(theta)
    z1 = -length/2
    x2 = radius2*numpy.cos(theta)
    y2 = radius2*numpy.sin(theta)
    z2 = length/2
    verts.append(Vector((x1,y1,z1)))
    verts.append(Vector((x2,y2,z2)))
    if i < N-1:
      faces.append([2*i, 2*(i+1), 2*(i+1)+1, 2*i+1])
    else:
      faces.append([2*i, 0, 1, 2*i+1])
      
  faces.append([2*(N-1-i) for i in range(N)])
  faces.append([2*i+1 for i in range(N)])
  
  mesh = bpy.data.meshes.new(name=name)
  mesh.from_pydata(verts, edges, faces)
  # useful for development when the mesh may be invalid.
  # mesh.validate(verbose=True)
  #object_data_add(bpy.context, mesh, operator=self)
  object_data_add(bpy.context, mesh)
  
  rotmat = getRotationMatrixFromAxis(utilities.common.unitVector(P2-P1))
  
  # add cylinder
  #bpy.ops.mesh.primitive_cylinder_add(location = Vector(cylinder_center), radius=cylinder_radius, depth=cylinder_length, rotation=(0,0,0))
  blender_obj = bpy.context.active_object
  blender_obj.matrix_world = rotmat
  blender_obj.location = center
  
  # name object and mesh
  blender_obj.name = name
  blender_obj.data.name = name + '.mesh'
  
  return(blender_obj)

def add_gwl_cylinder(self, start_point, end_point, name='Cylinder', cylinder_radius=None, cross_section_r0=0.05, cross_section_delta_r=0.1, cross_section_delta_theta=0.1, longitudinal_delta=0.1):
  return add_gwl_cone(self, start_point, end_point, name=name, radius1=cylinder_radius, radius2=cylinder_radius,
    cross_section_r0=cross_section_r0,
    cross_section_delta_r=cross_section_delta_r,
    cross_section_delta_theta=cross_section_delta_theta,
    longitudinal_delta=longitudinal_delta)

def add_gwl_cone(self, start_point, end_point, name='Cone', radius1=None, radius2=None, cross_section_r0=0.05, cross_section_delta_r=0.1, cross_section_delta_theta=0.1, longitudinal_delta=0.1):
  # .. todo:: integrate late with add_cone? Create a cone class with different writers? extend exisiting cone class? (but remember to leave useful standalone classes for generic blender addons...)
  
  # convert start and end points to vectors
  P1 = Vector(start_point)
  P2 = Vector(end_point)
  
  # define location and size of the cylinder
  length = (P2-P1).length
  if length != 0:
    normalized_direction_vector = (P2-P1)/length
  else:
    normalized_direction_vector = Vector([0,0,1])
  
  if radius1 is None:
    radius1 = 2*length/40.0
  if radius2 is None:
    radius2 = length/40.0
  
  center = P1 + (0.5*length)*normalized_direction_vector
  
  verts = []
  edges = []
  faces = []
  
  Nsections = int(numpy.ceil( length/longitudinal_delta + 1))
  
  for idx_z in range(Nsections):
    z = -length/2 + (idx_z/(Nsections-1))*length
    Rmax = ((radius2-radius1)/length)*(z+length/2) + radius1
    if Rmax > cross_section_r0:
      Nlayers = int(numpy.ceil( 1 + (Rmax-cross_section_r0)/cross_section_delta_r ))
    else:
      Nlayers = 1
    for idx_layer in range(Nlayers):
      if Nlayers > 1:
        r = cross_section_r0 + (idx_layer/(Nlayers-1))*(Rmax - cross_section_r0)
      else:
        r = min(cross_section_r0, Rmax)
      Nverts = int(numpy.ceil( (2*numpy.pi*r)/cross_section_delta_theta ))
      for idx_vert in range(Nverts):
        theta = idx_vert*2*numpy.pi/Nverts
        x = r*numpy.cos(theta)
        y = r*numpy.sin(theta)
        verts.append(Vector((x,y,z)))
        if idx_vert > 0:
          edges.append([len(verts)-2, len(verts)-1])
    
  mesh = bpy.data.meshes.new(name=name)
  mesh.from_pydata(verts, edges, faces)
  # useful for development when the mesh may be invalid.
  # mesh.validate(verbose=True)
  #object_data_add(bpy.context, mesh, operator=self)
  object_data_add(bpy.context, mesh)
  
  rotmat = getRotationMatrixFromAxis(utilities.common.unitVector(P2-P1))
  
  # add cylinder
  #bpy.ops.mesh.primitive_cylinder_add(location = Vector(cylinder_center), radius=cylinder_radius, depth=cylinder_length, rotation=(0,0,0))
  blender_obj = bpy.context.active_object
  blender_obj.matrix_world = rotmat
  blender_obj.location = center
  
  # name object and mesh
  blender_obj.name = name
  blender_obj.data.name = name + '.mesh'
  
  return(blender_obj)

def add_bend(centre=[0,0,0], bend_radius=1, tube_radius=0.1, name='bend', angle_start_deg=0, angle_end_deg=90):
  
  centre = numpy.array(centre)
  
  verts = []
  edges = []
  faces = []
  
  Nbend = 32
  Ncircle = 32
  
  uy = numpy.array([0, 1, 0])
  
  for j, phi_deg in enumerate(numpy.linspace(angle_start_deg, angle_end_deg, Nbend)):
    phi_rad = numpy.deg2rad(phi_deg)
    # phi = idx_bend*(numpy.pi/2)/(Nbend-1)
    P = centre + bend_radius*numpy.array([numpy.cos(phi_rad), 0, numpy.sin(phi_rad)])
    # P = bend_radius*numpy.array([numpy.cos(phi_rad), 0, numpy.sin(phi_rad)])
    # verts.append(P)
    
    for i in range(Ncircle):
      theta = i*2*numpy.pi/Ncircle
      e_r = numpy.array([numpy.cos(phi_rad), 0, numpy.sin(phi_rad)])
      M = P + tube_radius*(numpy.cos(theta)*e_r + numpy.sin(theta)*uy)
      verts.append(M)
      
  for j in range(Nbend-1):
    for i in range(Ncircle):
      if i < Ncircle-1:
        faces.append([(i) + (j)*Ncircle,
                    (i+1) + (j)*Ncircle,
                    (i+1) + (j+1)*Ncircle,
                    (i) + (j+1)*Ncircle])
      else:
        faces.append([(i) + (j)*Ncircle,
                    (0) + (j)*Ncircle,
                    (0) + (j+1)*Ncircle,
                    (i) + (j+1)*Ncircle])
    
  faces.append(list(reversed(range(Ncircle))))
  faces.append([i+(Nbend-1)*Ncircle for i in range(Ncircle)])
  
  mesh = bpy.data.meshes.new(name=name)
  mesh.from_pydata(verts, edges, faces)
  # useful for development when the mesh may be invalid.
  # mesh.validate(verbose=True)
  #object_data_add(bpy.context, mesh, operator=self)
  object_data_add(bpy.context, mesh)
  
  blender_obj = bpy.context.active_object
  blender_obj.location = [0,0,0]
  
  return(blender_obj)

def add_gwl_bend(centre=[0,0,0], bend_radius=1, tube_radius=0.1, name='bend', angle_start_deg=0, angle_end_deg=90, cross_section_r0=0.05, cross_section_delta_r=0.1, cross_section_delta_theta=0.1, longitudinal_delta=0.1):
  
  # .. todo:: generic GWL disk creation with normal direction specification, etc...
  # .. todo:: bends that get larger/smaller, i.e. conic bends...
  # .. todo:: generic line thickening system... (post-process a line with bevel/taper system)
  
  centre = numpy.array(centre)
  
  verts = []
  edges = []
  faces = []
  
  uy = numpy.array([0, 1, 0])
  
  Nbend = int(numpy.ceil( 1 + (bend_radius*numpy.deg2rad(abs(angle_end_deg-angle_start_deg)))/longitudinal_delta ))
  
  for j, phi_deg in enumerate(numpy.linspace(angle_start_deg, angle_end_deg, Nbend)):
    phi_rad = numpy.deg2rad(phi_deg)
    P = centre + bend_radius*numpy.array([numpy.cos(phi_rad), 0, numpy.sin(phi_rad)])
    # P = bend_radius*numpy.array([numpy.cos(phi_rad), 0, numpy.sin(phi_rad)])
    
    if tube_radius > cross_section_r0:
      Nlayers = int(numpy.ceil( 1 + (tube_radius-cross_section_r0)/cross_section_delta_r ))
    else:
      Nlayers = 1
    for idx_layer in range(Nlayers):
      if Nlayers > 1:
        r = cross_section_r0 + (idx_layer/(Nlayers-1))*(tube_radius - cross_section_r0)
      else:
        r = min(cross_section_r0, tube_radius)
      Nverts = int(numpy.ceil( (2*numpy.pi*r)/cross_section_delta_theta ))
      for idx_vert in range(Nverts):
        theta = idx_vert*2*numpy.pi/Nverts
        e_r = numpy.array([numpy.cos(phi_rad), 0, numpy.sin(phi_rad)])
        M = P + r*(numpy.cos(theta)*e_r + numpy.sin(theta)*uy)
        verts.append(M)
        if idx_vert > 0:
          edges.append([len(verts)-2, len(verts)-1])
      
  mesh = bpy.data.meshes.new(name=name)
  mesh.from_pydata(verts, edges, faces)
  # useful for development when the mesh may be invalid.
  # mesh.validate(verbose=True)
  #object_data_add(bpy.context, mesh, operator=self)
  object_data_add(bpy.context, mesh)
  
  blender_obj = bpy.context.active_object
  blender_obj.location = [0,0,0]
  
  return(blender_obj)

def add_arrow(self, start_point, end_point, name='arrow', cone_length=None, cone_radius=None, cylinder_radius=None, color=None):
    # ..todo:: fix/prevent cone longer than arrow?
  
    # convert start and end points to vectors
    P1 = Vector(start_point)
    P2 = Vector(end_point)
    
    # define location and size of the arrow components
    arrow_length = (P2-P1).length
    
    # handle zero-size arrow by placing sphere instead
    if arrow_length == 0:
      bpy.ops.mesh.primitive_uv_sphere_add(size=cone_radius, location=start_point)
      arrow_cylinder_obj = bpy.context.active_object
      
    else:
      normalized_direction_vector = (P2-P1)/arrow_length
      
      if cone_length is None:
        cone_length = arrow_length/5.0
      if cone_radius is None:
        cone_radius = arrow_length/20.0
      if cylinder_radius is None:
        cylinder_radius = cone_radius/2.0
      
      cylinder_length = arrow_length - cone_length
      cylinder_center = P1 + (0.5*cylinder_length)*normalized_direction_vector
      cone_center = P1 + (cylinder_length + 0.5*cone_length)*normalized_direction_vector
      
      #    print('cylinder_center = {}'.format(cylinder_center))
      #    print('cylinder_length = {}'.format(cylinder_length))
      #    print('cylinder_radius = {}'.format(cylinder_radius))
      #    
      #    print('cone_center = {}'.format(cone_center))
      #    print('cone_length = {}'.format(cone_length))
      #    print('cone_radius = {}'.format(cone_radius))
      
      # define world rotation matrix
      axisZ = (P2-P1) # because the default primitive cone is oriented along -Z, unlike the one imported from Blender UI...
      axisX = Orthogonal(axisZ)
      axisY = axisZ.cross(axisX)
      axisX.normalize()
      axisY.normalize()
      axisZ.normalize()
      axisX.resize_4d(); axisX[3] = 0
      axisY.resize_4d(); axisY[3] = 0
      axisZ.resize_4d(); axisZ[3] = 0
      axisW = Vector((0,0,0,1))
      rotmat = Matrix((axisX,axisY,axisZ,axisW))
      rotmat.transpose()

      # add cylinder
      bpy.ops.mesh.primitive_cylinder_add(location = Vector(cylinder_center), radius=cylinder_radius, depth=cylinder_length, rotation=(0,0,0))
      arrow_cylinder_obj = bpy.context.active_object
      arrow_cylinder_obj.matrix_world = rotmat
      arrow_cylinder_obj.location = cylinder_center

      # add cone
      bpy.ops.mesh.primitive_cone_add(radius1=cone_radius, depth=cone_length, location=Vector(cone_center), rotation=(0, 0, 0))
      arrow_cone_obj = bpy.context.active_object
      arrow_cone_obj.matrix_world = rotmat
      arrow_cone_obj.location = cone_center

      # join cylinder and cone
      bpy.ops.object.select_all(action = 'DESELECT')
      bpy.context.view_layer.objects.active = arrow_cylinder_obj
      arrow_cylinder_obj.select_set(True)
      arrow_cone_obj.select_set(True)
      bpy.ops.object.join()
    
    # name object and mesh
    arrow_cylinder_obj.name = name
    arrow_cylinder_obj.data.name = name+'.mesh'
    
    # set origin of created arrow object to P1
    setOrigin(arrow_cylinder_obj, P1)
    
    # apply rotation and scale
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    
    if color is not None:
      mat = bpy.data.materials.new('arrow-material')
      mat.diffuse_color = color
      bpy.ops.object.material_slot_add()
      arrow_cylinder_obj.material_slots[-1].material = mat
    
    return(arrow_cylinder_obj)

def add_lattice_vectors(self, a0, a1, a2, name='lattice_vectors', shift_origin=False, cone_length=None, cone_radius=None, cylinder_radius=None):
  
  loadBasicMaterials()
  
  a0 = Vector(a0)
  a1 = Vector(a1)
  a2 = Vector(a2)
  centro = 0.5*(a0+a1+a2)
  
  if shift_origin:
    start_point = -centro
  else:
    start_point = Vector([0,0,0])
  
  # get shortest arrow length
  arrow_length = min(a0.length, a1.length, a2.length)
  if not cone_length:
    cone_length = arrow_length/5.0
  if not cone_radius:
    cone_radius = arrow_length/20.0
  if not cylinder_radius:
    cylinder_radius = cone_radius/2.0
  
  obj_a0 = add_arrow(self, start_point, start_point+a0, name='a0', cone_length=cone_length, cone_radius=cone_radius, cylinder_radius=cylinder_radius)
  bpy.ops.object.material_slot_add()
  obj_a0.material_slots[obj_a0.material_slots.__len__() - 1].material = bpy.data.materials['red']

  obj_a1 = add_arrow(self, start_point, start_point+a1, name='a1', cone_length=cone_length, cone_radius=cone_radius, cylinder_radius=cylinder_radius)
  bpy.ops.object.material_slot_add()
  obj_a1.material_slots[obj_a1.material_slots.__len__() - 1].material = bpy.data.materials['green']

  obj_a2 = add_arrow(self, start_point, start_point+a2, name='a2', cone_length=cone_length, cone_radius=cone_radius, cylinder_radius=cylinder_radius)
  bpy.ops.object.material_slot_add()
  obj_a2.material_slots[obj_a2.material_slots.__len__() - 1].material = bpy.data.materials['blue']
  
  bpy.ops.object.add(type='EMPTY')
  obj_empty = bpy.context.active_object
  obj_empty.name = name
  selectObjects([obj_empty, obj_a0, obj_a1, obj_a2], active_object=obj_empty, context = bpy.context)
  bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
  
  return (obj_empty, obj_a0, obj_a1, obj_a2)

def add_lattice_cell(self, a0, a1, a2, name='lattice_cell', shift_origin=False, wiremode=True):
  a0 = Vector(a0)
  a1 = Vector(a1)
  a2 = Vector(a2)
  centro = 0.5*(a0+a1+a2)
  
  if shift_origin:
    start_point = -centro
  else:
    start_point = Vector([0,0,0])

  verts = [
            start_point + 0*a0 + 0*a1 + 1*a2,
            start_point + 0*a0 + 1*a1 + 1*a2,
            start_point + 1*a0 + 1*a1 + 1*a2,
            start_point + 1*a0 + 0*a1 + 1*a2,
            start_point + 1*a0 + 0*a1 + 0*a2,
            start_point + 1*a0 + 1*a1 + 0*a2,
            start_point + 0*a0 + 1*a1 + 0*a2,
            start_point + 0*a0 + 0*a1 + 0*a2,
          ]

  edges = []

  faces = []
  faces.append([3,2,1,0])
  faces.append([7,6,5,4])
  faces.append([0,1,6,7])
  faces.append([1,2,5,6])
  faces.append([2,3,4,5])
  faces.append([3,0,7,4])

  mesh = bpy.data.meshes.new(name="UnitCube")
  mesh.from_pydata(verts, edges, faces)
  # useful for development when the mesh may be invalid.
  # mesh.validate(verbose=True)
  if 'layers' in dir(self):
    object_data_add(bpy.context, mesh, operator=self)
  else:
    object_data_add(bpy.context, mesh, operator=None)
  obj_lattice_cell = bpy.context.active_object
  obj_lattice_cell.name = name
  
  if wiremode:
    bpy.context.object.display_type = 'WIRE'

  return (obj_lattice_cell)

def add_lattice_objects(self, a0, a1, a2, b0, b1, b2, name='lattice_objects', cone_length=None, cone_radius=None, cylinder_radius=None):
  
  loadBasicMaterials()

  # add non-shifted lattice cell
  shift_origin = False
  (obj_lat_empty, obj_lat_a0, obj_lat_a1, obj_lat_a2) = add_lattice_vectors(self, a0, a1, a2, name='lattice_vectors', shift_origin=shift_origin, cone_length=cone_length, cone_radius=cone_radius, cylinder_radius=cylinder_radius)
  obj_lat_cell = add_lattice_cell(self, a0, a1, a2, name='lattice_cell', shift_origin=shift_origin, wiremode=True)
  # parent cell to empty
  selectObjects([obj_lat_cell], active_object=obj_lat_empty, context = bpy.context)
  bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

  # add shifted lattice cell
  shift_origin = True
  (obj_lat_shifted_empty, obj_lat_shifted_a0, obj_lat_shifted_a1, obj_lat_shifted_a2) = add_lattice_vectors(self, a0, a1, a2, name='lattice_vectors-shifted', shift_origin=shift_origin, cone_length=cone_length, cone_radius=cone_radius, cylinder_radius=cylinder_radius)
  obj_lat_shifted_cell = add_lattice_cell(self, a0, a1, a2, name='lattice_cell-shifted', shift_origin=shift_origin, wiremode=True)
  # parent cell to empty
  selectObjects([obj_lat_shifted_cell], active_object=obj_lat_shifted_empty, context = bpy.context)
  bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

  # add non-shifted reciprocal lattice cell
  shift_origin = False
  (obj_rec_lat_empty, obj_rec_lat_b0, obj_rec_lat_b1, obj_rec_lat_b2) = add_lattice_vectors(self, b0, b1, b2, name='reciprocal_lattice_vectors', shift_origin=shift_origin, cone_length=cone_length, cone_radius=cone_radius, cylinder_radius=cylinder_radius)
  obj_rec_lat_cell = add_lattice_cell(self, b0, b1, b2, name='reciprocal_lattice_cell', shift_origin=shift_origin, wiremode=True)
  obj_rec_lat_b0.name = 'b0'
  obj_rec_lat_b1.name = 'b1'
  obj_rec_lat_b2.name = 'b2'
  # parent cell to empty
  selectObjects([obj_rec_lat_cell], active_object=obj_rec_lat_empty, context = bpy.context)
  bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

  # add shifted reciprocal lattice cell
  shift_origin = True
  (obj_rec_lat_shifted_empty, obj_rec_lat_shifted_b0, obj_rec_lat_shifted_b1, obj_rec_lat_shifted_b2) = add_lattice_vectors(self, b0, b1, b2, name='reciprocal_lattice_vectors-shifted', shift_origin=shift_origin, cone_length=cone_length, cone_radius=cone_radius, cylinder_radius=cylinder_radius)
  obj_rec_lat_shifted_cell = add_lattice_cell(self, b0, b1, b2, name='reciprocal_lattice_cell-shifted', shift_origin=shift_origin, wiremode=True)
  obj_rec_lat_shifted_b0.name = 'b0'
  obj_rec_lat_shifted_b1.name = 'b1'
  obj_rec_lat_shifted_b2.name = 'b2'
  # parent cell to empty
  selectObjects([obj_rec_lat_shifted_cell], active_object=obj_rec_lat_shifted_empty, context = bpy.context)
  bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

  ##### Group objects into collections
  lattice_objects = [obj_lat_empty,
                      obj_lat_shifted_empty,
                      obj_rec_lat_empty,
                      obj_rec_lat_shifted_empty,
                      ]

  # children = []
  # for obj in obj_list:
  #   children.extend(obj.children_recursive)
  # obj_list.extend(children)

  # hide_settings = [obj.hide_get() for obj in obj_list]
  # for obj in obj_list:
  #   obj.hide_set(False)

  # print(100*'<')
  # obj_list = selectObjects(obj_list, include_children=True)
  # print('Selected objects:')
  # for idx, obj in enumerate(bpy.context.selected_objects):
  #     print(idx, obj)
  # print(100*'>')

  # myCol = createGroup(obj_list, active_object=None, context=bpy.context, group_name="Lattice objects")

  # myCollection = make_coll

  # for h, obj in zip(hide_settings, obj_list):
  #   obj.hide_set(h)

  # TODO: figure out why this fails with "incorrect context":
  #selectObjects([obj_lat_empty, obj_lat_a0, obj_lat_a1, obj_lat_a2, obj_lat_cell], context=bpy.context)
  #bpy.ops.object.hide_view_set(unselected=False)
  #selectObjects([obj_lat_shifted_empty, obj_lat_shifted_a0, obj_lat_shifted_a1, obj_lat_shifted_a2, obj_lat_shifted_cell], context=bpy.context)
  #bpy.ops.object.hide_view_set(unselected=False)

  #selectObjects([obj_rec_lat_empty, obj_rec_lat_b0, obj_rec_lat_b1, obj_rec_lat_b2, obj_rec_lat_cell])
  #selectObjects([obj_rec_lat_shifted_empty, obj_rec_lat_shifted_b0, obj_rec_lat_shifted_b1, obj_rec_lat_shifted_b2, obj_rec_lat_shifted_cell])
  
  # TODO: group or somehow organize all these objects...
  #selectObjects([obj_lat_cell, obj_lat_empty])
  #bpy.ops.object.group_link(group=group_name)

  ##### Visibility settings.
  # These must come after setting everything else up, as Blender does not allow selecting hidden objects.
  # And hiding selected objects, deselects them.
  for i in [obj_lat_empty, obj_lat_a0, obj_lat_a1, obj_lat_a2, obj_lat_cell]:
    i.hide_set(True)

  for i in [obj_lat_shifted_empty, obj_lat_shifted_a0, obj_lat_shifted_a1, obj_lat_shifted_a2, obj_lat_shifted_cell]:
    i.hide_set(True)

  for i in [obj_rec_lat_empty, obj_rec_lat_b0, obj_rec_lat_b1, obj_rec_lat_b2, obj_rec_lat_cell]:
    i.hide_set(True)

  for i in [obj_rec_lat_shifted_empty, obj_rec_lat_shifted_b0, obj_rec_lat_shifted_b1, obj_rec_lat_shifted_b2,
            obj_rec_lat_shifted_cell]:
    i.hide_set(True)

  obj_rec_lat_shifted_cell.hide_set(False)
  obj_rec_lat_empty.hide_set(False)
  obj_rec_lat_b0.hide_set(False)
  obj_rec_lat_b1.hide_set(False)
  obj_rec_lat_b2.hide_set(False)

  return lattice_objects

def addEllipsoid(self, location, size, e0=[1,0,0], e1=[0,1,0], e2=[0,0,1]):
  # add UV sphere
  bpy.ops.mesh.primitive_uv_sphere_add()
  
  # get a handle on it
  blender_obj = bpy.context.active_object
  blender_obj.location = Vector(location)
  
  e0 = size[0]/2*utilities.common.unitVector(e0)
  e1 = size[1]/2*utilities.common.unitVector(e1)
  e2 = size[2]/2*utilities.common.unitVector(e2)
  
  for v in blender_obj.data.vertices:
    p = v.co.x*e0 + v.co.y*e1 + v.co.z*e2
    v.co = p
  
  return blender_obj
