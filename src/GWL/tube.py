#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import numpy
from numpy import array, radians, cos, sin, linspace, sqrt, ceil
from GWL.GWL_parser import GWLobject, calculateNvoxelsAndInterVoxelDistance
#import bpy
#import blender_scripts.blender_utilities as blender_utilities

## different ways of writing tubes:
#-horizontal circles
#-vertical lines
#-spirals
#-constant angular step or constant distance between points...
#-other still unknown way of doing it -> a function should be passed as arg

## example suppressor function
#(a,b) = suppressor(A,B)
#a=b=None if not allowed
#a=A,b=B if both allowed
#a=intersection point or b=intersection point if it's the case

## "boolean operations":
#-linear cutoffs: xmin,xmax,ymin,ymax
#-angular cutoff: thetamin,thetamax
#-other arbitrary supression of points -> a function should be passed as arg

## geometric vs writing parameters:
#-height, radius, centro, etc -> same no matter what writing method
#-steps, distance between points, etc -> change depending on writing method

## fundamental formulas
# Npts = Nsteps + 1
# E2E_size = C2C_size + voxelsize
# overlap = max(1-step/voxelsize, 0)
# C2C_size = end - start = Nsteps*step

## derived formulas
# C2C_size = E2E_size - voxelsize = end - start = Nsteps*step
# E2E_size = (Npts-1)*step + voxelsize

## calculation parameters:
#-voxel size
#-overlap
#-min/max overlap, etc

#class tube -> geometry params
  #def setWriter(spiralwriter)
#class spiralwriter -> writing params

## TODO: boolean operations on meshes without faces, only edges (GWL files), either as blender script/modifier or as an external function applicable to any GWLobject (and similar like FIB)
# -> so no point in implementing it inside tube and similar now

# Papa class:
class TubePapa(GWLobject):
  def __init__(self):    
    GWLobject.__init__(self)

  def computePoints(self):
    self.clear()
    write_sequence = []
    write_sequence.append([0,0,0])
    write_sequence.append([1,0,0])
    write_sequence.append([2,1,0])
    self.GWL_voxels.append(write_sequence)
    write_sequence = []
    write_sequence.append([0,0,1])
    write_sequence.append([1,0,1])
    write_sequence.append([2,1,1])
    self.GWL_voxels.append(write_sequence)
    
  def writeGWL(self, filename, writingOffset = [0,0,0,0]):
    print('TubePapa.writeGWL')
    self.computePoints()
    GWLobject.writeGWL(self, filename, writingOffset)
    return
  
  def getMeshData(self, position = [0,0,0]):
    self.computePoints()
    return(GWLobject.getMeshData(self, position))

def suppressorFunction_Xmax(A, B, Xmin):
  pointList = []
  
  if Xmin<A[0]:
    if Xmin<B[0]:
      pointList = [A,B]
      connectLeft = True
      connectRight = True
    else:
      pointList = [A,B]
      connectLeft = True
      connectRight = False
  else:
    if Xmin<B[0]:
      pointList = [A,B]
      connectLeft = True
      connectRight = True
    else:
      pointList = []
      connectLeft = False
      connectRight = False
  
  return pointList, connectLeft, connectRight

