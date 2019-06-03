#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
BFDTD+GWL class system + GUI::

  class PhotonicCrystallineDiamond(object):
    \'''
    Also known as:
    -Photonic Crystalline Diamond (PCD)
    -ice crystal
    -spin-ice
    -diamond
    \'''

    def __init__(self,
      mesh = None):
      return

  class PhotonicCrystallineDiamond_F_RD(PhotonicCrystallineDiamond):
    def __init__(self,
      mesh = None):
      return

But then we will want defects... :/ There is no way out. We need GUIs (with script support and parameter based structure design (like in RSOFT))...

idea: The RCD class should use generic lines/cylinders (independent of FDTD or GWL usage). It could even define multiple different ones (ex: vertical and non-vertical lines).
  These lines/cylinders could then be actually written using different classes: parallelepiped, spiral cylinder, flat lines, BFDTD cylinders, etc
  Depending on the chosen class (or maybe even class instance, which would then be copied over), different attributes like permittivity, writing direction, voxel distance, etc could then be defined.
  The generic crystal should store a list of lines to write with maybe an indication on whether or not to connect the current line to the next one ([a,b,c] instead of [[a,b],[b,c]]).
  (This mean it could be a GWLobject. The subclasses would just read the GWL object and replace A-B lines with some other random structure from A to B.)
  To optimize speed, it would be better to pass the "line function" to the writer process instead of first getting a list of lines and then looping through it again to write.

.. todo:: icecrystals with continuous lines

.. todo:: review this code and document it.

.. todo:: Parallepiped should also support inner+outer radius? :/

.. todo:: both BFDTD and GWL objects should have location/rotation properties -> need more abstract parent class, which could also handle parenting, grouping, array modifiers, etc. Again, very similar to the Blender system. It might be worth checking out how Blender, FreeCAD, Cascade, LibreCAD, OpenEMS, VTK, etc handle this. 2D applications like for the FIB or e-beam lithography could also profit from it.

attributes:

  * output location (only used on writing, does not need to be an object attribute (except maybe for BFDTD or other classes writing multiple files)):

    * outdir', action="store", dest="outdir", default=tempfile.gettempdir(), help='output directory')
    * basename', action="store", dest="basename", default='RCD', help='output basename')

  * general RCD properties:

    * cube_side", help="length of unit cube side", type=float, default=2.8)
    * Nx", help="number of periods in the X direction", type=int, default=3)
    * Ny", help="number of periods in the Y direction", type=int, default=3)
    * Nz", help="number of periods in the Z direction", type=int, default=3)
    * "--centro_X", help="Centre X position", type=float, default=0)
    * "--centro_Y", help="Centre Y position", type=float, default=0)
    * "--centro_Z", help="Centre Z position", type=float, default=0)

  * GWL:
  
    * special attributes (not sure where to put them):
    
      * TopDownWriting/downwardWriting", help="Write from top to bottom", action="store_true", default=True)
    
    * GWLobject properties:
    
      * "--set-lower-to-origin", help='offset structure so that its "lower corner" is moved to the (0,0,0) coordinates. This will make all coordinates positive.', action="store_true")

      * GWL power compensation:

        * "--write-power", help="Write power values using the power compensation (PC) parameters.", action="store_true")
        
        * "--PC_laser_power_at_z0", help="PC: laser power at z0", type=float, default=100)
        * "--PC_slope", help="PC: power compensation slope", type=float, default=0)
        * "--PC_interfaceAt", help="PC: interface position", type=float, default=0)
        * "--PC_bool_InverseWriting", help="PC: To write a file designed for use with the InvertZAxis command", action="store_true", default=False)
        * "--PC_float_height", help='PC: "substrate height", in practice just a value added to the interfaceAt value', type=float, default=0)
        * "--PC_bool_LaserPowerCommand", help="PC: Use the LaserPower command instead of a 4th coordinate for power.", action="store_true", default=False)

    * GWL Parallelepiped:
    
      * rod_height", help="rod height", type=float, default=0.375)
      * rod_width", help="rod width", type=float, default=0.25)
      * connected", help="connect lines", action="store_true")
      * orthogonal", help='orthogonal "z-axis"', action="store_true")
      * axis0", help="index of axis 0", choices=[0,1,2],  default=0, type=int)
      * axis1", help="index of axis 1", choices=[0,1,2],  default=1, type=int)
      * axis2", help="index of axis 2", choices=[0,1,2],  default=2, type=int)
      * N0", help="number of lines along axis 0", type=int, default=3)
      * N1", help="number of lines along axis 1", type=int, default=3)
      * N2", help="number of lines along axis 2", type=int, default=3)

    * GWL Cylinder/Tube:
    
      * "--method", help="writing method", type=str, choices=['spiral', 'vertical lines', 'horizontal disks'],  default='spiral')

      * inner_radius
      * outer_radius

      * "--PointDistance_r", help="PointDistance_r", type=float, default=0.2)
      * "--PointDistance_theta", help="PointDistance_theta", type=float, default=0.2)
      * "--PointDistance_z", help="PointDistance_z", type=float, default=0.2)

      * "--zigzag", help="zigzag", action="store_true")
      * "--rotateSpirals", help="rotateSpirals", action="store_true")
      * "--add_flat_ends", help="add_flat_ends", action="store_true")
      * "--closed_loop", help="closed_loop", action="store_true")

  * BFDTD:

    * BFDTD RCD properties:
  
      * cylinder_radius_normalized

      * BFDTD refractive indices:

        * n_defect
        * n_crystal
        * n_backfill

    * BFDTD .inp file:

      * fmin_normalized
      * fmax_normalized
    
    * BFDTD defect:

      * i_sub_defect
      * k_sub_defect

.. todo:: Create special "line class" or similar to add/replace lines with normal lines, cylinders, blocks and other crazy ideas... Maybe even general N-points -> recipe conversions...
.. todo:: Optimize by not recalculating similar lines... (only 4 different line orientations in principle)

.. todo:: The *User* (yes, yes, that crazy guy...) might want to write the RCD "line structures" (cylinders, paras, etc) with different powers and not use the simple Z-based power compensation.
.. todo:: tapered RCD and other crazy stuff...
.. todo:: F-RD...
'''

import argparse
import argparseui
import copy
import numpy
import os
import sys
import tempfile
import time

from math import *
from numpy import array, linspace
from PyQt5 import QtWidgets

from bfdtd.BFDTDobject import BFDTDobject
from bfdtd.GeometryObjects import GeometryObject, Sphere, Block, Distorted, Parallelepiped, Cylinder, Rotation, MeshBox

from bfdtd.excitation import Excitation, ExcitationWithGaussianTemplate, ExcitationWithUniformTemplate
from constants.physcon import get_c0
from GWL.GWL_parser import *
from GWL.parallelepiped import Parallelepiped

