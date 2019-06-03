#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#ctltovtk is even better!
#UNIX philosophy
#do one thing and do it well!

import os
import argparse
import tempfile

import bfdtd

def main():
  raise Exception('Unfinished script')
  
  parser = argparse.ArgumentParser()
  parser.add_argument('geofile', nargs='+')
  parser.add_argument('-o', '--outfile', help='Save  all  the input GEO files to a single CTL file.')
  parser.add_argument('--no-offset', action="store_true")
  parser.add_argument('-v', '--verbose', action="count", dest="verbosity", default=0, help='verbosity level')
  args = parser.parse_args()
  
  if args.verbosity > 0:
    print(args)
  
  if args.outfile:
    ctlfile = args.outfile
    print('{} -> {}'.format(args.geofile, ctlfile))
    sim = bfdtd.readBristolFDTD(*args.geofile, verbosity=args.verbosity)
    sim.writeCtlFile(ctlfile, no_offset = args.no_offset)
  else:
    for geofile in args.geofile:
      #ctlfile = os.path.splitext(args.geofile)[0] + '.ctl'
      ctlfile = geofile + '.ctl'
      print('{} -> {}'.format(geofile, ctlfile))
      sim = bfdtd.readBristolFDTD(geofile, verbosity=args.verbosity)
      sim.writeCtlFile(ctlfile, no_offset = args.no_offset)

  return 0

if __name__ == '__main__':
  main()
