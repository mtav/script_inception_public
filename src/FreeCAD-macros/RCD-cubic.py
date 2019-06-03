from __future__ import division # allows floating point division from integers

import Part
from FreeCAD import Base

from math import sqrt, pi, sin, cos, asin
import numpy
from numpy import array

from utilities.geometry import getAABBCylinder, AABB_intersect, getAABBCylinder_loc_dir_len
from utilities.common import unitVector

import box

FreeCAD.Console.PrintMessage("START...\n")

doc = FreeCAD.activeDocument()
if doc is None:
  App.newDocument("Unnamed")
  doc = FreeCAD.activeDocument()

#cubic_unit_cell_size = 50
cubic_unit_cell_size = 1 # scaling messes up boolean ops sometimes :(
g_cylinder_length = sqrt(3)/4 * cubic_unit_cell_size
g_cylinder_radius = 0.26 * cubic_unit_cell_size
#g_cylinder_radius = 0.05 * cubic_unit_cell_size + 0.1
#g_cylinder_radius = 0.05 * cubic_unit_cell_size
ball_radius = (0.1+0.05) * cubic_unit_cell_size
a = cubic_unit_cell_size
g_location = array([0,0,0])

FRD = False
#cyl_delta = 0.075 * cubic_unit_cell_size
cyl_delta = 0.1

def tetra_FRD(location, name):
  dir0 = [-1, 1,-1]
  dir1 = [ 1,-1,-1]
  dir2 = [ 1, 1, 1]
  dir3 = [-1,-1, 1]
  cyl0 = addCylinder(location, dir0, name+'_cyl0')
  cyl1 = addCylinder(location, dir1, name+'_cyl1')
  cyl2 = addCylinder(location, dir2, name+'_cyl2')
  cyl3 = addCylinder(location, dir3, name+'_cyl3')
  f = App.activeDocument().addObject("Part::MultiFuse","Fusion")
  f.Shapes = [cyl0, cyl1, cyl2, cyl3]
  cyl0.ViewObject.Visibility=False
  cyl1.ViewObject.Visibility=False
  cyl2.ViewObject.Visibility=False
  cyl3.ViewObject.Visibility=False
  return(f)

