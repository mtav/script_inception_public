#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import division

import os
import re
import sys
import argparse
import tempfile
import subprocess
import matplotlib.pyplot as plt
import csv

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('csvfile', help='CSV file', nargs='+')
  parser.add_argument('-v', '--verbose', action="count", dest="verbosity", default=0, help='verbosity level')
  args = parser.parse_args()
  print(args)
  
  fig1 = plt.gcf()
  
  for f in args.csvfile:
    FF = []
    gap_size = []
    gap_min = []
    gap_max = []
    with open(f, 'r') as csvfile:
      m = re.match(r'output-nrod_(\d+(?:\.\d+)?)\.nbg_(\d+(?:\.\d+)?)\.csv', os.path.basename(f))
      if m is None:
        print(os.path.basename(f))
        raise
      nrod = float(m.group(1))
      nbg = float(m.group(2))
      if args.verbosity >0:
        print('nrod={:.2f}, nbg={:.2f}'.format(nrod, nbg))

      reader = csv.DictReader(csvfile, delimiter=';')#, fieldnames=['nrod', 'nbg', 'rn', 'FF', 'gap_min', 'gap_max', 'gap_size'])
      for row in reader:
        FF.append(float(row['FF']))
        gap_size.append(float(row['gap_size']))
        gap_min.append(float(row['gap_min']))
        gap_max.append(float(row['gap_max']))
  
      # plt.plot(normal_FF, normal_gap_size, linestyle='-', label='Loaded from file!')
      plt.subplot(2, 1, 1)
      plt.plot(FF, gap_size, label='nrod:nbg={}:{}'.format(nrod, nbg))#, linestyle='-', marker='s', color='r')
      plt.xlabel('FF')
      plt.ylabel('gap size')
      plt.legend()
      
      plt.subplot(2, 1, 2)
      plt.plot(FF, gap_min, label='nrod:nbg={}:{} - gap_min'.format(nrod, nbg))#, linestyle='-', marker='s', color='r')
      plt.plot(FF, gap_max, label='nrod:nbg={}:{} - gap_max'.format(nrod, nbg))#, linestyle='-', marker='s', color='b')
      plt.xlabel('FF')
      plt.ylabel('a/lambda')
      plt.legend()

  plt.show()
  fig1.savefig('RCD-bandgap-plots.png')
  
  return 0

if __name__ == '__main__':
  main()
