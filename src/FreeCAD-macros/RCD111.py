from __future__ import division # allows floating point division from integers

import Part
from FreeCAD import Base

from math import sqrt, pi, sin, cos, asin
from numpy import array
import numpy

from utilities.geometry import getAABBCylinder, AABB_intersect, getAABBCylinder_loc_dir_len

import box
from bfdtd.RCD import RCD_HexagonalLattice

'''
.. todo:: Add to this library?: https://github.com/FreeCAD/FreeCAD-library
'''

FreeCAD.Console.PrintMessage("START...\n")

doc = FreeCAD.activeDocument()
if doc is None:
  App.newDocument("Unnamed")
  doc = FreeCAD.activeDocument()

cubic_unit_cell_size = 1
L = sqrt(3)/4 * cubic_unit_cell_size
#R = 0.05 * cubic_unit_cell_size
R = 0.26 * cubic_unit_cell_size

#location =  array([0,0,1.5])*L
location =  array([0,0,0])*L

offset2 = array([-sqrt(2)/4, 0, 11*sqrt(3)/24])

u2 = array([sqrt(2)/2, 0, 0])
v2 = array([0, sqrt(6)/2, 0])
w2 = array([0, 0, sqrt(3)])

unitCellType2_size = [numpy.linalg.norm(u2), numpy.linalg.norm(v2), numpy.linalg.norm(w2)]

# The tetrahedron centres
R0 = array([ sqrt(2)/4,   1/sqrt(6),     sqrt(3)/4])
R1 = array([-sqrt(2)/4,   1/sqrt(6),     sqrt(3)/4])
R2 = array([         0, -1/sqrt(24),     sqrt(3)/4])

G0 = array([ sqrt(2)/4,           0,  7*sqrt(3)/12])
G1 = array([         0,   sqrt(6)/4,  7*sqrt(3)/12])
G2 = array([-sqrt(2)/4,           0,  7*sqrt(3)/12])

B0 = array([ sqrt(2)/4,  -1/sqrt(6), 11*sqrt(3)/12])
B1 = array([         0,  1/sqrt(24), 11*sqrt(3)/12])
B2 = array([-sqrt(2)/4,  -1/sqrt(6), 11*sqrt(3)/12])

def addSphere(L, loc, name):
  defect_shape = Part.makeSphere(L/2, Base.Vector(0, 0, loc*L))
  defect_obj = doc.addObject("Part::Feature", name)
  defect_obj.Shape = defect_shape

def addSphere2(L, loc, name):
  obj = App.ActiveDocument.addObject("Part::Sphere", name)
  obj.Placement = App.Placement(App.Vector(0,0,loc*L),App.Rotation(App.Vector(0,0,1),0))
  obj.Radius = L/2
  obj.Label = name

#Sx=2
#Sy=2
#Sz=2
#backfill_shape = Part.makeBox(Sx, Sy, Sz, Base.Vector(-Sx/2, -Sy/2, -Sz/2))

def addCylinder(loc, direction, name, backfill_shape):
  #	A = loc
  #	B = loc + direction*L
  #M = max(R,L)
  #	loc
  #	if loc[0]<Sx
  x = direction[0]
  y = direction[1]
  z = direction[2]
  cyl_shape = Part.makeCylinder(R, L, Base.Vector(loc[0],loc[1], loc[2]), Base.Vector(x,y,z), 360)

  #cyl.Shape.BoundBox
  minBB_cyl = App.Vector(cyl_shape.BoundBox.XMin, cyl_shape.BoundBox.YMin, cyl_shape.BoundBox.ZMin)
  maxBB_cyl = App.Vector(cyl_shape.BoundBox.XMax, cyl_shape.BoundBox.YMax, cyl_shape.BoundBox.ZMax)

  minBB_block = [backfill_shape.BoundBox.XMin, backfill_shape.BoundBox.YMin, backfill_shape.BoundBox.ZMin]
  maxBB_block = [backfill_shape.BoundBox.XMax, backfill_shape.BoundBox.YMax, backfill_shape.BoundBox.ZMax]

  #backfill_shape.BoundBox.isIntersection(cyl.Shape.BoundBox)
  #	val = backfill_shape.isInside(lower, R, True) or backfill_shape.isInside(upper, R, True)
  #val = backfill_shape.BoundBox.isInside(minBB_cyl) or backfill_shape.BoundBox.isInside(maxBB_cyl)
  val = AABB_intersect(minBB_cyl, maxBB_cyl, minBB_block, maxBB_block)

  #val = cyl_shape.BoundBox.isInside(backfill_shape.BoundBox)
  FreeCAD.Console.PrintMessage("{} : {}\n".format(name, val))

  if val:
    cyl_obj = doc.addObject("Part::Feature", name)
    cyl_obj.Shape = cyl_shape
    #cyl_obj.ViewObject.DisplayMode = "Wireframe"
    cyl_obj.ViewObject.DisplayMode = "Flat Lines"
    cyl_obj.Label = name
    # backfill_shape = backfill_obj.Shape
    #backfill_shape = backfill_shape.cut(cyl_shape)
    return([cyl_obj])
  else:
    return([])

