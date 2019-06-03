#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
#import sys
#import re
import os
import numpy
import tempfile

# TODO list:
# -Add extended interpolation to .ini parser (cf python doc)
# -Add default values for woodpile, which can be updated from a [default] section in.ini files.
# -values of the form [[x,x,x],[x,x,x],[x,x,x]] or [x,x,x] should cause loops
# -pass strings of the form {w_factor}/{excitation_direction}/etc to create directory names from parameters
# -move looping system into weijeiWoodpile.py
# -> prepare*.py scripts will become almost unnecessary.
# -add possibility to include .ini files from other .ini files (or create special .ini filelists) (mainly necessary for easy loading)
# -move weijeiWoodpile.py into woodpile.py
# -create simple interface to choose .ini files
# -create Blender add-on or alternate interface to create woodpiles (and other objects)

from weijeiWoodpile import weijeiWoodpile

def prepare(destdir = '.'):

  refractive_index_defect = []
  refractive_index_log = []
  refractive_index_outer = []
  vertical_period = []
  w_factor = []

  # TODO: Read those values from an input file
  # For origin, cf:
  # /space/ANONYMIZED/DATA/MPB/woodpile_MPB_study/woodpile.w+h+n_log+n_outer/notes.txt
  # /space/ANONYMIZED/DATA/MPB/w_optimization_test/maximize_woodpile_bandgap/summary3.txt
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  excitation_direction_string = ['Ex','Ey','Ez']

  for shift_initial_layers in [True, False]:
  #for shift_initial_layers in [True]:
    #for defect_size_factor_vector in [[1,1,1],[3,1,1],[1,3,1],[1,1,3]]:
    #for defect_size_factor_vector in [[1,1,1]]:
    #for defect_size_factor_vector in [3*[i] for i in numpy.arange(0.25,2,0.25)]:
    #for defect_size_factor_vector in [3*[i] for i in numpy.arange(1,1.2,1)]:
    #for defect_size_factor_vector in [[1,1,1],[1,3,1],[3,1,1]]:
    #for defect_size_factor_vector in [[1,1,2],[1,2,1],[2,1,1],[1,1,3]]:
    #for defect_size_factor_vector in [[0.125,0.125,0.125]]:
    #for defect_size_factor_vector in [[0.25,0.25,0.25]]:
    #for defect_size_factor_vector in [[1,1,3]]:
    #for defect_size_factor_vector in [[1,1,2],[1,2,1],[2,1,1]]:
    #for defect_size_factor_vector in [3*[i] for i in numpy.arange(1,1.2,1)]:
    #for defect_size_factor_vector in [3*[i] for i in numpy.arange(0.85,1.25,0.05)]:
    #for defect_size_factor_vector in [[1,1,2],[1,2,1],[2,1,1],[1,1,3]]:
    #for defect_size_factor_vector in [[0.5,0.5,0.5]]:
    #for defect_size_factor_vector in [[1,1,1]]:
    #for defect_size_factor_vector in [[0.5,0.5,0.5]]:
    #for defect_size_factor_vector in [3*[i] for i in numpy.arange(0.25,2,0.25)]:
    #for defect_size_factor_vector in [3*[i] for i in numpy.arange(1,1.2,1)]:
    #for defect_size_factor_vector in [[1,1,1],[1,3,1],[3,1,1]]:
    #for defect_size_factor_vector in [[1,1,2],[1,2,1],[2,1,1],[1,1,3]]:
    #for defect_size_factor_vector in [[0.125,0.125,0.125]]:
    #for defect_size_factor_vector in [[0.25,0.25,0.25]]:
    #for defect_size_factor_vector in [[0.5,0.5,0.5]]:
    for i in range(len(refractive_index_log)):
    #for i in [0]:
      #for defect_offset_bool in [False,True]:
      #BASE0 = 'defect_offset_%d' % (not(defect_offset_bool))
      for defect_offset in [[0,0,0],[0,0,3./8.*vertical_period[i]]]:

        # prepare some variables for readability
        wf = w_factor[i]
        df = 1/numpy.sqrt(2)
        defect_width = [ wf, df/2., df-wf, df, df+wf, 3./2.*df, 2*df-wf, 1, 0.5, 0.25 ]

        z100 = []
        z050 = []
        z025 = []
        for defect_width_elt in defect_width:
          # z=1*c
          z100.append([defect_width_elt, defect_width_elt, 1.00])
          # z=0.5*c
          z050.append([defect_width_elt, defect_width_elt, 0.50])
          # z=0.25*c
          z025.append([defect_width_elt, defect_width_elt, 0.25])

        for defect_size_factor_vector in z100+z050+z025:
        #for defect_size_factor_vector in [[1,1,1],[1,1,0.5],[1,1,0.25],[0.5,0.5,0.5],[0.5,0.5,0.25],[0.25,0.25,0.25]]:
            for excitation_direction in [0,1,2]:
              BASE1 = 'defectType_%d.Size_%.3f.%.3f.%.3f' % (not(shift_initial_layers), defect_size_factor_vector[0], defect_size_factor_vector[1], defect_size_factor_vector[2])
              BASE2 = 'ndefect_%.2f.nlog_%.2f.nout_%.2f.a_%.2f.w_%.2f'%(refractive_index_defect[i],refractive_index_log[i],refractive_index_outer[i],vertical_period[i],w_factor[i])
              directory = destdir + os.sep + BASE2 + os.sep + BASE1 + os.sep + excitation_direction_string[excitation_direction] + os.sep
              if not os.path.isdir(directory):
                os.makedirs(directory)
              print(' directory = ' + directory)
              #defect_size_vector = vertical_period[i]/numpy.sqrt(2)*numpy.array(defect_size_factor_vector)
              #defect_size_vector = vertical_period[i]/numpy.sqrt(2)*numpy.array(defect_size_factor_vector)
              defect_size_vector = vertical_period[i]*numpy.array(defect_size_factor_vector)
              #defect_offset = [0,0,0]
              #defect_offset = [0,0,0.069*1]
              #defect_offset = [0,0,0.069*1.5]
              #defect_offset = [0,0,vertical_period[i]*0.25]

              foo = weijeiWoodpile()
              foo.vertical_period = vertical_period[i]
              foo.refractive_index_defect = refractive_index_defect[i]
              foo.refractive_index_log = refractive_index_log[i]
              foo.refractive_index_outer = refractive_index_outer[i]
              foo.excitation_direction = excitation_direction
              foo.w_factor = w_factor[i]
              foo.defect_size_vector = defect_size_vector
              foo.defect_offset = defect_offset
              foo.shift_initial_layers = shift_initial_layers
              foo.writeBFDTD(directory,'woodpile')

def main():
  parser = argparse.ArgumentParser(description = 'prepare some woodpile simulations')
  parser.add_argument('-d','--outdir', action="store", dest="outdir", default=tempfile.gettempdir() + os.sep + 'sims', help='output directory')
  arguments = parser.parse_args()
  prepare(arguments.outdir)

if __name__ == "__main__":
  main()
