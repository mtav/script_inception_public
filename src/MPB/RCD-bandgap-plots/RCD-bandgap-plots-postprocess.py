#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import division

import os
import re
import sys
import csv
import argparse
import tempfile
import subprocess

import MPB.MPB_parser

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('outfiles', nargs='+', help='MPB .out output files')
  parser.add_argument('-v', '--verbose', action="count", dest="verbosity", default=0, help='verbosity level')
  args = parser.parse_args()
  if args.verbosity >0:
    print(args)
  
  # writer = csv.writer(sys.stdout, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  # writer.writerow(['Spam'] * 5 + ['Baked Beans'])
  # writer.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

  # fieldnames = ['first_name', 'last_name']
  # writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames, delimiter=';')

  # writer.writeheader()
  # writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
  # writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
  # writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})
    
  
  writer = csv.DictWriter(sys.stdout, fieldnames=['nrod', 'nbg', 'rn', 'FF', 'FF_mean_position', 'gap_min', 'gap_max', 'gap_size'], delimiter=';')
  writer.writeheader()
  # sys.exit(0)
  
  for i in args.outfiles:
    if args.verbosity >0:
      print('---> {}'.format(i))
    m = re.match(r'nrod_(\d+(?:\.\d+)?)\.nbg_(\d+(?:\.\d+)?)\.rn_(\d+(?:\.\d+)?)\.out', os.path.basename(i))
    nrod = float(m.group(1))
    nbg = float(m.group(2))
    rn = float(m.group(3))
    if args.verbosity >0:
      print('nrod={:.2f}, nbg={:.2f}, rn={:.2f}'.format(nrod, nbg, rn))

    with open(i) as infile:
      MPB_data_list = MPB.MPB_parser.parse_MPB(infile, verbosity=0, merge_datasets=False)
      MPB_data_object = MPB_data_list[0]
      
      MPB_data_object.eps_low
      MPB_data_object.eps_high
      MPB_data_object.eps_arithmetic_mean
      MPB_data_object.eps_harmonic_mean
      MPB_data_object.FF_bigger_than_one
      MPB_data_object.FF_mean_position

      for i in MPB_data_object.gap_list:
        if args.verbosity >0:
          print(i.lower_band, i.gap_min, i.upper_band, i.gap_max, i.gap_size)
          print(i)
          print(nrod, nbg, rn, MPB_data_object.FF_bigger_than_one, i.gap_min, i.gap_max, i.gap_size)
        
        writer.writerow({'nrod':nrod,
                         'nbg':nbg,
                         'rn':rn,
                         'FF':MPB_data_object.FF_bigger_than_one,
                         'FF_mean_position':MPB_data_object.FF_mean_position,
                         'gap_min':i.gap_min,
                         'gap_max':i.gap_max,
                         'gap_size':i.gap_size})
      
  return 0

if __name__ == '__main__':
  main()