def tetra(location, name, backfill_shape):
  object_list = []
  
  dir0 = [0, 0, -sqrt(3)/4]
  dir1 = [0, -1/sqrt(6), sqrt(3)/12]
  dir2 = [sqrt(2)/4, 1/sqrt(24), sqrt(3)/12]
  dir3 = [-sqrt(2)/4, 1/sqrt(24), sqrt(3)/12]	
  object_list += addCylinder(location, dir0, name+'_cyl0', backfill_shape)
  object_list += addCylinder(location, dir1, name+'_cyl1', backfill_shape)
  object_list += addCylinder(location, dir2, name+'_cyl2', backfill_shape)
  object_list += addCylinder(location, dir3, name+'_cyl3', backfill_shape)
  
  return(object_list)

def unitCellType2(i, j, k, backfill_shape):
  object_list = []
  
  unit_cell_location = i*u2 + j*v2 + k*w2

  object_list += tetra(location + (unit_cell_location - offset2 + R1)*cubic_unit_cell_size, 'cell.{}.{}.{}.R1'.format(i,j,k), backfill_shape)
  object_list += tetra(location + (unit_cell_location - offset2 + G1)*cubic_unit_cell_size, 'cell.{}.{}.{}.G1'.format(i,j,k), backfill_shape)
  object_list += tetra(location + (unit_cell_location - offset2 + B1)*cubic_unit_cell_size, 'cell.{}.{}.{}.B1'.format(i,j,k), backfill_shape)

  object_list += tetra(location + (unit_cell_location - offset2 + R2)*cubic_unit_cell_size, 'cell.{}.{}.{}.R2'.format(i,j,k), backfill_shape)
  object_list += tetra(location + (unit_cell_location - offset2 + G2)*cubic_unit_cell_size, 'cell.{}.{}.{}.G2'.format(i,j,k), backfill_shape)
  object_list += tetra(location + (unit_cell_location - offset2 + B2)*cubic_unit_cell_size, 'cell.{}.{}.{}.B2'.format(i,j,k), backfill_shape)
  
  return(object_list)

def createRCD(backfill_shape):
  
  object_list = []
  
  Nx=1
  Ny=1
  Nz=1
  
  for i in range(-1, 2):
    for j in range(-1, 2):
      for k in range(-1, 4):
        object_list += unitCellType2(i, j, k, backfill_shape)
        
  f = App.activeDocument().addObject("Part::MultiFuse","Fusion")
  f.Shapes = object_list
  f.Label = 'RCD111'
  return(f)

def createInverseRCD111(shifted=False):
  group = App.ActiveDocument.addObject("App::DocumentObjectGroup", "InverseRCD111.{}".format(shifted))
  
  print('Creating unit cell block...')
  if shifted:
    unitCellType2_box = box.addBox([0,0,numpy.sqrt(3)/2], unitCellType2_size, name="unitCellType2_box", locationIsLower=False, wireframe=True)
  else:
    unitCellType2_box = box.addBox([0,0,0], unitCellType2_size, name="unitCellType2_box", locationIsLower=False, wireframe=True)
  
  print('Creating RCD111...')
  filtered = createRCD(unitCellType2_box.Shape)
  
  print('Creating inverse RCD111...')
  RCD111_inverse = App.activeDocument().addObject("Part::Cut","RCD_inverse")
  RCD111_inverse.Base = unitCellType2_box
  RCD111_inverse.Tool = filtered
  group.addObject(RCD111_inverse)
  return(RCD111_inverse)

