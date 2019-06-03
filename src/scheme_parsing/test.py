#!/usr/bin/env python

import pyscheme.parser
import pyscheme.parser
import pyscheme.scheme
import pyscheme.expressions
import sys
from glob import glob

def parseFile(filename):
  print "Processing "+filename;
  FILE = open(filename,'r');
  str = FILE.read();
  FILE.close();
  program = pyscheme.parser.parse('('+str+')')
  print program


if __name__ == '__main__':

  for arg in sys.argv[1:]: 
      filelist = glob(arg);
      for file in filelist:
          parseFile(file);
      # filelist = glob('*.ctl');
      # print "============"
      # print filelist
      # print "============"
    # parseFile(arg);