class HorizontalCircleTubeWithConstantAngularStep(GWLobject):
  def __init__(self):
    
    self.NumberOfSteps_R = 2
    self.NumberOfSteps_Theta = 9
    self.NumberOfSteps_Z = 2

    self.StepSize_R = 50/cos(radians(22.5))
    self.StepSize_ThetaDegrees = 45
    self.StepSize_Z = 40

    self.Start_R = 100/cos(radians(22.5))
    self.Start_ThetaDegrees = 22.5
    self.Start_Z = -20
    
    self.centro = array([0,0,60,0]) # we are always in a 4D space...
    
    self.powerFunction = lambda x, y, z: -1
    self.suppressorFunction = lambda A, B: (A,B)
    
    #self.inner_radius = 1
    #self.outer_radius = 2
    #self.height = 1
    #self.power = -1
    #self.PointDistance_r = 0.1
    #self.PointDistance_theta = 0.1 
    #self.PointDistance_z = 0.1
    #self.downwardWriting = True
    return

  def setCentro(self, vec3or4):
    if len(vec3or4)>=4:
      self.centro = array([vec3or4[0],vec3or4[1],vec3or4[2],vec3or4[3]])
    else:
      self.centro = array([vec3or4[0],vec3or4[1],vec3or4[2],0])
    return
  
  def setNumberOfSteps_R(self, NumberOfSteps_R):
    self.NumberOfSteps_R = int(NumberOfSteps_R)
    return
  def setNumberOfSteps_Theta(self, NumberOfSteps_Theta):
    self.NumberOfSteps_Theta = int(NumberOfSteps_Theta)
    return
  def setNumberOfSteps_Z(self, NumberOfSteps_Z):
    self.NumberOfSteps_Z = int(NumberOfSteps_Z)
    return

  def setStepSize_R(self, StepSize_R):
    self.StepSize_R = StepSize_R
    return
  def setStepSize_ThetaDegrees(self, StepSize_ThetaDegrees):
    self.StepSize_ThetaDegrees = StepSize_ThetaDegrees
    return
  def setStepSize_Z(self, StepSize_Z):
    self.StepSize_Z = StepSize_Z
    return

  def setStart_R(self, Start_R):
    self.Start_R = Start_R
    return
  def setStart_ThetaDegrees(self, Start_ThetaDegrees):
    self.Start_ThetaDegrees = Start_ThetaDegrees
    return
  def setStart_Z(self, Start_Z):
    self.Start_Z = Start_Z
    return
  
  def computePoints(self):
    
    #print("I'm in.")

    self.clear()
    for Z_idx in range(self.NumberOfSteps_Z):
      Z = self.Start_Z + Z_idx * self.StepSize_Z
      for R_idx in range(self.NumberOfSteps_R):
        write_sequence = []
        lastpoint = None
        R = self.Start_R + R_idx * self.StepSize_R
        for Theta_idx in range(self.NumberOfSteps_Theta):
          ThetaDegrees = self.Start_ThetaDegrees + Theta_idx * self.StepSize_ThetaDegrees
          ThetaRadians = radians(ThetaDegrees)
          P = self.centro + array([R*cos(ThetaRadians), R*sin(ThetaRadians), Z, self.powerFunction(R, ThetaRadians, Z)])
          #print(P)
          #pointlist = self.suppressorFunction(lastpoint, P)
          lastpoint = P
          write_sequence.append(P)
        self.GWL_voxels.append(write_sequence)
    
    #self.addTube(self.centro, self.inner_radius, self.outer_radius, self.height, -1, self.PointDistance_r, self.PointDistance_theta, self.PointDistance_z, self.downwardWriting)
  
  #def addTube(self, centro, inner_radius, outer_radius, height, power, PointDistance_r, PointDistance_theta, PointDistance_z, downwardWriting=True):
    
    ##print('=== addTube ===')
    ##print((numpy.linspace(inner_radius, outer_radius, float((outer_radius - inner_radius)/PointDistance_r))))
    #for radius in numpy.linspace(self.inner_radius, self.outer_radius, float(1+(self.outer_radius - self.inner_radius)/self.PointDistance_r)):
      #zrange = numpy.linspace(self.centro[2]+0.5*self.height, self.centro[2]-0.5*self.height, float(1+self.height/self.PointDistance_z))
      #if not self.downwardWriting:
        #zrange = reversed(zrange)
      #for z in zrange:
        ##print((radius,z))
      ##for i_theta in numpy.linspace(0, 2*numpy.pi, (outer_radius - inner_radius)/PointDistance_r):
        #self.addHorizontalCircle([self.centro[0],self.centro[1],z], radius, self.power, self.PointDistance_theta, closed_loop=self.closed_loop)
    return


  
  def getMeshData(self, position = [0,0,0]):
    self.computePoints()
    return(GWLobject.getMeshData(self, position))


