#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import subprocess

import utilities.common

def main():
  parser = argparse.ArgumentParser(description="A simple wrapper to store output of commands such as mpb, meep or fdtd in a file. By default the output file will be FILE.out if the input file is FILE.EXT (ex: FILE.ctl -> FILE.out, FILE.in -> FILE.out)",
                                   epilog='Example usage: {} -o test.out mpb a=120 test.ctl'.format(os.path.basename(sys.argv[0])))
  parser.add_argument('-v','--verbose', type=int, default=2, help='Set verbosity level. Default is 2, i.e. output command + command output.')
  parser.add_argument('-o','--outfile')
  parser.add_argument('-s','--suffix', default='', help='Not used if the --outfile option is used. Else, the suffix is appended to the default outfile name.')
  parser.add_argument('-n', '--dry-run', action='store_true')  
  parser.add_argument('cmd', nargs=argparse.REMAINDER, help='Must include at least one input file as final argument.')
  args = parser.parse_args()
  
  if not args.cmd:
    parser.print_help()
    sys.exit()
  
  infile = args.cmd[-1]
  if not os.path.exists(infile):
    raise Exception('File not found: {}'.format(infile))
  
  if not args.outfile:
    if args.suffix:
      if len(args.suffix)>=1 and args.suffix[0]!='.':
        args.suffix = '.' + args.suffix
    (root, ext) = os.path.splitext(infile)
    args.outfile = root + args.suffix + '.out'
  
  if args.verbose >= 3:
    print(args)
    print('cmd = {}'.format(args.cmd))
    print('infile = {}'.format(infile))
    print('outfile = {}'.format(args.outfile))
  
  if not args.dry_run:
    utilities.common.runCommandAndStoreOutput(args.cmd, args.outfile, args.verbose)
  
  return 0

if __name__ == '__main__':
  main()
