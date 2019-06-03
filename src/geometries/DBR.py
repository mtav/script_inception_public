#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import numpy
import argparse
import tempfile
import subprocess
from constants.physcon import get_c0

class DBR():
  
  def __init__(self):
    self.wavelength = 0.637
    self.nLow = 1
    self.nHigh = 2.4
    
  def __init__(self, wavelength, nLow, nHigh):
    self.wavelength = wavelength
    self.nLow = nLow
    self.nHigh = nHigh
    
  #def setWavelength(self, ):
    
  #def getHighIndexThickness(self):
    #return self.wavelength/(4*self.nHigh)
  #def getLowIndexThickness(self):
    #return self.wavelength/(4*self.nLow)

  def getFrequencyRange(self):
    t1 = self.wavelength/(4*self.nLow)
    t2 = self.wavelength/(4*self.nHigh)
    DBR_pair_thickness = t1+t2

    f0 = get_c0()/self.wavelength
    #f0 = ((self.nLow + self.nHigh)/(4*self.nLow*self.nHigh))*get_c0()/DBR_pair_thickness
    delta_f = (4/numpy.pi)*numpy.arcsin(abs(self.nLow-self.nHigh)/(self.nLow+self.nHigh))*f0

    fmax = f0 + delta_f/2
    fmin = f0 - delta_f/2

    lambda_min = get_c0()/fmax
    lambda_max = get_c0()/fmin
    
    return (fmin, fmax)

  def getWavelengthRange(self):
    (fmin, fmax) = self.getFrequencyRange()
    return (get_c0()/fmax, get_c0()/fmin)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('wavelength', type=float)
  parser.add_argument('nLow', type=float)
  parser.add_argument('nHigh', type=float)
  parser.add_argument('-v', '--verbose', action="count", dest="verbosity", default=0, help='verbosity level')
  args = parser.parse_args()
  print(args)
  
  obj = DBR(args.wavelength, args.nLow, args.nHigh)
  print('FrequencyRange = {}'.format(obj.getFrequencyRange()) )
  print('WavelengthRange = {}'.format(obj.getWavelengthRange()) )
  
  return 0
  
if __name__ == '__main__':
  main()