# tube class
class Tube(GWLobject):
  ''' This class allows you to create "tubes", i.e. cylinders with an optional inner radius.
  
  There are three writing methods available:
  
  * horizontal disks
  * vertical lines
  * spirals (with or without additional flat disks on top and bottom)

  .. todo:: Finish documenting...
  .. todo:: rotated tube... (part of the parent todo: general location+rotation system for GWL objects and BFDTD objects)
  '''
  def __init__(self):
    self.centro = [0,0,0]
    self.inner_radius = 1
    self.outer_radius = 2
    self.height = 3
    self.method = 'circles'
    
    self.PointDistance_r = 0.150
    self.PointDistance_theta = 0.150
    self.PointDistance_z = 2.7*0.150
    
    self.downwardWriting = True
    self.zigzag = True
    
    self.rotateSpirals = False
    self.add_flat_ends = True
    self.closed_loop = False
    
    self.power = -1
    
    GWLobject.__init__(self)
    return

  def setCentro(self, vec3):
    self.centro = array(vec3)
    return

  def setHeight(self, height):
    self.height = height
    return
  def setInnerRadius(self, inner_radius):
    # TODO
    return
  def setOuterRadius(self, outer_radius):
    self.outer_radius = outer_radius
    return
  def setAngularStepDegrees(self,x):
    # TODO
    return

  def setNumberOfSteps_R(self,x):
    # TODO
    return
  def setNumberOfSteps_Theta(self,x):
    # TODO
    return
  def setNumberOfSteps_Z(self,x):
    # TODO
    return

  def setStepSize_R(self,x):
    # TODO
    return
  def setStepSize_ThetaDegrees(self,x):
    # TODO
    return
  def setStepSize_Z(self,x):
    # TODO
    return

  def setStart_R(self,x):
    # TODO
    return
  def setStart_ThetaDegrees(self,x):
    # TODO
    return
  def setStart_Z(self,x):
    # TODO
    return

  #def setNlinesVertical(self):
    #Zlist = 
    #self.NlinesVertical = float(1+self.height/self.PointDistance_z)
    #return

  def addTube(self):
    for radius in linspace(self.inner_radius, self.outer_radius, float(1+(self.outer_radius - self.inner_radius)/self.PointDistance_r)):
      zrange = linspace(self.centro[2]+0.5*self.height, self.centro[2]-0.5*self.height, ceil(1+self.height/self.PointDistance_z))
      if not self.downwardWriting:
        zrange = reversed(zrange)
      for z in zrange:
        self.addHorizontalCircle([self.centro[0],self.centro[1],z], radius, self.power, self.PointDistance_theta, closed_loop=self.closed_loop)
    return

  # TODO: Improve/standardize voxelsize/overlap/step system, etc
  # TODO: Fix location of non-spiral tubes (they don't seem to get correctly centered on location in Blender addon)
  def computePoints(self):
    
    self.clear()
    
    ### spiral method
    if self.method == 'spiral':
      
      ### number of spirals/circles
      N_radius = int(1+(self.outer_radius - self.inner_radius)/self.PointDistance_r)
      
      ### Add first flat end
      if self.add_flat_ends:
        if self.downwardWriting:
          z = self.centro[2]+0.5*self.height
        else:
          z = self.centro[2]-0.5*self.height
        for radius in linspace(self.inner_radius, self.outer_radius, float(1+(self.outer_radius - self.inner_radius)/self.PointDistance_r)):
          self.addHorizontalCircle([self.centro[0], self.centro[1], z], radius, self.power, self.PointDistance_theta, closed_loop=self.closed_loop)

      ### Add spirals
      #for radius in numpy.linspace(self.inner_radius, self.outer_radius, float(1+(self.outer_radius - self.inner_radius)/self.PointDistance_r)):
      for radius_idx in range(N_radius):
        
        # radius of current spiral
        radius = self.inner_radius + radius_idx * self.PointDistance_r
        
        # set starting angle of current spiral
        if self.rotateSpirals:
          theta0 = radius_idx * 2*numpy.pi/N_radius
        else:
          theta0 = 0
        
        # set theta step
        step_theta = self.PointDistance_theta/radius
        
        # total number of points for the current spiral
        N_theta = int((2*numpy.pi*self.height)/(self.PointDistance_z*step_theta))

        # upwards/downwards writing handling
        if not self.downwardWriting:
          theta_idx_range = range(N_theta)
        else:
          theta_idx_range = reversed(range(N_theta))
        
        write_sequence = []
        for theta_idx in theta_idx_range:
          theta = theta_idx*step_theta
          x = radius*numpy.cos(theta0 + theta)
          y = radius*numpy.sin(theta0 + theta)
          z = -0.5*self.height + self.PointDistance_z*theta/(2*numpy.pi)
          write_sequence.append([x,y,z])
        
        self.GWL_voxels.append(write_sequence)
      
      ### Add second flat end
      if self.add_flat_ends:
        if self.downwardWriting:
          z = self.centro[2]-0.5*self.height
        else:
          z = self.centro[2]+0.5*self.height
        for radius in linspace(self.inner_radius, self.outer_radius, float(1+(self.outer_radius - self.inner_radius)/self.PointDistance_r)):
          self.addHorizontalCircle([self.centro[0], self.centro[1], z], radius, self.power, self.PointDistance_theta, closed_loop=self.closed_loop)

    ### vertical lines method
    elif self.method == 'vertical lines':
      self.addTubeWithVerticalLines(self.centro, self.inner_radius, self.outer_radius, self.height, -1, self.PointDistance_r, self.PointDistance_theta, self.downwardWriting, self.zigzag)

    ### horizontal disk method
    else:
      self.addTube()

  def writeGWL(self, filename, writingOffset = [0,0,0,0]):
    self.computePoints()
    GWLobject.writeGWL(self, filename, writingOffset)
    return
  
  def getMeshData(self, position = [0,0,0]):
    self.computePoints()
    #print(self.GWL_voxels[0][0])
    return(GWLobject.getMeshData(self, position))