class RCD_CubicLattice(object):
  '''
  .. note:: Keeping thing independent from GWL and BFDTD here for the moment.

  * cube_side: length of unit cube side
  * Nx: number of periods in the X direction
  * Ny: number of periods in the Y direction
  * Nz: number of periods in the Z direction
  * location
  * rotation (later)
  '''
  def __init__(self):
    self.cube_side = 1
    self.Nx = 3
    self.Ny = 3
    self.Nz = 3
    self._location = array([0,0,0])

    self.TopDownWriting = True

    return

  @property
  def location(self):
      """ location """
      return self._location
  @location.setter
  def location(self, value):
      self._location = array(value)

  def add_arguments(self, parser):
    parser.add_argument("--Nx", help="number of periods in the X direction", type=int, default=3)
    parser.add_argument("--Ny", help="number of periods in the Y direction", type=int, default=3)
    parser.add_argument("--Nz", help="number of periods in the Z direction", type=int, default=3)
    parser.add_argument("--cube_side", help="length of unit cube side", type=float, default=1)
    parser.add_argument("--location_X", help="X position", type=float, default=0)
    parser.add_argument("--location_Y", help="Y position", type=float, default=0)
    parser.add_argument("--location_Z", help="Z position", type=float, default=0)
    return

  def setAttributesFromParsedOptions(self, options):
    self.cube_side = options.cube_side
    self.Nx = options.Nx
    self.Ny = options.Ny
    self.Nz = options.Nz
    self.location = array([options.location_X, options.location_Y, options.location_Z])
    return
    
  #def line_structure_function(self, start_point, end_point):
    #self.addLine(start_point, end_point)
    #return
    
  def createRCD(self, line_structure_function):
    '''
    .. todo:: implement options for continuous writing:
        * line_structure_function(start_point, end_point, end_with_write, write_first_point)
        * start_point: array of size 3
        * end_point: array of size 3
        * end_with_write: True/False
        * write_first_point: True/False
    '''
    
    #line_structure_function([1,2,3],[4,5,6])
    #return
    
    if self.TopDownWriting:
      k_range = range(self.Nz-1,-1,-1)
    else:
      k_range = range(self.Nz)

    for k in k_range:
      print('k = '+str(k))
      Z = k+0.75
      # y = x + M + 0.5 lines
      for M in range(-self.Nx,self.Ny):
        for i in range(self.Nx):
          for i_sub in range(4):
            x1 = i+i_sub*0.25
            y1 = x1 + M + 0.5
            z1 = Z+0.25*((i_sub+1)%2)
            x2 = i+(i_sub+1)*0.25
            y2 = x2 + M + 0.5
            z2 = Z+0.25*(i_sub%2)
            if 0<=x1<=self.Nx and 0<=x2<=self.Nx and 0<=y1<=self.Ny and 0<=y2<=self.Ny:
              A = self.cube_side*numpy.array([x1,y1,z1])
              B = self.cube_side*numpy.array([x2,y2,z2])
              line_structure_function(A, B)

      Z = k+0.5
      # j = -i + M lines
      for M in range(1,self.Nx+self.Ny):
        for i in range(self.Nx):
          for i_sub in range(4):
            x1 = i+i_sub*0.25
            y1 = -x1 + M
            z1 = Z+0.25*(i_sub%2)
            x2 = i+(i_sub+1)*0.25
            y2 = -x2 + M
            z2 = Z+0.25*((i_sub+1)%2)
            if 0<=x1<=self.Nx and 0<=x2<=self.Nx and 0<=y1<=self.Ny and 0<=y2<=self.Ny:
              A = self.cube_side*numpy.array([x1,y1,z1])
              B = self.cube_side*numpy.array([x2,y2,z2])
              line_structure_function(A, B)

      Z = k+0.25
      # j = i + M lines
      for M in range(-(self.Nx-1),self.Ny):
        for i in range(max(-M,0),min(self.Ny-M,self.Nx)):
          for i_sub in range(4):
            x1 = i+i_sub*0.25
            y1 = x1 + M
            z1 = Z+0.25*((i_sub+1)%2)
            x2 = i+(i_sub+1)*0.25
            y2 = x2 + M
            z2 = Z+0.25*(i_sub%2)
            if 0<=x1<=self.Nx and 0<=x2<=self.Nx and 0<=y1<=self.Ny and 0<=y2<=self.Ny:
              A = self.cube_side*numpy.array([x1,y1,z1])
              B = self.cube_side*numpy.array([x2,y2,z2])
              line_structure_function(A, B)

      Z = k+0
      # y = -x + M + 0.5 lines
      for M in range(self.Nx+self.Ny):
        for i in range(self.Nx):
          for i_sub in range(4):
            x1 = i+i_sub*0.25
            y1 = -x1 + M + 0.5
            z1 = Z+0.25*(i_sub%2)
            x2 = i+(i_sub+1)*0.25
            y2 = -x2 + M + 0.5
            z2 = Z+0.25*((i_sub+1)%2)
            if 0<=x1<=self.Nx and 0<=x2<=self.Nx and 0<=y1<=self.Ny and 0<=y2<=self.Ny:
              A = self.cube_side*numpy.array([x1,y1,z1])
              B = self.cube_side*numpy.array([x2,y2,z2])
              line_structure_function(A, B)

    return

class RCD_GWL_Parallelepiped(GWLobject, RCD_CubicLattice):
  
  def __init__(self):
    GWLobject.__init__(self)
    RCD_CubicLattice.__init__(self)

    self.TopDownWriting = True
    
    self.rod_height = 0.1
    self.rod_width = 0.1
    self.connected = True
    self.orthogonal = True
    self.orientation = [0,1,2]
    self.N0 = 3
    self.N1 = 3
    self.N2 = 3
    
    return

  def add_arguments(self, parser):

    parser.add_argument("--TopDownWriting", help="Write from top to bottom", action="store_true", default=True)
  
    parser.add_argument("--rod_height", help="rod height", type=float, default=0.1)
    parser.add_argument("--rod_width", help="rod width", type=float, default=0.05)
    parser.add_argument("--connected", help="connect lines", action="store_true")
    parser.add_argument("--orthogonal", help='orthogonal "z-axis"', action="store_true")
    parser.add_argument("--axis0", help="index of axis 0", choices=[0,1,2],  default=0, type=int)
    parser.add_argument("--axis1", help="index of axis 1", choices=[0,1,2],  default=1, type=int)
    parser.add_argument("--axis2", help="index of axis 2", choices=[0,1,2],  default=2, type=int)
    parser.add_argument("--N0", help="number of lines along axis 0", type=int, default=3)
    parser.add_argument("--N1", help="number of lines along axis 1", type=int, default=3)
    parser.add_argument("--N2", help="number of lines along axis 2", type=int, default=3)

    return
  
  def get_argument_parser(self):
    parser = argparse.ArgumentParser(description = 'Create an RCD based on cubic unit cells and Parallelepiped objects.', fromfile_prefix_chars='@')
    parser.add_argument('-d','--outdir', action="store", dest="outdir", default=tempfile.gettempdir(), help='output directory')
    parser.add_argument('-b','--basename', action="store", dest="basename", default='RCD', help='output basename')
    RCD_CubicLattice.add_arguments(self, parser)
    GWLobject.add_arguments(self, parser)
    self.add_arguments(parser)
    return parser
    
  def setAttributesFromParsedOptions(self, options):
    RCD_CubicLattice.setAttributesFromParsedOptions(self, options)
    GWLobject.setAttributesFromParsedOptions(self, options)

    self.TopDownWriting = options.TopDownWriting
    
    self.rod_height = options.rod_height
    self.rod_width = options.rod_width
    self.connected = options.connected
    self.orthogonal = options.orthogonal
    self.orientation = [options.axis0, options.axis1, options.axis2]
    self.N0 = options.N0
    self.N1 = options.N1
    self.N2 = options.N2

    return
    
  def writeFromParsedOptions(self, options):
    print ("Options: ", options)    
    self.setAttributesFromParsedOptions(options)
    self.computePoints()
    self.updateLimits()
    self.writeGWLWithPowerCompensation(options.outdir + os.sep + options.basename + '.gwl')
    return

  def addParallelepiped(self, start_point, end_point):
    para = Parallelepiped()
    para.connected = self.connected
    res_vec3 = [self.N0, self.N1, self.N2]
    para.LineNumber_vec3 = [res_vec3[self.orientation[0]], res_vec3[self.orientation[1]], res_vec3[self.orientation[2]]]
    para.setFromLine(start_point, end_point, self.rod_width, self.rod_height, self.orthogonal, self.orientation)
    para.computePoints()
    self.addGWLobject(para)
    return

  def computePoints(self):
    self.clear()
    self.createRCD(self.addParallelepiped)
    return

class RCD_GWL_Cylinder(GWLobject, RCD_CubicLattice):
  '''
  .. todo:: Use the tube class once rotated tubes are implemented.
  '''
  
  def __init__(self):
    GWLobject.__init__(self)
    RCD_CubicLattice.__init__(self)

    self.TopDownWriting = True
    
    self.inner_radius = 0.05
    self.outer_radius = 0.1

    self._method = 'vertical lines'
    self.PointDistance_r = 0.02
    self.PointDistance_theta = 0.02
    self.PointDistance_z = 1
    self.zigzag = True
    self.rotateSpirals = True
    self.add_flat_ends = True
    self.closed_loop = True
    
    return

  @property
  def method(self):
      """ method """
      return self._method
  @method.setter
  def method(self, value):
    allowed_values = ['spiral', 'vertical lines', 'horizontal disks']
    if value in allowed_values:
      self._method = value
    else:
      raise ValueError('method must be one of:' + str(allowed_values))

  def add_arguments(self, parser):

    parser.add_argument("--TopDownWriting", help="Write from top to bottom", action="store_true", default=True)

    parser.add_argument("--inner-radius", help="inner radius", type=float, default=0.05)
    parser.add_argument("--outer-radius", help="outer radius", type=float, default=0.1)

    parser.add_argument("--method", help="writing method", type=str, choices=['spiral', 'vertical lines', 'horizontal disks'],  default='spiral')
    parser.add_argument("--PointDistance_r", help="PointDistance_r", type=float, default=0.02)
    parser.add_argument("--PointDistance_theta", help="PointDistance_theta", type=float, default=0.02)
    parser.add_argument("--PointDistance_z", help="PointDistance_z", type=float, default=0.02)
    parser.add_argument("--zigzag", help="zigzag", action="store_true")
    parser.add_argument("--rotateSpirals", help="rotateSpirals", action="store_true")
    parser.add_argument("--add_flat_ends", help="add_flat_ends", action="store_true")
    parser.add_argument("--closed_loop", help="closed_loop", action="store_true")
    return

  def get_argument_parser(self):
    parser = argparse.ArgumentParser(description = 'Create an RCD based on cubic unit cells and Parallelepiped objects.', fromfile_prefix_chars='@')
    parser.add_argument('-d','--outdir', action="store", dest="outdir", default=tempfile.gettempdir(), help='output directory')
    parser.add_argument('-b','--basename', action="store", dest="basename", default='RCD', help='output basename')
    RCD_CubicLattice.add_arguments(self, parser)
    GWLobject.add_arguments(self, parser)
    self.add_arguments(parser)
    return parser
    
  def writeFromParsedOptions(self, options):
    print ("Options: ", options)    
    self.setAttributesFromParsedOptions(options)
    self.computePoints()
    self.updateLimits()
    self.writeGWLWithPowerCompensation(options.outdir + os.sep + options.basename + '.gwl')
    return

  def setAttributesFromParsedOptions(self, options):
    RCD_CubicLattice.setAttributesFromParsedOptions(self, options)
    GWLobject.setAttributesFromParsedOptions(self, options)

    self.TopDownWriting = options.TopDownWriting
    
    self.inner_radius = options.inner_radius
    self.outer_radius = options.outer_radius

    self.method = options.method
    self.PointDistance_r = options.PointDistance_r
    self.PointDistance_theta = options.PointDistance_theta
    self.PointDistance_z = options.PointDistance_z
    self.zigzag = options.zigzag
    self.rotateSpirals = options.rotateSpirals
    self.add_flat_ends = options.add_flat_ends
    self.closed_loop = options.closed_loop

    return

  def addTube(self, start_point, end_point):
    self.addLineCylinder(start_point, end_point, self.PC_laser_power_at_z0, self.inner_radius, self.outer_radius, self.PointDistance_r, self.PointDistance_theta)
    return

  def computePoints(self):
    self.clear()
    self.createRCD(self.addTube)
    return

