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
  parser.add_argument('normal_RCD', help='CSV file with data for normal RCD')
  parser.add_argument('inversed_RCD', help='CSV file with data for inversed RCD')
  parser.add_argument('-v', '--verbose', action="count", dest="verbosity", default=0, help='verbosity level')
  args = parser.parse_args()
  print(args)
  
  normal_FF = []
  normal_gap_size = []
  normal_gap_min = []
  normal_gap_max = []
  with open(args.normal_RCD, 'r') as csvfile:
      reader = csv.DictReader(csvfile, delimiter=';')#, fieldnames=['nrod', 'nbg', 'rn', 'FF', 'gap_min', 'gap_max', 'gap_size'])
      for row in reader:
        normal_FF.append(float(row['FF']))
        normal_gap_size.append(float(row['gap_size']))
        normal_gap_min.append(float(row['gap_min']))
        normal_gap_max.append(float(row['gap_max']))
          
  inversed_FF = []
  inversed_gap_size = []
  inversed_gap_min = []
  inversed_gap_max = []
  with open(args.inversed_RCD, 'r') as csvfile:
      reader = csv.DictReader(csvfile, delimiter=';')#, fieldnames=['nrod', 'nbg', 'rn', 'FF', 'gap_min', 'gap_max', 'gap_size'])
      for row in reader:
        inversed_FF.append(float(row['FF']))
        inversed_gap_size.append(float(row['gap_size']))
        inversed_gap_min.append(float(row['gap_min']))
        inversed_gap_max.append(float(row['gap_max']))
  
  fig1 = plt.gcf()
  # plt.plot(normal_FF, normal_gap_size, linestyle='-', label='Loaded from file!')
  plt.subplot(3, 1, 1)
  plt.plot(normal_FF, normal_gap_size, label='normal RCD', linestyle='-', marker='s', color='r')
  plt.plot(inversed_FF, inversed_gap_size, label='inversed RCD', linestyle='-', marker='s', color='b')
  plt.xlabel('FF')
  plt.ylabel('gap size')
  plt.legend()
  plt.title('{} vs {}'.format(args.normal_RCD, args.inversed_RCD))
  
  plt.subplot(3, 1, 2)
  plt.plot(normal_FF, normal_gap_min, label='gap_min', linestyle='-', marker='s', color='r')
  plt.plot(normal_FF, normal_gap_max, label='gap_max', linestyle='-', marker='s', color='b')
  plt.xlabel('FF')
  plt.ylabel('a/lambda')
  plt.legend()
  plt.title('{}'.format(args.normal_RCD))

  plt.subplot(3, 1, 3)
  plt.plot(inversed_FF, inversed_gap_min, label='gap_min', linestyle='-', marker='s', color='r')
  plt.plot(inversed_FF, inversed_gap_max, label='gap_max', linestyle='-', marker='s', color='b')
  plt.xlabel('FF')
  plt.ylabel('a/lambda')
  plt.legend()
  plt.title('{}'.format(args.inversed_RCD))
  
  plt.show()
  fig1.savefig('{}-{}.png'.format(args.normal_RCD, args.inversed_RCD))
  
  return 0

if __name__ == '__main__':
  main()
