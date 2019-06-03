#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .BFDTDobject import BFDTDobject
from .GeometryObjects import GeometryObject, Sphere, Block, Distorted, Parallelepiped, Cylinder, Rotation, MeshBox

# TODO: construction of new geometry objects from other geometry objects... (automatic copying of size, position, permittivity, conductivity, etc)
class Ellipsoid(Block):
  def __init__(self, name=None, layer=None, group=None, block_direction=None, non_elliptical_directions=None):
    if name is None: name = 'ellipsoid'
    if layer is None: layer = 'ellipsoid'
    if group is None: group = 'ellipsoid'
    if block_direction is None: block_direction = 'x'
    if non_elliptical_directions is None: non_elliptical_directions = [False, True, False]
  
    Block.__init__(self)
    self.name = name
    self.layer = layer
    self.group = group
    self.block_direction = block_direction
    self.non_elliptical_directions = non_elliptical_directions
    
    # mesh used to discretize the ellipsoid into blocks
    self.mesh = MeshObject()
    self.mesh.setSizeAndResolution(self.getSize(),[11,11,11])
    
  def __str__(self):
    ret  = 'name = '+self.name+'\n'
    ret += 'lower = '+str(self.lower)+'\n'
    ret += 'upper = '+str(self.upper)+'\n'
    ret += 'permittivity = '+str(self.permittivity)+'\n'
    ret += 'conductivity = '+str(self.conductivity)+'\n'
    ret += Geometry_object.__str__(self)
    return ret

  def getMeshingParameters(self,xvec,yvec,zvec,epsx,epsy,epsz):
    voxels = self.getVoxels()
    for v in voxels:
      xvec,yvec,zvec,epsx,epsy,epsz = v.getMeshingParameters(xvec,yvec,zvec,epsx,epsy,epsz)
    
    #objx = numpy.sort([self.lower[0],self.upper[0]])
    #objy = numpy.sort([self.lower[1],self.upper[1]])
    #objz = numpy.sort([self.lower[2],self.upper[2]])
    #if block_direction=='x':
      #objx = numpy.array(self.lower) + self.mesh.getXmesh()
    #elif block_direction=='x':
      #objx = numpy.array(self.lower) + self.mesh.getXmesh()
    #elif block_direction=='x':
      #objx = numpy.array(self.lower) + self.mesh.getXmesh()
    #xvec = numpy.vstack([xvec,objx])
    #yvec = numpy.vstack([yvec,objy])
    #zvec = numpy.vstack([zvec,objz])

    #eps = self.permittivity
    #epsx = numpy.vstack([epsx,eps])
    #epsy = numpy.vstack([epsy,eps])
    #epsz = numpy.vstack([epsz,eps])

    return xvec,yvec,zvec,epsx,epsy,epsz

  def getVoxels(self):
    voxel_list = []

    C = self.getCentro()
    L = self.getLowerAbsolute()
    size = self.getSize()
    centre_x = self.mesh.getXmeshCentres()
    centre_y = self.mesh.getYmeshCentres()
    centre_z = self.mesh.getZmeshCentres()
    delta_x = self.mesh.getXmeshDelta()
    delta_y = self.mesh.getYmeshDelta()
    delta_z = self.mesh.getZmeshDelta()
    a = 0.5*size[0]
    b = 0.5*size[1]
    c = 0.5*size[2]
    
    if self.block_direction=='x' and self.non_elliptical_directions==[False, False, True]:
      for j in range(len(centre_y)):
        y = -b+centre_y[j]
        dimX = 2*a*numpy.sqrt(1-pow((y/b),2))
        block = Block()
        block.permittivity = self.permittivity
        block.conductivity = self.conductivity
        block.name = "%s.Zx.j%d" % (self.name,j)
        block.setLocation([C[0], L[1]+centre_y[j], C[2]])
        block.setSize([dimX, delta_y[j], size[2]])
        voxel_list.append(block)
    elif self.block_direction=='y' and self.non_elliptical_directions==[False, False, True]:
      for i in range(len(centre_x)):
        x = -a+centre_x[i]
        dimY = 2*b*numpy.sqrt(1-pow((x/a),2))
        block = Block()
        block.permittivity = self.permittivity
        block.conductivity = self.conductivity
        block.name = "%s.Zy.i%d" % (self.name,i)
        block.setLocation([L[0]+centre_x[i], C[1], C[2]])
        block.setSize([delta_x[i], dimY, size[2]])
        voxel_list.append(block)
    elif self.block_direction=='x' and self.non_elliptical_directions==[False, True, False]:
      for k in range(len(centre_z)):
        z = -c+centre_z[k]
        dimX = 2*a*numpy.sqrt(1-pow((z/c),2))
        block = Block()
        block.permittivity = self.permittivity
        block.conductivity = self.conductivity
        block.name = "%s.Yx.k%d" % (self.name,k)
        block.setLocation([C[0], C[1], L[2]+centre_z[k]])
        block.setSize([dimX, size[1], delta_z[k]])
        voxel_list.append(block)
    elif self.block_direction=='z' and self.non_elliptical_directions==[False, True, False]:
      for i in range(len(centre_x)):
        x = -a+centre_x[i]
        dimZ = 2*c*numpy.sqrt(1-pow((x/a),2))
        block = Block()
        block.permittivity = self.permittivity
        block.conductivity = self.conductivity
        block.name = "%s.Yz.i%d" % (self.name,i)
        block.setLocation([L[0]+centre_x[i], C[1], C[2]])
        block.setSize([delta_x[i], size[1], dimZ])
        voxel_list.append(block)
    elif self.block_direction=='y' and self.non_elliptical_directions==[True, False, False]:
      for k in range(len(centre_z)):
        z = -c+centre_z[k]
        dimY = 2*b*numpy.sqrt(1-pow((z/c),2))
        block = Block()
        block.permittivity = self.permittivity
        block.conductivity = self.conductivity
        block.name = "%s.Xy.k%d" % (self.name,k)
        block.setLocation([C[0],C[1],L[2]+centre_z[k]])
        block.setSize([size[0], dimY, delta_z[k]])
        voxel_list.append(block)
    elif self.block_direction=='z' and self.non_elliptical_directions==[True, False, False]:
      for j in range(len(centre_y)):
        y = -b+centre_y[j]
        dimZ = 2*c*numpy.sqrt(1-pow((y/b),2))
        block = Block()
        block.permittivity = self.permittivity
        block.conductivity = self.conductivity
        block.name = "%s.Xz.j%d" % (self.name,j)
        block.setLocation([C[0], L[1]+centre_y[j], C[2]])
        block.setSize([size[0], delta_y[j], dimZ])
        voxel_list.append(block)
    else:
      print('FATAL ERROR: not supported yet', file=sys.stderr)
      sys.exit(-1)
      
    return voxel_list

  def write_entry(self, FILE):
    '''writes the voxels to the file corresponding to the FILE handle'''
    voxels = self.getVoxels()
    for v in voxels:
      v.write_entry(FILE)

