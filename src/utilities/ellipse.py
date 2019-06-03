#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import division

'''
Ellipse-related calculations.
cf also:
  script_inception_public/src/reference/elliptical-rod-ends.kig
'''

import os
import re
import sys
import numpy
import argparse
import tempfile
import subprocess
import matplotlib
import matplotlib.pyplot as plt

class EllipticalRod():
  ellipsoid_width = 2*0.20
  ellipsoid_height_z = 3*ellipsoid_width
  
  def __str__(self):
    ret = '<------------------' + '\n'
    ret += 'EllipsoidWidth = {}'.format(self.getEllipsoidWidth()) + '\n'
    ret += 'EllipsoidHeightZ = {}'.format(self.getEllipsoidHeightZ()) + '\n'
    ret += 'CylinderHeightZ = {}'.format(self.getCylinderHeightZ()) + '\n'
    ret += 'CylinderDiameterBig = {}'.format(self.getCylinderDiameterBig()) + '\n'
    ret += 'CylinderDiameterSmall = {}'.format(self.getCylinderDiameterSmall()) + '\n'
    ret += 'PointTop = {}'.format(self.getPointTop()) + '\n'
    ret += 'PointBottom = {}'.format(self.getPointBottom()) + '\n'
    ret += 'TiltedEllipseHorizontalDiameter = {}'.format(self.getTiltedEllipseHorizontalDiameter()) + '\n'
    ret += 'TiltedEllipseVerticalDiameter = {}'.format(self.getTiltedEllipseVerticalDiameter()) + '\n'
    ret += '------------------>'
    return ret
  
  def plot(self):
    ellipsoid_height_z = self.getEllipsoidHeightZ()
    (cylinder_height_z, D_ell, D_cyl, (Xp, Yp), (Xm, Ym)) = EllipticalRodInfo1(self.getEllipsoidWidth(), self.getEllipsoidHeightZ())
    
    ax = plt.gca()
    plt.axis('equal')
    plt.xlim(-ellipsoid_height_z, ellipsoid_height_z)
    plt.ylim(-ellipsoid_height_z, ellipsoid_height_z)
    ellipse = matplotlib.patches.Ellipse((0, 0), self.getEllipsoidWidth(), self.getEllipsoidHeightZ(), fill=False)
    ax.add_patch(ellipse)
    x = numpy.linspace(-ellipsoid_height_z, ellipsoid_height_z, 100)
    plt.plot(x, (1/numpy.sqrt(2))*x)
    plt.plot(x, 0*x, 'r--')
    plt.plot(0*x, x, 'r--')
    
    plt.plot(x, (1/numpy.sqrt(2))*(x-Xp) + Yp, 'r--')
    plt.plot(x, (1/numpy.sqrt(2))*(x-Xm) + Ym, 'r--')
    
    plt.plot(x, (1/numpy.sqrt(2))*(x-0) + self.getEllipsoidHeightZ()/2, 'g--')
    plt.plot(x, (1/numpy.sqrt(2))*(x-0) - self.getEllipsoidHeightZ()/2, 'g--')
    
    # transverse
    u = numpy.array([-1, numpy.sqrt(2)])
    u = u/numpy.linalg.norm(u)
    
    v = numpy.array([numpy.sqrt(2), 1])
    v = v/numpy.linalg.norm(v)
    
    A =  (D_ell/2)*u + 0.5*self.getEllipsoidWidth()*v
    B = -(D_ell/2)*u + 0.5*self.getEllipsoidWidth()*v
    plt.plot([A[0], B[0]], [A[1], B[1]], 'k--x')
    
    A =  (D_cyl/2)*u - 0.5*self.getEllipsoidWidth()*v
    B = -(D_cyl/2)*u - 0.5*self.getEllipsoidWidth()*v
    plt.plot([A[0], B[0]], [A[1], B[1]], 'k--x')
    
    alpha_rad = self.getMajorAxisAngleWithRespectToVertical()
    plt.plot(x, -1/numpy.tan(alpha_rad)*x, 'm--')
    
    # points
    plt.plot(Xp, Yp, 'b+')
    plt.plot(Xm, Ym, 'b+')
    plt.plot(0, 0, 'b+')
    plt.plot(0, cylinder_height_z/2, 'b+')
    plt.plot(0, -cylinder_height_z/2, 'b+')
    plt.plot(0, ellipsoid_height_z/2, 'kx')
    plt.plot(0, -ellipsoid_height_z/2, 'kx')
    
    plt.show()
    return
  
  def getTiltedEllipseInfo(self):
    '''
    .. todo:: generalize to any direction + return minor+major axis vectors...
    '''
    (cylinder_height_z, D_ell, D_cyl, (Xp, Yp), (Xm, Ym)) = EllipticalRodInfo1(self.ellipsoid_width, self.ellipsoid_height_z)
    major_axis = numpy.array([Xp, Yp]) - numpy.array([Xm, Ym])
    minor_diameter = self.getEllipsoidWidth()
    major_diameter = numpy.linalg.norm(major_axis)
    alpha_rad = numpy.arccos( numpy.dot(major_axis, numpy.array([0,1])) / major_diameter )
    return (minor_diameter, major_diameter, alpha_rad)
  
  def getTiltedEllipseVerticalDiameter(self):
    (minor_diameter, major_diameter, alpha_rad) = self.getTiltedEllipseInfo()
    return major_diameter
  
  def getTiltedEllipseHorizontalDiameter(self):
    (minor_diameter, major_diameter, alpha_rad) = self.getTiltedEllipseInfo()
    return minor_diameter
  
  def getMajorAxisAngleWithRespectToVertical(self):
    '''Returns value in radians.'''
    (minor_diameter, major_diameter, alpha_rad) = self.getTiltedEllipseInfo()
    # (cylinder_height_z, D_ell, D_cyl, (Xp, Yp), (Xm, Ym)) = EllipticalRodInfo1(self.ellipsoid_width, self.ellipsoid_height_z)
    # major_axis = numpy.array([Xp, Yp]) - numpy.array([Xm, Ym])
    # alpha_rad = numpy.arccos( numpy.dot(major_axis, numpy.array([0,1])) / numpy.linalg.norm(major_axis) )
    return alpha_rad
    
  def getInfo1(self):
    (cylinder_height_z, D_ell, D_cyl, (Xp, Yp), (Xm, Ym)) = EllipticalRodInfo1(self.ellipsoid_width, self.ellipsoid_height_z)
    return (cylinder_height_z, D_ell, D_cyl, (Xp, Yp), (Xm, Ym))
    
  def getEllipsoidWidth(self):
    return self.ellipsoid_width
  
  def getEllipsoidHeightZ(self):
    return self.ellipsoid_height_z
  
  def getCylinderHeightZ(self):
    (cylinder_height_z, D_ell, D_cyl, (Xp, Yp), (Xm, Ym)) = EllipticalRodInfo1(self.ellipsoid_width, self.ellipsoid_height_z)
    return cylinder_height_z
  
  def getCylinderDiameterBig(self):
    (cylinder_height_z, D_ell, D_cyl, (Xp, Yp), (Xm, Ym)) = EllipticalRodInfo1(self.ellipsoid_width, self.ellipsoid_height_z)
    return D_cyl
  
  def getCylinderDiameterSmall(self):
    (cylinder_height_z, D_ell, D_cyl, (Xp, Yp), (Xm, Ym)) = EllipticalRodInfo1(self.ellipsoid_width, self.ellipsoid_height_z)
    return D_ell
  
  def getPointTop(self):
    (cylinder_height_z, D_ell, D_cyl, (Xp, Yp), (Xm, Ym)) = EllipticalRodInfo1(self.ellipsoid_width, self.ellipsoid_height_z)
    return (Xp, Yp)
  
  def getPointBottom(self):
    (cylinder_height_z, D_ell, D_cyl, (Xp, Yp), (Xm, Ym)) = EllipticalRodInfo1(self.ellipsoid_width, self.ellipsoid_height_z)
    return (Xm, Ym)
  
  def setEllipsoidWidth(self, ellipsoid_width):
    self.ellipsoid_width = ellipsoid_width
    return
  
  def setEllipsoidHeightZ(self, ellipsoid_height_z):
    self.ellipsoid_height_z = ellipsoid_height_z
    return
  
  def setCylinderHeightZ(self, cylinder_height_z):
    (ellipsoid_height_z, D_ell, D_cyl, (Xp, Yp), (Xm, Ym)) = EllipticalRodInfo2(self.getEllipsoidWidth(), cylinder_height_z)
    self.setEllipsoidHeightZ(ellipsoid_height_z)
    return
  
  def setCylinderDiameterBig(self, cylinder_diameter_big):
    cylinder_height_z = numpy.sqrt(3/2)*cylinder_diameter_big
    # printAnywhere('cylinder_height_z = {}'.format(cylinder_height_z))
    self.setCylinderHeightZ(cylinder_height_z)
    return
  
  def setCylinderDiameterSmall(self, cylinder_diameter_small):
    raise
    return

