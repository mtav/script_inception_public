#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import division
from FreeCAD import Base
import Part,PartGui
import box
import numpy
from numpy import array
import time

import utilities.ellipse

#default_MinorRadius = 0.20 # w_ell/2
#default_MajorRadius = 0.25*numpy.sqrt(3/2) # h_cyl_z/2

default_MinorRadius = 0.5*0.400 # w_ell/2
default_MajorRadius = 0.5*0.500 # D_cyl/2

#default_MinorRadius = 0.1 # w_ell/2
#default_MajorRadius = 0.1 # D_cyl/2

#default_MinorRadius = 0.26
#default_MajorRadius = 0.26*numpy.sqrt(3/2)

def addCylinder(tetra_position, direction, name, offset_cylinders = False, add_AABB=False, MinorRadius=default_MinorRadius, MajorRadius=default_MajorRadius, smooth_ends=False, tiltedEdges=True, smooth_A = False, smooth_B = False):
  
  # smooth_ends = True
  # smooth_A = False
  # smooth_B = False
  
  # .. todo: smooth only one end...
  
  # make sure that tetra_position is a FreeCAD.Vector
  tetra_position = FreeCAD.Vector(*tetra_position)
  
  rod_dir = FreeCAD.Vector(*direction)*(1/4)
  
  # # hack to reduce unnecessary smoothing:
  # smooth_ends = False
  # end_point = tetra_position + rod_dir
  # FreeCAD.Console.PrintMessage("start = {} end={}\n".format(tetra_position, end_point))
  # if end_point[0] in (-1/2, 1+1/2) or end_point[1] in (-1/2, 1+1/2) or end_point[2] in (-1/2, 1+1/2):
    # smooth_ends = True
  
  # FreeCAD.Console.PrintMessage("direction = {}\n".format(direction))
  rotation_centre = FreeCAD.Vector(0, 0, 0)
  
  # FreeCAD.Console.PrintMessage("MinorRadius = {}\n".format(MinorRadius))
  # FreeCAD.Console.PrintMessage("MajorRadius = {}\n".format(MajorRadius))
  # FreeCAD.Console.PrintMessage("2*MinorRadius = {}\n".format(2*MinorRadius))
  # FreeCAD.Console.PrintMessage("2*MajorRadius = {}\n".format(2*MajorRadius))
  rod_info = utilities.ellipse.EllipticalRod()
  rod_info.setEllipsoidWidth(2*MinorRadius)
  rod_info.setCylinderDiameterBig(2*MajorRadius)
  # rod_info.setEllipsoidWidth(1)
  # rod_info.setCylinderDiameterBig(1)
  #rod_info.setCylinderHeightZ(2*MajorRadius)
  # rod_info.setEllipsoidHeightZ(2*MajorRadius)
  #FreeCAD.Console.PrintMessage('{}\n'.format(rod_info))
  #rod_info.plot()
  
  rod_base = App.ActiveDocument.addObject("Part::Ellipse","Ellipse")
  rod_base.Label = '{}_base'.format(name)
  
  if not smooth_ends:
    
    # rod_base.MajorRadius = MajorRadius
    # rod_base.MinorRadius = MinorRadius
    rod_base.MajorRadius = 0.5*rod_info.getCylinderHeightZ()
    rod_base.MinorRadius = 0.5*rod_info.getEllipsoidWidth()
    
    ry_angle = 90
    rz_angle = numpy.degrees(numpy.arctan2(direction[1], direction[0]))
    
    ry = FreeCAD.Rotation(FreeCAD.Vector(0,1,0), ry_angle)
    rz = FreeCAD.Rotation(FreeCAD.Vector(0,0,1), rz_angle)
    
    rod_base.Placement = FreeCAD.Placement(tetra_position, rz.multiply(ry), rotation_centre)
    
  else:
    (cylinder_height_z, D_ell, D_cyl, (Xp, Yp), (Xm, Ym)) = rod_info.getInfo1()
    major_axis = numpy.array([Xp, Yp]) - numpy.array([Xm, Ym])
    
    major_radius = 0.5*numpy.linalg.norm(major_axis)
    minor_radius = 0.5*rod_info.getEllipsoidWidth()

    if major_radius < minor_radius:
      FreeCAD.Console.PrintMessage('major_radius <= minor_radius: {} <= {}\n'.format(major_radius, minor_radius))
    
    rod_base.MajorRadius = major_radius
    rod_base.MinorRadius = minor_radius
    
    ry_angle = 90
    rz_angle = numpy.degrees(numpy.arctan2(direction[1], direction[0]))
    
    ry = FreeCAD.Rotation(FreeCAD.Vector(0,1,0), ry_angle)
    rz = FreeCAD.Rotation(FreeCAD.Vector(0,0,1), rz_angle)
    
    # equivalent to [a,b,c] X [0,0,c], where direction=[a,b,c]
    minor_axis = FreeCAD.Vector(direction[1]*direction[2], -direction[0]*direction[2], 0)
    r_minor_axis_angle_deg = numpy.degrees(rod_info.getMajorAxisAngleWithRespectToVertical())
    r_minor_axis = FreeCAD.Rotation(minor_axis, r_minor_axis_angle_deg)
    
    rod_base.Placement = FreeCAD.Placement(tetra_position, r_minor_axis.multiply(rz.multiply(ry)), rotation_centre)

  # FreeCAD.Console.PrintMessage("rod_dir = {}, rz_angle = {}\n".format(rod_dir, rz_angle))
  # FreeCAD.Console.PrintMessage("ry = {}\n".format(ry))
  # FreeCAD.Console.PrintMessage("rz = {}\n".format(rz))
  # FreeCAD.Console.PrintMessage("tetra_position = {}\n".format(tetra_position))
  
  rod = App.ActiveDocument.addObject("Part::Extrusion","Extrude")
  rod.Base = rod_base
  rod.Dir = rod_dir
  rod.Solid = (True)
  rod_base.ViewObject.Visibility = False
  rod.Label = '{}-cyl'.format(name)
  
  rod_final = rod
  
  if smooth_ends:
    EllipsoidSmall1 = App.ActiveDocument.addObject("Part::Ellipsoid","Ellipsoid")
    EllipsoidSmall1.Radius1=rod_info.getEllipsoidHeightZ()/2
    EllipsoidSmall1.Radius2=rod_info.getEllipsoidWidth()/2
    EllipsoidSmall1.Radius3=rod_info.getEllipsoidWidth()/2
    EllipsoidSmall1.Placement=Base.Placement(tetra_position, Base.Rotation(0.0000,0.0000,0.0000,1.0000))
    EllipsoidSmall1.Label='EllipsoidSmall1'
    # EllipsoidSmall1.ViewObject.Visibility=False
    
    EllipsoidSmall2 = App.ActiveDocument.addObject("Part::Ellipsoid","Ellipsoid")
    EllipsoidSmall2.Radius1=rod_info.getEllipsoidHeightZ()/2
    EllipsoidSmall2.Radius2=rod_info.getEllipsoidWidth()/2
    EllipsoidSmall2.Radius3=rod_info.getEllipsoidWidth()/2
    EllipsoidSmall2.Placement=Base.Placement(tetra_position + rod_dir, Base.Rotation(0.0000,0.0000,0.0000,1.0000))
    EllipsoidSmall2.Label='EllipsoidSmall2'
    
    rod_final = App.activeDocument().addObject("Part::MultiFuse","rod_final")
    rod_final.Shapes = [rod, EllipsoidSmall1, EllipsoidSmall2]
    
  else:
    ellipsoid_list = []
    if smooth_A:
      EllipsoidBig1 = App.ActiveDocument.addObject("Part::Ellipsoid","Ellipsoid")
      EllipsoidBig1.Radius1=rod_info.getCylinderHeightZ()/2
      EllipsoidBig1.Radius2=rod_info.getEllipsoidWidth()/2
      EllipsoidBig1.Radius3=rod_info.getEllipsoidWidth()/2
      EllipsoidBig1.Placement=Base.Placement(tetra_position, Base.Rotation(0.0000,0.0000,0.0000,1.0000))
      EllipsoidBig1.Label='EllipsoidBig1'
      ellipsoid_list.append(EllipsoidBig1)
      
    if smooth_B:
      EllipsoidBig2 = App.ActiveDocument.addObject("Part::Ellipsoid","Ellipsoid")
      EllipsoidBig2.Radius1=rod_info.getCylinderHeightZ()/2
      EllipsoidBig2.Radius2=rod_info.getEllipsoidWidth()/2
      EllipsoidBig2.Radius3=rod_info.getEllipsoidWidth()/2
      EllipsoidBig2.Placement=Base.Placement(tetra_position + rod_dir, Base.Rotation(0.0000,0.0000,0.0000,1.0000))
      EllipsoidBig2.Label='EllipsoidBig2'
      ellipsoid_list.append(EllipsoidBig2)
    
    if len(ellipsoid_list) > 0:
      # .. todo:: BUG: figure out why the union of the objects is partially black. :(
      # .. todo:: export STL files are also wrong. cf: ~/Desktop/RCD-paper-ANONYMIZED-3/RCD-inverse-elliptical/0.4x0.5/FreeCAD-union-bug.png
      rod_final = App.activeDocument().addObject("Part::MultiFuse","rod_final")
      rod_final.Shapes = [rod] + ellipsoid_list
      # rod_final.Shapes = [EllipsoidBig1,rod,EllipsoidBig2]
    # group = App.ActiveDocument.addObject("App::DocumentObjectGroup", "EllipticalRod")
    # group.addObject(rod)
    # group.addObject(EllipsoidSmall1)
    # group.addObject(EllipsoidSmall2)
  
  rod_final.Label = name
  
  return(rod_final)

