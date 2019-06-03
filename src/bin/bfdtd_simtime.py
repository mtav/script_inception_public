#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import numpy
import argparse
import tempfile
import datetime

import bfdtd

'''
Module to check BFDTD job status and simulation times.

.. todo:: nice tabbed column output, maybe htop-like ncurses GUI. -> Would be nice as a more general torque job manager. With job-specific info outputs for progress, etc.
.. todo:: deal with missing .out/time logs...
.. todo:: batch processing option searching through a directory?
.. todo:: pre-defined format strings
.. todo:: better status info: "Compiling material map", "not yet started", etc
.. todo:: estimate time to first/next snapshots
'''

#class SimulationInfo:
  

def getSimulationInfoDictionary():
  simulation_info = {
    'infile':None,
    'outfile':None,
    'timelog':None,
    'iterations_current':None,
    'iterations_total':None,
    'iterations_left':None,
    'Ncells':None,
    'progress':None,
    'time_elapsed':None,
    'time_per_iteration_per_cell':None,
    'time_per_iteration':None,
    'time_left':None,
    'estimated_end_time':None,
    'status':None,
  }
  return simulation_info

def strfdelta(tdelta, fmt):
  '''
  from http://stackoverflow.com/questions/8906926/formatting-python-timedelta-objects
  .. todo:: Why is this still not part of python?
  '''
  d = {"days": tdelta.days}
  d["hours"], rem = divmod(tdelta.seconds, 3600)
  d["minutes"], d["seconds"] = divmod(rem, 60)
  return fmt.format(**d)

def analyzeTimeLog(timelog_filename, verbosity=0):
  if verbosity > 0:
    #print('Processing {}'.format(args.timelog.name))
    print('Processing {}'.format(timelog_filename))
  with open(timelog_filename) as timelog_fid:
    
    pattern_start = re.compile('starting program (\d\d):(\d\d):(\d\d)')
    pattern_iteration = re.compile('(\d+) iterations (\d\d):(\d\d):(\d\d)')
    
    L = timelog_fid.readline()
    if not L:
      raise Exception('File is empty')
    
    m = pattern_start.match(L)
    if not m:
      raise Exception('failed to match first line:\n{}'.format(L))
      
    H = int(m.group(1))
    M = int(m.group(2))
    S = int(m.group(3))
    
    days = 0
    
    start_time = datetime.time(hour=H, minute=M, second=S)
    start_datetime = datetime.datetime(1, 1, 1+days, hour=H, minute=M, second=S)
    if verbosity > 0:
      print((start_time, start_datetime))
    
    last_time = start_time
    
    datetime_list = []
    
    for L in timelog_fid:
      m = pattern_iteration.match(L)
      if not m:
        raise Exception('failed to match iteration line:\n{}'.format(L))

      N = int(m.group(1))
      H = int(m.group(2))
      M = int(m.group(3))
      S = int(m.group(4))
      
      iteration_time = datetime.time(hour=H, minute=M, second=S)
      
      if iteration_time < last_time:
        days += 1
        
      last_time = iteration_time
      
      iteration_datetime = datetime.datetime(1, 1, 1+days, hour=H, minute=M, second=S)
      
      if verbosity > 0:
        print((N, iteration_time, iteration_datetime))
      
      datetime_list.append((N, iteration_datetime))
      
    (first_N, first_datetime) = datetime_list[0]
    (last_N, last_datetime) = datetime_list[-1]
    
    delta_N = last_N - first_N
    delta_datetime = last_datetime - start_datetime
    
    if verbosity > 0:
      print('{} iterations in {}'.format(delta_N, delta_datetime))
  return (delta_N, delta_datetime)

def analyzeOutput(outfile, verbosity=0):
  done = False
  with open(outfile) as fid:
    for l in fid:
      if 'End of script file TRUE no script file present FALSE' in l:
        done = True

  return done

