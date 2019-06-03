#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import everything from the bfdtd_parser module
from bfdtd.bfdtd_parser import *

def main():

  # create a BFDTDobject instance, which will store everything related to the simulation
  sim = BFDTDobject()
  
  # set a size and resolution
  # Note: This will create a homogeneous mesh. For a custom mesh, please refer to some of the existing scripts. The meshing system is still changing a lot.)
  sim.setSizeAndResolution([10,10,10],[100,100,100])

  # create an object
  obj = Cylinder()

  # set some of its parameters
  obj.setLocation([1,2,3])
  obj.setStartEndPoints([-1,2,-5], [1,1,1])
  obj.setOuterRadius(0.5)

  # add the object to the simulation
  sim.appendGeometryObject(obj)
  
  # add an excitation to the simulation
  E = Excitation()
  sim.appendExcitation(E)

  # add a probe to the simulation
  P = Probe()
  P.setPosition([4,5,6])
  sim.appendProbe(P)

  # add a snapshot to the simulation
  F = FrequencySnapshot()
  F.setFrequencies([100])
  sim.appendSnapshot(F)

  # write out only a .geo file
  sim.writeGeoFile('foo.geo')

  # write out only a .inp file
  sim.writeInpFile('foo.inp')

  # write out only a .in file
  sim.writeFileList('foo.in')

  # write out all files necessary to submit the job using qsub (i.e. the *Torque* queueing system).
  sim.writeTorqueJobDirectory('somedir')

  # You can even run the simulation directly. Files will be written as necessary.
  sim.runSimulation()

  return 0

if __name__ == '__main__':
  main()