def createIceCrystal_GWL_singleLine_UnitcellByUnitcell(DSTDIR):
  ''' unit cell by unit cell '''
  
  name = 'IceCrystal'

  a = 1
  offset = numpy.array([0,0,0])

  crystal = GWLobject()

  Nx=1
  Ny=1
  Nz=1

  for i in range(Nx):
   for j in range(Ny):
    for k in range(Nz):
      P0=a*(offset+numpy.sqrt(2)/2*numpy.array([1,1,1])+numpy.array([i*numpy.sqrt(2),j*numpy.sqrt(2),k*numpy.sqrt(2)]))

      P1=a*(offset+numpy.sqrt(2)/2*numpy.array([1,0,0])+numpy.array([i*numpy.sqrt(2),j*numpy.sqrt(2),k*numpy.sqrt(2)]))
      P2=a*(offset+numpy.sqrt(2)/2*numpy.array([0,1,0])+numpy.array([i*numpy.sqrt(2),j*numpy.sqrt(2),k*numpy.sqrt(2)]))
      P3=a*(offset+numpy.sqrt(2)/2*numpy.array([0,0,1])+numpy.array([i*numpy.sqrt(2),j*numpy.sqrt(2),k*numpy.sqrt(2)]))

      P4=a*(offset+numpy.sqrt(2)/4*numpy.array([1,1,1])+numpy.array([i*numpy.sqrt(2),j*numpy.sqrt(2),k*numpy.sqrt(2)]))
      P5=a*(offset+numpy.sqrt(2)/4*numpy.array([1,3,3])+numpy.array([i*numpy.sqrt(2),j*numpy.sqrt(2),k*numpy.sqrt(2)]))
      P6=a*(offset+numpy.sqrt(2)/4*numpy.array([3,1,3])+numpy.array([i*numpy.sqrt(2),j*numpy.sqrt(2),k*numpy.sqrt(2)]))
      P7=a*(offset+numpy.sqrt(2)/4*numpy.array([3,3,1])+numpy.array([i*numpy.sqrt(2),j*numpy.sqrt(2),k*numpy.sqrt(2)]))

      crystal.addLine(P0,P4)
      crystal.addLine(P1,P4)
      crystal.addLine(P2,P4)
      crystal.addLine(P3,P4)

      crystal.addLine(P5,P0)
      crystal.addLine(P6,P0)
      crystal.addLine(P7,P0)

      crystal.addLine(P3+a*numpy.sqrt(2)*numpy.array([0,1,0]),P5)
      crystal.addLine(P2+a*numpy.sqrt(2)*numpy.array([0,0,1]),P5)
      crystal.addLine(P1+a*numpy.sqrt(2)*numpy.array([0,1,1]),P5)

      crystal.addLine(P3+a*numpy.sqrt(2)*numpy.array([1,0,0]),P6)
      crystal.addLine(P2+a*numpy.sqrt(2)*numpy.array([1,0,1]),P6)
      crystal.addLine(P1+a*numpy.sqrt(2)*numpy.array([0,0,1]),P6)

      crystal.addLine(P3+a*numpy.sqrt(2)*numpy.array([1,1,0]),P7)
      crystal.addLine(P2+a*numpy.sqrt(2)*numpy.array([1,0,0]),P7)
      crystal.addLine(P1+a*numpy.sqrt(2)*numpy.array([0,1,0]),P7)

  (mini,maxi) = crystal.getLimits()
  crystal.writeGWL(DSTDIR + os.path.sep + name + '.gwl', writingOffset = [0,0,0,0] )
  #crystal.writeGWL(DSTDIR + os.path.sep + name + '.gwl', writingOffset = [-mini[0],-mini[1],-mini[2],0] )
  #crystal.writeGWL(DSTDIR + os.path.sep + name + '.gwl', writingOffset = [-0.5*(mini[0]+maxi[0]),-0.5*(mini[1]+maxi[1]),-mini[2],0] )
  return

def createIceCrystal_GWL_TopDown(DSTDIR):
  ''' layer by layer '''
  
  name = 'IceCrystalTopDown'
  #name = 'createIceCrystal_GWL_TopDown.singleLines'
  ##  name = 'createIceCrystal_GWL_TopDown.linearCylinder.radius0.150'
  ##  name = 'createIceCrystal_GWL_TopDown.linearCylinder.radius0.500'

  #a=1.600
  #a=3.200
  ##  a=10/numpy.sqrt(2)
  ##  cube_side = numpy.sqrt(2)*a
  cube_side = 1

  offset=numpy.array([0,0,0])

  crystal = GWLobject()

  Nx = 1
  Ny = 1
  Nz = 1

  power = -1
  inner_radius = 0

  ##  outer_radius = 0.500
  ##  outer_radius = 0.150
  outer_radius = 0
  PointDistance_r = 0.150
  PointDistance_theta = 0.150

  # TODO: Make lines continuous (should be one long zigzag line for each "rod")
  # TODO: Flat lines instead of cylinders. WIP.

  for k in range(Nz-1,-1,-1):
    print('k = '+str(k))
    Z = k+0.75
    # y = x + M + 0.5 lines
    for M in range(-Nx,Ny):
      for i in range(Nx):
        for i_sub in range(4):
          x1 = i+i_sub*0.25
          y1 = x1 + M + 0.5
          z1 = Z+0.25*((i_sub+1)%2)
          x2 = i+(i_sub+1)*0.25
          y2 = x2 + M + 0.5
          z2 = Z+0.25*(i_sub%2)
          if 0<=x1<=Nx and 0<=x2<=Nx and 0<=y1<=Ny and 0<=y2<=Ny:
            crystal.addLineCylinder(cube_side*numpy.array([x1,y1,z1]),cube_side*numpy.array([x2,y2, z2]), power, inner_radius, outer_radius, PointDistance_r, PointDistance_theta)

    Z = k+0.5
    # j = -i + M lines
    for M in range(1,Nx+Ny):
      for i in range(Nx):
        for i_sub in range(4):
          x1 = i+i_sub*0.25
          y1 = -x1 + M
          z1 = Z+0.25*(i_sub%2)
          x2 = i+(i_sub+1)*0.25
          y2 = -x2 + M
          z2 = Z+0.25*((i_sub+1)%2)
          if 0<=x1<=Nx and 0<=x2<=Nx and 0<=y1<=Ny and 0<=y2<=Ny:
            crystal.addLineCylinder(cube_side*numpy.array([x1,y1,z1]),cube_side*numpy.array([x2,y2, z2]), power, inner_radius, outer_radius, PointDistance_r, PointDistance_theta)

    Z = k+0.25
    # j = i + M lines
    for M in range(-(Nx-1),Ny):
      for i in range(max(-M,0),min(Ny-M,Nx)):
        for i_sub in range(4):
          x1 = i+i_sub*0.25
          y1 = x1 + M
          z1 = Z+0.25*((i_sub+1)%2)
          x2 = i+(i_sub+1)*0.25
          y2 = x2 + M
          z2 = Z+0.25*(i_sub%2)
          if 0<=x1<=Nx and 0<=x2<=Nx and 0<=y1<=Ny and 0<=y2<=Ny:
            crystal.addLineCylinder(cube_side*numpy.array([x1,y1,z1]),cube_side*numpy.array([x2,y2, z2]), power, inner_radius, outer_radius, PointDistance_r, PointDistance_theta)

    Z = k+0
    # y = -x + M + 0.5 lines
    for M in range(Nx+Ny):
      for i in range(Nx):
        for i_sub in range(4):
          x1 = i+i_sub*0.25
          y1 = -x1 + M + 0.5
          z1 = Z+0.25*(i_sub%2)
          x2 = i+(i_sub+1)*0.25
          y2 = -x2 + M + 0.5
          z2 = Z+0.25*((i_sub+1)%2)
          if 0<=x1<=Nx and 0<=x2<=Nx and 0<=y1<=Ny and 0<=y2<=Ny:
            crystal.addLineCylinder(cube_side*numpy.array([x1,y1,z1]),cube_side*numpy.array([x2,y2, z2]), power, inner_radius, outer_radius, PointDistance_r, PointDistance_theta)

  (mini,maxi) = crystal.getLimits()

  crystal.writeGWL(DSTDIR + os.path.sep + name + '.gwl', writingOffset = [0,0,0,0] )
  #crystal.writeGWL(DSTDIR + os.path.sep + name + '.gwl', writingOffset = [-mini[0],-mini[1],-mini[2],0] )
  return

