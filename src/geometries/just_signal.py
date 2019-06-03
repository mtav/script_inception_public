#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# creates a simple excitation in a vaccum box with probes for plotting

import sys
import os
import numpy
import constants
import argparse
import tempfile
import bfdtd
from bfdtd.bfdtd_parser import *
from utilities.common import *
from bfdtd.excitationTemplate import *
from bfdtd.excitation_utilities import *

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('DSTDIR', default=tempfile.gettempdir(), nargs='?')
  args = parser.parse_args()  
  print(args.DSTDIR)

  if not os.path.isdir(args.DSTDIR):
    os.mkdir(args.DSTDIR)

  BASENAME = 'just_signal'

  sim = BFDTDobject()

  excitation_wavelength_mum = 0.910

  sim.box.setLower([0,0,0])
  sim.box.setUpper([10*excitation_wavelength_mum,10*excitation_wavelength_mum,10*excitation_wavelength_mum])

  D_mum = 2*excitation_wavelength_mum

  sim.flag.timeStep = 0.5
  sim.flag.iterations = int(numpy.ceil(0.05*D_mum/(get_c0()*sim.flag.timeStep*1e-12)))

  sim.boundaries.setBoundaryConditionsXposToPML()
  sim.boundaries.setBoundaryConditionsYposToPML()
  sim.boundaries.setBoundaryConditionsZposToPML()
  sim.boundaries.setBoundaryConditionsXnegToPML()
  sim.boundaries.setBoundaryConditionsYnegToPML()
  sim.boundaries.setBoundaryConditionsZnegToPML()

  P_excitation = 0.5*(sim.box.lower + sim.box.upper)
  delta = excitation_wavelength_mum
  propagation_direction = 'z'
  E1 = [1,0,0]
  freq_MHz = get_c0()/excitation_wavelength_mum

  excitation, template = ExcitationWrapper(Ysym=False, centre=P_excitation, size=delta, plane_direction=propagation_direction, type='1D', excitation_direction=E1, frequency=freq_MHz)
  excitation.time_constant = 10*4e-9
  sim.excitation_list.append(excitation)

  probe = bfdtd.Probe(position = [P_excitation[0],P_excitation[1],P_excitation[2]+D_mum]); probe.name = 'resonance_probe'
  sim.probe_list.append(probe)

  probe = bfdtd.Probe(position = P_excitation); probe.name = 'onsignal_probe'
  sim.probe_list.append(probe)

  probe = bfdtd.Probe(position = [P_excitation[0],P_excitation[1],P_excitation[2]+excitation_wavelength_mum/4.]); probe.name = 'resonance_probe'
  sim.probe_list.append(probe)

  #first = 1
  #frequency_vector = [1]

  #F = sim.addFrequencySnapshot(1,P_excitation[0]); F.first = first; F.frequency_vector = frequency_vector
  #F = sim.addFrequencySnapshot(2,P_excitation[1]); F.first = first; F.frequency_vector = frequency_vector
  #F = sim.addFrequencySnapshot(3,P_excitation[2]); F.first = first; F.frequency_vector = frequency_vector
  #F = sim.addTimeSnapshot(1,P_excitation[0]); F.first = first
  #F = sim.addTimeSnapshot(2,P_excitation[0]); F.first = first
  #F = sim.addTimeSnapshot(3,P_excitation[0]); F.first = first

  # define mesh
  sim.autoMeshGeometry(meshing_factor = excitation_wavelength_mum/4.)

  # write sim
  sim.writeAll(args.DSTDIR+os.sep+BASENAME, BASENAME)
  GEOshellscript(args.DSTDIR+os.sep+BASENAME+os.sep+BASENAME+'.sh', BASENAME,'$HOME/bin/fdtd', '$JOBDIR', WALLTIME = 360)
  print ('iterations = ', sim.flag.iterations)
  print ('Ncells = ', sim.getNcells())

if __name__ == "__main__":
  main()