def printAnywhere(s):
  try:
    import FreeCAD
    FreeCAD.Console.PrintMessage('{}\n'.format(s))
  except:
    print(s)
  return

def EllipticalRodInfo1(ellipsoid_width, ellipsoid_height_z):
  '''
  (x,y) is the basis in which the major axis is along x.
  (X,Y) is the basis in which the major axis is along Y.
  i.e.:
    x = Y
    y = -X
  .. todo:: rewrite things in a less confusing way + add documentation images
  '''
  
  a = 0.5*ellipsoid_height_z
  b = 0.5*ellipsoid_width
  
  D_ell = numpy.sqrt(2/3)*ellipsoid_height_z
  
  m = -numpy.sqrt(2)
  M = -1/m
  
  xp = numpy.sqrt( 1 / (1/(a**2) + (b**2)/((a**4)*(m**2))) )
  yp = -(b**2)/(a**2) * xp/m
  
  xm = -xp
  ym = -yp
  
  Xp = -yp
  Yp =  xp
  
  Xm = -ym
  Ym =  xm
  
  # unitary transverse vector
  u = numpy.array([-1, numpy.sqrt(2)])
  u = u/numpy.linalg.norm(u)
  
  A = numpy.array([Xp, Yp])
  B = numpy.array([Xm, Ym])
  AB = B - A
  D_cyl = abs(numpy.dot(AB, u))
  
  cylinder_height_z = abs(2*(-M*Xp + Yp))
  
  return (cylinder_height_z, D_ell, D_cyl, (Xp, Yp), (Xm, Ym))