def analyzeInput(fileName, verbosity=0):
  
  simulation_info = getSimulationInfoDictionary()
  
  infile = os.path.splitext(fileName)[0] + '.in'
  FDTDobj = bfdtd.readBristolFDTD(infile, verbosity=verbosity)
  
  outfile = os.path.splitext(fileName)[0] + '.out'
  timelog = os.path.join(os.path.dirname(fileName), 'time{}.txt'.format(FDTDobj.getIdString()))
  
  ok_timelog = True
  try:
    (delta_N, delta_datetime) = analyzeTimeLog(timelog, verbosity=verbosity)
  except:
    ok_timelog = False
    delta_N = 0
    delta_datetime = datetime.timedelta()
  
  ok_outfile = True
  try:
    done = analyzeOutput(outfile, verbosity=verbosity)
  except:
    ok_outfile = False
    done = False
  
  if done:
    delta_N = FDTDobj.getIterations()
    
  Ncells = FDTDobj.getNcells()
  
  #T = delta_datetime.total_seconds()
  if delta_N == 0:
    time_per_iteration_per_cell = datetime.timedelta()
    time_per_iteration = datetime.timedelta()
  else:
    time_per_iteration_per_cell = delta_datetime/(Ncells*delta_N)
    time_per_iteration = delta_datetime/delta_N
  
  progress = delta_N / FDTDobj.getIterations()
  iterations_left = FDTDobj.getIterations()-delta_N
  time_left = iterations_left*time_per_iteration
  ETA = datetime.datetime.now() + time_left
  
  #strfdelta(time_left
  #print('time_left : {} seconds = {} minutes = {} hours = {} days'.format(time_left)
  if verbosity > 0:
    print('infile = {}'.format(infile))
    print('outfile = {}'.format(outfile))
    print('timelog = {}'.format(timelog))
    print('Ncells = {}'.format(Ncells))
    print('time/iteration/cell : {} = {} seconds/iteration/cell = {} days/iteration/cell'.format(time_per_iteration_per_cell, time_per_iteration_per_cell.total_seconds(), time_per_iteration_per_cell.total_seconds()/(60*60*24)))
    print('time/iteration : {} = {} seconds/iteration = {} days/iteration'.format(time_per_iteration, time_per_iteration.total_seconds(), time_per_iteration.total_seconds()/(60*60*24)))
    print('progress : {:%}'.format(progress))
    print('time_left : {}'.format(time_left))
    print('estimated end time : {}'.format(ETA))
    print('done : {}'.format(done))
  
  simulation_info['infile'] = infile
  simulation_info['outfile'] = outfile
  simulation_info['timelog'] = timelog
  simulation_info['iterations_current'] = delta_N
  simulation_info['iterations_total'] = FDTDobj.getIterations()
  simulation_info['iterations_left'] = iterations_left
  simulation_info['Ncells'] = Ncells
  simulation_info['progress'] = progress
  simulation_info['time_elapsed'] = delta_datetime
  simulation_info['time_per_iteration_per_cell'] = time_per_iteration_per_cell
  simulation_info['time_per_iteration'] = time_per_iteration
  simulation_info['time_left'] = time_left
  simulation_info['estimated_end_time'] = ETA
  simulation_info['status'] = done
  
  return simulation_info

