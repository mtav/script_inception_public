#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import tempfile

import bfdtd
from utilities.harminv import getFrequencies
import geometries.DBR
from constants.physcon import get_c0

#def resonance_run(src, dst, freqListFile, fileBaseName=None, walltime=360):
def resonance_run(args):
  ''' Copy src to dst with added frequency snapshots from freqListFile '''
  src = os.path.abspath(args.src).rstrip(os.sep)
  dst = os.path.abspath(args.dst).rstrip(os.sep)
  if os.path.isdir(src):
    print(src +' is a directory')
    sim = bfdtd.readBristolFDTD(src+os.sep+os.path.basename(src)+'.in')
    if not args.fileBaseName:
      fileBaseName = os.path.basename(src)
  else:
    print(src +' is not a directory')
    sim = bfdtd.readBristolFDTD(src)
    if not args.fileBaseName:
      fileBaseName = os.path.splitext(os.path.basename(src))[0]
  
  freqs = getFrequencies(args.freqListFile)
  
  print('---')
  print('Frequencies:')
  for f in freqs:
    print(f)
  print('---')
  
  # get src snapshot lists
  (all_time_snapshots, time_snapshots, epsilon_snapshots, mode_filtered_probes) = sim.getAllTimeSnapshots()
  fsnap_list = sim.getFrequencySnapshots()
  
  new_snapshot_list = []
  
  if args.frequency_to_energy:
    for fsnap in fsnap_list:
      energy_snapshot = bfdtd.EnergySnapshot()
      energy_snapshot.setFromSnapshot(fsnap)
      energy_snapshot.setFrequencies(freqs)
      new_snapshot_list.append(energy_snapshot)
  
  if args.new_central:
    box = bfdtd.SnapshotBoxXYZ()
    exc = sim.getExcitations()[0]
    if args.intersection_at_P1:
      (P1, P2) = exc.getExtension()
      print('P1 = {}'.format(P1))
      box.setIntersectionPoint(P1)
    else:
      box.setIntersectionPoint(exc.getCentro())
    energy_snapshot = bfdtd.EnergySnapshot()
    energy_snapshot.setFrequencies(freqs)
    box.setBaseSnapshot(energy_snapshot)
    new_snapshot_list.append(box)
  
  print(new_snapshot_list)
  print(len(new_snapshot_list))
  
  if args.clearAllSnapshots:
    sim.clearAllSnapshots()
  if args.clearEpsilonSnapshots:
    sim.clearEpsilonSnapshots()
  if args.clearFrequencySnapshots:
    sim.clearFrequencySnapshots()
  if args.clearModeFilteredProbes:
    sim.clearModeFilteredProbes()
  if args.clearTimeSnapshots:
    sim.clearTimeSnapshots()
  if args.clearProbes:
    sim.clearProbes()
  if args.clearGeometry:
    sim.clearGeometry()
  
  if args.iterations:
    sim.setIterations(args.iterations)
  
  sim.appendSnapshot(new_snapshot_list)
  
  exc = sim.getExcitations()[0]
  if args.source_frequency_range:
    exc.setFrequencyRange(*args.source_frequency_range)
  elif args.source_wavelength_range:
    exc.setWavelengthRange(*args.source_wavelength_range)
  elif args.source_frequency_range_from_DBR:
    wavelength, nLow, nHigh = args.source_frequency_range_from_DBR
    obj = geometries.DBR.DBR(wavelength, nLow, nHigh)
    fmin, fmax = obj.getFrequencyRange()
    exc.setFrequencyRange(fmin, fmax)
  elif args.source_frequency_range_max:
    lambda0 = args.source_frequency_range_max
    f0 = get_c0()/lambda0
    delta_f = f0/4
    fmin = f0 - delta_f/2
    fmax = f0 + delta_f/2
    exc.setFrequencyRange(fmin, fmax)
  
  print('FrequencyRange = {}'.format(exc.getFrequencyRange()) )
  print('WavelengthRange = {}'.format(exc.getWavelengthRange()) )
  print('exc.getPeriod() = {}'.format(exc.getPeriod()) )
  print('exc.getTimeConstant() = {}'.format(exc.getTimeConstant()) )
  print('exc.getPeriod()/exc.getTimeConstant() = {}'.format(exc.getPeriod()/exc.getTimeConstant()))
  
  exc.setStartTime(0)
  
  sim.printInfo()
  
  sim.setFileBaseName(fileBaseName)
  sim.setWallTime(args.walltime)
  sim.setAutosetNFrequencySnapshots(10)
  
  if args.run_source:
    sim.setSizeAndResolution([1,1,1], [32,32,32])
    sim.getBoundaries().setBoundaryConditionsNormal()
    sim.clearAllSnapshots()
    sim.clearProbes()
    sim.clearGeometry()
    
    exc = sim.getExcitations()[0]
    exc.setLocation(sim.getCentro())
    exc.setSize([0,0,0])
    
    p = sim.appendProbe(bfdtd.Probe())
    p.setStep(1)
    p.setLocation(exc.getLocation())
    
    sim.setSimulationTime(sim.getExcitationEndTimeMax())
  
  sim.writeTorqueJobDirectory(dst)
  #sim.writeAll(dst, fileBaseName)
  #sim.writeShellScript(os.path.join(dst, fileBaseName+'.sh'))
  
  print(sim.getSnapshots())
  for s in sim.getSnapshots():
    print(s.getName())

def main(argv=None):
  '''
  Copy src to dst with added frequency snapshots from freqListFile
  '''
  parser = argparse.ArgumentParser()
  parser.add_argument('src')
  parser.add_argument('dst')
  parser.add_argument('freqListFile')
  parser.add_argument('-b', '--basename', dest='fileBaseName')
  parser.add_argument('-w', '--walltime', default=360, type=int)
  #group = parser.add_mutually_exclusive_group(required=True)
  parser.add_argument('--frequency-to-energy', action='store_true')
  parser.add_argument('--new-central', action='store_true')
  parser.add_argument('--intersection-at-P1', action='store_true')
  
  parser.add_argument('--iterations', type=float)
  
  parser.add_argument('--clearAllSnapshots', action='store_true')
  parser.add_argument('--clearEpsilonSnapshots', action='store_true')
  parser.add_argument('--clearFrequencySnapshots', action='store_true')
  parser.add_argument('--clearModeFilteredProbes', action='store_true')
  parser.add_argument('--clearTimeSnapshots', action='store_true')
  parser.add_argument('--clearProbes', action='store_true')
  parser.add_argument('--clearGeometry', action='store_true')
  
  excitation_range_group = parser.add_mutually_exclusive_group()
  excitation_range_group.add_argument('-lr', '--source-wavelength-range', type=float, nargs=2, metavar=('LAMBDA_MIN', 'LAMBDA_MAX'))
  excitation_range_group.add_argument('-fr', '--source-frequency-range', type=float, nargs=2, metavar=('FMIN', 'FMAX'))
  excitation_range_group.add_argument('--source-frequency-range-from-DBR', type=float, nargs=3, metavar=('wavelength', 'nLow', 'nHigh'))
  excitation_range_group.add_argument('--source-frequency-range-max', type=float, metavar=('wavelength'), help='sets delta_f = f0/4 = c0/(4*lambda0)')
  
  parser.add_argument('--run-source', action='store_true', help='create a special run to check the source properties')
  
  args = parser.parse_args()
  print(args)
  
  #resonance_run(args.src, args.dst, args.freqListFile, fileBaseName=args.basename, walltime=args.walltime, args)
  resonance_run(args)
  
if __name__ == "__main__":
  sys.exit(main())
