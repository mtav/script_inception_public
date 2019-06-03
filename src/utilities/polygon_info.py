#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import numpy
import argparse
import tempfile
import subprocess

class polygon():
  def __init__(self):
    self.N = 3
    self.R = 1
    return


  def getN(self):
    return self.N
  
  def setN(self, N):
    self.N = N


  def getArea(self):
    return self.N*numpy.power(self.R,2)*numpy.sin(self.getAlpha())/2

  def setArea(self, A):
    print('A = {}'.format(A))
    x = (A/self.N)*2*1/numpy.sin(self.getAlpha())
    print('x = {}'.format(x))
    self.R = numpy.sqrt( x )
    return

  
  def getSideLength(self):
    return self.R*numpy.sqrt(2)*numpy.sqrt(1-numpy.cos(self.getAlpha()))

  def setSideLength(self, S):
    self.R = S/numpy.sqrt( 2*(1-numpy.cos(self.getAlpha())) )
    return

    
  def getRadius(self):
    return self.R

  def setRadius(self, R):
    self.R = R
    return


  def getAlpha(self):
    return (2*numpy.pi)/self.N

  def getCornerAngle(self):
    return numpy.pi - self.getAlpha()

  def print_info(self):
    print('N = {}'.format(self.N))
    print('alpha = {} radians = {} degrees'.format(self.getAlpha(), numpy.rad2deg(self.getAlpha())))
    print('corner angle beta = {} radians = {} degrees'.format(self.getCornerAngle(), numpy.rad2deg(self.getCornerAngle())))
    print('R = {}'.format(self.R))
    print('S = {}'.format(self.getSideLength()))
    print('A = {}'.format(self.getArea()))
    return

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('DSTDIR', default=tempfile.gettempdir(), nargs='?')
  parser.add_argument('-v', '--verbose', action="count", dest="verbosity", default=0, help='verbosity level')
  args = parser.parse_args()
  print(args)
  
  DSTDIR = args.DSTDIR
  if not os.path.isdir(DSTDIR):
    os.mkdir(DSTDIR)

  return 0

if __name__ == '__main__':
  main()
