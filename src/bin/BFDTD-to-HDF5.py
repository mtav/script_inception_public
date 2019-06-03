#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

def main():
  # argument parsing
  parser = argparse.ArgumentParser(description = 'Convert BFDTD output into HDF5 files.')
  parser.add_argument('-v','--verbose', action="count", dest="verbosity", default=0, help='verbosity level')

  parser.add_argument('h5file', action="store", help='input HDF5 file', nargs='+')
  parser.add_argument('h5file', action="store", help='input HDF5 file', nargs='+')
  parser.add_argument('h5file', action="store", help='input HDF5 file', nargs='+')
  #parser.add_argument('vtsfile', action="store", help='output .vts file', nargs='?')
  #parser.add_argument('-b','--basepath', action="store", default=None, help='basepath for output files')

  parser.add_argument('--size', nargs=3, type=float, default=None, help='lattice size (only used for .h5 files without lattice vectors, i.e. MEEP output, not for MPB output.)')
  parser.add_argument('-d', '--dataset', help='use dataset <name> in the input files (default: first dataset)', metavar='name')

  arguments = parser.parse_args()

  if arguments.verbosity > 0:
    print('---------')
    print(arguments)
    print('---------')

  # read in frequency run input files
  # read in frequency run output files
  # read in epsilon run input files
  # read in epsilon run output files
  # compute energy density
  # write HDF5 file
  
  return 0

if __name__ == '__main__':
  main()