def createIceCrystal_GWL_TopDownFlatLines(DSTDIR):
  ''' layer by layer '''
  
  # TODO: Alternate line direction in each layer to optimize speed
  name = 'IceCrystalTopDownFlatLines'

  line_distance = 0.100
  line_number = 3

  ##  name = 'createIceCrystal_GWL_TopDown.linearCylinder.radius0.150'
  ##  name = 'createIceCrystal_GWL_TopDown.linearCylinder.radius0.500'

  #a=1.600
  #a=3.200
  ##  a=10/numpy.sqrt(2)
  ##  cube_side = numpy.sqrt(2)*a
  cube_side = 10

  offset=numpy.array([0,0,0])

  crystal = GWLobject()

  Nx = 2
  Ny = 2
  Nz = 1

  power = -1
  #inner_radius = 0

  ##  outer_radius = 0.500
  ##  outer_radius = 0.150
  #outer_radius = 0
  #PointDistance_r = 0.150
  #PointDistance_theta = 0.150

  # TODO: Make lines continuous (should be one long zigzag line for each "rod")
  # TODO: Flat lines instead of cylinders. WIP.

  for k in range(Nz-1,-1,-1):
    print('k = '+str(k))
    Z = k+0.75
    # y = x + M + 0.5 lines
    for M in range(-Nx,Ny):
      for i in range(Nx):
        for i_sub in range(4):
          x1 = i+i_sub*0.25
          y1 = x1 + M + 0.5
          z1 = Z+0.25*((i_sub+1)%2)
          x2 = i+(i_sub+1)*0.25
          y2 = x2 + M + 0.5
          z2 = Z+0.25*(i_sub%2)
          if 0<=x1<=Nx and 0<=x2<=Nx and 0<=y1<=Ny and 0<=y2<=Ny:
            crystal.addFlatLine(cube_side*numpy.array([x1,y1,z1]),cube_side*numpy.array([x2,y2, z2]), line_distance, line_number, power)

    Z = k+0.5
    # j = -i + M lines
    for M in range(1,Nx+Ny):
      for i in range(Nx):
        for i_sub in range(4):
          x1 = i+i_sub*0.25
          y1 = -x1 + M
          z1 = Z+0.25*(i_sub%2)
          x2 = i+(i_sub+1)*0.25
          y2 = -x2 + M
          z2 = Z+0.25*((i_sub+1)%2)
          if 0<=x1<=Nx and 0<=x2<=Nx and 0<=y1<=Ny and 0<=y2<=Ny:
            crystal.addFlatLine(cube_side*numpy.array([x1,y1,z1]),cube_side*numpy.array([x2,y2, z2]), line_distance, line_number, power)

    Z = k+0.25
    # j = i + M lines
    for M in range(-(Nx-1),Ny):
      for i in range(max(-M,0),min(Ny-M,Nx)):
        for i_sub in range(4):
          x1 = i+i_sub*0.25
          y1 = x1 + M
          z1 = Z+0.25*((i_sub+1)%2)
          x2 = i+(i_sub+1)*0.25
          y2 = x2 + M
          z2 = Z+0.25*(i_sub%2)
          if 0<=x1<=Nx and 0<=x2<=Nx and 0<=y1<=Ny and 0<=y2<=Ny:
            crystal.addFlatLine(cube_side*numpy.array([x1,y1,z1]),cube_side*numpy.array([x2,y2, z2]), line_distance, line_number, power)

    Z = k+0
    # y = -x + M + 0.5 lines
    for M in range(Nx+Ny):
      for i in range(Nx):
        for i_sub in range(4):
          x1 = i+i_sub*0.25
          y1 = -x1 + M + 0.5
          z1 = Z+0.25*(i_sub%2)
          x2 = i+(i_sub+1)*0.25
          y2 = -x2 + M + 0.5
          z2 = Z+0.25*((i_sub+1)%2)
          if 0<=x1<=Nx and 0<=x2<=Nx and 0<=y1<=Ny and 0<=y2<=Ny:
            crystal.addFlatLine(cube_side*numpy.array([x1,y1,z1]),cube_side*numpy.array([x2,y2, z2]), line_distance, line_number, power)

  (mini,maxi) = crystal.getLimits()

  crystal.writeGWL(DSTDIR + os.path.sep + name + '.gwl', writingOffset = [0,0,0,0] )
  #crystal.writeGWL(DSTDIR + os.path.sep + name + '.gwl', writingOffset = [-mini[0],-mini[1],-mini[2],0] )
  #crystal.writeGWL(DSTDIR + os.path.sep + name + '.gwl', writingOffset = [-0.5*(mini[0]+maxi[0]),-0.5*(mini[1]+maxi[1]),-mini[2],0] )
  #crystal.writeGWL(DSTDIR + os.path.sep + name + '.gwl', writingOffset = [-0.5*(mini[0]+maxi[0]), -0.5*(mini[1]+maxi[1]), -mini[2] ,0] )
  ##  crystal.writeGWL(DSTDIR + os.path.sep + name + '.gwl', writingOffset = [-7.5,-7.5,-7.5,0] )
  return

