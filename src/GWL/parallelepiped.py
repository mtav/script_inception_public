#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import numpy
import tempfile
from numpy.linalg import norm
from numpy import sqrt, cross, array, dot
from GWL.GWL_parser import GWLobject, calculateNvoxelsAndInterVoxelDistance

class Parallelepiped(GWLobject):
  '''
  A parallelepiped (i.e., a brick, possibly with non-orthogonal axes).

  The block will be filled with lines going along e1, in layers in the (e1,e2) plane, stacked along e3.

  .. todo:: Document code.
  .. todo:: center -> centro...
  .. todo:: think up better system for LineNumber, LineDistance, Overlap, VoxelSize, Length. Example:
  
            * set(Length, LineNumber)
            * set(LineDistance, LineNumber)
            * set(Length, VoxelSize, Overlap)
  
  .. todo:: Finish implementing LineDistance, Overlap in Blender addon somehow. cf design problem above.
  .. todo:: Finish implementing start-end point method in Blender addon somehow.
  
  .. todo:: extend Parallelepiped class:
  
            * distorted cube, including triangular ones (interpolate cubic grid onto distorted and then write various paras accordingly) (cf blender's lattice deform algorithm with linear interpolation)
            * use known/given voxelsize intelligently based on direction of lines, etc
            * power compensation -> period/linedistance compensation based on known/given voxelsize evolution (extend to other objects?)
  '''
  
  ### attributes:
  center_vec3 = numpy.array([0,0,0]) # Center point of the object. No default value.
  size_vec3 = numpy.array([1,1,1]) # The lengths of the block edges along each of its three axes. Not really a 3-vector (at least, not in the lattice basis), but it has three components, each of which should be nonzero. No default value.

  # The directions of the axes of the block; the lengths of these vectors are ignored. Must be linearly independent. They default to the three lattice directions.
  # The block will be filled with lines going along e1, in layers in the (e1,e2) plane, stacked along e3.
  e1_vec3 = numpy.array([1,0,0])
  e2_vec3 = numpy.array([0,1,0])
  e3_vec3 = numpy.array([0,0,1])

  LineNumber_vec3 = [5,5,5]

  # WARNING: voxelsize and overlap in this class relate to e1,e2,e3 which are chosen by the user, not the usual x,y,z!!!
  # TODO: Rename those variables to reflect the dependency on e1,e2,e3 instead of x,y,z. Or create smarter system.
  voxelsize_vec3 = numpy.array([0.150,0.150,0.450])
  
  # should the lines all be connected or not
  connected = False
  # TODO: enable/disable zigzag as well... Towards a single "block/quad" class...
  
  ###################################
  # to be discarded and replaced by internal or external parameter calculating functions
  overlap_vec3 = numpy.array([0,0,0.5])
  voxelsize_vec3_xyz = numpy.array([0.150,0.150,0.450])
  overlap_vec3_xyz = numpy.array([0,0,0.5])
  ###################################
  
  def __init__(self):
    GWLobject.__init__(self)

  def getNormalizedVectors(self):
    self.e1_vec3 = numpy.array(self.e1_vec3)
    self.e2_vec3 = numpy.array(self.e2_vec3)
    self.e3_vec3 = numpy.array(self.e3_vec3)
    e1_vec3_norm = self.e1_vec3/norm(self.e1_vec3)
    e2_vec3_norm = self.e2_vec3/norm(self.e2_vec3)
    e3_vec3_norm = self.e3_vec3/norm(self.e3_vec3)
    
    return (e1_vec3_norm, e2_vec3_norm, e3_vec3_norm)
  
  def setSizeFromVectors(self):
    self.e1_vec3 = numpy.array(self.e1_vec3)
    self.e2_vec3 = numpy.array(self.e2_vec3)
    self.e3_vec3 = numpy.array(self.e3_vec3)
    self.size_vec3 = numpy.array( [norm(self.e1_vec3), norm(self.e2_vec3), norm(self.e3_vec3)] )
    return 

  def setFromLine(self, A, B, rod_width, rod_height, orthogonal, orientation):

    A = array(A)
    B = array(B)
    self.center_vec3 = 0.5*(A+B)
    
    size = [norm(B-A), rod_width, rod_height]
    self.size_vec3 = numpy.array([size[orientation[0]], size[orientation[1]], size[orientation[2]]])
    self.voxelsize_vec3 = numpy.array([self.voxelsize_vec3_xyz[orientation[0]], self.voxelsize_vec3_xyz[orientation[1]], self.voxelsize_vec3_xyz[orientation[2]]])
    self.overlap_vec3 = numpy.array([self.overlap_vec3_xyz[orientation[0]], self.overlap_vec3_xyz[orientation[1]], self.overlap_vec3_xyz[orientation[2]]])

    #self.size_vec3 = [norm(B-A), rod_width, rod_height]
    
    x = array([1,0,0])
    y = array([0,1,0])
    z = array([0,0,1])
    
    if norm(B-A)==0:
      e1 = x
      e2 = y
      e3 = z
    else:
      e1 = B-A
      if norm(cross(z,e1)) == 0:
        e1 = dot(e1,z)*z
        e3 = y # choice based on nanoscribe InvertZAxis system
        e2 = cross(e3,e1)
      else:
        e2 = cross(z,e1)
        if orthogonal:
          #print('orthogonal')
          e3 = cross(e1,e2)
        else:
          #print('non-orthogonal')
          e3 = z


    elist = [e1,e2,e3]
    self.e1_vec3 = elist[orientation[0]]
    self.e2_vec3 = elist[orientation[1]]
    self.e3_vec3 = elist[orientation[2]]
    
    return

  def getMinMaxPoints(self):
    (e1_vec3_norm, e2_vec3_norm, e3_vec3_norm) = self.getNormalizedVectors()
    
    e1min = self.center_vec3 - self.size_vec3[0]*e1_vec3_norm
    e1max = self.center_vec3 + self.size_vec3[0]*e1_vec3_norm

    e2min = self.center_vec3 - self.size_vec3[1]*e2_vec3_norm
    e2max = self.center_vec3 + self.size_vec3[1]*e2_vec3_norm

    e3min = self.center_vec3 - self.size_vec3[2]*e3_vec3_norm
    e3max = self.center_vec3 + self.size_vec3[2]*e3_vec3_norm
    
    return (e1min, e1max, e2min, e2max, e3min, e3max)

  def computeVectors(self):
    # TODO
    
    (e1min, e1max, e2min, e2max, e3min, e3max) = self.getMinMaxPoints()
        
    self.addLine()
    self.addLine()
    self.addLine()
    return

  def computeOutline(self):
    # TODO
    self.addLine()
    self.addLine()
    self.addLine()
    self.addLine()

    self.addLine()
    self.addLine()
    self.addLine()
    self.addLine()

    self.addLine()
    self.addLine()
    self.addLine()
    self.addLine()
    return
    
  def computePoints(self):
    self.clear()

    #self.e1_vec3 = numpy.array(self.e1_vec3)
    #self.e2_vec3 = numpy.array(self.e2_vec3)
    #self.e3_vec3 = numpy.array(self.e3_vec3)
    #e1_vec3_norm = self.e1_vec3/numpy.linalg.norm(self.e1_vec3)
    #e2_vec3_norm = self.e2_vec3/numpy.linalg.norm(self.e2_vec3)
    #e3_vec3_norm = self.e3_vec3/numpy.linalg.norm(self.e3_vec3)
    
    (e1_vec3_norm, e2_vec3_norm, e3_vec3_norm) = self.getNormalizedVectors()

    self.center_vec3 = numpy.array(self.center_vec3)

    #(LineNumber_e2, LineDistance_e2) = calculateNvoxelsAndInterVoxelDistance(Length=self.size_vec3[1], Voxelsize=self.voxelsize_vec3[1], Overlap=self.overlap_vec3[1])
    #(LineNumber_e3, LineDistance_e3) = calculateNvoxelsAndInterVoxelDistance(Length=self.size_vec3[2], Voxelsize=self.voxelsize_vec3[2], Overlap=self.overlap_vec3[2])

    LineNumber_e1 = self.LineNumber_vec3[0]
    LineNumber_e2 = self.LineNumber_vec3[1]
    LineNumber_e3 = self.LineNumber_vec3[2]

    e2_list = []
    L = self.size_vec3[1] #(LineNumber_e2-1)*LineDistance_e2
    if LineNumber_e2 > 1:
      e2_list = numpy.linspace(-0.5*L, 0.5*L, LineNumber_e2)
    else:
      e2_list = [0]

    e3_list = []
    L = self.size_vec3[2] #(LineNumber_e3-1)*LineDistance_e3
    if LineNumber_e3 > 1:
      e3_list = numpy.linspace(-0.5*L, 0.5*L, LineNumber_e3)
    else:
      e3_list = [0]

    #print(e2_list)
    #print(e3_list)

    pointList = []
    counter = 0
    counter_e2 = 0

    for e3_factor in e3_list:
      for e2_idx in range(len(e2_list)):

        if counter_e2%2 == 0:
          e2_factor = e2_list[e2_idx]
        else:
          e2_factor = e2_list[-e2_idx-1]

        #print(self.center_vec3)
        #print(self.size_vec3[0])
        #print(self.voxelsize_vec3[0])
        #print((-0.5*(self.size_vec3[0]-self.voxelsize_vec3[0])))
        #print(e1_vec3_norm)
        #print(e2_vec3_norm)
        #print(e3_vec3_norm)

        #print(e2_factor)
        #print(e3_factor)

        #A = self.center_vec3 + (-0.5*(self.size_vec3[0]-self.voxelsize_vec3[0]))*e1_vec3_norm + e2_factor*e2_vec3_norm + e3_factor*e3_vec3_norm
        #B = self.center_vec3 + (0.5*(self.size_vec3[0]-self.voxelsize_vec3[0]))*e1_vec3_norm + e2_factor*e2_vec3_norm + e3_factor*e3_vec3_norm
        A = self.center_vec3 + (-0.5*self.size_vec3[0])*e1_vec3_norm + e2_factor*e2_vec3_norm + e3_factor*e3_vec3_norm
        B = self.center_vec3 + (0.5*self.size_vec3[0])*e1_vec3_norm + e2_factor*e2_vec3_norm + e3_factor*e3_vec3_norm
        #print(A)
        #print(B)
        if counter%2 == 0:
          pointList.append(A)
          pointList.append(B)
          if not self.connected:
            self.GWL_voxels.append(pointList)
            pointList = []
        else:
          pointList.append(B)
          pointList.append(A)
          if not self.connected:
            self.GWL_voxels.append(pointList)
            pointList = []
            
        counter += 1

      counter_e2 += 1

    if self.connected:
      self.GWL_voxels.append(pointList)

  def writeGWL(self, filename, writingOffset = [0,0,0,0]):
    self.computePoints()
    GWLobject.writeGWL(self, filename, writingOffset)
    return
    
  def getMeshData(self):
    self.computePoints()
    return(GWLobject.getMeshData(self))

