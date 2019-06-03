#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to change the index/permittivity of specifically named objects in a simulation.
"""

import sys
import argparse
import bfdtd

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', nargs='+')
  parser.add_argument('-o', '--outdir',required=True)
  parser.add_argument('-b', '--basename',required=True)
  parser.add_argument('-t', '--target', default='defect')
  eps_group = parser.add_mutually_exclusive_group(required=True)
  eps_group.add_argument('-e', '--epsilon', type=float)
  eps_group.add_argument('-n', '--index', type=float)
  
  args = parser.parse_args()
  
  print(args)
  
  # read input
  sim = bfdtd.readBristolFDTD(*args.infile, verbosity=0)
  
  # change index of targets
  obj_list = sim.getGeometryObjectsByName(args.target)
  for obj in obj_list:
    if args.index:
      obj.setRefractiveIndex(args.index)
    else:
      obj.setRelativePermittivity(args.epsilon)

  # create epsilon run of new sim
  sim.setIterations(1)
  sim.setFileBaseName(args.basename)
  sim.setWallTime(120)
  sim.writeTorqueJobDirectory(args.outdir)
  
  return 0

if __name__ == '__main__':
  main()
