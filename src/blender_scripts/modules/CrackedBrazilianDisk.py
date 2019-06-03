#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy
import tempfile

class CrackedBrazilianDisk():
  disk_diametro = 15
  disk_height = 5
  hole_width = 1
  hole_length = 5
  wall_width = 2
  wall_length_extra = 0
  wall_height_extra = 0
  
  def getDiskDiametro(self):
    return(self.disk_diametro)
  def getDiskHeight(self):
    return(self.disk_height)
  def getHoleWidth(self):
    return(self.hole_width)
  def getHoleLength(self):
    return(self.hole_length)
  def getWallWidth(self):
    return(self.wall_width)
  def getWallLengthExtra(self):
    return(self.wall_length_extra)
  def getWallHeightExtra(self):
    return(self.wall_height_extra)
  
  def setDiskDiametre(self, value):
    self.disk_diametro = value
    return
  def setDiskHeight(self, value):
    self.disk_height = value
    return
  def setHoleWidth(self, value):
    self.hole_width = value
    return
  def setHoleLength(self, value):
    self.hole_length = value
    return
  def setWallWidth(self, value):
    self.wall_width = value
    return
  def setWallLengthExtra(self, value):
    self.wall_length_extra = value
    return
  def setWallHeightExtra(self, value):
    self.wall_height_extra = value
    return
    
  def createBlenderObject(self, blender_operator, context):
    import bpy
    from blender_scripts.modules.GeometryObjects import add_cylinder, add_tetra, add_block
    from blender_scripts.modules.blender_utilities import selectObjects
    
    cursor_location3 = numpy.array(bpy.context.scene.cursor_location)
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.5*self.disk_diametro, depth=self.disk_height)
    obj_disk = bpy.context.active_object
    obj_disk.name = 'CBD.disk'
    
    obj_wall_top = add_block(blender_operator, location3 = numpy.array([0, 0.5*self.getDiskDiametro(), 0]), size3 = [self.getDiskDiametro() + 2*self.getWallLengthExtra(), self.getWallWidth(), self.getDiskHeight() + 2*self.getWallHeightExtra()], name='CBD.wall_top')
    obj_wall_top.parent = obj_disk
    
    obj_wall_bottom = add_block(blender_operator, location3 = -numpy.array([0, 0.5*self.getDiskDiametro(), 0]), size3 = [self.getDiskDiametro() + 2*self.getWallLengthExtra(), self.getWallWidth(), self.getDiskHeight() + 2*self.getWallHeightExtra()], name='CBD.wall_bottom')
    obj_wall_bottom.parent = obj_disk
    
    obj_hole = add_block(blender_operator, location3 = cursor_location3, size3 = [self.getHoleWidth(), self.getHoleLength(), 2*self.getDiskHeight()], name='CBD.hole')
    #obj_hole.parent = obj_disk
    
    bool_mod = obj_disk.modifiers.new('CBD.hole-modifier', 'BOOLEAN')
    bool_mod.operation = 'DIFFERENCE'
    bool_mod.object = obj_hole
    #obj_hole.hide = True
    
    selectObjects([obj_disk], active_object=obj_disk, context = bpy.context)
    bpy.ops.object.modifier_apply(modifier=bool_mod.name, apply_as='DATA')
    
    selectObjects([obj_hole], active_object=obj_hole, context = bpy.context)
    bpy.ops.object.delete()
    
    selectObjects([obj_disk], active_object=obj_disk, context = bpy.context)
    
    return(obj_disk)
    
  def writeFIBStreamFile(self, outfile):
    return

def test():
  obj = CrackedBrazilianDisk()
  obj.writeFIBStreamFile(tempfile.gettempdir()+'CBD.str')
  return

if __name__ == '__main__':
  test()
