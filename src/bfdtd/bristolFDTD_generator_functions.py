#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import tempfile
import argparse
import textwrap

from utilities.getuserdir import *
from utilities.common import *

########################
# GENERATOR FUNCTIONS
########################
# mandatory objects

# geometry objects

# measurement objects

# files
def GEOcommand(filename, BASENAME):
  ''' CMD file generation '''

  #open file
  with open(filename, 'w') as FILE:

    #~ FILE = fopen(strcat(filename,'.cmd'),'wt')

    # Executable = 'D:\fdtd\source\latestfdtd02_03\subgrid\Fdtd32.exe'
    Executable = os.path.join(getuserdir(),'bin','fdtd.exe')

    #write file
    FILE.write("Executable = %s\n" % Executable)
    FILE.write("\n")
    FILE.write("input = %s.in\n" %  BASENAME)
    FILE.write("\n")
    FILE.write("output = fdtd.out\n")
    FILE.write("\n")
    FILE.write("error = error.log\n")
    FILE.write("\n")
    FILE.write("Universe = vanilla\n")
    FILE.write("\n")
    FILE.write("transfer_files = ALWAYS\n")
    FILE.write("\n")
    FILE.write("transfer_input_files = entity.lst, %s.geo, %s.inp\n" %  (BASENAME, BASENAME))
    FILE.write("\n")
    FILE.write("Log = foo.log\n")
    FILE.write("\n")
    FILE.write("Rank = Memory >= 1000\n")
    FILE.write("\n")
    FILE.write("LongRunJob = TRUE\n")
    FILE.write("\n")
    FILE.write("###Requirements = (LongRunMachine =?= TRUE)\n")
    FILE.write("\n")
    FILE.write("queue\n")

    #close file
    FILE.close()

def GEOin(filename, file_list, overwrite=True, use_relpath=False):
  ''' IN file generation '''
  
  # check if file already exists
  if not overwrite and os.path.exists(filename):
    raise UserWarning('File already exists: ' + filename)
  
  dstdir = os.path.dirname(os.path.abspath(filename))
  
  #write file
  with open(filename, 'w') as FILE:
    for f in file_list:
      f_final = f
      if use_relpath:
        f_final = os.path.relpath(os.path.abspath(f), start=dstdir)
      FILE.write('{}\n'.format(f_final))

def GEOshellscript(filename, BASENAME, EXE = 'fdtd', WORKDIR = '$JOBDIR', WALLTIME = 12, overwrite=True, PPN=1):
  '''
  .. todo:: simplify it + merge with GEOshellscript_advanced by adding options
  .. todo:: Test if cd ${PBS_O_WORKDIR} also works if the job is not submitted from the directory containing the script.
  '''

  # check if file already exists
  if not overwrite and os.path.exists(filename):
    raise UserWarning('File already exists: ' + filename)
  
  #open file
  with open(filename, 'w') as FILE:
    FILE.write(textwrap.dedent('''\
    #!/bin/bash
    #
    #PBS -l nodes=1:ppn={:d}
    #PBS -l walltime={:d}:00:00
    #PBS -mabe
    #PBS -joe
    #
    
    export WORKDIR={}
    export EXE={}
    
    if [ -z ${{PBS_O_WORKDIR+x}} ]
    then
      echo "PBS_O_WORKDIR is unset"
      export WORKDIR="$(readlink -f $(dirname "${{0}}"))"
    else
      echo "PBS_O_WORKDIR is set"
      # on compute node, change directory to 'submission directory':
      # cd ${{PBS_O_WORKDIR}}
    fi

    cd ${{WORKDIR}}

    echo "WORKDIR = ${{WORKDIR}}"
    echo "pwd = $(pwd)"
    
    $EXE {}.in > {}.out
    '''.format(PPN, WALLTIME, WORKDIR, EXE, BASENAME, BASENAME) ))
    
    ##write file
    #FILE.write("#!/bin/bash\n")
    #FILE.write("#\n")
    #FILE.write("#PBS -l walltime=%d:00:00\n" % WALLTIME)
    #FILE.write("#PBS -mabe\n")
    #FILE.write("#PBS -joe\n")
    #FILE.write("#\n")
    #FILE.write("\n")
    #FILE.write("\n")
    #FILE.write("export WORKDIR=%s\n" % WORKDIR)
    #FILE.write("export EXE=%s\n" % EXE)
    #FILE.write("\n")
    #FILE.write("cd $WORKDIR\n")
    #FILE.write("\n")
    #FILE.write("$EXE %s.in > %s.out\n" %  (BASENAME, BASENAME))
    ##FILE.write("fix_filenames.py -v .\n")
  
    ##close file
    #FILE.close()

def GEOshellscript_advanced(filename, BASENAME, probe_col, EXE = 'fdtd', WORKDIR = '$JOBDIR', WALLTIME = 12):
  '''
  .. todo:: maybe create a submission function in python...
  '''

  #open file
  with open(filename, 'w') as FILE:
    #write file
    FILE.write("#!/bin/bash\n")
    FILE.write("#\n")
    FILE.write("#PBS -l walltime=%d:00:00\n" % WALLTIME)
    FILE.write("#PBS -mabe\n")
    FILE.write("#PBS -joe\n")
    FILE.write("#\n")
    FILE.write("\n")
    FILE.write("set -eux\n")
    FILE.write("\n")
    FILE.write('if [ -n "${JOBDIR+x}" ]; then\n')
    FILE.write('  echo JOBDIR is set\n')
    FILE.write('else\n')
    FILE.write('  echo JOBDIR is not set\n')
    FILE.write('  JOBDIR="$(readlink -f $(dirname "$0"))"\n')
    FILE.write('fi\n')
    FILE.write("\n")
    FILE.write("export WORKDIR=%s\n" % WORKDIR)
    FILE.write("export EXE=%s\n" % EXE)
    FILE.write("\n")
    FILE.write("cd $WORKDIR\n")
    FILE.write("\n")
    FILE.write("$EXE %s.in > %s.out\n" %  (BASENAME, BASENAME))
    FILE.write("fix_filenames.py -v .\n")
    FILE.write("matlab_batcher.sh getResonanceFrequencies2 \"'$WORKDIR/p001id.prn',%d,'$WORKDIR/freq_list.txt'\"\n" % probe_col)
    FILE.write("resonance_run.py $WORKDIR $WORKDIR/resonance $WORKDIR/freq_list.txt\n")
    FILE.write("cd resonance/ && $EXE %s.in >> %s.out\n" %  (BASENAME, BASENAME))
    FILE.write("fix_filenames.py -v .\n")
    FILE.write("plotAll.sh .\n")
  
    #close file
    FILE.close()

def main(argv=None):
  return

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('DSTDIR', default=tempfile.gettempdir(), nargs='?')
  parser.add_argument('-v', '--verbose', action="count", dest="verbosity", default=0, help='verbosity level')
  args = parser.parse_args()
  print(args)
  
  DSTDIR = args.DSTDIR
  if not os.path.isdir(DSTDIR):
    os.mkdir(DSTDIR)
  
  print('Writing into: ' + args.DSTDIR)
  GEOcommand(os.path.join(args.DSTDIR, 'tmp.bat'), 'BASENAME')
  GEOin(os.path.join(args.DSTDIR, 'tmp.in'), ['file','list'])
  GEOshellscript(os.path.join(args.DSTDIR, 'tmp.sh'), 'BASENAME', '/usr/bin/superexe', '/work/todo', 999)
  
  return 0

if __name__ == "__main__":
  main()
