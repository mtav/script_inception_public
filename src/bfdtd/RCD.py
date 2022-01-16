#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
RCD BFDTD objects

RCD = Rod Connected Diamond

.. todo:: Hexagonal layout
.. todo:: Blender addon
.. todo:: FCC sphere structure
.. todo:: general lattice + unit cell system like MPB (with all the 14 3D bravais lattices? or at least BCC/FCC/hex)
.. todo:: PyQt interface
.. todo:: Add option to write out unit cells and lattice vectors for easier understanding (part of blender add-on?)
'''

import os
import copy
import tempfile

import numpy
from numpy import array, sqrt
from numpy.linalg import norm

# .. todo:: simplify to something like import bfdtd in the future. (look up info on good module layout practice)
from .BFDTDobject import BFDTDobject
from .GeometryObjects import GeometryObject, Cylinder, Distorted, Parallelepiped, Sphere, Block
from .meshobject import MeshObject
from .excitation import Excitation, ExcitationWithGaussianTemplate, ExcitationWithUniformTemplate

from meshing.meshing import linspaces, HeterogeneousMesh1D, HomogeneousMesh1D, HomogeneousMeshParameters1D, Mesh1D, Mesh3D, MultiMesh1D

class RCD_HexagonalLattice(GeometryObject):
  ''' This class allows you to create RCD structures with some cylinders alligned along the Z axis. '''

  def __init__(self):
    ''' constructor '''
    GeometryObject.__init__(self)
    self.name = self.__class__.__name__
    self.inner_radius = 0
    self.outer_radius = 0.1
    self.cubic_unit_cell_size = 1
    self.geo_list = None
    self.unit_cell_index_list = None
    
    self.unit_cell_type = 1
    
    self.shifted = False
    
    # quick and dirty, but so that DH can do more crazy things until we find a better solution...
    self.use_spheres = False
    self.use_cylinders = True
    self.add_bottom_sphere = False
    self.relative_sphere_radius = 1
    self.relative_sphere_index = 1
    
    # The tetrahedron centres
    self.__R0__ = array([ sqrt(2)/4,   1/sqrt(6),     sqrt(3)/4])
    self.__R1__ = array([-sqrt(2)/4,   1/sqrt(6),     sqrt(3)/4])
    self.__R2__ = array([         0, -1/sqrt(24),     sqrt(3)/4])

    self.__G0__ = array([ sqrt(2)/4,           0,  7*sqrt(3)/12])
    self.__G1__ = array([         0,   sqrt(6)/4,  7*sqrt(3)/12])
    self.__G2__ = array([-sqrt(2)/4,           0,  7*sqrt(3)/12])

    self.__B0__ = array([ sqrt(2)/4,  -1/sqrt(6), 11*sqrt(3)/12])
    self.__B1__ = array([         0,  1/sqrt(24), 11*sqrt(3)/12])
    self.__B2__ = array([-sqrt(2)/4,  -1/sqrt(6), 11*sqrt(3)/12])
    
    # cell type 1 parameters
    self.__offset1__ = array([ sqrt(2)/4, 0, 11*sqrt(3)/24])
    self.__u1__ = array([sqrt(2)/4, -sqrt(6)/4, 0])
    self.__v1__ = array([sqrt(2)/4,  sqrt(6)/4, 0])
    self.__w1__ = array([0, 0, sqrt(3)])

    # cell type 2 parameters
    self.__offset2__ = array([-sqrt(2)/4, 0, 11*sqrt(3)/24])
    self.__u2__ = array([sqrt(2)/2, 0, 0])
    self.__v2__ = array([0, sqrt(6)/2, 0])
    self.__w2__ = array([0, 0, sqrt(3)])

  def setShifted(self, shifted):
    self.shifted = shifted
    return(self.shifted)

  def setOuterRadius(self, outer_radius):
    ''' set outer radius of rods '''
    self.outer_radius = outer_radius
    return

  def getOuterRadius(self):
    ''' get outer radius of rods '''
    return(self.outer_radius)

  def setLocation(self, location):
    '''Set the location of the RCD.
    
    .. todo:: Add RCD illustrations.
    '''
    self.location = array(location)
    return

  def setCubicUnitCellSize(self, cubic_unit_cell_size):
    self.cubic_unit_cell_size = cubic_unit_cell_size
    return

  def setUnitCellType(self, unit_cell_type):
    self.unit_cell_type = unit_cell_type
    return

  def getUnitCellType(self):
    return(self.unit_cell_type)
    
  def getLatticeVectors(self):
    if self.unit_cell_type == 1:
      return((self.cubic_unit_cell_size*self.__u1__, self.cubic_unit_cell_size*self.__v1__, self.cubic_unit_cell_size*self.__w1__))
    else:
      return((self.cubic_unit_cell_size*self.__u2__, self.cubic_unit_cell_size*self.__v2__, self.cubic_unit_cell_size*self.__w2__))

  def getXMesh(self, Nx, Ny, Nz, NcellsMin):
    X_mesh = MultiMesh1D()
    
    (u,v,w) = self.getLatticeVectors()
    RCD_min_x = -(Nx-1+1/2)*norm(u)
    delta = norm(u)/2
    
    cur_min = self.getLocation()[0] + RCD_min_x
    for i in range((2*Nx-1)*2+1):
      m = HomogeneousMeshParameters1D(cur_min, cur_min+delta)
      m.setNcellsMin(NcellsMin)
      m.name = 'RCD_X_' + str(i)
      #X_mesh.addChild(m)
      X_mesh.mesh_list.append(m)
      cur_min = cur_min + delta

    return(X_mesh)

  def getYMesh(self, Nx, Ny, Nz, NcellsMin):
    Y_mesh = MultiMesh1D()
    
    (u,v,w) = self.getLatticeVectors()
    RCD_min_y = -(Ny-1+1/2+1/6)*norm(v)
    delta = norm(v)/6
    
    cur_min = self.getLocation()[1] + RCD_min_y
    for i in range((2*Ny-1)*6+2):
      m = HomogeneousMeshParameters1D(cur_min, cur_min+delta)
      m.setNcellsMin(NcellsMin)
      m.name = 'RCD_Y_' + str(i)
      #Y_mesh.addChild(m)
      Y_mesh.mesh_list.append(m)
      cur_min = cur_min + delta

    return(Y_mesh)

  def getZMesh(self, Nx, Ny, Nz, NcellsMin1, NcellsMin2):
    Z_mesh = MultiMesh1D()
    
    (u,v,w) = self.getLatticeVectors()
    RCD_min_z = -(Nz-1)*norm(w) - self.__offset2__[2]*self.cubic_unit_cell_size
    delta = norm(w)/12
    
    cur_min = self.getLocation()[2] + RCD_min_z
    for i in range(3*(2*Nz-1)):
      m = HomogeneousMeshParameters1D(cur_min, cur_min+3*delta)
      m.setNcellsMin(NcellsMin1)
      m.name = 'RCD_Z_' + str(i)
      Z_mesh.mesh_list.append(m)

      m = HomogeneousMeshParameters1D(cur_min+3*delta, cur_min+4*delta)
      m.setNcellsMin(NcellsMin2)
      m.name = 'RCD_Z_' + str(i)
      Z_mesh.mesh_list.append(m)
      
      cur_min = cur_min + 4*delta

    return(Z_mesh)

  def getXMesh_with_SpacingMax(self, Nx, Ny, Nz, spacing_max):
    X_mesh = MultiMesh1D()
    
    (u,v,w) = self.getLatticeVectors()
    RCD_min_x = -(Nx-1+1/2)*norm(u)
    delta = norm(u)/2
    
    cur_min = self.getLocation()[0] + RCD_min_x
    for i in range((2*Nx-1)*2+1):
      m = HomogeneousMeshParameters1D(cur_min, cur_min+delta)
      m.setSpacingMax(spacing_max)
      m.name = 'RCD_X_' + str(i)
      #X_mesh.addChild(m)
      X_mesh.mesh_list.append(m)
      cur_min = cur_min + delta

    return(X_mesh)

  def getYMesh_with_SpacingMax(self, Nx, Ny, Nz, spacing_max):
    Y_mesh = MultiMesh1D()
    
    (u,v,w) = self.getLatticeVectors()
    RCD_min_y = -(Ny-1+1/2+1/6)*norm(v)
    delta = norm(v)/6
    
    cur_min = self.getLocation()[1] + RCD_min_y
    for i in range((2*Ny-1)*6+2):
      m = HomogeneousMeshParameters1D(cur_min, cur_min+delta)
      m.setSpacingMax(spacing_max)
      m.name = 'RCD_Y_' + str(i)
      #Y_mesh.addChild(m)
      Y_mesh.mesh_list.append(m)
      cur_min = cur_min + delta

    return(Y_mesh)

  def getZMesh_with_SpacingMax(self, Nx, Ny, Nz, spacing_max):
    Z_mesh = MultiMesh1D()
    
    (u,v,w) = self.getLatticeVectors()
    RCD_min_z = -(Nz-1)*norm(w) - self.__offset2__[2]*self.cubic_unit_cell_size
    delta = norm(w)/12
    
    cur_min = self.getLocation()[2] + RCD_min_z
    for i in range(12*(2*Nz-1)):
      m = HomogeneousMeshParameters1D(cur_min, cur_min+delta)
      m.setSpacingMax(spacing_max)
      m.name = 'RCD_Z_' + str(i)
      Z_mesh.mesh_list.append(m)      
      cur_min = cur_min + delta

    return(Z_mesh)

  def getUnitCell(self):
    ''' Get a Distorted object representing the unit cell '''
    unit_cell = Parallelepiped()
    unit_cell.setDirectionsAndSize(self.__u1__, self.__v1__, self.__w1__, [norm(self.__u1__), norm(self.__v1__), norm(self.__w1__)])
    unit_cell.setLocation(self.getLocation())
    return unit_cell

  def getCubicUnitCell(self):
    ''' Get a Distorted object representing the cubic unit cell '''
    unit_cell = Parallelepiped()
    u1 = [0, 0.8165, 0.57735]
    v1 = [-0.70711, -0.40825, 0.57735]
    w1 = [0.70711, -0.40825, 0.57735]
    unit_cell.setDirectionsAndSize(u1, v1, w1, [norm(u1), norm(v1), norm(w1)])
    unit_cell.setLocation(self.getLocation() + [0, 0, 1.5*self.getRodLength()])
    return unit_cell
    
  def getRodLength(self):
    return(sqrt(3)/4*self.cubic_unit_cell_size)

  def tetra(self, location, name='tetra'):
    '''
    Return a list of 4 cylinders aranged as a "tetrahedron", with one of the cylinders facing downwards.
    *location* is the position of the point at which all cylinders join.
    '''

    geo_list = []
    
    if self.use_cylinders:
      base_cyl = Cylinder()
      base_cyl.setOuterRadius(self.outer_radius)
      base_cyl.setRelativeConductivity(self.getRelativeConductivity())
      base_cyl.setRelativePermittivity(self.getRelativePermittivity())

      cyl0 = copy.deepcopy(base_cyl)
      cyl0.setStartEndPoints(location, location + array([0, 0, -sqrt(3)/4])*self.cubic_unit_cell_size)
      cyl0.setName(name + '.cyl0')

      cyl1 = copy.deepcopy(base_cyl)
      cyl1.setStartEndPoints(location, location + array([0, -1/sqrt(6), sqrt(3)/12])*self.cubic_unit_cell_size)
      cyl1.setName(name + '.cyl1')

      cyl2 = copy.deepcopy(base_cyl)
      cyl2.setStartEndPoints(location, location + array([sqrt(2)/4, 1/sqrt(24), sqrt(3)/12])*self.cubic_unit_cell_size)
      cyl2.setName(name + '.cyl2')

      cyl3 = copy.deepcopy(base_cyl)
      cyl3.setStartEndPoints(location, location + array([-sqrt(2)/4, 1/sqrt(24), sqrt(3)/12])*self.cubic_unit_cell_size)
      cyl3.setName(name + '.cyl3')
      
      geo_list.extend([cyl0, cyl1, cyl2, cyl3])

    if self.use_spheres:
      base_sphere = Sphere()
      base_sphere.setOuterRadius(self.outer_radius*self.relative_sphere_radius)
      base_sphere.setRefractiveIndex(self.getRefractiveIndex()*self.relative_sphere_index)

      sphere0 = copy.deepcopy(base_sphere)
      sphere0.setLocation(location)
      sphere0.setName(name + '.sphere0')

      sphere1 = copy.deepcopy(base_sphere)
      sphere1.setLocation(location + array([0, -1/sqrt(6), sqrt(3)/12])*self.cubic_unit_cell_size)
      sphere1.setName(name + '.sphere1')

      sphere2 = copy.deepcopy(base_sphere)
      sphere2.setLocation(location + array([sqrt(2)/4, 1/sqrt(24), sqrt(3)/12])*self.cubic_unit_cell_size)
      sphere2.setName(name + '.sphere2')

      sphere3 = copy.deepcopy(base_sphere)
      sphere3.setLocation(location + array([-sqrt(2)/4, 1/sqrt(24), sqrt(3)/12])*self.cubic_unit_cell_size)
      sphere3.setName(name + '.sphere3')

      geo_list.extend([sphere0, sphere1, sphere2, sphere3])

    if self.add_bottom_sphere:
      base_sphere = Sphere()
      base_sphere.setOuterRadius(self.outer_radius*self.relative_sphere_radius)
      base_sphere.setRefractiveIndex(self.getRefractiveIndex()*self.relative_sphere_index)

      sphere_bottom = copy.deepcopy(base_sphere)
      sphere_bottom.setLocation(location + array([0, 0, -sqrt(3)/4])*self.cubic_unit_cell_size)
      sphere_bottom.setName(name + '.sphere_bottom')
      geo_list.extend([sphere_bottom])
    
    return(geo_list)

  def unitCellType1(self, i, j, k):
    '''
    A unit-cell containing 3 "tetrahedrons".
    lattice vectors: u1,v1,w1
    '''
    
    geo_list = []
    
    if self.shifted:
      offset = numpy.array([0, 0, -sqrt(3)/2])
    else:
      offset = numpy.array([0, 0, 0])
    unit_cell_location = offset + i*self.__u1__ + j*self.__v1__ + k*self.__w1__
    
    geo_list.extend(self.tetra(self.location + (unit_cell_location - self.__offset1__ + self.__R0__)*self.cubic_unit_cell_size, 'cell.{}.{}.{}.R0'.format(i,j,k)))
    geo_list.extend(self.tetra(self.location + (unit_cell_location - self.__offset1__ + self.__G0__)*self.cubic_unit_cell_size, 'cell.{}.{}.{}.G0'.format(i,j,k)))
    geo_list.extend(self.tetra(self.location + (unit_cell_location - self.__offset1__ + self.__B0__)*self.cubic_unit_cell_size, 'cell.{}.{}.{}.B0'.format(i,j,k)))

    return(geo_list)
  
  def unitCellType2(self, i, j, k):
    '''
    A unit-cell containing 6 "tetrahedrons".
    lattice vectors: u2,v2,w2
    '''

    geo_list = []

    if self.shifted:
      offset = numpy.array([0, 0, -sqrt(3)/2])
    else:
      offset = numpy.array([0, 0, 0])
    unit_cell_location = offset + i*self.__u2__ + j*self.__v2__ + k*self.__w2__
    
    geo_list.extend(self.tetra(self.location + (unit_cell_location - self.__offset2__ + self.__R1__)*self.cubic_unit_cell_size, 'cell.{}.{}.{}.R1'.format(i,j,k)))
    geo_list.extend(self.tetra(self.location + (unit_cell_location - self.__offset2__ + self.__G1__)*self.cubic_unit_cell_size, 'cell.{}.{}.{}.G1'.format(i,j,k)))
    geo_list.extend(self.tetra(self.location + (unit_cell_location - self.__offset2__ + self.__B1__)*self.cubic_unit_cell_size, 'cell.{}.{}.{}.B1'.format(i,j,k)))

    geo_list.extend(self.tetra(self.location + (unit_cell_location - self.__offset2__ + self.__R2__)*self.cubic_unit_cell_size, 'cell.{}.{}.{}.R2'.format(i,j,k)))
    geo_list.extend(self.tetra(self.location + (unit_cell_location - self.__offset2__ + self.__G2__)*self.cubic_unit_cell_size, 'cell.{}.{}.{}.G2'.format(i,j,k)))
    geo_list.extend(self.tetra(self.location + (unit_cell_location - self.__offset2__ + self.__B2__)*self.cubic_unit_cell_size, 'cell.{}.{}.{}.B2'.format(i,j,k)))

    return(geo_list)
  
  def createGeoList(self):
    if self.unit_cell_index_list is None:
      self.createRectangularArray(1,1,1)
    self.geo_list = []
    for (i,j,k) in self.unit_cell_index_list:
      if self.unit_cell_type == 1:
        self.geo_list.extend(self.unitCellType1(i,j,k))
      else:
        self.geo_list.extend(self.unitCellType2(i,j,k))        
    return(self.geo_list)
    
  def createRectangularArray(self, Nx, Ny, Nz):
    self.unit_cell_index_list = []
    for i in range(Nx):
      for j in range(Ny):
        for k in range(Nz):
          self.unit_cell_index_list.append((i,j,k))
    return(self.unit_cell_index_list)

  def createRectangularArraySymmetrical(self, Nx, Ny, Nz):
    self.unit_cell_index_list = []
    for i in range(-Nx+1, Nx):
      for j in range(-Ny+1, Ny):
        for k in range(-Nz+1, Nz):
          self.unit_cell_index_list.append((i,j,k))
    return(self.unit_cell_index_list)

  def fillBox(self, location, size):
    location = numpy.array(location)
    size = numpy.array(size)
    e1, e2, e3 = self.getLatticeVectors()
    sx = e1[0]
    sy = e2[1]
    sz = e3[2]
    L = location - 0.5*size
    U = location + 0.5*size
    
    i_min = int(numpy.floor(L[0]/sx))
    i_max = int(numpy.ceil(U[0]/sx))
    
    j_min = int(numpy.floor(L[1]/sy))
    j_max = int(numpy.ceil(U[1]/sy))
    
    k_min = int(numpy.floor(L[2]/sz))
    k_max = int(numpy.ceil(U[2]/sz))

    # print('i: [{}, {}]'.format(i_min, i_max))
    # print('j: [{}, {}]'.format(j_min, j_max))
    # print('k: [{}, {}]'.format(k_min, k_max))
    
    self.unit_cell_index_list = []
    for i in range(i_min, i_max+1):
      for j in range(j_min, j_max+1):
        for k in range(k_min, k_max+1):
          self.unit_cell_index_list.append((i,j,k))

    self.createGeoList()

    box = Block()
    box.setLocation(location)
    box.setSize(size)

    # the pythonic way to do things:
    self.geo_list = filter(lambda cyl: cyl.AABB_intersects(box), self.geo_list)
    
    return(self.unit_cell_index_list)
  
  def write_entry(self, FILE):
    for obj in self.getGeoList():
      obj.write_entry(FILE)
      
  def getIndexOf(self, i, j, k, tetra_location, tetra_cylinder):
    idx = [i.name for i in self.getGeoList()].index('cell.{}.{}.{}.{}.cyl{}'.format(i, j, k, tetra_location, tetra_cylinder))
    return(idx)

  def clearGeoList(self):
    # TODO: Check if we need to do a proper clear, i.e. delete all elements (might be problem if it's a copy, due to breaking original)
    self.geo_list = None
    return

  def getGeoList(self):
    if self.geo_list is None:
      self.createGeoList()
    return(self.geo_list)

  def getMeshObject(self, Nx, Ny, Nz):
    # quick and dirty meshing...
    (u,v,w) = self.getLatticeVectors()
    
    RCD_size_x = (2*Nx-1+1/2)*norm(u)
    RCD_size_y = (2*Ny-1+2/6)*norm(v)
    RCD_size_z = (2*Nz-1)*norm(w)

    RCD_min_x = -(Nx-1+1/2)*norm(u)
    RCD_min_y = -(Ny-1+1/2+1/6)*norm(v)
    RCD_min_z = -(Nz-1)*norm(w) - self.__offset2__[2]*self.cubic_unit_cell_size

    RCD_delta_x = ((2*Nx-1)*2+1)*[norm(u)/2]
    RCD_delta_y = ((2*Ny-1)*6+2)*[norm(v)/6]
    RCD_delta_z = (2*Nz-1)*3*[norm(w)/8, norm(w)/8, norm(w)/12]

    RCD_mesh = MeshObject()
    RCD_mesh.setXmeshDelta(RCD_delta_x)
    RCD_mesh.setYmeshDelta(RCD_delta_y)
    RCD_mesh.setZmeshDelta(RCD_delta_z)
    return(RCD_mesh)
  
  def createBlenderObject(self, blender_operator, context):
    # Creates a unit-cell of the crystal in blender and returns the created object
    
    # import necessary packages
    import bpy
    import numpy
    
    from blender_scripts.modules.GeometryObjects import add_cylinder, add_tetra, add_block
    from blender_scripts.modules.blender_utilities import selectObjects, joinObjects
    
    # get cursor location for placement
    cursor_location3 = numpy.array(bpy.context.scene.cursor.location)
    
    self.setLocation(cursor_location3)
    
    geo_list = self.getGeoList()
    
    cyl_blender_list = []
    for cyl_BFDTD in geo_list:
      cyl_blender = cyl_BFDTD.createBlenderObject(blender_operator, context)
      cyl_blender_list.append(cyl_blender)
    
    #obj = add_cylinder(self, [0,0,0], [1,1,1], name='Cylinder', cylinder_radius=0.1)
    obj = joinObjects(cyl_blender_list, origin=cursor_location3, name='RCD111', context=context)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    
    return(obj)

class FRD_HexagonalLattice(RCD_HexagonalLattice):
  def __init__(self):
    super().__init__()
    self.RCD_on = True
    self.refractive_index_RCD = 1
    self.FRD_on = True
    self.refractive_index_FRD = 1
  
  def unitCellType1(self, i, j, k):
    '''
    A unit-cell containing 3 "tetrahedrons".
    lattice vectors: u1,v1,w1
    '''
    geo_list = []
    unit_cell_location = i*self.__u1__ + j*self.__v1__ + k*self.__w1__
    
    # TODO: Check why +sqrt(3)/4 and not -sqrt(3)/4 (Actually works with both. cf FRD symmetries.)
    FRD_offset = array([0, 0, -sqrt(3)/4])
    
    # RCD part
    if self.RCD_on:
      self.setRefractiveIndex(self.refractive_index_RCD)
      geo_list.extend(self.tetra(self.location + (unit_cell_location - self.__offset1__ + self.__R0__)*self.cubic_unit_cell_size, 'cell.{}.{}.{}.R0'.format(i,j,k)))
      geo_list.extend(self.tetra(self.location + (unit_cell_location - self.__offset1__ + self.__G0__)*self.cubic_unit_cell_size, 'cell.{}.{}.{}.G0'.format(i,j,k)))
      geo_list.extend(self.tetra(self.location + (unit_cell_location - self.__offset1__ + self.__B0__)*self.cubic_unit_cell_size, 'cell.{}.{}.{}.B0'.format(i,j,k)))
      
    # FRD part
    if self.FRD_on:
      self.setRefractiveIndex(self.refractive_index_FRD)
      geo_list.extend(self.tetra(self.location + (FRD_offset + unit_cell_location - self.__offset2__ + self.__R1__)*self.cubic_unit_cell_size, 'cell.{}.{}.{}.R1.FRD'.format(i,j,k)))
      geo_list.extend(self.tetra(self.location + (FRD_offset + unit_cell_location - self.__offset2__ + self.__G1__)*self.cubic_unit_cell_size, 'cell.{}.{}.{}.G1.FRD'.format(i,j,k)))
      geo_list.extend(self.tetra(self.location + (FRD_offset + unit_cell_location - self.__offset2__ + self.__B1__)*self.cubic_unit_cell_size, 'cell.{}.{}.{}.B1.FRD'.format(i,j,k)))

    return(geo_list)
  
  def unitCellType2(self, i, j, k):
    '''
    A unit-cell containing 6 "tetrahedrons".
    lattice vectors: u2,v2,w2
    '''
    
    geo_list = []
    unit_cell_location = i*self.__u2__ + j*self.__v2__ + k*self.__w2__

    # TODO: Check why +sqrt(3)/4 and not -sqrt(3)/4 (Actually works with both. cf FRD symmetries.)
    FRD_offset = array([0, 0, -sqrt(3)/4])

    # RCD part
    if self.RCD_on:
      self.setRefractiveIndex(self.refractive_index_RCD)
      geo_list.extend(self.tetra(self.location + (unit_cell_location - self.__offset2__ + self.__R1__)*self.cubic_unit_cell_size, 'cell.{}.{}.{}.R1'.format(i,j,k)))
      geo_list.extend(self.tetra(self.location + (unit_cell_location - self.__offset2__ + self.__G1__)*self.cubic_unit_cell_size, 'cell.{}.{}.{}.G1'.format(i,j,k)))
      geo_list.extend(self.tetra(self.location + (unit_cell_location - self.__offset2__ + self.__B1__)*self.cubic_unit_cell_size, 'cell.{}.{}.{}.B1'.format(i,j,k)))

      geo_list.extend(self.tetra(self.location + (unit_cell_location - self.__offset2__ + self.__R2__)*self.cubic_unit_cell_size, 'cell.{}.{}.{}.R2'.format(i,j,k)))
      geo_list.extend(self.tetra(self.location + (unit_cell_location - self.__offset2__ + self.__G2__)*self.cubic_unit_cell_size, 'cell.{}.{}.{}.G2'.format(i,j,k)))
      geo_list.extend(self.tetra(self.location + (unit_cell_location - self.__offset2__ + self.__B2__)*self.cubic_unit_cell_size, 'cell.{}.{}.{}.B2'.format(i,j,k)))

    # FRD part
    if self.FRD_on:
      self.setRefractiveIndex(self.refractive_index_FRD)
      geo_list.extend(self.tetra(self.location + (FRD_offset + unit_cell_location - self.__offset2__ + self.__R1__)*self.cubic_unit_cell_size, 'cell.{}.{}.{}.R1.FRD'.format(i,j,k)))
      geo_list.extend(self.tetra(self.location + (FRD_offset + unit_cell_location - self.__offset2__ + self.__G1__)*self.cubic_unit_cell_size, 'cell.{}.{}.{}.G1.FRD'.format(i,j,k)))
      geo_list.extend(self.tetra(self.location + (FRD_offset + unit_cell_location - self.__offset2__ + self.__B1__)*self.cubic_unit_cell_size, 'cell.{}.{}.{}.B1.FRD'.format(i,j,k)))

      geo_list.extend(self.tetra(self.location + (FRD_offset + unit_cell_location - self.__offset2__ + self.__R2__)*self.cubic_unit_cell_size, 'cell.{}.{}.{}.R2.FRD'.format(i,j,k)))
      geo_list.extend(self.tetra(self.location + (FRD_offset + unit_cell_location - self.__offset2__ + self.__G2__)*self.cubic_unit_cell_size, 'cell.{}.{}.{}.G2.FRD'.format(i,j,k)))
      geo_list.extend(self.tetra(self.location + (FRD_offset + unit_cell_location - self.__offset2__ + self.__B2__)*self.cubic_unit_cell_size, 'cell.{}.{}.{}.B2.FRD'.format(i,j,k)))

    return(geo_list)

def RCD_vector_dictionary():
  V = dict()
  V_groups = dict()
  
  # conventional basis
  V['x'] = numpy.array([1,0,0])
  V['y'] = numpy.array([0,1,0])
  V['z'] = numpy.array([0,0,1])
  V_groups['Conventional basis'] = ('x', 'y', 'z')
  # RCD111 basis
  V['x-RCD111'] = (1/numpy.sqrt(2))*numpy.array([1,0,-1])
  V['y-RCD111'] = (1/numpy.sqrt(6))*numpy.array([-1,2,-1])
  V['z-RCD111'] = (1/numpy.sqrt(3))*numpy.array([1,1,1])
  V_groups['RCD111 basis'] = ('x-RCD111', 'y-RCD111', 'z-RCD111')
  
  # RCD111 vectors
  RCD111 = RCD_HexagonalLattice()
  
  # The tetrahedron centres
  V['R0'] = RCD111.__R0__
  V['R1'] = RCD111.__R1__
  V['R2'] = RCD111.__R2__
  
  V['G0'] = RCD111.__G0__
  V['G1'] = RCD111.__G1__
  V['G2'] = RCD111.__G2__
  
  V['B0'] = RCD111.__B0__
  V['B1'] = RCD111.__B1__
  V['B2'] = RCD111.__B2__
  V_groups['RCD111-tetrahedron-centres'] = ('R0','R1','R2', 'G0','G1','G2', 'B0', 'B1', 'B2')
  
  # cell type 1 parameters
  V['offset1'] = RCD111.__offset1__
  V['u1'] = RCD111.__u1__
  V['v1'] = RCD111.__v1__
  V['w1'] = RCD111.__w1__
  V_groups['RCD111-type1-parameters'] = ('offset1', 'u1', 'v1', 'w1')
  
  # cell type 2 parameters
  V['offset2'] = RCD111.__offset2__
  V['u2'] = RCD111.__u2__
  V['v2'] = RCD111.__v2__
  V['w2'] = RCD111.__w2__
  V_groups['RCD111-type2-parameters'] = ('offset2', 'u2', 'v2', 'w2')
  
  #V['Conventional basis'] = ('x', 'y', 'z')
  #V['RCD111 basis'] = ('x-RCD111', 'y-RCD111', 'z-RCD111')
  
  # transformation matrices
  M_RCD111_to_conventional = numpy.array([V['x-RCD111'], V['y-RCD111'], V['z-RCD111']]).transpose()
  M_conventional_to_RCD111 = numpy.linalg.inv(M_RCD111_to_conventional)
  
  (FCC_BZ_V, FCC_BZ_V_groups) = FCC_BZ_dictionary(scale=1)
  #V = {**V, **FCC_BZ_V}
  #V_groups = {**V_groups, **FCC_BZ_V_groups}
  
  (output_V, output_V_groups) = apply_transform(FCC_BZ_V, FCC_BZ_V_groups, M_conventional_to_RCD111, 0.5*2/3, '-RCD111-1')
  V = {**V, **output_V}
  V_groups = {**V_groups, **output_V_groups}
  
  (output_V, output_V_groups) = apply_transform(FCC_BZ_V, FCC_BZ_V_groups, M_conventional_to_RCD111, 2/3, '-RCD111-2')
  V = {**V, **output_V}
  V_groups = {**V_groups, **output_V_groups}
  
  #print('-----------')
  #print(M_RCD111_to_conventional.dot(numpy.array([1,0,0])))
  #print(V['x-RCD111'])
  #print('-----------')
  #print(M_RCD111_to_conventional.dot(numpy.array([0,1,0])))
  #print(V['y-RCD111'])
  #print('-----------')
  #print(M_RCD111_to_conventional.dot(numpy.array([0,0,1])))
  #print(V['z-RCD111'])
  #print('-----------')
  #print(M_conventional_to_RCD111.dot(V['x-RCD111']))
  #print(M_conventional_to_RCD111.dot(V['y-RCD111']))
  #print(M_conventional_to_RCD111.dot(V['z-RCD111']))
  #print('-----------')
  
  ## add suffix, rotate and scale
  #suffix = '-RCD111'
  #for idx, key in enumerate(FCC_BZ_V):
    #new_key = key + suffix
    #new_vector = M_conventional_to_RCD111.dot(FCC_BZ_V[key])
    #V[new_key] = new_vector
  
  #for idx, key in enumerate(FCC_BZ_V_groups):
    #old_list = FCC_BZ_V_groups[key]
    #new_list = []
    #for i in old_list:
      #new_list.append(i + suffix)
    #V_groups[key+suffix] = new_list
    
  return (V , V_groups)

def FCC_BZ_dictionary(scale=1):
  # .. todo:: Use BrillouinZoneFCT() from BZ addon (or otherwise reduce code duplication)
  V = dict()
  V_groups = dict()
  
  V['a1'] = 0.5*numpy.array([0,1,1])
  V['a2'] = 0.5*numpy.array([1,0,1])
  V['a3'] = 0.5*numpy.array([1,1,0])
  V_groups['a'] = ('a1', 'a2', 'a3')
  
  V['b1'] = numpy.array([-1,1,1])
  V['b2'] = numpy.array([1,-1,1])
  V['b3'] = numpy.array([1,1,-1])
  V_groups['b'] = ('b1', 'b2', 'b3')
  
  V['Gamma'] = numpy.array([0,0,0])
  
  V_groups['X'] = []
  for i in range(2):
    k = 'X'+['-x','+x'][i]; V[k] = numpy.array([[-1,1][i], 0, 0]); V_groups['X'].append(k)
    k = 'X'+['-y','+y'][i]; V[k] = numpy.array([0, [-1,1][i], 0]); V_groups['X'].append(k)
    k = 'X'+['-z','+z'][i]; V[k] = numpy.array([0, 0, [-1,1][i]]); V_groups['X'].append(k)
    
  V_groups['K'] = []
  for i in range(2):
    for j in range(2):
      k = 'K' + ['-x','+x'][i] + ['-y','+y'][j]
      V[k] = (3/4)*numpy.array([[-1,1][i], [-1,1][j], 0])
      V_groups['K'].append(k)
      
      k = 'K' + ['-y','+y'][i] + ['-z','+z'][j]
      V[k] = (3/4)*numpy.array([0, [-1,1][i], [-1,1][j]])
      V_groups['K'].append(k)
      
      k = 'K' + ['-x','+x'][i] + ['-z','+z'][j]
      V[k] = (3/4)*numpy.array([[-1,1][i], 0, [-1,1][j]])
      V_groups['K'].append(k)
  
  V_groups['L'] = []
  for i in range(2):
    for j in range(2):
      for k in range(2):
        key = 'L' + ['-x','+x'][i] + ['-y','+y'][j] + ['-z','+z'][k]
        V[key] = (1/2)*numpy.array([[-1,1][i], [-1,1][j], [-1,1][k]])
        V_groups['L'].append(key)
  
  # add prefix and scale
  prefix = 'FCC-BZ-'
  key_list = list(V.keys())
  for k in key_list:
    V[prefix+k] = scale*V.pop(k)
  key_list = list(V_groups.keys())
  for k in key_list:
    group_old = V_groups.pop(k)
    group_new = []
    for idx, val in enumerate(group_old):
      group_new.append(prefix + val)
    V_groups[prefix+k] = group_new
    
    #V_groups[prefix+k] = V_groups.pop(k)
    #for idx, val in enumerate(V_groups[prefix+k]):
      #V_groups[prefix+k][idx] = prefix + V_groups[prefix+k][idx]
  
  return (V , V_groups)

def apply_transform(input_V, input_V_groups, mat3, scale, suffix):
  # add suffix, rotate and scale
  # .. todo:: V, V_groups could become a new class/object?
  # .. todo:: add_suffix/add_prefix functions?
  # .. todo:: have rotation/scaling as option in the add_arrow addon? use blender's add object helper's feature to align with axis?
  output_V = dict()
  output_V_groups = dict()
  for idx, key in enumerate(input_V):
    new_key = key + suffix
    new_vector = scale*mat3.dot(input_V[key])
    output_V[new_key] = new_vector
  
  for idx, key in enumerate(input_V_groups):
    old_list = input_V_groups[key]
    new_list = []
    for i in old_list:
      new_list.append(i + suffix)
    output_V_groups[key+suffix] = new_list
  return (output_V, output_V_groups)

def RCD111_waveguide_vector_dictionary():
  # .. todo:: agree on single set of conventions + document it (+ add lyx doc to SIP repo?)
  
  V = dict()
  V_groups = dict()
  (V_RCD, V_groups_RCD) = RCD_vector_dictionary()
  
  # for i in V_groups_RCD['FCC-BZ-K-RCD111-1']:
    # print(i)
  
  V['b1'] = V_RCD['FCC-BZ-K-x-y-RCD111-1']
  V['b2'] = V_RCD['FCC-BZ-K-y-z-RCD111-1']
  V['b3'] = V_RCD['FCC-BZ-K-x-z-RCD111-1']
  
  V['m1'] = V_RCD['FCC-BZ-K-x+y-RCD111-2']
  V['m2'] = V_RCD['FCC-BZ-K-y+z-RCD111-2']
  V['m3'] = V_RCD['FCC-BZ-K-x+z-RCD111-2']
  V['m4'] = V_RCD['FCC-BZ-K+x-y-RCD111-2']
  V['m5'] = V_RCD['FCC-BZ-K+y-z-RCD111-2']
  V['m6'] = V_RCD['FCC-BZ-K+x-z-RCD111-2']
  
  V['t1'] = V_RCD['FCC-BZ-K+x+y-RCD111-1']
  V['t2'] = V_RCD['FCC-BZ-K+y+z-RCD111-1']
  V['t3'] = V_RCD['FCC-BZ-K+x+z-RCD111-1']
  
  V_groups['t'] = ('t1','t2','t3')
  V_groups['b'] = ('b1','b2','b3')
  V_groups['m'] = ('m1','m2','m3','m4','m5','m6')
  
  # the 6 out of plane directions
  V['rcd111-up-1'] = 0.5*numpy.array([0,-1/numpy.sqrt(6),1/numpy.sqrt(3)])
  V['rcd111-up-2'] = 0.5*numpy.array([-numpy.sqrt(2)/4, 1/(2*numpy.sqrt(6)), 1/numpy.sqrt(3)])
  V['rcd111-up-3'] = 0.5*numpy.array([numpy.sqrt(2)/4, 1/numpy.sqrt(24), 1/numpy.sqrt(3)])
  
  V_groups['rcd111-up'] = ('rcd111-up-1','rcd111-up-2','rcd111-up-3')
  
  V['rcd111-down-1'] = -V['rcd111-up-1']
  V['rcd111-down-2'] = -V['rcd111-up-2']
  V['rcd111-down-3'] = -V['rcd111-up-3']
  
  V_groups['rcd111-down'] = ('rcd111-down-1','rcd111-down-2','rcd111-down-3')
  
  V['rcd111-hex-1'] = numpy.array([sqrt(2)/2, 0, 0])
  V['rcd111-hex-2'] = numpy.array([sqrt(2)/4, sqrt(6)/4, 0])
  V['rcd111-hex-3'] = numpy.array([-sqrt(2)/4, sqrt(6)/4, 0])
  V['rcd111-hex-4'] = numpy.array([-sqrt(2)/2, 0, 0])
  V['rcd111-hex-5'] = numpy.array([-sqrt(2)/4, -sqrt(6)/4, 0])
  V['rcd111-hex-6'] = numpy.array([sqrt(2)/4, -sqrt(6)/4, 0])
  
  V_groups['rcd111-hex'] = ('rcd111-hex-1', 'rcd111-hex-2', 'rcd111-hex-3', 'rcd111-hex-4', 'rcd111-hex-5', 'rcd111-hex-6')
  
  # .. todo:: move into a more appropriate place... + add RCD111 transform basis
  V['cartesian-x'] = numpy.array([1, 0, 0])
  V['cartesian-y'] = numpy.array([0, 1, 0])
  V['cartesian-z'] = numpy.array([0, 0, 1])
  V_groups['cartesian'] = ('cartesian-x', 'cartesian-y', 'cartesian-z')
  
  return (V, V_groups)
