#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import numpy
import argparse
import tempfile
from meshing.meshing import subGridMultiLayer
from bfdtd.bfdtd_parser import *
from bfdtd.snapshot import *
from utilities.common import *
from constants.constants import *

# .. todo:: Easy X,Y,Z direction switching and/or rotation...

class DBRlayer(Block):
  def write_entry(self, FILE=sys.stdout):
    # for cylinders
    cyl = Cylinder()
    cyl.setLocation(self.getCentro())
    cyl.setHeight(self.getSize()[0])
    cyl.setDiametre(self.getSize()[1])
    cyl.setAxis([1,0,0])
    cyl.setRefractiveIndex(self.getRefractiveIndex())
    cyl.write_entry(FILE)
    # for blocks
##    self.write_entry(FILE)

DBRlayer=Block

def simpleDBRpillar(DSTDIR, BASENAME, radius, n_high, n_low, Ntop, Nbottom, Lambda_mum):
  pillar = BFDTDobject()

  # mesh resolution:
  #delta = Lambda_mum/(10*n_high)
  delta = Lambda_mum/(16*n_high)


  freq = get_c0()/Lambda_mum
  n_quartz_coverslip = 1.4537
  h_air = Lambda_mum/(4*n_low)
  h_diamond = Lambda_mum/(4*n_high)
  h_cavity = Lambda_mum/(n_high)
  height = Nbottom*(h_air+h_diamond) + h_cavity + Ntop*(h_air+h_diamond)
  buffer_space = 2
  subbuffer = 4*delta
  FullBox_upper = [ height+2*buffer_space, 2*(radius+buffer_space), 2*(radius+buffer_space) ]
  P_centre = [ buffer_space + Nbottom*(h_air+h_diamond) + 0.5*h_cavity, 0.5*FullBox_upper[1], 0.5*FullBox_upper[2] ]

  # define flag
  pillar.flag.iterations = 1000000

  # define boundary conditions
  pillar.boundaries.Xpos_bc = 2
  #pillar.boundaries.Ypos_bc = 1 # Metal wall
  pillar.boundaries.Ypos_bc = 2 # Mur 1st
  pillar.boundaries.Zpos_bc = 2

  # define box
  pillar.getBox().setLower([0,0,0])
  if pillar.boundaries.Ypos_bc == 2:
    pillar.getBox().setUpper(FullBox_upper)
  else:
    pillar.getBox().setUpper([ FullBox_upper[0], 0.5*FullBox_upper[1], FullBox_upper[2] ])

  # define geometry
  Ymin = P_centre[1]-radius
  Ymax = P_centre[1]+radius
  Zmin = P_centre[2]-radius
  Zmax = P_centre[2]+radius

  X_current = buffer_space

  for i in range(Nbottom):

    block = DBRlayer()
    block.setLowerAbsolute([ X_current, Ymin, Zmin ])
    block.setUpperAbsolute([ X_current+h_diamond, Ymax, Zmax ])
    block.setRefractiveIndex(n_high)
    pillar.appendGeometryObject(block)
    X_current = X_current + h_diamond

    block = DBRlayer()
    block.setLowerAbsolute([ X_current, Ymin, Zmin ])
    block.setUpperAbsolute([ X_current+h_air, Ymax, Zmax ])
    block.setRefractiveIndex(n_low)
    pillar.appendGeometryObject(block)
    X_current = X_current + h_air

  block = DBRlayer()
  block.setLowerAbsolute([ X_current, Ymin, Zmin ])
  block.setUpperAbsolute([ X_current+h_cavity, Ymax, Zmax ])
  block.setRefractiveIndex(n_high)
  pillar.appendGeometryObject(block)
  X_current = X_current + h_cavity

  for i in range(Ntop):
    block = DBRlayer()
    block.setLowerAbsolute([ X_current, Ymin, Zmin ])
    block.setUpperAbsolute([ X_current+h_air, Ymax, Zmax ])
    block.setRefractiveIndex(n_low)
    pillar.geometry_object_list.append(block)
    X_current = X_current + h_air

    block = DBRlayer()
    block.setLowerAbsolute([ X_current, Ymin, Zmin ])
    block.setUpperAbsolute([ X_current+h_diamond, Ymax, Zmax ])
    block.setRefractiveIndex(n_high)
    pillar.appendGeometryObject(block)
    X_current = X_current + h_diamond

  # define excitation
  excitation = Excitation()
  if pillar.boundaries.Ypos_bc == 2: #full-sim
    P1 = [ P_centre[0], P_centre[1]-1*delta, P_centre[2] ]
    P2 = [ P_centre[0], P_centre[1]+1*delta, P_centre[2] ]
  else: # half-sim
    P1 = [ P_centre[0], P_centre[1]-1*delta, P_centre[2] ]
    P2 = P_centre

  excitation.setExtension(P1, P2)
  excitation.setFrequency(freq)
  excitation.setEy()
  pillar.appendExcitation(excitation)

  #probe = pillar.appendProbe(Probe(position = excitation.getCentro()))
  #probe.setName('probe ')
  #p = pillar.appendProbe(Probe(position = excitation.getCentro()))
  #p = pillar.appendProbe(Probe(position = excitation.getCentro()))
  #p = pillar.appendProbe(Probe(position = excitation.getCentro()))

  probe_distance = 4*delta

  P_input_excitation = excitation.getCentro()
  # add probes around excitation
  probe_defect = pillar.appendProbe(Probe())
  probe_defect.setPosition(P_input_excitation)
  probe_defect.setName('probe_defect_Centro')
  probe_defect.setStep(1)

  probe_defect = pillar.appendProbe(Probe())
  probe_defect.setPosition(P_input_excitation + probe_distance*array([1,0,0]))
  probe_defect.setName('probe_defect_X')
  probe_defect.setStep(1)

  probe_defect = pillar.appendProbe(Probe())
  probe_defect.setPosition(P_input_excitation + probe_distance*array([0,1,0]))
  probe_defect.setName('probe_defect_Y')
  probe_defect.setStep(1)

  probe_defect = pillar.appendProbe(Probe())
  probe_defect.setPosition(P_input_excitation + probe_distance*array([0,0,1]))
  probe_defect.setName('probe_defect_Z')
  probe_defect.setStep(1)

  # define probe on top of pillar
  if pillar.boundaries.Ypos_bc == 2:
    probe = Probe(position = [ buffer_space+height+1*delta+(buffer_space-delta)/61, P_centre[1], P_centre[2] ])
  else:
    probe = Probe(position = [ buffer_space+height+1*delta+(buffer_space-delta)/61, P_centre[1]-delta, P_centre[2] ])
  pillar.appendProbe(probe)
  probe.setStep(1)

  # define frequency snapshots
  #freqSnapshots = get_c0()/0.90776846389  #Lambda_mum 0.90776846389
  freqSnapshots = get_c0()/1.5  #Lambda_mum 0.89361525246
  first = min(65400,pillar.flag.iterations)
  frequency_vector = [freqSnapshots]
  F = pillar.addFrequencySnapshot('x', P_centre[0]); F.first = first; F.frequency_vector = frequency_vector
  if pillar.boundaries.Ypos_bc == 2:
    F = pillar.addFrequencySnapshot('y', P_centre[1]); F.first = first; F.frequency_vector = frequency_vector
  else:
    F = pillar.addFrequencySnapshot('y', P_centre[1]-delta); F.first = first; F.frequency_vector = frequency_vector
  F = pillar.addFrequencySnapshot('z', P_centre[2]); F.first = first; F.frequency_vector = frequency_vector

  # define Time Snapshot
  F = pillar.addTimeSnapshot('x', P_centre[0]); F.first = first;
  if pillar.boundaries.Ypos_bc == 2:
    F = pillar.addTimeSnapshot('y', P_centre[1]); F.first = first;
  else:
    F = pillar.addTimeSnapshot('y', P_centre[1]-delta); F.first = first;
  F = pillar.addTimeSnapshot('z', P_centre[2]); F.first = first;

