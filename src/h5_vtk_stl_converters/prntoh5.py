#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import bfdtd.bfdtd_parser as bfdtd

def main():
  parser = argparse.ArgumentParser(description = 'Convert Bristol-FDTD output into an HDF5 file.')
  
  parser.add_argument('-v','--verbose', action="count", dest="verbosity", default=0, help='verbosity level')
  parser.add_argument('infile', action="store", help='BFDTD input file', nargs='+')
  parser.add_argument('-b','--basepath', default=None, help='basepath for output files')

  parser.add_argument('-t','--snap_number_time', default=[0], type=int, nargs='+')
  parser.add_argument('-f','--snap_number_freq', default=[], type=int, nargs='+')

  parser.add_argument('-T','--snap_number_time-range', default=[], type=int, nargs=2)
  parser.add_argument('-F','--snap_number_freq-range', default=[], type=int, nargs=2)

  parser.add_argument('-l', '--snap_number_freq-latest', action="store_true")
  parser.add_argument('-a', '--snap_number_freq-all', action="store_true")

  parser.add_argument('-n', '--dry-run', action='store_true', help='Just do a dry/test-run to check existence of files.')

  arguments = parser.parse_args()

  if arguments.verbosity > 0:
    print('---------')
    print(arguments)
    print('---------')
  
  data_paths = set()
  
  sim = bfdtd.BFDTDobject()
  sim.verbosity = arguments.verbosity
  # read input
  if arguments.infile:
    for infile in arguments.infile:
      sim.readBristolFDTD(infile)
      data_paths.add(os.path.dirname(infile))
  
  print('data_paths = {}'.format(data_paths))
  sim.setDataPaths(list(data_paths))
  
  # merge all snap_number values
  snap_number_time_all = arguments.snap_number_time
  if arguments.snap_number_time_range:
    snap_number_time_all += list(range(arguments.snap_number_time_range[0], arguments.snap_number_time_range[1]+1))
  snap_number_time_all = list(set(snap_number_time_all))
  snap_number_time_all.sort()
  
  print('snap_number_time_all = {}'.format(snap_number_time_all))
  
  for idx in snap_number_time_all:
    sim.readDataTimeSnapshots(idx, arguments.dry_run)
  
  # if there are frequency snapshots
  if sim.getFrequencySnapshots():
    
    snap_number_freq_all = arguments.snap_number_freq
    if arguments.snap_number_freq_range:
      snap_number_freq_all += list(range(arguments.snap_number_freq_range[0], arguments.snap_number_freq_range[1]+1))
    
    snap_number_freq_max = sim.getLatestFrequencySnapTimeNumber()
    if arguments.verbosity > 0:
      print('snap_number_freq_max = {}'.format(snap_number_freq_max))
    
    if arguments.snap_number_freq_all:
      snap_number_freq_all += list(range(0, snap_number_freq_max+1))
    
    # if -l was used, i.e. latest snapshot requested
    if arguments.snap_number_freq_latest:
      if snap_number_freq_max < 0:
        raise Exception('No frequency snapshots found!')
      snap_number_freq_all.append(snap_number_freq_max)
    
    # clean up and sort list
    snap_number_freq_all = list(set(snap_number_freq_all))
    snap_number_freq_all.sort()
    
    print('snap_number_freq_all = {}'.format(snap_number_freq_all))
    
    if arguments.verbosity > 1:
      print('snap_number_freq_all = {}'.format(snap_number_freq_all))
    for idx in snap_number_freq_all:
      sim.readDataFrequencySnapshots(idx, arguments.dry_run)
  
  # write .h5 file
  if arguments.basepath:
    basepath = arguments.basepath
  else:
    basepath = os.path.splitext(arguments.infile[0])[0]
  
  h5file = basepath + '.h5'
  
  print('Writing data to {}'.format(h5file))
  if not arguments.dry_run:
    sim.writeHDF5(h5file)
  
  return

if __name__ == '__main__':
  main()