def EllipticalRodInfo2(ellipsoid_width, cylinder_height_z):
  C = cylinder_height_z/2
  m = -numpy.sqrt(2)
  c = -m*C
  b = 0.5*ellipsoid_width
  a = abs(numpy.sqrt(c**2 - b**2)/m)
  ellipsoid_height_z = 2*a
  if ellipsoid_height_z < 0:
    print(c)
    print(b)
    raise
  
  (cylinder_height_z, D_ell, D_cyl, (Xp, Yp), (Xm, Ym)) = EllipticalRodInfo1(ellipsoid_width, ellipsoid_height_z)
  
  return (ellipsoid_height_z, D_ell, D_cyl, (Xp, Yp), (Xm, Ym))

def main():
  ellipsoid_width = 2*0.20
  cylinder_height_z = 2*0.25*numpy.sqrt(3/2)
  ellipsoid_height_z = 3*ellipsoid_width
  
  # (cylinder_height_z, D_ell, D_cyl, (Xp, Yp), (Xm, Ym)) = EllipticalRodInfo1(ellipsoid_width, ellipsoid_height_z)
  # print(Xp,Yp)
  # print(Xm,Ym)
  # (cylinder_height_z, D_ell, D_cyl, a, b) = EllipticalRodInfo1(ellipsoid_width, ellipsoid_height_z)
  # print(a,b)
  
  # EllipticalRodInfo2(ellipsoid_width, cylinder_height_z)
  
  # (ellipsoid_height_z, D_ell, D_cyl, (Xp, Yp), (Xm, Ym)) = EllipticalRodInfo2(ellipsoid_width, cylinder_height_z)
  
  # setEllipsoidHeightZ
  # rod = EllipticalRod()
  # rod.setEllipsoidWidth(ellipsoid_width)
  # rod.setEllipsoidHeightZ(ellipsoid_height_z)
  # print(rod)
  # rod.plot()
  
  # rod = EllipticalRod()
  # rod.setEllipsoidWidth(0.2)
  # rod.setEllipsoidHeightZ(0.3)
  # print(rod)
  # rod.plot()
  
  # rod = EllipticalRod()
  # rod.setEllipsoidWidth(1)
  # rod.setEllipsoidHeightZ(1)
  # print(rod)
  # rod.plot()
  
  # rod = EllipticalRod()
  # rod.setEllipsoidWidth(1)
  # rod.setEllipsoidHeightZ(10)
  # print(rod)
  # rod.plot()
  
  # setCylinderHeightZ 
  # rod = EllipticalRod()
  # rod.setEllipsoidWidth(ellipsoid_width)
  # rod.setCylinderHeightZ(cylinder_height_z)
  # print(rod)
  # rod.plot()
  
  # rod = EllipticalRod()
  # rod.setEllipsoidWidth(0.2)
  # rod.setCylinderHeightZ(0.3)
  # print(rod)
  # rod.plot()
  
  # rod = EllipticalRod()
  # rod.setEllipsoidWidth(1)
  # rod.setCylinderHeightZ(1)
  # print(rod)
  # rod.plot()
  
  rod = EllipticalRod()
  rod.setEllipsoidWidth(0.4)
  rod.setCylinderDiameterBig(0.5)
  print(rod)
  rod.plot()
  
  rod = EllipticalRod()
  rod.setEllipsoidWidth(1)
  rod.setCylinderDiameterBig(1)
  print(rod)
  rod.plot()
  
  # rod = EllipticalRod()
  # rod.setEllipsoidWidth(1)
  # rod.setCylinderHeightZ(10)
  # print(rod)
  # rod.plot()
  
  return 0

if __name__ == '__main__':
  main()
