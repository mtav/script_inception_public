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
  if defect_list:
    print(defect_list[0].getOuterRadius())
  else:
    print(0)
  
  return 0

if __name__ == '__main__':
  main()
