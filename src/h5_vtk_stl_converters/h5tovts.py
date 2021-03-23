#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# works with vtk 6.1.0, i.e. the python-vtk6 package on Debian-based distros
# TODO: Add vtk version checker + eventual multiversion support.

import os
import sys
import vtk
import h5py
import shlex
import argparse
import warnings

import h5utils
from h5utils import MPB_h5tovts, BFDTD_h5_to_vts, h5_getDataSets

def h5tovts_argparse():
  '''
  .. todo:: converting .prn to unstructured .h5 would increase conversion speed (and then of course direct .prn to .vts conversion and/or C++ code)
  '''

  parser = argparse.ArgumentParser(description = 'Convert an MPB-created HDF5 file to a .vts file.')
  parser.add_argument('-v','--verbose', action="count", dest="verbosity", default=0, help='verbosity level')

  parser.add_argument('h5file', action="store", help='input HDF5 file', nargs='+')
  parser.add_argument('--single-h5file', action='store_true', help='If this option is given, all h5file arguments passed are merged together into a single file, i.e. "h5tovts.py a b c.h5" will try to open "a b c.h5". This has been added to deal with spaces in filenames, something python2 has trouble with.')
  #parser.add_argument('vtsfile', action="store", help='output .vts file', nargs='?')
  #parser.add_argument('-b','--basepath', action="store", default=None, help='basepath for output files')
  parser.add_argument('-s','--suffix', action="store", default='', help='additional suffix for output files')

  parser.add_argument('--size', nargs=3, type=float, default=None, help='lattice size (only used for .h5 files without lattice vectors, i.e. MEEP output, not for MPB output.)')
  parser.add_argument('-d', '--dataset', help='use dataset <name> in the input files (default: first dataset)', metavar='name', nargs='+', default=[])

  parser.add_argument('--bfdtd', action='store_true', help='HDF5 file is in the BFDTD format')
  parser.add_argument('-l', '--list', action='store_true', help='list contents only')

  parser.add_argument('--double', action='store_true', help='Use Double instead of Float.')
  parser.add_argument('--real-units', action='store_true', help='Use "real units", i.e. multiply by epsilon0/mu0 for energy densities.')

  parser.add_argument('--x-range', default=[0,1], type=float, nargs=2)
  parser.add_argument('--y-range', default=[0,1], type=float, nargs=2)
  parser.add_argument('--z-range', default=[0,1], type=float, nargs=2)

  parser.add_argument('-n', '--dry-run', action='store_true', help='Just do a dry/test-run.')

  if sys.version_info.major >= 3:
    arguments = parser.parse_args()
  else:
    arguments = parser.parse_args(shlex.split(' '.join(sys.argv[1:]))) # fix for python2, to allow passing multiple filenames with spaces, by surrounding them with escaped quotes, i.e. \"a b c\"

  if arguments.verbosity > 0:
    print('---------')
    print(arguments)
    print('---------')
  
  if not len(sys.argv) > 1:
    parser.print_help()
  else:
    #if arguments.basepath is None:
      #arguments.basepath = os.path.splitext(arguments.h5file)[0]
    if arguments.double:
      h5utils.vtkScalarArray = vtk.vtkDoubleArray      

    if arguments.single_h5file:
      arguments.h5file = [' '.join(arguments.h5file)]
      
    for h5file in arguments.h5file:
      if not os.path.exists(h5file):
        warnings.warn('Error: File not found: {}'.format(h5file))
        warnings.warn('If the filename contains spaces, simply use the --single-h5file option (for a single input file). For multiple files, use escaped double quotes, i.e. \"a b c\", or even \"" if there are parentheses, etc.')
        continue
      
      basepath = os.path.splitext(h5file)[0] + arguments.suffix
      if arguments.list:
        with h5py.File(h5file, "r") as HDF5_file_object:
          h5_getDataSets(HDF5_file_object)
      else:
        print('==> {} -> {}.vts and/or {}.vti'.format(h5file, basepath, basepath))
        # .. todo:: might be worth switching to a class/object to reduce argument length?
        if arguments.bfdtd:
          BFDTD_h5_to_vts(h5file, basepath, arguments.size, arguments.dataset, arguments.verbosity, arguments.x_range, arguments.y_range, arguments.z_range, arguments.real_units, arguments.dry_run)
        else:
          MPB_h5tovts(h5file, basepath, arguments.size, arguments.dataset, arguments.verbosity)
  
  return

if __name__ == '__main__':
  h5tovts_argparse()
