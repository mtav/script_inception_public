#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
A wrapper to run BFDTD in smarter ways.

At the moment, the main goal is to always generate the data in the same directory as the input file.
'''

import os
import argparse
from utilities.common import runSimulation

def main():
  '''.. todo:: come up with options later maybe. Ex: clean dir before running, no overwrite, generate .h5, etc. '''
  parser = argparse.ArgumentParser()
  parser.add_argument('-v','--verbose', action="count", dest="verbosity", default=0, help='verbosity level')
  parser.add_argument('infile', nargs='+', help='Input files (usually .in files).')
  parser.add_argument('--exe', help='Executable to run the input files with. Default: fdtd', default='fdtd')
  args = parser.parse_args()
  if args.verbosity >= 1:
    print(args)
  for infile in args.infile:
    print('===> Processing {}'.format(infile))
    runSimulation(args.exe, infile, verbosity=args.verbosity)
  return 0

if __name__ == '__main__':
  main()
