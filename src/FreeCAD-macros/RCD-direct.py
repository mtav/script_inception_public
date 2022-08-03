from __future__ import division # allows floating point division from integers

import Part
from FreeCAD import Base

from math import sqrt, pi, sin, cos, asin
from numpy import array

FreeCAD.Console.PrintMessage("START...\n")

doc = FreeCAD.activeDocument()

#cubic_unit_cell_size = 50
cubic_unit_cell_size = 5 # scaling messes up boolean ops sometimes :(
L = sqrt(3)/4 * cubic_unit_cell_size
#R = 0.26 * cubic_unit_cell_size
R = 0.5
#R = 0.05 * cubic_unit_cell_size + 0.1
ball_radius = (0.1+0.05) * cubic_unit_cell_size
a = cubic_unit_cell_size
location = array([0,0,0])

offset_cylinders = False
FRD = False
#cyl_delta = 0.075 * cubic_unit_cell_size
cyl_delta = 0.1

u = array([1, 0, 0])
v = array([0, 1, 0])
w = array([0, 0, 1])

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

def RCDCubicUnitCell(i, j, k):
	unit_cell_location = i*u + j*v + k*w
	
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

def RCDCubicUnitCell_FRD(i, j, k):
	unit_cell_location = i*u + j*v + k*w

	t0_FRD = tetra_FRD(location + (unit_cell_location+array([1/4, 1/4, 1/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.0'.format(i,j,k))
	t1_FRD = tetra_FRD(location + (unit_cell_location+array([3/4, 3/4, 1/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.1'.format(i,j,k))
	t2_FRD = tetra_FRD(location + (unit_cell_location+array([3/4, 1/4, 3/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.2'.format(i,j,k))
	t3_FRD = tetra_FRD(location + (unit_cell_location+array([1/4, 3/4, 3/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.3'.format(i,j,k))

	f_FRD = App.activeDocument().addObject("Part::MultiFuse","Fusion")
	f_FRD.Shapes = [t0_FRD, t1_FRD, t2_FRD, t3_FRD]
	t0_FRD.ViewObject.Visibility=False
	t1_FRD.ViewObject.Visibility=False
	t2_FRD.ViewObject.Visibility=False
	t3_FRD.ViewObject.Visibility=False
	f_FRD.Label = 'cell.{}.{}.{}_FRD'.format(i+1,j+1,k+1)

	return(f_FRD)

def createRCD():
	L = []
	for i in range(-1, 2):
		for j in range(-1, 2):
			for k in range(-1, 2):
				U = RCDCubicUnitCell(i, j, k)
				L.append(U)
	RCD = App.activeDocument().addObject("Part::MultiFuse","Fusion")
	RCD.Shapes = L
	return(RCD)

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

#	App.activeDocument().Common.Shapes = [App.activeDocument().RCDpart,App.activeDocument().unitCube,]
#>>> Gui.activeDocument().RCDpart.Visibility=False
#>>> Gui.activeDocument().unitCube.Visibility=False

#	t2 = tetra(location + (array([1/2, 1/2, 1/2])+array([1/2, 0, -1/2]))*cubic_unit_cell_size, 't0')
#	t2 = tetra(location + (array([1/2, 1/2, 1/2])+array([1, 1/2, -1/2]))*cubic_unit_cell_size, 't0')

#	t2 = tetra(location + (array([1/2, 1/2, 1/2])+array([0, -1/2, -1/2]))*cubic_unit_cell_size, 't0')

	#main_RCD = RCDCubicUnitCell(0, 0, 0)
#	main_RCD = RCDCubicUnitCell_FRD(0, 0, 0)

	# X+ face
#	cyl0 = addCylinder(Base.Vector(1,   1/2,   0)*cubic_unit_cell_size,     [1, -1, 1], 'xplus-0')
#	cyl0 = addCylinder(Base.Vector(1,   1/2,   0)*cubic_unit_cell_size,     [1, -1, 1], 'xplus-0')
#	cyl1 = addCylinder(Base.Vector(1, 1/2, 1/2)*cubic_unit_cell_size,     [1,-1,-1], 'xplus-1')
#	cyl2 = addCylinder(Base.Vector(1, 1/2, 1/2)*cubic_unit_cell_size,     [1, 1, 1], 'xplus-2')
#	cyl3 = addCylinder(Base.Vector(1,   1,   1)*cubic_unit_cell_size,     [1,-1,-1], 'xplus-3')
#	xplus = App.activeDocument().addObject("Part::MultiFuse","xplus")
#	xplus.Shapes = [cyl0, cyl1, cyl2, cyl3]


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

for i in doc.Objects:
	doc.removeObject(i.Name)

#RCDCubicUnitCell_FRD(0, 0, 0)
createRCD()
#createDirectRCD()
#RCDCubicUnitCell(0, 0, 0)
#createInverseRCD()

#addSphere(Base.Vector(0.5,0.5,0.5)*cubic_unit_cell_size, 0.24*cubic_unit_cell_size)

#addCube(cubic_unit_cell_size, [0,0,0], 'unitCube')

createWireBox(2*cubic_unit_cell_size, 0.05*cubic_unit_cell_size)

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

FreeCAD.Console.PrintMessage("...DONE\n")
