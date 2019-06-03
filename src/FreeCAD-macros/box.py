'''
Extra functions to simplify block creation.
'''

from __future__ import division # allows floating point division from integers

import Part
from FreeCAD import Base
import numpy
import FreeCAD

def addBox(location, size, name='box', locationIsLower=False, wireframe=False):
  
  obj = FreeCAD.ActiveDocument.addObject("Part::Box", name)
  
  if locationIsLower:
    loc = numpy.array(location)
  else:
    loc = numpy.array(location) - 0.5*numpy.array(size)
  
  loc = FreeCAD.Vector(*loc)
  obj.Placement = FreeCAD.Placement(loc, FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
  
  obj.Length = size[0]
  obj.Width  = size[1]
  obj.Height = size[2]
  obj.Label = name
  if wireframe:
    obj.ViewObject.DisplayMode = "Wireframe"
  return(obj)

def addCube_centre_size(centre, size=[1,1,1], name='cube'):
  side_length_X, side_length_Y, side_length_Z = size
  minBB = numpy.array(centre) - 0.5*numpy.array(size)
  obj = addCubeXYZ(side_length_X, side_length_Y, side_length_Z, minBB, name)
  return(obj)

def addCube(side_length, loc, name):
  obj = FreeCAD.ActiveDocument.addObject("Part::Box", name)
  obj.Placement = FreeCAD.Placement(FreeCAD.Vector(loc[0],loc[1],loc[2]), FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
  #	obj.Placement = FreeCAD.Placement(FreeCAD.Vector(loc[0],loc[1],loc[2])) # all args are mandatory :/
  obj.Length = side_length
  obj.Width = side_length
  obj.Height = side_length
  obj.Label = name
  return(obj)

def addCubeXYZ(side_length_X, side_length_Y, side_length_Z, minBB, name):
  obj = FreeCAD.ActiveDocument.addObject("Part::Box", name)
  obj.Placement = FreeCAD.Placement(FreeCAD.Vector(minBB[0],minBB[1],minBB[2]), FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
  obj.Length = side_length_X
  obj.Width = side_length_Y
  obj.Height = side_length_Z
  obj.Label = name
  return(obj)

def createWireBox(box_size, box_thickness):

  p = box_size - box_thickness

  x0 = addCubeXYZ(box_size, box_thickness, box_thickness, Base.Vector(0,0,0), 'x0')
  x1 = addCubeXYZ(box_size, box_thickness, box_thickness, Base.Vector(0,p,0), 'x1')
  x2 = addCubeXYZ(box_size, box_thickness, box_thickness, Base.Vector(0,0,p), 'x2')
  x3 = addCubeXYZ(box_size, box_thickness, box_thickness, Base.Vector(0,p,p), 'x3')

  y0 = addCubeXYZ(box_thickness, box_size, box_thickness, Base.Vector(0,0,0), 'y0')
  y1 = addCubeXYZ(box_thickness, box_size, box_thickness, Base.Vector(p,0,0), 'y1')
  y2 = addCubeXYZ(box_thickness, box_size, box_thickness, Base.Vector(0,0,p), 'y2')
  y3 = addCubeXYZ(box_thickness, box_size, box_thickness, Base.Vector(p,0,p), 'y3')

  z0 = addCubeXYZ(box_thickness, box_thickness, box_size, Base.Vector(0,0,0), 'z0')
  z1 = addCubeXYZ(box_thickness, box_thickness, box_size, Base.Vector(p,0,0), 'z1')
  z2 = addCubeXYZ(box_thickness, box_thickness, box_size, Base.Vector(0,p,0), 'z2')
  z3 = addCubeXYZ(box_thickness, box_thickness, box_size, Base.Vector(p,p,0), 'z3')

  WireBox = FreeCAD.activeDocument().addObject("Part::MultiFuse","WireBox")
  WireBox.Shapes = [x0,x1,x2,x3, y0,y1,y2,y3, z0,z1,z2,z3]

  return(WireBox)

def addAABB(minBB, maxBB, name='AABB'):
  '''Add a box representing an AABB bounding box from minBB to maxBB.'''
  #print(minBB, maxBB)
  minBB = numpy.array(minBB)
  maxBB = numpy.array(maxBB)
  loc = minBB
  #print('loc = ', loc)
  S = numpy.abs(maxBB - minBB)
  AABB = addCubeXYZ(S[0], S[1], S[2], loc, name)
  AABB.ViewObject.DisplayMode = "Wireframe"
  return(AABB)

def createGrid(minBB, maxBB):
  '''Create a grid (step size=1) from minBB to maxBB'''
  
  i_min,j_min,k_min = minBB
  i_max,j_max,k_max = maxBB
  
  obj_list = []
  for i in range(i_min, i_max):
    for j in range(j_min, j_max):
      for k in range(k_min, k_max):
        obj = addCubeXYZ(1,1,1,[i,j,k],'grid.{}.{}.{}'.format(i,j,k))
        obj.ViewObject.DisplayMode = "Wireframe"
        obj.ViewObject.Visibility=False
        obj_list.append(obj)
        
  if len(obj_list)>1:
    grid = FreeCAD.activeDocument().addObject("Part::MultiFuse","Fusion")
    grid.Shapes = obj_list
  else:
    grid = obj
  
  grid.ViewObject.Visibility=True
  grid.ViewObject.DisplayMode = "Wireframe"
  grid.Label = 'grid'
  return(grid)
