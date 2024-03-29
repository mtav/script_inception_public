#!/usr/bin/env python3

import argparse
import random
import subprocess
import time
import os
import glob
import bin.qstat
import sys
import textwrap

from datetime import datetime

testmode=False

def qsub(fsp_file):
  if testmode:
    foo = random.choices(['/foo', '/'], weights=[10,1])[0]
    s = subprocess.run(['ls','-d',foo], capture_output=True)
  else:
    cmd=['fdtd-run-pbs.sh', fsp_file]
    s = subprocess.run(cmd, capture_output=True)
  if s.returncode==0:
    return True
  else:
    return False
  # return random.choices([True, False], weights=[1,1000])[0]

def qsubMassive(fsp_files):
  successful_submissions=0
  attempts=0
  N = len(fsp_files)
  for idx, f in enumerate(fsp_files):
    print(f'[{datetime.now()}] Submitting job {idx+1}/{N}: {f}')
    q=False
    while(not q):
      q=qsub(f)
      attempts+=1
      if q:
        successful_submissions+=1
      else:
        nsec=15*60
        print(f'[{datetime.now()}] Sleeping {nsec} seconds...')
        time.sleep(nsec)

  print(f'successful_submissions: {successful_submissions}/{N} after {attempts} attempts')
  return

def checkStatus(fsp_file, job_dict):
  
  ##### default status
  status='unknown'
  
  ##### get various related filenames
  # BASE=os.path.basename(fsp_file)
  fsp_file_fullpath = os.path.realpath(fsp_file)
  DIR, BASE_FSP = os.path.split(fsp_file_fullpath)
  BASE,EXT = os.path.splitext(BASE_FSP)
  sh_file = BASE+'.sh'
  log_file = BASE+'_p0.log'
  fsp_tmp_file = BASE+'.fsp.tmp'
  out_file_list = glob.glob(os.path.join(DIR, BASE+'.sh.o*'))
  err_file_list = glob.glob(os.path.join(DIR, BASE+'.sh.e*'))
  
  ##### check if a related job is currently in the PBS system
  sh_file_fullpath = os.path.join(DIR, BASE+'.sh')
  # print(f'sh_file_fullpath: {sh_file_fullpath}')
  # print(sh_file_fullpath in job_dict.keys())
  # raise
  if sh_file_fullpath in job_dict.keys():
    status = job_dict[sh_file_fullpath]['job_state']
  else:
    status = 'not submitted' # new default status
  
    ##### check success/failure of past jobs
    out_file_list_success = []
    for f_path in out_file_list:
      with open(f_path) as f:
        s=f.read()
        out_file_list_success.append('finished' in s)
        
    # if .o files have been found, check them for success or failure.
    # TODO: deal with .o files from previous runs, in case jobs have been resubmitted..., i.e. qstat output should be checked first!
    if len(out_file_list_success)>0:
      if any(out_file_list_success):
        if os.stat(fsp_file_fullpath).st_size == 0:
          status = 'empty'
        else:
          status = 'success'
      else:
        status = 'failed'
  
  return status

def cleanupJob(fsp_file, dry_run=False, verbosity=0):
  ##### get various related filenames
  fsp_file_fullpath = os.path.realpath(fsp_file)
  DIR, BASE_FSP = os.path.split(fsp_file_fullpath)
  BASE, EXT = os.path.splitext(BASE_FSP)
  
  sh_file = BASE+'.sh'
  log_file = BASE+'_p0.log'
  fsp_tmp_file = BASE+'.fsp.tmp'
  
  sh_file_fullpath = os.path.join(DIR, sh_file)
  log_file_fullpath = os.path.join(DIR, log_file)
  fsp_tmp_file_fullpath = os.path.join(DIR, fsp_tmp_file)
  
  out_file_list = glob.glob(os.path.join(DIR, BASE+'.sh.o*'))
  err_file_list = glob.glob(os.path.join(DIR, BASE+'.sh.e*'))  
  
  generated_files = [sh_file_fullpath, log_file_fullpath, fsp_tmp_file_fullpath]
  generated_files.extend(out_file_list)
  generated_files.extend(err_file_list)
  for i in generated_files:
    if os.path.exists(i):
      if not dry_run:
        if verbosity>0:
          print(f'Removing {i}')
        os.remove(i)
      else:
        print(f'Would remove {i}')
      
  return

