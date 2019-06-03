#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
import tempfile

import bfdtd

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
  U = Excitation()
  U.setExtension([0,0,0], u)
  V = Excitation()
  V.setExtension([0,0,0], v)
  W = Excitation()
  W.setExtension([0,0,0], w)
  
  sim.appendExcitation(U)
  sim.appendExcitation(V)
  sim.appendExcitation(W)
  
  sim.writeInpFile(tempfile.gettempdir() + os.sep + 'RCD111_E.inp')
  return

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('ctlfile', default='test.geo.ctl', nargs='?')
  parser.add_argument('geofile', default='test.geo', nargs='?')
  parser.add_argument('-v', '--verbose', action="count", dest="verbosity", default=0, help='verbosity level')
  args = parser.parse_args()
  
  if args.verbosity > 0:
    print(args)
  
  sim = bfdtd.BFDTDobject()
  sim.setSizeAndResolution([1,2,4],[10,10,10],True)
  
  c = sim.appendGeometryObject(bfdtd.Cylinder())
  c.setLocation([1/2, 2/2, 1])
  c.setOuterRadius(0.25)
  c.setAxis([1,1,1])
  c.setHeight(1)
  c.setRelativePermittivity(2)
  
  s = sim.appendGeometryObject(bfdtd.Sphere())
  s.setLocation([1/2, 2/2, 2])
  s.setOuterRadius(0.25)
  s.setRelativePermittivity(3)
  
  b = sim.appendGeometryObject(bfdtd.Block())
  b.setLocation([1/2, 2/2, 3])
  b.setSize([1/8, 1/4, 1/2])
  b.setRelativePermittivity(4)
  
  sim.writeCtlFile(args.ctlfile)
  sim.writeGeoFile(args.geofile)

  return 0

if __name__ == '__main__':
  main()
  #test5()
