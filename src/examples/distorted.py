#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bfdtd.bfdtd_parser import *
from constants.physcon import *

if __name__ == '__main__':

  sim = BFDTDobject()

  disX = Distorted(name='disX')
  disX.setRefractiveIndex(1.5)
  disX.vertices[3] = disX.vertices[3] + numpy.array([0,1,2])
  disX.vertices[2] = disX.vertices[2] + numpy.array([0,1,2])
  disX.translate([1,2,2])

  disY = Distorted(name='disY')
  disY.setRefractiveIndex(1.5)
  disY.vertices[3] = disY.vertices[3] + numpy.array([2,0,1])
  disY.vertices[0] = disY.vertices[0] + numpy.array([2,0,1])
  disY.translate([2,1,2])

  disZ = Distorted(name='disZ')
  disZ.setRefractiveIndex(1.5)
  disZ.vertices[3] = disZ.vertices[3] + numpy.array([1,2,0])
  disZ.vertices[4] = disZ.vertices[4] + numpy.array([1,2,0])
  disZ.translate([2,2,1])

  sim.geometry_object_list=[disX,disY,disZ]

  sim.box.upper=[6,6,6]

  sim.addEpsilonSnapshot('x',1.5)
  sim.addEpsilonSnapshot('y',1.5)
  sim.addEpsilonSnapshot('z',1.5)

  sim.flag.iterations=1
  e=Excitation()
  e.setExtension([1,1,1],[2,1,1])
  sim.excitation_list.append(e)
  sim.autoMeshGeometry(0.1)
  sim.writeAll('distorted_test')
