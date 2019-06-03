#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import os
import sys
import argparse
import subprocess
import tempfile
import textwrap

import utilities.common

import MEEP.MEEP_parser

# .. todo:: report MEEP BUG: Unlike MPB, MEEP does not support absolute paths in the filename-prefix (because it prepends ./ in all cases)
# .. todo:: Add support for string formatting? (ex: "%02d" number formatting?) (but manual suffix definition can help with that already...(just make sure .png&co naming ok))

def print_path_info(prefix, path):
  print('{} = {}'.format(prefix, path))
  print('  dirname({}) = {}'.format(prefix, os.path.dirname(path)))
  print('  basename({}) = {}'.format(prefix, os.path.basename(path)))
  return

def main():
  parser = argparse.ArgumentParser(description="A simple wrapper to store the output of meep and postprocess it into a usable CSV file.",
                                   epilog='Example usage: {} -o test.out a=120 test.ctl'.format(os.path.basename(sys.argv[0])))
  parser.add_argument('-v','--verbose', type=int, default=2, help='Set verbosity level. Default is 2, i.e. output command + command output.', dest='verbosity')
  parser.add_argument('-d','--workdir')
  parser.add_argument('-o','--outfile')
  parser.add_argument('-s','--suffix', default='', help='Appends a suffix to the default outfile name.')
  parser.add_argument('-a','--automatic-suffix', action='store_true', help='Generates an automatic suffix based on parameters passed to the meep command. Not used if the --suffix option is also used.')
  parser.add_argument('-p','--automatic-filename-prefix', action='store_true', help='generate a filename-prefix to be used for .h5 files and anything generated from them (.png, .vtk, .vts)')
  parser.add_argument('-n', '--dry-run', action='store_true')
  parser.add_argument('-e', '--output_epsilon_only', action='store_true')
  parser.add_argument('--disable-run-functions', action='store_true', help='Disable run functions. Useful to only print the geometry info without having to edit the .ctl file.')
  parser.add_argument('--direct-parsing', action='store_true', help='Do not create a .out file. Read the .ctl file and get the info from there "directly".')
  parser.add_argument('-r', '--reference-run', action='store_true', help='This will add the "reference_run?=true" parameter to the meep command. By default, "reference_run?=false" is used.')
  parser.add_argument('-m', '--merge-datasets', action='store_true')
  parser.add_argument('--h5topng', action='store_true')
  parser.add_argument('--h5tovtk', action='store_true')
  parser.add_argument('--h5tovts', action='store_true')
  parser.add_argument('--xdg-open', action='store_true')
  parser.add_argument('--mimeopen', action='store_true')
  parser.add_argument('--grep-flux', action='store_true')
  parser.add_argument('cmd', nargs=argparse.REMAINDER, help='Must include at least one input file as final argument.')
  args = parser.parse_args()

  if not args.cmd:
    parser.print_help()
    sys.exit()
  
  parameters = args.cmd[:-1]
  infile = os.path.abspath(args.cmd[-1])
  if not os.path.exists(infile):
    raise Exception('File not found: {}'.format(infile))

  (infile_root, ext) = os.path.splitext(infile)
  infile_basename = os.path.basename(infile_root)
  infile_dirname = os.path.dirname(infile_root)

  if not args.workdir:
    args.workdir = infile_dirname

  args.workdir = os.path.abspath(args.workdir)
  print('args.workdir = {}'.format(args.workdir))
  filename_prefix = infile_basename
  print('filename_prefix = {}'.format(filename_prefix))
  
  if not args.outfile:
    if args.suffix:
      if len(args.suffix)>=1 and args.suffix[0]!='.':
        args.suffix = '.' + args.suffix
    elif args.automatic_suffix and len(parameters)>0:
      args.suffix = '.' + '.'.join(parameters)
    args.outfile = infile_basename + args.suffix + '.out'
  
  outfile_fullpath = os.path.join(args.workdir, args.outfile)
  
  if args.automatic_filename_prefix:
    (root, ext) = os.path.splitext(args.outfile)
    filename_prefix = root
    print('filename_prefix = {}'.format(filename_prefix))
  
  
  extra_parameters = []
  if args.automatic_filename_prefix:
    extra_parameters += ['filename-prefix="'+filename_prefix+'"']
  
  if args.output_epsilon_only:
    extra_parameters += ['output_epsilon_only?=true']
  
  if args.reference_run:
    extra_parameters += ['reference_run?=true']
    # hack for reference runs
    outfile_fullpath = os.path.splitext(outfile_fullpath)[0] + '.ref.out'
  else:
    extra_parameters += ['reference_run?=false']

  cmd_full = ['meep'] + extra_parameters + parameters + [infile]
  
  # create a special infile redefining the run functions
  if args.disable_run_functions:
    wrapper_file = MEEP.MEEP_parser.createWrapperFile(infile)
    cmd_full = ['meep'] + extra_parameters + parameters + [wrapper_file]
    if args.verbosity >= 3:
      print('wrapper_file = {}'.format(wrapper_file))
  
  if args.direct_parsing:
    (MEEP_data_list, geo_list) = MEEP.MEEP_parser.getInfoFromCTL(infile)
    MEEP.MEEP_parser.printInfo(MEEP_data_list, geo_list, verbosity=args.verbosity)
    return
  
  epsilon_suffix = '-eps-000000.00'
  epsilon_file = filename_prefix + epsilon_suffix + '.h5'
  
  if args.verbosity >= 3:
    print(args)
    print('workdir = {}'.format(args.workdir))    
    
    print_path_info('infile', infile)
    print_path_info('outfile', outfile_fullpath)
    print_path_info('filename_prefix', filename_prefix)
    print_path_info('epsilon_file', epsilon_file)
    
    #print('infile = {}'.format(infile))
    #print('outfile_fullpath = {}'.format(outfile_fullpath))
    #print('outfile_dirname = {}'.format(os.path.dirname(outfile_fullpath)))
    #print('outfile_basename = {}'.format(os.path.basename(outfile_fullpath)))
    #print('filename_prefix = {}'.format(filename_prefix))
    #print('epsilon_file = {}'.format(epsilon_file))
    
    print('extra_parameters = {}'.format(extra_parameters))
    print('parameters = {}'.format(parameters))
    print('cmd:\n {}'.format(' '.join(cmd_full)))
  
  if not args.dry_run:
    if args.workdir:
      if not os.path.exists(args.workdir):
        os.makedirs(args.workdir)
      os.chdir(args.workdir)
    if args.verbosity >= 3:
      print('os.getcwd() = {}'.format(os.getcwd()))
    utilities.common.runCommandAndStoreOutput(cmd_full, outfile_fullpath, args.verbosity)
    
    if args.grep_flux:
      cmdgrep = ['grep', 'flux1:', outfile_fullpath]
      datfile = os.path.splitext(outfile_fullpath)[0] + '.dat'
      utilities.common.runCommandAndStoreOutput(cmdgrep, datfile, args.verbosity)

    if args.h5topng:
      subprocess.check_call(['h5topng', epsilon_file])
      if args.xdg_open:
        subprocess.check_call(['xdg-open', filename_prefix + epsilon_suffix + '.png'])
      if args.mimeopen:
        subprocess.check_call(['mimeopen', filename_prefix + epsilon_suffix + '.png'])

    if args.h5tovtk:
      subprocess.check_call(['h5tovtk', epsilon_file])
      if args.xdg_open:
        subprocess.check_call(['xdg-open', filename_prefix + epsilon_suffix + '.vtk'])
      if args.mimeopen:
        subprocess.check_call(['mimeopen', filename_prefix + epsilon_suffix + '.vtk'])

    if args.h5tovts:
      #import shlex
      #cmd = shlex.split('h5tovts.py \""' + epsilon_file + '\""')
      cmd = ['h5tovts.py', '--single-h5file', epsilon_file]
      print(cmd)
      subprocess.check_call(cmd)
      if args.xdg_open:
        subprocess.check_call(['xdg-open', filename_prefix + epsilon_suffix + '.vts'])
      if args.mimeopen:
        subprocess.check_call(['mimeopen', filename_prefix + epsilon_suffix + '.vts'])
  
  return 0

if __name__ == '__main__':
  main()
