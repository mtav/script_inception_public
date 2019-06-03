#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import numpy as np
import argparse
import tempfile
import bfdtd
from bfdtd.bfdtd_parser import *
from utilities.common import *
from constants.physcon import get_c0, get_e, get_eV, get_epsilon0, get_mu0, get_h, get_h_eVs, get_hb, get_me
from bfdtd.excitationTemplate import *

from bfdtd.excitation_utilities import *

def chalco(DSTDIR, BASENAME):

  n_chalcogenide = 2.4
  n_air = 1.0
  n_Au = 1.0
  n_glass = 1.5

  nHigh = n_chalcogenide
  nLow = n_air

  Lambda_mum = 0.637
  
  #######################
  # layer specifications
  #######################
  layer_size_DBR_left = np.array(30*[ Lambda_mum/(4*n_chalcogenide),Lambda_mum/(4*n_air) ])
  excitation_DBR_left = np.array(30*[ 0, 0 ])
  
  denominator_factor = np.array([4.04, 4.04, 4.28, 4.28, 4.56, 4.56])
  n = 3*[nHigh, nLow]
  layer_size_taper_left = Lambda_mum/(denominator_factor*n)
  excitation_taper_left = np.array(3*[ 0, 0 ])
  
  layer_size_cavity = np.array([Lambda_mum/(4.71*n_chalcogenide)])
  excitation_cavity = np.array([1])

  denominator_factor = np.array([4.56, 4.56, 4.28, 4.28, 4.04, 4.04])
  n = 3*[nLow, nHigh]
  layer_size_taper_right = Lambda_mum/(denominator_factor*n)
  excitation_taper_right = np.array(3*[ 0, 0 ])
  
  layer_size_DBR_right = np.array(15*[ Lambda_mum/(4*n_air), Lambda_mum/(4*n_chalcogenide) ])
  excitation_DBR_right = np.array(15*[ 0, 0 ])

  layer_size_total_cavity = np.concatenate( (layer_size_taper_left, layer_size_cavity, layer_size_taper_right) )
  print('cavity layers = '+str(layer_size_total_cavity))
  print('cavity size = '+str(sum(layer_size_total_cavity)))
  
  layer_size_total_cavity = ((2*Lambda_mum/n_chalcogenide)/sum(layer_size_total_cavity))*layer_size_total_cavity
  
  excitation_all = np.concatenate( (excitation_DBR_left, excitation_taper_left, excitation_cavity, excitation_taper_right, excitation_DBR_right) )
  #layer_size_all = np.concatenate( (layer_size_DBR_left, layer_size_taper_left, layer_size_cavity, layer_size_taper_right, layer_size_DBR_right) )
  layer_size_all = np.concatenate( (layer_size_DBR_left, layer_size_total_cavity, layer_size_DBR_right) )
  print(layer_size_all)
  ######################
  
  pillar = BFDTDobject()
  
  # pillar parameters
  Au_thickness = 0.200
  chalcogenide_thickness = 0.300
  glass_thickness = 1.0

  width_chalcogenide = 0.300
  width_substrate = 1.0
  pillar_height = sum(layer_size_all)
  print('pillar_height = '+str(pillar_height))
  buffer = 1 #0.300
  FullBox_upper = [ pillar_height + 2*buffer, width_substrate + 2*buffer, glass_thickness + Au_thickness + chalcogenide_thickness + 2*buffer ]

  freq = get_c0()/Lambda_mum
  delta = Lambda_mum/(10*nHigh)

  # define flag
  pillar.flag.iterations = 100000
  #pillar.flag.iterations = 10
  
  # define boundary conditions
  #pillar.boundaries.Xpos_bc = 2
  #pillar.boundaries.Ypos_bc = 1 #1
  #pillar.boundaries.Zpos_bc = 2
  
  PML = False
  if PML:
    # PML
    pillar.boundaries.Xpos_bc = 10
    pillar.boundaries.Ypos_bc = 1
    pillar.boundaries.Zpos_bc = 10
    pillar.boundaries.Xneg_bc = 10
    pillar.boundaries.Yneg_bc = 10
    pillar.boundaries.Zneg_bc = 10
  
    pillar.boundaries.Xpos_param = [ 8, 2, 1e-3 ]
    pillar.boundaries.Ypos_param = [ 1, 1, 0 ]
    pillar.boundaries.Zpos_param = [ 8, 2, 1e-3 ]
    pillar.boundaries.Xneg_param = [ 8, 2, 1e-3 ]
    pillar.boundaries.Yneg_param = [ 8, 2, 1e-3 ]
    pillar.boundaries.Zneg_param = [ 8, 2, 1e-3 ]
  else:
    # no PML
    pillar.boundaries.Xpos_bc = 2
    pillar.boundaries.Ypos_bc = 1
    pillar.boundaries.Zpos_bc = 2
    pillar.boundaries.Xneg_bc = 2
    pillar.boundaries.Yneg_bc = 2
    pillar.boundaries.Zneg_bc = 2
  
    pillar.boundaries.Xpos_param = [1,1,0]
    pillar.boundaries.Ypos_param = [1,1,0]
    pillar.boundaries.Zpos_param = [1,1,0]
    pillar.boundaries.Xneg_param = [1,1,0]
    pillar.boundaries.Yneg_param = [1,1,0]
    pillar.boundaries.Zneg_param = [1,1,0]
  
  # define box
  pillar.box.lower = [0,0,0]
  if pillar.boundaries.Ypos_bc == 2:
    pillar.box.upper = FullBox_upper
    P_centre = pillar.box.getCenter()
  else:
    pillar.box.upper = [ FullBox_upper[0], 0.5*FullBox_upper[1], FullBox_upper[2] ]
    P_centre = pillar.box.getCentro()
    P_centre[1] = 0.5*FullBox_upper[1]
  
  glass_centre = [ P_centre[0], P_centre[1], buffer + 0.5*glass_thickness ]
  Au_centre = [ P_centre[0], P_centre[1], buffer + glass_thickness + 0.5*Au_thickness ]
  chalcogenide_centre = [ P_centre[0], P_centre[1], buffer + glass_thickness + Au_thickness +0.5*chalcogenide_thickness ]
  
  # define glass pillar
  glass_pillar = bfdtd.Block()
  glass_pillar.lower = [ glass_centre[0]-0.5*pillar_height, glass_centre[1]-0.5*width_substrate, glass_centre[2]-0.5*glass_thickness ]
  glass_pillar.upper = [ glass_centre[0]+0.5*pillar_height, glass_centre[1]+0.5*width_substrate, glass_centre[2]+0.5*glass_thickness ]
  glass_pillar.permittivity = pow(n_glass,2)
  glass_pillar.conductivity = 0
  pillar.geometry_object_list.append(glass_pillar)

  # define Au pillar
  Au_pillar = bfdtd.Block()
  Au_pillar.lower = [ Au_centre[0]-0.5*pillar_height, Au_centre[1]-0.5*width_substrate, Au_centre[2]-0.5*Au_thickness ]
  Au_pillar.upper = [ Au_centre[0]+0.5*pillar_height, Au_centre[1]+0.5*width_substrate, Au_centre[2]+0.5*Au_thickness ]
  Au_pillar.permittivity = pow(n_Au,2)
  Au_pillar.conductivity = 0
  pillar.geometry_object_list.append(Au_pillar)

  # define chalcogenide pillar
  N = len(layer_size_all)
  print('N = '+str(N))
  lower_x = glass_pillar.lower[0]
  for idx in range(N):
    if idx%2 == 0:
      #print layer_size[idx]
      grating = bfdtd.Block()
      grating.lower = [ lower_x,                   chalcogenide_centre[1]-0.5*width_chalcogenide, chalcogenide_centre[2]-0.5*chalcogenide_thickness ]
      grating.upper = [ lower_x + layer_size_all[idx], chalcogenide_centre[1]+0.5*width_chalcogenide, chalcogenide_centre[2]+0.5*chalcogenide_thickness ]
      grating.permittivity = pow(n_chalcogenide,2)
      grating.conductivity = 0
      pillar.geometry_object_list.append(grating)
    if excitation_all[idx] == 1:
      L = np.array([ lower_x,                   chalcogenide_centre[1]-0.5*width_chalcogenide, chalcogenide_centre[2]-0.5*chalcogenide_thickness ])
      U = np.array([ lower_x + layer_size_all[idx], chalcogenide_centre[1]+0.5*width_chalcogenide, chalcogenide_centre[2]+0.5*chalcogenide_thickness ])
      P_excitation = 0.5*(L+U)
    lower_x = lower_x + layer_size_all[idx]
    
  #################
  ## define excitation
  #################
  if pillar.boundaries.Ypos_bc == 2:
    Ysym = False
  else:
    Ysym = True

  template_radius = 0
  QuadrupleExcitation(Ysym,pillar,P_excitation,'x',delta,template_radius,freq,0)
  #################
  
  #################
  ## define frequency snapshots and probes
  #################
  #first = min(65400,pillar.flag.iterations)
  #frequency_vector = [freq]
  
  ## define probe
  #P = [ main_pillar.upper[0] + delta, P_centre[1], P_centre[2] ]
  #if Ysym:
    #P[1] = P[1]-delta
    
  #probe = Probe(position = P); probe.name = 'resonance_probe'
  #pillar.probe_list.append(probe)
  
  ## define snapshots around probe
  #F = pillar.addFrequencySnapshot(1,P[0]); F.first = first; F.frequency_vector = frequency_vector; F.name='x_'+str(0)
  #F = pillar.addFrequencySnapshot(2,P[1]); F.first = first; F.frequency_vector = frequency_vector; F.name='y_'+str(0)
  #F = pillar.addFrequencySnapshot(3,P[2]); F.first = first; F.frequency_vector = frequency_vector; F.name='z_'+str(0)
  
  ## define central snapshots
  #F = pillar.addFrequencySnapshot(1,P_excitation[0]); F.first = first; F.frequency_vector = frequency_vector
  #if pillar.boundaries.Ypos_bc == 2:
    #F = pillar.addFrequencySnapshot(2,P_excitation[1]); F.first = first; F.frequency_vector = frequency_vector
  #else:
    #F = pillar.addFrequencySnapshot(2,P_excitation[1]-delta); F.first = first; F.frequency_vector = frequency_vector
  #F = pillar.addFrequencySnapshot(3,P_excitation[2]); F.first = first; F.frequency_vector = frequency_vector
  
  ## box frequency snapshots
  #F = pillar.addBoxFrequencySnapshots(); F.first = first; F.frequency_vector = frequency_vector
  
  ## efficiency snapshots around structure
  ## TODO: write function to do this
  #L = [ main_pillar.lower[0], main_pillar.lower[1]-grating_depth, main_pillar.lower[2]-grating_depth ] - delta*np.array([1,1,1])
  #U = [ main_pillar.upper[0], main_pillar.upper[1]+grating_depth, main_pillar.upper[2]+grating_depth ] + delta*np.array([1,1,1])
  #if pillar.boundaries.Ypos_bc == 1:
    #U[1] = min(U[1],pillar.box.upper[1])
  #F = Frequency_snapshot(name='Efficiency box frequency snapshot', P1=L, P2=U); F.first = first; F.frequency_vector = frequency_vector;
  #pillar.snapshot_list.append(F)

  # define mesh
  pillar.autoMeshGeometry(Lambda_mum/20.0)

  # write pillar
  pillar.writeAll(DSTDIR+os.sep+BASENAME, BASENAME)
  GEOshellscript(DSTDIR+os.sep+BASENAME+os.sep+BASENAME+'.sh', BASENAME,'$HOME/bin/fdtd', '$JOBDIR', WALLTIME = 360)
  #GEOshellscript_advanced(DSTDIR+os.sep+BASENAME+os.sep+BASENAME+'.sh', BASENAME, getProbeColumnFromExcitation(pillar.excitation_list[0].E),'$HOME/bin/fdtd', '$JOBDIR', WALLTIME = 360)
  print(pillar.getNcells())
  
def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('DSTDIR', default=tempfile.gettempdir(), nargs='?')
  args = parser.parse_args()  
  print(args.DSTDIR)
  
  if not os.path.isdir(args.DSTDIR):
    os.mkdir(args.DSTDIR)
  chalco(args.DSTDIR, 'chalco')

if __name__ == "__main__":
  main()
