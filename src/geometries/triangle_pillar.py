#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import numpy
import shutil
import argparse
import tempfile
import bfdtd
import constants
#from meshing.meshing import subGridMultiLayer
#from bfdtd.triangular_prism import TriangularPrism
from bfdtd.SpecialTriangularPrism import SpecialTriangularPrism
#from bfdtd.bfdtd_parser import *
#from utilities.common import *
#from bfdtd.excitationTemplate import *
from utilities.bfdtd_utilities import efficiency_run
from bfdtd.excitation_utilities import QuadrupleExcitation
from bfdtd.bristolFDTD_generator_functions import GEOshellscript

def prismPillar(DSTDIR, BASENAME, pos, exc):
  sim = bfdtd.BFDTDobject()
  
  # constants
  n_air = 1; n_diamond = 2.4
  Lambda_mum = 0.637
  delta = Lambda_mum/(10*n_diamond)
  freq = constants.get_c0()/Lambda_mum
  k=4; radius = k*Lambda_mum/(4*n_diamond)
  Nbottom = 3; Ntop = 3
  h_air = Lambda_mum/(4*n_air)
  h_diamond = Lambda_mum/(4*n_diamond)
  h_cavity = Lambda_mum/(n_diamond)
  height = Nbottom*(h_air+h_diamond) + h_cavity + Ntop*(h_air+h_diamond)
  print('height = ',height)
  buffer = 0.05
  FullBox_upper = [ height+2*buffer, 2*(radius+buffer), 2*(radius+buffer) ]
  
  P_centre = [ buffer + Nbottom*(h_air+h_diamond) + 0.5*h_cavity, 0.5*FullBox_upper[1], 0.5*FullBox_upper[2] ]
  
  # define flag
  sim.flag.iterations = 100000
  #sim.flag.iterations = 1
  
  # define boundary conditions
  sim.boundaries.Xpos_bc = 2
  sim.boundaries.Ypos_bc = 2 #1
  sim.boundaries.Zpos_bc = 2
  
  # define box
  sim.box.lower = [0,0,0]
  if sim.boundaries.Ypos_bc == 2:
    sim.box.upper = FullBox_upper
  else:
    sim.box.upper = [ FullBox_upper[0], 0.5*FullBox_upper[1], FullBox_upper[2] ]
  
  #P_centre = sim.box.getCenter()
  
  ## define geometry
  
  #prism = TriangularPrism()
  prism = SpecialTriangularPrism()
  prism.lower = [ 0, 0, 0 ]
  prism.upper = [ height, 2*3./2.*radius*1.0/numpy.sqrt(3), 3./2.*radius ]
  #prism.lower = [1,1,1]
  #prism.upper = [1,10,1]
  #prism.lower = [1,2,3]
  #prism.upper = [3,7,13]
  prism.orientation = [2,0,1]
  #prism.orientation = [2,1,0]
  prism.permittivity = pow(n_diamond,2)
  prism.conductivity = 0
  prism.NvoxelsX = 30
  prism.NvoxelsY = 30
  prism.NvoxelsZ = 30
  
  prismPos = numpy.copy(sim.box.getCentro())
  if sim.boundaries.Ypos_bc == 1:
    prismPos[1] = sim.box.upper[1]
  prism.setGeoCentre(prismPos)
  #sim.probe_list.append(Probe(position = prism.getGeoCentre()))
  #prism.setGeoCentre([0,0,0])
  #sim.probe_list.append(Probe(position = prism.getGeoCentre()))
  
  sim.geometry_object_list.append(prism)
  
  buffersize=10*delta
  n_meshblock = 2.4
  
  # X buffers
  block = bfdtd.Block()
  block.setRefractiveIndex(n_meshblock)  
  block.setLowerAbsolute([ prism.lower[0]-buffersize, prism.lower[1], prism.lower[2] ])
  block.setUpperAbsolute([ prism.lower[0], prism.upper[1], prism.upper[2] ])
  sim.mesh_object_list.append(block)
  
  block = bfdtd.Block()
  block.setRefractiveIndex(n_meshblock)  
  block.setLowerAbsolute([ prism.upper[0], prism.lower[1], prism.lower[2] ])
  block.setUpperAbsolute([ prism.upper[0]+buffersize, prism.upper[1], prism.upper[2] ])
  sim.mesh_object_list.append(block)
  
  # Y buffers
  block = bfdtd.Block()
  block.setRefractiveIndex(n_meshblock)
  block.setLowerAbsolute([ prism.lower[0], prism.lower[1]-buffersize, prism.lower[2] ])
  block.setUpperAbsolute([ prism.upper[0], prism.lower[1], prism.upper[2] ])
  sim.mesh_object_list.append(block)
  
  block = bfdtd.Block()
  block.setRefractiveIndex(n_meshblock)
  block.setLowerAbsolute([ prism.lower[0], prism.upper[1], prism.lower[2] ])
  block.setUpperAbsolute([ prism.upper[0], prism.upper[1]+buffersize, prism.upper[2] ])
  sim.mesh_object_list.append(block)
  
  # Z buffers
  block = bfdtd.Block()
  block.setRefractiveIndex(n_meshblock)
  block.setLowerAbsolute([ prism.lower[0], prism.lower[1], prism.lower[2]-buffersize ])
  block.setUpperAbsolute([ prism.upper[0], prism.upper[1], prism.lower[2] ])
  sim.mesh_object_list.append(block)
  
  block = bfdtd.Block()
  block.setRefractiveIndex(n_meshblock)
  block.setLowerAbsolute([ prism.lower[0], prism.lower[1], prism.upper[2] ])
  block.setUpperAbsolute([ prism.upper[0], prism.upper[1], prism.upper[2]+buffersize ])
  sim.mesh_object_list.append(block)
  
  #sim.autoMeshGeometry(0.637/10)
  #print sim.getNcells()
  
  ##################################
  # prepare some points
  
  (A1_global,B1_global,C1_global,A2_global,B2_global,C2_global) = prism.getGlobalEnvelopPoints()
  #sim.probe_list.append(Probe(position = A1_global))
  #sim.probe_list.append(Probe(position = B1_global))
  #sim.probe_list.append(Probe(position = C1_global))
  #sim.probe_list.append(Probe(position = A2_global))
  #sim.probe_list.append(Probe(position = B2_global))
  #sim.probe_list.append(Probe(position = C2_global))
  
  bottom_centre = (A1_global+B1_global+C1_global)/3.0
  print('bottom_centre = ',bottom_centre)
  top_centre = (A2_global+B2_global+C2_global)/3.0
  
  P_centre = prism.getGeoCentre()
  
  template_radius = prism.getInscribedSquarePlaneRadius(P_centre)
  print('template_radius = ',template_radius)
  
  P3 = numpy.array(P_centre)
  
  prism_height = prism.upper[0] - prism.lower[0]
  prism_bottom = prism.lower[1]
  
  P1 = numpy.copy(bottom_centre)
  P1[0] = A1_global[0] - delta
  P2 = numpy.copy(bottom_centre)
  P2[2] = A1_global[2] - delta
  
  P4 = numpy.copy(top_centre)
  P4[2] = A2_global[2] - delta
  P5 = numpy.copy(top_centre)
  P5[0] = A2_global[0] + delta
  
  sim.autoMeshGeometry(0.637/10)
  # define excitation
  ################
  if sim.boundaries.Ypos_bc == 2:
    Ysym = False
  else:
    Ysym = True

  if pos == 0:
    QuadrupleExcitation(Ysym, sim, P1, 'x', delta, template_radius, freq, exc)
  elif pos == 1:
    QuadrupleExcitation(Ysym, sim, P2+2*delta*numpy.array([0,0,1]), 'z', delta,template_radius, freq, exc)
  elif pos == 2:
    QuadrupleExcitation(Ysym, sim, P3, 'x', delta, template_radius, freq, exc)
  elif pos == 3:
    QuadrupleExcitation(Ysym, sim, P4, 'z', delta, template_radius, freq, exc)
  elif pos == 4:
    QuadrupleExcitation(Ysym, sim, P5, 'x', delta, template_radius, freq, exc)
  else:
    raise Exception('Invalid value for pos.')
  ################
  
  # create template
  #x_min = 0.0
  #x_max = 4.00
  #y_min = 0.0
  #y_max = 4.00
  #step_x = 2.00e-2
  #step_y = 2.00e-1
  #x_list = arange(x_min,x_max,step_x)
  #y_list = arange(y_min,y_max,step_y)
  
  
  #probe_X = [ P_centre[0]-(0.5*height+delta), P_centre[0], P_centre[0]+(0.5*height+delta) ]
  
  #if sim.boundaries.Ypos_bc == 2:
    #probe_Y = [ P_centre[1] ]
  #else:
    #probe_Y = [ P_centre[1]-delta ]
  
  #probe_Z = [ P_centre[2]-radius-delta, P_centre[2] ]
  
  #for x in probe_X:
    #for y in probe_Y:
      #for z in probe_Z:
        #probe = Probe(position = [ x,y,z ])
        #sim.probe_list.append(probe)
  
  # define frequency snapshots and probes
  first = min(65400,sim.flag.iterations)
  frequency_vector = [freq]
  
  P1_m = numpy.copy(P1)
  P2_m = numpy.copy(P2)
  P3_m = numpy.copy(P3)
  P4_m = numpy.copy(P4)
  P5_m = numpy.copy(P5)
  if sim.boundaries.Ypos_bc == 1:
    voxeldim_global = prism.getVoxelDimensions()
    P1_m[1] = P1_m[1] - voxeldim_global[1]
    P2_m[1] = P2_m[1] - voxeldim_global[1]
    P3_m[1] = P3_m[1] - voxeldim_global[1]
    P4_m[1] = P4_m[1] - voxeldim_global[1]
    P5_m[1] = P5_m[1] - voxeldim_global[1]
  
  Plist = [P1_m,P2_m,P3_m,P4_m,P5_m]
  for idx in range(len(Plist)):
    P = Plist[idx]
    F = sim.addFrequencySnapshot('x', P[0]); F.first = first; F.frequency_vector = frequency_vector; F.name='x_'+str(idx)
    F = sim.addFrequencySnapshot('y', P[1]); F.first = first; F.frequency_vector = frequency_vector; F.name='y_'+str(idx)
    F = sim.addFrequencySnapshot('z', P[2]); F.first = first; F.frequency_vector = frequency_vector; F.name='z_'+str(idx)
    probe = bfdtd.Probe(position = P); probe.name = 'p_'+str(idx)
    sim.probe_list.append(probe)
  
  #F = sim.addFrequencySnapshot(1,P_centre[0]); F.first = first; F.frequency_vector = frequency_vector
  #if sim.boundaries.Ypos_bc == 2:
    #F = sim.addFrequencySnapshot(2,P_centre[1]); F.first = first; F.frequency_vector = frequency_vector
  #else:
    #F = sim.addFrequencySnapshot(2,P_centre[1]-delta); F.first = first; F.frequency_vector = frequency_vector
  #F = sim.addFrequencySnapshot(3,P_centre[2]); F.first = first; F.frequency_vector = frequency_vector
  
  F = sim.addBoxFrequencySnapshots(); F.first = first; F.frequency_vector = frequency_vector
  
  L = [prism.lower[0], prism.lower[1], prism.lower[2]]-delta*numpy.array([1,1,1])
  U = [prism.upper[0], prism.upper[1], prism.upper[2]]+delta*numpy.array([1,1,1])
  F = bfdtd.FrequencySnapshot()
  F.setName('Efficiency box frequency snapshot')
  F.setExtension(L, U)
  F.setFirst(first)
  F.setFrequencies(frequency_vector)
  sim.appendSnapshot(F)

  print('==========================================')
  L = P2 - template_radius*numpy.array([1,1,0])
  U = P2 + template_radius*numpy.array([1,1,0])
  print(('L=',L))
  print(('U=',U))
  F = bfdtd.FrequencySnapshot()
  F.setName('Efficiency input frequency snapshot')
  F.setExtension(L, U)
  F.setPlaneOrientationZ()
  F.setFirst(first)
  F.setFrequencies(frequency_vector)
  sim.appendSnapshot(F)
  print('==========================================')

  print('==========================================')
  L = P4 - template_radius*numpy.array([1,1,0])
  U = P4 + template_radius*numpy.array([1,1,0])
  print(('L=',L))
  print(('U=',U))
  F = bfdtd.FrequencySnapshot()
  F.setName('Efficiency output frequency snapshot')
  F.setExtension(L, U)
  F.setPlaneOrientationZ()
  F.setFirst(first)
  F.setFrequencies(frequency_vector)
  sim.appendSnapshot(F)
  print('==========================================')
  
  F = sim.addTimeSnapshot('z', P1[2]); F.first = first
  
  ## define mesh
  #sim.addMeshingBox(lower,upper,)
  #sim.autoMeshGeometry(0.637/10)
  
  # write
  #DSTDIR = os.getenv('DATADIR')
  #DSTDIR = os.getenv('TESTDIR')
  #DSTDIR = os.getenv('TESTDIR')+os.sep+'triangle_pillar'
  #DSTDIR = os.getenv('DATADIR')+os.sep+'triangle_pillar'
  dest = DSTDIR+os.sep+BASENAME
  sim.writeAll(dest, BASENAME)
  GEOshellscript(dest+os.sep+BASENAME+'.sh', BASENAME,'$HOME/bin/fdtd', '$JOBDIR', WALLTIME = 360)
  newdest = dest+os.sep+'nogeometry'
  efficiency_run(dest,newdest)
  GEOshellscript(newdest+os.sep+BASENAME+'.sh', BASENAME,'$HOME/bin/fdtd', '$JOBDIR', WALLTIME = 360)

  template = dest+os.sep+'template.dat'
  try:
    shutil.copyfile(template,newdest+os.sep+'template.dat')
  except IOError as e:
    print('File not found : ' + template)
  
  #GEOshellscript_advanced(DSTDIR+os.sep+BASENAME+os.sep+BASENAME+'.sh', BASENAME, getProbeColumnFromExcitation(excitation.E),'$HOME/bin/fdtd', '$JOBDIR', WALLTIME = 360)
  print(sim.getNcells())

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('DSTDIR', default=tempfile.gettempdir(), nargs='?')
  args = parser.parse_args()
  print(args)

  DSTDIR = args.DSTDIR
  if not os.path.isdir(DSTDIR):
      os.mkdir(DSTDIR)

  #for pos in range(5):
    #for exc in range(4):
      #prismPillar(DSTDIR,'triangle_pillar_'+str(pos)+'_'+str(exc),pos,exc)
  #pos=0
  #exc=0
  #prismPillar('triangle_pillar_'+str(pos)+'_'+str(exc),pos,exc)

  pos=1
  #exc=3
  for exc in range(4):
    prismPillar(DSTDIR, 'triangle_pillar_'+str(pos)+'_'+str(exc), pos, exc)

if __name__ == "__main__":
  main()
