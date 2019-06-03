#!/usr/bin/env python3

from GWL.GWL_parser import *

def func1():
  P1=[1,1,1]
  P2=[0,0,2]
  power=-1
  inner_radius=0
  outer_radius=0
  PointDistance_r=0.1
  PointDistance_theta=0.1

  print(('P1=',P1))
  print(('P2=',P2))

  # prepare some variables
  v = numpy.array(P2)-numpy.array(P1) # vector to rotate
  print(('v=',v))
  centro = 0.5*(numpy.array(P2)+numpy.array(P1)) # center of LineCylinder
  print(('centro=',centro))
  u = numpy.array([0,0,1]) # direction of standard TubeWithVerticalLines
  print(('u=',u))

  theta = Angle(u,v) # angle by which to rotate
  print(('theta=',theta))

  rotation_axis = numpy.cross(u,v) # axis around which to rotate
  print(('rotation_axis=',rotation_axis))

  height = numpy.linalg.norm(v)
  print(('height=',height))

  # build a basis from the P1-P2 direction
  k = v
  i = Orthogonal(k)
  j = numpy.cross(k,i)

  print(('i=',i))
  print(('j=',j))
  print(('k=',k))

  i = i/numpy.linalg.norm(i)
  j = j/numpy.linalg.norm(j)
  k = k/numpy.linalg.norm(k)

  print(('i=',i))
  print(('j=',j))
  print(('k=',k))

  # transformation matrix from (x,y,z) into (i,j,k)
  P = numpy.transpose(numpy.matrix([i,j,k]))
  print(P)
  print(P.T)
  print(P*P.T)

  # create a vertical tube and rotate it
  tube = GWLobject()
  origin = [0,0,0]
  tube.addTubeWithVerticalLines(origin, inner_radius, outer_radius, height, power, PointDistance_r, PointDistance_theta, downwardWriting=False)
  print(('tube.GWL_voxels=',tube.GWL_voxels))
  tube.write_GWL('test.gwl')

  print(P)
  print(('centro=',centro))
  tube.applyTransformationMatrix(P, centro)
  print(('tube.GWL_voxels=',tube.GWL_voxels))

def func2():
  obj=GWLobject();
  obj.addLineCylinder(P1=[1,1,1], P2=[0,0,2], power=-1, inner_radius=0.05, outer_radius=0.1, PointDistance_r=0.01, PointDistance_theta=0.01)
  obj.write_GWL('test.gwl')

if __name__ == "__main__":
  func2()
