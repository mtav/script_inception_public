#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
import tempfile
from numpy import arange, cos, sin, floor, radians, isnan, NaN
from GWL.GWL_parser import GWLobject
from utilities.common import matlab_range
from utilities.createGUI import createGUI

class SpiralPhasePlate(GWLobject):

  '''Spiral phase plate

  Original algorithm and documentation by Dave Philips.
  Code ported to python3 by Mike Taverne, with added PyQt GUI and Blender addon.

  This program generates coordinates to draw a spiral phase plate in the nanoscribe.
  The coordinates are ordered from top to bottom.
  Each layer is a series of concentric circels, with the z values changed to draw the appropriate tilted surface with a step.
  Each layer is drawn from the inside out (I'm not sure if inside out or outside in is best).
  I had some earlier problems with the disk spliting apart when developed at the discontinuity, so I have made sure that each ring is properly joined to itself. 

  There is a commented out if stataement in the middle of the coordinate for loop (lines 57 and 60), if you uncomment this then it will truncate the coordinates when their z values go negative.

  The coordinates are produced in a big list with Nan in place of where nanoscribe needs a 'write' command.
  At the end, the coordinates are written to a file called 'spiralphaseplate.gwl', and the lines containing Nans are converted to 'write'.

  If the coordinate list is less than 5000 rows long then it is also plotted within Matlab.

  Check that the created file is the same as the one created by the Matlab script:
  octave Phase_plate.m && ./rewriteGWL.py spiralphaseplate.gwl spiralphaseplate.PP.gwl && python3 Phase_plate.py && ./rewriteGWL.py spiralphaseplate2.gwl spiralphaseplate2.PP.gwl && diff spiralphaseplate.PP.gwl spiralphaseplate2.PP.gwl && checkcmd

  octave Phase_plate.m
  ./rewriteGWL.py spiralphaseplate.gwl spiralphaseplate.PP.gwl
  python3 Phase_plate.py
  diff spiralphaseplate.PP.gwl /tmp/spiralphaseplate.gwl
  grep -c Write spiralphaseplate.PP.gwl /tmp/spiralphaseplate.gwl

  for i in 1 2 3 4; do diff -q "$HOME/Desktop/spiralphaseplate_${i}.gwl" "/tmp/spiralphaseplate_${i}.PP.gwl"; done

  Structural Parameter Inputs:

  .. todo:: Update this documentation.
  .. todo:: TopToBottom and similar variables should be part of GWLobject...
  .. todo:: Add formula shown by Daniel to calculate height from number of discontinuities (OAM mode?)
  '''

  def __init__(self):
    
    super().__init__()
    
    self.maxHeight = 0.85/1.52 #: height of phase step in microns
    self.radius = 4.275 #: radius of phase plate in microns
    self.N_Discontinuities = 4 #: number of steps around 360 degrees - this parameter is redundant as when you're fabricating it, you only ever need 1 step, the height of which you can change to be any multiple of 2pi  
    self.phiStep = 2 #: angular separation of each writing anchor point around a circle, in degrees
    self.radialStep = 0.2 #: distance apart of each ring, in microns
    self.heightStep = 0.3 #: distance appart of each layer, in microns
    self.N_HeightSteps = 7 #: number of additional layers to draw beyond the top layer, i.e. if N_HeightSteps = 2, then total number of layers in the structure = 3)
    self.truncateBottom = False
    self.minZ = -0.001
    return

  def computePoints(self):
    
    self.clear()
    
    maxAngle = 360/self.N_Discontinuities;
    noRadialSteps = floor(self.radius/self.radialStep);

    startAngle = []
    finishAngle = []

    self.startNewVoxelSequence()

    for s in matlab_range(0, 1, self.N_HeightSteps):
      if len(self.GWL_voxels[-1]) > 0:
        self.startNewVoxelSequence()
      for radiusHere in matlab_range(0, self.radialStep, self.radius):
        if len(self.GWL_voxels[-1]) > 0:
          self.startNewVoxelSequence()
        for dis in matlab_range(1, 1, self.N_Discontinuities):
          startAngle.append( (dis-1)*maxAngle );
          finishAngle.append( startAngle[-1] + maxAngle );
          if len(self.GWL_voxels[-1]) > 0:
            self.startNewVoxelSequence()
          for phi in matlab_range(startAngle[dis-1], self.phiStep, finishAngle[dis-1]):
            x = radiusHere*cos(radians(phi));
            y = radiusHere*sin(radians(phi));
            h = self.maxHeight*(1 - (phi-startAngle[dis-1])/(maxAngle)) - s*self.heightStep;
            if (not self.truncateBottom) or (h >= self.minZ):
              self.addVoxel([x, y, h])
            if ((phi == finishAngle[dis-1]) and (s == 0)):
              self.addVoxel([x, y, self.maxHeight])
    return
  
  def get_argument_parser(self):
    parser = argparse.ArgumentParser(description = self.__doc__.split('\n')[0], fromfile_prefix_chars='@')
    parser.add_argument('-d','--outdir', action="store", dest="outdir", default=tempfile.gettempdir(), help='output directory')
    parser.add_argument('-b','--basename', action="store", dest="basename", default='SpiralPhasePlate', help='output basename')
    GWLobject.add_arguments(self, parser)
    self.add_arguments(parser)
    return parser
  
  def add_arguments(self, parser):
    parser.add_argument("--maxHeight", help="height of phase step in microns", type=float, default=self.maxHeight)
    parser.add_argument("--radius", help="radius of phase plate in microns", type=float, default=self.radius)
    parser.add_argument("--N_Discontinuities", help="number of steps around 360 degrees", type=int, default=self.N_Discontinuities)
    parser.add_argument("--phiStep", help="angular separation of each writing anchor point around a circle, in degrees", type=float, default=self.phiStep)
    parser.add_argument("--radialStep", help="distance apart of each ring, in microns", type=float, default=self.radialStep)
    parser.add_argument("--heightStep", help="distance appart of each layer, in microns", type=float, default=self.heightStep)
    parser.add_argument("--N_HeightSteps", help="number of additional layers to draw beyond the top layer, i.e. if N_HeightSteps = 2, then total number of layers in the structure = 3)", type=int, default=self.N_HeightSteps)
    parser.add_argument("--truncateBottom", help="truncate bottom", action="store_true", default=False)
    parser.add_argument("--minZ", help="Z position under which to truncate", type=float, default=self.minZ)
    return

  def writeFromParsedOptions(self, options):
    print ("Options: ", options)    
    self.setAttributesFromParsedOptions(options)
    self.computePoints()
    self.updateLimits()
    self.writeGWLWithPowerCompensation(options.outdir + os.sep + options.basename + '.gwl')
    return

  def setAttributesFromParsedOptions(self, options):
    GWLobject.setAttributesFromParsedOptions(self, options)
    self.maxHeight = options.maxHeight
    self.radius = options.radius
    self.N_Discontinuities = options.N_Discontinuities
    self.phiStep = options.phiStep
    self.radialStep = options.radialStep
    self.heightStep = options.heightStep
    self.N_HeightSteps = options.N_HeightSteps
    self.truncateBottom = options.truncateBottom
    self.minZ = options.minZ
    return