def createIceCrystal_GWL_WithCylinders(DSTDIR):
  ''' unit cell by unit cell '''
  
  name = 'IceCrystalWithCylinders'

  a = 1

  offset = numpy.array([0,0,0])

  crystal = GWLobject()

  power = -1
  inner_radius = 0

  outer_radius = 0.3
  PointDistance_r = 0.150
  PointDistance_theta = 0.150

  Nx=1
  Ny=1
  Nz=1

  for i in range(Nx):
   for j in range(Ny):
    for k in range(Nz):
         P0=a*(offset+numpy.sqrt(2)/2*numpy.array([1,1,1])+numpy.array([i*numpy.sqrt(2),j*numpy.sqrt(2),k*numpy.sqrt(2)]))

         P1=a*(offset+numpy.sqrt(2)/2*numpy.array([1,0,0])+numpy.array([i*numpy.sqrt(2),j*numpy.sqrt(2),k*numpy.sqrt(2)]))
         P2=a*(offset+numpy.sqrt(2)/2*numpy.array([0,1,0])+numpy.array([i*numpy.sqrt(2),j*numpy.sqrt(2),k*numpy.sqrt(2)]))
         P3=a*(offset+numpy.sqrt(2)/2*numpy.array([0,0,1])+numpy.array([i*numpy.sqrt(2),j*numpy.sqrt(2),k*numpy.sqrt(2)]))

         P4=a*(offset+numpy.sqrt(2)/4*numpy.array([1,1,1])+numpy.array([i*numpy.sqrt(2),j*numpy.sqrt(2),k*numpy.sqrt(2)]))
         P5=a*(offset+numpy.sqrt(2)/4*numpy.array([1,3,3])+numpy.array([i*numpy.sqrt(2),j*numpy.sqrt(2),k*numpy.sqrt(2)]))
         P6=a*(offset+numpy.sqrt(2)/4*numpy.array([3,1,3])+numpy.array([i*numpy.sqrt(2),j*numpy.sqrt(2),k*numpy.sqrt(2)]))
         P7=a*(offset+numpy.sqrt(2)/4*numpy.array([3,3,1])+numpy.array([i*numpy.sqrt(2),j*numpy.sqrt(2),k*numpy.sqrt(2)]))

         crystal.addLineCylinder(P0, P4, power, inner_radius, outer_radius, PointDistance_r, PointDistance_theta)
         crystal.addLineCylinder(P1, P4, power, inner_radius, outer_radius, PointDistance_r, PointDistance_theta)
         crystal.addLineCylinder(P2, P4, power, inner_radius, outer_radius, PointDistance_r, PointDistance_theta)
         crystal.addLineCylinder(P3, P4, power, inner_radius, outer_radius, PointDistance_r, PointDistance_theta)

         crystal.addLineCylinder(P5, P0, power, inner_radius, outer_radius, PointDistance_r, PointDistance_theta)
         crystal.addLineCylinder(P6, P0, power, inner_radius, outer_radius, PointDistance_r, PointDistance_theta)
         crystal.addLineCylinder(P7, P0, power, inner_radius, outer_radius, PointDistance_r, PointDistance_theta)

         crystal.addLineCylinder(P3+a*numpy.sqrt(2)*numpy.array([0,1,0]), P5, power, inner_radius, outer_radius, PointDistance_r, PointDistance_theta)
         crystal.addLineCylinder(P2+a*numpy.sqrt(2)*numpy.array([0,0,1]), P5, power, inner_radius, outer_radius, PointDistance_r, PointDistance_theta)
         crystal.addLineCylinder(P1+a*numpy.sqrt(2)*numpy.array([0,1,1]), P5, power, inner_radius, outer_radius, PointDistance_r, PointDistance_theta)

         crystal.addLineCylinder(P3+a*numpy.sqrt(2)*numpy.array([1,0,0]), P6, power, inner_radius, outer_radius, PointDistance_r, PointDistance_theta)
         crystal.addLineCylinder(P2+a*numpy.sqrt(2)*numpy.array([1,0,1]), P6, power, inner_radius, outer_radius, PointDistance_r, PointDistance_theta)
         crystal.addLineCylinder(P1+a*numpy.sqrt(2)*numpy.array([0,0,1]), P6, power, inner_radius, outer_radius, PointDistance_r, PointDistance_theta)

         crystal.addLineCylinder(P3+a*numpy.sqrt(2)*numpy.array([1,1,0]), P7, power, inner_radius, outer_radius, PointDistance_r, PointDistance_theta)
         crystal.addLineCylinder(P2+a*numpy.sqrt(2)*numpy.array([1,0,0]), P7, power, inner_radius, outer_radius, PointDistance_r, PointDistance_theta)
         crystal.addLineCylinder(P1+a*numpy.sqrt(2)*numpy.array([0,1,0]), P7, power, inner_radius, outer_radius, PointDistance_r, PointDistance_theta)

  (mini,maxi) = crystal.getLimits()
  crystal.writeGWL(DSTDIR + os.path.sep + name + '.gwl', writingOffset = [0,0,0,0] )
  #crystal.writeGWL(DSTDIR + os.path.sep + name + '.gwl', writingOffset = [-mini[0],-mini[1],-mini[2],0] )
  #crystal.writeGWL(DSTDIR + os.path.sep + name + '.gwl', writingOffset = [-0.5*(mini[0]+maxi[0]),-0.5*(mini[1]+maxi[1]),-mini[2],0] )
  return