class TubeLarge(TubePapa):
  def __init__(self):
    TubePapa.__init__(self)
    self.centro = [0,0,0]
    self.radius = 10
    #self.fraction = 0.5
    #self.fractionLeft = 0.5
    #self.fractionRight = 0.5
    self.NlinesHorizontal = 10
    self.height = 5
    self.NlinesVertical = 5
    self.Xmin = -7.5
    self.Xmax = 5

  def computePoints(self):
    self.clear()
    
    #Xlist = linspace(self.radius, self.fraction*self.radius, self.NlinesHorizontal)
    Xlist = linspace( max(-self.radius,self.Xmin), min(self.Xmax,self.radius), self.NlinesHorizontal)
    Zlist = linspace(0.5*self.height, -0.5*self.height, self.NlinesVertical)
    
    write_sequence = []
    Xdir = 0
    Ydir = 0
    for Z in Zlist:
      if Xdir%2 == 0:
        XlistLocal = Xlist
      else:
        XlistLocal = reversed(Xlist)
      for X in XlistLocal:
        Mpos = array(self.centro) + array([X,sqrt(self.radius**2-X**2),Z])
        Mneg = array(self.centro) + array([X,-sqrt(self.radius**2-X**2),Z])
        if Ydir%2 == 0:
          write_sequence.extend([Mpos,Mneg])
        else:
          write_sequence.extend([Mneg,Mpos])
        self.GWL_voxels.append(write_sequence); write_sequence = []
        Ydir += 1
      Xdir += 1
    self.GWL_voxels.append(write_sequence)

class HalfTubeLargeWithInnerAndOuter(TubePapa):
  def __init__(self):
    TubePapa.__init__(self)
    self.centro = [0,0,0]
    self.inner_radius = 5
    self.outer_radius = 10
    self.NlinesHorizontal = 10
    self.height = 5
    self.NlinesVertical = 5
    #self.fraction = 0
    self.Xmin = -7.5
    self.Xmax = 5

  def computePoints(self):
    self.clear()
    
    #Xlist = linspace(self.outer_radius, self.fraction*self.outer_radius, self.NlinesHorizontal)
    Xlist = linspace( max(-self.outer_radius,self.Xmin), min(self.Xmax,self.outer_radius), self.NlinesHorizontal)
    Zlist = linspace(0.5*self.height, -0.5*self.height, self.NlinesVertical)
    
    write_sequence = []
    Xdir = 0
    Ydir = 0
    for Z in Zlist:
      if Xdir%2 == 0:
        XlistLocal = Xlist
      else:
        XlistLocal = reversed(Xlist)
      for X in XlistLocal:
        if abs(X) >= self.inner_radius:
          Mpos = array(self.centro) + array([X,sqrt(self.outer_radius**2-X**2),Z])
          Mneg = array(self.centro) + array([X,-sqrt(self.outer_radius**2-X**2),Z])
          if Ydir%2 == 0:
            write_sequence.extend([Mpos,Mneg])
          else:
            write_sequence.extend([Mneg,Mpos])
        else:
          Mpos_outer = array(self.centro) + array([X,sqrt(self.outer_radius**2-X**2),Z])
          Mpos_inner = array(self.centro) + array([X,sqrt(self.inner_radius**2-X**2),Z])
          Mneg_inner = array(self.centro) + array([X,-sqrt(self.inner_radius**2-X**2),Z])
          Mneg_outer = array(self.centro) + array([X,-sqrt(self.outer_radius**2-X**2),Z])
          if Ydir%2 == 0:
            write_sequence.extend([Mpos_outer,Mpos_inner])
            self.GWL_voxels.append(write_sequence); write_sequence = []
            write_sequence.extend([Mneg_inner,Mneg_outer])
          else:
            write_sequence.extend([Mneg_outer,Mneg_inner])
            self.GWL_voxels.append(write_sequence); write_sequence = []
            write_sequence.extend([Mpos_inner,Mpos_outer])
        self.GWL_voxels.append(write_sequence); write_sequence = []
        Ydir += 1
      Xdir += 1
    self.GWL_voxels.append(write_sequence)

