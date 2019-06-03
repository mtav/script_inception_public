#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import copy
import numpy
import argparse
import tempfile
import bfdtd
import constants
from numpy import array
from bfdtd.bristolFDTD_generator_functions import GEOshellscript
#from bfdtd.bfdtd_parser import *
#from utilities.common import *
#from meshing.subGridMultiLayer import *
#from bfdtd.triangular_prism import TriangularPrism
#from bfdtd.SpecialTriangularPrism import SpecialTriangularPrism
#from bfdtd.excitationTemplate import *
#from bfdtd.excitation_utilities import *

def semi_loncar(DSTDIR,BASENAME,pos,exc):
  pillar = bfdtd.BFDTDobject()
  
  # constants
  n_air = 1; n_diamond = 2.4
  Lambda_mum = 0.637
  delta = Lambda_mum/(10*n_diamond)
  freq = constants.get_c0()/Lambda_mum
  cylinder_radius = 0.300
  pillar_radius = 0.500
  inter_centre_distance = 1.111
  h_air = Lambda_mum/(4*n_air)
  h_diamond = Lambda_mum/(4*n_diamond)
  h_cavity = Lambda_mum/(n_diamond)
  pillar_height = 7 + 3*inter_centre_distance
  print('pillar_height = {}'.format(pillar_height))
  buffer = 0.05
  FullBox_upper = [ pillar_height+2*buffer, 2*(pillar_radius+buffer), 2*(pillar_radius+buffer) ]
  
  P_centre = [ buffer + 0.5*pillar_height, 0.5*FullBox_upper[1], 0.5*FullBox_upper[2] ]
  pillar_bottom_centre = P_centre - array([0.5*pillar_height,0,0])
  
  # define flag
  pillar.flag.iterations = 100000
  #pillar.flag.iterations = 1
  
  # define boundary conditions
  pillar.boundaries.Xpos_bc = 2
  pillar.boundaries.Ypos_bc = 2 #1
  pillar.boundaries.Zpos_bc = 2
  
  # define box
  pillar.box.lower = [0,0,0]
  if pillar.boundaries.Ypos_bc == 2:
    pillar.box.upper = FullBox_upper
  else:
    pillar.box.upper = [ FullBox_upper[0], 0.5*FullBox_upper[1], FullBox_upper[2] ]
  
  #P_centre = pillar.box.getCenter()
  
  ## define geometry

  block = bfdtd.Block()
  block.lower = [ P_centre[0]-0.5*pillar_height, P_centre[1]-pillar_radius, P_centre[2]-pillar_radius ]
  block.upper = [ P_centre[0]+0.5*pillar_height, P_centre[1]+pillar_radius, P_centre[2]+pillar_radius ]
  block.setRefractiveIndex(n_diamond)
  block.conductivity = 0
  pillar.setGeometryObjects([ block ])

  cylinder = bfdtd.Cylinder()
  cylinder.centre = pillar_bottom_centre + array([inter_centre_distance-cylinder_radius,0,0])
  cylinder.outer_radius = 0.5*cylinder_radius
  cylinder.height = 2*pillar_radius
  cylinder.setRefractiveIndex(n_air)
  cylinder.conductivity = 0

  cylinder1 = copy.deepcopy(cylinder)
  cylinder1.centre = cylinder.centre + array([0*inter_centre_distance,0,0])
  cylinder2 = copy.deepcopy(cylinder)
  cylinder2.centre = cylinder.centre + array([1*inter_centre_distance,0,0])
  cylinder3 = copy.deepcopy(cylinder)
  cylinder3.centre = cylinder.centre + array([2*inter_centre_distance,0,0])
  
  pillar.appendGeometryObject(block)
  pillar.appendGeometryObject(cylinder1)
  pillar.appendGeometryObject(cylinder2)
  pillar.appendGeometryObject(cylinder3)
  
  buffersize=10*delta
  n_meshblock = 2.4
  
  # X buffers
  block = bfdtd.Block()
  block.setRefractiveIndex(n_meshblock)
  block.setRelativeConductivity(0)
  block.lower = [ block.getLowerAbsolute()[0]-buffersize, block.getLowerAbsolute()[1], block.getLowerAbsolute()[2] ]
  block.upper = [ block.getLowerAbsolute()[0], block.getUpperAbsolute()[1], block.getUpperAbsolute()[2] ]
  pillar.mesh_object_list.append(block)
  
  block = bfdtd.Block()
  block.setRefractiveIndex(n_meshblock)
  block.setRelativeConductivity(0)
  block.lower = [ block.getUpperAbsolute()[0], block.getLowerAbsolute()[1], block.getLowerAbsolute()[2] ]
  block.upper = [ block.getUpperAbsolute()[0]+buffersize, block.getUpperAbsolute()[1], block.getUpperAbsolute()[2] ]
  pillar.mesh_object_list.append(block)
  
  # Y buffers
  block = bfdtd.Block()
  block.setRefractiveIndex(n_meshblock)
  block.setRelativeConductivity(0)
  block.lower = [ block.getLowerAbsolute()[0], block.getLowerAbsolute()[1]-buffersize, block.getLowerAbsolute()[2] ]
  block.upper = [ block.getUpperAbsolute()[0], block.getLowerAbsolute()[1], block.getUpperAbsolute()[2] ]
  pillar.mesh_object_list.append(block)
  
  block = bfdtd.Block()
  block.setRefractiveIndex(n_meshblock)
  block.setRelativeConductivity(0)
  block.lower = [ block.getLowerAbsolute()[0], block.getUpperAbsolute()[1], block.getLowerAbsolute()[2] ]
  block.upper = [ block.getUpperAbsolute()[0], block.getUpperAbsolute()[1]+buffersize, block.getUpperAbsolute()[2] ]
  pillar.mesh_object_list.append(block)
  
  # Z buffers
  block = bfdtd.Block()
  block.setRefractiveIndex(n_meshblock)
  block.setRelativeConductivity(0)
  block.lower = [ block.getLowerAbsolute()[0], block.getLowerAbsolute()[1], block.getLowerAbsolute()[2]-buffersize ]
  block.upper = [ block.getUpperAbsolute()[0], block.getUpperAbsolute()[1], block.getLowerAbsolute()[2] ]
  pillar.mesh_object_list.append(block)
  
  block = bfdtd.Block()
  block.setRefractiveIndex(n_meshblock)
  block.setRelativeConductivity(0)
  block.lower = [ block.getLowerAbsolute()[0], block.getLowerAbsolute()[1], block.getUpperAbsolute()[2] ]
  block.upper = [ block.getUpperAbsolute()[0], block.getUpperAbsolute()[1], block.getUpperAbsolute()[2]+buffersize ]
  pillar.mesh_object_list.append(block)
  
  #pillar.autoMeshGeometry(0.637/10)
  #print pillar.getNcells()
  
  ##################################
  # prepare some points
  
  #(A1_global,B1_global,C1_global,A2_global,B2_global,C2_global) = block.getGlobalEnvelopPoints()
  #pillar.probe_list.append(Probe(position = A1_global))
  #pillar.probe_list.append(Probe(position = B1_global))
  #pillar.probe_list.append(Probe(position = C1_global))
  #pillar.probe_list.append(Probe(position = A2_global))
  #pillar.probe_list.append(Probe(position = B2_global))
  #pillar.probe_list.append(Probe(position = C2_global))
  
  #bottom_centre = (A1_global+B1_global+C1_global)/3.0
  #print('bottom_centre = ',bottom_centre)
  #top_centre = (A2_global+B2_global+C2_global)/3.0
  
  P_centre = block.getCentro()
  
  #template_radius = block.getInscribedSquarePlaneRadius(P_centre)
  #print('template_radius = ',template_radius)
  
  #P3 = array(P_centre)
  
  #prism_height = block.getUpperAbsolute()[0] - block.getLowerAbsolute()[0]
  #prism_bottom = block.getLowerAbsolute()[1]
  
  #P1 = copy(bottom_centre)
  #P1[0] = A1_global[0] - delta
  #P2 = copy(bottom_centre)
  #P2[2] = A1_global[2] - delta
  
  #P4 = copy(top_centre)
  #P4[2] = A2_global[2] - delta
  #P5 = copy(top_centre)
  #P5[0] = A2_global[0] + delta
  
  #pillar.autoMeshGeometry(0.637/10)
  # define excitation
  ################
  if pillar.boundaries.Ypos_bc == 2:
    Ysym = False
  else:
    Ysym = True

  #if pos == 0:
    #QuadrupleExcitation(Ysym,pillar,P1,'x',delta,template_radius,freq,exc)
  #elif pos == 1:
    #QuadrupleExcitation(Ysym,pillar,P2,'z',delta,template_radius,freq,exc)
  #elif pos == 2:
    #QuadrupleExcitation(Ysym,pillar,P3,'x',delta,template_radius,freq,exc)
  #elif pos == 3:
    #QuadrupleExcitation(Ysym,pillar,P4,'z',delta,template_radius,freq,exc)
  #elif pos == 4:
    #QuadrupleExcitation(Ysym,pillar,P5,'x',delta,template_radius,freq,exc)
  #else:
    #sys.exit(-1)
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
  
  #if pillar.boundaries.Ypos_bc == 2:
    #probe_Y = [ P_centre[1] ]
  #else:
    #probe_Y = [ P_centre[1]-delta ]
  
  #probe_Z = [ P_centre[2]-radius-delta, P_centre[2] ]
  
  #for x in probe_X:
    #for y in probe_Y:
      #for z in probe_Z:
        #probe = Probe(position = [ x,y,z ])
        #pillar.probe_list.append(probe)
  
  # define frequency snapshots and probes
  first = min(65400,pillar.flag.iterations)
  frequency_vector = [freq]
  
  #P1_m = copy(P1)
  #P2_m = copy(P2)
  #P3_m = copy(P3)
  #P4_m = copy(P4)
  #P5_m = copy(P5)
  #if pillar.boundaries.Ypos_bc == 1:
    #voxeldim_global = block.getVoxelDimensions()
    #P1_m[1] = P1_m[1] - voxeldim_global[1]
    #P2_m[1] = P2_m[1] - voxeldim_global[1]
    #P3_m[1] = P3_m[1] - voxeldim_global[1]
    #P4_m[1] = P4_m[1] - voxeldim_global[1]
    #P5_m[1] = P5_m[1] - voxeldim_global[1]
  
  #Plist = [P1_m,P2_m,P3_m,P4_m,P5_m]
  #for idx in range(len(Plist)):
    #P = Plist[idx]
    #F = pillar.addFrequencySnapshot(1,P[0]); F.first = first; F.frequency_vector = frequency_vector; F.name='x_'+str(idx)
    #F = pillar.addFrequencySnapshot(2,P[1]); F.first = first; F.frequency_vector = frequency_vector; F.name='y_'+str(idx)
    #F = pillar.addFrequencySnapshot(3,P[2]); F.first = first; F.frequency_vector = frequency_vector; F.name='z_'+str(idx)
    #probe = Probe(position = P); probe.name = 'p_'+str(idx)
    #pillar.probe_list.append(probe)
  
  #F = pillar.addFrequencySnapshot(1,P_centre[0]); F.first = first; F.frequency_vector = frequency_vector
  #if pillar.boundaries.Ypos_bc == 2:
    #F = pillar.addFrequencySnapshot(2,P_centre[1]); F.first = first; F.frequency_vector = frequency_vector
  #else:
    #F = pillar.addFrequencySnapshot(2,P_centre[1]-delta); F.first = first; F.frequency_vector = frequency_vector
  #F = pillar.addFrequencySnapshot(3,P_centre[2]); F.first = first; F.frequency_vector = frequency_vector
  
  F = pillar.addBoxFrequencySnapshots(); F.first = first; F.frequency_vector = frequency_vector
  
  ## define mesh
  #pillar.addMeshingBox(lower,upper,)
  #pillar.autoMeshGeometry(0.637/10)
  
  # write
  #DSTDIR = os.getenv('DATADIR')
  #DSTDIR = os.getenv('TESTDIR')
  #DSTDIR = os.path.join(os.getenv('TESTDIR'), 'triangle_pillar')
  #DSTDIR = os.path.join(os.getenv('DATADIR'), 'triangle_pillar')
  pillar.writeAll(os.path.join(DSTDIR, BASENAME), BASENAME)
  GEOshellscript(os.path.join(DSTDIR, BASENAME, BASENAME+'.sh'), BASENAME,'$HOME/bin/fdtd', '$JOBDIR', WALLTIME = 360)
  #GEOshellscript_advanced(os.path.join(DSTDIR, BASENAME, BASENAME+'.sh'), BASENAME, getProbeColumnFromExcitation(excitation.E),'$HOME/bin/fdtd', '$JOBDIR', WALLTIME = 360)
  print(pillar.getNcells())
  
def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('DSTDIR', default=tempfile.gettempdir(), nargs='?')
  args = parser.parse_args()  
  print(args.DSTDIR)

  if not os.path.isdir(args.DSTDIR):
    os.mkdir(args.DSTDIR)

  #for pos in range(5):
    #for exc in range(4):
      #semi_loncar(args.DSTDIR,'semi_loncar_'+str(pos)+'_'+str(exc),pos,exc)
  pos = 4
  exc = 2
  semi_loncar(args.DSTDIR, 'semi_loncar_{}_{}'.format(pos, exc), pos, exc)

if __name__ == "__main__":
  main()
