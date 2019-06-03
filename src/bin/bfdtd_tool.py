#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
script to quickly get various info from bfdtd related files

.. todo:: Integrate some of those functions into the BFDTD class?
.. todo:: Add something to create epsilon snapshots from a geometry? based on existing mode volume frequency snapshots?
.. todo:: Figure out how to pass lists of float via @config files...
.. todo:: move from parser groups to subparsers
.. todo:: Use parent parsers for input, output, verbose, etc?
"""

### Useful for debugging:
#import code
#code.interact(local=locals())

#for k,v in arguments.__dict__.items():
  #print((k,v))
#return

import bfdtd.bfdtd_parser as bfdtd
from utilities.common import *
from utilities.brisFDTD_ID_info import *
import constants
import argparse
import sys
import re
import os
import warnings
import utilities.brisFDTD_ID_info as brisFDTD_ID_info
import tkinter.filedialog

import bfdtd

# .. todo:: PyQt5+argparseui disabled until set up again. Fix.
#from PyQt5 import QtWidgets
#import argparseui

from utilities.harminv import getFrequencies

def printNcells(arguments):
  sim_in = bfdtd.BFDTDobject()
  sim_in.verbosity = arguments.verbosity
  for infile in arguments.infile:
    sim_in.readBristolFDTD(infile)
  print(sim_in.getNcells())
  return

def printExcitation(arguments):
  sim_in = bfdtd.BFDTDobject()
  sim_in.verbosity = arguments.verbosity
  for infile in arguments.infile:
    sim_in.readBristolFDTD(infile)
  if arguments.id_list is None:
    arguments.id_list = range(len(sim_in.excitation_list))
  for i in arguments.id_list:
    print('=== excitation '+str(i)+' ===')
    print(sim_in.excitation_list[i])
  return

def printSnapshotFrequencyList(arguments):
  sim_in = bfdtd.BFDTDobject()
  sim_in.verbosity = arguments.verbosity
  for infile in arguments.infile:
    sim_in.readBristolFDTD(infile)
  print(sim_in.getSnapshotFrequencySet())
  return
  
def printAll(arguments):
  sim_in = bfdtd.BFDTDobject()
  sim_in.verbosity = arguments.verbosity
  for infile in arguments.infile:
    sim_in.readBristolFDTD(infile)
  print(sim_in)
  return

def printExcitationDirection(arguments):
  sim_in = bfdtd.BFDTDobject()
  sim_in.verbosity = arguments.verbosity
  for infile in arguments.infile:
    sim_in.readBristolFDTD(infile)
  if arguments.id_list is None:
    arguments.id_list = range(len(sim_in.excitation_list))
  for i in arguments.id_list:
    print('=== excitation '+str(i)+' ===')
    print(sim_in.excitation_list[i].E)
  return

def rotate(infile, outfile, axis_point, axis_direction, angle_degrees):
  sim = bfdtd.readBristolFDTD(infile)
  sim.rotate(axis_point, axis_direction, angle_degrees)
  sim.writeGeoFile(outfile)

def automeshWithMeshingFactor(infile, outfile, meshing_factor):
  sim = bfdtd.readBristolFDTD(infile)
  sim.autoMeshGeometry(meshing_factor)
  sim.writeInpFile(outfile)

# .. todo:: finish this in a nice usable way
def automeshWithMaxCells(infile, outfile, meshing_factor, MAXCELLS, Lambda, a):
  sim = bfdtd.readBristolFDTD(infile)
  sim.autoMeshGeometry(meshing_factor)
  sim.writeInpFile(outfile)

  sim = bfdtd.readBristolFDTD(infile)
  sim.autoMeshGeometry(Lambda/a)
  while(sim.getNcells()>MAXCELLS and a>1):
    a = a-1
    sim.autoMeshGeometry(Lambda/a)
  sim.writeInpFile(outfile)

def writeInpFile(arguments):
  FDTDobj = bfdtd.BFDTDobject()
  FDTDobj.verbosity = arguments.verbosity
  # read input
  if arguments.infile:
    for infile in arguments.infile:
      FDTDobj.readBristolFDTD(infile)
  # write output
  FDTDobj.writeInpFile(arguments.writeInpFile)
  return

def printFrequencySnapshotInfo(arguments):
  FDTDobj = bfdtd.readBristolFDTD(*arguments.infile, verbosity = arguments.BFDTDreader_verbosity)
  
  for idx, fsnap in enumerate(FDTDobj.getFrequencySnapshots()):
    print('idx+1={}, name={}, plane={}, f={}, centro={}, pos:{}={}'.format(idx+1,
                                                             fsnap.getName(),
                                                             fsnap.getPlaneLetter(),
                                                             fsnap.getFrequencies(),
                                                             fsnap.getCentro(),
                                                             fsnap.getPlaneLetter(),
                                                             fsnap.getCentro()[fsnap.getPlanePythonIndex()]))
  return

def printFormattedString(arguments):
  FDTDobj = bfdtd.readBristolFDTD(*arguments.infile, verbosity = arguments.BFDTDreader_verbosity)

  dt = FDTDobj.getTimeStep()
  iterations = FDTDobj.getIterations()
  total_time = FDTDobj.getSimulationTime()
  
  lmin=[]
  lcen=[]
  lmax=[]
  fmin=[]
  fcen=[]
  fmax=[]
  eloc=[]
  
  for E in FDTDobj.getExcitations():
    lmin.append(E.getWavelengthMin())
    lcen.append(E.getWavelength())
    lmax.append(E.getWavelengthMax())
    fmin.append(E.getFrequencyMin())
    fcen.append(E.getFrequency())
    fmax.append(E.getFrequencyMax())
    eloc.append(E.getLocation())

  print(arguments.FORMAT.format(dt = dt,
                                total_time = total_time,
                                iterations = iterations,
                                lmin = lmin,
                                lcen = lcen,
                                lmax = lmax,
                                fmin = fmin,
                                fcen = fcen,
                                fmax = fmax,
                                eloc = eloc
                                ))
  return

def fixSnapshots(infile, newbasename):
  '''
  -read infile
  -remove any time snapshots
  -set frequency snapshots to first=3200, repetition=32000
  -move snapshots 1 grid away from excitation.P1
  -write to ./fixedSnapshots/newbasename
  '''
  sim = bfdtd.readBristolFDTD(infile)
  sim.fileList = []
  sim.clearTimeSnapshots()
  for s in sim.snapshot_list:
    s.first = 3200
    s.repetition = 32000

  refP = sim.excitation_list[0].P1

  (idxX,valX)=findNearest(sim.mesh.getXmesh(),refP[0])
  (idxY,valY)=findNearest(sim.mesh.getYmesh(),refP[1])
  (idxZ,valZ)=findNearest(sim.mesh.getZmesh(),refP[2])

  sim.snapshot_list[0].P1[0]=sim.snapshot_list[0].P2[0]=sim.mesh.getXmesh()[idxX-1]
  sim.snapshot_list[1].P1[1]=sim.snapshot_list[1].P2[1]=sim.mesh.getYmesh()[idxY-1]
  sim.snapshot_list[2].P1[2]=sim.snapshot_list[2].P2[2]=sim.mesh.getZmesh()[idxZ-1]

  sim.writeAll('./fixedSnapshots',newbasename)

def addModeVolumeFrequencySnapshots(arguments):
  '''
  .. todo:: find nice generic+flexible system for this...
  '''
  
  FDTDobj = bfdtd.BFDTDobject()
  FDTDobj.verbosity = arguments.verbosity
  for infile in arguments.infile:
    FDTDobj.readBristolFDTD(infile)
  
  (size,res) = FDTDobj.mesh.getSizeAndResolution()
  
  if arguments.verbosity>0:
    print('res = ',res)

  if arguments.slicing_direction is None:
    # take the direction with the smallest number of snapshots to reduce number of generated .prn files
    S = ['X','Y','Z']
    arguments.slicing_direction = S[res.index(min(res))]
    
  frequency_vector = []
  if arguments.readFreqFromInput:
    #print('FUUUUUUUUUUUUUUUUUUUU')
    frequency_list = set()
    for freq_snap in FDTDobj.frequency_snapshot_list:
      for freq in freq_snap.frequency_vector:
        frequency_list.add(freq)
    print(frequency_list)
    frequency_vector.extend(frequency_list)
    print(frequency_vector)

    #sys.exit(-1)
  if arguments.freqListFile is not None:
    frequency_vector.extend(getFrequencies(arguments.freqListFile))
  if arguments.wavelength_mum is not None:
    frequency_vector.extend([get_c0()/i for i in arguments.wavelength_mum])
  if arguments.frequency_MHz is not None:
    frequency_vector.extend(arguments.frequency_MHz)
  
  if len(frequency_vector)<=0:
    print('ERROR: Great scot! You forgot to specify frequencies.', file=sys.stderr)
    sys.exit(-1)

  FDTDobj.flag.iterations = arguments.iterations
  
  NAME = 'ModeVolume'
  #print(arguments.slicing_direction)
  if arguments.slicing_direction == 'X':
    pos_list = FDTDobj.mesh.getXmesh()
    for pos in pos_list:
      e = FDTDobj.addEpsilonSnapshot('X',pos)
      e.name = NAME + '.eps'
      e.first = 1
      e.repetition = FDTDobj.flag.iterations + 1 # So that only one epsilon snapshot is created. We don't need more.
      f = FDTDobj.addFrequencySnapshot('X',pos)
      f.name = NAME + '.freq'
      f.first = arguments.first
      f.repetition = arguments.repetition
      f.starting_sample = arguments.starting_sample
      f.frequency_vector = frequency_vector
  elif arguments.slicing_direction == 'Y':
    pos_list = FDTDobj.mesh.getYmesh()
    for pos in pos_list:
      e = FDTDobj.addEpsilonSnapshot('Y',pos)
      e.name = NAME + '.eps'
      e.first = 1
      e.repetition = FDTDobj.flag.iterations + 1 # So that only one epsilon snapshot is created. We don't need more.
      f = FDTDobj.addFrequencySnapshot('Y',pos)
      f.name = NAME + '.freq'
      f.first = arguments.first
      f.repetition = arguments.repetition
      f.starting_sample = arguments.starting_sample
      f.frequency_vector = frequency_vector
  elif arguments.slicing_direction == 'Z':
    pos_list = FDTDobj.mesh.getZmesh()
    #for pos in pos_list:
    # another quick hack to reduce the number of snapshots to 101 around the center... .. todo:: add options for that...
    reduced_range = range(len(pos_list))
    pos_mid = int(numpy.floor(len(pos_list)/2))
    #reduced_range = pos_list[ pos_mid-50:pos_mid+50+1]
    reduced_range = pos_list[ pos_mid-25:pos_mid+25+1]
    #reduced_range = pos_list[ pos_mid-1:pos_mid+1+1]
    #reduced_range = pos_list[ pos_mid-12:pos_mid+12+1]

    # temporary hack
    #arguments.repetition = FDTDobj.flag.iterations - arguments.first
    
    full_list = []
    for pos in reduced_range:
      ##pos = pos_list[idx]
      #e = FDTDobj.addEpsilonSnapshot('Z',pos)
      #e.name = NAME + '.eps'
      #e.first = 1
      #e.repetition = FDTDobj.flag.iterations + 1 # So that only one epsilon snapshot is created. We don't need more.
      
      ## and more quick hacks...
      #e.P1[0] = min(reduced_range)
      #e.P1[1] = min(reduced_range)
      #e.P2[0] = max(reduced_range)
      #e.P2[1] = max(reduced_range)
      
      #f = FDTDobj.addFrequencySnapshot('Z',pos)
      #f.name = NAME + '.freq'
      #f.first = arguments.first
      #f.repetition = arguments.repetition
      #f.frequency_vector = frequency_vector
      
      F = bfdtd.FrequencySnapshot()
      F.name = NAME + '.freq'
      F.plane = 'Z'
      F.P1 = [ FDTDobj.box.lower[0], FDTDobj.box.lower[1], pos]
      F.P2 = [ FDTDobj.box.upper[0], FDTDobj.box.upper[1], pos]
      F.first = arguments.first
      F.repetition = arguments.repetition
      F.starting_sample = arguments.starting_sample
      F.frequency_vector = frequency_vector
      
      full_list.append(F)
      
      ## and more quick hacks...
      #f.P1[0] = min(reduced_range)
      #f.P1[1] = min(reduced_range)
      #f.P2[0] = max(reduced_range)
      #f.P2[1] = max(reduced_range)
      
  else:
    print('ERROR: invalid slicing direction : arguments.slicing_direction = ' + str(arguments.slicing_direction), file=sys.stderr)
    sys.exit(-1)

  ## temporary hack to rectify excitation direction
  #P1 = numpy.array(FDTDobj.excitation_list[0].P1)
  #P2 = numpy.array(FDTDobj.excitation_list[0].P2)
  #Pdiff = P2-P1
  #Pdiff = list(Pdiff)
  #exc_dir = Pdiff.index(max(Pdiff))
  #if exc_dir == 0:
    #FDTDobj.excitation_list[0].E = [1,0,0]
  #elif exc_dir == 1:
    #FDTDobj.excitation_list[0].E = [0,1,0]
  #elif exc_dir == 2:
    #FDTDobj.excitation_list[0].E = [0,0,1]
  #else:
    #print('ERROR: wrong exc_dir = '+str(exc_dir)+' Pdiff = '+str(Pdiff), file=sys.stderr)
    #sys.exit(-1)

  # temporary hack to disable frequency snaphsots
  #FDTDobj.clearFrequencySnapshots()
  #FDTDobj.clearTimeSnapshots()

  # Add full X,Y,Z central snapshots for reference
  pos = FDTDobj.box.getCentro()

  for i in [0,1]:
    letter = ['X','Y','Z'][i]
    #e = FDTDobj.addEpsilonSnapshot(letter,pos[i])
    #e.name = 'central.'+letter+'.eps'
    #e.first = 1
    #e.repetition = FDTDobj.flag.iterations + 1 # So that only one epsilon snapshot is created. We don't need more.
    f = FDTDobj.addFrequencySnapshot(letter,pos[i]);
    f.name = 'central.'+letter+'.fsnap'
    f.first = arguments.first
    f.repetition = arguments.repetition
    f.starting_sample = arguments.starting_sample
    f.frequency_vector = frequency_vector
    full_list.append(f)

  print(full_list)
  list_1 = full_list[0:len(full_list)//2]
  list_2 = full_list[len(full_list)//2:len(full_list)]
    
  if arguments.outdir is None:
    print('ERROR: no outdir specified', file=sys.stderr)
    sys.exit(-1)
  
  if arguments.basename is None:
    arguments.basename = os.path.basename(os.path.abspath(arguments.outdir))
  
  # hack: remove epsilon snapshots and probes to increase speed
  FDTDobj.clearAllSnapshots()
  FDTDobj.clearEpsilonSnapshots()
  FDTDobj.clearProbes()
  
  FDTDobj.fileList = []
  
  destdir = os.path.join(arguments.outdir,'./part_1')
  FDTDobj.snapshot_list = list_1
  FDTDobj.writeAll(destdir, arguments.basename)
  FDTDobj.writeShellScript(destdir + os.path.sep + arguments.basename + '.sh', arguments.basename, arguments.executable, '$JOBDIR', WALLTIME = arguments.walltime)

  destdir = os.path.join(arguments.outdir,'./part_2')
  FDTDobj.snapshot_list = list_2
  FDTDobj.writeAll(destdir, arguments.basename)
  FDTDobj.writeShellScript(destdir + os.path.sep + arguments.basename + '.sh', arguments.basename, arguments.executable, '$JOBDIR', WALLTIME = arguments.walltime)

  return

# .. todo:: nice default values for output dirs/basename
# .. todo:: support use of full epsilon snapshots, i.e. all epsilon values available for the full mesh
def calculateModeVolume(arguments):
  # .. todo:: Finish this
  # NOTE: Add way to specify snapshots, epsilon/frequency snapshot pairs

  # read in mesh
  if arguments.meshfile is None:
    print('ERROR: No meshfile specified.', file=sys.stderr)
    sys.exit(-1)
  sim_mesh = bfdtd.readBristolFDTD(arguments.meshfile, arguments.verbosity)

  # read in snapshot files from the various input files
  if len(arguments.infile) <= 0 :
    print('ERROR: No infile(s) specified.', file=sys.stderr)
    sys.exit(-1)
  sim_in = bfdtd.BFDTDobject()
  sim_in.verbosity = arguments.verbosity
  for infile in arguments.infile:
    sim_in.readBristolFDTD(infile)

  # .. todo:: add path of file based on where it was read from
  # .. todo:: read in .prn files
  # calculate mode volume

  snaplist = sim_in.getFrequencySnapshots()
  for numID in range(len(snaplist)):
    snapshot = snaplist[numID]
    #print(['x','y','z'][snapshot.plane-1])
    #print(sim_in.flag.id_string)
    fsnap_filename, alphaID, pair = brisFDTD_ID_info.numID_to_alphaID_FrequencySnapshot(numID+1, ['x','y','z'][snapshot.plane-1], sim_in.flag.id_string.strip('"'), snap_time_number = 1)
    print(fsnap_filename)
    esnap_filename, alphaID, pair = brisFDTD_ID_info.numID_to_alphaID_EpsilonSnapshot(numID+1, ['x','y','z'][snapshot.plane-1], sim_in.flag.id_string.strip('"'), snap_time_number = 1)
    print(esnap_filename)
  
  #if arguments.fsnapfiles is None:
    #arguments.fsnapfiles = sim_in.getFrequencySnapshots():
  #if arguments.esnapfiles is None:
    #arguments.esnapfiles = sim_in.getEpsilonSnapshots()
    
  #if len(arguments.fsnapfiles) != len(arguments.esnapfiles):
    #print('ERROR: number of frequency snapshots and epsilon snapshots do not match', file=sys.stderr)
    #sys.exit(-1)
  #else:
    #print('OK')

  #print(arguments.fsnapfiles)
  #print(arguments.esnapfiles)
    
  return

def addCentralXYZSnapshots(arguments):

  if arguments.infile is None:
    print('ERROR: No input file specified.', file=sys.stderr)
    sys.exit(-1)

  FDTDobj = bfdtd.BFDTDobject()
  FDTDobj.verbosity = arguments.verbosity
  for infile in arguments.infile:
    FDTDobj.readBristolFDTD(infile)
  
  # hack: remove epsilon snapshots and probes to increase speed
  FDTDobj.clearEpsilonSnapshots()
  #FDTDobj.clearProbes()
  FDTDobj.clearAllSnapshots()
  
  (size,res) = FDTDobj.mesh.getSizeAndResolution()
  
  if arguments.verbosity>0:
    print('res = ',res)
  
  frequency_vector = []
  if arguments.freqListFile is not None:
    frequency_vector.extend(getFrequencies(arguments.freqListFile))
  if arguments.wavelength_mum is not None:
    frequency_vector.extend([get_c0()/i for i in arguments.wavelength_mum])
  if arguments.frequency_MHz is not None:
    frequency_vector.extend(arguments.frequency_MHz)
  
  if len(frequency_vector)<=0:
    print('ERROR: Great scot! You forgot to specify frequencies.', file=sys.stderr)
    sys.exit(-1)

  FDTDobj.flag.iterations = arguments.iterations
  
  # hack: Make sure there will be at least one long duration snapshot at the end
  #arguments.repetition = FDTDobj.flag.iterations - arguments.first
    
  # Add full X,Y,Z central snapshots
  #pos = FDTDobj.box.getCentro()

  pos = [0,0,0]
  # another hack to get the defect position...
  for obj in FDTDobj.geometry_object_list:
    if obj.name == 'defect':
      pos = obj.getCentro()

  for i in [0,1,2]:
    letter = ['X','Y','Z'][i]
    f = FDTDobj.addFrequencySnapshot(letter,pos[i]);
    f.name = 'central.'+letter+'.fsnap'
    f.first = arguments.first
    f.repetition = arguments.repetition
    f.frequency_vector = frequency_vector
    f.starting_sample = arguments.starting_sample
    
  if arguments.outdir is None:
    print('ERROR: no outdir specified', file=sys.stderr)
    sys.exit(-1)
  
  if arguments.basename is None:
    arguments.basename = os.path.basename(os.path.abspath(arguments.outdir))
  
  FDTDobj.fileList = []
  FDTDobj.writeAll(arguments.outdir, arguments.basename)
  FDTDobj.writeShellScript(arguments.outdir + os.path.sep + arguments.basename + '.sh', arguments.basename, arguments.executable, '$JOBDIR', WALLTIME = arguments.walltime)

  return
  
def clearOutputs(arguments):
  if arguments.infile is None:
    print('ERROR: No infile specified.')
    sys.exit(-1)

  if arguments.outdir is None:
    print('ERROR: no outdir specified', file=sys.stderr)
    sys.exit(-1)
  
  if arguments.basename is None:
    arguments.basename = os.path.basename(os.path.abspath(arguments.outdir))
  
  FDTDobj = bfdtd.readBristolFDTD(arguments.infile, arguments.verbosity)
  FDTDobj.clearProbes()
  FDTDobj.clearAllSnapshots()

  FDTDobj.fileList = []
  FDTDobj.writeAll(arguments.outdir, arguments.basename)
  FDTDobj.writeShellScript(arguments.outdir + os.path.sep + arguments.basename + '.sh', arguments.basename, arguments.executable, '$JOBDIR', WALLTIME = arguments.walltime)
  
  return

# .. todo:: no, really, there must be a better way to do this...
# .. todo:: Also, rewrite in-place? Read some args from shellscript? (would require shellscript parser essentially...)
def clearAllSnapshots(arguments):
  if arguments.infile is None:
    print('ERROR: No infile specified.')
    sys.exit(-1)

  if arguments.outdir is None:
    print('ERROR: no outdir specified', file=sys.stderr)
    sys.exit(-1)
  
  if arguments.basename is None:
    arguments.basename = os.path.basename(os.path.abspath(arguments.outdir))
  
  FDTDobj = bfdtd.readBristolFDTD(arguments.infile, arguments.verbosity)
  FDTDobj.clearAllSnapshots()

  FDTDobj.fileList = []
  FDTDobj.writeAll(arguments.outdir, arguments.basename)
  #FDTDobj.writeShellScript(arguments.outdir + os.path.sep + arguments.basename + '.sh', arguments.basename, arguments.executable, '$JOBDIR', WALLTIME = arguments.walltime)
  
  return

def addEpsilonSnapshots(arguments):
  
  if arguments.infile is None:
    print('ERROR: No infile specified.')
    sys.exit(-1)

  if arguments.outdir is None:
    print('ERROR: no outdir specified', file=sys.stderr)
    sys.exit(-1)
  
  if arguments.basename is None:
    arguments.basename = os.path.basename(os.path.abspath(arguments.outdir))

  FDTDobj = bfdtd.BFDTDobject()
  FDTDobj.verbosity = arguments.verbosity
  for infile in arguments.infile:
    FDTDobj.readBristolFDTD(infile)
    
  #FDTDobj.clearProbes()
  #FDTDobj.clearAllSnapshots()

  if arguments.iterations is None:
    FDTDobj.flag.iterations = 1
  else:
    FDTDobj.flag.iterations = arguments.iterations
  
  (size,res) = FDTDobj.mesh.getSizeAndResolution()
  
  if arguments.verbosity>0:
    print('res = ',res)

  if arguments.slicing_direction is None:
    # take the direction with the smallest number of snapshots to reduce number of generated .prn files
    S = ['X','Y','Z']
    arguments.slicing_direction = S[res.index(min(res))]
  
  NAME = 'Epsilon'
  if arguments.slicing_direction == 'X':
    pos_list = FDTDobj.mesh.getXmesh()
    for pos in pos_list:
      e = FDTDobj.addEpsilonSnapshot('X',pos)
      e.name = NAME
      e.first = 1
      e.repetition = FDTDobj.flag.iterations + 1 # So that only one epsilon snapshot is created. We don't need more.
  elif arguments.slicing_direction == 'Y':
    pos_list = FDTDobj.mesh.getYmesh()
    for pos in pos_list:
      e = FDTDobj.addEpsilonSnapshot('Y',pos)
      e.name = NAME
      e.first = 1
      e.repetition = FDTDobj.flag.iterations + 1 # So that only one epsilon snapshot is created. We don't need more.
  elif arguments.slicing_direction == 'Z':
    pos_list = FDTDobj.mesh.getZmesh()
    for pos in pos_list:
      e = FDTDobj.addEpsilonSnapshot('Z',pos)
      e.name = NAME
      e.first = 1
      e.repetition = FDTDobj.flag.iterations + 1 # So that only one epsilon snapshot is created. We don't need more.      
  else:
    print('ERROR: invalid slicing direction : arguments.slicing_direction = ' + str(arguments.slicing_direction), file=sys.stderr)
    sys.exit(-1)

  #FDTDobj.fileList = []
  FDTDobj.clearFileList()
  FDTDobj.writeAll(arguments.outdir, arguments.basename)
  #FDTDobj.writeShellScript(arguments.outdir + os.path.sep + arguments.basename + '.sh', arguments.basename, arguments.executable, '$JOBDIR', WALLTIME = arguments.walltime)
  #FDTDobj.writeInpFile(arguments.outdir + os.path.sep + arguments.basename + '.inp')
    
  return

def FreqToEps(arguments):
  '''Convert frequency snapshots to epsilon snapshots. The original frequency snapshots are removed by default, but can be left if desired.'''
  
  # read in snapshot files from the various input files
  if arguments.infile is None or len(arguments.infile) <= 0 :
    print('ERROR: No infile(s) specified.', file=sys.stderr)
    sys.exit(-1)
  
  FDTDobj = bfdtd.BFDTDobject()
  FDTDobj.verbosity = arguments.verbosity
  for infile in arguments.infile:
    FDTDobj.readBristolFDTD(infile)

  if not arguments.leaveProbes:
    FDTDobj.clearProbes()
  if arguments.iterations:
    FDTDobj.setIterations(arguments.iterations)
  else:
    FDTDobj.setIterations(1)

  oldlist = FDTDobj.getFrequencySnapshots()
  newlist = []
  for idx in range(len(oldlist)):
    snap = oldlist[idx]
    if arguments.namefilter is None or arguments.namefilter in snap.name:
      eps = bfdtd.EpsilonSnapshot()
      eps.name = 'ModeVolume.eps'
      eps.plane = snap.plane
      eps.P1 = snap.P1
      eps.P2 = snap.P2
      eps.first = 1
      eps.repetition = FDTDobj.flag.iterations + 1
      newlist.append(eps)

  if not arguments.leaveFrequencySnapshots:
    FDTDobj.clearFrequencySnapshots()
  
  # append the epsilon snapshots to FDTDobj
  FDTDobj.snapshot_list += newlist
  
  # Just leave one excitation. Should be enough to prevent crash and reduce running time.
  if not arguments.leaveExcitations:
    FDTDobj.excitation_list = [ FDTDobj.excitation_list[0] ]
  
  # set up output path components
  if arguments.outdir is None:
    print('ERROR: no outdir specified', file=sys.stderr)
    sys.exit(-1)
  if arguments.basename is None:
    arguments.basename = os.path.basename(os.path.abspath(arguments.outdir))
  
  FDTDobj.clearFileList()
  FDTDobj.setFileBaseName(arguments.basename)
  FDTDobj.setWallTime(arguments.walltime)
  
  # write files
  if not arguments.no_act:
    FDTDobj.writeAll(arguments.outdir, arguments.basename, overwrite=arguments.overwrite)
    FDTDobj.writeShellScript(arguments.outdir + os.path.sep + arguments.basename + '.sh', EXE=arguments.executable, overwrite=arguments.overwrite)
  else:
    print('arguments.outdir = {}'.format(arguments.outdir))
    print('arguments.basename = {}'.format(arguments.basename))
    print('arguments.executable = {}'.format(arguments.executable))
    print('arguments.walltime = {}'.format(arguments.walltime))
    print('arguments.overwrite = {}'.format(arguments.overwrite))
  
  return

def get_argument_parser():
  """return an ArgumentParser object p with this module's options;
  with an additional dict attribute p._geniegui to specify
  "special" treatment (file/path dialogs) for some options.
  """

  # .. todo:: split options into read-only and read-write operations?
  # operations: read & print info, copy, copy with changes, write back with changes, create shellscript, create .in file, etc
  # too many operations. Needs GUI!
  
  # command-line option handling
  parser = argparse.ArgumentParser(description = 'Get info about bfdtd related files and/or process them in certain ways.', fromfile_prefix_chars='@')
  parser.add_argument('-i','--infile', action="append", help='input file(s) (.geo, .inp or .in) (can be more than one)')
  #parser.add_argument('-i','--infile', action="store", help='input file (.geo, .inp or .in)')
  parser.add_argument('-v','--verbose', action="count", dest="verbosity", default=0, help='verbosity level')
  parser.add_argument('--BFDTDreader-verbosity', type=int, default=0, help='verbosity level of the BFDTD reader')

  parser.add_argument('-o','--outfile', action="store", dest="outfile", default=None, help='output file')
  parser.add_argument('-d','--outdir', action="store", dest="outdir", default=None, help='output directory')
  parser.add_argument('-b','--basename', action="store", dest="basename", default=None, help='output basename')

  parser.add_argument('--walltime', type=int, default=360, help='walltime in hours (default: 360 hours = 15*24 hours = 15 days)')
  
  parser.add_argument('-f', '--format', dest='FORMAT', metavar='FORMAT', help='Use FORMAT as the format string that controls the output.', default='iterations={iterations}')
  #parser.add_argument('FORMAT', nargs='?', metavar='FORMAT', help='formatting string', default='timestep = {dt}\niterations = {iterations}\ntotal_time = {total_time}\nfmin = {fmin[0]}\nfcen = {fcen[0]}\nfmax = {fmax[0]}\nlambda_min = {lmin[0]}\nlambda_cen = {lcen[0]}\nlambda_max = {lmax[0]}')

  subparsers = parser.add_subparsers(help='Available subcommands', dest='chosen_subcommand')
  
  # parser for printExcitation
  parser_printExcitation = subparsers.add_parser('printExcitation', help='print out the Excitation objects')
  parser_printExcitation.set_defaults(func=printExcitation)

  # parser for printExcitationDirection
  parser_printExcitationDirection = subparsers.add_parser('printExcitationDirection', help='print out the directions of excitation objects')
  parser_printExcitationDirection.set_defaults(func=printExcitationDirection)

  # parser for printFrequencySnapshotInfo
  parser_printFrequencySnapshotInfo = subparsers.add_parser('printFrequencySnapshotInfo', help='print information about the frequency snapshots')
  parser_printFrequencySnapshotInfo.set_defaults(func=printFrequencySnapshotInfo)
  
  # parser for printAll
  parser_printAll = subparsers.add_parser('printAll', help='print out all information')
  parser_printAll.set_defaults(func=printAll)

  # parser for FreqToEps
  parser_FreqToEps = subparsers.add_parser('FreqToEps', help='Convert frequency to epsilon snapshots.')
  parser_FreqToEps.set_defaults(func=FreqToEps)
  parser_FreqToEps.add_argument('--leaveProbes', help='Do not remove probe entries (default: False).', action="store_true", default=False)
  parser_FreqToEps.add_argument('--leaveFrequencySnapshots', help='Do not remove frequency snapshot entries (default: False).', action="store_true", default=False)
  parser_FreqToEps.add_argument('--leaveExcitations', help='Do not remove excitation entries (default: False). Note that one excitation will always be left for the simulation to run.', action="store_true", default=False)
  parser_FreqToEps.add_argument("-n", "--no-act", action="store_true", dest="no_act", default=False, help="Do not write output files. Just show what would be written.")
  parser_FreqToEps.add_argument("--overwrite", action="store_true", default=False, help="Overwrite existing files. (default: False)")

  # excitation + timestep info (useful for probe analysis)
  parser_printFormattedString = subparsers.add_parser('printFormattedString', help='print out formatted information', formatter_class=argparse.RawDescriptionHelpFormatter,
      description='''\
        Print out formatted information.
        
        Usage:
          bfdtd_tool.py -i qedc3_2_05.in -f FORMAT printFormattedString

        FORMAT controls the output.  Interpreted "replacement fields" are:

          dt : the timestep used by the simulation
          iterations : number of iterations
          total_time : total simulation time

          fmin[n] : the minimum frequency of the nth excitation
          fcen[n] : the central frequency of the nth excitation
          fmax[n] : the maximum frequency of the nth excitation
          lmin[n] : the minimum wavelength of the nth excitation
          lcen[n] : the central wavelength of the nth excitation
          lmax[n] : the maximum wavelength of the nth excitation
          eloc[n] : the location of the nth excitation

        Example format strings:
          'timestep={dt:.2f} fmin={fmin[0]:.3e} fcen={fcen[0]} fmax={fmax[0]:.0f} lambda_min={lmin[0]} lambda_cen={lcen[0]} lambda_max={lmax[0]}'
          'timestep={dt:.2f} iterations={iterations} total_time={total_time:.f}'
          '{eloc[0][0]} {eloc[0][1]} {eloc[0][2]}'
      ''')
  parser_printFormattedString.set_defaults(func=printFormattedString)
  #parser_printFormattedString.add_argument('FORMAT', nargs='?', metavar='FORMAT', help='formatting string', default='timestep = {dt}\niterations = {iterations}\ntotal_time = {total_time}\nfmin = {fmin[0]}\nfcen = {fcen[0]}\nfmax = {fmax[0]}\nlambda_min = {lmin[0]}\nlambda_cen = {lcen[0]}\nlambda_max = {lmax[0]}')
  
  #group = parser.add_mutually_exclusive_group()
  #group.add_argument('--foo', action='store_true')
  #group.add_argument('--bar', action='store_false')
  
  #subparsers = parser.add_subparsers(help='functions',dest='subparser_name')
  #modevolume_parser = subparsers.add_parser('modevolume', help='Add frequency snapshots to calculate the mode volume')
  #modevolume_parser.add_argument('--slicing-direction', choices=['X','Y','Z'])

  #tmp_parser = subparsers.add_parser('lol', help='lalalala')
  #tmp_parser.add_argument('--slicing-death', choices=['Xoxo','Yoyo','Zozo'], help='lol you are LEAKING!')

  group = parser.add_argument_group('Read-only operations')
  group.add_argument('-N','--ncells', action="store_true", dest='print_Ncells', default=False, help='print the number of cells')
  group.add_argument('--printSnapshotFrequencyList', action="store_true", dest='printSnapshotFrequencyList', default=False, help='print out a list of frequencies used in frequency snapshots')
  
  group.add_argument('--id', action="store", metavar='ID', dest="id_list", nargs='+', type=int, help='ID(s) of the object(s) you want to print out.')
  
  group = parser.add_argument_group('Writing operations')
  group.add_argument('--writeInpFile', help='create .inp file based on all the specified input', metavar='FILENAME')
  
  group = parser.add_argument_group('Add mode volume snapshots')
  group.add_argument('--add-modevolume-snapshots', help='Add frequency snapshots to calculate the mode volume', action="store_true", default=False)
  group.add_argument('--slicing-direction', choices=['X','Y','Z'], default=None, dest='slicing_direction')
  group.add_argument('--first', type=int, default=3200, help='first iteration at which to take snapshot')
  group.add_argument('--repetition', type=int, default=32000, help='step in number of iterations at which to take snapshots')
  group.add_argument('--starting_sample', type=int, default=6400, help='starting sample for the snapshots')
  group.add_argument('--iterations', type=int, default=None, help='number of iterations') # previous default: 67200
  # .. todo:: Make linebreaks work in CLI help. :(
  group.add_argument('--freqListFile', default=None, help='''\
                                                            frequency list file
                                                            format:
                                                            PeakNo	Frequency(Hz)	Wavelength(nm)	QFactor
                                                            1	4.7257745e+14	634.37741293	40.4569
                                                            2	4.9540615e+14	605.14480606	90.37''')

  group.add_argument('--readFreqFromInput', action="store_true", default=False, help='read frequencies from input')

  # .. todo:: default args should probably be gotten from the various classes
  group.add_argument('--exe', action="store", metavar='EXE', dest="executable", help='exe to use', default='fdtd')

  group.add_argument('--frequency_MHz', type=float, help='frequency in MHz', action='store', metavar='f(MHz)', nargs='+')
  group.add_argument('--wavelength_mum', type=float, help='wavelength in µm', action='store', metavar='lambda(µm)', nargs='+')

  group = parser.add_argument_group('Calculate mode volume (NOT YET WORKING!!!)')
  group.add_argument('--calc-modevolume', help='Calculate the mode volume (NOT YET WORKING!!!)', action="store_true", dest='calc_modevolume', default=False)
  group.add_argument('--fsnapfiles', metavar='FSNAP', help='Frequency snapshots to use', nargs='+')
  group.add_argument('--tsnapfiles', metavar='TSNAP', help='Time snapshots to use', nargs='+')
  group.add_argument('--esnapfiles', metavar='ESNAP', help='Epsilon snapshots to use', nargs='+')
  group.add_argument('--msnapfiles', metavar='MSNAP', help='Mode filtered probes to use', nargs='+')
  group.add_argument('--probefiles', metavar='PROBE', help='Probes to use', nargs='+')
  group.add_argument('--prnfiles', metavar='PRN', help='.prn files to use', nargs='+')
  group.add_argument('--namefilter', metavar='STRING', help='string to look for in object names', default=None)
  group.add_argument('--meshfile', metavar='INP', help='.inp file containing the mesh to use', default=None)

  group = parser.add_argument_group('addCentralXYZSnapshots')
  group.add_argument('--addCentralXYZSnapshots', help='addCentralXYZSnapshots', action="store_true", dest='addCentralXYZSnapshots', default=False)

  group = parser.add_argument_group('clearAllOutput')
  group.add_argument('--clearAllOutput', help='clearAllOutput', action="store_true", dest='clearAllOutput', default=False)
  
  group = parser.add_argument_group('addEpsilonSnapshots')
  group.add_argument('--addEpsilonSnapshots', help='addEpsilonSnapshots', action="store_true", dest='addEpsilonSnapshots', default=False)

  group = parser.add_argument_group('clearOutputs')
  group.add_argument('--clearOutputs', help='clearOutputs', action="store_true", dest='clearOutputs', default=False)

  group = parser.add_argument_group('clearAllSnapshots')
  group.add_argument('--clearAllSnapshots', help='clearAllSnapshots', action="store_true", dest='clearAllSnapshots', default=False)

  group = parser.add_argument_group('Rotate')
  group.add_argument('-r','--rotate', action="store_true", dest='rotate', default=False, help='Rotate the geometry.')
  #axis_point
  #axis_direction
  #angle_degrees

  group = parser.add_argument_group('Meshing')
  group.add_argument('-m','--mesh', action="store_true", dest='mesh', default=False, help='Automatically mesh the geometry.')

  # .. todo:: for later use :)
  #parser.add_argument("--path","-p", default="",
                 #help = "project path (directory) containing an .sff file")
  #parser._geniegui = dict()
  #parser._geniegui["--path"] = "dir"
  return parser

# .. todo:: Add PPN specification option?
def main(args=[]):
  parser = get_argument_parser()

  # use graphical dialogs if no arguments are given
  if len(args)==0:
    open_dialog = tkinter.filedialog.Open()

    # options (all have default values):
    #
    # - defaultextension: added to filename if not explicitly given
    #
    # - filetypes: sequence of (label, pattern) tuples.  the same pattern
    #   may occur with several patterns.  use "*" as pattern to indicate
    #   all files.
    #
    # - initialdir: initial directory.  preserved by dialog instance.
    #
    # - initialfile: initial file (ignored by the open dialog).  preserved
    #   by dialog instance.
    #
    # - parent: which window to place the dialog on top of
    #
    # - title: dialog title
    #
    # - multiple: if true user may select more than one file
    #
    # options for the directory chooser:
    #
    # - initialdir, parent, title: see above
    #
    # - mustexist: if true, user must pick an existing directory
    #
    open_dialog.options['title'] = 'Choose a .cfg file...'
    open_dialog.options['filetypes'] = [("configuration files","*.cfg"),("all files", "*")]
    cfgfile = open_dialog.show()
    if os.path.isfile(cfgfile):
      args = ['@'+cfgfile]

  arguments = parser.parse_args(args)

  if arguments.verbosity > 0:
    print('---------')
    print(arguments)
    print('---------')
  
  if len(args) == 0:
    parser.print_help()
    return
  elif 'func' in arguments: # if a sub-command has been chosen
    arguments.func(arguments)
    return
  else: # if no sub-command has been chosen
    # .. todo:: implement this nicer way?:
    #  Only works if func has been defined (for example with subcommand and set_defaults())
    #  arguments.func(arguments)  # call the appropriate subcommand function
    
    # .. todo:: Some/most functions could be moved into the BFDTD object class
    if arguments.writeInpFile:
      writeInpFile(arguments)
      return
    if arguments.print_Ncells:
      printNcells(arguments)
      return
    if arguments.printSnapshotFrequencyList:
      printSnapshotFrequencyList(arguments)
      return

    if arguments.add_modevolume_snapshots:
      addModeVolumeFrequencySnapshots(arguments)
      return
    if arguments.calc_modevolume:
      calculateModeVolume(arguments)
      return
    if arguments.addCentralXYZSnapshots:
      addCentralXYZSnapshots(arguments)
      return
    if arguments.clearAllOutput:
      clearAllOutput(arguments)
      return
    if arguments.addEpsilonSnapshots:
      addEpsilonSnapshots(arguments)
      return
    if arguments.clearOutputs:
      clearOutputs(arguments)
      return
    if arguments.clearAllSnapshots:
      clearAllSnapshots(arguments)
      return

    # default action:
    #printAll(arguments)
    printFormattedString(arguments)

    return

def do_something(argparseuiinstance):
    options = argparseuiinstance.parse_args()
    print ("Options: ", options)

def main_argparseui():
  
  parser = get_argument_parser()
  
  app = QtWidgets.QApplication(sys.argv)
  a = argparseui.ArgparseUi(parser,use_save_load_button=True,ok_button_handler=do_something)
  a.show()
  app.exec_()
  if a.result() != 1:
      # Do what you like with the arguments...
      print ("Cancel pressed")
  return
    
if __name__ == "__main__":
  warnings.simplefilter("error")
  main(sys.argv[1:])
  #main_argparseui()
