#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import numpy
import argparse
import tempfile
import bfdtd
import constants
#from bfdtd.bfdtd_parser import *
#from utilities.common import *
#from bfdtd.excitationTemplate import *
#from bfdtd.excitation_utilities import *
from bfdtd.bristolFDTD_generator_functions import GEOshellscript
from bfdtd.excitation_utilities import QuadrupleExcitation

valid_defect_types = ['cylinder_holes',
                      'block_holes',
                      'cylinder_layers',
                      'grating']

# TODO: implement as class/subclass of BFDTDobject or pillar_1D
def rectangularYagiWithTaper(DSTDIR, BASENAME, nHigh, nLow, Lambda_mum, layer_size, excitation_array, PML, pillar_diametro, defect_type):
  '''
  layer_size : list of layer sizes, including the cavity
  excitation_array : list of zeros and ones, the same length as layer_size. A source will be placed into the layer with the corresponding index if excitation_array[idx]==1
  PML : true/false, use Perfect Matching Layers or not?
  '''
  #denominator_factor = numpy.array(denominator_factor)
  #n = numpy.array(n)
  
  hole_length = 2*pillar_diametro
  
  pillar = bfdtd.BFDTDobject()
  
  # calculate layer height
  #layer_size = Lambda_mum/(denominator_factor*n)
  #print(layer_size)

  # pillar parameters
  pillar_height = sum(layer_size)
  #print('pillar_height = '+str(pillar_height))
  #pillar_radius = 0.5*0.340
  pillar_radius = 0.5*pillar_diametro
  bufferSpace = 1
  FullBox_upper = [ pillar_height+2*bufferSpace, 2*(pillar_radius+bufferSpace), 2*(pillar_radius+bufferSpace) ]
  #FullBox_upper = [ 10, 10, 4 ]
  #grating_depth = 3*0.100
  grating_depth = 0.100
  freq = constants.get_c0()/Lambda_mum
  delta = Lambda_mum/(10*nHigh)

  # define flag
  pillar.flag.iterations = 1048000
  #pillar.flag.iterations = 100000
  #pillar.flag.iterations = 10
  
  # define boundary conditions
  #pillar.boundaries.Xpos_bc = 2
  #pillar.boundaries.Ypos_bc = 1 #1
  #pillar.boundaries.Zpos_bc = 2
  
  # default excitation location
  P_excitation = pillar.getCentro()
  
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
    pillar.boundaries.Ypos_bc = 2
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
    P_centre = pillar.box.getCentro()
  else:
    pillar.box.upper = [ FullBox_upper[0], 0.5*FullBox_upper[1], FullBox_upper[2] ]
    P_centre = pillar.box.getCentro()
    P_centre[1] = 0.5*FullBox_upper[1]
  
  # define main pillar
  main_pillar = bfdtd.Block()
  main_pillar.setLowerAbsolute([ P_centre[0]-0.5*pillar_height, P_centre[1]-pillar_radius, P_centre[2]-pillar_radius ])
  main_pillar.setUpperAbsolute([ P_centre[0]+0.5*pillar_height, P_centre[1]+pillar_radius, P_centre[2]+pillar_radius ])
  #main_pillar.setLowerAbsolute([  0, P_centre[1]-pillar_radius, P_centre[2]-pillar_radius ])
  #main_pillar.setUpperAbsolute([ 10, P_centre[1]+pillar_radius, P_centre[2]+pillar_radius ])
  main_pillar.setRefractiveIndex(nHigh)
  main_pillar.setName('main_pillar')
  if defect_type != 'cylinder_layers':
    pillar.setGeometryObjects([ main_pillar ])

  # define defects
  N = len(layer_size)
  #print('N = '+str(N))
  lower_x = main_pillar.getLowerAbsolute()[0]
  
  if defect_type == 'cylinder_holes':
    # .. todo:: fix mesh (i.e. replace MeshBox with latest meshing system...)
    #mesh_box = bfdtd.MeshBox()
    #mesh_box.lower = [ pillar.box.lower[0], P_centre[1]-pillar_radius, P_centre[2]-0.5*max(layer_size) ]
    #mesh_box.upper = [ pillar.box.upper[0], P_centre[1]+pillar_radius, P_centre[2]+0.5*max(layer_size) ]
    #mesh_box.permittivity3D = [1e-3, 1e-3, pow(2*nHigh,2)]
    #pillar.mesh_object_list.append(mesh_box)
    pass
  
  for idx in range(N):
    if defect_type == 'cylinder_holes':
      if idx%2 == 1:
        #print layer_size[idx]
        defect = bfdtd.Cylinder()
        defect.setName('Cylinder_{}'.format(idx))
        defect.setDiametre(layer_size[idx])
        defect.setLocation([lower_x + 0.5*layer_size[idx],P_centre[1],P_centre[2]])
        defect.setHeight(hole_length)
        defect.setRefractiveIndex(nLow)
        pillar.appendGeometryObject(defect)
      #print 'idx = ',idx, 'excitation_array = ', excitation_array
      if excitation_array[idx] == 1:
        L = numpy.array([ lower_x, P_centre[1]-pillar_radius-grating_depth, P_centre[2]-pillar_radius-grating_depth])
        U = numpy.array([ lower_x + layer_size[idx], P_centre[1]+pillar_radius+grating_depth, P_centre[2]+pillar_radius+grating_depth ])
        P_excitation = 0.5*(L+U)
      lower_x = lower_x + layer_size[idx]
    elif defect_type == 'block_holes':
      if idx%2 == 1:
        #print layer_size[idx]
        defect = bfdtd.Block()
        defect.setName('Block_{}'.format(idx))
        defect.setLowerAbsolute([ lower_x,                   P_centre[1]-0.5*hole_length, P_centre[2]-pillar_radius+grating_depth ])
        defect.setUpperAbsolute([ lower_x + layer_size[idx], P_centre[1]+0.5*hole_length, P_centre[2]+pillar_radius-grating_depth ])
        defect.setRefractiveIndex(nLow)
        pillar.geometry_object_list.append(defect)
      #print 'idx = ',idx, 'excitation_array = ', excitation_array
      if excitation_array[idx] == 1:
        L = numpy.array([ lower_x, P_centre[1]-pillar_radius-grating_depth, P_centre[2]-pillar_radius-grating_depth])
        U = numpy.array([ lower_x + layer_size[idx], P_centre[1]+pillar_radius+grating_depth, P_centre[2]+pillar_radius+grating_depth ])
        P_excitation = 0.5*(L+U)
      lower_x = lower_x + layer_size[idx]
    elif defect_type == 'cylinder_layers':
      # TODO: finish implementing this. Also see pillar_1D.py and similar scripts to reduce code duplication.
      defect = bfdtd.Cylinder()
      defect.setName('Cylinder_{}'.format(idx))
      lower = numpy.array([ lower_x,                   P_centre[1]-pillar_radius, P_centre[2]-pillar_radius+grating_depth])
      upper = numpy.array([ lower_x + layer_size[idx], P_centre[1]+pillar_radius, P_centre[2]+pillar_radius-grating_depth ])
      defect.setLocation(0.5*(lower+upper))
      defect.setOuterRadius(pillar_radius)
      if idx%2 == 0:
        defect.setRefractiveIndex(nHigh)
      else:
        defect.setRefractiveIndex(nLow)
      defect.setHeight(layer_size[idx])
      defect.setAxis([1,0,0])
      pillar.geometry_object_list.append(defect)
      #print 'idx = ',idx, 'excitation_array = ', excitation_array
      if excitation_array[idx] == 1:
        L = numpy.array([ lower_x, P_centre[1]-pillar_radius-grating_depth, P_centre[2]-pillar_radius-grating_depth])
        U = numpy.array([ lower_x + layer_size[idx], P_centre[1]+pillar_radius+grating_depth, P_centre[2]+pillar_radius+grating_depth ])
        P_excitation = 0.5*(L+U)
      lower_x = lower_x + layer_size[idx]
    elif defect_type == 'grating':
      if idx%2 == 0:
        #print layer_size[idx]
        defect = bfdtd.Block()
        defect.setName('Block_{}'.format(idx))
        defect.setLowerAbsolute([ lower_x, P_centre[1]-pillar_radius-grating_depth, P_centre[2]-pillar_radius-grating_depth])
        defect.setUpperAbsolute([ lower_x + layer_size[idx], P_centre[1]+pillar_radius+grating_depth, P_centre[2]+pillar_radius+grating_depth ])
        defect.setRefractiveIndex(nHigh)
        pillar.geometry_object_list.append(defect)
      #print 'idx = ',idx, 'excitation_array = ', excitation_array
      if excitation_array[idx] == 1:
        L = numpy.array([ lower_x, P_centre[1]-pillar_radius-grating_depth, P_centre[2]-pillar_radius-grating_depth])
        U = numpy.array([ lower_x + layer_size[idx], P_centre[1]+pillar_radius+grating_depth, P_centre[2]+pillar_radius+grating_depth ])
        P_excitation = 0.5*(L+U)
      lower_x = lower_x + layer_size[idx]
      #if lower_x > 10:
        #break
    else:
      print('unknown defect type: '+defect_type)
      sys.exit(1)
        
  #print(pillar.getGeometryObjects())
  
  ################
  # define excitation
  ################
  if pillar.boundaries.Ypos_bc == 2:
    Ysym = False
  else:
    Ysym = True

  template_radius = 0
  QuadrupleExcitation(Ysym, pillar, P_excitation, 'x', delta, template_radius, freq, 0)
  ################
  
  ################
  # define frequency snapshots and probes
  ################
  first = min(65400,pillar.flag.iterations)
  frequency_vector = [freq]
  
  # define probe
  P = [ main_pillar.getUpperAbsolute()[0] + delta, P_centre[1], P_centre[2] ]
  if Ysym:
    P[1] = P[1]-delta
  probe = bfdtd.Probe(position = P); probe.name = 'resonance_probe'
  pillar.appendProbe(probe)

  P = [ P_excitation[0] + delta, P_centre[1], P_centre[2] ]
  if Ysym:
    P[1] = P[1]-delta
  probe = bfdtd.Probe(position = P); probe.name = 'resonance_probe'
  pillar.appendProbe(probe)
  
  # define snapshots around probe
  #F = pillar.addFrequencySnapshot(1,P[0]); F.first = first; F.frequency_vector = frequency_vector; F.name='x_'+str(0)
  #F = pillar.addFrequencySnapshot(2,P[1]); F.first = first; F.frequency_vector = frequency_vector; F.name='y_'+str(0)
  #F = pillar.addFrequencySnapshot(3,P[2]); F.first = first; F.frequency_vector = frequency_vector; F.name='z_'+str(0)
  
  # define central snapshots
  F = pillar.addFrequencySnapshot('x', P_excitation[0]); F.first = first; F.frequency_vector = frequency_vector
  if pillar.boundaries.Ypos_bc == 2:
    F = pillar.addFrequencySnapshot('y', P_excitation[1]); F.first = first; F.frequency_vector = frequency_vector
  else:
    F = pillar.addFrequencySnapshot('y', P_excitation[1]-delta); F.first = first; F.frequency_vector = frequency_vector
  F = pillar.addFrequencySnapshot('z', P_excitation[2]); F.first = first; F.frequency_vector = frequency_vector

  F = pillar.addTimeSnapshot('x', P_excitation[0]); F.first = first
  if pillar.boundaries.Ypos_bc == 2:
    F = pillar.addTimeSnapshot('y', P_excitation[1]); F.first = first
  else:
    F = pillar.addTimeSnapshot('y', P_excitation[1]-delta); F.first = first
  F = pillar.addTimeSnapshot('z', P_excitation[2]); F.first = first
  
  # box frequency snapshots
  #F = pillar.addBoxFrequencySnapshots(); F.first = first; F.frequency_vector = frequency_vector
  
  # efficiency snapshots around structure
  ## TODO: write function to do this
  #L = [ main_pillar.lower[0], main_pillar.lower[1]-grating_depth, main_pillar.lower[2]-grating_depth ] - delta*numpy.array([1,1,1])
  #U = [ main_pillar.upper[0], main_pillar.upper[1]+grating_depth, main_pillar.upper[2]+grating_depth ] + delta*numpy.array([1,1,1])
  #if pillar.boundaries.Ypos_bc == 1:
    #U[1] = min(U[1],pillar.box.upper[1])
  #F = Frequency_snapshot(name='Efficiency box frequency snapshot', P1=L, P2=U); F.first = first; F.frequency_vector = frequency_vector;
  #pillar.snapshot_list.append(F)

  lower_wall = bfdtd.Block()
  lower_wall.setName('lower_wall')
  lower_wall.setLowerAbsolute([ 0,0,0 ])
  lower_wall.setUpperAbsolute([ 0.5, pillar.box.upper[1],pillar.box.upper[2] ])
  lower_wall.setRefractiveIndex(nHigh)
  lower_wall.setRelativeConductivity(0)
  #pillar.appendGeometryObject(lower_wall)

  upper_wall = bfdtd.Block()
  upper_wall.setName('upper_wall')
  upper_wall.setLowerAbsolute([ pillar.box.upper[0]-0.5,0,0 ])
  upper_wall.setUpperAbsolute([ pillar.box.upper[0], pillar.box.upper[1],pillar.box.upper[2] ])
  upper_wall.setRefractiveIndex(nHigh)
  upper_wall.setRelativeConductivity(0)
  #pillar.appendGeometryObject(upper_wall)

  # define mesh
  a = 20
  pillar.autoMeshGeometry(0.637/a)
  while(pillar.getNcells()>8000000 and a>1):
    a = a-1
    pillar.autoMeshGeometry(0.637/a)
  
  #pillar.autoMeshGeometry(1000)

  # write pillar
  #pillar.writeAll(DSTDIR+os.sep+BASENAME, BASENAME)
  ##GEOshellscript(DSTDIR+os.sep+BASENAME+os.sep+BASENAME+'.sh', BASENAME,'$HOME/bin/fdtd', '$JOBDIR', WALLTIME = 360)
  #GEOshellscript_advanced(DSTDIR+os.sep+BASENAME+os.sep+BASENAME+'.sh', BASENAME, getProbeColumnFromExcitation(pillar.excitation_list[0].E),'$HOME/bin/fdtd', '$JOBDIR', WALLTIME = 360)

  pillar.writeAll(DSTDIR, BASENAME)
  GEOshellscript(DSTDIR+os.sep+BASENAME+'.sh', BASENAME,'$HOME/bin/fdtd', '$JOBDIR', WALLTIME = 360)
  #GEOshellscript_advanced(DSTDIR+os.sep+BASENAME+os.sep+BASENAME+'.sh', BASENAME, getProbeColumnFromExcitation(pillar.excitation_list[0].E),'$HOME/bin/fdtd', '$JOBDIR', WALLTIME = 360)

  print('pillar.getNcells() = '+str(pillar.getNcells()))
  if pillar.getNcells()>8000000:
    sys.exit(-1)

