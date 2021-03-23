#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import numpy
import argparse
import tempfile
import subprocess

import photonics.utilities.common

def AABB_intersect(box1_minBB, box1_maxBB, box2_minBB, box2_maxBB):
  dims = len(box1_minBB)
  for i in range(dims):
    if box1_maxBB[i] < box2_minBB[i]:
      return(False)
    if box1_minBB[i] > box2_maxBB[i]:
      return(False)
  return(True)

def getAABBCylinder(start_point, end_point, radius):
  '''
  Returns the lower and upper corners **(minBB, maxBB)** of the *AABB* (*Axis-Aligned Bouding Box*) of a cylinder of radius **radius**, going from **start_point** to **end_point**.
  
  bpy.ops.mesh.primitive_cylinder_add(radius=self.radius, depth=self.length, location=self.centre)
  
  https://www.gamedev.net/forums/topic/338522-bounding-box-for-a-cylinder/?PageSpeed=noscript
  
  .. todo:: Figure out why this formula is correct.
  .. todo:: Create shared function to get AABB bounding box (maybe there is some library?)
  .. todo:: Create new operator to create box using lower+upper
  '''
  
  A = numpy.array(start_point)
  B = numpy.array(end_point)
  
  D = B - A
  L = numpy.linalg.norm(D)
  
  minBB = numpy.minimum(A, B)
  maxBB = numpy.maximum(A, B)
  
  if L != 0:
    kx = numpy.sqrt((D[1]**2+D[2]**2)/(L**2))
    ky = numpy.sqrt((D[0]**2+D[2]**2)/(L**2))
    kz = numpy.sqrt((D[0]**2+D[1]**2)/(L**2))
    minBB = minBB - numpy.array([kx*radius, ky*radius, kz*radius])
    maxBB = maxBB + numpy.array([kx*radius, ky*radius, kz*radius])
  
  return (minBB, maxBB)

def getAABBCylinder_loc_dir_len(location, direction, length, radius, locationIsStartPoint=True):
  u = utilities.common.unitVector(direction)
  if locationIsStartPoint:
    A = location
    B = location + length*u
  else:
    A = location - (length/2)*u
    B = location + (length/2)*u
  (minBB, maxBB) = getAABBCylinder(A, B, radius)
  return (minBB, maxBB)

if __name__ == '__main__':
  print(getAABBCylinder([0,0,0],[1,1,1],1))
