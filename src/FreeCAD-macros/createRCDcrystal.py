from __future__ import division # allows floating point division from integers

import Part
from FreeCAD import Base

import MeshPartGui, FreeCADGui
import Mesh, Part, PartGui
import MeshPart
import Draft

import numpy as np
from math import sqrt, pi, sin, cos, asin
from numpy import array

import time
import tkinter
from PySide2 import QtWidgets

###############################################################################
# get the start time
st = time.time()
FreeCAD.Console.PrintMessage("START...\n")
###############################################################################

#doc = FreeCAD.activeDocument()
doc = App.newDocument()

###############################################################################
##### PARAMETERS YOU CAN CHANGE:
###############################################################################
# Pick the crystal you want:

##### normal RCD
RCD_parameter_list = [{'shift':False, 'FRD':False}]

##### normal RCD shifted
# RCD_parameter_list = [{'shift':True, 'FRD':False}]

##### normal RCD rotated 90 degrees
# RCD_parameter_list = [{'shift':True, 'FRD':True}]

##### normal RCD shifted rotated 90 degrees
# RCD_parameter_list = [{'shift':False, 'FRD':True}]

##### normal FRD (8 cylinder intersection in the centre)
# RCD_parameter_list = [{'shift':False, 'FRD':False},
#                       {'shift':True, 'FRD':True}]

##### shited FRD (ball structure in the centre)
# RCD_parameter_list = [{'shift':True, 'FRD':False},
#                       {'shift':False, 'FRD':True}]

##### double RCD
# RCD_parameter_list = [{'shift':False, 'FRD':False},
#                       {'shift':True, 'FRD':False}]

##### double RCD shifted
#RCD_parameter_list = [{'shift':False, 'FRD':True},
#                       {'shift':True, 'FRD':True}]

#RCD_parameter_list = [{'shift':False, 'FRD':True},
#                      {'shift':True, 'FRD':True},
#			{'shift':False, 'FRD':False},
#			{'shift':True, 'FRD':False}]

########

# number of periods
Nx=1
Ny=1
Nz=1
# unit-cell size
cubic_unit_cell_size = 1 # scaling messes up boolean ops sometimes :(
# cylinder radius
R=0.10 # cylinder radius
create_array = False # create array (takes longer)
###############################################################################
##### DO NOT EDIT ANYTHING BELOW THIS LINE, UNLESS YOU KNOW WHAT YOU ARE DOING.
###############################################################################

L = sqrt(3)/4 * cubic_unit_cell_size

#R = 0.05 * cubic_unit_cell_size + 0.1
ball_radius = (0.1+0.05) * cubic_unit_cell_size
a = cubic_unit_cell_size
location = array([0,0,0])

offset_cylinders = False
#FRD = False
#cyl_delta = 0.075 * cubic_unit_cell_size
cyl_delta = 0.1

u = array([1, 0, 0])
v = array([0, 1, 0])
w = array([0, 0, 1])

def mychoicebox(choicelist):
	# https://stackoverflow.com/questions/50538963/creating-a-choicelist-dialog-box-with-tkinter
	global result

	def buttonfn():
		global result
		result = var.get()
		choicewin.quit()

	choicewin = tkinter.Tk()
	choicewin.resizable(False, False)
	choicewin.title("ChoiceBox")

	tkinter.Label(choicewin, text="Select an item:").grid(row=0, column=0, sticky="W")

	var = tkinter.StringVar(choicewin)
	var.set("No data")  # default option
	popupMenu = tkinter.OptionMenu(choicewin, var, *choicelist)
	popupMenu.grid(sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W, row=1, column=0)

	tkinter.Button(choicewin, text="Done", command=buttonfn).grid(row=2, column=0)
	choicewin.mainloop()
	return result

def addCylinder(loc, dir, name):
	x = dir[0]
	y = dir[1]
	z = dir[2]
	u = Base.Vector(x,y,z).normalize()
	if offset_cylinders:
		cyl_shape = Part.makeCylinder(R, L-2*cyl_delta, Base.Vector(loc[0],loc[1], loc[2]) + u*cyl_delta, u, 360)
	else:
		cyl_shape = Part.makeCylinder(R, L, Base.Vector(loc[0],loc[1], loc[2]), u, 360)
	cyl_obj = doc.addObject("Part::Feature", name)
	cyl_obj.Shape = cyl_shape
	cyl_obj.ViewObject.DisplayMode = "Flat Lines"
	cyl_obj.Label = name
	return(cyl_obj)

