#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def getFrequencies(filename):
  '''
  Returns a list of frequencies (in Mhz) based on a file in the following format::
  
    PeakNo	Frequency(Hz)	Wavelength(nm)	QFactor	
    1	4.7257745e+14	634.37741293	40.4569
    2	4.9540615e+14	605.14480606	90.37
  '''
  freq_MHz = []
  with open(filename, 'r') as f:
    f.readline() # read/skip the first line
    for line in f:
      split_line = line.split()
      if split_line:
        if len(split_line) > 1:
          freq_MHz.append(float(split_line[1])*1e-6)
        else:
          raise Exception('Not enough columns in line. Each line must have at least two columns, with frequency in the second column (in Hz).')
    #read_data = f.read()
    #print(read_data)
  f.closed
  return freq_MHz
