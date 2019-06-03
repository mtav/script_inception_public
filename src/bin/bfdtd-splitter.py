#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ..todo:: walltime for epsilon simulations should be shorter...
# ..todo:: deal with missing probes, snapshot frequencies, low number of iterations, etc...

import os
import re
import sys
import copy
import bfdtd
import numpy
import argparse
import tempfile
import subprocess
import utilities.harminv

'''
To create split jobs covering the whole box.

Splitting considerations:
  N <= 52: OK for all BFDTD versions
  26 snapshots: a-z, 1-26
  52 snapshots: a-az, 1-52
  N > 52: only for BFDTD >= 2008, else numbering is different
  99 snapshots: a-cu, 1-99
  N > 99 snapshots: time snapshots start using ":"

.. todo::

  -double mesh resolution runs
  -probes with step 1 (or based on period if it has a big effect on sim time)
  -function for in-place editing of sims (ex: update iteration number)
  -check/calibrate time/RAM requirements based on sim in order to adapt Niterations, repetitions, etc
  -what repetition values to use? min repetition value?
  -BFDTD: check what frequency snapshots do exactly and try to validate using probes/time snapshots. Does 05 include time data used by previous fsnaps 01,02,etc? Or is it a sliding window? -> cumulative according to Railton's mail
  -BFDTD "easy fix": better file numbering/naming
  -automatic split-writing when required, making this script almost obsolete

.. todo:: any nice way to convert absolute to relative paths? (for filelist writing using any kind of paths)
.. todo:: laptop blender update + SIP setup
.. todo:: importBFDTD --skip-spheres option (and/or object limit option)

.. todo:: handle probe absence...

.. note:: Usine à gaz! Kludge!
'''

