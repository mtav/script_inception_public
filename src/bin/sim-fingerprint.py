#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import bfdtd
import argparse

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', nargs='+')
  args = parser.parse_args()

  sim = bfdtd.readBristolFDTD(*args.infile, verbosity=0)
  
  defect_list = sim.getGeometryObjectsByName('defect')
  if len(defect_list)!=1:
    raise Exception('invalid number of defects found!: len(defect_list)={}'.format(len(defect_list)) )
  defect_radius = defect_list[0].getOuterRadius()
  defect_permittivity = defect_list[0].getRelativePermittivity()

  freq_set = sim.getSnapshotFrequencySet()
  if len(freq_set)!=1:
    raise Exception('invalid number of frequencies found!: len(freq_set)={}'.format(len(freq_set)) )
  freq = freq_set.pop()
  
  print('{};{};{}'.format(defect_permittivity, defect_radius, freq))
  
  return 0

if __name__ == '__main__':
  main()
