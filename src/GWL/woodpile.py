#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy
import bfdtd
from GWL.GWL_parser import *
from bfdtd.bfdtd_parser import *
import GWL.tilted_grating

class Woodpile(object):
  
  '''
  This class allows you to create BFDTD and GWL files for a woodpile crystal.
  
  .. todo:: Is there a better way to define properties? (shorter code)
  .. todo:: Same as with meshing: First carefully think through the GWL/BFDTD woodpile system, then implement. Should be as flexible as possible (offsets, shifts, etc), while remaining simple to use.
  '''
  @property
  def Nlayers_Z(self):
      """Number of layers in the Z direction"""
      return self._Nlayers_Z

  @Nlayers_Z.setter
  def Nlayers_Z(self, value):
    try:
      self._Nlayers_Z = int(value)
    except ValueError:
        print("Could not convert value to an integer.")
        raise

  @property
  def NRodsPerLayer_X(self):
      """Number of rods in a layer in the X direction"""
      return self._NRodsPerLayer_X

  @NRodsPerLayer_X.setter
  def NRodsPerLayer_X(self, value):
    try:
      self._NRodsPerLayer_X = int(value)
    except ValueError:
        print("Could not convert value to an integer.")
        raise

  @property
  def NRodsPerLayer_Y(self):
      """Number of rods in a layer in the Y direction"""
      return self._NRodsPerLayer_Y

  @NRodsPerLayer_Y.setter
  def NRodsPerLayer_Y(self, value):
    try:
      self._NRodsPerLayer_Y = int(value)
    except ValueError:
        print("Could not convert value to an integer.")
        raise

  def __init__(self):
    self._Nlayers_Z = 12
    self._NRodsPerLayer_X = 17
    self._NRodsPerLayer_Y = 17

    # TODO: create get/set functions for rod width/height + interRodDistance/interLayerDistance
    # NOTE: Keep rod width/height + interRodDistance/interLayerDistance, etc separate for more flexibility or not?
    self.rod_width = 0.100
    self.rod_height = 0.200

    self.LineNumber_X = 1
    self.LineDistance_X = 0.050
    self.LineNumber_Y = 1
    self.LineDistance_Y = 0.050
    self.LineNumber_Z = 1
    self.LineDistance_Z = 0.100

    # TODO: Pass function/class name directly in order the facilitate extendability. Might require arguments to be class attributes so the function/class can access them.
    #self.rod_type = 'line'
    self.rod_type = 'block'
    #self.rod_type = 'cylinder'
    
    self.interLayerDistance = 0.212
    self.interRodDistance = 0.600

    # TODO: Get rid of this, since there are already GWL translating functions?
    self.offset = numpy.array([0,0,0]) # general offset of the whole structure, added to all points

    # self.bottomLayerYPeriodic = True: ->first written layer will be periodic in the Y direction
    # else: first written layer will be periodic in the X direction
    self.bottomLayerYPeriodic = False

    self.BottomToTop = False # True=write from bottom to top, False=write from top to bottom    
    self.isSymmetrical = True # If True, the layers will alternate between N and N+1 rods per layer to enable central symmetry, otherwise all layers will have the same number of rods.
    
    # These variables determine whether the first written layer of type X-periodic or Y-periodic is shifted or not.
    # The following layers will be changed accordingly. Essentially, it allows vertical shifting of the layers.
    # This allows you to create "ADCB" instead of "ABCD" woodpiles.
    # (affected by BottomToTop! (TODO: fix this))
    # TODO: Allow creation of "ABAB" woodpiles... Or even more complex?
    self.shiftInitialLayerType_X = False
    self.shiftInitialLayerType_Y = False

    # TODO: find better name? redundant with X/Yoffset and X/Ymin/max, no?
    #self.additionalRodLength = 0

    # TODO: create setSize functions?
    self.Xmin = -5.5
    self.Xmax = 5.5
    self.Ymin = -5.5
    self.Ymax = 5.5
    
    # additional separate offsets for X and Y layers...
    self.Xoffset = 0
    self.Yoffset = 0

  def setRodType():
    return

  def setRodWidth():
    ''' set rod width (WARNING: will set LineNumber and LineDistance accordingly) '''
    return
  def setRodHeight():
    ''' set rod height (WARNING: will set LineNumber and LineDistance accordingly) '''
    return

  def setLineNumberAndDistance_XY():
    ''' set LineNumber and LineDistance (WARNING: will set rod width accordingly) '''
    return
  def setLineNumberAndDistance_Z():
    ''' set LineNumber and LineDistance (WARNING: will set rod height accordingly) '''
    return

  def setVoxelSize3():
    return

  def setOverlap3():
    #self.overlap = 
    return

  def adaptXYMinMax(self):
    
    # TODO: should take into account the width of logs, etc
    if self.isSymmetrical:
      #LX = self.NRodsPerLayer_X*self.interRodDistance + 2*self.additionalRodLength
      #LY = self.NRodsPerLayer_Y*self.interRodDistance + 2*self.additionalRodLength
      LX = self.NRodsPerLayer_X*self.interRodDistance
      LY = self.NRodsPerLayer_Y*self.interRodDistance
    else:
      #LX = self.NRodsPerLayer_X*self.interRodDistance - 0.5*self.interRodDistance + 2*self.additionalRodLength
      #LY = self.NRodsPerLayer_Y*self.interRodDistance - 0.5*self.interRodDistance + 2*self.additionalRodLength
      LX = self.NRodsPerLayer_X*self.interRodDistance - 0.5*self.interRodDistance
      LY = self.NRodsPerLayer_Y*self.interRodDistance - 0.5*self.interRodDistance
      
    self.Xmin = -0.5*LX
    self.Xmax = 0.5*LX
    self.Ymin = -0.5*LY
    self.Ymax = 0.5*LY

  def getGWLandBFDTDobjects(self):
    GWL_obj = GWLobject()
    BFDTD_obj = BFDTDobject()
    
    layer_type_X = self.shiftInitialLayerType_X
    layer_type_Y = self.shiftInitialLayerType_Y

    if self.BottomToTop:
      layer_idx_list = range(self.Nlayers_Z)
    else:
      layer_idx_list = range(self.Nlayers_Z-1,-1,-1)

    for layer_idx in layer_idx_list:
      direction = layer_idx % 2 + self.bottomLayerYPeriodic % 2
      
      # TODO: reduce code duplication here between lines in X and lines in Y direction.
      if direction % 2 == 0: # lines in the Y direction
        
        if self.isSymmetrical:
          N = self.NRodsPerLayer_X + (layer_type_X+1)%2
        else:
          N = self.NRodsPerLayer_X
        
        # NOTE: some leftover from fitting the nanoscribe-style woodpile? Add option for it...? :/
        #for rod_idx in range(N-1,-1,-1):
        for rod_idx in range(N):
          X = self.Xmin + self.Xoffset + layer_type_X*0.5*self.interRodDistance + rod_idx*self.interRodDistance
          P1 = self.offset + numpy.array([X, self.Ymax, layer_idx*self.interLayerDistance])
          P2 = self.offset + numpy.array([X, self.Ymin, layer_idx*self.interLayerDistance])
          if self.rod_type == 'line':
            GWL_obj.addLine(P1,P2)
          elif self.rod_type == 'blockContinuous':
            obj = GWL.tilted_grating.Parallelepiped()
            obj.e1_vec3 = [0,1,0]
            obj.e2_vec3 = [1,0,0]
            if self.BottomToTop:
              obj.e3_vec3 = [0,0,1]
            else:
              obj.e3_vec3 = [0,0,-1]
            width = self.LineNumber_X*self.LineDistance_X
            height = self.LineNumber_Z*self.LineDistance_Z
            obj.voxelsize_vec3 = numpy.array([self.LineDistance_X,self.LineDistance_Y,self.LineDistance_Z])
            obj.size_vec3 = [abs(P2[1]-P1[1])+obj.voxelsize_vec3[0],width,height]
            obj.overlap_vec3 = numpy.array([0,0,0])
            obj.center_vec3 = 0.5*(P1+P2)
            obj.computePoints()
            GWL_obj.addGWLobject(obj)
          else:
            GWL_obj.addYblock(P1, P2, self.LineNumber_X, self.LineDistance_X, self.LineNumber_Z, self.LineDistance_Z, self.BottomToTop)
          block = bfdtd.Block()
          block.setLowerAbsolute( P1 - 0.5*self.rod_width*numpy.array([1,0,0]) - 0.5*self.rod_height*numpy.array([0,0,1]) )
          block.setUpperAbsolute( P2 + 0.5*self.rod_width*numpy.array([1,0,0]) + 0.5*self.rod_height*numpy.array([0,0,1]) )
          block.setName("woodpile")
          BFDTD_obj.geometry_object_list.append(block)
        layer_type_X = (layer_type_X + 1) % 2
        
      else: # lines in the X direction
        
        if self.isSymmetrical:
          N = self.NRodsPerLayer_Y + (layer_type_Y+1)%2
        else:
          N = self.NRodsPerLayer_Y
          
        for rod_idx in range(N):
          Y = self.Ymin + self.Yoffset + layer_type_Y*0.5*self.interRodDistance + rod_idx*self.interRodDistance
          P1 = self.offset + numpy.array([self.Xmin, Y, layer_idx*self.interLayerDistance])
          P2 = self.offset + numpy.array([self.Xmax, Y, layer_idx*self.interLayerDistance])
          if self.rod_type == 'line':
            GWL_obj.addLine(P1,P2)
          # TODO: This is a quick hack at the moment. A lot of stuff needs to be rewritten to make things nicer.
          elif self.rod_type == 'blockContinuous':
            obj = GWL.tilted_grating.Parallelepiped()
            obj.e1_vec3 = [1,0,0]
            obj.e2_vec3 = [0,1,0]
            if self.BottomToTop:
              obj.e3_vec3 = [0,0,1]
            else:
              obj.e3_vec3 = [0,0,-1]
            width = self.LineNumber_Y*self.LineDistance_Y
            height = self.LineNumber_Z*self.LineDistance_Z
            obj.voxelsize_vec3 = numpy.array([self.LineDistance_X,self.LineDistance_Y,self.LineDistance_Z])
            obj.size_vec3 = [abs(P2[0]-P1[0])+obj.voxelsize_vec3[0],width,height]
            obj.overlap_vec3 = numpy.array([0,0,0])
            obj.center_vec3 = 0.5*(P1+P2)
            obj.computePoints()
            GWL_obj.addGWLobject(obj)
          else:
            GWL_obj.addXblock(P1, P2, self.LineNumber_Y, self.LineDistance_Y, self.LineNumber_Z, self.LineDistance_Z, self.BottomToTop)
          block = bfdtd.Block()
          block.setLowerAbsolute( P1 - 0.5*self.rod_width*numpy.array([0,1,0]) - 0.5*self.rod_height*numpy.array([0,0,1]) )
          block.setUpperAbsolute( P2 + 0.5*self.rod_width*numpy.array([0,1,0]) + 0.5*self.rod_height*numpy.array([0,0,1]) )
          block.setName("woodpile")
          BFDTD_obj.geometry_object_list.append(block)
        layer_type_Y = (layer_type_Y + 1) % 2
        
      # optional: just add another write to easily distinguish layers inside file
      # TODO: Replace with comment. Requires addition of some addComment() command.
      GWL_obj.startNewVoxelSequence()
    return (GWL_obj, BFDTD_obj)

  def write_GWL(self, filename):
    raise('Deprecated: Use writeGWL() instead.')
    return

  def write_BFDTD(self, filename):
    raise('Deprecated: Use writeBFDTD() instead.')
    return

  def writeGWL(self, filename):
    (GWL_obj, BFDTD_obj) = self.getGWLandBFDTDobjects()
    (Pmin, Pmax) = GWL_obj.getLimits()
    GWL_obj.writeGWL(filename, writingOffset = [0,0,-Pmin[2],0] ) # write object so that Zmin = 0
    
  def writeBFDTD(self, filename):
    # TODO: finish implementing this function
    (GWL_obj, BFDTD_obj) = self.getGWLandBFDTDobjects()
    print('Writing GWL to '+filename)
    BFDTD_obj.writeGeoFile(filename)

def main():
  woodpile_obj = Woodpile()
  woodpile_obj.rod_width = 0.2
  woodpile_obj.rod_height = 1
  woodpile_obj.interLayerDistance = 1
  woodpile_obj.interRodDistance = 2

  woodpile_obj.LineNumber_X = 2
  woodpile_obj.LineDistance_X = 0.050
  woodpile_obj.LineNumber_Y = 2
  woodpile_obj.LineDistance_Y = 0.050
  woodpile_obj.LineNumber_Z = 2
  woodpile_obj.LineDistance_Z = 0.100

  woodpile_obj.rod_type='block'
  woodpile_obj.adaptXYMinMax()
  woodpile_obj.writeGWL('woodpile_test.gwl')
  woodpile_obj.writeBFDTD('woodpile_test.geo')
  
if __name__ == "__main__":
  main()