# for testing
def test0():
  sim = BFDTDobject()
  C = numpy.array([1,2,3])
  
  block = Block()
  block.setSize(C)
  block.setLocation(0.5*C)
  #sim.geometry_object_list.append(block)
  
  sim.box.setCentro(block.getCentro())
  sim.box.setSize(block.getSize())

  ellipsoid = Ellipsoid()
  ellipsoid.setRefractiveIndex(2.4)
  ellipsoid.setLocation(block.getCentro())
  ellipsoid.setSize(block.getSize())
  ellipsoid.mesh.setSizeAndResolution(ellipsoid.getSize(),[11,11,11])

  sim.geometry_object_list.append(ellipsoid)

  meshing_factor = 1/15

  ellipsoid.non_elliptical_directions = [True, False, False]

  ellipsoid.block_direction = 'y'
  name = 'ellipsoid.Xy'
  sim.writeGeoFile(name + '.geo')
  sim.autoMeshGeometry(meshing_factor)
  sim.writeInpFile(name + '.inp')

  ellipsoid.block_direction = 'z'
  name = 'ellipsoid.Xz'
  sim.writeGeoFile(name + '.geo')
  sim.autoMeshGeometry(meshing_factor)
  sim.writeInpFile(name + '.inp')

  ellipsoid.non_elliptical_directions = [False, True, False]

  ellipsoid.block_direction = 'z'
  name = 'ellipsoid.Yz'
  sim.writeGeoFile(name + '.geo')
  sim.autoMeshGeometry(meshing_factor)
  sim.writeInpFile(name + '.inp')

  ellipsoid.block_direction = 'x'
  name = 'ellipsoid.Yx'
  sim.writeGeoFile(name + '.geo')
  sim.autoMeshGeometry(meshing_factor)
  sim.writeInpFile(name + '.inp')

  ellipsoid.non_elliptical_directions = [False, False, True]

  ellipsoid.block_direction = 'x'
  name = 'ellipsoid.Zx'
  sim.writeGeoFile(name + '.geo')
  sim.autoMeshGeometry(meshing_factor)
  sim.writeInpFile(name + '.inp')

  ellipsoid.block_direction = 'y'
  name = 'ellipsoid.Zy'
  sim.writeGeoFile(name + '.geo')
  sim.autoMeshGeometry(meshing_factor)
  sim.writeInpFile(name + '.inp')
  
def test1():
  C = numpy.array([1,2,3])
  
  sim = BFDTDobject()
  sim.box.setExtension([0,0,0], C)
  
  ellipsoid = Ellipsoid()
  ellipsoid.setRefractiveIndex(2.4)
  ellipsoid.setLocation(sim.box.getCentro())
  ellipsoid.setSize(C)
  ellipsoid.mesh.setSizeAndResolution(ellipsoid.getSize(),[11,11,11])

  sim.geometry_object_list.append(ellipsoid)
  sim.autoMeshGeometry(10)
  
  sim.writeGeoFile('ellipsoid.geo')
  sim.writeInpFile('ellipsoid.inp')
  return
  
if __name__ == "__main__":
  test0()
  test1()
