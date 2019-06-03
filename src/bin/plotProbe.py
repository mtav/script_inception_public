#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import argparse
import tempfile
import subprocess
import pick
import utilities.prnutils
import matplotlib.pyplot as plt

def plotProbe(filename):
  (h, d) = utilities.prnutils.readProbeFile(filename)
  component, index = pick.pick(h, 'Select component to plot:')
  print(component, index)
  plt.plot(d['time_mus'], d[component])
  plt.xlabel('Time ($\mu s$)')
  plt.ylabel('{} (arbitrary units)'.format(component))
  plt.title('{} - {}'.format(filename, component))
  plt.show()
  return

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('probefile')
  parser.add_argument('-v', '--verbose', action="count", dest="verbosity", default=0, help='verbosity level')
  args = parser.parse_args()
  print(args)
  
  plotProbe(args.probefile)
  
  return 0

if __name__ == '__main__':
  main()
