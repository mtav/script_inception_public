#!/usr/bin/env python3

import os
import sys
import random
import tempfile
from bfdtd.bfdtd_parser import *
from utilities.brisFDTD_ID_info import FREQUENCYSNAPSHOT_MAX, TIMESNAPSHOT_MAX, MODEFILTEREDPROBE_MAX

with tempfile.TemporaryDirectory() as tmp:
  print('simdir = {}'.format(tmp))
    
  sim = BFDTDobject()

  N = random.randint(1, min(FREQUENCYSNAPSHOT_MAX, TIMESNAPSHOT_MAX, MODEFILTEREDPROBE_MAX))

  for i in range(N):
    snapshot = random.choice([TimeSnapshot(), EpsilonSnapshot(), ModeFilteredProbe(), FrequencySnapshot()])
    plane = random.choice(['x','y','z'])
    snapshot.setPlaneLetter(plane)
    sim.appendSnapshot(snapshot)

  #sim.setSnapshots(439*[ModeFilteredProbe()])
  sim.runSimulation(tmp)

  snaps, probes = sim.getOutputFileNames()
  for i in snaps:
    f = os.path.join(tmp, i)
    x = os.path.exists(f)
    print('{} : {}'.format(f, x))
    if not x:
      raise

  print('simdir = {}'.format(tmp))

with tempfile.TemporaryDirectory() as tmp:
  print('simdir = {}'.format(tmp))    
  sim = BFDTDobject()
  sim.setSnapshots(MODEFILTEREDPROBE_MAX*[ModeFilteredProbe()] + FREQUENCYSNAPSHOT_MAX*[FrequencySnapshot()])
  sim.runSimulation(tmp)
  snaps, probes = sim.getOutputFileNames()
  for i in snaps:
    f = os.path.join(tmp, i)
    x = os.path.exists(f)
    print('{} : {}'.format(f, x))
    if not x:
      raise
  print('simdir = {}'.format(tmp))

with tempfile.TemporaryDirectory() as tmp:
  print('simdir = {}'.format(tmp))    
  sim = BFDTDobject()
  sim.setSnapshots(TIMESNAPSHOT_MAX*[TimeSnapshot()] + FREQUENCYSNAPSHOT_MAX*[FrequencySnapshot()])
  sim.runSimulation(tmp)
  snaps, probes = sim.getOutputFileNames()
  for i in snaps:
    f = os.path.join(tmp, i)
    x = os.path.exists(f)
    print('{} : {}'.format(f, x))
    if not x:
      raise
  print('simdir = {}'.format(tmp))

with tempfile.TemporaryDirectory() as tmp:
  print('simdir = {}'.format(tmp))    
  sim = BFDTDobject()
  sim.setSnapshots(TIMESNAPSHOT_MAX*[EpsilonSnapshot()] + FREQUENCYSNAPSHOT_MAX*[FrequencySnapshot()])
  sim.runSimulation(tmp)
  snaps, probes = sim.getOutputFileNames()
  for i in snaps:
    f = os.path.join(tmp, i)
    x = os.path.exists(f)
    print('{} : {}'.format(f, x))
    if not x:
      raise
  print('simdir = {}'.format(tmp))