def listJobs(args):
  N = len(args.fsp_files)

  #sys.stderr.close()
  job_dict = bin.qstat.getUserJobDict()

  status_dict = dict()
  status_dict['success'] = []
  status_dict['failed'] = []
  status_dict['not submitted'] = []
  status_dict['Q'] = []
  status_dict['R'] = []
  status_dict['C'] = []

  ncols = int(subprocess.check_output(['tput','cols']))

  for idx, f in enumerate(args.fsp_files):
    status = checkStatus(f, job_dict)
    status_dict[status].append(f)
    # if status[-3]:
    if args.verbosity >=1:
      print(f'Job {idx+1}/{N}: {f} -> status : {status}')
    else:
      info_str_1 = f'Job {idx+1}/{N}:'
      info_str_2 = f'{f}'
      info_str_3 = f' -> status : {status}'
      max_len = ncols - 2 - len(info_str_1) - len(info_str_3)
      if len(info_str_2) > max_len:
        if max_len > 3:
          info_str_2 = '...'+info_str_2[-(max_len-3):]
        else:
          info_str_2 = max_len*'.'
      info_str = info_str_1 + info_str_2 + info_str_3
      N_spaces = (ncols - len(info_str) - 2) # Negative values lead to empty strings. :)
      print( '[' + info_str + N_spaces*' ' + ']', end='\r')

  print()

  for k in status_dict.keys():
    Nk = len(status_dict[k])
    print(f'{k} : {Nk}')
    if 0 < Nk and Nk <= 10:
      for i in status_dict[k]:
        print(f'  {i}')
  
  if len(status_dict['failed']) > 0:
    print()
    Nk = len(status_dict['failed'])
    print(f'failed : {Nk}')
    for i in status_dict['failed']:
      print(f'  {i}')
    print()
    if input('Resubmit failed jobs? (y=yes, n=no)')=='y':
      qsubMassive(status_dict['failed'])

def submitJobs(args):
  qsubMassive(args.fsp_files)
  return

def subCommand_cleanupJobs(args):
  for idx, f in enumerate(args.fsp_files):
    print(f'==> {idx+1}/{len(args.fsp_files)}: {f}')
    cleanupJob(f, dry_run=args.dry_run, verbosity=args.verbosity)
  return

def runLumericalScript(lsf_file, fsp_file, dry_run=False, workdir=None):
  cmd = ['fdtd-solutions', '-nw', '-run', lsf_file, fsp_file]
  print('----> Running Lumerical:')
  print('workdir:', workdir)
  print('cmd:')
  print(f"  {' '.join(cmd)}")
  if not dry_run:
    subprocess.run(cmd, cwd=workdir)

def createLumericalScript(lsf_file, script_txt, dry_run=False):
  # create LSF script
  print(f'----> Creating file {lsf_file} with these contents:')
  print('----')
  print(script_txt.strip())
  print('----')
  if not dry_run:
    with open(lsf_file, "w") as f:
        f.write(script_txt)
  return

def subCommand_savesweepJobs(args):
  print(args)

  workdir = os.path.relpath(os.path.dirname(os.path.abspath(args.fsp_file)))
  print('workdir:', workdir)

  base, ext = os.path.splitext(os.path.basename(args.fsp_file))
  lsf_file = os.path.join(workdir, f'{base}.savesweep.lsf')
  print('lsf_file:', lsf_file)

  script_txt = textwrap.dedent(f'''\
                write('write: Creating files for sweep {args.sweepname}...');
                savesweep('{args.sweepname}');
                write('write: DONE');
                ''')

  createLumericalScript(lsf_file, script_txt, dry_run=args.dry_run)
  runLumericalScript(lsf_file, args.fsp_file, dry_run=args.dry_run, workdir=workdir)

def subCommand_loadsweepJobs(args):
  print(args)

  workdir = os.path.relpath(os.path.dirname(os.path.abspath(args.fsp_file)))
  print('workdir:', workdir)

  base, ext = os.path.splitext(os.path.basename(args.fsp_file))
  lsf_file = os.path.join(workdir, f'{base}.loadsweep.lsf')
  print('lsf_file:', lsf_file)

  script_txt = textwrap.dedent(f'''\
                write('write: Loading files for sweep {args.sweepname}...');
                loadsweep('{args.sweepname}');
                write('write: DONE');
                ''')

  createLumericalScript(lsf_file, script_txt, dry_run=args.dry_run)
  runLumericalScript(lsf_file, args.fsp_file, dry_run=args.dry_run, workdir=workdir)

