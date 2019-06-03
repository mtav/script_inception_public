#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import division

from .BFDTDobject import BFDTDobject
from .GeometryObjects import GeometryObject, Sphere, Block, Distorted, Parallelepiped, Cylinder, Rotation, MeshBox
from utilities.common import fixLowerUpper

class TriangularPrism(GeometryObject):
  '''Creates prism without 45 degree mirrors. Should be superseded by the current SpecialTriangularPrism completely at one point.'''
  def __init__(self,
    name = 'triangularprism',
    layer = 'triangularprism',
    group = 'triangularprism',
    lower = [0,0,0],
    upper = [1,1,1],
    permittivity = 1,# vacuum by default
    conductivity = 0,
    Nvoxels = 10,
    orientation = [0,1,2]):
    
    GeometryObject.__init__(self)
    self.name = name
    self.layer = layer
    self.group = group
    self.lower = lower
    self.upper = upper
    self.permittivity = permittivity
    self.conductivity = conductivity
    self.Nvoxels = Nvoxels
    self.orientation = orientation
    self.COMMENT = 'triangularprism'
    
  def __str__(self):
    ret  = 'name = '+self.name+'\n'
    ret += 'lower = '+str(self.lower)+'\n'
    ret += 'upper = '+str(self.upper)+'\n'
    ret += 'permittivity = '+str(self.permittivity)+'\n'
    ret += 'conductivity = '+str(self.conductivity)+'\n'
    ret += 'Nvoxels = '+str(self.Nvoxels)+'\n'
    ret += 'orientation = '+str(self.orientation)+'\n'
    ret += Geometry_object.__str__(self)
    return ret
    
  #def read_entry(self,entry):
    #if entry.name:
      #self.name = entry.name
    #self.lower = float_array(entry.data[0:3])
    #self.upper = float_array(entry.data[3:6])
    #self.permittivity = float(entry.data[6])
    #self.conductivity = float(entry.data[7])
    
  def getVoxels(self):
    voxel_list = []
    # X = triangle size
    # Y = triangle peak
    # Z = prism length
    ####################################
    mini = [0,0,0]
    maxi = [0,0,0]
    mini[0] = self.lower[self.orientation.index(0)]
    mini[1] = self.lower[self.orientation.index(1)]
    mini[2] = self.lower[self.orientation.index(2)]
    maxi[0] = self.upper[self.orientation.index(0)]
    maxi[1] = self.upper[self.orientation.index(1)]
    maxi[2] = self.upper[self.orientation.index(2)]
    print(mini[0],maxi[0])
    print(mini[1],maxi[1])
    print(mini[2],maxi[2])
    D = maxi[1] - mini[1]
    R = 0.5*(maxi[0]-mini[0])
    N = self.Nvoxels
    print(D)
    voxel_radius_X = R/( 2.*self.Nvoxels + 1.)
    for i in range(self.Nvoxels):
      # bottom blocks
      L = [ mini[0]+2*R*(i)/(2*N+1), mini[1]+D*(0)/(N+1), mini[2]]
      U = [ mini[0]+2*R*(i + 1)/(2*N+1), mini[1]+D*(i + 1.)/(N+1.), maxi[2]]
      print(L, U, mini[0], R, i, 2*N+1, D, mini[1], i+1, N+1,(i + 1)/(N+1))
      LL = [ L[self.orientation[0]],L[self.orientation[1]],L[self.orientation[2]] ]
      UU = [ U[self.orientation[0]],U[self.orientation[1]],U[self.orientation[2]] ]
      b = Block()
      b.setName(self.COMMENT)
      b.setLowerAbsolute(LL)
      b.setUpperAbsolute(UU)
      b.setRelativePermittivity(self.permittivity)
      b.setRelativeConductivity(self.conductivity)
      voxel_list.append(b)
      # top blocks
      L = [ mini[0]+2*R*((2*N+1)-(i))/(2*N+1), mini[1]+D*(0)/(N+1), mini[2]]
      U = [ mini[0]+2*R*((2*N+1)-(i + 1))/(2*N+1), mini[1]+D*(i + 1)/(N+1), maxi[2]]
      LL = [ L[self.orientation[0]],L[self.orientation[1]],L[self.orientation[2]] ]
      UU = [ U[self.orientation[0]],U[self.orientation[1]],U[self.orientation[2]] ]
      b = Block()
      b.setName(self.COMMENT)
      b.setLowerAbsolute(LL)
      b.setUpperAbsolute(UU)
      b.setRelativePermittivity(self.permittivity)
      b.setRelativeConductivity(self.conductivity)
      voxel_list.append(b)
    ## middle block
    L = [ mini[0]+2*R*(N)/(2*N+1), mini[1]+D*(0)/(N+1), mini[2]]
    U = [ mini[0]+2*R*(N + 1)/(2*N+1), mini[1]+D*(N + 1)/(N+1), maxi[2]]
    LL = [ L[self.orientation[0]],L[self.orientation[1]],L[self.orientation[2]] ]
    UU = [ U[self.orientation[0]],U[self.orientation[1]],U[self.orientation[2]] ]
    b = Block()
    b.setName(self.COMMENT)
    b.setLowerAbsolute(LL)
    b.setUpperAbsolute(UU)
    b.setRelativePermittivity(self.permittivity)
    b.setRelativeConductivity(self.conductivity)
    voxel_list.append(b)
    ####################################
    return voxel_list
    
  def write_entry(self, FILE):
    voxels = self.getVoxels()
    for v in voxels:
      v.write_entry(FILE)
    
  def getCenter(self):
    C = [ 0.5*(self.lower[0]+self.upper[0]), 0.5*(self.lower[1]+self.upper[1]), 0.5*(self.lower[2]+self.upper[2]) ]
    #CC = [ C[self.orientation[i]] for i in [0,1,2] ]
    return(C)

if __name__ == "__main__":
  foo = TriangularPrism()
  foo.getVoxels()
  #foo.write_entry()
