#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# .. todo:: Convert to unit tests.

import os
import argparse
import tempfile
import numpy

import bfdtd

def test0():
  parser = argparse.ArgumentParser()
  parser.add_argument('DSTDIR', default=tempfile.gettempdir(), nargs='?')
  parser.add_argument('-v', '--verbose', action="count", dest="verbosity", default=0, help='verbosity level')
  parser.add_argument('-r', '--run', action="store_true")
  args = parser.parse_args()
  print(args)
  
  sim = bfdtd.BFDTDobject()
  sim.setVerbosity(args.verbosity)
  sim.setSizeAndResolution([1,2,3],[32,32,32], True)
  
  E = bfdtd.Excitation()
  E.setTimeConstant(1e-8)
  E.setPeriod(E.getTimeConstant()/10)
  E.setStartTime(0)
  E.setLocation(sim.getCentro())
  E.setEx()
  #E.setSize([2*1/32,0,0])
  sim.appendExcitation(E)
  
  print(E)
  
  p = bfdtd.Probe()
  p.setStep(1)
  p.setLocation(E.getLocation())
  sim.appendProbe(p)
  
  n = 5
  bsize = [0.5, 2*0.5, 3*0.5] # E.getLambda()/(2*n)
  
  b = bfdtd.Block()
  b.setLocation(sim.getCentro())
  b.setRefractiveIndex(n)
  b.setSize(bsize)
  sim.appendGeometryObject(b)
  
  energy_snapshot = bfdtd.EnergySnapshot()
  energy_snapshot.setFrequencies(E.getFrequency())
  
  f = bfdtd.SnapshotBoxXYZ()
  f.setBaseSnapshot(energy_snapshot)
  f.setIntersectionPoint(sim.getCentro())
  sim.appendSnapshot(f)
  
  #sim.appendSnapshot(bfdtd.EpsilonSnapshot())
  
  sim.setSimulationTime(2*E.getEndTime())
  sim.setAutosetNFrequencySnapshots(10)
  
  if args.run:
    sim.runSimulation(args.DSTDIR)
  
  print('------------')
  E.printInfo()
  print('------------')
  sim.printInfo()
  print('------------')

# default 
#------------
#self.getStartTime() = 0.0
#self.getPeakTime() = 2e-08
#self.getEndTime() = 4e-08
#self.getPeriod() = 3.3356409519815204e-09
#------------
#self.getNcells() = 32768
#self.getIterations() = 739
#self.getSimulationTime() = 4.002723944839243e-08
#self.getTimeStep() = 5.416405879349449e-11 -> mus
#------------

  
  return 0


def test_setFrequencyRange():
  E = bfdtd.Excitation()
  fmin = 157414649.10606748
  fmax = 202390263.1363725
  E.setFrequencyRange(fmin, fmax)
  fmin = 157414649
  fmax = 202390263.1363725
  E.setFrequencyRange(fmin, fmax, autofix=True)
  fmin = 157414649.10606748
  fmax = 202390263.2
  E.setFrequencyRange(fmin, fmax, autofix=True)
  for i in range(-9,10):
    f0 = 1.23456789*(10**i)
    print('{:.3e}'.format(f0))
    E.setFrequencyRange(7/8*f0, 9/8*f0)
  for i in range(-9,10):
    f0 = 1.23456789*(10**i)
    print('{:.3e}'.format(f0))
    E.setFrequencyRange(7/8*f0, 9.1/8*f0, autofix=True)
  for i in range(-9,10):
    f0 = 1.23456789*(10**i)
    print('{:.3e}'.format(f0))
    E.setFrequencyRange(6.9/8*f0, 9/8*f0, autofix=True)
  return
  
def test_checkPeriodvsTimeConstant():
  print('=== test_checkPeriodvsTimeConstant ===')
  E = bfdtd.Excitation()
  E.setTimeConstant(1-1e-9)
  E.setPeriod(1)
  E.checkPeriodvsTimeConstant(raise_exception=True)
  E.setTimeConstant(1)
  E.setPeriod(1)
  E.checkPeriodvsTimeConstant(raise_exception=True)
  E.setTimeConstant(1+1e-9)
  E.setPeriod(1)
  E.checkPeriodvsTimeConstant(raise_exception=True)
  E.setTimeConstant(1-2e-9)
  E.setPeriod(1)
  E.checkPeriodvsTimeConstant(raise_exception=True)
  return

if __name__ == '__main__':
  test0()
  test_setFrequencyRange()
  test_checkPeriodvsTimeConstant()
