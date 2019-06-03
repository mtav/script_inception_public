#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('dirlist', type=argparse.FileType('r'))
  args = parser.parse_args()
  
  #print('Missing directories:')
  #print('line number, directory')
  header = args.dirlist.readline().strip()
  print(header)

  for line_idx, line in enumerate(args.dirlist):
    s = line.strip()
    #print(s)
    d = s.split(';')[-1]
    d = d.strip()
    #print(len(s))
    if os.path.exists(d):
      print(s)
      #print(line_idx+1, d)

  return 0

if __name__ == '__main__':
  main()
