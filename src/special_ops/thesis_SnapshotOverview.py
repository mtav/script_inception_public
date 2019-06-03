#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import argparse
import tempfile
import subprocess

import bfdtd

def main():
  parser = argparse.ArgumentParser()
  #parser.add_argument('-o', '--outfile', default='snapshot_overview.txt')
  parser.add_argument('infile')
  parser.add_argument('-v', '--verbose', action="count", dest="verbosity", default=0, help='verbosity level')
  args = parser.parse_args()
  #print(args)
  
  sim = bfdtd.readBristolFDTD(args.infile, verbosity=args.verbosity)
  N = sim.getLatestFrequencySnapTimeNumber()
  (fsnapshot_file_names, tsnapshot_file_names, esnapshot_file_names, probe_file_names) = sim.getOutputFileNames(fsnap_time_number=N)
  freq_list = sim.getSnapshotFrequencySet()
  Nfreqs = len(freq_list)
  
  (ex, ey, ez) = esnapshot_file_names
  (ex, ext) = os.path.splitext(ex)
  (ey, ext) = os.path.splitext(ey)
  (ez, ext) = os.path.splitext(ez)
  
  for (idx,freq) in enumerate(freq_list):
    fx = fsnapshot_file_names[0+idx]
    fy = fsnapshot_file_names[0+idx+Nfreqs]
    fz = fsnapshot_file_names[0+idx+2*Nfreqs]
    (fx, ext) = os.path.splitext(fx)
    (fy, ext) = os.path.splitext(fy)
    (fz, ext) = os.path.splitext(fz)
    print('{} {} {} {} {} {} {}'.format(fx, ex, fy, ey, fz, ez, freq))
  
  return 0

if __name__ == '__main__':
  main()
