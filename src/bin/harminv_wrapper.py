#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import re
import sys
import argparse

'''
Intended to become a harmiv wrapper for Python.
Unfinished.

.. todo:: pythonMEEP might already have something like that. Look into it.
.. todo:: move into utilities or similar...
.. todo:: probe list input + more modularization (separate harminv log generation and file comparison)
'''

def getPeaks(filename):
  peak_list = []
  file = open(filename,'r')
  file.readline()
  for line in file:
    parts = line.split(',')
    frequency = float(parts[0])
    decay_constant = float(parts[1])
    Q = float(parts[2])
    amplitude = float(parts[3])
    phase = float(parts[4])
    error = float(parts[5])
    peak_list.append([frequency, decay_constant, Q, amplitude, phase, error])
  file.close()
  return peak_list

def comparePeaks(harminv_filename, matlab_filename, out_filename):
  harminv_peak_list = getPeaks(harminv_filename)
  matlab_peak_list = getPeaks(matlab_filename)

  #for peak_idx in range(len(matlab_peak_list)):
    #print peak_idx
    #print matlab_peak_list[peak_idx][0]-matlab_peak_list[peak_idx][0]

  merge_peak_list = [[] for i in range(len(matlab_peak_list))]

  for peak_idx in range(len(matlab_peak_list)):
    matlab_peak = matlab_peak_list[peak_idx]
    mindiff_set = False
    mindiff = -1
    for harminv_peak in harminv_peak_list:
      diff = abs(harminv_peak[0]-matlab_peak[0])
      if (not mindiff_set) or (mindiff_set and diff < mindiff):
        mindiff = diff
        merge_peak_list[peak_idx] = harminv_peak
        mindiff_set = True

  #for peak in merge_peak_list:
    #print peak

  print((merge_peak_list[len(merge_peak_list)-1]))

  out_file = open(out_filename,'w')
  
  out_file.write('frequency (MHz), decay constant, Q, amplitude, phase, error, wavelength (nm)\n')
  c0 = 2.99792458E8; # m/s=nm/ns=nm*GHz=10^3*nm*MHz
  # resonance_peak = merge_peak_list[len(merge_peak_list)-1]
  resonance_peak = merge_peak_list[0]
  wavelength = c0/(1e-3*resonance_peak[0]); # nm
  resonance_peak.append(wavelength)
  out_file.write(str(resonance_peak) + '\n')
  out_file.close()

  #print "SUCCESS"
  return resonance_peak

def harminv(infile, outfile, parameterFile):
  pattern = re.compile("final: dt=(.*) fmin=(.*) fmax=(.*)")
  
  if os.path.isfile(parameterFile):
    f = open(parameterFile,'r')
    str = f.readline()
    m = pattern.match(str)
    m.groups()
    dt = m.group(1)
    fmin = m.group(2)
    fmax = m.group(3)
    f.close()
    
    f = open(outfile,'w')
    f.close()
    print(('-->Processing '+infile))
    if os.path.isfile(infile):
      # f = open(outfile,'a')
      # f.write('=== '+infile+'\n')
      # f.close()
      cmd='harminv -t '+dt+' '+fmin+'-'+fmax+' <'+infile+' 1>'+outfile+' 2>&1'
      print('\t'+cmd)
      os.system(cmd)
      # f = open(outfile,'a')
      # f.write('=============================================================\n')
      # f.close()
      
      # compare with matlab output
      #~ harminv_filename = outfile
      #~ base = os.path.dirname(outfile) + '/' + os.path.basename(outfile).split('_')[0]
      #~ matlab_filename = base + '_bilan.txt'
      #~ out_filename = base + '_resonance.txt'
      #~ return comparePeaks(harminv_filename, matlab_filename, out_filename)
      return

def harminv_top_probes(dir):
  pattern = re.compile("final: dt=(.*) fmin=(.*) fmax=(.*)")

  print('Processing '+dir)
  parameterFile = dir+'/'+'harminv_parameters.txt'

  if os.path.isfile(parameterFile):
    f = open(parameterFile,'r')
    line = f.readline()
    m = pattern.match(line)
    m.groups()
    dt = m.group(1)
    fmin = m.group(2)
    fmax = m.group(3)
    f.close()
    
    probeFiles = []
    probeFiles.append(dir+'/'+'p62id_Ex.prn')
    probeFiles.append(dir+'/'+'p71id_Ex.prn')
    probeFiles.append(dir+'/'+'p80id_Ex.prn')
    probeFiles.append(dir+'/'+'p89id_Ex.prn')
    # f = open(outfile,'w')
    # f.close()
    resonance_peak_list = []
    best_peak = []
    Qmax = -1
    for infile in probeFiles:
      print('dir=',dir)
      outfile = os.path.splitext(infile)[0] + '_harminv.log'
      peak = harminv(infile, outfile, parameterFile)
      Q = peak[2]
      if(Q>Qmax):
        Qmax = Q
        best_peak = peak
      
      resonance_peak_list.append(peak)
      # print '-->Processing '+infile
      # if os.path.isfile(infile):
        # f = open(outfile,'a')
        # f.write('=== '+infile+'\n')
        # f.close()
        # cmd='harminv -t '+dt+' '+fmin+'-'+fmax+' <'+infile+' 1>>'+outfile+' 2>&1'
        # print '\t'+cmd
        # os.system(cmd)
        # f = open(outfile,'a')
        # f.write('=============================================================\n')
        # f.close()
  print('And the winner is:')
  print(best_peak)

  out_file = open(dir+'/'+'best_peak.txt','w')
  out_file.write('frequency (MHz), decay constant, Q, amplitude, phase, error, wavelength (nm)\n')
  out_file.write(str(best_peak) + '\n')
  out_file.close()
  return best_peak

def batch_harminv(topdir):
  print(topdir+'resonance_peaks.csv')
  f = open(topdir+'/'+'resonance_peaks.csv','w')
  f.write('pillar\tfrequency(MHz)\tdecay_constant\tQ\tamplitude\tphase\terror\twavelength(nm)\n')
  for dir in os.listdir(topdir):
    if os.path.isdir(os.path.join(topdir, dir)):
      peak = harminv_top_probes(dir)
      f.write(dir)
      for n in peak:
        f.write('\t'+str(n))
      f.write('\n')
  f.close()
  
def main():
  # quick frequency list parser, to check format
  parser = argparse.ArgumentParser()
  parser.add_argument('infile')
  
  args = parser.parse_args()
  for f in getFrequencies(args.infile):
    print(f)
  
  return
  
  # original code+intent
  parser = argparse.ArgumentParser(description = 'python harminv wrapper, allowing direct usage of bfdtd probe files')
  parser.add_argument("-b", "--batch", action="store_true", dest="batch", default=False, help="Process subdirectories (batch job)")  
  parser.add_argument("-t", "--top-probes", action="store_true", dest="top_probes", default=False, help="Process all top probes")
  
  (options, args) = parser.parse_args()
  
  if options.batch:
    print('You have selected batch processing.')
    batch_harminv(args[0])
    print('SUCCESS')
  elif options.top_probes:
    print('You have selected top probes processing.')
    harminv_top_probes(args[0])
    print('SUCCESS')
  else:
    print('You have selected single probe processing.')
    harminv(args[0],args[1],args[2])
    print('SUCCESS')

if __name__ == "__main__":
  main()
