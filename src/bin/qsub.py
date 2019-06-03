#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# qsub wrapper

# things of interest:
#-check out qstat Tcl support (may require recompile)
#-check out xpbsmon
#https://oss.trac.surfsara.nl/pbs_python
#https://pypi.python.org/pypi/pbs-python/
#https://github.com/jkitchin/python-torque
#https://freshcode.club/projects/pbs_python
#pbsnodes and other pbs commands
# TODO: fix pick+pipe bug: find . | xargs qsub.py -> hangs
# TODO: check script for PBS option and ask if they were not specified anywhere (CLI or script)

# TODO/BUG: non-recurring Invalid credential error -> try to resubmit on failure
#qsub: submit error (Invalid credential)
#Traceback (most recent call last):
  #File "~/Development/script_inception_public/bin/qsub.py", line 362, in <module>
    #main()
  #File "~/Development/script_inception_public/bin/qsub.py", line 324, in main
    #myqsub.submit(script)
  #File "~/Development/script_inception_public/bin/qsub.py", line 224, in submit
    #utilities.common.check_call_and_log(cmd, logfile_object)
  #File "~/Development/script_inception_public/utilities/common.py", line 73, in check_call_and_log
    #raise subprocess.CalledProcessError(retcode, cmd)
#subprocess.CalledProcessError: Command '['qsub', '-mabe', '-joe', '-q', 'default', '-l', 'nodes=1:ppn=1', '-l', 'walltime=120:00:00', '-M', 'xxx@yyy.com', '-v', 'JOBDIR=~/TEST/BCC-coated-woodpiles/2017-05-02/resolution=32/coating_index=2.10/thickness_mum=0.010', '~/TEST/BCC-coated-woodpiles/2017-05-02/resolution=32/coating_index=2.10/thickness_mum=0.010/BCC-coated-woodpiles.mpirun.sh']' returned non-zero exit status 173

import os
import re
import sys
import stat
import getpass
import argparse
import tempfile
import subprocess
import datetime
import pick
import utilities.common

LOGFILE = os.path.join(os.path.expanduser('~'), 'qsub.log')

#Queue            Memory CPU Time Walltime Node  Run Que Lm  State
#---------------- ------ -------- -------- ----  --- --- --  -----
#gaia               --      --    720:00:0   --    0   0 --   E R
#gpu                --      --    360:00:0   --   24  94 --   E R
#ghlc               --      --    480:00:0   --    2   0 --   E R
#long               --      --    360:00:0   --  273   1 --   E R
#paleo              --      --    360:00:0   --    1   0 --   E R
#galaxy-std         --      --    240:00:0   --    0   0 --   E R
#cfdgroup           --      --    480:00:0   --    3   0 --   E R
#medium             --      --    240:00:0   --  109   9 --   E R
#testq              --      --    01:00:00   --    2   1 --   E R
#veryshort          --      --    12:00:00   --  210 133 --   E R
#visualisation      --      --    576:00:0   --    0   0 --   E R
#himem              --      --    360:00:0   --    8   2 --   E R
#vsmp               --      --    360:00:0   --    0   0 --   E R
#system             --      --    240:00:0   --    0   0 --   E R
#galaxy-high        --      --    240:00:0   --    0   0 --   E R
#short              --      --    120:00:0   --  699 440 --   E R
#default            --      --       --      --    0  41 --   E R
#bridge             --      --    360:00:0   --    2   0 --   E R
#'teaching'           --      --    24:00:00   --   11   0 --   E R
#'accis'              --      --    360:00:0   --    6   0 --   E R
#'glaciol'            --      --    360:00:0   --    0   0 --   E R
#'amd-gpu'            --      --    360:00:0   --    0   0 --   E R


  #qsub [-a date_time]
  #[-A account_string]
  #[-b secs]
  #[-c checkpoint_options]
  #[-C directive_prefix]
  #[-d path]
  #[-D path] [-e path] [-f] [-h] [-I] [-j join] [-k keep] [-l resource_list] [-m mail_options] [-M user_list] [-n node exclusive] [-N
       #name] [-o path] [-p priority] [-P proxy_username[:group]]  [-q destination] [-r c] [-S path_list] [-t array_request] [-T prologue/epilogue script_name] [-u user_list] [-v variable_list] [-V] [-w]  path  [-W  additional_attributes]  [-x]
       #[-X] [-z] [script]

