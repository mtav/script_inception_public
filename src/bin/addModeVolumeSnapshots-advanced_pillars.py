#!/usr/bin/env python3

'''
Script to prepare mode volume runs based on a list of frequency-selection.txt files.

Given a file dir/E?/foo, it will look for the following files:

  * dir/Ex/frequency-selection.txt
  * dir/Ey/frequency-selection.txt
  * dir/Ez/frequency-selection.txt

And create the following sim dirs:

  * dir/epsilon
  * dir/Ex/MV-freq-(.*)-MHz-lambda-(.*)-mum
  * dir/Ey/MV-freq-(.*)-MHz-lambda-(.*)-mum
  * dir/Ez/MV-freq-(.*)-MHz-lambda-(.*)-mum

.. note:: If you don't have frequencies for some directions, just use dummy files with header only.

.. warning:: This script assumes that Ex, Ey, Ez have the same mesh and excitation centre position. (which is the case for our RCD111 simulations)

.. todo:: Clean up, make more user-friendly and clear and add to repo.
.. todo:: split mesh from input and use .in file more? requires standard sim method.
.. todo:: setFrequencies -> Unit? doc somewhere.
.. todo:: set/getFileBaseName() -> get rid of camel-case? Define standard...
.. todo:: Add indent to BFDTD entries
.. todo:: Add BFDTD groups (custom by user), scenes (per sim), layers (per type), etc
.. todo:: Set first, rep, etc to None by default, in which case automatic determination is done according to timestep and excitations
.. todo:: overwrite=false should offer yes/no dialog? (or easy way to build it around it with try/except)
.. todo:: overwrite could also check for output in the directory. If there isn't any, overwriting is less risky...
.. todo:: finally make a torque/job submission/management/progress checking GUI...
.. todo:: show queue info in prompt -> smarter prompt (zsh?)
.. todo:: show repo info in prompt -> smarter prompt (zsh?)
.. todo:: pythonify/argparsify superqsub/batch_qsub
.. todo:: argparsify/python3-fy qstat.py

.. todo:: make it work with relative paths like "./frequency-selection.txt" when run from local dir
.. todo:: proper argparse support
.. todo:: disable grep system call, or replace with python code, and/or make optional
.. todo:: .bat file run for windows???
.. todo:: Add option for basename...
'''

# Usual values:
FIRST = [65400, 12800]
REPETITION = [131050, 32000]
STARTING_SAMPLE = [6400, 12800]

MIN_TIME_OFFSET_TIME_CONSTANT_RATIO = 3 # = time_offset/time_constant
MIN_SAMPLINGTIME_MAXPERIOD_RATIO = 100 # repetition*dt/Tmax = repetition*dt*fmin
MIN_NFFT_POINTS_IN_EXCITATION_RANGE = 100 # = repetition*dt*(fmax-fmin)

import os
import numpy
from numpy import ceil, floor
from bfdtd.bfdtd_parser import readBristolFDTD
from bfdtd.snapshot import SnapshotBoxVolume, SnapshotBoxXYZ, FrequencySnapshot, EpsilonSnapshot
from utilities.harminv import getFrequencies
from constants.constants import get_c0
import subprocess
from utilities.common import findNearestInSortedArray, checkSnapshotNumber
import argparse
import sys
import tempfile

#maindir = '~/TEST/newMVboxTest/sample_dir/'
#destdir = '/tmp/MVrun/'

