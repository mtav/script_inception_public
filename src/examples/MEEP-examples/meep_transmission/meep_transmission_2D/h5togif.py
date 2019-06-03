#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
import tempfile
import subprocess

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('h5_field')
  args = parser.parse_args()
  print(args)
  
  #DSTDIR = args.DSTDIR
  #if not os.path.isdir(DSTDIR):
    #os.mkdir(DSTDIR)

  ret = subprocess.run(['h5ls', args.h5_field], check=True, stdout=subprocess.PIPE)
  S = ret.stdout.decode()

  return 0

if __name__ == '__main__':
  main()
