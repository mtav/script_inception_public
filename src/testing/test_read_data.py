#!/usr/bin/env python3

import os
import sys
import random
import tempfile

from utilities.brisFDTD_ID_info import FREQUENCYSNAPSHOT_MAX, TIMESNAPSHOT_MAX, MODEFILTEREDPROBE_MAX

import bfdtd

#tmp = tempfile.mkdtemp()
tmp = '/tmp/test/'
print('simdir = {}'.format(tmp))

sim = bfdtd.BFDTDobject()

sim.setSizeAndResolution([3,3,3], [30,40,50])

b = bfdtd.Block()
b.setSize([1,1,1])
b.setLocation(sim.getCentro())
b.setRelativePermittivity(2)
sim.appendGeometryObject(b)

#t = sim.appendSnapshot(TimeSnapshot())
#t.setEpsilon(True)

#sim.appendSnapshot(TimeSnapshot())

for s in [bfdtd.EpsilonSnapshot, bfdtd.FrequencySnapshot]:
  ex = sim.appendSnapshot(s())
  ey = sim.appendSnapshot(s())
  ez = sim.appendSnapshot(s())

  ex.setFirst(0)
  ex.setRepetition(1)
  ey.setFirst(0)
  ey.setRepetition(1)
  ez.setFirst(0)
  ez.setRepetition(1)

  ex.setCentro(sim.getCentro())
  ex.setPlaneOrientationX()

  ey.setCentro(sim.getCentro())
  ey.setPlaneOrientationY()

  ez.setCentro(sim.getCentro())
  ez.setPlaneOrientationZ()

sim.setIterations(10)

sim.runSimulation(tmp)

sim.setDataPaths([tmp])
#sim.readDataEpsilon()
sim.readDataTimeSnapshots()
sim.readDataFrequencySnapshots()
sim.writeHDF5('/tmp/test.h5')

for i in sim.getOutputFileNames()[0]:
  print(i)

print('simdir = {}'.format(tmp))
