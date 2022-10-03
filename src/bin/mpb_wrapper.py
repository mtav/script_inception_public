#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import subprocess
import shlex

import utilities.common
import MPB.MPB_parser

# .. todo:: improve support for MPB split (each process outputs same because outputs are merged at end? but all joined into same file, so duplicate datasets are generated.)
# .. todo:: move more options into tee_wrapper and/or somehow merge. Need support for exes with options (ex: mpb-split NUM-SPLIT).

# .. todo:: mpb_wrapper.py: "=" sign in path name causes crash (interpreted as parameter) -> this is actually a bug in the MPB and MEEP interpreters (i.e. libctl)!!!

def print_path_info(prefix, path):
  print('{} = {}'.format(prefix, path))
  print('  dirname({}) = {}'.format(prefix, os.path.dirname(path)))
  print('  basename({}) = {}'.format(prefix, os.path.basename(path)))
  return

def main():
  parser = argparse.ArgumentParser(description="A simple wrapper to store the output of mpb and postprocess it into a usable CSV file.",
                                   epilog='Example usage: {} -o test.out a=120 test.ctl'.format(os.path.basename(sys.argv[0])))
  parser.add_argument('-v','--verbose', type=int, default=2, help='Set verbosity level. Default is 2, i.e. output command + command output.')
  parser.add_argument('-d','--workdir')
  parser.add_argument('-o','--outfile')
  parser.add_argument('-s','--suffix', default='', help='Appends a suffix to the default outfile name.')
  parser.add_argument('-a','--automatic-suffix', action='store_true', help='Generates an automatic suffix based on parameters passed to the mpb command. Not used if the --suffix option is also used.')
  parser.add_argument('-p','--automatic-filename-prefix', action='store_true', help='generate a filename-prefix to be used for .h5 files and anything generated from them (.png, .vtk, .vts)')
  parser.add_argument('-n', '--dry-run', action='store_true')
  parser.add_argument('-e', '--output_epsilon_only', action='store_true')
  parser.add_argument('-m', '--merge-datasets', action='store_true')
  parser.add_argument('-r', '--use-relative-paths', action='store_true', help='Use relative paths before running commands. (helps when the path contains unusual characters like "=")')
  parser.add_argument('--h5topng', action='store_true')
  parser.add_argument('--h5topng-options', type=str, default='')
  parser.add_argument('--h5tovtk', action='store_true')
  parser.add_argument('--h5tovts', action='store_true')
  parser.add_argument('--xdg-open', action='store_true')
  parser.add_argument('--mimeopen', action='store_true')
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
  filename_prefix = os.path.join(args.workdir, infile_basename + '-')
  
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
    filename_prefix = os.path.join(os.path.abspath(args.workdir), root + '-')

  extra_parameters = []
  if args.automatic_filename_prefix:
    extra_parameters += ['filename-prefix="'+filename_prefix+'"']

  if args.output_epsilon_only:
    extra_parameters += ['output_epsilon_only?=true']

  if args.use_relative_paths:
    infile = os.path.relpath(infile, start=args.workdir)
    outfile_fullpath = os.path.relpath(outfile_fullpath, start=args.workdir)

  cmd_full = ['mpb'] + extra_parameters + parameters + [infile]

  epsilon_file = filename_prefix + 'epsilon.h5'

  if args.verbose == 1:
    print(f"workdir: {args.workdir} , cmd: {' '.join(cmd_full)}")
  elif args.verbose >= 3:
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
    if args.verbose >= 3:
      print('os.getcwd() = {}'.format(os.getcwd()))
          
    utilities.common.runCommandAndStoreOutput(cmd_full, outfile_fullpath, args.verbose)
    
    
    with open(outfile_fullpath, 'r') as f:
      MPB.MPB_parser.writeCSV(f, verbosity=args.verbose, merge_datasets=args.merge_datasets)

    if args.h5topng:
      h5topng_cmd = ['h5topng'] + shlex.split(args.h5topng_options) + [epsilon_file]
      subprocess.check_call(h5topng_cmd)
      if args.xdg_open:
        subprocess.check_call(['xdg-open', filename_prefix + 'epsilon.png'])
      if args.mimeopen:
        subprocess.check_call(['mimeopen', filename_prefix + 'epsilon.png'])

    if args.h5tovtk:
      subprocess.check_call(['h5tovtk', epsilon_file])
      if args.xdg_open:
        subprocess.check_call(['xdg-open', filename_prefix + 'epsilon.vtk'])
      if args.mimeopen:
        subprocess.check_call(['mimeopen', filename_prefix + 'epsilon.vtk'])

    if args.h5tovts:
      #import shlex
      #cmd = shlex.split('h5tovts.py \""' + epsilon_file + '\""')
      cmd = ['h5tovts.py', '--single-h5file', epsilon_file]
      print(cmd)
      subprocess.check_call(cmd)
      if args.xdg_open:
        subprocess.check_call(['xdg-open', filename_prefix + 'epsilon.vts'])
      if args.mimeopen:
        subprocess.check_call(['mimeopen', filename_prefix + 'epsilon.vts'])
  
  return 0

if __name__ == '__main__':
  main()
