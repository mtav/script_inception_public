#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import sys

def getPeaks(filename):
  peak_list = [];
  file = open(filename,'r');
  file.readline();
  for line in file:
    parts = line.split(',');
    frequency = float(parts[0]);
    decay_constant = float(parts[1]);
    Q = float(parts[2]);
    amplitude = float(parts[3]);
    phase = float(parts[4]);
    error = float(parts[5]);
    peak_list.append([frequency, decay_constant, Q, amplitude, phase, error])
  file.close();
  return peak_list;

def comparePeaks(harminv_filename, matlab_filename, out_filename):
  harminv_peak_list = getPeaks(harminv_filename)
  matlab_peak_list = getPeaks(matlab_filename)

  #for peak_idx in range(len(matlab_peak_list)):
    #print peak_idx
    #print matlab_peak_list[peak_idx][0]-matlab_peak_list[peak_idx][0];

  merge_peak_list = [[] for i in range(len(matlab_peak_list))]

  for peak_idx in range(len(matlab_peak_list)):
    matlab_peak = matlab_peak_list[peak_idx];
    mindiff_set = False;
    mindiff = -1;
    for harminv_peak in harminv_peak_list:
      # TODO: Finish?
      raise UserWarning('Unfinished and untested bit of code.')
      diff = abs(harminv_peak[0]-matlab_peak[0])
      if (not mindiff_set) or (mindiff_set and diff < mindiff):
        mindiff = diff
        merge_peak_list[peak_idx] = harminv_peak;
        mindiff_set = True;

  #for peak in merge_peak_list:
    #print peak

  print(merge_peak_list[len(merge_peak_list)-1])

  out_file = open(out_filename,'w');
  out_file.write(str(merge_peak_list[len(merge_peak_list)-1])+'\n')
  out_file.close();

  #print "SUCCESS"

if __name__ == '__main__':

  # harminv_filename = sys.argv[1];
  # matlab_filename = sys.argv[2];
  # out_filename = sys.argv[3];
  # out_filename = 'resonance.txt'

  comparePeaks(sys.argv[1],sys.argv[2],sys.argv[3])