def createIceCrystal_BFDTD(DSTDIR, Nx, Ny, Nz, n_defect, n_crystal, n_backfill, cylinder_radius_normalized, fmin_normalized, fmax_normalized, i_sub_defect=0, k_sub_defect=1):
  '''
  To prepare a BFDTD simulation with an RCD/FRD structure.
  
  .. warning:: FRD currently broken! + 2 backfills are created in the case of FRD. DO NOT USE AS IS!!!  

  BFDTD export WIP
  
  .. todo:: review this code and document it.
  .. todo:: Idea: Add clipping function to BFDTD to remove any objects outside a certain area. (could maybe even be extended to advanced boolean stuff! :) )
  
  * a : unit cube size
  * c0 : speed of light
  * Nx : number of periods in the X direction
  * Ny : number of periods in the Y direction
  * Nz : number of periods in the Z direction
  * n_defect : refractive index of the defect
  * n_crystal : refractive index of the crystal
  * n_backfill : refractive index of the backfill
  * cylinder_radius_normalized : r/a
  * excitation_frequency_normalized  : f/(c0/a)
  * fmin_normalized  : fmin/(c0/a)
  * fmax_normalized  : fmax/(c0/a)

  .. todo:: A lot of things:
  
    * Centre excitation on defect
    * Centre defect in sim box
    * adapt size of sim box to geometry
    * clip geometry to given bounding box
    * add epsilon sanpshots
    * add frequency snapshots
    * add time snapshots
    * make it easier to add excitation with specific orientation, size, bandwidth, etc
    * pass orientation through matrix/basis vectors
  
  working in mm, ms, kHz
  '''
  
  name = 'PhotonicCrystallineDiamond'

  cube_side = 1
  cyl_length = cube_side*sqrt(3)/4
  outer_radius = cylinder_radius_normalized*cube_side
  #outer_radius = 0.123
  #cyl_length = 42

  #cyl_length = 3
  #n_crystal = 1
  #n_backfill = 3.3
  
  # number of periods in the X,Y,Z directions
  # Note: FRD is currently only correct when Nx=Ny (simple 90 degree rotation system)
  #Nx = 3
  #Ny = 3
  #Nz = 3
  #cube_side = (4/sqrt(3))*cyl_length
  #outer_radius = 0.26*cyl_length
  #outer_radius = 0.263018408555208*cube_side
  #fmin_kHz = 18e6
  #fmax_kHz = 35e6
  #f0 = 0.5*(fmin_kHz+fmax_kHz)
  excitation_frequency_normalized = (fmin_normalized+fmax_normalized)/2
  #f0 = excitation_frequency_normalized*get_c0()/cube_side
  fmin = fmin_normalized*get_c0()/cube_side
  fmax = fmax_normalized*get_c0()/cube_side

  f0 = 0.5*(fmin+fmax)
  Lambda_mm = get_c0()/f0
  probe_distance = cyl_length
  dipole_length = outer_radius

  #line_distance = 0.1
  #line_number = 3
  #rod_height = 0.05
  #rod_width = 0.05
  #orientation = [2,0,1]
  #orthogonal = True
  offset = numpy.array([0,0,0])
  power = -1
  inner_radius = 0
  PointDistance_r = 0.150
  PointDistance_theta = 0.150

  # defect parameters
  i_defect = Nx//2
  j_defect = Ny//2
  k_defect = Nz//2
  #i_sub_defect = 0
  #k_sub_defect = 1
  #n_defect = 4

  defect_list = []

  crystal = BFDTDobject()
  
  backfill = Block()
  crystal.appendGeometryObject(backfill)

  # k : index of current "Z-layer"
  for k in range(Nz-1,-1,-1):
    
    print('k = '+str(k))
    
    k_sub = 3
    Z = k + k_sub*0.25
    # y = x + M + 0.5 lines
    M_defect = j_defect - i_defect
    for M in range(-Nx,Ny):
      for i in range(Nx):
        for i_sub in range(4):
          x1 = i+i_sub*0.25
          y1 = x1 + M + 0.5
          z1 = Z+0.25*((i_sub+1)%2)
          x2 = i+(i_sub+1)*0.25
          y2 = x2 + M + 0.5
          z2 = Z+0.25*(i_sub%2)
          if 0<=x1<=Nx and 0<=x2<=Nx and 0<=y1<=Ny and 0<=y2<=Ny:
            A = cube_side*numpy.array([x1,y1,z1])
            B = cube_side*numpy.array([x2,y2,z2])
            cyl = Cylinder()
            cyl.setInnerRadius(inner_radius)
            cyl.setOuterRadius(outer_radius)
            cyl.setStartEndPoints(A, B)
            j = floor(((y1+y2)/2)/cube_side)
            #print('(k={}, k_defect={}, M={}, M_defect={}, i={}, i_defect={}, i_sub={}, i_sub_defect={}, k_sub={}, k_sub_defect={})'.format(k,k_defect,M,M_defect,i,i_defect,i_sub,i_sub_defect,k_sub,k_sub_defect))
            if k == k_defect and j == j_defect and i == i_defect and i_sub == i_sub_defect and k_sub == k_sub_defect:
              cyl.name = 'defect'
              cyl.setRefractiveIndex(n_defect)
              defect_list.append(cyl)
              print('Added defect!')
            else:
              cyl.setRefractiveIndex(n_crystal)
              crystal.appendGeometryObject(cyl)
          #else:
            #print('This should not happen', file=sys.stderr)

    k_sub = 2
    Z = k + k_sub*0.25
    # y = -x + M lines
    M_defect = j_defect + i_defect
    for M in range(1,Nx+Ny):
      for i in range(Nx):
        for i_sub in range(4):
          x1 = i+i_sub*0.25
          y1 = -x1 + M
          z1 = Z+0.25*(i_sub%2)
          x2 = i+(i_sub+1)*0.25
          y2 = -x2 + M
          z2 = Z+0.25*((i_sub+1)%2)
          if 0<=x1<=Nx and 0<=x2<=Nx and 0<=y1<=Ny and 0<=y2<=Ny:
            A = cube_side*numpy.array([x1,y1,z1])
            B = cube_side*numpy.array([x2,y2,z2])
            cyl = Cylinder()
            cyl.setInnerRadius(inner_radius)
            cyl.setOuterRadius(outer_radius)
            cyl.setStartEndPoints(A, B)
            #print((k,k_defect,M-1,M_defect,i,i_defect,i_sub,i_sub_defect,k_sub,k_sub_defect))
            if k == k_defect and M-1 == M_defect and i == i_defect and i_sub == i_sub_defect and k_sub == k_sub_defect:
              cyl.name = 'defect'
              cyl.setRefractiveIndex(n_defect)
              defect_list.append(cyl)
              print('Added defect!')
            else:
              cyl.setRefractiveIndex(n_crystal)
              crystal.appendGeometryObject(cyl)
          #else:
            #print('This should not happen', file=sys.stderr)

    k_sub = 1
    Z = k + k_sub*0.25
    # y = x + M lines
    M_defect = j_defect - i_defect
    for M in range(-(Nx-1),Ny):
      for i in range(max(-M,0),min(Ny-M,Nx)):
        for i_sub in range(4):
          x1 = i+i_sub*0.25
          y1 = x1 + M
          z1 = Z+0.25*((i_sub+1)%2)
          x2 = i+(i_sub+1)*0.25
          y2 = x2 + M
          z2 = Z+0.25*(i_sub%2)
          if 0<=x1<=Nx and 0<=x2<=Nx and 0<=y1<=Ny and 0<=y2<=Ny:
            A = cube_side*numpy.array([x1,y1,z1])
            B = cube_side*numpy.array([x2,y2,z2])
            cyl = Cylinder()
            cyl.setInnerRadius(inner_radius)
            cyl.setOuterRadius(outer_radius)
            cyl.setStartEndPoints(A, B)
            #print((k,k_defect,M,M_defect,i,i_defect,i_sub,i_sub_defect,k_sub,k_sub_defect))
            if k == k_defect and M == M_defect and i == i_defect and i_sub == i_sub_defect and k_sub == k_sub_defect:
              cyl.name = 'defect'
              cyl.setRefractiveIndex(n_defect)
              defect_list.append(cyl)
              print('Added defect!')
            else:
              cyl.setRefractiveIndex(n_crystal)
              crystal.appendGeometryObject(cyl)
          #else:
            #print('This should not happen', file=sys.stderr)

    k_sub = 0
    Z = k + k_sub*0.25
    # y = -x + M + 0.5 lines
    M_defect = j_defect + i_defect - 0.5
    for M in range(Nx+Ny):
      for i in range(Nx):
        for i_sub in range(4):
          x1 = i+i_sub*0.25
          y1 = -x1 + M + 0.5
          z1 = Z+0.25*(i_sub%2)
          x2 = i+(i_sub+1)*0.25
          y2 = -x2 + M + 0.5
          z2 = Z+0.25*((i_sub+1)%2)
          if 0<=x1<=Nx and 0<=x2<=Nx and 0<=y1<=Ny and 0<=y2<=Ny:
            A = cube_side*numpy.array([x1,y1,z1])
            B = cube_side*numpy.array([x2,y2,z2])
            cyl = Cylinder()
            cyl.setInnerRadius(inner_radius)
            cyl.setOuterRadius(outer_radius)
            cyl.setStartEndPoints(A, B)
            j = floor(((y1+y2)/2)/cube_side)
            #print('(k={}, k_defect={}, M={}, M_defect={}, i={}, i_defect={}, i_sub={}, i_sub_defect={}, k_sub={}, k_sub_defect={})'.format(k,k_defect,M,M_defect,i,i_defect,i_sub,i_sub_defect,k_sub,k_sub_defect))
            if k == k_defect and j == j_defect and i == i_defect and i_sub == i_sub_defect and k_sub == k_sub_defect:
              cyl.name = 'defect'
              cyl.setRefractiveIndex(n_defect)
              defect_list.append(cyl)
              print('Added defect!')
            else:
              cyl.setRefractiveIndex(n_crystal)
              crystal.appendGeometryObject(cyl)
          #else:
            #print('This should not happen', file=sys.stderr)

  # add defect at the end to put it over the other defects
  # TODO: Maybe add option to put it under the other cylinders? (add layer system and move to front/back/layer X system to BFDTDobject)
  
  defect_pos = defect_list[0].getCentro()
  defect = Sphere()
  defect.setLocation(defect_pos)
  defect.setInnerRadius(0)
  defect.setOuterRadius(0.5*cyl_length)
  defect.name = 'defect'
  defect.setRefractiveIndex(n_defect)
  #defect_list = [defect]
  
  for idx,defect in enumerate(defect_list):
    print('Adding defect {}/{}'.format(idx+1,len(defect_list)))
    crystal.appendGeometryObject(defect)

  crystal.setSizeAndResolution(cube_side*array([Nx+2,Ny+2,Nz+2]),20*array([Nx+2,Ny+2,Nz+2]))
  foo1 = list(linspace(0,3,20*3+1))
  foo2 = list(linspace(3,4,8*4+1))
  foo3 = list(linspace(4,7,20*3+1))
  foo = foo1 + foo2[1:] + foo3[1:]
  crystal.mesh.setXmesh(foo)
  crystal.mesh.setYmesh(foo)
  crystal.mesh.setZmesh(foo)

  (xmesh, ymesh, zmesh) = crystal.mesh.getMesh()
  delta = xmesh[1]-xmesh[0]
  
  # TODO: Add backfill option to BFDTD object (when writing without geom, should leave in backfill)

  #crystal.writeGeoFile(DSTDIR + os.path.sep + name + '.geo')

  geometry_translation_vector = cube_side*array([1,1,1])
  crystal.translate(geometry_translation_vector)
  # rotate here
  #crystal.rotate([0,0,0], [0,1,0], 90)

  backfill.setSize(crystal.box.getSize())
  backfill.setLocation(crystal.box.getCentro())
  backfill.setRefractiveIndex(n_backfill)

  P_input_excitation = defect_pos + geometry_translation_vector

  probe_defect = Probe(position = P_input_excitation); probe_defect.name = 'probe_defect_Centro'
  probe_defect.setStep(1)
  crystal.probe_list.append(probe_defect)

  probe_defect = Probe(position = P_input_excitation + probe_distance*array([1,0,0])); probe_defect.name = 'probe_defect_X'
  probe_defect.setStep(1)
  crystal.probe_list.append(probe_defect)

  probe_defect = Probe(position = P_input_excitation + probe_distance*array([0,1,0])); probe_defect.name = 'probe_defect_Y'
  probe_defect.setStep(1)
  crystal.probe_list.append(probe_defect)

  probe_defect = Probe(position = P_input_excitation + probe_distance*array([0,0,1])); probe_defect.name = 'probe_defect_Z'
  probe_defect.setStep(1)
  crystal.probe_list.append(probe_defect)

  #crystal.boundaries.setBoundaryConditionsToPML()

  #crystal.setIterations(100)
  crystal.setIterations(2e6)

  ##################
  # excitation

  #excitation = Excitation()
  #excitation.setLambda(cube_side)
  #delta = array([0,0,0.25*cube_side])
  #excitation.setExtension(crystal.box.getCentro()-delta,crystal.box.getCentro()+delta)
  #crystal.appendExcitation(excitation)

  #C = crystal.box.getCentro()
  #C[2] = 0.5*cube_side

  #radius = 0.5*Lambda_mm

  #excitation = ExcitationWithGaussianTemplate()
  #excitation = ExcitationWithUniformTemplate()
  excitation = Excitation()
  excitation.setName('input')
  #excitation.setFrequency(f0)
  excitation.setFrequencyRange(fmin,fmax)
  excitation.setCentro(P_input_excitation)
  excitation.setEx()
  excitation.setSize([dipole_length,0,0])

  #excitation.sigma_x = radius
  #excitation.sigma_y = radius
  #excitation.amplitude = 1
  excitation.plane_direction = 'z'
  #excitation.excitation_direction = ['Exre']
  
  #excitation.template_filename = 'input.dat'
  
  #L = crystal.box.getLower()
  #print(('L = ',L))
  #U = crystal.box.getUpper()
  #L[2] = P_input_excitation[2]
  #print(('L = ',L))
  #U[2] = P_input_excitation[2]
  #L = L + 8*array([delta, delta, 0])
  #print(('L = ',L))
  #U = U - 8*array([delta, delta, 0])
  #L = [0,0,0]
  #print(('L = ',L))
  
  #excitation.setExtension(defect_pos + 0.5*excitation_size*excitation_direction,)
  
  #print(excitation)
  crystal.appendExcitation(excitation)
  ##################

  ##################
  ## measurement objects
  #C = crystal.box.getCentro()
  #C[2] = 0.75*cube_side
  #P_input = C

  #C = crystal.box.getCentro()
  #C[2] = crystal.box.getUpper()[2] - 0.5*cube_side
  #P_output = C

  #probe_input = Probe(position = P_input); probe_input.name = 'probe_input'
  #crystal.probe_list.append(probe_input)
  #probe_output = Probe(position = P_output); probe_output.name = 'probe_output'
  #crystal.probe_list.append(probe_output)

  #crystal.addModeFilteredProbe('z',P_input)
  #crystal.addModeFilteredProbe('z',P_output)
  ##################

  crystal.setExecutable('fdtd64_2013')
  crystal.setWallTime(360)
  crystal.setFileBaseName(name)

  excitation.setEx()
  excitation.setSize([dipole_length, 0, 0])
  crystal.writeTorqueJobDirectory(DSTDIR+os.path.sep+'Ex')

  excitation.setEy()
  excitation.setSize([0, dipole_length, 0])
  crystal.writeTorqueJobDirectory(DSTDIR+os.path.sep+'Ey')

  excitation.setEz()
  excitation.setSize([0, 0, dipole_length])
  crystal.writeTorqueJobDirectory(DSTDIR+os.path.sep+'Ez')
  
  ##################
  # ROTATION STUFF, to finish later eventually

  #(xmesh, ymesh, zmesh) = crystal.mesh.getMesh()

  #for x in xmesh:
    #crystal.addEpsilonSnapshot('x',x)

  #crystal.addEpsilonSnapshot('x',crystal.box.getCentro())
  #crystal.addEpsilonSnapshot('y',crystal.box.getCentro())
  #crystal.addEpsilonSnapshot('z',crystal.box.getCentro())

  #alpha_to_xy_deg = degrees(numpy.arctan(1/sqrt(2)))
  #alpha_to_z_deg = degrees(numpy.arccos(-1/sqrt(3)))
  #rotation_centro = defect_pos + geometry_translation_vector

  #crystal.writeGeoFile(DSTDIR+os.path.sep+'normal.geo')
  #return
  
  #Xaligned = copy.deepcopy(crystal)
  #Xaligned.rotate(rotation_centro, [1,-1,0], alpha_to_xy_deg)
  #Xaligned.rotate(rotation_centro, [0,0,1], -45)
  ##Xaligned.excitation_li
  #Xaligned.writeGeoFile(DSTDIR+os.path.sep+'X.geo')

  #Yaligned = copy.deepcopy(crystal)
  #Yaligned.rotate(rotation_centro, [1,-1,0], alpha_to_xy_deg)
  #Yaligned.rotate(rotation_centro, [0,0,1], 45)
  #Yaligned.writeGeoFile(DSTDIR+os.path.sep+'Y.geo')
  
  #Zaligned = copy.deepcopy(crystal)
  #Zaligned.rotate(rotation_centro, [1,-1,0], alpha_to_z_deg)
  #Zaligned.rotate(rotation_centro, [0,0,1], -45)
  #Zaligned.writeGeoFile(DSTDIR+os.path.sep+'Z.geo')

  ##crystal.writeGeoFile(DSTDIR+os.path.sep+'rotated45.geo')
  ##crystal.rotate([0,0,0], [0,1,0], 90)
  ##crystal.writeGeoFile(DSTDIR+os.path.sep+'rotated90.geo')
  #return
  
  #superfunc = lambda x: crystal.writeShellScript(x, BASENAME=None, EXE='fdtd64_2013', WORKDIR='$JOBDIR', WALLTIME=360)

  #crystal.writeAll(DSTDIR+os.path.sep+'PCD_withGeom', name, withGeom=True, writeShellScriptFunction=superfunc)
  #crystal.writeAll(DSTDIR+os.path.sep+'PCD_withoutGeom',name, withGeom=False, writeShellScriptFunction=superfunc)

  FRD = copy.deepcopy(crystal.geometry_object_list)
  for i in FRD:
    i.rotate(crystal.box.getCentro(),[0,0,1],90)
    i.setRefractiveIndex(1.2)
  crystal.geometry_object_list += FRD
  crystal.clearFileList() # TODO: Maybe do something so this isn't necessary anymore? Is unintuitive.

  crystal.setFileBaseName(name+'_FRD')
  crystal.writeTorqueJobDirectory(DSTDIR + os.path.sep + 'FRD_withGeom')
  #crystal.writeAll(DSTDIR+os.path.sep+'FRD_withoutGeom',name+'_FRD', withGeom=False, writeShellScriptFunction=superfunc)

  return