class TruncatedTube(GWLobject):
  def __init__(self):
    GWLobject.__init__(self)
    
    self.centro = [0,0,0]
    self.inner_radius = 0.5
    self.outer_radius = 1
    self.height = 1

    self.z_step = 0.1
    self.theta_step_deg = 1
    self.r_step = 1

    self.truncationDistanceFromCentro = 0.7
    self.startAngle_deg = 0
    self.endAngle_deg = 360

    self.voxel_width = 0.100
    self.voxel_height = 0.200

    self.closed_loop = False

    return

  def writeGWL(self, filename, writingOffset = [0,0,0,0]):
    self.computePoints()
    GWLobject.writeGWL(self, filename, writingOffset)
    return

  def getMeshData(self, position = [0,0,0]):
    self.computePoints()
    #print(self.GWL_voxels[0][0])
    return(GWLobject.getMeshData(self, position))

  def computePoints(self):
    self.clear()

    log_width = self.outer_radius - self.inner_radius
    
    (LineNumber_R, LineDistance_R) = calculateNvoxelsAndInterVoxelDistance(Length=log_width, Voxelsize=self.voxel_width, Overlap=0)
    (LineNumber_theta, LineDistance_theta) = calculateNvoxelsAndInterVoxelDistance(Length=2*numpy.pi*self.outer_radius, Voxelsize=self.voxel_width, Overlap=0)
    (LineNumber_Z, LineDistance_Z) = calculateNvoxelsAndInterVoxelDistance(Length=self.height, Voxelsize=self.voxel_height, Overlap=6./7.)
    #print('LineNumber_Z='+str(LineNumber_Z))
    #print('LineDistance_Z='+str(LineDistance_Z))

    power = -1
    PointDistance_R = LineDistance_R
    PointDistance_theta = LineDistance_theta
    PointDistance_Z = LineDistance_Z

    for index_R in range(LineNumber_R):
      # calculate radius of current circle
      radius = 0.5*(self.inner_radius+self.outer_radius) - 0.5*((LineNumber_R-1)*PointDistance_R) + index_R*PointDistance_R
      if self.truncationDistanceFromCentro < radius:
        if abs(radius) > abs(self.truncationDistanceFromCentro):
          #startAngle = numpy.arccos(self.truncationDistanceFromCentro/radius)
          #endAngle = 2*numpy.pi-numpy.arccos(self.truncationDistanceFromCentro/radius)
          startAngle = -numpy.arccos(self.truncationDistanceFromCentro/radius)
          endAngle = numpy.arccos(self.truncationDistanceFromCentro/radius)
        else:
          startAngle = 0
          endAngle = 2*numpy.pi
        for index_Z in range(LineNumber_Z):
          zloc = self.centro[2]+0.5*((LineNumber_Z-1)*PointDistance_Z) - index_Z*PointDistance_Z
          self.addHorizontalCircle([self.centro[0],self.centro[1],zloc], radius, power, PointDistance_theta, startAngle, endAngle, closed_loop=self.closed_loop)

def testTruncatedTube():
  foo = TruncatedTube()
  foo.inner_radius = 0.5
  foo.outer_radius = 1.5
  foo.height = 2
  foo.truncationDistanceFromCentro = 1
  
  foo.centro = [0,0,0]
  v,e,f = foo.getMeshData()
  print(v[0])
  
  foo.centro = [1,0,0]
  v,e,f = foo.getMeshData()
  print(v[0])
  foo.writeGWL(sys.argv[1])

def testTube():
  foo = Tube()
  foo.inner_radius = 0.5
  foo.outer_radius = 0.5
  foo.height = 0
  
  foo.centro = [0,0,0]
  v,e,f = foo.getMeshData()
  print(v[0])
  
  foo.centro = [1,0,0]
  v,e,f = foo.getMeshData()
  print(v[0])
  foo.writeGWL(sys.argv[1])

def usage_example():
  #obj = Tube()
  #blender_utilities.addSimpleObject(obj.getMeshData, object_name='object', mesh_name='mesh', context=bpy.context)

  obj = Tube()
  #obj.centro = self.location # not passed, since blender already takes care of the relative mesh location
  obj.inner_radius = 0.5
  obj.outer_radius = 1
  obj.height = 1
  obj.method = 'spiral'
  obj.PointDistance_r = 0.1
  obj.PointDistance_theta = 0.1
  obj.PointDistance_z = 0.1
  obj.downwardWriting = True
  obj.zigzag = True
  obj.rotateSpirals = False
  obj.add_flat_ends = True
  obj.closed_loop = True

  obj.writeGWL(sys.argv[1]+os.sep+'tmp.gwl')
  print('DONE')

if __name__ == "__main__":
  usage_example()