def writeSplit(sim, dstdir, snapshot_list, Nparts, inFile_pre_list=None, inFile_post_list=None, verbosity=0, overwrite=False, call_makedirs=False, PPN=1):
  
  # create dirs if needed
  if call_makedirs:
    if not os.path.exists(dstdir):
      os.makedirs(dstdir)
  
  if overwrite:
    mode = 'w'
  else:
    mode = 'x'
  
  Ndigits = len(str(abs(Nparts-1)))
  
  chunk_list = numpy.array_split(snapshot_list, Nparts)
  for chunk_idx, chunk in enumerate(chunk_list):
    part_string = 'part_{:0{Ndigits}d}'.format(chunk_idx, Ndigits=Ndigits)
    workdir = os.path.join(dstdir, part_string)
    
    if not os.path.isdir(workdir):
      os.mkdir(workdir)
    
    part_base = '{}.{}'.format(sim.getFileBaseName(), part_string)
    part_in_file = os.path.join(workdir, '{}.in'.format(part_base))
    part_sh_file = os.path.join(workdir, '{}.sh'.format(part_base))
    part_inp_file = os.path.join(workdir, '{}.inp'.format(part_base))
    
    if verbosity > 0:
      print(part_string)
      print(part_base)
      print(part_in_file)
      print(part_sh_file)
      print(part_inp_file)
    
    # write .sh file
    bfdtd.GEOshellscript(part_sh_file, part_base, WALLTIME = sim.getWallTime(), overwrite=overwrite, PPN=PPN)
    
    # write .inp file
    with open(part_inp_file, mode) as fid:
      for s in chunk:
        s.write_entry(fid)
    
    # write .in file
    file_list = []
    
    if inFile_pre_list is not None:
      file_list.extend(inFile_pre_list)
    
    file_list.append(part_inp_file)
    
    if inFile_post_list is not None:
      file_list.extend(inFile_post_list)
    
    if verbosity > 0:
      print('file_list = {}'.format(file_list))
    
    sim.writeFileList(part_in_file, fileList=file_list, use_relpath=True, overwrite=overwrite)

  return

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile')
  parser.add_argument('-d', '--dstdir', default=tempfile.gettempdir())
  parser.add_argument('--basename', default=None)
  parser.add_argument('--Nsnaps-max', default=52, type=int, help='maximum number of snapshots per part (default=52)')
  parser.add_argument('--clearProbes', action='store_true')
  parser.add_argument('--no-clearAllSnapshots', action='store_true')
  
  parser.add_argument('--frequency', type=float, nargs='+', help='Define a list of frequencies on the command line.')
  parser.add_argument('--frequency-list-simple', type=open, help='Read frequencies from a frequency list file. Format: one frequency per line.')
  parser.add_argument('--frequency-list-selection-format', help='Read frequencies from a frequency list file. Format: selection output from plotProbe.')
  parser.add_argument('--no-frequency-from-infile', action='store_false', dest='frequency_from_infile', help='By default, a list of frequencies is extracted from the infile. Use this option to disable this.')
  
  parser.add_argument('--first', type=int, default=None)
  parser.add_argument('--repetition', type=int, default=None)
  parser.add_argument('--starting-sample', type=int, default=None)
  parser.add_argument('--no-autofix', action='store_true')
  parser.add_argument('--no-check', action='store_true')
  parser.add_argument('--plane', type=str, choices=['x', 'y', 'z'])
  parser.add_argument('--walltime', type=int, default=360, help='default walltime to use')
  parser.add_argument('--walltime-epsilon', type=int, default=12, help='walltime to use for epsilon runs')
  parser.add_argument('--iterations', type=float, default=None)
  parser.add_argument('-Nx', type=int, default=1, help='factor by which to increase the resolution in the X direction')
  parser.add_argument('-Ny', type=int, default=1, help='factor by which to increase the resolution in the Y direction')
  parser.add_argument('-Nz', type=int, default=1, help='factor by which to increase the resolution in the Z direction')
  parser.add_argument('-o', '--overwrite', action='store_true')
  parser.add_argument('-y', '--yes-to-all', action='store_true')
  parser.add_argument('-v', '--verbose', action="count", dest="verbosity", default=0, help='verbosity level')
  
  parser.add_argument('--PPN', type=int, default=1, help='PPN for torque jobs')
  
  parser.add_argument('--no-common-output', action='store_false', dest='createMainDir')
  parser.add_argument('--no-mesh-output', action='store_false', dest='createMeshDir')
  parser.add_argument('--no-probe-output', action='store_false', dest='createProbeDir')
  parser.add_argument('--no-epsilon-snapshot-output', action='store_false', dest='createEpsilonSnapshotDir')
  parser.add_argument('--no-frequency-snapshot-output', action='store_false', dest='createFrequencySnapshotDir')
  
  args = parser.parse_args()
  
  if args.verbosity > 0:
    print(args)
  
  ##### prepare simulation
  # read input
  sim = bfdtd.readBristolFDTD(args.infile, verbosity=args.verbosity)
  
  # increase resolution
  mesh = bfdtd.increaseResolution3D(sim.getMesh(), args.Nx, args.Ny, args.Nz)
  sim.setMesh(mesh)
  
  # choose slicing plane direction
  if args.plane:
    plane_letter = args.plane
  else:
    # shortest mesh direction
    (sim_size, resolution) = sim.getSizeAndResolution()
    plane_python_index = numpy.argmin(resolution)
    plane_letter = ['x','y','z'][plane_python_index]
  
  # choose snapshot frequencies
  frequency_list = []
  if args.frequency:
    frequency_list.extend(args.frequency)
  if args.frequency_from_infile:
    frequency_list.extend(sim.getSnapshotFrequencySet())
  if args.frequency_list_simple:
    for f in args.frequency_list_simple:
      frequency_list.append(float(f))
  if args.frequency_list_selection_format:
    frequency_list.extend(utilities.harminv.getFrequencies(args.frequency_list_selection_format))
  
  frequency_list = list(set(frequency_list))
  frequency_list.sort()
  #if args.frequency:
    #frequency = args.frequency
  #else:
    #frequency_set = sim.getSnapshotFrequencySet()
    #if len(frequency_set) != 1:
      #raise Exception('Invalid number of frequencies found: frequency_set = {}'.format(frequency_set))
    #frequency = frequency_set.pop()
    
  # default snapshot parameters
  first = args.first
  repetition = args.repetition
  starting_sample = args.starting_sample
  # define defaults based on existing snapshot
  if len(sim.getFrequencySnapshots()) > 0:
    fsnap = sim.getFrequencySnapshots()[0]
    if args.first is None:
      first = fsnap.getFirst()
    if args.repetition is None:
      repetition = fsnap.getRepetition()
    if args.starting_sample is None:
      starting_sample = fsnap.getStartingSample()
  
  # set walltime
  sim.setWallTime(args.walltime)
  
  # for sanity
  sim.getFlag().setIdString('_id_')
  
  # set basename
  if args.basename:
    sim.setFileBaseName(args.basename)
    
  # set number of iterations
  if args.iterations:
    sim.setIterations(args.iterations)
  
  # clear stuff if requested
  if not args.no_clearAllSnapshots:
    sim.clearAllSnapshots()
  if args.clearProbes:
    sim.clearProbes()
  
  ##### add ModeVolumeBoxFull
  
  # define ModeVolumeBoxFull
  MV = bfdtd.ModeVolumeBoxFull()
  MV.setPlaneLetter(plane_letter)
  MV.setFullExtensionOn()
  MV.setFrequencies(frequency_list)
  MV.setFirst(first)
  MV.setRepetition(repetition)
  MV.setStartingSample(starting_sample)
  
  # get snapshot list
  #epsilon_snapshot_list, frequency_snapshot_list = MV.getSplitSnapshots(sim.getMesh())
  
  # add them as a list (for split writing)
  #sim.appendSnapshot(epsilon_snapshot_list + frequency_snapshot_list)
  sim.appendSnapshot(MV)
  
  #print('-------------------')
  #print(sim.getSnapshots(split=False))
  #print(sim.getSnapshots(split=True))
  #print('-------------------')
  #print(sim.getFrequencySnapshots(split=False))
  #print(sim.getFrequencySnapshots(split=True))
  #print('-------------------')
  #print(sim.getEpsilonSnapshots(split=False))
  #print(sim.getEpsilonSnapshots(split=True))
  #print('-------------------')
  #raise
  
  ##### fix+check
  if args.no_autofix:
    sim.disableAutoFix()
  else:
    sim.fixSimulation()
  
  if args.no_check:
    sim.disableSafetyChecks()
  else:
    sim.checkSimulation(output_checks=False)

  ##### splitting parameters
  epsilon_snapshot_list = sim.getEpsilonSnapshots(split=True)
  Nsnaps_esnap = len(epsilon_snapshot_list)
  Nparts_esnap = int(numpy.ceil(Nsnaps_esnap / args.Nsnaps_max))
  
  frequency_snapshot_list = sim.getFrequencySnapshots(split=True)
  Nsnaps_fsnap = len(frequency_snapshot_list)
  Nparts_fsnap = int(numpy.ceil(Nsnaps_fsnap / args.Nsnaps_max))
  
  ##### define output directories and filenames
  
  # basename
  base = sim.getFileBaseName()
  probe_step = sim.getProbes()[0].getStep()
  
  # directories
  main_dir = args.dstdir
  mesh_dir = 'mesh-{}x{}x{}'.format(*resolution)
  probe_dir = 'probes-step-{}'.format(probe_step)
  esnap_dir = 'epsilon'
  
  # files
  main_dir_geo_file = os.path.join(main_dir, '{}.geo'.format(base))
  main_dir_flag_file = os.path.join(main_dir, '{}.flag.inp'.format(base))
  main_dir_boundaries_file = os.path.join(main_dir, '{}.boundaries.inp'.format(base))
  main_dir_excitations_file = os.path.join(main_dir, '{}.excitations.inp'.format(base))
  
  mesh_dir_mesh_file = os.path.join(main_dir, mesh_dir, '{}.mesh.inp'.format(base))

  probe_dir_base = '{}.probes'.format(base)
  probe_dir_inp_file = os.path.join(main_dir, mesh_dir, probe_dir, '{}.inp'.format(probe_dir_base))
  probe_dir_sh_file = os.path.join(main_dir, mesh_dir, probe_dir, '{}.sh'.format(probe_dir_base))
  probe_dir_in_file = os.path.join(main_dir, mesh_dir, probe_dir, '{}.in'.format(probe_dir_base))

  esnap_dir_flag_file = os.path.join(main_dir, mesh_dir, esnap_dir, '{}.flag.inp'.format(base))
  esnap_dir_epsilon_file = os.path.join(main_dir, mesh_dir, esnap_dir, '{}.epsilon.inp'.format(base))
  esnap_dir_in_file = os.path.join(main_dir, mesh_dir, esnap_dir, '{}.epsilon.in'.format(base))

  # full directory names
  esnap_dir_full = os.path.join(main_dir, mesh_dir, esnap_dir)

  #dir_list = [main_dir,
              #os.path.join(main_dir, mesh_dir),
              #os.path.join(main_dir, mesh_dir, probe_dir),
              #os.path.join(main_dir, mesh_dir, esnap_dir),
              #os.path.join(main_dir, mesh_dir, fsnap_dir)]

  ##### sim info
  if args.verbosity >= 0:
    print('-----------------------------------------------------------')
    print('main_dir = {}'.format(main_dir))
    print('plane_letter = {}'.format(MV.getPlaneLetter()))
    #print('frequency_list = {}'.format(MV.getFrequencies()))
    print('frequency_list = {}'.format(frequency_list))
    print('starting_sample = {}'.format(MV.getStartingSample()))
    print('first = {}'.format(MV.getFirst()))
    print('repetition = {}'.format(MV.getRepetition()))
    print('probe_step = {}'.format(probe_step))
    print('-----------------------------------------------------------')
    print('Nsnaps_max = {}'.format(args.Nsnaps_max))
    print('-----------------------------------------------------------')
    print('Nsnaps_esnap = {}'.format(Nsnaps_esnap))
    print('Nparts_esnap = {}'.format(Nparts_esnap))
    print('-----------------------------------------------------------')
    print('Nsnaps_fsnap = {}'.format(Nsnaps_fsnap))
    print('Nparts_fsnap = {}'.format(Nparts_fsnap))
    print('-----------------------------------------------------------')
    sim.printInfo()
    print('-----------------------------------------------------------')
    
  ##### summarize what will be created and ask for confirmation
  
  if not args.yes_to_all:
    ok = input('Proceed? (y/n): ')
    if ok != 'y':
      sys.exit(-1)
  
  ######################################################################
  ##### output files
  
  ################################
  ##### main_dir
  
  if args.createMainDir:
    # create .geo file
    sim.writeGeoFile(main_dir_geo_file, overwrite=args.overwrite, call_makedirs=True)
    
    # create flag .inp file
    sim.getFlag().writeToFile(main_dir_flag_file, overwrite=args.overwrite, call_makedirs=True)
    
    # create boundaries .inp file
    sim.getBoundaries().writeToFile(main_dir_boundaries_file, overwrite=args.overwrite, call_makedirs=True)
    
    # create excitation .inp file
    sim.writeExcitationsToFile(main_dir_excitations_file, overwrite=args.overwrite, call_makedirs=True)
  
  ################################
  ##### mesh_dir
  if args.createMeshDir:
    # create mesh .inp file
    sim.getMesh().writeToFile(mesh_dir_mesh_file, overwrite=args.overwrite, call_makedirs=True)
  
  ################################
  ##### probe_dir
  if args.createProbeDir:
    # create probe .inp file
    sim.writeProbesToFile(probe_dir_inp_file, overwrite=args.overwrite, call_makedirs=True)
    
    # create probe .in file
    sim.writeFileList(probe_dir_in_file, fileList=[main_dir_flag_file,
                                                    main_dir_boundaries_file,
                                                    main_dir_excitations_file,
                                                    probe_dir_inp_file,
                                                    mesh_dir_mesh_file,
                                                    main_dir_geo_file], use_relpath=True, overwrite=args.overwrite)
    
    # write .sh file
    bfdtd.GEOshellscript(probe_dir_sh_file, probe_dir_base, WALLTIME = sim.getWallTime(), overwrite=args.overwrite, PPN=args.PPN)
  
  ################################
  ##### esnap_dir
  
  if args.createEpsilonSnapshotDir:
    # set to epsilon walltime
    sim.setWallTime(args.walltime_epsilon)
    
    # create flag .inp file
    flag = copy.deepcopy(sim.getFlag())
    flag.setIterations(1)
    flag.writeToFile(esnap_dir_flag_file, overwrite=args.overwrite, call_makedirs=True)
    
    # create esnap .inp files
    inFile_pre_list =[esnap_dir_flag_file,
                      main_dir_boundaries_file,
                      main_dir_excitations_file]
    inFile_post_list = [mesh_dir_mesh_file, main_dir_geo_file]
    writeSplit(sim, esnap_dir_full, epsilon_snapshot_list, Nparts_esnap, inFile_pre_list=inFile_pre_list, inFile_post_list=inFile_post_list, overwrite=args.overwrite, call_makedirs=True, PPN=args.PPN)
    
    # set back to global walltime
    sim.setWallTime(args.walltime)
  
  ################################
  ##### fsnap_dir
  
  if args.createFrequencySnapshotDir:
    # create fsnap .inp files
    for frequency in frequency_list:
      print('frequency = {}'.format(frequency))
      fsnap_dir = 'freq-{}-start-{}-first-{}-repetition-{}'.format(frequency, MV.getStartingSample(), MV.getFirst(), MV.getRepetition())
      fsnap_dir_full = os.path.join(main_dir, mesh_dir, fsnap_dir)
      inFile_pre_list =[main_dir_flag_file,
                        main_dir_boundaries_file,
                        main_dir_excitations_file]
      inFile_post_list = [mesh_dir_mesh_file, main_dir_geo_file]
      for fsnap in frequency_snapshot_list:
        fsnap.setFrequencies(frequency)
      writeSplit(sim, fsnap_dir_full, frequency_snapshot_list, Nparts_fsnap, inFile_pre_list=inFile_pre_list, inFile_post_list=inFile_post_list, overwrite=args.overwrite, call_makedirs=True, PPN=args.PPN)
  
  return 0

if __name__ == '__main__':
  main()