##  F = pillar.addFrequencySnapshot('z', P_centre[2]+1+delta); F.first = first; F.frequency_vector = frequency_vector

  # adding a box snapshot:
  # step 1: define the common frequency snapshot properties
  F = FrequencySnapshot()
  F.setName('Box frequency snapshot')
  F.setFirst(first)
  #F.setRepetition(100)
  #F.setStartingSample(2)
  # F.setWavelengths([0.900]) # in microns
  F.setFrequencies(frequency_vector) # in MHz
  F.setFullExtensionOff()
  # step 2: define the box
  fbox = SnapshotBoxSurface()
  # step 3: pass the "base snapshot" to the box
  fbox.setBaseSnapshot(F)
  # step 4: define the box extension
  #pillar_lower_corner = [buffer_space+h_air-delta, P_centre[1]-radius-delta, P_centre[2]-radius-delta]
  pillar_lower_corner = [buffer_space+2*delta, P_centre[1]-radius-2*delta, P_centre[2]-radius-2*delta]
  pillar_upper_corner = [buffer_space+height+1*delta+(buffer_space-delta)/61, P_centre[1]+radius+2*delta, P_centre[2]+radius+2*delta]
  fbox.setExtension(pillar_lower_corner, pillar_upper_corner) # lower corner, upper corner of the box
  # step 5: Add the snapshot box to the simulation
  pillar.appendSnapshot(fbox)

  pillar.appendProbe(Probe(pillar_lower_corner))
  pillar.appendProbe(Probe(pillar_upper_corner))

  #F = FrequencySnapshot()
  #F.setFirst(first)
  #F.setFrequencies(frequency_vector)
  #fbox = SnapshotBoxSurface()
  #fbox.setBaseSnapshot(F)
  #fbox.setExtension(*pillar.getExtension())
  #pillar.appendSnapshot(fbox)

  # full box snapshot
