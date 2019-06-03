#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import copy
import tempfile
from numpy import array, sqrt

from .BFDTDobject import BFDTDobject
from .GeometryObjects import GeometryObject, Cylinder, Distorted, Parallelepiped, Sphere
from .RCD import RCD_HexagonalLattice

class RCD_HexagonalLattice_ChiralWaveguide(RCD_HexagonalLattice):
  def __init__(self):
    super().__init__()
    self._chirality = 'right'

  @property
  def chirality(self):
    """ chirality of the waveguide: right or left """
    return self._chirality

  @chirality.setter
  def chirality(self, value):
    if not isinstance(value, str) or value.lower() not in ['right','left']:
      raise AttributeError("chirality has to be 'right' or 'left'")
    self._chirality = value
    
  def unitCell(self, i, j, k):
    '''
    A unit-cell containing 6 "tetrahedrons".
    lattice vectors: u2,v2,w2
    '''
    geo_list = []
    unit_cell_location = i*self.__u2__ + j*self.__v2__ + k*self.__w2__

    tetraR1 = self.tetra(self.location + (unit_cell_location - self.__offset2__ + self.__R1__)*self.cubic_unit_cell_size, 'cell.{}.{}.{}.R1'.format(i,j,k))
    tetraG1 = self.tetra(self.location + (unit_cell_location - self.__offset2__ + self.__G1__)*self.cubic_unit_cell_size, 'cell.{}.{}.{}.G1'.format(i,j,k))
    tetraB1 = self.tetra(self.location + (unit_cell_location - self.__offset2__ + self.__B1__)*self.cubic_unit_cell_size, 'cell.{}.{}.{}.B1'.format(i,j,k))

    tetraR2 = self.tetra(self.location + (unit_cell_location - self.__offset2__ + self.__R2__)*self.cubic_unit_cell_size, 'cell.{}.{}.{}.R2'.format(i,j,k))
    tetraG2 = self.tetra(self.location + (unit_cell_location - self.__offset2__ + self.__G2__)*self.cubic_unit_cell_size, 'cell.{}.{}.{}.G2'.format(i,j,k))
    tetraB2 = self.tetra(self.location + (unit_cell_location - self.__offset2__ + self.__B2__)*self.cubic_unit_cell_size, 'cell.{}.{}.{}.B2'.format(i,j,k))

    if self.chirality == 'left':
      if self.use_cylinders:
        geo_list.extend([tetraR2[0], tetraR2[3]])
        geo_list.extend([tetraG2[0], tetraG2[2]])
        geo_list.extend([tetraB1[0], tetraB1[1]])
      if self.use_spheres:
        # I feel dirty...
        if self.use_cylinders:
          geo_list.extend([tetraR2[0+4], tetraR2[3+4]])
          geo_list.extend([tetraG2[0+4], tetraG2[2+4]])
          geo_list.extend([tetraB1[0+4], tetraB1[1+4]])
        else:
          geo_list.extend([tetraR2[0], tetraR2[3]])
          geo_list.extend([tetraG2[0], tetraG2[2]])
          geo_list.extend([tetraB1[0], tetraB1[1]])
      if self.add_bottom_sphere:
        geo_list.extend([tetraR2[-1]])
        
    else:
      if self.use_cylinders:
        geo_list.extend([tetraR2[0], tetraR2[3]])
        geo_list.extend([tetraG2[0], tetraG2[1]])
        geo_list.extend([tetraB2[0], tetraB2[2]])
      if self.use_spheres:
        # so dirty...
        if self.use_cylinders:
          geo_list.extend([tetraR2[0+4], tetraR2[3+4]])
          geo_list.extend([tetraG2[0+4], tetraG2[1+4]])
          geo_list.extend([tetraB2[0+4], tetraB2[2+4]])
        else:
          geo_list.extend([tetraR2[0], tetraR2[3]])
          geo_list.extend([tetraG2[0], tetraG2[1]])
          geo_list.extend([tetraB2[0], tetraB2[2]])
      if self.add_bottom_sphere:
        geo_list.extend([tetraR2[-1]])

    return(geo_list)
    
  def createGeoList(self):
    if self.unit_cell_index_list is None:
      self.createRectangularArray(1,1,1)
    self.geo_list = []
    for (i,j,k) in self.unit_cell_index_list:
        self.geo_list.extend(self.unitCell(i,j,k))
    return(self.geo_list)

def main():
  sim = BFDTDobject()
  sim.setVerbosity(2)
  waveguide = RCD_HexagonalLattice_ChiralWaveguide()
  waveguide.chirality = 'left'
  waveguide.createRectangularArraySymmetrical(1,1,5)
  waveguide.setRefractiveIndex(1)

  waveguide.use_spheres = True
  waveguide.use_cylinders = True
  waveguide.add_bottom_sphere = False
  waveguide.relative_sphere_radius = 1
  waveguide.relative_sphere_index = 1

  sim.appendGeometryObject(waveguide)
  sim.writeGeoFile(tempfile.gettempdir() + os.sep + 'RCD_HexagonalLattice_ChiralWaveguide_left.geo')

  sim = BFDTDobject()
  sim.setVerbosity(2)
  waveguide = RCD_HexagonalLattice_ChiralWaveguide()
  waveguide.chirality = 'right'
  waveguide.createRectangularArraySymmetrical(1,1,5)
  waveguide.setRefractiveIndex(10)
  
  waveguide.setLocation([5,0,0])

  waveguide.use_spheres = True
  waveguide.use_cylinders = True
  waveguide.add_bottom_sphere = False
  waveguide.relative_sphere_radius = 2
  waveguide.relative_sphere_index = 2

  sim.appendGeometryObject(waveguide)
  sim.writeGeoFile(tempfile.gettempdir() + os.sep + 'RCD_HexagonalLattice_ChiralWaveguide_right.geo')

  return 0

if __name__ == '__main__':
  main()
