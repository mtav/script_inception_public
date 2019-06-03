#!/usr/bin/env python3

import os
import re
import sys
import getpass
import argparse
import subprocess

'''
At the moment, this is just a wrapper script for qstat, offering enhanced output.
Long-term, an easy to use job manager would be beneficial.

The main tools for managing jobs are:

  * qsub
  * qstat
  * qdel

The corresponding existing wrapper scripts:

  * superqsub.sh
  * batch_qsub.sh
  * qdel_all.sh
  * qdel_queued.sh

Ideas:

  * Create torque-utils.py module shared by the corresponding python wrapper scripts?
  * Create single script with CLI options?
  * Create GUI? -> terminal(ncurses) or X(tk, Qt, etc)? Any GUI toolkit with terminal+X support?

.. todo:: Finish this
.. todo:: qsub wrapper: check if job is not already running before submitting by checking qstat output
.. todo:: combine with bfdtd_simtime.py to list progress of jobs as well! This will also allow estimating how many iterations a sim will reach before walltime cutoff, etc.
'''

def parseQstatFullOutput(qstat_full_output):
  '''
  Parses "qstat -f" output into a more usable format
    input: qstat -f output in string format
    output: a list of dictionaries containing the various attributes of a job
  '''
  
  job_list = []
  
  pattern_job = re.compile("Job Id: (?P<jobId>.*?)\n(?P<jobDetails>.*?)\n\n",re.DOTALL)
  for job_blob in pattern_job.finditer(qstat_full_output):
    job_dict = {}
    
    job_id = job_blob.groupdict()['jobId']
    job_details = job_blob.groupdict()['jobDetails']
    
    job_dict['jobId'] = job_id
    
    job_details = job_details.replace('\n\t','')
    
    pattern_jobitems = re.compile("\s*(?P<key>.*?)\s*=\s*(?P<value>.*)\s*")
    for job_item in pattern_jobitems.finditer(job_details):
      key = job_item.groupdict()['key']
      value = job_item.groupdict()['value']
      job_dict[key]=value
    
    job_list.append(job_dict)
  
  return(job_list)

def main():
  '''
  qstat wrapper
  '''
  parser = argparse.ArgumentParser(description='qstat wrapper offering enhancec output')
  
  if len(sys.argv)>1:
    with open(sys.argv[1], 'r') as f:
      qstat_full_output = f.read()
  else:
    qstat_process = subprocess.Popen(['qstat','-f'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    #return_code = qstat_process.wait() # causes hanging on python 2.7.2
    (qstat_full_output, qstat_stderr) = qstat_process.communicate()
  
  job_list = parseQstatFullOutput(qstat_full_output)
  
  #Job id                    Name             User            Time Use S Queue
  #------------------------- ---------------- --------------- -------- - -----
  
  try:
    for job in job_list:
      if getpass.getuser() in job['Job_Owner']:
        #print(job['Job_Name'])
        #print(job['jobId'])
        #print(job['submit_args'].split()[-1])
        
        if 'Variable_List' in job.keys():
          variable_dict = dict([i.split('=',1) for i in job['Variable_List'].split(',')])
          #print(variable_dict)
          #print(variable_dict['JOBDIR'])
          #print(variable_dict['PBS_O_WORKDIR'])        
          script_path = os.path.join(variable_dict['PBS_O_WORKDIR'],job['submit_args'].split()[-1])
        else:
          script_path = job['submit_args'].split()[-1]
        
        if 'resources_used.cput' in job.keys():
          running_time = job['resources_used.cput']
        else:
          running_time = '00:00:00'
        
        #job['jobId']
        #script_path
        #job['Job_Owner']
        #running_time
        #job['job_state']
        #job['queue']
        print(job['jobId'] + ' job_state=' + job['job_state'] + ' running_time=' + str(running_time) + ' -> ' + script_path, flush=True)
  
  except (BrokenPipeError, IOError):
      pass
  #print('Number of jobs = '+str(len(job_list)))
  
  sys.stderr.close()
  return
  
if __name__ == "__main__":
  main()
