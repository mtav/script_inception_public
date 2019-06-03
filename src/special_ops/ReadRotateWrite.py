#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import numpy
import copy
from GWL.GWL_parser import GWLobject

def ReadRotateWrite(infile):
  orig = GWLobject()
  orig.readGWL(infile)
  for alpha_deg in numpy.linspace(0,45,10):
    obj = copy.deepcopy(orig)
    obj.rotate([0,0,0], [0,0,1], alpha_deg)
    outfile = infile + '.alpha_' + str(alpha_deg) +'.gwl'
    obj.writeGWL(outfile)
  return

if __name__ == "__main__":
  ReadRotateWrite(sys.argv[1])
