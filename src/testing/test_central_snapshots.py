#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
import tempfile

import bfdtd

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('DSTDIR', default=tempfile.gettempdir(), nargs='?')
  args = parser.parse_args()
  print(args)
  
  DSTDIR = args.DSTDIR
  if not os.path.isdir(DSTDIR):
    os.mkdir(DSTDIR)
    
  sim = bfdtd.BFDTDobject()
  sim.setSizeAndResolution([2, 3, 4], [20, 20, 20], True)
  
  sphere = bfdtd.Sphere()
  sphere.setLocation(sim.getCentro())
  sphere.setOuterRadius(0.5)
  sphere.setRelativePermittivity(2)

  sim.setGeometryObjects([sphere])
  
  e = bfdtd.EpsilonSnapshot()
  
  s = bfdtd.SnapshotBoxXYZ()
  s.setBaseSnapshot(e)
  s.setExtension(*sim.getExtension())
  s.setIntersectionPoint(sim.getCentro())
  
  sim.setSnapshots(s)
  sim.writeTorqueJobDirectory(DSTDIR)
  
  sim.runSimulation(DSTDIR)
  
  return 0

if __name__ == '__main__':
  main()