def calculateLayerSizes(taper_type, Nbottom, Ntop, Lambda_mum, nHigh, nLow,
    denominator_factor_DBR_left_nHigh, denominator_factor_DBR_left_nLow, denominator_factor_taper_left,
    denominator_factor_cavity,
    denominator_factor_taper_right, denominator_factor_DBR_right_nLow, denominator_factor_DBR_right_nHigh):
  '''
  taper_type : Use 0
  '''
  
  denominator_factor_taper_left = numpy.array(denominator_factor_taper_left)
  denominator_factor_taper_right = numpy.array(denominator_factor_taper_right)
  
  #######################
  # layer specifications
  #######################

  #print denominator_factor_taper_left
  #print denominator_factor_taper_right
  #sys.exit(0)
  
  # left taper layer
  if len(denominator_factor_taper_left)%2:
    print('ERROR: denominator_factor_taper_left list must be multiple of 2')
    sys.exit(-1)
  else:
    N_TaperPairs_left = int(len(denominator_factor_taper_left)/2)
    n_left = N_TaperPairs_left*[nHigh, nLow]
    excitation_taper_left = numpy.array(N_TaperPairs_left*[ 0, 0 ])
    layer_size_taper_left = Lambda_mum/(denominator_factor_taper_left*n_left)

  # right taper layer
  if len(denominator_factor_taper_right)%2:
    print('ERROR: denominator_factor_taper_right list must be multiple of 2')
    sys.exit(-1)
  else:
    N_TaperPairs_right = int(len(denominator_factor_taper_right)/2)
    n_right = N_TaperPairs_right*[nLow, nHigh]
    excitation_taper_right = numpy.array(N_TaperPairs_right*[ 0, 0 ])
    layer_size_taper_right = Lambda_mum/(denominator_factor_taper_right*n_right)

  # regular left DBR layers
  layer_size_DBR_left = numpy.array(Nbottom*[ Lambda_mum/(denominator_factor_DBR_left_nHigh*nHigh),Lambda_mum/(denominator_factor_DBR_left_nLow*nLow) ])
  excitation_DBR_left = numpy.array(Nbottom*[ 0, 0 ])

  # regular right DBR layers
  layer_size_DBR_right = numpy.array(Ntop*[ Lambda_mum/(denominator_factor_DBR_right_nLow*nLow), Lambda_mum/(denominator_factor_DBR_right_nHigh*nHigh) ])
  excitation_DBR_right = numpy.array(Ntop*[ 0, 0 ])
  
  # cavity
  layer_size_cavity = numpy.array([Lambda_mum/(denominator_factor_cavity*nHigh)])
  excitation_cavity = numpy.array([1])
  
  layer_size_total_cavity = numpy.concatenate( (layer_size_taper_left, layer_size_cavity, layer_size_taper_right) )
  #print('cavity layers = '+str(layer_size_total_cavity))
  #print('cavity size = '+str(sum(layer_size_total_cavity)))
  
  if taper_type == 0:
    layer_size_total_cavity = (1)*layer_size_total_cavity
  elif taper_type == 1:
    layer_size_total_cavity = ((1*Lambda_mum/nHigh)/sum(layer_size_total_cavity))*layer_size_total_cavity
  else:
    layer_size_total_cavity = ((2*Lambda_mum/nHigh)/sum(layer_size_total_cavity))*layer_size_total_cavity
  
  excitation_all = numpy.concatenate( (excitation_DBR_left, excitation_taper_left, excitation_cavity, excitation_taper_right, excitation_DBR_right) )
  #layer_size_all = numpy.concatenate( (layer_size_DBR_left, layer_size_taper_left, layer_size_cavity, layer_size_taper_right, layer_size_DBR_right) )
  layer_size_all = numpy.concatenate( (layer_size_DBR_left, layer_size_total_cavity, layer_size_DBR_right) )
  #print(layer_size_all)
  return layer_size_all, excitation_all
  ######################

