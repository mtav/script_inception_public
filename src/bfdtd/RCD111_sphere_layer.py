#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from numpy import array, sqrt
from .RCD_FRD_111_hybrid import RCD_FRD_111_hybrid
#from .bfdtd_parser import BFDTDobject, Cylinder, Rotation, Probe, Sphere, Block, truncateGeoList
from .GeometryObjects import *
from .bfdtd_parser import *

class RCD111_sphere_layer(RCD_FRD_111_hybrid):
  def __init__(self, obj):
    super().__init__()
    self.__dict__ = obj.__dict__ # TODO: check if this is good/bad practice
    self.sphere_radius = 0.1
    self.sphere_index = 2
    return
  
  #def unitCellType2(self, i, j, k):
    #'''Really ugly hack, but it is possible! Yay for python!'''

    #geo_list = []
    #unit_cell_location = i*self.RCD.__u2__ + j*self.RCD.__v2__ + k*self.RCD.__w2__

    #s0 = Sphere()
    #s1 = Sphere()
    #s0.setOuterRadius(0.1)
    #s1.setOuterRadius(0.1)
    #s0.setLocation(self.RCD.location + (unit_cell_location - self.RCD.__offset2__ + self.RCD.__G1__)*self.RCD.cubic_unit_cell_size)
    #s1.setLocation(self.RCD.location + (unit_cell_location - self.RCD.__offset2__ + self.RCD.__G2__)*self.RCD.cubic_unit_cell_size)
    #geo_list.extend([s0,s1])

    #return(geo_list)

  def unitCellType2(self, i, j, k):
    '''
    A unit-cell containing 6 "tetrahedrons".
    lattice vectors: u2,v2,w2
    '''
    geo_list = []
    unit_cell_location = i*self.RCD.__u2__ + j*self.RCD.__v2__ + k*self.RCD.__w2__

    #geo_list.extend(self.tetra(self.RCD.location + (unit_cell_location - self.RCD.__offset2__ + self.RCD.__R1__)*self.RCD.cubic_unit_cell_size, 'cell.{}.{}.{}.R1'.format(i,j,k)))
    geo_list.extend(self.tetra(self.RCD.location + (unit_cell_location - self.RCD.__offset2__ + self.RCD.__G1__ - array([0,0,sqrt(3)/4/2]) )*self.RCD.cubic_unit_cell_size, 'cell.{}.{}.{}.G1'.format(i,j,k)))
    #geo_list.extend(self.tetra(self.RCD.location + (unit_cell_location - self.RCD.__offset2__ + self.RCD.__B1__)*self.RCD.cubic_unit_cell_size, 'cell.{}.{}.{}.B1'.format(i,j,k)))

    #geo_list.extend(self.tetra(self.RCD.location + (unit_cell_location - self.RCD.__offset2__ + self.RCD.__R2__)*self.RCD.cubic_unit_cell_size, 'cell.{}.{}.{}.R2'.format(i,j,k)))
    geo_list.extend(self.tetra(self.RCD.location + (unit_cell_location - self.RCD.__offset2__ + self.RCD.__G2__ - array([0,0,sqrt(3)/4/2]) )*self.RCD.cubic_unit_cell_size, 'cell.{}.{}.{}.G2'.format(i,j,k)))
    #geo_list.extend(self.tetra(self.RCD.location + (unit_cell_location - self.RCD.__offset2__ + self.RCD.__B2__)*self.RCD.cubic_unit_cell_size, 'cell.{}.{}.{}.B2'.format(i,j,k)))

    return(geo_list)
    
  def tetra(self, loc, name):
    s0 = Sphere()
    s0.setOuterRadius(self.sphere_radius)
    s0.setLocation(loc)
    s0.setName(name)
    s0.setRefractiveIndex(self.sphere_index)
    return([s0])

  def build(self):
    self.sim.clearGeometry()
    self.RCD.unitCellType2 = self.unitCellType2
    #self.RCD.getGeoList = self.unitCellType2
    self.RCD.clearGeoList()
    self.RCD.setLocation(self.sim.box.getCentro())
    self.RCD.createRectangularArraySymmetrical(self.Nx, self.Ny, 1)

    xmin = self.buffer_x
    ymin = self.buffer_y
    zmin = self.buffer_z
    xmax = self.buffer_x + self.dim_x
    ymax = self.buffer_y + self.dim_y
    zmax = self.buffer_z + self.dim_z

    # get list of objects
    geo_list = self.RCD.getGeoList()
    geo_list = truncateGeoList(geo_list, xmin, xmax, ymin, ymax, zmin, zmax)
    print((xmin, xmax, ymin, ymax, zmin, zmax))
    self.sim.appendGeometryObject(geo_list)
    #geo_list = truncateGeoList(geo_list, xmin, xmax, ymin, ymax, zmin, zmax)
    #print((xmin, xmax, ymin, ymax, zmin, zmax))
    #geo_list = truncateGeoList(geo_list, xmin, xmax, ymin, ymax, zmin, zmax)

    #self.sim.appendGeometryObject(geo_list)

    return
  
  def write(self):
    # TODO: we could also just clear all geo objects, add new ones and then write, keeping all other sim settings intact...

    fileList = ['RCD111.inp', 'RCD111.geo', 'defect_layer.geo', 'box.geo']
    if not self.skip_Ex_writing:
      self.sim.writeGeoFile(os.path.join(self.outdir,'Ex','RCD111.geo'), withGeom=True, withBox=False)
      self.sim.writeGeoFile(os.path.join(self.outdir,'Ex','box.geo'), withGeom=False, withBox=True)
      self.sim.writeFileList(os.path.join(self.outdir,'Ex','RCD111.in'), fileList)

    if not self.skip_Ey_writing:
      self.sim.writeGeoFile(os.path.join(self.outdir,'Ey','RCD111.geo'), withGeom=True, withBox=False)
      self.sim.writeGeoFile(os.path.join(self.outdir,'Ey','box.geo'), withGeom=False, withBox=True)
      self.sim.writeFileList(os.path.join(self.outdir,'Ey','RCD111.in'), fileList)

    if not self.skip_Ez_writing:
      self.sim.writeGeoFile(os.path.join(self.outdir,'Ez','RCD111.geo'), withGeom=True, withBox=False)
      self.sim.writeGeoFile(os.path.join(self.outdir,'Ez','box.geo'), withGeom=False, withBox=True)
      self.sim.writeFileList(os.path.join(self.outdir,'Ez','RCD111.in'), fileList)
    
    self.build()
    
    if not self.skip_Ex_writing:
      self.sim.writeGeoFile(os.path.join(self.outdir,'Ex','defect_layer.geo'), withGeom=True, withBox=False)

    if not self.skip_Ey_writing:
      self.sim.writeGeoFile(os.path.join(self.outdir,'Ey','defect_layer.geo'), withGeom=True, withBox=False)

    if not self.skip_Ez_writing:
      self.sim.writeGeoFile(os.path.join(self.outdir,'Ez','defect_layer.geo'), withGeom=True, withBox=False)
    pass

if __name__ == '__main__':
	pass