def tetra(location, name):
	dir0 = [-1,-1,-1]
	dir1 = [1, 1,-1]
	dir2 = [1,-1,1]
	dir3 = [-1,1,1]
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

def RCDCubicUnitCell(i, j, k, shift=False):
    unit_cell_location = i*u + j*v + k*w
    
    if shift:
        t0 = tetra(location + (unit_cell_location+array([3/4, 3/4, 1/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.0'.format(i,j,k))
        t1 = tetra(location + (unit_cell_location+array([1/4, 1/4, 1/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.1'.format(i,j,k))
        t2 = tetra(location + (unit_cell_location+array([3/4, 1/4, 3/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.2'.format(i,j,k))
        t3 = tetra(location + (unit_cell_location+array([1/4, 3/4, 3/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.3'.format(i,j,k))
    else:
        t0 = tetra(location + (unit_cell_location+array([1/4, 3/4, 1/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.0'.format(i,j,k))
        t1 = tetra(location + (unit_cell_location+array([3/4, 1/4, 1/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.1'.format(i,j,k))
        t2 = tetra(location + (unit_cell_location+array([1/4, 1/4, 3/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.2'.format(i,j,k))
        t3 = tetra(location + (unit_cell_location+array([3/4, 3/4, 3/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.3'.format(i,j,k))
    
    f = App.activeDocument().addObject("Part::MultiFuse","Fusion")
    f.Shapes = [t0, t1, t2, t3]
    t0.ViewObject.Visibility=False
    t1.ViewObject.Visibility=False
    t2.ViewObject.Visibility=False
    t3.ViewObject.Visibility=False
    f.Label = 'cell.{}.{}.{}'.format(i+1,j+1,k+1)

    return(f)

def RCDCubicUnitCell_FRD(i, j, k, shift=False):
    unit_cell_location = i*u + j*v + k*w
    if shift:
        t0_FRD = tetra_FRD(location + (unit_cell_location+array([1/4, 1/4, 1/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.0'.format(i,j,k))
        t1_FRD = tetra_FRD(location + (unit_cell_location+array([3/4, 3/4, 1/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.1'.format(i,j,k))
        t2_FRD = tetra_FRD(location + (unit_cell_location+array([3/4, 1/4, 3/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.2'.format(i,j,k))
        t3_FRD = tetra_FRD(location + (unit_cell_location+array([1/4, 3/4, 3/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.3'.format(i,j,k))
    else:
        t0_FRD = tetra_FRD(location + (unit_cell_location+array([3/4, 1/4, 1/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.0'.format(i,j,k))
        t1_FRD = tetra_FRD(location + (unit_cell_location+array([1/4, 3/4, 1/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.1'.format(i,j,k))
        t2_FRD = tetra_FRD(location + (unit_cell_location+array([1/4, 1/4, 3/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.2'.format(i,j,k))
        t3_FRD = tetra_FRD(location + (unit_cell_location+array([3/4, 3/4, 3/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.3'.format(i,j,k))
    
    f_FRD = App.activeDocument().addObject("Part::MultiFuse","Fusion")
    f_FRD.Shapes = [t0_FRD, t1_FRD, t2_FRD, t3_FRD]
    t0_FRD.ViewObject.Visibility=False
    t1_FRD.ViewObject.Visibility=False
    t2_FRD.ViewObject.Visibility=False
    t3_FRD.ViewObject.Visibility=False
    f_FRD.Label = 'cell.{}.{}.{}_FRD'.format(i+1,j+1,k+1)
    
    return(f_FRD)


def createRCD(Nx, Ny, Nz, add_extra=False, name='RCD', FRD=False, shift=False):
	L = []  # list of unit-cells
	if add_extra:
		imin = -1
		jmin = -1
		kmin = -1
		imax = Nx
		jmax = Ny
		kmax = Nz
	else:
		imin = 0
		jmin = 0
		kmin = 0
		imax = Nx - 1
		jmax = Ny - 1
		kmax = Nz - 1
	for i in range(imin, imax + 1):
		for j in range(jmin, jmax + 1):
			for k in range(kmin, kmax + 1):
				if FRD:
					U = RCDCubicUnitCell_FRD(i, j, k, shift=shift)
				else:
					U = RCDCubicUnitCell(i, j, k, shift=shift)

				L.append(U)

	# if add_extra or Nx*Ny*Nz>1:
	if len(L) > 1:
		# merge cells into one supercell
		RCD = App.activeDocument().addObject("Part::MultiFuse", "Fusion")
		RCD.Shapes = L
		RCD.Label = name
		return (RCD)
	else:
		# only one unit-cell
		L[0].Label = name
		return (L[0])

def addCube(side_length, loc, name):
	obj = App.ActiveDocument.addObject("Part::Box", name)
	obj.Placement = App.Placement(App.Vector(loc[0],loc[1],loc[2]), App.Rotation(App.Vector(0,0,1),0))
#	obj.Placement = App.Placement(App.Vector(loc[0],loc[1],loc[2])) # all args are mandatory :/
	obj.Length = side_length
	obj.Width = side_length
	obj.Height = side_length
	obj.Label = name
	return obj

def addCubeXYZ(side_length_X, side_length_Y, side_length_Z, loc, name):
	obj = App.ActiveDocument.addObject("Part::Box", name)
	obj.Placement = App.Placement(App.Vector(loc[0],loc[1],loc[2]), App.Rotation(App.Vector(0,0,1),0))
	obj.Length = side_length_X
	obj.Width = side_length_Y
	obj.Height = side_length_Z
	obj.Label = name
	return obj

def createInverseRCD():
	main_RCD = RCDCubicUnitCell(0, 0, 0)

	if FRD:
		main_FRD = RCDCubicUnitCell_FRD(0, 0, 0)

	# X+ face
	cyl0 = addCylinder(Base.Vector(1,   0,   0)*cubic_unit_cell_size,     [1, 1, 1], 'xplus-0')
	cyl1 = addCylinder(Base.Vector(1, 1/2, 1/2)*cubic_unit_cell_size,     [1,-1,-1], 'xplus-1')
	cyl2 = addCylinder(Base.Vector(1, 1/2, 1/2)*cubic_unit_cell_size,     [1, 1, 1], 'xplus-2')
	cyl3 = addCylinder(Base.Vector(1,   1,   1)*cubic_unit_cell_size,     [1,-1,-1], 'xplus-3')
	xplus = App.activeDocument().addObject("Part::MultiFuse","xplus")
	xplus.Shapes = [cyl0, cyl1, cyl2, cyl3]
	
	# X- face
	cyl0 = addCylinder(Base.Vector(0,   0,   1)*cubic_unit_cell_size,     [-1, 1, -1], 'xminus-0')
	cyl1 = addCylinder(Base.Vector(0, 1/2, 1/2)*cubic_unit_cell_size,     [-1, -1, 1], 'xminus-1')
	cyl2 = addCylinder(Base.Vector(0, 1/2, 1/2)*cubic_unit_cell_size,     [-1, 1, -1], 'xminus-2')
	cyl3 = addCylinder(Base.Vector(0,   1,   0)*cubic_unit_cell_size,     [-1, -1, 1], 'xminus-3')
	xminus = App.activeDocument().addObject("Part::MultiFuse","xminus")
	xminus.Shapes = [cyl0, cyl1, cyl2, cyl3]
	
	# Y+ face
	cyl0 = addCylinder(Base.Vector(  0,   1,   0)*cubic_unit_cell_size,     [ 1,  1,  1], 'yplus-0')
	cyl1 = addCylinder(Base.Vector(1/2,   1, 1/2)*cubic_unit_cell_size,     [-1,  1, -1], 'yplus-1')
	cyl2 = addCylinder(Base.Vector(1/2,   1, 1/2)*cubic_unit_cell_size,     [ 1,  1,  1], 'yplus-2')
	cyl3 = addCylinder(Base.Vector(  1,   1,   1)*cubic_unit_cell_size,     [-1,  1, -1], 'yplus-3')
	yplus = App.activeDocument().addObject("Part::MultiFuse","yplus")
	yplus.Shapes = [cyl0, cyl1, cyl2, cyl3]
	
	# Y- face
	cyl0 = addCylinder(Base.Vector(  0,   0,    1)*cubic_unit_cell_size,    [ 1, -1, -1], 'yminus-0')
	cyl1 = addCylinder(Base.Vector(1/2,   0,  1/2)*cubic_unit_cell_size,    [-1, -1,  1], 'yminus-1')
	cyl2 = addCylinder(Base.Vector(1/2,   0,  1/2)*cubic_unit_cell_size,    [ 1, -1, -1], 'yminus-2')
	cyl3 = addCylinder(Base.Vector(  1,   0,    0)*cubic_unit_cell_size,    [-1, -1,  1], 'yminus-3')
	yminus = App.activeDocument().addObject("Part::MultiFuse","yminus")
	yminus.Shapes = [cyl0, cyl1, cyl2, cyl3]
	
	# Z+ face
	cyl0 = addCylinder(Base.Vector(  0, 0,   1)*cubic_unit_cell_size,     [ 1, 1, 1], 'zplus-0')
	cyl1 = addCylinder(Base.Vector(1/2, 1/2, 1)*cubic_unit_cell_size,     [-1,-1, 1], 'zplus-1')
	cyl2 = addCylinder(Base.Vector(1/2, 1/2, 1)*cubic_unit_cell_size,     [ 1, 1, 1], 'zplus-2')
	cyl3 = addCylinder(Base.Vector(  1, 1,   1)*cubic_unit_cell_size,     [-1,-1, 1], 'zplus-3')
	zplus = App.activeDocument().addObject("Part::MultiFuse","zplus")
	zplus.Shapes = [cyl0, cyl1, cyl2, cyl3]
	
	# Z- face
	cyl0 = addCylinder(Base.Vector(  0,   1, 0)*cubic_unit_cell_size,     [ 1,-1,-1], 'zminus-0')
	cyl1 = addCylinder(Base.Vector(1/2, 1/2, 0)*cubic_unit_cell_size,     [-1, 1,-1], 'zminus-1')
	cyl2 = addCylinder(Base.Vector(1/2, 1/2, 0)*cubic_unit_cell_size,     [ 1,-1,-1], 'zminus-2')
	cyl3 = addCylinder(Base.Vector(  1,   0, 0)*cubic_unit_cell_size,     [-1, 1,-1], 'zminus-3')
	zminus = App.activeDocument().addObject("Part::MultiFuse","zminus")
	zminus.Shapes = [cyl0, cyl1, cyl2, cyl3]

	cut = App.activeDocument().addObject("Part::MultiFuse","cut")
	cut.Shapes = [main_RCD, xplus, xminus, yplus, yminus, zplus, zminus]

	unitCube = addCube(cubic_unit_cell_size, [0,0,0], 'unitCube')

	RCD_inverse = App.activeDocument().addObject("Part::Cut","RCD_inverse")
	RCD_inverse.Base = unitCube
	RCD_inverse.Tool = cut

def createDirectRCD():
	t0 = tetra(location + (array([1/2, 1/2, 1/2]))*cubic_unit_cell_size, 't0')

	tx0 = tetra(location + (array([1/2, 1/2, 1/2])+array([0,  1/2,  1/2]))*cubic_unit_cell_size, 'tx0')
	tx1 = tetra(location + (array([1/2, 1/2, 1/2])+array([0,  1/2, -1/2]))*cubic_unit_cell_size, 'tx1')
	tx2 = tetra(location + (array([1/2, 1/2, 1/2])+array([0, -1/2,  1/2]))*cubic_unit_cell_size, 'tx2')
	tx3 = tetra(location + (array([1/2, 1/2, 1/2])+array([0, -1/2, -1/2]))*cubic_unit_cell_size, 'tx3')
	xplus = App.activeDocument().addObject("Part::MultiFuse","xplus")
	xplus.Shapes = [tx0, tx1, tx2, tx3]

	ty0 = tetra(location + (array([1/2, 1/2, 1/2])+array([ 1/2, 0,  1/2]))*cubic_unit_cell_size, 'ty0')
	ty1 = tetra(location + (array([1/2, 1/2, 1/2])+array([ 1/2, 0, -1/2]))*cubic_unit_cell_size, 'ty1')
	ty2 = tetra(location + (array([1/2, 1/2, 1/2])+array([-1/2, 0,  1/2]))*cubic_unit_cell_size, 'ty2')
	ty3 = tetra(location + (array([1/2, 1/2, 1/2])+array([-1/2, 0, -1/2]))*cubic_unit_cell_size, 'ty3')
	yplus = App.activeDocument().addObject("Part::MultiFuse","yplus")
	yplus.Shapes = [ty0, ty1, ty2, ty3]

	tz0 = tetra(location + (array([1/2, 1/2, 1/2])+array([ 1/2,  1/2, 0]))*cubic_unit_cell_size, 'tz0')
	tz1 = tetra(location + (array([1/2, 1/2, 1/2])+array([ 1/2, -1/2, 0]))*cubic_unit_cell_size, 'tz1')
	tz2 = tetra(location + (array([1/2, 1/2, 1/2])+array([-1/2,  1/2, 0]))*cubic_unit_cell_size, 'tz2')
	tz3 = tetra(location + (array([1/2, 1/2, 1/2])+array([-1/2, -1/2, 0]))*cubic_unit_cell_size, 'tz3')
	zplus = App.activeDocument().addObject("Part::MultiFuse","zplus")
	zplus.Shapes = [tz0, tz1, tz2, tz3]

	RCDpart = App.activeDocument().addObject("Part::MultiFuse","RCDpart")
	RCDpart.Shapes = [t0, xplus, yplus, zplus]

	unitCube = addCube(cubic_unit_cell_size, [0,0,0], 'unitCube')

	intersect = App.activeDocument().addObject("Part::MultiCommon","Common")
	intersect.Shapes = [RCDpart, unitCube]

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

def createWireBox(box_size, box_thickness):

	p = box_size-box_thickness

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

	WireBox = App.activeDocument().addObject("Part::MultiFuse","WireBox")
	WireBox.Shapes = [x0,x1,x2,x3, y0,y1,y2,y3, z0,z1,z2,z3]

	return

def main():

	# remove all current objects in document
	for i in doc.Objects:
		doc.removeObject(i.Name)


	side_length_X = Nx*cubic_unit_cell_size
	side_length_Y = Ny*cubic_unit_cell_size
	side_length_Z = Nz*cubic_unit_cell_size

	#RCDCubicUnitCell_FRD(0, 0, 0)
	# for FRD in [False, True]:
	#     for shift in [False, True]:
	#         createRCD(Nx, Ny, Nz, add_extra=False, name=f'RCD_FRD-{FRD}_shift-{shift}', FRD=FRD, shift=shift)

	postprocess = True
	convertToMesh = True
	# if doFRD:
	#     RCD = createRCD(1, 1, 1, add_extra=True, name=f'RCD', FRD=False, shift=False)
	#     FRD = createRCD(1, 1, 1, add_extra=True, name=f'FRD', FRD=True, shift=True)
	#     if postprocess:
	#         crystal = App.activeDocument().addObject("Part::MultiFuse","crystal")
	#         crystal.Shapes = [RCD, FRD]
	# else:
	#     crystal = createRCD(1, 1, 1, add_extra=True, name=f'RCD', FRD=False, shift=False)
	#     # crystal.Label = 'mylabel'

	# for FRD in [True, False]:
	# 	for shift in [True, False]:
	# 		createRCD(1, 1, 1, add_extra=False, name=f'createRCD_FRD-{FRD}_shift-{shift}', FRD=FRD, shift=shift)

	RCD_list = []
	for params in RCD_parameter_list:
		FRD = params['FRD']
		shift = params['shift']
		RCD = createRCD(1, 1, 1, add_extra=True, name=f'createRCD_FRD-{FRD}_shift-{shift}', FRD=FRD, shift=shift)
		RCD_list.append(RCD)

	if postprocess:
		##### Merge the crystals and truncate them with a box.

		if len(RCD_list) == 1:
			crystal = RCD_list[0]
		else:
			crystal = App.activeDocument().addObject("Part::MultiFuse", "crystal")
			crystal.Shapes = RCD_list

		#createRCD(Nx, Ny, Nz, add_extra=True, name='RCD_ext')
		# box = addCubeXYZ(side_length_X, side_length_Y, side_length_Z, [0,0,0], 'box')
		box = addCubeXYZ(1, 1, 1, [0,0,0], 'box')

		RCD_truncated = App.activeDocument().addObject("Part::MultiCommon","Common")
		#App.activeDocument().Common.Shapes = [box, RCD]
		# App.activeDocument().Common.Shapes = [box, RCD, FRD]
		App.activeDocument().Common.Shapes = [box, crystal]

	if create_array:
	  if convertToMesh:
	      FreeCAD.ActiveDocument.recompute()
	      # print(RCD_truncated)
	      # print(type(RCD_truncated))

	      __shape__=Part.getShape(RCD_truncated,"")
	      print('type(RCD_truncated)', type(RCD_truncated))
	      print('type(__shape__)', type(__shape__))
	      print('RCD_truncated.Shape:', RCD_truncated.Shape)
	      print('RCD_truncated.Shape.Volume:', RCD_truncated.Shape.Volume)
	      #print('Volume 2:', __shape__.Volume)
	      # print(__shape__)
	      __mesh__ = App.activeDocument().addObject("Mesh::Feature","Mesh")
	      __mesh__.Mesh = MeshPart.meshFromShape(Shape=__shape__, LinearDeflection=0.1, AngularDeflection=0.523599, Relative=False)

	      _obj_ = Draft.make_ortho_array(__mesh__,
	                                      v_x = FreeCAD.Vector(cubic_unit_cell_size, 0.0, 0.0),
	                                      v_y = FreeCAD.Vector(0.0, cubic_unit_cell_size, 0.0),
	                                      v_z = FreeCAD.Vector(0.0, 0.0, cubic_unit_cell_size),
	                                      n_x=Nx, n_y=Ny, n_z=Nz, use_link=True)
	      _obj_.Fuse = False
	  else:
	      _obj_ = Draft.make_ortho_array(RCD_truncated,
	                                      v_x = FreeCAD.Vector(cubic_unit_cell_size, 0.0, 0.0),
	                                      v_y = FreeCAD.Vector(0.0, cubic_unit_cell_size, 0.0),
	                                      v_z = FreeCAD.Vector(0.0, 0.0, cubic_unit_cell_size),
	                                      n_x=Nx, n_y=Ny, n_z=Nz, use_link=True)
	      _obj_.Fuse = False

	#createDirectRCD()
	#RCDCubicUnitCell(0, 0, 0)
	#createInverseRCD()

	#addSphere(Base.Vector(0.5,0.5,0.5)*cubic_unit_cell_size, 0.24*cubic_unit_cell_size)

	#addCube(cubic_unit_cell_size, [0,0,0], 'unitCube')

	#createWireBox(2*cubic_unit_cell_size, 0.05*cubic_unit_cell_size)

	#createBallConnector()

	#unitCube1 = addCube(cubic_unit_cell_size, [0,0,0], 'unitCube1')
	#unitCube2 = addCube(cubic_unit_cell_size, [1/2,1/2,1/2], 'unitCube2')
	#RCD_inverse = App.activeDocument().addObject("Part::Cut","RCD_inverse")
	#RCD_inverse.Base = unitCube1
	#RCD_inverse.Tool = unitCube2

	doc.recompute()
	#doc.ActiveView.setAxisCross(True)
	Gui.ActiveDocument.ActiveView.setAxisCross(True)
	Gui.SendMsgToActiveView("ViewFit")

	print(f'convertToMesh={convertToMesh}, postprocess={postprocess}')

	print('---> RCD parameters used:')
	for params in RCD_parameter_list:
		print(params)

	print('type(RCD_truncated)', type(RCD_truncated))
	print('RCD_truncated.Shape:', RCD_truncated.Shape)
	print('RCD_truncated.Shape.Volume:', RCD_truncated.Shape.Volume)
	print('RCD_truncated.Shape.Area:', RCD_truncated.Shape.Area)

	###############################################################################
	FreeCAD.Console.PrintMessage("...DONE\n")
	# get the end time
	et = time.time()

	# get the execution time
	elapsed_time = et - st
	print('Execution time:', elapsed_time, 'seconds')

def getOption(title, label, items):
    # https://stackoverflow.com/questions/23273858/using-qt-pyside-to-get-user-input-with-qinputdialog
    app = QtWidgets.QApplication(sys.argv)
    gui = QtWidgets.QWidget()
    item, ok = QtWidgets.QInputDialog.getItem(gui, title, label, items, 0, False)
    app.exit()
    return item, ok

if __name__ == '__main__':
    #print(getOption('Crystal options', 'Choose an option:', ['RCD', 'FRD', 'double RCD']))
    main()
	# Testing:

	# reply = mychoicebox(["one", "two", "three"])
	# print("reply:", reply)