def test0():
  foo = Parallelepiped()
  print(foo.getMeshData())
  return

def test1():
  A = [0,0,0]
  B = [10,0,0]
  orthogonal = False

  para = Parallelepiped()
  para.LineNumber_vec3 = [3,4,5]
  #para.voxelsize_vec3 = [0.1,0.1,0.1]
  #para.overlap_vec3 = [0,0,0]

  para.setFromLine(A, B,2,3,orthogonal,[0,1,2])
  para.computePoints()
  para.writeGWL(tempfile.gettempdir()+os.sep+'Parallelepiped_012.gwl')

  para.setFromLine(A, B,2,3,orthogonal,[1,2,0])
  para.computePoints()
  para.writeGWL(tempfile.gettempdir()+os.sep+'Parallelepiped_120.gwl')

  para.setFromLine(A, B,2,3,orthogonal,[2,0,1])
  para.computePoints()
  para.writeGWL(tempfile.gettempdir()+os.sep+'Parallelepiped_201.gwl')

  para.setFromLine(A, B,2,3,orthogonal,[0,2,1])
  para.computePoints()
  para.writeGWL(tempfile.gettempdir()+os.sep+'Parallelepiped_021.gwl')

  para.setFromLine(A, B,2,3,orthogonal,[2,1,0])
  para.computePoints()
  para.writeGWL(tempfile.gettempdir()+os.sep+'Parallelepiped_210.gwl')

  para.setFromLine(A, B,2,3,orthogonal,[1,0,2])
  para.computePoints()
  para.writeGWL(tempfile.gettempdir()+os.sep+'Parallelepiped_102.gwl')

  return

if __name__ == "__main__":
  test0()
  test1()
