#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Rename folders based on parameters from BFDTD input files.
"""

import argparse
import sys
import re
import os
import bfdtd.bfdtd_parser as bfdtd
import textwrap

def get_argument_parser():
  '''
  command-line option handling
  '''

  parser = argparse.ArgumentParser(description = 'Rename folders based on parameters from BFDTD input files.')
  parser.add_argument('--BFDTDreader-verbosity', type=int, default=0, help='verbosity level of the BFDTD reader')
  parser.add_argument('-v','--verbose', action="count", dest="verbosity", default=0, help='verbosity level')
  parser.add_argument("-n", "--no-act", action="store_true", dest="no_act", default=False, help="No Action: show what links would have been retargeted or removed.")
  parser.add_argument('--not-interactive', help='Do not prompt before applying changes.', action="store_true", default=False)

  subparsers = parser.add_subparsers(help='Available subcommands')

  # parser for rename
  parser_rename = subparsers.add_parser('rename', help='Rename directories based on parameters from some BFDTD files within them.',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent('''
    The renaming works as follows:
    
      newdir_subbed = re.sub(arguments.pattern, arguments.repl, orig_dir)
      newdir_formatted = newdir_subbed.format(snapfreq=list(sim_in.getSnapshotFrequencySet()))
      
    Interpreted sequences are:
      snapfreq : a list of unique frequencies used in the frequency snapshots.
      freqsnap_first
      freqsnap_repetition
      freqsnap_starting_sample
      
    So you can use the following for example:
      {snapfreq} : all snapshot frequencies
      {snapfreq[IDX]} : a specific snapshot frequency (but because it's a set, the indexing is a bit random...)

    Example usage:
      bfdtd_rename.py rename  -i "part_1/woodpile.in" -p ".*" -r "\g<0>.snapfreq_{snapfreq[0]}" *
    '''))

  parser_rename.add_argument('-i','--infile', required=True, help='BFDTD input files to read. (specify the path relative to the directories to process)', action='append', default=[])
  parser_rename.add_argument('-p','--pattern', required=True, help='pattern to look for')
  parser_rename.add_argument('-r','--repl', required=True, help='string with which to replace the matched pattern')
  parser_rename.add_argument('dirs', nargs='+', help='The directories you want to rename.')
  
  parser_rename.set_defaults(func=rename)
  
  return parser

def rename(arguments):
  
  for orig_dir in arguments.dirs:

    if arguments.verbosity > 0:
      print('===> Processing {}'.format(orig_dir))
    
    if not os.path.isdir(orig_dir):
      print('ERROR: {} is not a valid directory. Skipping it.'.format(orig_dir), file=sys.stderr)
      continue
    
    sim_in = bfdtd.BFDTDobject()
    sim_in.verbosity = arguments.BFDTDreader_verbosity
    
    for infile in arguments.infile:
      ret = sim_in.readBristolFDTD(os.path.join(orig_dir, infile))
      if ret != 0:
        # if reading one file fails
        break
      
    if ret != 0:
      print('ERROR: Failed to read {}. Skipping {}.'.format(infile, orig_dir), file=sys.stderr)
      continue
    
    freqsnap_first = set()
    freqsnap_repetition = set()
    freqsnap_starting_sample = set()
    
    for i in sim_in.getFrequencySnapshots():
      freqsnap_first.add(int(i.first))
      freqsnap_repetition.add(int(i.repetition))
      freqsnap_starting_sample.add(int(i.starting_sample))
    
    freqsnap_first = list(freqsnap_first)
    freqsnap_repetition = list(freqsnap_repetition)
    freqsnap_starting_sample = list(freqsnap_starting_sample)
    
    newdir_subbed = re.sub(arguments.pattern, arguments.repl, orig_dir)
    
    try:
      newdir_formatted = newdir_subbed.format(
        snapfreq = list(sim_in.getSnapshotFrequencySet()),
        freqsnap_first = freqsnap_first,
        freqsnap_repetition = freqsnap_repetition,
        freqsnap_starting_sample = freqsnap_starting_sample)
        
    except IndexError as err:
      print("ERROR: IndexError: {0}".format(err), file=sys.stderr)
      print("ERROR: Skipping", orig_dir, file=sys.stderr)
    except:
      print("ERROR: Unexpected error:", sys.exc_info()[0], file=sys.stderr)
      print("ERROR: Skipping", orig_dir, file=sys.stderr)
    else:
      if arguments.verbosity > 1:
        print('{} -> {} -> {}'.format(orig_dir, newdir_subbed, newdir_formatted))
      if arguments.not_interactive:
        ans = 'y'
      else:
        ans = input('Rename {} to {}? (y/n): '.format(orig_dir, newdir_formatted)).strip()
      if ans == 'y':
        if not arguments.no_act:
          if not os.path.isdir(orig_dir):
            print('ERROR:',orig_dir,'is not a directory!!! Aborting to avoid overwriting files while renaming.', file=sys.stderr)
            sys.exit(-1)
          os.renames(orig_dir, newdir_formatted)
        print('{} -> {}'.format(orig_dir, newdir_formatted))
      else:
        print('Doing nothing.')
    
  return

def main():
  parser = get_argument_parser()
  arguments = parser.parse_args()

  if arguments.verbosity > 0:
    print('---------')
    print(arguments)
    print('---------')
  
  if not len(sys.argv) > 1 or 'func' not in arguments:
    parser.print_help()
  else:
    arguments.func(arguments)

  return(0)

if __name__ == "__main__":
  main()
