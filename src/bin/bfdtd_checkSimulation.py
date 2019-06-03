#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import bfdtd
import argparse
import tempfile

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile', nargs='+')
  parser.add_argument('-v', '--verbose', action="count", dest="verbosity", default=0, help='verbosity level')
  parser.add_argument('-c', '--continue-on-error', action="store_true", help='continue on errors')
  args = parser.parse_args()
  
  if args.verbosity > 0:
    print(args)
  
  ok = []
  fail = []
  
  for infile in args.infile:
    sim = bfdtd.readBristolFDTD(infile, verbosity=args.verbosity)
    sim.setVerbosity(args.verbosity)
    #sim.setSafetyChecks(False)
    try:
      sim.checkSimulation()
    except Exception as inst:
      print('{} : FAIL -> {}'.format(infile, inst.args))
      fail.append(infile)
      if not args.continue_on_error:
        raise
    except:
      print('Unexpected exception!:')
      raise
    else:
      print('{} : OK'.format(infile))
      ok.append(infile)
    
  print('OK: {}/{}'.format(len(ok), len(args.infile)) )
  print('FAIL: {}/{}'.format(len(fail), len(args.infile)))
  print('N(total)-N(ok)-N(fail) = {}'.format(len(args.infile) - len(ok) - len(fail)))
  return 0

if __name__ == '__main__':
  main()

