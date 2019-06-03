#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
FreeCAD library to create various RCD-based structures.
'''

from __future__ import division

import box
import numpy
from utilities.geometry import getAABBCylinder, AABB_intersect, getAABBCylinder_loc_dir_len
from utilities.common import unitVector
from FreeCAD import Base

# TODO: turn into class shared by BFDTD, MEEP, FreeCAD, Blender, etc
class RCD():
  def __init__(self):
    self.cubic_unit_cell_size = 1
    self.g_cylinder_radius = 0.26 * self.cubic_unit_cell_size
    self.g_cylinder_length = numpy.sqrt(3)/4 * self.cubic_unit_cell_size
    self.doc = FreeCAD.activeDocument()
    return
  
  def createInverseRCD_at_location(self, unitcell_centro, shifted=False):

    group = App.ActiveDocument.addObject("App::DocumentObjectGroup", "InverseRCD.{}.{:.3f}.{:.3f}.{:.3f}".format(shifted, *unitcell_centro))
    
    unitCube = box.addCube_centre_size(unitcell_centro, name='unitCube')
    unitCube.ViewObject.DisplayMode = "Wireframe"
    
    group.addObject(unitCube)

    unitcell_centro = numpy.array(unitcell_centro)
    i_min = int(numpy.floor(unitcell_centro[0]-0.5))-1
    i_max = int(numpy.ceil(unitcell_centro[0]+0.5))+1
    j_min = int(numpy.floor(unitcell_centro[1]-0.5))-1
    j_max = int(numpy.ceil(unitcell_centro[1]+0.5))+1
    k_min = int(numpy.floor(unitcell_centro[2]-0.5))-1
    k_max = int(numpy.ceil(unitcell_centro[2]+0.5))+1

    AABB = box.addAABB([i_min,j_min,k_min], [i_max,j_max,k_max])
    group.addObject(AABB)

    grid = box.createGrid([i_min,j_min,k_min], [i_max,j_max,k_max])
    group.addObject(grid)

    Nx = i_max - i_min
    Ny = j_max - j_min
    Nz = k_max - k_min
    cylinder_list = getCylinders_createRCD([i_min,j_min,k_min], [i_max,j_max,k_max], shifted=shifted)
    print('Nx*Ny*Nz*16 :', Nx*Ny*Nz*16)
    print('full:', len(cylinder_list))
    #print('Creating full...')
    #full = createCylinders(cylinder_list, 'full', add_AABB=False)
    #full.ViewObject.Visibility = False
    
    cylinder_list_new = self.filterCylinders(cylinder_list, [1,1,1], unitcell_centro, locationIsStartPoint=False)
    #print(cylinder_list_new)
    print('filtered:', len(cylinder_list_new))
    print('Creating filtered...')
    filtered = self.createCylinders(cylinder_list_new, 'filtered')
    group.addObject(filtered)
    
    #cut = App.activeDocument().addObject("Part::MultiFuse","cut")
    #cut.Shapes = [main_RCD, xplus, xminus, yplus, yminus, zplus, zminus]
    
    #cube_location = [0,0,0]
    #cube_location = [0.25,0.25,0.25]
    
    #unitCube = box.addCube(cubic_unit_cell_size, cube_location, 'unitCube')
    
    RCD_inverse = App.activeDocument().addObject("Part::Cut","RCD_inverse")
    RCD_inverse.Base = unitCube
    RCD_inverse.Tool = filtered
    group.addObject(RCD_inverse)
    
    return
  
  def addCylinder(self, loc, direction, name, offset_cylinders = False, add_AABB=False):
    #print(loc, direction, name)
    #raise
    # normal cylinder: s|---------|
    # offset cylinder: s   |---|
    x = direction[0]
    y = direction[1]
    z = direction[2]
    u = Base.Vector(x,y,z).normalize()
    # makeCylinder ( radius, height,[pnt,direction,angle] )
    if offset_cylinders:
      cyl_shape = Part.makeCylinder(self.g_cylinder_radius, self.g_cylinder_length-2*cyl_delta, Base.Vector(loc[0],loc[1], loc[2]) + u*cyl_delta, u, 360)
    else:
      cyl_shape = Part.makeCylinder(self.g_cylinder_radius, self.g_cylinder_length, Base.Vector(loc[0],loc[1], loc[2]), u, 360)
    cyl_obj = self.doc.addObject("Part::Feature", name)
    cyl_obj.Shape = cyl_shape
    cyl_obj.ViewObject.DisplayMode = "Flat Lines"
    cyl_obj.Label = name
    
    if add_AABB:
      (minBB_cyl, maxBB_cyl) = getAABBCylinder_loc_dir_len(loc, direction, self.g_cylinder_length, self.g_cylinder_radius, locationIsStartPoint=True)
      addAABB(minBB_cyl, maxBB_cyl, '{}.AABB'.format(name))
    return(cyl_obj)
  
  def filterCylinders(self, cylinder_list, side_length_vec, block_location, locationIsStartPoint=True):

    block_location = numpy.array(block_location)
    side_length_vec = numpy.array(side_length_vec)

    if locationIsStartPoint:
      minBB_block = block_location
      maxBB_block = block_location + side_length_vec
    else:
      minBB_block = block_location - 0.5*side_length_vec
      maxBB_block = block_location + 0.5*side_length_vec
    
    cylinder_list_new = []
    for cyl_tuple in cylinder_list:
      cyl_loc, cyl_direction, cyl_name = cyl_tuple
      #u = unitVector(cyl_direction)
      #A = cyl_loc - (g_cylinder_length/2)*u
      #B = cyl_loc + (g_cylinder_length/2)*u
      #(minBB_cyl, maxBB_cyl) = getAABBCylinder(A, B, g_cylinder_radius)
      (minBB_cyl, maxBB_cyl) = getAABBCylinder_loc_dir_len(cyl_loc, cyl_direction, self.g_cylinder_length, self.g_cylinder_radius, locationIsStartPoint=True)

      if AABB_intersect(minBB_cyl, maxBB_cyl, minBB_block, maxBB_block):
        cylinder_list_new.append(cyl_tuple)
      #else:
        #print(minBB_block)
        #print(maxBB_block)
        #print(minBB_cyl)
        #print(maxBB_cyl)
        #print(maxBB_cyl < minBB_block)
        #print(minBB_cyl > maxBB_block)
      
    return(cylinder_list_new)
  
  def createCylinders(self, cylinder_list, group_name, add_AABB=False):
    object_list = []
    for loc, direction, cylinder_name in cylinder_list:
      #print(i)
      #loc, direction, cylinder_name = i
      #print(loc)
      #print(direction)
      #print(name)
      cyl = self.addCylinder(loc, direction, cylinder_name, add_AABB=add_AABB)
      cyl.ViewObject.Visibility=False
      object_list.append(cyl)
    f = App.activeDocument().addObject("Part::MultiFuse","Fusion")
    f.Shapes = object_list
    f.Label = group_name
    return(f)

def getCylinders_tetra(location, name):

  dir0 = [-1,-1,-1]
  dir1 = [1, 1,-1]
  dir2 = [1,-1,1]
  dir3 = [-1,1,1]

  cyl0 = (location, dir0, name+'_cyl0')
  cyl1 = (location, dir1, name+'_cyl1')
  cyl2 = (location, dir2, name+'_cyl2')
  cyl3 = (location, dir3, name+'_cyl3')

  cylinder_list = [cyl0, cyl1, cyl2, cyl3]

  return(cylinder_list)

def getCylinders_RCDCubicUnitCell(i, j, k, shifted=False, g_location = [0,0,0], cubic_unit_cell_size=1):
  cylinder_list = []
  
  g_location = numpy.array(g_location)
  
  u = numpy.array([1, 0, 0])
  v = numpy.array([0, 1, 0])
  w = numpy.array([0, 0, 1])
  
  unit_cell_location = i*u + j*v + k*w
  
  if shifted:
    t0 = getCylinders_tetra(g_location + (unit_cell_location + numpy.array([3/4, 1/4, 1/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.0'.format(i,j,k))
    t1 = getCylinders_tetra(g_location + (unit_cell_location + numpy.array([1/4, 3/4, 1/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.1'.format(i,j,k))
    t2 = getCylinders_tetra(g_location + (unit_cell_location + numpy.array([1/4, 1/4, 3/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.2'.format(i,j,k))
    t3 = getCylinders_tetra(g_location + (unit_cell_location + numpy.array([3/4, 3/4, 3/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.3'.format(i,j,k))
  else:
    t0 = getCylinders_tetra(g_location + (unit_cell_location + numpy.array([1/4, 1/4, 1/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.0'.format(i,j,k))
    t1 = getCylinders_tetra(g_location + (unit_cell_location + numpy.array([3/4, 3/4, 1/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.1'.format(i,j,k))
    t2 = getCylinders_tetra(g_location + (unit_cell_location + numpy.array([3/4, 1/4, 3/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.2'.format(i,j,k))
    t3 = getCylinders_tetra(g_location + (unit_cell_location + numpy.array([1/4, 3/4, 3/4]))*cubic_unit_cell_size, 'tetra.{}.{}.{}.3'.format(i,j,k))
  
  cylinder_list.extend(t0)
  cylinder_list.extend(t1)
  cylinder_list.extend(t2)
  cylinder_list.extend(t3)

  return(cylinder_list)

def getCylinders_createRCD(minBB, maxBB, shifted=False):
  i_min,j_min,k_min = minBB
  i_max,j_max,k_max = maxBB
  
  cylinder_list = []
  # returns cylinder parameters (centre, direction, radius, length)
  for i in range(i_min, i_max):
    for j in range(j_min, j_max):
      for k in range(k_min, k_max):
        cylinder_list += getCylinders_RCDCubicUnitCell(i, j, k, shifted)
  return(cylinder_list)

def main():
  FreeCAD.Console.PrintMessage("START...\n")
  doc = FreeCAD.activeDocument()
  if doc is None:
    App.newDocument("Unnamed")
    doc = FreeCAD.activeDocument()
  
  obj = RCD()
  obj.createInverseRCD_at_location([0.5+1/8,0.5+1/8,0.5+1/8], shifted=False)

  doc.recompute()
  Gui.ActiveDocument.ActiveView.setAxisCross(True)
  Gui.SendMsgToActiveView("ViewFit")
  FreeCAD.Console.PrintMessage("...DONE\n")

  return 0

if __name__ == '__main__':
  main()
