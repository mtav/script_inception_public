#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import bfdtd
import argparse
import tempfile
import subprocess

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile')
  parser.add_argument('-v', '--verbose', action="count", dest="verbosity", default=0, help='verbosity level')
  args = parser.parse_args()
  
  print('=== {} ==='.format(args.infile))
  sim = bfdtd.BFDTDobject()
  sim.setVerbosity(args.verbosity)
  sim.readBristolFDTD(args.infile)
  m = sim.getMesh()
  print(m.getMinDeltas())
  
  return 0
  
if __name__ == '__main__':
  main()
