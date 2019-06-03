#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
import tempfile
#from geometries.pillar_1D import *
from geometries.pillar_1D_wrapper import rectangular_holes

def main(argv=None):
  parser = argparse.ArgumentParser()
  
  #default_destdir = os.getenv('TESTDIR')
  default_destdir = tempfile.gettempdir()
  
  parser.add_argument("-d", "--destdir", action="store", type=str, dest="destdir", default=default_destdir, help="destination directory")
  parser.add_argument("-i", type=int, dest="iterations", default=65400+524200+524200, help="number of iterations")
  parser.add_argument("-b", type=int, dest="N_bottom", default=9, help="number of holes at the bottom")
  parser.add_argument("-t", type=int, dest="N_top", default=7, help="number of holes at the top")
  parser.add_argument("-e", type=str, dest="excitationTypeStr", default='Zm1', help="excitationType: Ym1,Ym2,Zm1,Zm2")
  parser.add_argument("-f", type=str, dest="FrequencyList", default='', help="frequency of the frequency snapshots: ex: \"100.1,150.2,200.3,250.4\"")
  
  options = parser.parse_args()
  
  print('destdir = ', options.destdir)
  print('iterations = ', options.iterations)
  print('N_bottom = ', options.N_bottom)
  print('N_top = ', options.N_top)
  print('excitationTypeStr = ', options.excitationTypeStr)
  print('FrequencyList = ', options.FrequencyList)
  
  if len(options.FrequencyList) == 0:
    freq_snapshots = []
  else:
    #print options.FrequencyList.split(',')
    freq_snapshots = [float(x) for x in options.FrequencyList.split(',')]
  print(freq_snapshots)

  excitationType = -1
  if options.excitationTypeStr == 'Ym1':
    excitationType = 0
  elif options.excitationTypeStr == 'Zm1':
    excitationType = 1
  elif options.excitationTypeStr == 'Ym2':
    excitationType = 2
  elif options.excitationTypeStr == 'Zm2':
    excitationType = 3
  print('excitationType = ', excitationType)

  if os.path.isdir(options.destdir):
    rectangular_holes(options.destdir, options.N_bottom, options.N_top, excitationType, options.iterations, freq_snapshots)
  else:
    print('options.destdir = {} is not a directory'.format(options.destdir))

if __name__ == "__main__":
  main()
