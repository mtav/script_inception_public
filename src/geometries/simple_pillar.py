#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import numpy
import argparse
import tempfile
import bfdtd
import constants
from meshing.meshing import subGridMultiLayer
from utilities.common import LimitsToThickness, getProbeColumnFromExcitation
from bfdtd.bristolFDTD_generator_functions import GEOshellscript_advanced
#from bfdtd.bfdtd_parser import *
#from utilities.common import *

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('DSTDIR', default=tempfile.gettempdir(), nargs='?')
  args = parser.parse_args()  
  print(args.DSTDIR)
  
  pillar = bfdtd.BFDTDobject()

  # constants
  n_air = 1; n_diamond = 2.4
  Lambda_mum = 0.637
  delta = Lambda_mum/(10*n_diamond)
  freq = constants.get_c0()/Lambda_mum
  k=1; radius = k*Lambda_mum/(4*n_diamond)
  Nbottom = 30; Ntop = 30
  h_air = Lambda_mum/(4*n_air)
  h_diamond = Lambda_mum/(4*n_diamond)
  h_cavity = Lambda_mum/(n_diamond)
  height = Nbottom*(h_air+h_diamond) + h_cavity + Ntop*(h_air+h_diamond)
  buffer = 0.25
  FullBox_upper = [ height+2*buffer, 2*(radius+buffer), 2*(radius+buffer) ]
  P_centre = [ buffer + Nbottom*(h_air+h_diamond) + 0.5*h_cavity, 0.5*FullBox_upper[1], 0.5*FullBox_upper[2] ]

  # define flag
  pillar.flag.iterations = 100000

  # define boundary conditions
  pillar.boundaries.Xpos_bc = 2
  pillar.boundaries.Ypos_bc = 1 #2
  pillar.boundaries.Zpos_bc = 2

  # define box
  pillar.box.lower = [0,0,0]
  if pillar.boundaries.Ypos_bc == 2:
    pillar.box.upper = FullBox_upper
  else:
    pillar.box.upper = [ FullBox_upper[0], 0.5*FullBox_upper[1], FullBox_upper[2] ]

  # define geometry
  block = bfdtd.Block()
  block.setLowerAbsolute([ P_centre[0]-0.5*height, P_centre[1]-radius, P_centre[2]-radius ])
  block.setUpperAbsolute([ P_centre[0]+0.5*height, P_centre[1]+radius, P_centre[2]+radius ])
  block.setRefractiveIndex(n_diamond)
  pillar.setGeometryObjects([ block ])

  # define excitation
  excitation = bfdtd.Excitation()
  P1 = [ P_centre[0], P_centre[1]-1*delta, P_centre[2] ]
  P2 = P_centre
  excitation.setExtension(P1, P2)
  excitation.setFrequency(freq)
  excitation.setEy()
  pillar.appendExcitation(excitation)

  # define probe
  if pillar.boundaries.Ypos_bc == 2:
    probe = bfdtd.Probe(position = [ buffer+height+delta, P_centre[1], P_centre[2] ])
  else:
    probe = bfdtd.Probe(position = [ buffer+height+delta, P_centre[1]-delta, P_centre[2] ])
  pillar.probe_list = [ probe ]

  # define frequency snapshots
  first = min(65400,pillar.flag.iterations)
  frequency_vector = [freq]
  F = pillar.addFrequencySnapshot('x',P_centre[0]); F.first = first; F.frequency_vector = frequency_vector
  if pillar.boundaries.Ypos_bc == 2:
    F = pillar.addFrequencySnapshot('y',P_centre[1]); F.first = first; F.frequency_vector = frequency_vector
  else:
    F = pillar.addFrequencySnapshot('y',P_centre[1]-delta); F.first = first; F.frequency_vector = frequency_vector
  F = pillar.addFrequencySnapshot('z',P_centre[2]); F.first = first; F.frequency_vector = frequency_vector
  F = pillar.addBoxFrequencySnapshots(); F.first = first; F.frequency_vector = frequency_vector

  # define mesh
  thicknessVector_X = [ block.getLowerAbsolute()[0]-pillar.box.lower[0], P_centre[0]-block.getLowerAbsolute()[0], block.getUpperAbsolute()[0]-P_centre[0], delta, pillar.box.upper[0]-(block.getUpperAbsolute()[0]+delta) ]
  if pillar.boundaries.Ypos_bc == 2:
    thicknessVector_Y = [ block.getLowerAbsolute()[1]-pillar.box.lower[1], (P_centre[1]-delta)-block.getLowerAbsolute()[1], delta, delta, block.getUpperAbsolute()[1]-(P_centre[1]+delta), pillar.box.upper[1]-block.getUpperAbsolute()[1] ]
  else:
    thicknessVector_Y = [ block.getLowerAbsolute()[1]-pillar.box.lower[1], (P_centre[1]-delta)-block.getLowerAbsolute()[1], delta ]
  thicknessVector_Z = LimitsToThickness([ pillar.box.lower[2], block.getLowerAbsolute()[2], P_centre[2], block.getUpperAbsolute()[2], pillar.box.upper[2] ])
  max_delta_Vector_X = [ delta ]*len(thicknessVector_X)
  max_delta_Vector_Y = [ delta ]*len(thicknessVector_Y)
  max_delta_Vector_Z = [ delta ]*len(thicknessVector_Z)
  delta_X_vector, local_delta_X_vector = subGridMultiLayer(max_delta_Vector_X, thicknessVector_X)
  delta_Y_vector, local_delta_Y_vector = subGridMultiLayer(max_delta_Vector_Y, thicknessVector_Y)
  delta_Z_vector, local_delta_Z_vector = subGridMultiLayer(max_delta_Vector_Z, thicknessVector_Z)
  pillar.getMesh().setXmeshDelta(delta_X_vector)
  pillar.getMesh().setYmeshDelta(delta_Y_vector)
  pillar.getMesh().setZmeshDelta(delta_Z_vector)

  # write
  #DSTDIR = os.getenv('DATADIR')
  #DSTDIR = os.getenv('TESTDIR')
  #DSTDIR = os.getenv('DATADIR')+os.sep+'run_20110602'
  #DSTDIR = tempfile.mkdtemp()
  BASENAME = 'simple_pillar'
  pillar.writeAll(args.DSTDIR+os.sep+BASENAME, BASENAME)
  GEOshellscript_advanced(args.DSTDIR+os.sep+BASENAME+os.sep+BASENAME+'.sh', BASENAME, getProbeColumnFromExcitation(excitation.E),'$HOME/bin/fdtd', '$JOBDIR', WALLTIME = 360)
  print(pillar.getNcells())
  print('DSTDIR = {}'.format(args.DSTDIR))

if __name__ == "__main__":
  main()