def test_RCD_GWL():
  time_start = time.time()
  
  DSTDIR = tempfile.mkdtemp()
  
  print( 'Output in ' + DSTDIR)

  createIceCrystal_GWL_singleLine_UnitcellByUnitcell(DSTDIR)
  createIceCrystal_GWL_WithCylinders(DSTDIR)
  createIceCrystal_GWL_TopDown(DSTDIR)
  createIceCrystal_GWL_TopDownFlatLines(DSTDIR)

  print("Elapsed time: %.4f sec" % (time.time() - time_start))
  return

def test_RCD_BFDTD_unitcell():

  WORKDIR = tempfile.mkdtemp()

  N=1

  Nx=Ny=Nz=N
  n_backfill=1.00
  n_crystal=3.60
  n_defect=1.52
  cylinder_radius_normalized=0.26*sqrt(3)/4
  fmin_normalized = 0.45
  fmax_normalized = 0.65
  excitation_frequency_normalized = (fmin_normalized+fmax_normalized)/2

  for i_sub_defect in [0,1,2,3]:
    for k_sub_defect in [0,1,2,3]:
      print('i_sub_defect = ', i_sub_defect)
      print('k_sub_defect = ', k_sub_defect)
      DSTDIR = WORKDIR + os.sep + 'i-{}_j-{}'.format(i_sub_defect,k_sub_defect)
      createIceCrystal_BFDTD(DSTDIR, Nx, Ny, Nz, n_defect, n_crystal, n_backfill, cylinder_radius_normalized, fmin_normalized, fmax_normalized, i_sub_defect, k_sub_defect)

  return

def test_RCD_BFDTD_0():
  
  WORKDIR = tempfile.mkdtemp()
  
  res_vec3 = [10,3,2]
  base_name = 'IcePara'
  PCslope = 0.0137
  iface = 0.5

  i_sub_defect = 0
  k_sub_defect = 1
  delta_f = 1.2

  N=3
  
  Nx=Ny=Nz=N
  n_backfill=1
  n_crystal=3.6
  n_defect=1.52
  cylinder_radius_normalized=0.26*sqrt(3)/4
  excitation_frequency_normalized=0.52
  DSTDIR = WORKDIR + os.sep + 'N={}x{}x{}.n_defect={:.2f}.n_crystal={:.2f}.n_backfill={:.2f}.rn={:.3f}.f0n={:.3f}'.format(Nx, Ny, Nz, n_defect, n_crystal, n_backfill, cylinder_radius_normalized, excitation_frequency_normalized)
  createIceCrystal_BFDTD(DSTDIR, Nx, Ny, Nz, n_defect, n_crystal, n_backfill, cylinder_radius_normalized, excitation_frequency_normalized-delta_f, excitation_frequency_normalized+delta_f, i_sub_defect, k_sub_defect)

  Nx=Ny=Nz=N
  n_backfill=4.1
  n_crystal=1
  n_defect=n_backfill
  cylinder_radius_normalized=0.27
  excitation_frequency_normalized=(0.6226+0.4467)/2
  DSTDIR = WORKDIR + os.sep + 'N={}x{}x{}.n_defect={:.2f}.n_crystal={:.2f}.n_backfill={:.2f}.rn={:.3f}.f0n={:.3f}'.format(Nx, Ny, Nz, n_defect, n_crystal, n_backfill, cylinder_radius_normalized, excitation_frequency_normalized)
  createIceCrystal_BFDTD(DSTDIR, Nx, Ny, Nz, n_defect, n_crystal, n_backfill, cylinder_radius_normalized, excitation_frequency_normalized-delta_f, excitation_frequency_normalized+delta_f, i_sub_defect, k_sub_defect)

  Nx=Ny=Nz=N
  n_backfill=3.5
  n_crystal=1
  n_defect=n_backfill
  cylinder_radius_normalized=0.27
  excitation_frequency_normalized=(0.5147+0.6785)/2
  DSTDIR = WORKDIR + os.sep + 'N={}x{}x{}.n_defect={:.2f}.n_crystal={:.2f}.n_backfill={:.2f}.rn={:.3f}.f0n={:.3f}'.format(Nx, Ny, Nz, n_defect, n_crystal, n_backfill, cylinder_radius_normalized, excitation_frequency_normalized)
  createIceCrystal_BFDTD(DSTDIR, Nx, Ny, Nz, n_defect, n_crystal, n_backfill, cylinder_radius_normalized, excitation_frequency_normalized-delta_f, excitation_frequency_normalized+delta_f, i_sub_defect, k_sub_defect)

  Nx=Ny=Nz=N
  n_backfill=3.3
  n_crystal=1
  n_defect=n_backfill
  cylinder_radius_normalized=0.26
  excitation_frequency_normalized=(0.5140+0.6598)/2
  DSTDIR = WORKDIR + os.sep + 'N={}x{}x{}.n_defect={:.2f}.n_crystal={:.2f}.n_backfill={:.2f}.rn={:.3f}.f0n={:.3f}'.format(Nx, Ny, Nz, n_defect, n_crystal, n_backfill, cylinder_radius_normalized, excitation_frequency_normalized)
  createIceCrystal_BFDTD(DSTDIR, Nx, Ny, Nz, n_defect, n_crystal, n_backfill, cylinder_radius_normalized, excitation_frequency_normalized-delta_f, excitation_frequency_normalized+delta_f, i_sub_defect, k_sub_defect)

  Nx=Ny=Nz=N
  n_backfill=2.4
  n_crystal=1
  n_defect=n_backfill
  cylinder_radius_normalized=0.24
  excitation_frequency_normalized=(0.6210+0.6941)/2
  DSTDIR = WORKDIR + os.sep + 'N={}x{}x{}.n_defect={:.2f}.n_crystal={:.2f}.n_backfill={:.2f}.rn={:.3f}.f0n={:.3f}'.format(Nx, Ny, Nz, n_defect, n_crystal, n_backfill, cylinder_radius_normalized, excitation_frequency_normalized)
  createIceCrystal_BFDTD(DSTDIR, Nx, Ny, Nz, n_defect, n_crystal, n_backfill, cylinder_radius_normalized, excitation_frequency_normalized-delta_f, excitation_frequency_normalized+delta_f, i_sub_defect, k_sub_defect)

  return