def process(maindir, destdir, overwrite, dry_run, disabled_epsilon=False, disabled_directions=[]):
  print('maindir = {}'.format(maindir))
  print('destdir = {}'.format(destdir))
  print('overwrite = {}'.format(overwrite))
  print('dry_run = {}'.format(dry_run))
  print('disabled_epsilon = {}'.format(disabled_epsilon))
  print('disabled_directions = {}'.format(disabled_directions))

  for direction in ['Ex','Ey','Ez']:

    if direction not in disabled_directions:
      # get the frequency list, to fail quickly in case of problems
      flist = os.path.join(maindir, direction, 'frequency-selection.txt')
      freq_MHz_list = getFrequencies(flist)

    # read in base file
    infile = os.path.join(maindir, direction, 'RCD111.in')
    sim = readBristolFDTD(infile, verbosity=0)
    sim.setFileBaseName('RCD111')
    # clean sim
    sim.clearProbes()
    sim.clearAllSnapshots()
    sim.clearFileList()

    # get excitation location
    excitation = sim.getExcitations()[0]
    excitation_location = excitation.getLocation()

    # get min/max param values
    dt = sim.getTimeStep()
    time_offset = max(excitation.getTimeOffset(), MIN_TIME_OFFSET_TIME_CONSTANT_RATIO*excitation.getTimeConstant())
    starting_sample_min = int(ceil( (time_offset + MIN_TIME_OFFSET_TIME_CONSTANT_RATIO*excitation.getTimeConstant())/dt ))
    #print(dt)
    #print(starting_sample_min)
    Npoints_per_period_min = int(floor( (1/excitation.getFrequencyMax())/dt ))
    #print(Npoints_per_period_min)
    repetition_min_1 = int(ceil( (MIN_SAMPLINGTIME_MAXPERIOD_RATIO/excitation.getFrequencyMin())/dt ))
    repetition_min_2 = int(ceil( (MIN_NFFT_POINTS_IN_EXCITATION_RANGE/(excitation.getFrequencyMax()-excitation.getFrequencyMin()))/dt ))
    #print(repetition_min_1)
    #print(repetition_min_2)

    first_min = starting_sample_min + max(repetition_min_1, repetition_min_2)
    #print(first_min)

    repetition = max([repetition_min_1, repetition_min_2] + REPETITION)
    starting_sample = max([starting_sample_min] + STARTING_SAMPLE)
    first = max([starting_sample + repetition] + FIRST)

    print('starting_sample = {}, first = {}, repetition = {}'.format(starting_sample, first, repetition))

    #print('starting_sample = {}'.format(starting_sample))
    #print('first = {}'.format(first))
    #print('repetition = {}'.format(repetition))

    # set up the volume box
    partial_box = SnapshotBoxVolume()

    # set up the XYZ box
    xyz_box = SnapshotBoxXYZ()
    xyz_box.setIntersectionPoint(excitation_location)

    # MV box size is chosen so that it will cover 1+2*47 = 95 mesh lines (we want Nsnaps<=99, but that includes 3 x/y/z snaps)
    xmesh = sim.getXmesh()
    (idx, val) = findNearestInSortedArray(xmesh, excitation_location[0], 0)
    MV_box_size = (xmesh[idx+47] + xmesh[idx+48])/2 - (xmesh[idx-47] + xmesh[idx-48])/2
    print('MV_box_size = {} = {}*sim.getSize()'.format(MV_box_size, MV_box_size/(sim.getSize()[0])))

    # set up base frequency snapshot (we need two at the moment because one has full extension and the other one does not)
    fsnap_base_partial = FrequencySnapshot()
    fsnap_base_partial.setCentro(excitation_location)
    #fsnap_base_partial.setSize([MV_box_size, MV_box_size, MV_box_size])
    fsnap_base_partial.setSize([MV_box_size, 2.0638028, 2.0638028])
    fsnap_base_partial.setPlaneOrientationX()
    fsnap_base_partial.setFullExtensionOff()
    fsnap_base_partial.setStartingSample(starting_sample)
    fsnap_base_partial.setFirst(first)
    fsnap_base_partial.setRepetition(repetition)

    fsnap_base_full = FrequencySnapshot()
    fsnap_base_full.setFromSnapshot(fsnap_base_partial)
    fsnap_base_full.setFullExtensionOn()
    #fsnap_base_full.setCentro(excitation_location)
    #fsnap_base_full.setSize(MV_box_size)
    #fsnap_base_full.setPlaneOrientationX()

    if direction == 'Ex':
      # create epsilon run
      outdir_epsilon = os.path.join(destdir, 'epsilon')
      print('outdir_epsilon = {}'.format(outdir_epsilon))

      # set up base epsilon snapshots
      esnap_base_partial = EpsilonSnapshot()
      esnap_base_partial.setFromSnapshot(fsnap_base_partial)

      esnap_base_full = EpsilonSnapshot()
      esnap_base_full.setFromSnapshot(fsnap_base_full)

      #esnap_base_partial.setCentro(excitation_location)
      #esnap_base_partial.setSize(sim.getSize()/2)
      #esnap_base_partial.setPlaneOrientationY()

      ## set up base frequency snapshot
      #fsnap_base = FrequencySnapshot()
      #fsnap_base.setFromSnapshot(esnap_base)

      # attach base snapshots to boxes
      partial_box.setBaseSnapshot(esnap_base_partial)
      xyz_box.setBaseSnapshot(esnap_base_full)
      # add the snapshots
      sim.setSnapshots([partial_box, xyz_box])

      # set up a short simulation
      sim.setIterations(1)
      sim.setWallTime(120)

      # write
      if not dry_run and not disabled_epsilon:
        sim.writeTorqueJobDirectory(outdir_epsilon, overwrite=overwrite)
        checkSnapshotNumber(os.path.join(outdir_epsilon, sim.getFileBaseName()+'.inp'), verbose=True)

    if direction not in disabled_directions:
      for freq_MHz in freq_MHz_list:
        print('freq_MHz = {}'.format(freq_MHz))
        wavelength_mum = get_c0()/freq_MHz
        outdir_MV = os.path.join(destdir, direction, 'MV-freq-{:.0f}-MHz-lambda-{:.6f}-mum'.format(freq_MHz, wavelength_mum))
        print('outdir_MV = {}'.format(outdir_MV))

        # set snapshot frequency
        fsnap_base_partial.setFrequencies([freq_MHz])
        fsnap_base_full.setFrequencies([freq_MHz])

        # attach base snapshots to boxes
        partial_box.setBaseSnapshot(fsnap_base_partial)
        xyz_box.setBaseSnapshot(fsnap_base_full)
        # add the snapshots
        sim.setSnapshots([partial_box, xyz_box])

        # set up a long simulation
        sim.setIterations(1e9)
        sim.setWallTime(120)

        # write
        if not dry_run:
          sim.writeTorqueJobDirectory(outdir_MV, overwrite=overwrite)
          checkSnapshotNumber(os.path.join(outdir_MV, sim.getFileBaseName()+'.inp'), verbose=True)

  return

  ## get the frequencies

  ## create BFDTDobject
  #sim=BFDTDobject()

  ## clean it

  ## add MV box

  ## add XYZ snapshots

  #MV=ModeVolumeBox()

  #foo=SnapshotBoxXYZ()
  #sim.appendSnapshot(foo)
  #sim.setSnapshots(foo)

  #foo.setIntersectionPoint(sim.getCentro())
  #XYZ=EnergySnapshot()
  #foo.setBaseSnapshot(XYZ)

  ## write out
  #sim.setFileBaseName()
  ##sim.writeAll('Ez.SnapshotBoxXYZ')
  #sim.writeTorqueJobDirectory()

  #return 0

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--disable-epsilon', action='store_true')
  parser.add_argument('--disable-Ex', action='store_true')
  parser.add_argument('--disable-Ey', action='store_true')
  parser.add_argument('--disable-Ez', action='store_true')
  parser.add_argument('--epsilon-only', action='store_true')
  parser.add_argument('--overwrite', action='store_true')
  parser.add_argument('-n', '--dry-run', action='store_true')
  #parser.add_argument('--srcdir')
  #parser.add_argument('--dstdir')
  parser.add_argument('infile', nargs='+')
  args = parser.parse_args()
  print(args)
  # find . -path "*/Ex/frequency-selection.txt"
  # find . -path "*/Ex/frequency-selection.txt" | xargs ~/TEST/newMVboxTest/addMV.py
  #overwrite = False
  #dry_run = False

  for infile in args.infile:
    print('=====> Processing {}'.format(infile))
    maindir = destdir = os.path.split(os.path.dirname(os.path.realpath(infile)))[0]

    #destdir = tempfile.mkdtemp()
    #print(destdir)

    disabled_directions = []
    if args.disable_Ex:
      disabled_directions.append('Ex')
    if args.disable_Ey:
      disabled_directions.append('Ey')
    if args.disable_Ez:
      disabled_directions.append('Ez')
    if args.epsilon_only:
      disabled_directions = ['Ex', 'Ey', 'Ez']

    process(maindir, destdir, args.overwrite, args.dry_run, args.disable_epsilon, disabled_directions)

  return

if __name__ == '__main__':
  main()
	#main(maindir, destdir)
	#main(maindir, destdir)