def subCommand_runscriptJobs(args):
  lsf_file = os.path.abspath(args.lsf_file)
  print('lsf_file:', lsf_file)
  for idx, f in enumerate(args.fsp_files):
    workdir = os.path.relpath(os.path.dirname(os.path.abspath(f)))
    runLumericalScript(lsf_file, f, dry_run=args.dry_run, workdir=workdir)
  
def main():
  parser = argparse.ArgumentParser(description='Manage lumerical jobs.')
  # parser.add_argument('fsp_files', metavar='FSP', nargs='+', help='.fsp files')
  parser.add_argument('-v','--verbose', type=int, default=0, help='Set verbosity level. Default is 0.', dest='verbosity')
  # parser.add_argument('--submit', action='store_true', help='Submit simulations')
  # parser.add_argument('--resubmit', action='store_true', help='Resubmit failed simulations')
  
  subparsers = parser.add_subparsers(title='Available sub-commands')

  # create the parser for the "list" command
  parser_list = subparsers.add_parser('list', help='Check job status.')
  parser_list.add_argument('fsp_files', metavar='FSP', nargs='+', help='.fsp files')
  # parser_list.add_argument('--resubmit', action='store_true', help='Resubmit failed simulations')
  parser_list.set_defaults(func=listJobs)

  # create the parser for the "submit" command
  parser_submit = subparsers.add_parser('submit', help='Submit jobs.')
  parser_submit.add_argument('fsp_files', metavar='FSP', nargs='+', help='.fsp files')
  # parser_submit.add_argument('-x', type=int, default=1)
  # parser_submit.add_argument('y', type=float)
  parser_submit.set_defaults(func=submitJobs)
  
  # create the parser for the "cleanup" command
  parser_cleanup = subparsers.add_parser('cleanup', help='Remove .o, .e, .log files.')
  parser_cleanup.add_argument('fsp_files', metavar='FSP', nargs='+', help='.fsp files')
  parser_cleanup.add_argument('-n', '--dry-run', action='store_true', help='Only list files that would be removed, without removing them.')
  parser_cleanup.set_defaults(func=subCommand_cleanupJobs)
  
  # create the parser for the "savesweep" command
  parser_savesweep = subparsers.add_parser('savesweep', help='Create sweep files.')
  parser_savesweep.add_argument('fsp_file', help='.fsp file')
  parser_savesweep.add_argument('sweepname', help='Name of the sweep in the .fsp file.')
  parser_savesweep.add_argument('-n', '--dry-run', action='store_true', help='Show what would be done only.')
  parser_savesweep.set_defaults(func=subCommand_savesweepJobs)

  # create the parser for the "loadsweep" command
  parser_loadsweep = subparsers.add_parser('loadsweep', help='Load sweep files.')
  parser_loadsweep.add_argument('fsp_file', help='.fsp file')
  parser_loadsweep.add_argument('sweepname', help='Name of the sweep in the .fsp file.')
  parser_loadsweep.add_argument('-n', '--dry-run', action='store_true', help='Show what would be done only.')
  parser_loadsweep.set_defaults(func=subCommand_loadsweepJobs)

  # create the parser for the "runscript" command
  parser_runscript = subparsers.add_parser('runscript', help='Run script file.', description='Run the same script on multiple .fsp files, running each in its own subdirectory.')
  parser_runscript.add_argument('lsf_file', help='.lsf file to run on each .fsp file.', metavar='LSF_SCRIPT')
  parser_runscript.add_argument('fsp_files', metavar='FSP', nargs='+', help='.fsp files')
  parser_runscript.add_argument('-n', '--dry-run', action='store_true', help='Show what would be done only.')
  parser_runscript.set_defaults(func=subCommand_runscriptJobs)

  args = parser.parse_args()
  # print(args)
  if 'func' in args:
    args.func(args)
  else:
    parser.print_help()
  # sys.exit()
  
if __name__ == '__main__':
  main()