def RCDCubicUnitCell_FRD(i, j, k):
  unit_cell_location = i*u + j*v + k*w

  t0_FRD = tetra_FRD(g_location + (unit_cell_location+array([1/4, 1/4, 1/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.0'.format(i,j,k))
  t1_FRD = tetra_FRD(g_location + (unit_cell_location+array([3/4, 3/4, 1/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.1'.format(i,j,k))
  t2_FRD = tetra_FRD(g_location + (unit_cell_location+array([3/4, 1/4, 3/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.2'.format(i,j,k))
  t3_FRD = tetra_FRD(g_location + (unit_cell_location+array([1/4, 3/4, 3/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.3'.format(i,j,k))

  f_FRD = App.activeDocument().addObject("Part::MultiFuse","Fusion")
  f_FRD.Shapes = [t0_FRD, t1_FRD, t2_FRD, t3_FRD]
  t0_FRD.ViewObject.Visibility=False
  t1_FRD.ViewObject.Visibility=False
  t2_FRD.ViewObject.Visibility=False
  t3_FRD.ViewObject.Visibility=False
  f_FRD.Label = 'cell.{}.{}.{}_FRD'.format(i+1,j+1,k+1)

  return(f_FRD)

def createRCD(shifted=False):
  for i in range(-1, 2):
    for j in range(-1, 2):
      for k in range(-1, 2):
        RCDCubicUnitCell(i, j, k, shifted)

def createBallConnector():
  sphere = App.ActiveDocument.addObject("Part::Sphere","Sphere")
  sphere.Label = "Sphere"
  sphere.Radius = ball_radius
  cyl_list = []
  for i in [-1,1]:
    for j in [-1,1]:
      for k in [-1,1]:
        cyl_list.append(addCylinder([0,0,0], [i,j,k], 'cyl_{}{}{}'.format((i+1)//2, (j+1)//2, (k+1)//2)))
  
  cut = App.activeDocument().addObject("Part::MultiFuse","cut")
  cut.Shapes = cyl_list

  ball_connector = App.activeDocument().addObject("Part::Cut","ball_connector")
  ball_connector.Base = sphere
  ball_connector.Tool = cut

  return

def addSphere(loc, r):
  sphere = App.ActiveDocument.addObject("Part::Sphere","Sphere")
  sphere.Label = "Sphere"
  sphere.Radius = r
  sphere.Placement = App.Placement(App.Vector(loc[0],loc[1],loc[2]), App.Rotation(App.Vector(0,0,1),0))

  return(sphere)

for i in doc.Objects:
  doc.removeObject(i.Name)

#createRCD(shifted=False)
#createRCD(shifted=True)
#createRCD()
Nx=1
Ny=1
Nz=1
side_length_X=1
side_length_Y=2
side_length_Z=3
loc=[1,1,1]
#cylinder_list = getCylinders_createRCD(Nx,Ny,Nz)
##print(cylinder_list)
#print('Nx*Ny*Nz*16 :', Nx*Ny*Nz*16)
#print('full:', len(cylinder_list))
#print('Creating full...')
#full = createCylinders(cylinder_list, 'full', add_AABB=False)
#full.ViewObject.Visibility = False

#cylinder_list_new = filterCylinders(cylinder_list, [side_length_X,side_length_Y,side_length_Z], loc)
##print(cylinder_list_new)
#print('filtered:', len(cylinder_list_new))
#print('Creating filtered...')
#filtered = createCylinders(cylinder_list_new, 'filtered')

#box = box.addCubeXYZ(side_length_X, side_length_Y, side_length_Z, loc, 'box')
#box.ViewObject.DisplayMode = "Wireframe"

#createGrid(2,3,4)
#createInverseRCD_at_location([-2.54,1.25,0.241])

#createInverseRCD_at_location([3,4,5])

#createInverseRCD_at_location([7.5,-4.5,5.5])

#createInverseRCD_at_location([1/8,1/8,1/8])

#createInverseRCD_at_location([0.25,0.25,0.25])

#createInverseRCD_at_location([0.5,0.5,0.5], shifted=False)

#createInverseRCD_at_location([0.5,0.5,1], shifted=False)

createInverseRCD_at_location([0.5+1/8,0.5+1/8,0.5+1/8], shifted=False)

addSphere(loc, r)

#createInverseRCD_at_location([1/8,1/8,1/8], shifted=False)

#RCDCubicUnitCell(0, 0, 0)
#createInverseRCD(shifted=True)
#createInverseRCD(shifted=False)
#RCDCubicUnitCell(0, 0, 0, shifted=False)
#RCDCubicUnitCell(0, 0, 0, shifted=True)
#addCylinder([0,0,0], [1,0,0], 'true', offset_cylinders = True)
#addCylinder([0,0,0], [1,0,0], 'false', offset_cylinders = False)

#addSphere(Base.Vector(0.5,0.5,0.5)*cubic_unit_cell_size, 0.24*cubic_unit_cell_size)

#box.addCube(cubic_unit_cell_size, [0,0,0], 'unitCube')

#box.createWireBox(1*cubic_unit_cell_size, 0.05*cubic_unit_cell_size)

#createBallConnector()

#unitCube1 = box.addCube(cubic_unit_cell_size, [0,0,0], 'unitCube1')
#unitCube2 = box.addCube(cubic_unit_cell_size, [1/2,1/2,1/2], 'unitCube2')
#RCD_inverse = App.activeDocument().addObject("Part::Cut","RCD_inverse")
#RCD_inverse.Base = unitCube1
#RCD_inverse.Tool = unitCube2

doc.recompute()
#doc.ActiveView.setAxisCross(True)
Gui.ActiveDocument.ActiveView.setAxisCross(True)
Gui.SendMsgToActiveView("ViewFit")

from PySide import QtGui
QtGui.QMessageBox.information(None, 'RCD-cubic', "DONE")

FreeCAD.Console.PrintMessage("...DONE\n")
