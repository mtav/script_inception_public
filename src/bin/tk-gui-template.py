#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''For playing around with tk GUIs and testing cross-platform support.'''

import os
import re
import sys
import argparse
import tempfile
import subprocess

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('DSTDIR', default=tempfile.gettempdir(), nargs='?')
  parser.add_argument('-v', '--verbose', action="count", dest="verbosity", default=0, help='verbosity level')
  args = parser.parse_args()
  print(args)
  
  DSTDIR = args.DSTDIR
  if not os.path.isdir(DSTDIR):
    os.mkdir(DSTDIR)

  return 0

if __name__ == '__main__':
  main()