def testSpirals():

  obj = SpiralPhasePlate()
  obj.maxHeight = 0.85/1.52
  obj.radius = 4.275
  obj.phiStep = 2
  obj.radialStep = 0.2
  obj.heightStep = 0.3
  obj.N_HeightSteps = 7
  obj.truncateBottom = False
  obj.minZ = -0.001
  
  for i in [1,2,3,4]:
    obj.N_Discontinuities = i
    obj.computePoints()
    obj.updateLimits()
    outfile1 = tempfile.gettempdir() + os.sep + 'spiralphaseplate_'+str(i)+'.gwl'
    outfile2 = tempfile.gettempdir() + os.sep + 'spiralphaseplate_'+str(i)+'.PP.gwl'
    obj.writeGWLWithPowerCompensation(outfile1)
    
    a = GWLobject()
    a.readGWL(outfile1)
    a.writeGWLWithPowerCompensation(outfile2)

  obj = SpiralPhasePlate()
  obj.truncateBottom = True
  obj.minZ = -1
  obj.computePoints()
  obj.writeGWLWithPowerCompensation('foo.gwl')
  return

def testGWLobject():
  A = SpiralPhasePlate()
  A.addVoxel([1,2,3])
  print('after first add', A.GWL_voxels)
  A.clear()
  print('after clear', A.GWL_voxels)
  A.addVoxel([4,5,6])
  print('after second add', A.GWL_voxels)
  return
  
if __name__ == "__main__":
  #testSpirals()
  #print('====================')
  #testGWLobject()
  createGUI(SpiralPhasePlate())