def main():
  '''
  Calculate BFDTD simulation based on time.txt .
  .. todo:: Should do date increment properly, but for now, only incrementing days should be fine, because it is always less than 30 in principle.
  .. todo:: Multifile support? (i.e. loop through all passed time logs)
  .. todo:: Add speed estimate in time/(Niter*Ncells) based on input files
  .. todo:: write to .csv and/or plot to see if speed is linear
  '''

  #simulation_info = getSimulationInfoDictionary()
  #'Available keys:\n'
  #list(simulation_info.keys()):
    #help_string += 'k,'
  
  parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description='''\
  Calculate BFDTD simulation time based on time.txt.
  
  Available keys for formatting:
  
    infile
    outfile
    timelog
    iterations_current
    iterations_total
    iterations_left
    Ncells
    progress
    time_elapsed
    time_per_iteration_per_cell
    time_per_iteration
    time_left
    estimated_end_time
    status
  
  ''')
  #parser.add_argument('timelog', default='time_id_.txt', nargs='?', type=open, help='Usually time_id_.txt or time.txt for older sims.')
  #parser.add_argument('timelog', default='time_id_.txt', nargs='?', help='Usually time_id_.txt or time.txt for older sims.')
  parser.add_argument('infile', nargs='+')
  #parser.add_argument('-i', '--infile')
  parser.add_argument('-t', '--input-type', choices=['in', 'out', 'time'], help='input file type', default='in')
  #parser.add_argument('-t', action='store_true')
  parser.add_argument('-v', '--verbose', action="count", dest="verbosity", default=0, help='verbosity level')
  parser.add_argument('-f', '--format', dest='FORMAT', metavar='FORMAT', help='Use FORMAT as the format string that controls the output.', default='{infile}, Ncells: {Ncells}, done:{status}, iterations: {iterations_current}/{iterations_total}={progress:%}, elapsed time: {time_elapsed}, time left: {time_left}, estimated end time: {estimated_end_time}, time/iteration: {time_per_iteration}, time/iteration/cell: {time_per_iteration_per_cell}')
  args = parser.parse_args()
  
  if args.verbosity > 0:
    print(args)
    
  simulation_info_list = []
  
  if args.input_type == 'time':
    raise Exception('Not yet implemented. TODO')
    for timelog in args.infile:
      (delta_N, delta_datetime) = analyzeTimeLog(timelog, verbosity=args.verbosity)
      
  elif args.input_type == 'out':
    raise Exception('Not yet implemented. TODO')
  else:
    for infile in args.infile:
      simulation_info = analyzeInput(infile, verbosity=args.verbosity)
      simulation_info_list.append(simulation_info)
      
  for simulation_info in simulation_info_list:
    print(args.FORMAT.format(**simulation_info))
    
    #print('{}, Ncells: {}, done:{}, iterations: {}/{}={:%}, elapsed time: {}, time left: {}, estimated end time: {}, time/iteration: {}, time/iteration/cell: {}'.format(
        #simulation_info['infile'],
        #simulation_info['Ncells'],
        #simulation_info['status'],
        #simulation_info['iterations_current'],
        #simulation_info['iterations_total'],
        #simulation_info['progress'],
        #simulation_info['time_elapsed'],
        #simulation_info['time_left'],
        #simulation_info['estimated_end_time'],
        #simulation_info['time_per_iteration'],
        #simulation_info['time_per_iteration_per_cell'],
      #))
  return
  
  #if args.infile:
    #FDTDobj = bfdtd.readBristolFDTD(args.infile, verbosity=args.verbosity)
    #Ncells = FDTDobj.getNcells()
    #print('Ncells = {}'.format(Ncells))
    
    ##T = delta_datetime.total_seconds()
    #time_per_iteration_per_cell = delta_datetime/(Ncells*delta_N)
    #time_per_iteration = delta_datetime/delta_N
    #print('time/iteration/cell : {} = {} seconds/iteration/cell = {} days/iteration/cell'.format(time_per_iteration_per_cell, time_per_iteration_per_cell.total_seconds(), time_per_iteration_per_cell.total_seconds()/(60*60*24)))
    #print('time/iteration : {} = {} seconds/iteration = {} days/iteration'.format(time_per_iteration, time_per_iteration.total_seconds(), time_per_iteration.total_seconds()/(60*60*24)))
    
    #progress = delta_N / FDTDobj.getIterations()
    #time_left = (FDTDobj.getIterations()-delta_N)*time_per_iteration
    #ETA = datetime.datetime.now() + time_left
    
    #print('progress : {:%}'.format(progress))
    #print('time_left : {}'.format(time_left))
    #print('estimated end time : {}'.format(ETA))
    ##strfdelta(time_left
    ##print('time_left : {} seconds = {} minutes = {} hours = {} days'.format(time_left)
    
  return 0

if __name__ == '__main__':
  main()