##  F = pillar.addBoxFrequencySnapshots()
##  F.setFirst(first)
##  F.setFrequencies(frequency_vector)

  # define mesh
  thicknessVector_X = [ buffer_space ]
  thicknessVector_X.extend([h_diamond, h_air]*Nbottom)
  thicknessVector_X.extend([0.5*h_cavity, 0.5*h_cavity])
  thicknessVector_X.extend([h_air, h_diamond]*Ntop)
  thicknessVector_X.extend([delta, buffer_space-delta])

  max_delta_Vector_X = [ Lambda_mum/(16*n_high) ]
  max_delta_Vector_X.extend([Lambda_mum/(16*n_high), Lambda_mum/(32*n_low)]*Nbottom)
  max_delta_Vector_X.extend([Lambda_mum/(16*n_high), Lambda_mum/(16*n_high)])
  max_delta_Vector_X.extend([Lambda_mum/(32*n_low), Lambda_mum/(16*n_high)]*Ntop)
  #max_delta_Vector_X.extend([delta, Lambda_mum/(20*n_low)])
  #max_delta_Vector_X.extend([Lambda_mum/(16*n_low), Lambda_mum/(16*n_high)])
  max_delta_Vector_X.extend([delta, delta])

  # very basic thickness definition
  #max_delta_Vector_X = [ delta ]*len(thicknessVector_X)

  thicknessVector_Y = [ (block.getLowerAbsolute()[1]-subbuffer)-pillar.getBox().getLower()[1], subbuffer, (P_centre[1]-delta)-block.getLowerAbsolute()[1], delta ]
  max_delta_Vector_Y = [ h_air, delta, delta, delta ]
  if pillar.boundaries.Ypos_bc == 2:
    thicknessVector_Y = symmetrifyEven(thicknessVector_Y)
    max_delta_Vector_Y = symmetrifyEven(max_delta_Vector_Y)

  thicknessVector_Z = LimitsToThickness([ pillar.getBox().lower[2], block.getLowerAbsolute()[2]-subbuffer, block.getLowerAbsolute()[2], P_centre[2], block.getUpperAbsolute()[2], block.getUpperAbsolute()[2]+subbuffer, pillar.getBox().getUpper()[2] ])
  max_delta_Vector_Z = [ h_air, thicknessVector_Z[1]/4, delta, delta, thicknessVector_Z[4]/4, h_air ]

  delta_X_vector, local_delta_X_vector = subGridMultiLayer(max_delta_Vector_X, thicknessVector_X)
  delta_Y_vector, local_delta_Y_vector = subGridMultiLayer(max_delta_Vector_Y, thicknessVector_Y)
  delta_Z_vector, local_delta_Z_vector = subGridMultiLayer(max_delta_Vector_Z, thicknessVector_Z)
  pillar.getMesh().setXmeshDelta(delta_X_vector)
  pillar.getMesh().setYmeshDelta(delta_Y_vector)
  pillar.getMesh().setZmeshDelta(delta_Z_vector)

  # substrate
  block = Block()
  block.setLowerAbsolute([ 0, 0, 0 ])
  #block.setUpperAbsolute([ buffer_space+h_diamond, pillar.getBox().getUpper()[1], pillar.getBox().getUpper()[2] ])
  block.setUpperAbsolute([ buffer_space, pillar.getBox().getUpper()[1], pillar.getBox().getUpper()[2] ])
  block.setRefractiveIndex(n_quartz_coverslip)  #  n_quartz_coverslip=1.4537
  pillar.appendGeometryObject(block)

  # write
  #pillar.writeAll(DSTDIR+os.sep+BASENAME, BASENAME)
  #GEOshellscript_advanced(DSTDIR+os.sep+BASENAME+os.sep+BASENAME+'.sh', BASENAME, getProbeColumnFromExcitation(excitation.E),'$HOME/bin/fdtd', '$JOBDIR', WALLTIME = 360)

  pillar.setFileBaseName(BASENAME)
  pillar.setWallTime(120)
  pillar.writeTorqueJobDirectory(DSTDIR + os.sep + BASENAME)

  print('{:.3e}'.format(pillar.getNcells()))
  print('DSTDIR = {}'.format(DSTDIR))
  return