def getCylinders_createRCD111(backfill_shape):
  cylinder_list = []
  
  Nx=1
  Ny=1
  Nz=1
  
  for i in range(-1, 2):
    for j in range(-1, 2):
      for k in range(-1, 2):
        cylinder_list += getCylinders_unitCellType2(i, j, k, backfill_shape)
  return(cylinder_list)

def createInverseRCD111_at_location(unitcell_centro, shifted=False):
  group = App.ActiveDocument.addObject("App::DocumentObjectGroup", "InverseRCD.{}.{:.3f}.{:.3f}.{:.3f}".format(shifted, *unitcell_centro))
  
  print('Creating unit cell block...')
  unitCellType2_box = box.addBox(unitcell_centro, unitCellType2_size, name="unitCellType2_box", locationIsLower=False, wireframe=True)
  group.addObject(unitCellType2_box)
  return

# clear document
for i in doc.Objects:
  doc.removeObject(i.Name)

#addSphere2(L/2, 0, 'defect_0.0')
#addSphere2(L, 0.5, 'defect_0.5')
#addSphere2(L, 1, 'defect_1.0')
#addSphere2(L, 1.5, 'defect_1.5')
#addSphere2(L, 2, 'defect_2.0')

#backfill_obj = doc.addObject("Part::Feature", 'backfill')
#backfill_obj.Shape = backfill_shape
#backfill_obj.ViewObject.DisplayMode = "Wireframe"

#box.addBox([0,0,0], [1,1,1], name='box00', locationIsLower=False, wireframe=False)
#box.addBox([0,0,0], [1,1,1], name='box01', locationIsLower=False, wireframe=True )
#box.addBox([0,0,0], [1,1,1], name='box10', locationIsLower=True , wireframe=False)
#box.addBox([0,0,0], [1,1,1], name='box11', locationIsLower=True , wireframe=True )

#delta = 0.5
#backfill_obj = box.addBox([-delta, -delta, -2*L-delta], [2*delta, 2*delta, 4*L + 2*delta], name="backfill", locationIsLower=True, wireframe=True)
#backfill_obj.ViewObject.LineColor = (1.,0.,0.)

#backfill_obj = App.ActiveDocument.addObject("Part::Box","backfill")
#backfill_obj.Placement = App.Placement(App.Vector(-delta, -delta, -2*L-delta), App.Rotation(App.Vector(0,0,1), 0))
#backfill_obj.Length = 2*delta
#backfill_obj.Width = 2*delta
#backfill_obj.Height = 4*L + 2*delta
#backfill_obj.ViewObject.DisplayMode = "Wireframe"
#backfill_obj.ViewObject.LineColor = (1.,0.,0.)

#delta = 0.75
#BB_obj = box.addBox([-delta, -delta, -2*L-delta], [2*delta, 2*delta, 4*L + 2*delta], name="bounding_box", locationIsLower=True, wireframe=True)
#BB_obj.ViewObject.LineColor = (1.,0.,0.)

#unitCellType2_box = box.addBox([0,0,0], unitCellType2_size, name="unitCellType2_box", locationIsLower=False, wireframe=True)

#BB_obj = App.ActiveDocument.addObject("Part::Box","bounding_box")
#BB_obj.Placement = App.Placement(App.Vector(-delta, -delta, -2*L-delta), App.Rotation(App.Vector(0,0,1), 0))
#BB_obj.Length = 2*delta
#BB_obj.Width = 2*delta
#BB_obj.Height = 4*L + 2*delta
#BB_obj.ViewObject.DisplayMode = "Wireframe"
#BB_obj.ViewObject.LineColor = (1.,0.,0.)

#backfill_shape = BB_obj.Shape

#addCylinder([0,0,0], [0,0,1], '000', backfill_shape)
#addCylinder([1,0,0], [0,0,1], '100', backfill_shape)
#addCylinder([2,0,0], [0,0,1], '200', backfill_shape)
#createRCD(backfill_shape)
#createRCD(unitCellType2_box.Shape)

createInverseRCD111(shifted=False)
createInverseRCD111(shifted=True)
#createInverseRCD111_at_location([0,0,0], shifted=False)

doc.recompute()

Gui.ActiveDocument.ActiveView.setAxisCross(True)
Gui.SendMsgToActiveView("ViewFit")

from PySide import QtGui
QtGui.QMessageBox.information(None, 'RCD111', "DONE")

FreeCAD.Console.PrintMessage("...DONE\n")
