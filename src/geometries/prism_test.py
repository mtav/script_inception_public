#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import numpy
import argparse
import tempfile
from bfdtd.bfdtd_parser import *
from utilities.common import *
from bfdtd.triangular_prism import TriangularPrism
from bfdtd.SpecialTriangularPrism import SpecialTriangularPrism
from bfdtd.excitationTemplate import *
from bfdtd.excitation_utilities import *

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('DSTDIR', default=tempfile.gettempdir(), nargs='?')
  args = parser.parse_args()  
  print(args.DSTDIR)

  height = 10
  radius = 1

  prism = TriangularPrism()
  #prism = SpecialTriangularPrism()
  prism.lower = [ 0, 0, 0 ]
  prism.upper = [ height, 2*3./2.*radius*1.0/numpy.sqrt(3), 3./2.*radius ]
  #prism.lower = [1,1,1]
  #prism.upper = [1,10,1]
  #prism.lower = [1,2,3]
  #prism.upper = [3,7,13]
  prism.orientation = [2,0,1]
  #prism.orientation = [2,1,0]
  prism.setRefractiveIndex(2.4)
  prism.NvoxelsX = 30
  prism.NvoxelsY = 30
  prism.NvoxelsZ = 30

  sim = BFDTDobject()
  sim.appendGeometryObject(prism)
  sim.writeGeoFile(os.path.join(args.DSTDIR, 'prism_test.geo'))

if __name__ == "__main__":
  main()