def OldDiamondTest():
  n_air = 1
  n_diamond = 2.4
  Lambda_mum = 0.637
  Nbottom = 40
  Ntop = 20
  for k in [1,2,3,4,5,6,7,8]:
    BASENAME = 'simple_DBR_pillar.k_'+str(k)
    radius = k*Lambda_mum/(4*n_diamond)
    simpleDBRpillar(tempfile.gettempdir(), BASENAME, radius, n_diamond, n_air, Ntop, Nbottom, Lambda_mum)
  return

def PillarPetros(DSTDIR):
  #DSTDIR = os.getenv('DATADIR')
  #DSTDIR = os.getenv('TESTDIR')
  #DSTDIR = os.getenv('DATADIR')+os.sep+'run_20110602'
  #DSTDIR = tempfile.mkdtemp()
  #DSTDIR = tempfile.gettempdir()
  #simpleDBRpillar(DSTDIR=DSTDIR, BASENAME='SquarePillarPetros-906nm', radius=1, n_high=3.55, n_low=2.95, Ntop=5, Nbottom=18, Lambda_mum=0.906)
  #simpleDBRpillar(DSTDIR=DSTDIR, BASENAME='CircularPillarPetros-906nm', radius=1, n_high=3.55, n_low=2.95, Ntop=5, Nbottom=18, Lambda_mum=0.906)
  #simpleDBRpillar(DSTDIR=DSTDIR, BASENAME='SquarePillarPetros-893nm', radius=1, n_high=3.608, n_low=2.988, Ntop=5, Nbottom=18, Lambda_mum=0.893)
  #simpleDBRpillar(DSTDIR=DSTDIR, BASENAME='CircularPillarPetros-893nm', radius=1, n_high=3.608, n_low=2.988, Ntop=5, Nbottom=18, Lambda_mum=0.893)
  simpleDBRpillar(DSTDIR=DSTDIR, BASENAME='SquarePillarPetros-SnS-n1.28', radius=1, n_high=3.0, n_low=1.28, Ntop=6, Nbottom=18, Lambda_mum=1.55)
  #simpleDBRpillar(DSTDIR=DSTDIR, BASENAME='SquarePillarPetros-SnS-n1.33', radius=1, n_high=3.0, n_low=1.33, Ntop=6, Nbottom=18, Lambda_mum=1.55)
  #simpleDBRpillar(DSTDIR=DSTDIR, BASENAME='SquarePillarPetros-SnS-n1.52', radius=1, n_high=3.0, n_low=1.52, Ntop=6, Nbottom=18, Lambda_mum=1.55)

  return

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('DSTDIR', default=tempfile.gettempdir(), nargs='?')
  args = parser.parse_args()
  print(args)

  DSTDIR = args.DSTDIR
  if not os.path.isdir(DSTDIR):
    os.mkdir(DSTDIR)

  #OldDiamondTest()
  PillarPetros(DSTDIR)
  #main()
