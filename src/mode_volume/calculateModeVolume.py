#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# calculates the mode volume

import argparse

def main():
  # command-line option handling
  parser = argparse.ArgumentParser(description = 'calculate mode volume')
  parser.add_argument('infile', action="store", help='input file (.geo, .inp or .in)')
  parser.add_argument('-v','--verbose', action="count", dest="verbosity", default=0, help='verbosity level')

  parser.add_argument('-o','--outfile', action="store", dest="outfile", default=None, help='output file')
  parser.add_argument('-d','--outdir', action="store", dest="outdir", default=None, help='output directory')
  parser.add_argument('-b','--basename', action="store", dest="basename", default=None, help='output basename')

  return

if __name__ == "__main__":
  main()
