#!/usr/bin/env python3
#import numpy
import os
import sys
import shutil
import argparse
import subprocess

def testLocalRun(nprocs, fspfile, workdir):
  '''
  -create a new directory
  -copy the fsp file to it
  -submit using fdtd-run-local.sh
  '''
  print(f'pwd={os.getcwd()}')
  origdir = os.getcwd()

  (root, ext) = os.path.splitext(fspfile)
  (base, ext) = os.path.splitext(root)
  print(f'-> mkdir {workdir}')
  os.makedirs(workdir, exist_ok=True)
  src = fspfile
  dst = os.path.join(workdir, f'{base}.fsp')
  print(f'-> copying {src} -> {dst}')
  shutil.copyfile(src, dst)
  cmd = ['fdtd-run-local.sh', '-n', str(nprocs), f'{base}.fsp']
  print(f"-> cmd: {' '.join(cmd)}")
  os.chdir(workdir)
  print(f'pwd={os.getcwd()}')
  subprocess.run(cmd)
  # return to original directory
  os.chdir(origdir)
  print(f'pwd={os.getcwd()}')

def testSbatchRun(nprocs, fspfile, workdir, args):
  '''
  -create a new directory
  -copy the fsp file to it
  -submit using fdtd-run-local.sh
  '''
  print(f'pwd={os.getcwd()}')
  origdir = os.getcwd()

  (root, ext) = os.path.splitext(fspfile)
  (base, ext) = os.path.splitext(root)
  print(f'-> mkdir {workdir}')
  os.makedirs(workdir, exist_ok=True)
  src = fspfile
  dst = os.path.join(workdir, f'{base}.fsp')
  print(f'-> copying {src} -> {dst}')
  shutil.copyfile(src, dst)
  
  # cd to workdir
  os.chdir(workdir)
  print(f'pwd={os.getcwd()}')
  
  # cmd = ['fdtd-run-local.sh', '-n', str(nprocs), f'{base}.fsp']
  cmd = ['fdtd-run-slurm.sh', '-n', str(nprocs), '-s', f'{base}.fsp'] # create script only
  # cmd = ['fdtd-run-slurm.sh', '-n', str(nprocs), f'{base}.fsp'] # create script and run
  print(f"-> cmd: {' '.join(cmd)}")
  subprocess.run(cmd)
  
  scriptname = f'{base}.sh'
  jobname = os.path.basename(os.path.abspath(workdir))
  cmd = ['sbatch', '--time', args.time, '--partition', args.partition, '--job-name', jobname, scriptname] # command to submit jobs
  print(f"-> cmd: {' '.join(cmd)}")
  subprocess.run(cmd)
  
  # return to original directory
  os.chdir(origdir)
  print(f'pwd={os.getcwd()}')
  
def memoryStudy():
  parser = argparse.ArgumentParser()
  parser.add_argument("-m", "--mem", help="memory limit", type=int, nargs='+')
  parser.add_argument("-c", "--cpus-per-task", help="cpus/task", type=int, nargs='+')
  parser.add_argument("-n", "--dry-run", help="do not submit jobs", action='store_true')
  args = parser.parse_args()
  print(args)
  # sys.exit()

  if args.mem:
    mem_range = args.mem
  else:
    mem_step=10
    mem_range = range(100,200+mem_step,mem_step)
    
  if args.cpus_per_task:
    cpu_range = args.cpus_per_task
  else:
    cpu_range = range(1,29)
  
  # testing
  # mem_range = [200] #range(10,200+mem_step,mem_step)
  # cpu_range = [1] # range(1,11)
  
  for cpu in cpu_range:
    print(f'-----> cpu: {cpu}')
    for mem in mem_range:
      jobname = f'memory_study.mem_{mem}MB_cpu_{cpu}'
      print(f'  mem: {mem}, jobname: {jobname}')
      # subprocess.run(["sbatch", "-l"])  # doesn't capture output
      cmd = ['sbatch', '--mem', f'{mem}M', '--output', f'{jobname}.out', '--cpus-per-task', str(cpu), '--job-name', f'{jobname}', './basic_test.sh']
      print(f'  {cmd}')
      print('  '.join(cmd))
      if not args.dry_run:
        subprocess.run(cmd)

def getJobScript():
  return
      
def memoryStudy2():
  parser = argparse.ArgumentParser(description='Submit multiple jobs, with varying numbers of cores.')
  parser.add_argument("-n", "--dry-run", help="do not submit jobs", action='store_true')
  parser.add_argument('-r', '--range', default=[1,28], nargs=2, metavar=('N_START','N_END'), help='Range of numbers to try.', type=int)
  parser.add_argument('-p', '--partition', default='test', help='Partition/queue to use.')
  parser.add_argument('-t', '--time', default='00:05:00', help='Time limit for jobs.')
  parser.add_argument('fspfile')
  args = parser.parse_args()
  print(args)

  start=args.range[0]
  end=args.range[1]
  for nprocs in range(start, end+1):
    # workdir = f'login-node-fdtd-run-local.sh-test-n{nprocs}'
    # workdir = f'sbatch-mpiexec-n{nprocs}'
    base, ext = os.path.splitext(os.path.basename(args.fspfile))
    # print(base, ext)
    workdir = f'{base}-nprocs-{nprocs}'
    # print(workdir)
    print(f'---> nprocs: {nprocs}, fspfile: {args.fspfile}, workdir: {workdir}')
    if not args.dry_run:
      # testLocalRun(nprocs, args.fspfile, workdir)
      testSbatchRun(nprocs, args.fspfile, workdir, args)

def main():
  # memoryStudyLocalRun()
  memoryStudy2()

if __name__ == "__main__":
    main()
