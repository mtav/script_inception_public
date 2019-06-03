#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import sys
import argparse
from numpy import array, zeros, sqrt, linspace

from h5utils import stltoh5, Lattice, FCClattice, BCClattice

def stltoh5_argparse():
  
  # command-line option handling
  parser = argparse.ArgumentParser(description = 'Convert an STL file to an HDF5 file for use with MPB, as well as a .vtp and .vts file for reference.')
  parser.add_argument('-v','--verbose', action="count", dest="verbosity", default=0, help='verbosity level')

  #parser.add_argument('--stlfile', action="store", help='input STL file', required=True)
  parser.add_argument('stlfile', action="store", help='input STL file')
  parser.add_argument('-b','--basepath', action="store", default=None, help='basepath for output files')

  material_inside = parser.add_mutually_exclusive_group()
  material_inside.add_argument('--epsilon_inside', type=float, default=12, help='relative epsilon of the inner material')
  material_inside.add_argument('--n_inside', type=float, default=None, help='refractive index of the inner material')

  material_outside = parser.add_mutually_exclusive_group()
  material_outside.add_argument('--epsilon_outside', type=float, default=1, help='relative epsilon of the outer material')
  material_outside.add_argument('--n_outside', type=float, default=None, help='refractive index of the outer material')

  lattice_group = parser.add_argument_group('lattice')
  lattice_group.add_argument('--basis1', nargs=3, type=float, help='lattice vector basis1', metavar=('X','Y','Z'))
  lattice_group.add_argument('--basis2', nargs=3, type=float, help='lattice vector basis2', metavar=('X','Y','Z'))
  lattice_group.add_argument('--basis3', nargs=3, type=float, help='lattice vector basis3', metavar=('X','Y','Z'))
  lattice_group.add_argument('--basis-size', nargs=3, type=float, help='lattice basis size')
  lattice_group.add_argument('--size', nargs=3, type=float, default=[1,1,1], help='lattice size')
  lattice_group.add_argument('--Ncells', nargs=3, type=int, default=[100,100,100], help='number of cells in the grid in a given direction. i.e. total number of cells will be Ncells^3', metavar=('Nx','Ny','Nz'))

  lattice_presets_group = parser.add_argument_group(title='lattice preset configurations', description='You can use these instead of the basis and basis-size options. Any additional basis and basis-size specifications will be applied afterwards, allowing you to change part of the preset configuration.')
  lattice_presets = lattice_presets_group.add_mutually_exclusive_group()
  lattice_presets.add_argument('--FCC', dest='preset', action='store_const', const='FCC', help='Use a "standard FCC lattice" (face centered cubic).')
  lattice_presets.add_argument('--BCC', dest='preset', action='store_const', const='BCC', help='Use a "standard BCC lattice" (body centered cubic).')

  arguments = parser.parse_args()

  if arguments.verbosity > 0:
    print('---------')
    print(arguments)
    print('---------')
  
  if not len(sys.argv) > 1:
    parser.print_help()
  else:

    if arguments.n_inside:
      epsilon_inside = pow(arguments.n_inside, 2)
    elif arguments.epsilon_inside:
      epsilon_inside = arguments.epsilon_inside
    else:
      raise

    if arguments.n_outside:
      epsilon_outside = pow(arguments.n_outside, 2)
    elif arguments.epsilon_outside:
      epsilon_outside = arguments.epsilon_outside
    else:
      raise

    if arguments.basepath is None:
      (arguments.basepath, ext) = os.path.splitext(arguments.stlfile)

    # set up lattice
    lattice = Lattice()
    if arguments.preset is 'FCC':
      lattice = FCClattice()
    elif arguments.preset is 'BCC':
      lattice = BCClattice()

    if arguments.basis1:
      lattice.basis1 = array(arguments.basis1)
    if arguments.basis2:
      lattice.basis2 = array(arguments.basis2)
    if arguments.basis3:
      lattice.basis3 = array(arguments.basis3)
    if arguments.basis_size:
      lattice.basis_size = arguments.basis_size

    lattice.size = arguments.size
    lattice.setResolution(arguments.Ncells[0], arguments.Ncells[1], arguments.Ncells[2])

    print('--> arguments:')
    print('n_inside = {}'.format( sqrt(epsilon_inside) ))
    print('epsilon_inside = {}'.format( epsilon_inside ))
    print('n_outside = {}'.format( sqrt(epsilon_outside) ))
    print('epsilon_outside = {}'.format( epsilon_outside ))
    print('stlfile = {}'.format( arguments.stlfile ))
    print('basepath = {}'.format( arguments.basepath ))
    print(lattice)

    stltoh5(arguments.stlfile, arguments.basepath, epsilon_inside, epsilon_outside, lattice, arguments.verbosity)
    
    return 0

if __name__ == '__main__':
  stltoh5_argparse()