def parseQstatFullOutput(qstat_full_output, section_type='Queue'):
  '''
  Parses "qstat -f" output into a more usable format
    input: qstat -f output in string format
    output: a list of dictionaries containing the various attributes of a job
  '''
  
  section_dict = {}
  
  section_pattern = re.compile('{}: (?P<section_id>.*?)\n(?P<section_items>.*?)\n\n'.format(section_type), re.DOTALL)
  for section_blob in section_pattern.finditer(qstat_full_output):
    item_dict = {}
    
    section_id = section_blob.groupdict()['section_id']
    section_items = section_blob.groupdict()['section_items']
    
    # get rid of linebreaks in attributes
    section_items = section_items.replace('\n\t','')
    
    # convert to dictionary
    item_pattern = re.compile("\s*(?P<key>.*?)\s*=\s*(?P<value>.*)\s*")
    for item in item_pattern.finditer(section_items):
      key = item.groupdict()['key']
      value = item.groupdict()['value']
      item_dict[key] = value
    
    # add dictionary of this section
    section_dict[section_id] = item_dict
  
  return(section_dict)

def getTorqueQueueInfo():
  qstat_process = subprocess.Popen(['qstat','-f', '-Q'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
  #return_code = qstat_process.wait() # causes hanging on python 2.7.2
  (qstat_full_output, qstat_stderr) = qstat_process.communicate()
  queue_dict = parseQstatFullOutput(qstat_full_output)
  
  for queue_id, queue_info in queue_dict.items():
    print(queue_info.keys())
    print((queue_id, queue_info['resources_max.walltime']))

class qsubmitter:
  queue = 'default'
  walltime = None
  nodes = None
  ppn = None
  mail = None
  
  force_submit = None
  
  dry_run = False
  
  verbosity = 0
  
  def __init__(self, args):
    
    self.verbosity = args.verbosity
    self.dry_run = args.dry_run
    
    if 'QSUBMAIL' in os.environ:
      self.mail = os.environ['QSUBMAIL']
    elif getpass.getuser():
      self.mail = '{}@bristol.ac.uk'.format(getpass.getuser())
    
    if args.walltime is None and args.interactive:
      self.walltime, index = pick.pick([12, 120, 240, 360], 'Walltime?')
    else:
      self.walltime = args.walltime
    
    if args.nodes is None and args.interactive:
      self.nodes, index = pick.pick(range(1,11), 'number of nodes?')
    else:
      self.nodes = args.nodes
    
    #4GB/core
    if args.ppn is None and args.interactive:
      ppn_options = [ 'PPN = {} -> RAM = {} GB'.format(i+1, 4*(i+1)) for i in range(16)]
      options, index = pick.pick(ppn_options, 'PPN?')
      self.ppn = index + 1
    else:
      self.ppn = args.ppn
      
    if args.queue is None:
      self.queue = 'default'
    else:
      self.queue = args.queue
    
  def submit(self, script):
    
    (root, ext) = os.path.splitext(script)
    outfile = root + '.out'
    
    if os.path.exists(outfile):
      if self.force_submit is None:
        option, index = pick.pick(['skip', 'skip (for all)', 'remove .out file and submit', 'remove .out file and submit (for all)'], '{}\nScript seems to have been started before (.out file found). What do you want to do?'.format(script))
        if index == 0:
          force_submit_current = False
        elif index == 1:
          force_submit_current = False
          self.force_submit = False
        elif index == 2:
          force_submit_current = True
        elif index == 3:
          force_submit_current = True
          self.force_submit = True
      else:
        force_submit_current = self.force_submit
    
      if force_submit_current:
        print('removing {}'.format(outfile))
      else:
        print('skipping {}'.format(script))
        return
    
    if self.verbosity > 0:
      print('===> submitting {}'.format(script))
    
    origdir = os.getcwd()
    script_abspath = os.path.abspath(script)
    scriptdir = os.path.dirname(script_abspath)
    
    if self.verbosity > 1:
      print('origdir = {}'.format(origdir))
      print('scriptdir = {}'.format(scriptdir))
    
    os.chdir(scriptdir)
    
    #scriptdir = os.path.dirname(script)
    #if not os.chdir(scriptdir):
      #raise Exception('Failed to change to {}'.format(scriptdir))
      
    #if not os.chdir(origdir):
      #raise Exception('Failed to change back to {}'.format(origdir))
    #print('<')
    #print(os.getcwd())
    #print(os.path.dirname(script))
    #os.chdir(os.path.dirname(script))
    #print(os.getcwd())
    #print('>')
    cmd = ['qsub',
           '-mabe',
           '-joe',
           '-q', self.queue]
    
    if self.nodes and self.ppn:
      cmd += ['-l', 'nodes={}:ppn={}'.format(self.nodes, self.ppn)]
    
    if self.walltime:
      cmd += ['-l', 'walltime={}:00:00'.format(self.walltime)]
    
    cmd += ['-M', self.mail,
           '-v', 'JOBDIR={}'.format(scriptdir),
           script_abspath]
    
    if self.verbosity > 1:
      print(cmd)
    
    if self.verbosity > 0:
      print(' '.join(cmd))
    
    if not self.dry_run:
      with open(LOGFILE, 'a') as logfile_object:
        logfile_object.write('==================\n')
        logfile_object.write('{}\n'.format(datetime.datetime.now()))
        logfile_object.write('{}\n'.format(script_abspath))
        logfile_object.write('submitted from: {}\n'.format(os.getcwd()))
        logfile_object.write('TORQUE_QUEUE={} PPN={} WALLTIME={}\n'.format(self.queue, self.ppn, self.walltime))
        utilities.common.check_call_and_log(cmd, logfile_object)
        logfile_object.write('==================\n')
    
    os.chdir(origdir)
    
    return
  
  def printInfo(self):
    print('queue={}'.format(self.queue))
    print('walltime={}'.format(self.walltime))
    print('nodes={}'.format(self.nodes))
    print('ppn={}'.format(self.ppn))
    print('mail={}'.format(self.mail))
    return
    
  def __str__(self):
    s = 'queue={}\nwalltime={}\nnodes={}\nppn={}\nmail={}'.format(self.queue, self.walltime, self.nodes, self.ppn, self.mail)
    return(s)

#qsub(script, walltime=None, queue=None, nodes, ppn, mail):
  ##PBS -l walltime=120:00:00
##PBS -mabe
##PBS -joe

  #qsub -q $TORQUE_QUEUE -l nodes=1:ppn=$PPN -M $QSUBMAIL -v JOBDIR="$(readlink -f "$(dirname "$SCRIPT")")" "$SCRIPT" 2>&1 | tee -a $LOGFILE
  #return
  
       #-N name Declares a name for the job.  The name specified may be up to and including 15 characters in length.  It must consist of printable, non white space characters with the first character alphabetic.

#BC1:
#92 nodes each with two dual-core Opteron processors, memory 8 GB RAM per node (2 GB per core)
#ppn=4
#2GB/core
#8GB/node

#BC2:
#416 nodes each with 2 x 2.8 GHz 4 core Intel Harpertown E5462 processors, memory 8 GB RAM per node (1GB per core), 193GB scratch space on /local
#ppn=8
#1GB/core
#8GB/node

#BC3:
#223 base blades which have 16 x 2.6Hz SandyBridge cores, 4GB/core and a 1TB SATA disk.
#ppn=16
#4GB/core
#64GB/node

def findFiles(dirname, ext):
  print('Searching for {} files in "{}" ...'.format(ext, dirname))
  L = []
  for root, dirs, files in os.walk(dirname):
    for f in files:
      if f.endswith(ext):
        L.append(os.path.join(root, f))
  return(L)

def main():
  
  mode = os.fstat(0).st_mode
  if stat.S_ISFIFO(mode):
    raise Exception("stdin is piped. Please use $(cmd) to pass arguments instead.")
  elif stat.S_ISREG(mode):
    raise Exception("stdin is redirected. Please use $(cmd) to pass arguments instead.")
  else:
    pass
    #print("stdin is terminal")
  
  parser = argparse.ArgumentParser(description='For batch submissions, use qsub.py $(find . -name "*.sh") for example. Argument piping is not yet supported due to the interactive nature of the script.')
  parser.add_argument('script_list', metavar='script', nargs='+')
  parser.add_argument('-n', '--dry-run', action='store_true', help='print submission commands, but do not submit')
  parser.add_argument('-v', '--verbose', action="count", dest="verbosity", default=0, help='verbosity level')
  parser.add_argument('--walltime', type=int)
  parser.add_argument('--ppn', type=int)
  parser.add_argument('--nodes', type=int)
  
  # .. todo:: get queue options from system
  #parser.add_argument('--queue', choices=getQueues())
  parser.add_argument('-q', '--queue')
  
  parser.add_argument('-i', '--interactive', action='store_true', help='Interactively ask for unspecified settings.')
  args = parser.parse_args()
  
  if args.verbosity > 1:
    print(args)
  
  myqsub = qsubmitter(args)
  
  #if args.verbosity > 0:
    #myqsub.printInfo()
  
  option, index = pick.pick(['yes', 'no'], '{}\n\nIs this correct?'.format(myqsub))
  if option == 'no':
    sys.exit(0)
  
  #script_list_all = []
  #for script in args.script_list:
    #if os.path.isfile(script):
      #script_list_all.append(script)
    #elif os.path.isdir(script):
      #script_list_all.extend(findFiles(script, '.sh'))
    
  #selected = pick.pick(script_list_all, 'Select scripts to submit (press SPACE to mark, ENTER to continue):', multi_select=True)
  #script_list = [fname for (fname, i) in selected]
  
  for script in args.script_list:
    if os.path.isfile(script):
      myqsub.submit(script)
    else:
      raise Exception('{} not found from {}'.format(script, os.getcwd()))

  #getTorqueQueueInfo()
  #if args.script_list:
    #script_list = args.script_list
  #else:
    #script_list_all = findFiles('.', '.sh')
    #selected = pick.pick(script_list_all, 'Select scripts to submit (press SPACE to mark, ENTER to continue):', multi_select=True)
    #script_list = [fname for (fname, i) in selected]
  
  #for script in args.script_list:
    #if os.path.isfile(script):
      #myqsub.submit(script)
    #if os.path.isdir(script):
      #script_list_all = findFiles('.', '.sh')
      #selected = pick.pick(script_list_all, 'Select scripts to submit (press SPACE to mark, ENTER to continue):', multi_select=True)
      #script_list = [fname for (fname, i) in selected]
    
  return 0

def checkSource():
  # http://stackoverflow.com/questions/13442574/how-do-i-determine-if-sys-stdin-is-redirected-from-a-file-vs-piped-from-another
  import os, stat

  mode = os.fstat(0).st_mode
  if stat.S_ISFIFO(mode):
    print("stdin is piped")
  elif stat.S_ISREG(mode):
    print("stdin is redirected")
  else:
    print("stdin is terminal")
    a = pick.pick([1,2,3], 'choose:')
    print(a)
    pick.pick(['a','b'], 'choose:')

if __name__ == '__main__':
  main()
  #checkSource()
