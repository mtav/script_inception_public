#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import tempfile

import bfdtd
import bfdtd.RCD

def test1():
  sim = bfdtd.BFDTDobject()
  RCD = bfdtd.RCD.RCD_HexagonalLattice()
  sim.appendGeometryObject(RCD)
  
  N = 1
  
  RCD.setLocation(RCD.__offset1__)
  RCD.createRectangularArray(N,N,N)
  RCD.setUnitCellType(1)
  RCD.createGeoList()
  sim.writeGeoFile(tempfile.gettempdir() + os.sep + 'RCD_rect_{}x{}x{}_type{}.geo'.format(N,N,N,RCD.getUnitCellType()))

  RCD.setLocation(RCD.__offset2__)
  RCD.createRectangularArray(N,N,N)
  RCD.setUnitCellType(2)
  RCD.createGeoList()
  sim.writeGeoFile(tempfile.gettempdir() + os.sep + 'RCD_rect_{}x{}x{}_type{}.geo'.format(N,N,N,RCD.getUnitCellType()))

  RCD.setLocation(RCD.__offset1__)
  RCD.createRectangularArraySymmetrical(N,N,N)
  RCD.setUnitCellType(1)
  RCD.createGeoList()
  sim.writeGeoFile(tempfile.gettempdir() + os.sep + 'RCD_sym_{}x{}x{}_type{}.geo'.format(N,N,N,RCD.getUnitCellType()))

  RCD.setLocation(RCD.__offset2__)
  RCD.createRectangularArraySymmetrical(N,N,N)
  RCD.setUnitCellType(2)
  RCD.createGeoList()
  sim.writeGeoFile(tempfile.gettempdir() + os.sep + 'RCD_sym_{}x{}x{}_type{}.geo'.format(N,N,N,RCD.getUnitCellType()))

def test2():
  sim = bfdtd.BFDTDobject()
  sim.setVerbosity(2)
  RCD = bfdtd.RCD.RCD_HexagonalLattice()
  sim.appendGeometryObject(RCD)
  sim.appendGeometryObject(RCD.getUnitCell())
  sim.appendGeometryObject(RCD.getCubicUnitCell())
  sim.writeGeoFile(tempfile.gettempdir() + os.sep + 'RCD.geo')

def test3():
  sim = bfdtd.BFDTDobject()
  sim.setVerbosity(2)
  
  RCD = bfdtd.RCD.RCD_HexagonalLattice()
  sim.appendGeometryObject(RCD)
  
  RCD.setLocation([0,0,0])
  
  RCD.setUnitCellType(1)
  RCD.createGeoList()
  sim.writeGeoFile(tempfile.gettempdir() + os.sep + 'RCD_type{}.geo'.format(RCD.getUnitCellType()))

  RCD.setUnitCellType(2)
  RCD.createGeoList()
  sim.writeGeoFile(tempfile.gettempdir() + os.sep + 'RCD_type{}.geo'.format(RCD.getUnitCellType()))

  return

def test4():
  sim = bfdtd.BFDTDobject()
  sim.setVerbosity(2)
  obj = bfdtd.RCD.FRD_HexagonalLattice()
  obj.setUnitCellType(2)
  sim.appendGeometryObject(obj)

  obj.RCD_on = False
  obj.refractive_index_RCD = 1
  obj.FRD_on = True
  obj.refractive_index_FRD = 10

  obj.setOuterRadius(0.01)

  obj.use_spheres = True
  obj.use_cylinders = True
  obj.add_bottom_sphere = True
  obj.relative_sphere_radius = 2
  obj.relative_sphere_index = 2

  sim.writeGeoFile(tempfile.gettempdir() + os.sep + 'tmp.geo')
  return

def test5():
  sim = bfdtd.BFDTDobject()
  RCD = bfdtd.RCD.RCD_HexagonalLattice()
  RCD.setUnitCellType(2)
  sim.appendGeometryObject(RCD)

  RCD.setOuterRadius(0.1)
  RCD.setRefractiveIndex(2)
  RCD.createRectangularArraySymmetrical(1,1,1)
  sim.writeGeoFile(tempfile.gettempdir() + os.sep + 'RCD111_1x1x1.geo')

  RCD.clearGeoList()
  RCD.setOuterRadius(0.05)
  RCD.setRefractiveIndex(3)
  RCD.createRectangularArraySymmetrical(3,3,3)
  
  sim.writeGeoFile(tempfile.gettempdir() + os.sep + 'RCD111_3x3x3.geo')
  
  (u,v,w) = RCD.getLatticeVectors()
  U = bfdtd.Excitation()
  U.setExtension([0,0,0], u)
  V = bfdtd.Excitation()
  V.setExtension([0,0,0], v)
  W = bfdtd.Excitation()
  W.setExtension([0,0,0], w)
  
  sim.appendExcitation(U)
  sim.appendExcitation(V)
  sim.appendExcitation(W)
  
  sim.writeInpFile(tempfile.gettempdir() + os.sep + 'RCD111_E.inp')
  return

if __name__ == "__main__":
  test1()
  test2()
  test3()
  test4()
  test5()
