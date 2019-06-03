#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import copy
import argparse
import tempfile
import bfdtd
from bfdtd.bfdtd_parser import *
from bfdtd.SpecialTriangularPrism import SpecialTriangularPrism

def createSim(DSTDIR, geom):
  Lambda = 0.637
  
  sim = BFDTDobject()
  sim.boundaries.setBoundaryConditionsToPML()
  
  sim.flag.iterations = 65400
  #sim.flag.iterations = 30000
  #sim.flag.iterations = 1000
  #sim.flag.iterations = 10

  n = 2.4
  #height = 5*Lambda/n
  #radius = 0.5*Lambda/n
  height = 1
  radius = 10

  sim.box.lower = [0,0,0]
  sim.box.upper = [height+4*Lambda,2*radius+1*Lambda,2*radius+1*Lambda]
  P_centre = sim.box.getCentro()
    
  ######################################
  # GEOMETRY
  bulk_block = bfdtd.Block()
  bulk_block.lower = sim.box.lower
  bulk_block.upper = sim.box.upper
  bulk_block.setRefractiveIndex(2.4)

  block = bfdtd.Block()
  block.lower = [ P_centre[0]-0.5*height, P_centre[1]-radius, P_centre[2]-radius ]
  block.upper = [ P_centre[0]+0.5*height, P_centre[1]+radius, P_centre[2]+radius ]
  block.setRefractiveIndex(2.4)

  prism = SpecialTriangularPrism()
  prism.lower = [ 0, 0, 0 ]
  prism.upper = [ height, 2*3./2.*radius*1.0/numpy.sqrt(3), 3./2.*radius ]
  prism.orientation = [2,0,1]
  prism.setRefractiveIndex(2.4)
  prism.NvoxelsX = 30
  prism.NvoxelsY = 30
  prism.NvoxelsZ = 30
  prism.setGeoCentre(sim.box.getCentro())

  prism_block = bfdtd.Block()
  #prism_block.lower = [ P_centre[0]-0.5*height, P_centre[1]-0.5*radius, P_centre[2]-numpy.sqrt(3.0)/2.0*radius ]
  #prism_block.upper = [ P_centre[0]+0.5*height, P_centre[1]+radius, P_centre[2]+numpy.sqrt(3.0)/2.0*radius ]
  prism_block.lower = prism.lower
  prism_block.upper = prism.upper
  prism_block.setRefractiveIndex(2.4)
  
  vertices = numpy.zeros([8,3])
  
  distorted_0 = bfdtd.Distorted()
  vertices[0] = P_centre + numpy.array([ -0.5*height, -numpy.sqrt(3)/2.*radius,      radius ])
  vertices[1] = P_centre + numpy.array([  0.5*height, -numpy.sqrt(3)/2.*radius,      radius ])
  vertices[2] = P_centre + numpy.array([  0.5*height,              -numpy.sqrt(3)/2.*radius, -0.5*radius ])
  vertices[3] = P_centre + numpy.array([ -0.5*height,              -numpy.sqrt(3)/2.*radius, -0.5*radius ])
  vertices[4] = P_centre + numpy.array([ -0.5*height,               numpy.sqrt(3)/2.*radius, -0.5*radius ])
  vertices[5] = P_centre + numpy.array([  0.5*height,               numpy.sqrt(3)/2.*radius, -0.5*radius ])
  vertices[6] = P_centre + numpy.array([  0.5*height,  numpy.sqrt(3)/2.*radius,      radius ])
  vertices[7] = P_centre + numpy.array([ -0.5*height,  numpy.sqrt(3)/2.*radius,      radius ])
  distorted_0.setVerticesAbsolute(vertices)
  distorted_0.setRefractiveIndex(2.4)

  distorted_1 = bfdtd.Distorted()
  vertices[0] = P_centre + numpy.array([ -0.5*height, -numpy.sqrt(3)/2.*radius,      radius ])
  vertices[1] = P_centre + numpy.array([  0.5*height-3./2.*radius, -numpy.sqrt(3)/2.*radius,      radius ])
  vertices[2] = P_centre + numpy.array([  0.5*height,              -numpy.sqrt(3)/2.*radius, -0.5*radius ])
  vertices[3] = P_centre + numpy.array([ -0.5*height,              -numpy.sqrt(3)/2.*radius, -0.5*radius ])
  vertices[4] = P_centre + numpy.array([ -0.5*height,               numpy.sqrt(3)/2.*radius, -0.5*radius ])
  vertices[5] = P_centre + numpy.array([  0.5*height,               numpy.sqrt(3)/2.*radius, -0.5*radius ])
  vertices[6] = P_centre + numpy.array([  0.5*height-3./2.*radius,  numpy.sqrt(3)/2.*radius,      radius ])
  vertices[7] = P_centre + numpy.array([ -0.5*height,  numpy.sqrt(3)/2.*radius,      radius ])
  distorted_1.setVerticesAbsolute(vertices)
  distorted_1.setRefractiveIndex(2.4)

  distorted_2 = bfdtd.Distorted()
  vertices[0] = P_centre + numpy.array([ -0.5*height+3./2.*radius, -numpy.sqrt(3)/2.*radius,      radius ])
  vertices[1] = P_centre + numpy.array([  0.5*height, -numpy.sqrt(3)/2.*radius,      radius ])
  vertices[2] = P_centre + numpy.array([  0.5*height,              -numpy.sqrt(3)/2.*radius, -0.5*radius ])
  vertices[3] = P_centre + numpy.array([ -0.5*height,              -numpy.sqrt(3)/2.*radius, -0.5*radius ])
  vertices[4] = P_centre + numpy.array([ -0.5*height,               numpy.sqrt(3)/2.*radius, -0.5*radius ])
  vertices[5] = P_centre + numpy.array([  0.5*height,               numpy.sqrt(3)/2.*radius, -0.5*radius ])
  vertices[6] = P_centre + numpy.array([  0.5*height,  numpy.sqrt(3)/2.*radius,      radius ])
  vertices[7] = P_centre + numpy.array([ -0.5*height+3./2.*radius,  numpy.sqrt(3)/2.*radius,      radius ])
  distorted_2.setVerticesAbsolute(vertices)
  distorted_2.setRefractiveIndex(2.4)

  distorted_3 = bfdtd.Distorted()
  vertices[0] = P_centre + numpy.array([ -0.5*height+3./2.*radius, -numpy.sqrt(3)/2.*radius,      radius ])
  vertices[1] = P_centre + numpy.array([  0.5*height-3./2.*radius, -numpy.sqrt(3)/2.*radius,      radius ])
  vertices[2] = P_centre + numpy.array([  0.5*height,              -numpy.sqrt(3)/2.*radius, -0.5*radius ])
  vertices[3] = P_centre + numpy.array([ -0.5*height,              -numpy.sqrt(3)/2.*radius, -0.5*radius ])
  vertices[4] = P_centre + numpy.array([ -0.5*height,               numpy.sqrt(3)/2.*radius, -0.5*radius ])
  vertices[5] = P_centre + numpy.array([  0.5*height,               numpy.sqrt(3)/2.*radius, -0.5*radius ])
  vertices[6] = P_centre + numpy.array([  0.5*height-3./2.*radius,  numpy.sqrt(3)/2.*radius,      radius ])
  vertices[7] = P_centre + numpy.array([ -0.5*height+3./2.*radius,  numpy.sqrt(3)/2.*radius,      radius ])
  distorted_3.setVerticesAbsolute(vertices)
  distorted_3.setRefractiveIndex(2.4)

  distorted_4 = bfdtd.Distorted()
  vertices[0] = P_centre + numpy.array([ -0.5*height, 0,      radius ])
  vertices[1] = P_centre + numpy.array([  0.5*height, 0,      radius ])
  vertices[2] = P_centre + numpy.array([  0.5*height, -numpy.sqrt(3)/2.*radius, -0.5*radius ])
  vertices[3] = P_centre + numpy.array([ -0.5*height, -numpy.sqrt(3)/2.*radius, -0.5*radius ])
  vertices[4] = P_centre + numpy.array([ -0.5*height,  numpy.sqrt(3)/2.*radius, -0.5*radius ])
  vertices[5] = P_centre + numpy.array([  0.5*height,  numpy.sqrt(3)/2.*radius, -0.5*radius ])
  vertices[6] = P_centre + numpy.array([  0.5*height, 0,      radius ])
  vertices[7] = P_centre + numpy.array([ -0.5*height, 0,      radius ])
  distorted_4.setVerticesAbsolute(vertices)
  distorted_4.setRefractiveIndex(2.4)

  distorted_5 = bfdtd.Distorted()
  vertices[0] = P_centre + numpy.array([ -0.5*height,              0,      radius ])
  vertices[1] = P_centre + numpy.array([  0.5*height-3./2.*radius, 0,      radius ])
  vertices[2] = P_centre + numpy.array([  0.5*height,              -numpy.sqrt(3)/2.*radius, -0.5*radius ])
  vertices[3] = P_centre + numpy.array([ -0.5*height,              -numpy.sqrt(3)/2.*radius, -0.5*radius ])
  vertices[4] = P_centre + numpy.array([ -0.5*height,               numpy.sqrt(3)/2.*radius, -0.5*radius ])
  vertices[5] = P_centre + numpy.array([  0.5*height,               numpy.sqrt(3)/2.*radius, -0.5*radius ])
  vertices[6] = P_centre + numpy.array([  0.5*height-3./2.*radius, 0,      radius ])
  vertices[7] = P_centre + numpy.array([ -0.5*height,              0,      radius ])
  distorted_5.setVerticesAbsolute(vertices)
  distorted_5.setRefractiveIndex(2.4)

  distorted_6 = bfdtd.Distorted()
  vertices[0] = P_centre + numpy.array([ -0.5*height+3./2.*radius, 0,      radius ])
  vertices[1] = P_centre + numpy.array([  0.5*height,              0,      radius ])
  vertices[2] = P_centre + numpy.array([  0.5*height,              -numpy.sqrt(3)/2.*radius, -0.5*radius ])
  vertices[3] = P_centre + numpy.array([ -0.5*height,              -numpy.sqrt(3)/2.*radius, -0.5*radius ])
  vertices[4] = P_centre + numpy.array([ -0.5*height,               numpy.sqrt(3)/2.*radius, -0.5*radius ])
  vertices[5] = P_centre + numpy.array([  0.5*height,               numpy.sqrt(3)/2.*radius, -0.5*radius ])
  vertices[6] = P_centre + numpy.array([  0.5*height,              0,      radius ])
  vertices[7] = P_centre + numpy.array([ -0.5*height+3./2.*radius, 0,      radius ])
  distorted_6.setVerticesAbsolute(vertices)
  distorted_6.setRefractiveIndex(2.4)

  distorted_7 = bfdtd.Distorted()
  vertices[0] = P_centre + numpy.array([ -0.5*height+3./2.*radius,  0,      radius ])
  vertices[1] = P_centre + numpy.array([  0.5*height-3./2.*radius,  0,      radius ])
  vertices[2] = P_centre + numpy.array([  0.5*height,               -numpy.sqrt(3)/2.*radius, -0.5*radius ])
  vertices[3] = P_centre + numpy.array([ -0.5*height,               -numpy.sqrt(3)/2.*radius, -0.5*radius ])
  vertices[4] = P_centre + numpy.array([ -0.5*height,                numpy.sqrt(3)/2.*radius, -0.5*radius ])
  vertices[5] = P_centre + numpy.array([  0.5*height,                numpy.sqrt(3)/2.*radius, -0.5*radius ])
  vertices[6] = P_centre + numpy.array([  0.5*height-3./2.*radius,  0,      radius ])
  vertices[7] = P_centre + numpy.array([ -0.5*height+3./2.*radius,  0,      radius ])
  distorted_7.setVerticesAbsolute(vertices)
  distorted_7.setRefractiveIndex(2.4)
  
  cylinder_base = bfdtd.Cylinder()
  cylinder_base.setRefractiveIndex(1)
  rcyl = 0.5*Lambda/(4.*1.)
  intercyl = 0.5*radius
  cylinder_base.outer_radius = rcyl
  cylinder_base.height = 2*radius
  cylinder_list = []
  for i in range(6):
    cylinder_list.append(copy.deepcopy(cylinder_base))
    cylinder_list[i].centre = P_centre + numpy.array([Lambda,0,0]) - numpy.array([radius+rcyl+i*(intercyl+2*rcyl),0,0])
  
  #sim.geometry_object_list.extend([bulk_block, block, prism, prism_block, distorted_0, distorted_1, distorted_2, distorted_3, distorted_4, distorted_5, distorted_6, distorted_7])
  #sim.geometry_object_list.extend([bulk_block, block, prism, prism_block])
  sim.geometry_object_list.extend([bulk_block, block])
  #sim.geometry_object_list.extend([block])
  #sim.geometry_object_list.extend(cylinder_list)
  ######################################
  
  P_input = P_centre - numpy.array([0.5*height+0.5*Lambda,0,0])
  P_input_excitation = P_input - numpy.array([0.5*Lambda,0,0])
  P_output = P_centre + numpy.array([0.5*height+0.5*Lambda,0,0])
  
  (A1_global,B1_global,C1_global,A2_global,B2_global,C2_global) = prism.getGlobalEnvelopPoints()
  triangle_input = (A1_global+B1_global+C1_global)/3.0
  triangle_output = (A2_global+B2_global+C2_global)/3.0
  
  P_input_top = numpy.array([triangle_input[0],triangle_input[1],prism.upper[2]-0.1*Lambda])
  P_output_top = numpy.array([triangle_output[0],triangle_output[1],prism.upper[2]-0.1*Lambda])

  P_input_bottom = numpy.array([triangle_input[0],triangle_input[1],prism.lower[2]+0.1*Lambda])
  P_output_bottom = numpy.array([triangle_output[0],triangle_output[1],prism.lower[2]+0.1*Lambda])
  
  e_input = ExcitationWithGaussianTemplate()
  e_input.name = 'input'
  e_input.centre = P_input_excitation
  e_input.sigma_x = 0.1*radius
  e_input.sigma_y = 0.1*radius
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
  sim.addModeFilteredProbe('x',P_input[0])

  probe_output = bfdtd.Probe(position = P_output); probe_output.name = 'probe_output'
  sim.probe_list.append(probe_output)
  sim.addModeFilteredProbe('x',P_output[0])
  
  F = sim.addFrequencySnapshot('x',P_input[0]); F.first = 10; F.frequency_vector = [get_c0()/Lambda]
  F = sim.addFrequencySnapshot('y',P_input[1]); F.first = 10; F.frequency_vector = [get_c0()/Lambda]
  F = sim.addFrequencySnapshot('z',P_input[2]); F.first = 10; F.frequency_vector = [get_c0()/Lambda]

  T = sim.addTimeSnapshot('x',P_input[0]); T.first = 10; T.repetition = 10;
  T = sim.addTimeSnapshot('y',P_input[1]); T.first = 10; T.repetition = 10;
  T = sim.addTimeSnapshot('z',P_input[2]); T.first = 10; T.repetition = 10;

  #probe_output = Probe(position = P_output); probe_output.name = 'probe_output'
  #sim.probe_list.append(probe_output)
  #sim.addModeFilteredProbe('x',P_output[0])

  #probe_input_top = Probe(position = P_input_top); probe_input_top.name = 'probe_input_top'
  #sim.probe_list.append(probe_input_top)
  #sim.addModeFilteredProbe('z',P_input_top[2])
  
  #probe_output_top = Probe(position = P_output_top); probe_output_top.name = 'probe_output_top'
  #sim.probe_list.append(probe_output_top)
  #sim.addModeFilteredProbe('z',P_output_top[2])

  #probe_input_bottom = Probe(position = P_input_bottom); probe_input_bottom.name = 'probe_input_bottom'
  #sim.probe_list.append(probe_input_bottom)
  #sim.addModeFilteredProbe('z',P_input_bottom[2])
  
  #probe_output_bottom = Probe(position = P_output_bottom); probe_output_bottom.name = 'probe_output_bottom'
  #sim.probe_list.append(probe_output_bottom)
  #sim.addModeFilteredProbe('z',P_output_bottom[2])
  
  # define mesh
  a = 10
  sim.autoMeshGeometry(Lambda/a)
  #MAXCELLS=8000000;
  MAXCELLS=1000000;
  while(sim.getNcells()>MAXCELLS and a>1):
    a = a-1
    sim.autoMeshGeometry(Lambda/a)
  
  print('sim.getNcells() = '+str(sim.getNcells()))
  if sim.getNcells()>MAXCELLS:
    sys.exit(-1)

  if geom=='empty':
    print(geom)
    sim.geometry_object_list = []
  elif geom=='bulk':
    print(geom)
    sim.geometry_object_list = [bulk_block]
  elif geom=='block':
    print(geom)
    sim.geometry_object_list = [block]
  elif geom=='prism':
    print(geom)
    sim.geometry_object_list = [prism]
  elif geom=='prism_block':
    print(geom)
    sim.geometry_object_list = [prism_block]
  elif geom=='distorted_0':
    print(geom)
    sim.geometry_object_list = [distorted_0]
  elif geom=='distorted_1':
    print(geom)
    sim.geometry_object_list = [distorted_1]
  elif geom=='distorted_2':
    print(geom)
    sim.geometry_object_list = [distorted_2]
  elif geom=='distorted_3':
    print(geom)
    sim.geometry_object_list = [distorted_3]
  elif geom=='distorted_4':
    print(geom)
    sim.geometry_object_list = [distorted_4]
  elif geom=='distorted_5':
    print(geom)
    sim.geometry_object_list = [distorted_5]
  elif geom=='distorted_6':
    print(geom)
    sim.geometry_object_list = [distorted_6]
  elif geom=='distorted_7':
    print(geom)
    sim.geometry_object_list = [distorted_7]
  elif geom=='cylinder':
    print(geom)
    sim.geometry_object_list = [block]
    sim.geometry_object_list.extend(cylinder_list)
  else:
    print('unknown geom: '+geom)
    sys.exit(-1)

  BASENAME = 'transmission'
  sim.writeAll(DSTDIR+os.path.sep+geom,BASENAME)
  sim.writeShellScript(DSTDIR+os.path.sep+geom+os.path.sep+BASENAME+'.sh', EXE='/space/ANONYMIZED/home_rama/bin/fdtd64_2008', WORKDIR='$JOBDIR', WALLTIME=12)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('DSTDIR', default=tempfile.gettempdir(), nargs='?')
  args = parser.parse_args()  
  print(args.DSTDIR)

  if not os.path.isdir(args.DSTDIR):
    os.mkdir(args.DSTDIR)
  #for geom in ['empty','bulk','block','prism','prism_block','distorted_0','distorted_1','distorted_2','distorted_3','distorted_4','distorted_5','distorted_6','distorted_7','cylinder']:
  for geom in ['empty','block']:
    createSim(args.DSTDIR, geom)

if __name__ == "__main__":
  main()