def tetra(location, name, smooth_ends=False, MinorRadius=default_MinorRadius, MajorRadius=default_MajorRadius):
  dir0 = [-1,-1,-1]
  dir1 = [1, 1,-1]
  dir2 = [1,-1,1]
  dir3 = [-1,1,1]
  cyl0 = addCylinder(location, dir0, name+'_cyl0', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
  cyl1 = addCylinder(location, dir1, name+'_cyl1', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
  cyl2 = addCylinder(location, dir2, name+'_cyl2', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
  cyl3 = addCylinder(location, dir3, name+'_cyl3', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
  f = App.activeDocument().addObject("Part::MultiFuse","Fusion")
  f.Shapes = [cyl0, cyl1, cyl2, cyl3]
  f.Label = name
  cyl0.ViewObject.Visibility=False
  cyl1.ViewObject.Visibility=False
  cyl2.ViewObject.Visibility=False
  cyl3.ViewObject.Visibility=False
  return(f)

def makeTetra(tetra_position):
  raise
  
  MinorRadius = 0.2
  MajorRadius = 0.25*numpy.sqrt(3/2)

  rotation_centre = FreeCAD.Vector(0, 0, 0)
  
  tetra_label = 'tetra-{:.3f}-{:.3f}-{:.3f}'.format(*tetra_position)

  rod0 = addCylinder(tetra_position, [-1,-1,-1], tetra_label+'-rod0', MinorRadius=MinorRadius, MajorRadius=MajorRadius)
  rod1 = addCylinder(tetra_position, [-1, 1, 1], tetra_label+'-rod1', MinorRadius=MinorRadius, MajorRadius=MajorRadius)
  rod2 = addCylinder(tetra_position, [ 1,-1, 1], tetra_label+'-rod2', MinorRadius=MinorRadius, MajorRadius=MajorRadius)
  rod3 = addCylinder(tetra_position, [ 1, 1,-1], tetra_label+'-rod3', MinorRadius=MinorRadius, MajorRadius=MajorRadius)
  
  tetra = App.activeDocument().addObject("Part::MultiFuse","RCDpart")
  tetra.Shapes = [rod0, rod1, rod2, rod3]
  tetra.Label = tetra_label

  return(tetra)

def elliptical_RCDCubicUnitCell(i, j, k, shifted=False):
  raise
  
  position = FreeCAD.Vector(i, j, k)

  if shifted:
    t0 = makeTetra(position + FreeCAD.Vector(3/4, 1/4, 1/4))
    t1 = makeTetra(position + FreeCAD.Vector(1/4, 3/4, 1/4))
    t2 = makeTetra(position + FreeCAD.Vector(1/4, 1/4, 3/4))
    t3 = makeTetra(position + FreeCAD.Vector(3/4, 3/4, 3/4))
  else:
    t0 = makeTetra(position + FreeCAD.Vector(1/4, 1/4, 1/4))
    t1 = makeTetra(position + FreeCAD.Vector(3/4, 3/4, 1/4))
    t2 = makeTetra(position + FreeCAD.Vector(3/4, 1/4, 3/4))
    t3 = makeTetra(position + FreeCAD.Vector(1/4, 3/4, 3/4))
  
  f = App.activeDocument().addObject("Part::MultiFuse","Fusion")
  f.Shapes = [t0, t1, t2, t3]
  t0.ViewObject.Visibility = False
  t1.ViewObject.Visibility = False
  t2.ViewObject.Visibility = False
  t3.ViewObject.Visibility = False
  
  f.Label = 'cell.{}.{}.{}'.format(i+1,j+1,k+1)
  
  return(f)

#>>> App.ActiveDocument.Ellipse.Angle0=0.0000
#>>> App.ActiveDocument.Ellipse.Angle1=360.0000
# 1,1,1 direction:
#App.ActiveDocument.Ellipse.Placement=Base.Placement(Base.Vector(0.0000,0.0000,0.0000),Base.Rotation(0.0600,0.4558,0.7046,0.5406))
# 1,1,0 direction:
#  App.ActiveDocument.Ellipse.Placement=Base.Placement(Base.Vector(0.0000,0.0000,0.0000),Base.Rotation(0.2706,0.6533,0.6533,0.2706))
#  App.ActiveDocument.Ellipse.Label='Ellipse'
#>>> 
#>>> App.ActiveDocument.recompute()
#>>> Gui.SendMsgToActiveView("ViewFit")
#>>> Gui.ActiveDocument.ActiveView.setAxisCross(True)
#>>> FreeCAD.getDocument("Unnamed").addObject("Part::Extrusion","Extrude")
#>>> FreeCAD.getDocument("Unnamed").Extrude.Base = FreeCAD.getDocument("Unnamed").Ellipse
#>>> FreeCAD.getDocument("Unnamed").Extrude.Dir = (1,1,1)
#>>> FreeCAD.getDocument("Unnamed").Extrude.Solid = (True)
#>>> FreeCAD.getDocument("Unnamed").Extrude.TaperAngle = (0)
#>>> FreeCADGui.getDocument("Unnamed").Ellipse.Visibility = False
#>>> FreeCAD.getDocument("Unnamed").Extrude.Label = 'Extrude'
#>>> 
#>>> Gui.ActiveDocument.Extrude.ShapeColor=Gui.ActiveDocument.Ellipse.ShapeColor
#>>> Gui.ActiveDocument.Extrude.LineColor=Gui.ActiveDocument.Ellipse.LineColor
#>>> Gui.ActiveDocument.Extrude.PointColor=Gui.ActiveDocument.Ellipse.PointColor
#>>> 
  return

def RCDCubicUnitCell(i, j, k, shifted=False, g_location=[0,0,0], cubic_unit_cell_size=1, smooth_ends=False, MinorRadius=default_MinorRadius, MajorRadius=default_MajorRadius):
  u = numpy.array([1, 0, 0])
  v = numpy.array([0, 1, 0])
  w = numpy.array([0, 0, 1])
  
  unit_cell_location = i*u + j*v + k*w
  g_location = numpy.array(g_location)
  
  if shifted:
    t0 = tetra(g_location + (unit_cell_location+array([3/4, 1/4, 1/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.0'.format(i,j,k), smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    t1 = tetra(g_location + (unit_cell_location+array([1/4, 3/4, 1/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.1'.format(i,j,k), smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    t2 = tetra(g_location + (unit_cell_location+array([1/4, 1/4, 3/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.2'.format(i,j,k), smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    t3 = tetra(g_location + (unit_cell_location+array([3/4, 3/4, 3/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.3'.format(i,j,k), smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
  else:
    t0 = tetra(g_location + (unit_cell_location+array([1/4, 1/4, 1/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.0'.format(i,j,k), smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    t1 = tetra(g_location + (unit_cell_location+array([3/4, 3/4, 1/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.1'.format(i,j,k), smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    t2 = tetra(g_location + (unit_cell_location+array([3/4, 1/4, 3/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.2'.format(i,j,k), smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    t3 = tetra(g_location + (unit_cell_location+array([1/4, 3/4, 3/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.3'.format(i,j,k), smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)

  f = App.activeDocument().addObject("Part::MultiFuse","Fusion")
  f.Shapes = [t0, t1, t2, t3]
  t0.ViewObject.Visibility = False
  t1.ViewObject.Visibility = False
  t2.ViewObject.Visibility = False
  t3.ViewObject.Visibility = False
  f.Label = 'cell.{}.{}.{}'.format(i+1,j+1,k+1)

  return(f)

def createInverseRCD_cut(shifted=False, FRD=False, cubic_unit_cell_size=1, smooth_ends=False, MinorRadius=default_MinorRadius, MajorRadius=default_MajorRadius):
  main_RCD = RCDCubicUnitCell(0, 0, 0, shifted=shifted, smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)

  if FRD:
    main_FRD = RCDCubicUnitCell_FRD(0, 0, 0, smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)

  if shifted:
    # X+ face: 8
    cyl0 = addCylinder(Base.Vector(1, 0, 1/2)*cubic_unit_cell_size,     [1, 1, 1], 'xplus-0', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl1 = addCylinder(Base.Vector(1, 0, 1/2)*cubic_unit_cell_size,     [1,-1,-1], 'xplus-1', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl2 = addCylinder(Base.Vector(1, 1/2, 1)*cubic_unit_cell_size,     [1, 1, 1], 'xplus-2', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl3 = addCylinder(Base.Vector(1, 1/2, 1)*cubic_unit_cell_size,     [1,-1,-1], 'xplus-3', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl4 = addCylinder(Base.Vector(1, 1/2, 0)*cubic_unit_cell_size,     [1, 1, 1], 'xplus-4', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl5 = addCylinder(Base.Vector(1, 1/2, 0)*cubic_unit_cell_size,     [1,-1,-1], 'xplus-5', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl6 = addCylinder(Base.Vector(1, 1, 1/2)*cubic_unit_cell_size,     [1, 1, 1], 'xplus-6', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl7 = addCylinder(Base.Vector(1, 1, 1/2)*cubic_unit_cell_size,     [1,-1,-1], 'xplus-7', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    xplus = App.activeDocument().addObject("Part::MultiFuse","xplus")
    xplus.Shapes = [cyl0, cyl1, cyl2, cyl3, cyl4, cyl5, cyl6, cyl7]

    # X- face: 8
    cyl0 = addCylinder(Base.Vector(0,   1, 1/2)*cubic_unit_cell_size,     [-1, 1, -1], 'xminus-0', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl1 = addCylinder(Base.Vector(0,   1, 1/2)*cubic_unit_cell_size,     [-1, -1, 1], 'xminus-1', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl2 = addCylinder(Base.Vector(0, 1/2,   1)*cubic_unit_cell_size,     [-1, 1, -1], 'xminus-2', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl3 = addCylinder(Base.Vector(0, 1/2,   1)*cubic_unit_cell_size,     [-1, -1, 1], 'xminus-3', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl4 = addCylinder(Base.Vector(0, 1/2, 0)*cubic_unit_cell_size,     [-1, 1, -1], 'xminus-4', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl5 = addCylinder(Base.Vector(0, 1/2, 0)*cubic_unit_cell_size,     [-1, -1, 1], 'xminus-5', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl6 = addCylinder(Base.Vector(0, 0, 1/2)*cubic_unit_cell_size,     [-1, 1, -1], 'xminus-6', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl7 = addCylinder(Base.Vector(0, 0, 1/2)*cubic_unit_cell_size,     [-1, -1, 1], 'xminus-7', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    xminus = App.activeDocument().addObject("Part::MultiFuse","xminus")
    xminus.Shapes = [cyl0, cyl1, cyl2, cyl3, cyl4, cyl5, cyl6, cyl7]

    ## Y+ face: 6
    cyl0 = addCylinder(Base.Vector(1/2,   1, 0)*cubic_unit_cell_size,     [ 1,  1,  1], 'yplus-0', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl1 = addCylinder(Base.Vector(1/2,   1, 0)*cubic_unit_cell_size,     [-1,  1, -1], 'yplus-1', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl2 = addCylinder(Base.Vector(  1,   1,   1/2)*cubic_unit_cell_size,     [-1,  1, -1], 'yplus-2', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl3 = addCylinder(Base.Vector(1/2,   1, 1)*cubic_unit_cell_size,     [ 1,  1,  1], 'yplus-3', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl4 = addCylinder(Base.Vector(1/2,   1, 1)*cubic_unit_cell_size,     [-1,  1, -1], 'yplus-4', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl5 = addCylinder(Base.Vector(  0,   1,   1/2)*cubic_unit_cell_size,     [1,  1, 1], 'yplus-5', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    yplus = App.activeDocument().addObject("Part::MultiFuse","yplus")
    yplus.Shapes = [cyl0, cyl1, cyl2, cyl3, cyl4, cyl5]
    
    ## Y- face: 6
    cyl0 = addCylinder(Base.Vector(1/2,   0,    0)*cubic_unit_cell_size,    [ 1, -1, -1], 'yminus-0', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl1 = addCylinder(Base.Vector(1/2,   0,    0)*cubic_unit_cell_size,    [-1, -1,  1], 'yminus-1', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl2 = addCylinder(Base.Vector(0,   0,    1/2)*cubic_unit_cell_size,    [ 1, -1, -1], 'yminus-2', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl3 = addCylinder(Base.Vector(1/2,   0,    1)*cubic_unit_cell_size,    [ 1, -1, -1], 'yminus-3', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl4 = addCylinder(Base.Vector(1/2,   0,    1)*cubic_unit_cell_size,    [-1, -1,  1], 'yminus-4', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl5 = addCylinder(Base.Vector(1,   0,    1/2)*cubic_unit_cell_size,    [-1, -1,  1], 'yminus-5', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    yminus = App.activeDocument().addObject("Part::MultiFuse","yminus")
    yminus.Shapes = [cyl0, cyl1, cyl2, cyl3, cyl4, cyl5]
    
    # Z+ face: 4
    cyl0 = addCylinder(Base.Vector(1/2, 0,   1)*cubic_unit_cell_size,     [ 1, 1, 1], 'zplus-0', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl1 = addCylinder(Base.Vector(1, 1/2, 1)*cubic_unit_cell_size,     [-1,-1, 1], 'zplus-1', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl2 = addCylinder(Base.Vector(0, 1/2,   1)*cubic_unit_cell_size,     [ 1, 1, 1], 'zplus-2', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl3 = addCylinder(Base.Vector(1/2, 1, 1)*cubic_unit_cell_size,     [-1,-1, 1], 'zplus-3', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    zplus = App.activeDocument().addObject("Part::MultiFuse","zplus")
    zplus.Shapes = [cyl0, cyl1, cyl2, cyl3]
    
    # Z- face: 4
    cyl0 = addCylinder(Base.Vector(1/2,   0, 0)*cubic_unit_cell_size,     [ -1,1,-1], 'zminus-0', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl1 = addCylinder(Base.Vector(0, 1/2, 0)*cubic_unit_cell_size,     [1, -1,-1], 'zminus-1', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl2 = addCylinder(Base.Vector(1,   1/2, 0)*cubic_unit_cell_size,     [ -1,1,-1], 'zminus-2', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl3 = addCylinder(Base.Vector(1/2, 1, 0)*cubic_unit_cell_size,     [1, -1,-1], 'zminus-3', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    zminus = App.activeDocument().addObject("Part::MultiFuse","zminus")
    zminus.Shapes = [cyl0, cyl1, cyl2, cyl3]
  else:
    # X+ face
    cyl0 = addCylinder(Base.Vector(1,   0,   0)*cubic_unit_cell_size,     [1, 1, 1], 'xplus-0', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl1 = addCylinder(Base.Vector(1, 1/2, 1/2)*cubic_unit_cell_size,     [1,-1,-1], 'xplus-1', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl2 = addCylinder(Base.Vector(1, 1/2, 1/2)*cubic_unit_cell_size,     [1, 1, 1], 'xplus-2', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl3 = addCylinder(Base.Vector(1,   1,   1)*cubic_unit_cell_size,     [1,-1,-1], 'xplus-3', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    xplus = App.activeDocument().addObject("Part::MultiFuse","xplus")
    xplus.Shapes = [cyl0, cyl1, cyl2, cyl3]
    
    # X- face
    cyl0 = addCylinder(Base.Vector(0,   0,   1)*cubic_unit_cell_size,     [-1, 1, -1], 'xminus-0', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl1 = addCylinder(Base.Vector(0, 1/2, 1/2)*cubic_unit_cell_size,     [-1, -1, 1], 'xminus-1', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl2 = addCylinder(Base.Vector(0, 1/2, 1/2)*cubic_unit_cell_size,     [-1, 1, -1], 'xminus-2', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl3 = addCylinder(Base.Vector(0,   1,   0)*cubic_unit_cell_size,     [-1, -1, 1], 'xminus-3', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    xminus = App.activeDocument().addObject("Part::MultiFuse","xminus")
    xminus.Shapes = [cyl0, cyl1, cyl2, cyl3]
    
    # Y+ face
    cyl0 = addCylinder(Base.Vector(  0,   1,   0)*cubic_unit_cell_size,     [ 1,  1,  1], 'yplus-0', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl1 = addCylinder(Base.Vector(1/2,   1, 1/2)*cubic_unit_cell_size,     [-1,  1, -1], 'yplus-1', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl2 = addCylinder(Base.Vector(1/2,   1, 1/2)*cubic_unit_cell_size,     [ 1,  1,  1], 'yplus-2', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl3 = addCylinder(Base.Vector(  1,   1,   1)*cubic_unit_cell_size,     [-1,  1, -1], 'yplus-3', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    yplus = App.activeDocument().addObject("Part::MultiFuse","yplus")
    yplus.Shapes = [cyl0, cyl1, cyl2, cyl3]
    
    # Y- face
    cyl0 = addCylinder(Base.Vector(  0,   0,    1)*cubic_unit_cell_size,    [ 1, -1, -1], 'yminus-0', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl1 = addCylinder(Base.Vector(1/2,   0,  1/2)*cubic_unit_cell_size,    [-1, -1,  1], 'yminus-1', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl2 = addCylinder(Base.Vector(1/2,   0,  1/2)*cubic_unit_cell_size,    [ 1, -1, -1], 'yminus-2', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl3 = addCylinder(Base.Vector(  1,   0,    0)*cubic_unit_cell_size,    [-1, -1,  1], 'yminus-3', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    yminus = App.activeDocument().addObject("Part::MultiFuse","yminus")
    yminus.Shapes = [cyl0, cyl1, cyl2, cyl3]
    
    # Z+ face
    cyl0 = addCylinder(Base.Vector(  0, 0,   1)*cubic_unit_cell_size,     [ 1, 1, 1], 'zplus-0', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl1 = addCylinder(Base.Vector(1/2, 1/2, 1)*cubic_unit_cell_size,     [-1,-1, 1], 'zplus-1', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl2 = addCylinder(Base.Vector(1/2, 1/2, 1)*cubic_unit_cell_size,     [ 1, 1, 1], 'zplus-2', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl3 = addCylinder(Base.Vector(  1, 1,   1)*cubic_unit_cell_size,     [-1,-1, 1], 'zplus-3', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    zplus = App.activeDocument().addObject("Part::MultiFuse","zplus")
    zplus.Shapes = [cyl0, cyl1, cyl2, cyl3]
    
    # Z- face
    cyl0 = addCylinder(Base.Vector(  0,   1, 0)*cubic_unit_cell_size,     [ 1,-1,-1], 'zminus-0', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl1 = addCylinder(Base.Vector(1/2, 1/2, 0)*cubic_unit_cell_size,     [-1, 1,-1], 'zminus-1', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl2 = addCylinder(Base.Vector(1/2, 1/2, 0)*cubic_unit_cell_size,     [ 1,-1,-1], 'zminus-2', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    cyl3 = addCylinder(Base.Vector(  1,   0, 0)*cubic_unit_cell_size,     [-1, 1,-1], 'zminus-3', smooth_ends=smooth_ends, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
    zminus = App.activeDocument().addObject("Part::MultiFuse","zminus")
    zminus.Shapes = [cyl0, cyl1, cyl2, cyl3]
  
  cut = App.activeDocument().addObject("Part::MultiFuse","cut")
  cut.Shapes = [main_RCD, xplus, xminus, yplus, yminus, zplus, zminus]
  
  return cut

def createInverseRCD(shifted=False, FRD=False, cubic_unit_cell_size=1, create_RCD_cube_intersection=False, MinorRadius=default_MinorRadius, MajorRadius=default_MajorRadius):
  
  cut = createInverseRCD_cut(shifted=shifted, FRD=FRD, cubic_unit_cell_size=cubic_unit_cell_size, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
  
  cube_location = [0,0,0]
  #cube_location = [0.25,0.25,0.25]
  
  unitCube = box.addCube(cubic_unit_cell_size, cube_location, 'unitCube')
  
  RCD_inverse = App.activeDocument().addObject("Part::Cut","RCD_inverse")
  RCD_inverse.Base = unitCube
  RCD_inverse.Tool = cut
  
  if create_RCD_cube_intersection:
    RCD_cube_intersection = App.activeDocument().addObject("Part::MultiCommon","RCD_cube_intersection")
    RCD_cube_intersection.Shapes = [unitCube, cut]
  return RCD_inverse

def tetra_volume(smooth_ends=True, MinorRadius=default_MinorRadius, MajorRadius=default_MajorRadius):
  FreeCAD.Console.PrintMessage("===> tetra_volume called\n")
  tetra_list = []
  tetra_list_inner = []
  tetra_list_outer = []
  Nx = 0
  Ny = 2
  Nz = 2
  for i in range(-1, Nx+1):
    for j in range(-1, Ny+1):
      for k in range(-1, Nz+1):
        FreeCAD.Console.PrintMessage("{},{},{}\n".format(i,j,k))
        if (i%2, j%2, k%2) == (0,0,0) or (i%2, j%2, k%2) == (1,1,0) or (i%2, j%2, k%2) == (0,1,1) or (i%2, j%2, k%2) == (1,0,1):
          loc = (i/2+1/4, j/2+1/4, k/2+1/4)
          # s = App.ActiveDocument.addObject("Part::Sphere","Sphere")
          # s.Placement = App.Placement(App.Vector(*loc),App.Rotation(App.Vector(0,0,1),0))
          # s.Radius = 0.1
          if i in (-1, Nx) or j in (-1, Ny) or k in (-1, Nz):
            s = True
          else:
            s = False
          # if s:
          # s = False
          t = tetra(loc, 'tetra-{}'.format(loc), smooth_ends=s, MinorRadius=MinorRadius, MajorRadius=MajorRadius)
          if s:
            tetra_list_outer.append(t)
          else:
            tetra_list_inner.append(t)
          tetra_list.append(t)
  
  obj = None
  if len(tetra_list_inner) > 0:
    FreeCAD.Console.PrintMessage("===> tetra_volume fusing tetras inner\n")
    obj_inner = App.activeDocument().addObject("Part::MultiFuse","tetra_volume_inner")
    obj_inner.Shapes = tetra_list_inner
  
  if len(tetra_list_outer) > 0:
    FreeCAD.Console.PrintMessage("===> tetra_volume fusing tetras outer\n")
    obj_outer = App.activeDocument().addObject("Part::MultiFuse","tetra_volume_outer")
    obj_outer.Shapes = tetra_list_outer
  
  FreeCAD.Console.PrintMessage("===> tetra_volume fusing tetras all\n")
  tetra_volume = App.activeDocument().addObject("Part::MultiFuse","tetra_volume")
  tetra_volume.Shapes = tetra_list # [obj_inner, obj_outer]
  
  # selection_box = box.addAABB([-1/4, -1/4, -1/4], [1/2, 1+1/4, 1+1/4], name='box')
  unitCube = box.addAABB([0,0,0], [1,1,1], name='unitCube')
  
  # RCD_cube_intersection = App.activeDocument().addObject("Part::MultiCommon","RCD_cube_intersection")
  # RCD_cube_intersection.Shapes = [unitCube, tetra_volume]
  
  FreeCAD.Console.PrintMessage("===> tetra_volume done\n")
  return obj

def createSpecialSacrificialLayer(smooth_ends=True):
  '''
  .. todo:: Use modulo 2 system to enable/disable adding tetras in sub-blocks. i.e. create a function to fill a specific 1/2-integer volume with tetras.
  .. todo:: Blender addon to do just that? (+ maybe with tetra rotation for more FRD madness?)
  '''
  xplus_1 = tetra([1+1/4, 1/4, 1/4], 'tetra-xplus-1', smooth_ends=smooth_ends)
  xplus_2 = tetra([1+1/4, 3/4, 3/4], 'tetra-xplus-2', smooth_ends=smooth_ends)
  xplus = App.activeDocument().addObject("Part::MultiFuse","xplus")
  xplus.Shapes = [xplus_1, xplus_2]
    
  xminus_1 = tetra([0-1/4, 3/4, 1/4], 'tetra-xminus-1', smooth_ends=smooth_ends)
  xminus_2 = tetra([0-1/4, 1/4, 3/4], 'tetra-xminus-2', smooth_ends=smooth_ends)
  xminus = App.activeDocument().addObject("Part::MultiFuse","xminus")
  xminus.Shapes = [xminus_1, xminus_2]
  
  yplus_1 = tetra([1/4, 1+1/4, 1/4], 'tetra-yplus-1', smooth_ends=smooth_ends)
  yplus_2 = tetra([3/4, 1+1/4, 3/4], 'tetra-yplus-2', smooth_ends=smooth_ends)
  yplus = App.activeDocument().addObject("Part::MultiFuse","yplus")
  yplus.Shapes = [yplus_1, yplus_2]
  
  yminus_1 = tetra([3/4, 0-1/4, 1/4], 'tetra-yminus-1', smooth_ends=smooth_ends)
  yminus_2 = tetra([1/4, 0-1/4, 3/4], 'tetra-yminus-2', smooth_ends=smooth_ends)
  yminus = App.activeDocument().addObject("Part::MultiFuse","yminus")
  yminus.Shapes = [yminus_1, yminus_2]
  
  zplus_1 = tetra([1/4, 1/4, 1+1/4], 'tetra-zplus-1', smooth_ends=smooth_ends)
  zplus_2 = tetra([3/4, 3/4, 1+1/4], 'tetra-zplus-2', smooth_ends=smooth_ends)
  zplus = App.activeDocument().addObject("Part::MultiFuse","zplus")
  zplus.Shapes = [zplus_1, zplus_2]
  
  zminus_1 = tetra([3/4, 1/4, 0-1/4], 'tetra-zminus-1', smooth_ends=smooth_ends)
  zminus_2 = tetra([1/4, 3/4, 0-1/4], 'tetra-zminus-2', smooth_ends=smooth_ends)
  zminus = App.activeDocument().addObject("Part::MultiFuse","zminus")
  zminus.Shapes = [zminus_1, zminus_2]
  
  return

# Center,

    # makeCylinder(radius,height,[pnt,dir,angle]) -- Make a cylinder with a given radius and height
# class GeomEllipse(GeomCurve)
 # |  Describes an ellipse in 3D space
 # |  To create an ellipse there are several ways:
 # |  Part.Ellipse()
 # |          Creates an ellipse with major radius 2 and minor radius 1 with the
 # |          center in (0,0,0)
 # |  
 # |  Part.Ellipse(Ellipse)
 # |          Create a copy of the given ellipse
 # |  
 # |  Part.Ellipse(S1,S2,Center)
 # |          Creates an ellipse centered on the point Center, where
 # |          the plane of the ellipse is defined by Center, S1 and S2,
 # |          its major axis is defined by Center and S1,
 # |          its major radius is the distance between Center and S1, and
 # |          its minor radius is the distance between S2 and the major axis.
 # |  
 # |  Part.Ellipse(Center,MajorRadius,MinorRadius)
 # |          Creates an ellipse with major and minor radii MajorRadius and
 # |          MinorRadius, and located in the plane defined by Center and
 # |          the normal (0,0,1)
 # |  

# Gui.activateWorkbench("PartWorkbench")
#>>> App.newDocument("Unnamed")
#>>> App.setActiveDocument("Unnamed")
#>>> App.ActiveDocument=App.getDocument("Unnamed")
#>>> Gui.ActiveDocument=Gui.getDocument("Unnamed")
#>>> from FreeCAD import Base
#>>> import Part,PartGui
#>>> App.ActiveDocument.addObject("Part::Ellipse","Ellipse")
#>>> App.ActiveDocument.Ellipse.MajorRadius=4.0000
#>>> App.ActiveDocument.Ellipse.MinorRadius=2.0000
#>>> App.ActiveDocument.Ellipse.Angle0=0.0000
#>>> App.ActiveDocument.Ellipse.Angle1=360.0000
#>>> App.ActiveDocument.Ellipse.Placement=Base.Placement(Base.Vector(0.0000,0.0000,0.0000),Base.Rotation(0.0600,0.4558,0.7046,0.5406))
#>>> App.ActiveDocument.Ellipse.Label='Ellipse'
#>>> 
#>>> App.ActiveDocument.recompute()
#>>> Gui.SendMsgToActiveView("ViewFit")
#>>> Gui.ActiveDocument.ActiveView.setAxisCross(True)
#>>> FreeCAD.getDocument("Unnamed").addObject("Part::Extrusion","Extrude")
#>>> FreeCAD.getDocument("Unnamed").Extrude.Base = FreeCAD.getDocument("Unnamed").Ellipse
#>>> FreeCAD.getDocument("Unnamed").Extrude.Dir = (1,1,1)
#>>> FreeCAD.getDocument("Unnamed").Extrude.Solid = (True)
#>>> FreeCAD.getDocument("Unnamed").Extrude.TaperAngle = (0)
#>>> FreeCADGui.getDocument("Unnamed").Ellipse.Visibility = False
#>>> FreeCAD.getDocument("Unnamed").Extrude.Label = 'Extrude'
#>>> 
#>>> Gui.ActiveDocument.Extrude.ShapeColor=Gui.ActiveDocument.Ellipse.ShapeColor
#>>> Gui.ActiveDocument.Extrude.LineColor=Gui.ActiveDocument.Ellipse.LineColor
#>>> Gui.ActiveDocument.Extrude.PointColor=Gui.ActiveDocument.Ellipse.PointColor
#>>> 

def main1():
  
  object_list = []
  for i in [0,1]:
    for j in [0]:
      for k in [0]:
        cell = elliptical_RCDCubicUnitCell(i,j,k, shifted=False)
        object_list.append(cell)
  RCD = App.activeDocument().addObject("Part::MultiFuse","Fusion")
  RCD.Shapes = object_list
  RCD.Label = 'RCD'

  #RCD = elliptical_RCDCubicUnitCell(0,0,0)
  #elliptical_RCDCubicUnitCell(FreeCAD.Vector(1,0,0))
  #elliptical_RCDCubicUnitCell(FreeCAD.Vector(0,1,0))
  #elliptical_RCDCubicUnitCell(FreeCAD.Vector(0,0,1))

  unit_cube = box.addBox([0,0,0], [1,1,1], name='unit_cube', locationIsLower=True, wireframe=False)

  if False:
    cut = doc.addObject("Part::Cut","Cut")
    cut.Base = unit_cube
    cut.Tool = RCD
    unit_cube.ViewObject.Visibility=False
    RCD.ViewObject.Visibility=False

def makeTruncatedBits(coating):
  RCD_polymer = RCDCubicUnitCell(0, 0, 0, shifted=False, smooth_ends=True, MinorRadius=default_MinorRadius, MajorRadius=default_MajorRadius)
  RCD_coated = RCDCubicUnitCell(0, 0, 0, shifted=False, smooth_ends=True, MinorRadius=default_MinorRadius+coating, MajorRadius=default_MajorRadius+coating)
  
  RCD = App.activeDocument().addObject("Part::Cut","RCD_coating")
  RCD.Base = RCD_coated
  RCD.Tool = RCD_polymer
  
  unit_cell = box.addAABB([0,0,0], [1,1,1], name='unit_cell')
  box_xplus = box.addAABB([1,-1,-1], [2,2,2], name='box_xplus')
  box_yplus = box.addAABB([-1,1,-1], [2,2,2], name='box_yplus')
  box_xyplus = box.addAABB([1,1,-1], [2,2,2], name='box_xyplus')
  
  RCD_xplus = App.activeDocument().addObject("Part::Cut","RCD_xplus")
  RCD_xplus.Base = RCD
  RCD_xplus.Tool = box_xplus
  
  RCD_yplus = App.activeDocument().addObject("Part::Cut","RCD_yplus")
  RCD_yplus.Base = RCD
  RCD_yplus.Tool = box_yplus
  
  RCD_xyplus = App.activeDocument().addObject("Part::Cut","RCD_xyplus")
  RCD_xyplus.Base = RCD
  RCD_xyplus.Tool = box_xyplus
  return

def main2():
  FreeCAD.Console.PrintMessage("START...\n")
  start = time.time()

  doc = FreeCAD.activeDocument()
  if doc is None:
    App.newDocument("Unnamed")
    doc = FreeCAD.activeDocument()

  for i in doc.Objects:
    doc.removeObject(i.Name)
  
  # unitCube = box.addCube(1, [0,0,0], 'unitCube')
  # unitCube.ViewObject.DisplayMode = "Wireframe"
  
  # auto-smooth test
  # cyl0 = addCylinder([1/4+0, 1/4, 1/4], [-1,-1,-1], 'rod-smooth', smooth_ends=True, MinorRadius=default_MinorRadius, MajorRadius=default_MajorRadius, smooth_A = False, smooth_B = False)
  # cyl0 = addCylinder([1/4+1, 1/4, 1/4], [-1,-1,-1], 'rod-smooth', smooth_ends=True, MinorRadius=default_MinorRadius, MajorRadius=default_MajorRadius, smooth_A = False, smooth_B = True)
  # cyl0 = addCylinder([1/4+2, 1/4, 1/4], [-1,-1,-1], 'rod-smooth', smooth_ends=True, MinorRadius=default_MinorRadius, MajorRadius=default_MajorRadius, smooth_A = True, smooth_B = False)
  # cyl0 = addCylinder([1/4+3, 1/4, 1/4], [-1,-1,-1], 'rod-smooth', smooth_ends=True, MinorRadius=default_MinorRadius, MajorRadius=default_MajorRadius, smooth_A = True, smooth_B = True)
  # for i in range(-1, 3):
    # FreeCAD.Console.PrintMessage("{}\n".format(i))
    # cyl0 = addCylinder([i/2+1/4, 1/4, 1/4], [-1,-1,-1], 'rod-smooth', smooth_ends=True, MinorRadius=default_MinorRadius, MajorRadius=default_MajorRadius)
  
  # multiple radius test
  # coating = 0.16 # leaves some defecs when viewed in Blender
  # coating = 0.17 # leaves some defecs when viewed in Blender
  # coating = 0.20 # leaves some defecs when viewed in Blender
  coating = 0.21
  # cyl0 = addCylinder([0,0,0], [1,1,1], 'rod-smooth', smooth_ends=True, MinorRadius=default_MinorRadius, MajorRadius=default_MajorRadius)
  # cyl0 = addCylinder([0,0,0], [1,1,1], 'rod-smooth', smooth_ends=True, MinorRadius=default_MinorRadius+coating, MajorRadius=default_MajorRadius+coating)
  # # tetra([0,0,0], 'tetra-smooth', smooth_ends=True, MinorRadius=default_MinorRadius, MajorRadius=default_MajorRadius)
  # # tetra([0,0,0], 'tetra-smooth', smooth_ends=True, MinorRadius=default_MinorRadius+coating, MajorRadius=default_MajorRadius+coating)
  # RCD = RCDCubicUnitCell(0, 0, 0, shifted=False, smooth_ends=True, MinorRadius=default_MinorRadius, MajorRadius=default_MajorRadius)
  # RCDCubicUnitCell(0, 0, 0, shifted=False, smooth_ends=True, MinorRadius=default_MinorRadius+coating, MajorRadius=default_MajorRadius+coating)
  
  
  # tetra_volume()
  tetra_volume(smooth_ends=True, MinorRadius=default_MinorRadius, MajorRadius=default_MajorRadius)
  tetra_volume(smooth_ends=True, MinorRadius=default_MinorRadius+coating, MajorRadius=default_MajorRadius+coating)
  
  # polymer = tetra_volume(smooth_ends=True, MinorRadius=default_MinorRadius, MajorRadius=default_MajorRadius)
  # chalcogenide = tetra_volume(smooth_ends=True, MinorRadius=default_MinorRadius+coating, MajorRadius=default_MajorRadius+coating)

  # RCDCubicUnitCell(0, 0, 0, shifted=False, smooth_ends=True)
  #createSpecialSacrificialLayer()

  # createInverseRCD_cut(shifted=False, FRD=False, cubic_unit_cell_size=1, smooth_ends=False)
  # createInverseRCD_cut(shifted=False, FRD=False, cubic_unit_cell_size=1, smooth_ends=True)

  # createInverseRCD(shifted=True, create_RCD_cube_intersection=True)
  # createInverseRCD(shifted=False, create_RCD_cube_intersection=True)
  # for coating in numpy.linspace(0, 0.2, 5):
  # for coating in numpy.linspace(0.15, 0.2, 5):
  # for coating in numpy.linspace(0.15, 0.1625, 5):
  # for coating in [0.15, 0.16]:
    # RCD_inverse = createInverseRCD(shifted=False, create_RCD_cube_intersection=False, MinorRadius=default_MinorRadius+coating, MajorRadius=default_MajorRadius+coating)
    # RCD_inverse.Label = 'coating_{}'.format(coating)

  # cyl0 = addCylinder([0,0,0], [1,1,1], 'rod', smooth_ends=False)
  # cyl0 = addCylinder([0,0,0], [1,1,1], 'rod-smooth', smooth_ends=True)
  # # makeTetra([0,0,0])
  # tetra([0,0,0], 'tetra', smooth_ends=False)
  # tetra([0,0,0], 'tetra-smooth', smooth_ends=True)
  # RCDCubicUnitCell(0, 0, 0, shifted=False, smooth_ends=True)
  # RCDCubicUnitCell(0, 0, 0, shifted=True, smooth_ends=True)

  # cyl0 = addCylinder([0,0,0], [1,1,1], 'rod', smooth_ends=False)
  # cyl0 = addCylinder([0,0,0], [1,1,1], 'rod-default')
  # tetra([0,0,0], 'tetra-default')
  # RCDCubicUnitCell(0, 0, 0)

  FreeCAD.Console.PrintMessage("...recomputing... This can take a while...\n")
  doc.recompute()
  Gui.ActiveDocument.ActiveView.setAxisCross(True)
  Gui.SendMsgToActiveView("ViewFit")

  end = time.time()
  FreeCAD.Console.PrintMessage("Time: {} minutes\n".format((end - start)/60))
  FreeCAD.Console.PrintMessage("...DONE\n")

if __name__ == '__main__':
  main2()
#  rod_info = utilities.ellipse.EllipticalRod()
#  #rod_info.setEllipsoidWidth(2*MinorRadius)
#  #rod_info.setCylinderDiameterBig(2*MajorRadius)
#  rod_info.setEllipsoidWidth(1)
#  rod_info.setCylinderDiameterBig(1)
#  #rod_info.setCylinderHeightZ(2*MajorRadius)
#  # rod_info.setEllipsoidHeightZ(2*MajorRadius)
#  FreeCAD.Console.PrintMessage('{}\n'.format(rod_info))
#  rod_info.plot()
