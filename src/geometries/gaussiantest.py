#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import numpy
import constants
import argparse
import tempfile
from bfdtd.bfdtd_parser import *
from utilities.common import *
from meshing.meshing import subGridMultiLayer
from bfdtd.triangular_prism import TriangularPrism
from bfdtd.SpecialTriangularPrism import SpecialTriangularPrism
from bfdtd.excitationTemplate import *

def gaussianPillar(source, target, direction, rotation, DSTDIR):
  pillar = BFDTDobject()
  
  # constants
  Lambda_mum = 0.637
  freq = get_c0()/Lambda_mum
  
  # define flag
  pillar.flag.iterations = 100000
  
  # define boundary conditions
  pillar.boundaries.Xpos_bc = 2
  pillar.boundaries.Ypos_bc = 2
  pillar.boundaries.Zpos_bc = 2
  
  # define box
  pillar.box.lower = [0,0,0]
  pillar.box.upper = [2,2,2]
  
  ## define geometry
  
  # define excitation
  P_centre = pillar.box.getCentro()
  excitation = Excitation()
  
  excitation.current_source = 11
  
  if source=='x':
    excitation.P1 = [ P_centre[0], pillar.box.lower[1], pillar.box.lower[2] ]
    excitation.P2 = [ P_centre[0], pillar.box.upper[1], pillar.box.upper[2] ]
    out_col_name = 'Eyre'
    column_titles = ['y','z','Exre','Exim','Eyre','Eyim','Ezre','Ezim','Hxre','Hxim','Hyre','Hyim','Hzre','Hzim']
  if source=='y':
    excitation.P1 = [ pillar.box.lower[0], P_centre[1], pillar.box.lower[2] ]
    excitation.P2 = [ pillar.box.upper[0], P_centre[1], pillar.box.upper[2] ]
    out_col_name = 'Ezre'
    column_titles = ['x','z','Exre','Exim','Eyre','Eyim','Ezre','Ezim','Hxre','Hxim','Hyre','Hyim','Hzre','Hzim']
  if source=='z':
    excitation.P1 = [ pillar.box.lower[0], pillar.box.lower[1], P_centre[2] ]
    excitation.P2 = [ pillar.box.upper[0], pillar.box.upper[1], P_centre[2] ]
    out_col_name = 'Exre'
    column_titles = ['x','y','Exre','Exim','Eyre','Eyim','Ezre','Ezim','Hxre','Hxim','Hyre','Hyim','Hzre','Hzim']

  excitation.E = [1,1,1]
  excitation.H = [1,1,1]
  excitation.frequency = freq
  
  excitation.template_filename = 'template.dat'
  excitation.template_source_plane = source
  excitation.template_target_plane = target
  excitation.template_direction = direction
  excitation.template_rotation = rotation
  
  pillar.excitation_list = [ excitation ]
  
  # create template
  #x_min = 0.0
  #x_max = 4.00
  #y_min = 0.0
  #y_max = 4.00
  #step_x = 2.00e-2
  #step_y = 2.00e-1
  #x_list = arange(x_min,x_max,step_x)
  #y_list = arange(y_min,y_max,step_y)
  #mesh = MeshObject()
  #mesh.setMesh(x_list,y_list,[])
  
  template = ExcitationGaussian1(amplitude = 1, beam_centre_x = P_centre[0], beam_centre_y = P_centre[1], sigma_x = 0.1, sigma_y = 0.9, fileName='template.dat')
  template.out_col_name = out_col_name
  template.column_titles = column_titles
  #pillar.excitation_template_list.append(template1)
  
  # define probe
  
  # define frequency snapshots
  first = min(65400,pillar.flag.iterations)
  frequency_vector = [freq]
  F = pillar.addFrequencySnapshot('x', P_centre[0]); F.first = first; F.frequency_vector = frequency_vector
  F = pillar.addFrequencySnapshot('y', P_centre[1]); F.first = first; F.frequency_vector = frequency_vector
  F = pillar.addFrequencySnapshot('z', P_centre[2]); F.first = first; F.frequency_vector = frequency_vector
  F = pillar.addBoxFrequencySnapshots(); F.first = first; F.frequency_vector = frequency_vector
  
  pillar.autoMeshGeometry(Lambda_mum/8)
  
  # write
  #DSTDIR = os.getenv('TESTDIR')+os.sep+'gaussiantest'
  BASENAME = 'gaussian_pillar_'+source+'_'+target+'_'+str(direction)+'_'+str(rotation)
  pillar.writeAll(DSTDIR+os.sep+BASENAME, BASENAME)
  #GEOshellscript(DSTDIR+os.sep+BASENAME+os.sep+BASENAME+'.sh', BASENAME, getProbeColumnFromExcitation(excitation.E),'$HOME/bin/fdtd', '$JOBDIR', WALLTIME = 360)
  pillar.writeShellScript(fileName=DSTDIR+os.sep+BASENAME+os.sep+BASENAME+'.sh', BASENAME=BASENAME, EXE='$HOME/bin/fdtd', WORKDIR='$JOBDIR', WALLTIME=360)
  template.writeDatFile(DSTDIR+os.sep+BASENAME+os.sep+'template.dat',pillar.mesh)
  
  print(pillar.getNcells())

def main(argv=None):
  parser = argparse.ArgumentParser()
  parser.add_argument('DSTDIR', default=tempfile.gettempdir(), nargs='?')
  args = parser.parse_args()  
  print(args.DSTDIR)
  
  for s in ['x','y','z']:
    #for t in ['x','y','z']:
      for d in [1]:
        for r in [0,1]:
          gaussianPillar(s, s, d, r, args.DSTDIR)

if __name__ == "__main__":
  main()