def test_RCD_BFDTD_1():

  WORKDIR = tempfile.mkdtemp()

  N=3

  Nx=Ny=Nz=N
  n_backfill=1.00
  n_crystal=4
  n_defect=2
  cylinder_radius_normalized=0.26*sqrt(3)/4
  fmin_normalized = 0.45
  fmax_normalized = 0.65
  excitation_frequency_normalized = (fmin_normalized+fmax_normalized)/2
  DSTDIR = WORKDIR + os.sep + 'N={}x{}x{}.n_defect={:.2f}.n_crystal={:.2f}.n_backfill={:.2f}.rn={:.3f}.f0n={:.3f}'.format(Nx, Ny, Nz, n_defect, n_crystal, n_backfill, cylinder_radius_normalized, excitation_frequency_normalized)
  createIceCrystal_BFDTD(DSTDIR, Nx, Ny, Nz, n_defect, n_crystal, n_backfill, cylinder_radius_normalized, fmin_normalized, fmax_normalized)

  Nx=Ny=Nz=N
  n_backfill=2.40
  n_crystal=1
  n_defect=2.40
  cylinder_radius_normalized=0.5542563*sqrt(3)/4
  fmin_normalized = 0.621
  fmax_normalized = 0.6941
  excitation_frequency_normalized = (fmin_normalized+fmax_normalized)/2
  DSTDIR = WORKDIR + os.sep + 'N={}x{}x{}.n_defect={:.2f}.n_crystal={:.2f}.n_backfill={:.2f}.rn={:.3f}.f0n={:.3f}'.format(Nx, Ny, Nz, n_defect, n_crystal, n_backfill, cylinder_radius_normalized, excitation_frequency_normalized)
  createIceCrystal_BFDTD(DSTDIR, Nx, Ny, Nz, n_defect, n_crystal, n_backfill, cylinder_radius_normalized, fmin_normalized, fmax_normalized)

  Nx=Ny=Nz=N
  n_backfill=3.30
  n_crystal=1
  n_defect=3.30
  cylinder_radius_normalized=0.6004443*sqrt(3)/4
  fmin_normalized = 0.514
  fmax_normalized = 0.6598
  excitation_frequency_normalized = (fmin_normalized+fmax_normalized)/2
  DSTDIR = WORKDIR + os.sep + 'N={}x{}x{}.n_defect={:.2f}.n_crystal={:.2f}.n_backfill={:.2f}.rn={:.3f}.f0n={:.3f}'.format(Nx, Ny, Nz, n_defect, n_crystal, n_backfill, cylinder_radius_normalized, excitation_frequency_normalized)
  createIceCrystal_BFDTD(DSTDIR, Nx, Ny, Nz, n_defect, n_crystal, n_backfill, cylinder_radius_normalized, fmin_normalized, fmax_normalized)

  Nx=Ny=Nz=N
  n_backfill=3.50
  n_crystal=1
  n_defect=3.50
  cylinder_radius_normalized=0.6235383*sqrt(3)/4
  fmin_normalized = 0.5147
  fmax_normalized = 0.6785
  excitation_frequency_normalized = (fmin_normalized+fmax_normalized)/2
  DSTDIR = WORKDIR + os.sep + 'N={}x{}x{}.n_defect={:.2f}.n_crystal={:.2f}.n_backfill={:.2f}.rn={:.3f}.f0n={:.3f}'.format(Nx, Ny, Nz, n_defect, n_crystal, n_backfill, cylinder_radius_normalized, excitation_frequency_normalized)
  createIceCrystal_BFDTD(DSTDIR, Nx, Ny, Nz, n_defect, n_crystal, n_backfill, cylinder_radius_normalized, fmin_normalized, fmax_normalized)

  Nx=Ny=Nz=N
  n_backfill=4.10
  n_crystal=1
  n_defect=4.10
  cylinder_radius_normalized=0.6235383*sqrt(3)/4
  fmin_normalized = 0.4467
  fmax_normalized = 0.6226
  excitation_frequency_normalized = (fmin_normalized+fmax_normalized)/2
  DSTDIR = WORKDIR + os.sep + 'N={}x{}x{}.n_defect={:.2f}.n_crystal={:.2f}.n_backfill={:.2f}.rn={:.3f}.f0n={:.3f}'.format(Nx, Ny, Nz, n_defect, n_crystal, n_backfill, cylinder_radius_normalized, excitation_frequency_normalized)
  createIceCrystal_BFDTD(DSTDIR, Nx, Ny, Nz, n_defect, n_crystal, n_backfill, cylinder_radius_normalized, fmin_normalized, fmax_normalized)
  return

def test_RCD_BFDTD_2():
  DSTDIR = tempfile.mkdtemp()
  Nx = 3
  Ny = 3
  Nz = 3
  n_defect = 2
  n_crystal = 3
  n_backfill = 4
  cylinder_radius_normalized = 0.1
  excitation_frequency_normalized = 6
  fmin_normalized = 7
  fmax_normalized = 8
  i_sub_defect = 2
  k_sub_defect = 3

  delta_f = 3.4
  
  createIceCrystal_BFDTD(DSTDIR, Nx, Ny, Nz, n_defect, n_crystal, n_backfill, cylinder_radius_normalized, excitation_frequency_normalized-delta_f, excitation_frequency_normalized+delta_f)
  createIceCrystal_BFDTD(DSTDIR, Nx, Ny, Nz, n_defect, n_crystal, n_backfill, cylinder_radius_normalized, fmin_normalized, fmax_normalized)
  createIceCrystal_BFDTD(DSTDIR, Nx, Ny, Nz, n_defect, n_crystal, n_backfill, cylinder_radius_normalized, fmin_normalized, fmax_normalized)
  createIceCrystal_BFDTD(DSTDIR, Nx, Ny, Nz, n_defect, n_crystal, n_backfill, cylinder_radius_normalized, fmin_normalized, fmax_normalized, i_sub_defect, k_sub_defect)
  return

if __name__ == "__main__":
  # TODO: Fix FRD cylinder rotation and double backfill
  test_RCD_GWL()
  test_RCD_BFDTD_unitcell()
  test_RCD_BFDTD_0()
  test_RCD_BFDTD_1()
  test_RCD_BFDTD_2()
  
  obj = RCD_GWL_Parallelepiped()
  obj.computePoints()
  obj.updateLimits()
  obj.writeGWLWithPowerCompensation('/tmp/RCD.gwl')

  obj = RCD_GWL_Cylinder()
  obj.computePoints()
  obj.updateLimits()
  obj.writeGWLWithPowerCompensation('/tmp/lol.gwl')
