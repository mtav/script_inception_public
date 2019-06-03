#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import bfdtd
import argparse
import tempfile
import subprocess

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', help='source .inp file containing original mesh')
  parser.add_argument('outfile', help='destination .inp file to write containing new mesh')
  parser.add_argument('-Nx', type=int, default=1, help='factor by which to increase the resolution in the X direction')
  parser.add_argument('-Ny', type=int, default=1, help='factor by which to increase the resolution in the Y direction')
  parser.add_argument('-Nz', type=int, default=1, help='factor by which to increase the resolution in the Z direction')
  parser.add_argument('-v', '--verbose', action="count", dest="verbosity", default=0, help='verbosity level')
  args = parser.parse_args()
  
  # read input
  sim = bfdtd.readBristolFDTD(args.infile, verbosity=args.verbosity)
  mesh = bfdtd.increaseResolution3D(sim.getMesh(), args.Nx, args.Ny, args.Nz)
  with open(args.outfile, 'w') as fid:
    mesh.writeMesh(fid)
  
  return 0

if __name__ == '__main__':
  main()
