#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import tempfile
import bfdtd
from bfdtd.bfdtd_parser import *

def createSim(DSTDIR):
  Lambda = 0.637
  
  sim = BFDTDobject()
  
  sim.flag.iterations = 65400
  
  sim.box.lower = [0,0,0]
  sim.box.upper = [12*Lambda,3*Lambda,3*Lambda]
  P_centre = sim.box.getCentro()
  
  height = 10*Lambda
  radius = 0.5*Lambda
  
  block = bfdtd.Block()
  block.lower = [ P_centre[0]-0.5*height, P_centre[1]-radius, P_centre[2]-radius ]
  block.upper = [ P_centre[0]+0.5*height, P_centre[1]+radius, P_centre[2]+radius ]
  block.setRefractiveIndex(2.4)
  sim.geometry_object_list.append(block)
  
  P_input = P_centre - numpy.array([4*Lambda,0,0])
  P_input_excitation = P_input - numpy.array([0.1*Lambda,0,0])
  P_output = P_centre + numpy.array([4*Lambda,0,0])
  
  e_input = ExcitationWithGaussianTemplate()
  e_input.name = 'input'
  e_input.centre = P_input_excitation
  e_input.sigma_x = radius
  e_input.sigma_y = radius
  e_input.amplitude = 1
  e_input.plane_direction = 'x'
  e_input.excitation_direction = ['Eyre']
  e_input.frequency = get_c0()/Lambda
  e_input.template_filename = 'input.dat'
  e_input.setExtension(P_input_excitation - numpy.array([0,radius,radius]), P_input_excitation + numpy.array([0,radius,radius]))
  sim.excitation_list.append(e_input)
  
  # measurement objects
  probe_input = bfdtd.Probe(position = P_input); probe_input.name = 'probe_input'
  sim.probe_list.append(probe_input)
  
  probe_output = bfdtd.Probe(position = P_output); probe_output.name = 'probe_output'
  sim.probe_list.append(probe_output)
  
  sim.addModeFilteredProbe('x',P_input[0])
  
  sim.addModeFilteredProbe('x',P_output[0])
  
  # define mesh
  a = 5
  sim.autoMeshGeometry(Lambda/a)
  while(sim.getNcells()>8000000 and a>1):
    a = a-1
    sim.autoMeshGeometry(Lambda/a)
  
  print('sim.getNcells() = '+str(sim.getNcells()))
  if sim.getNcells()>8000000:
    sys.exit(-1)
  
  sim.writeAll(DSTDIR,'transmission')

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('DSTDIR', default=tempfile.gettempdir(), nargs='?')
  args = parser.parse_args()  
  print(args.DSTDIR)

  if not os.path.isdir(args.DSTDIR):
    os.mkdir(args.DSTDIR)
  #for geom in ['empty','bulk','block','prism','prism_block','distorted_0','distorted_1','distorted_2','distorted_3','distorted_4','distorted_5','distorted_6','distorted_7','cylinder']:
  createSim(args.DSTDIR)

if __name__ == "__main__":
  main()