def quicktest():
  for defect_type in valid_defect_types:
    DSTDIR = '/tmp'
    BASENAME = defect_type
    nHigh = 2.4
    nLow = 1
    Lambda_mum = 0.637
    layer_size = 3*[0.5, 1] + [2] + 3*[1, 0.5]
    excitation_array = [0]*len(layer_size)
    PML = False
    pillar_diametro = 1
    rectangularYagiWithTaper(DSTDIR, BASENAME, nHigh, nLow, Lambda_mum, layer_size, excitation_array, PML, pillar_diametro, defect_type)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('DSTDIR', default=tempfile.gettempdir(), nargs='?')
  args = parser.parse_args()  
  print(args.DSTDIR)

  if not os.path.isdir(args.DSTDIR):
    os.mkdir(args.DSTDIR)

  ## case 1
  #nHigh = 3.39
  #nLow = 2.83
  #Lambda_mum = 0.950

  #rectangularYagiWithTaper(DSTDIR, 'rectangularYagiWithTaper.Lambda_'+str(Lambda_mum), nHigh, nLow, Lambda_mum)
  
  ## case 2
  #nHigh = 3.55
  #nLow = 2.94
  #Lambda_mum = 0.994

  #rectangularYagiWithTaper(DSTDIR, 'rectangularYagiWithTaper.Lambda_'+str(Lambda_mum), nHigh, nLow, Lambda_mum)

  # new optimal values: 4	4	4.14	4.14	4.28	4.28	4.56	4.56	4.67	4.56	4.56	4.28	4.28	4.14	4.14	4	4

  # case 3

  nHigh = 2.4
  nLow = 1
  Lambda_mum = 0.637

  # left taper
  #denominator_factor_taper_left = numpy.array([4.04, 4.04, 4.28, 4.28, 4.56, 4.56])
  #denominator_factor_taper_left = numpy.array([4.14, 4.14, 4.28, 4.28, 4.56, 4.56])
  #denominator_factor_taper_left = numpy.array([4.14, 4.14, 4.28, 4.28, 4.56, 4.56])
  #denominator_factor_taper_left = numpy.array([])
  # right taper
  #denominator_factor_taper_right = numpy.array([4.56, 4.56, 4.28, 4.28, 4.04, 4.04])
  #denominator_factor_taper_right = numpy.array([4.56, 4.56, 4.28, 4.28, 4.14, 4.14])
  #denominator_factor_taper_right = numpy.array([4.56, 4.56, 4.28, 4.28, 4.14, 4.14])
  #denominator_factor_taper_right = numpy.array([])
  
  #denominator_factor_cavity = 4.71
  #denominator_factor_cavity = 4.67
  #denominator_factor_cavity = 4

  #denominator_factor_DBR_left_nHigh = denominator_factor_DBR_right_nHigh = 4
  #denominator_factor_DBR_left_nLow = denominator_factor_DBR_right_nLow = 8
  #denominator_factor_taper_left = numpy.array([0.3,0.3,0.2,0.2,0.5,0.5])
  #denominator_factor_cavity = 1
  #denominator_factor_taper_right = denominator_factor_taper_left[::-1]

  # 1
  #denominator_factor_DBR_left_nHigh = denominator_factor_DBR_right_nHigh = 3.76
  #denominator_factor_DBR_left_nLow = denominator_factor_DBR_right_nLow = 3.68
  #denominator_factor_taper_left = numpy.array([3.87, 3.89, 4.10, 4.13, 4.36, 4.40])
  #denominator_factor_cavity = 4.51
  #denominator_factor_taper_right = denominator_factor_taper_left[::-1]

  # 2
  #denominator_factor_DBR_left_nHigh = denominator_factor_DBR_right_nHigh = 4.00
  #denominator_factor_DBR_left_nLow = denominator_factor_DBR_right_nLow = 4.00
  #denominator_factor_taper_left = numpy.array([3.88, 3.88, 4.12, 4.12, 4.38, 4.38])
  #denominator_factor_cavity = 4.51
  #denominator_factor_taper_right = denominator_factor_taper_left[::-1]

  # 1 no taper
  #denominator_factor_DBR_left_nHigh = denominator_factor_DBR_right_nHigh = 3.76
  #denominator_factor_DBR_left_nLow = denominator_factor_DBR_right_nLow = 3.68
  #denominator_factor_taper_left = numpy.array(3*[denominator_factor_DBR_right_nHigh, denominator_factor_DBR_right_nLow])
  #denominator_factor_cavity = 4.51
  #denominator_factor_taper_right = denominator_factor_taper_left[::-1]

  # 2 no taper
  #denominator_factor_DBR_left_nHigh = denominator_factor_DBR_right_nHigh = 4.00
  #denominator_factor_DBR_left_nLow = denominator_factor_DBR_right_nLow = 4.00
  #denominator_factor_taper_left = numpy.array(3*[denominator_factor_DBR_right_nHigh, denominator_factor_DBR_right_nLow])
  #denominator_factor_cavity = 4.51
  #denominator_factor_taper_right = denominator_factor_taper_left[::-1]

  denominator_factor_DBR_left_nHigh = denominator_factor_DBR_right_nHigh = 1./5.*4.00
  denominator_factor_DBR_left_nLow = denominator_factor_DBR_right_nLow = 1./5.*4.00
  denominator_factor_taper_left = [] #numpy.array(3*[denominator_factor_DBR_right_nHigh, denominator_factor_DBR_right_nLow])
  denominator_factor_cavity = 1./5.*4.51
  denominator_factor_taper_right = denominator_factor_taper_left[::-1]

  #for taper_type in [0,1,2]:
  for defect_type in valid_defect_types:
    print('defect_type = {}'.format(defect_type))
    for pillar_diametro in [0.340, 0.5, 1]:
      for taper_type in [0]:
      
        #denominator_factor_base = [ 4, 4, 4.04, 4.04, 4.28, 4.28, 4.56, 4.56, 4.71, 4.56, 4.56, 4.28, 4.28, 4.04, 4.04, 4, 4 ]
        #n_base = [ nHigh , nLow , nHigh , nLow , nHigh , nLow , nHigh , nLow , nHigh , nLow , nHigh , nLow , nHigh , nLow , nHigh , nLow , nHigh ]
        #excitation_array_base = [ 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0 ]
      
        #for PML in [True,False]:
        for PML in [False]:
          #for (Nbottom,Ntop) in [(4,4),(30,25),(25,25)]:
          for (Nbottom,Ntop) in [(4,4)]:
            #denominator_factor = (Nbottom-4)*[4, 4] + denominator_factor_base + (Ntop-4)*[4, 4]
            #n = (Nbottom-4)*[nHigh , nLow] + n_base + (Ntop-4)*[nLow , nHigh]
            #excitation_array = (Nbottom-4)*[0 , 0] + excitation_array_base + (Ntop-4)*[0 , 0]
            layer_size_all, excitation_cavity = calculateLayerSizes(taper_type, Nbottom, Ntop, Lambda_mum, nHigh, nLow,
              denominator_factor_DBR_left_nHigh, denominator_factor_DBR_left_nLow, denominator_factor_taper_left,
              denominator_factor_cavity,
              denominator_factor_taper_right, denominator_factor_DBR_right_nLow, denominator_factor_DBR_right_nHigh)
            dosiernomo = 'rectangularYagiWithTaper.Lambda_'+str(Lambda_mum)+'.Nbottom_'+str(Nbottom)+'.Ntop_'+str(Ntop)+'.PML_'+str(PML)+'.taper_type_'+str(taper_type)+'.pillar_diametro_'+str(pillar_diametro)+'.defect_type_'+str(defect_type)
            if not os.path.isdir(os.path.join(args.DSTDIR, dosiernomo)):
              os.makedirs(os.path.join(args.DSTDIR, dosiernomo))
            #rectangularYagiWithTaper(os.path.join(args.DSTDIR, dosiernomo), dosiernomo, nHigh, nLow, Lambda_mum, layer_size_all, excitation_cavity, PML, pillar_diametro, 'grating')
            #rectangularYagiWithTaper(os.path.join(args.DSTDIR, dosiernomo), dosiernomo, nHigh, nLow, Lambda_mum, layer_size_all, excitation_cavity, PML, pillar_diametro, 'cylinder_layers')
            rectangularYagiWithTaper(os.path.join(args.DSTDIR, dosiernomo), dosiernomo, nHigh, nLow, Lambda_mum, layer_size_all, excitation_cavity, PML, pillar_diametro, defect_type)
    
if __name__ == "__main__":
  quicktest()
  #main()
