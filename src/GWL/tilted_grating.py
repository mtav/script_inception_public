#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy
from GWL.GWL_parser import GWLobject
from GWL.parallelepiped import Parallelepiped

class TiltedGrating(GWLobject):
  def __init__(self):
    self.Nlines = 11
    self.angle_deg = 60
    self.line_width = 1
    self.line_height = 2
    self.line_length = 10
    self.period = 2
    self.connected = False

    GWLobject.__init__(self)

  def computePoints(self):
    self.clear()
    # TODO: Only create block (with point list) once and add offsets during writing?
    for i in range(self.Nlines):
      block = Parallelepiped()
      block.center_vec3 = [i*self.period,0,0]
      block.connected = self.connected

      block.e1_vec3 = [0,1,0]
      block.e2_vec3 = [1,0,0]
      block.e3_vec3 = 1*numpy.array([numpy.cos(numpy.radians(self.angle_deg)),0,numpy.sin(numpy.radians(self.angle_deg))])

      block.size_vec3 = [self.line_length, self.line_width, self.line_height]
      block.computePoints()
      self.addGWLobject(block)

  def writeGWL(self, filename, writingOffset = [0,0,0,0]):
    self.computePoints()
    GWLobject.writeGWL(self, filename, writingOffset)
    return

  def getMeshData(self):
    self.computePoints()
    return(GWLobject.getMeshData(self))

def block_example_2():
    obj = Parallelepiped()
    obj.e1_vec3 = [1,1,0]
    obj.e2_vec3 = [-1,1,0]
    obj.e3_vec3 = [0,1,1]
    obj.size_vec3 = [5,10,15]
    obj.center_vec3 = [1,2,3]
    obj.writeGWL('block.example2.gwl')
    return

def block_example():

    main_obj = GWLobject()

    size = 10
    height = 5
    width = 2
    angle_deg = 170
    e3_horiz = numpy.cos(numpy.radians(angle_deg))
    e3_vert = -1*numpy.sin(numpy.radians(angle_deg))

    distFromCentre = 0.5*size-0.5*e3_horiz*height

    obj = Parallelepiped()
    obj.e1_vec3 = [0,1,0]
    obj.e2_vec3 = [1,0,0]
    obj.e3_vec3 = [-e3_horiz,0,e3_vert]
    obj.size_vec3 = [size,width,height]
    obj.center_vec3 = [distFromCentre,0,0]
    obj.computePoints()
    obj.writeGWL('blockxp.gwl')
    main_obj.addGWLobject(obj)

    obj = Parallelepiped()
    obj.e1_vec3 = [0,1,0]
    obj.e2_vec3 = [1,0,0]
    obj.e3_vec3 = [e3_horiz,0,e3_vert]
    obj.size_vec3 = [size,width,height]
    obj.center_vec3 = [-distFromCentre,0,0]
    obj.computePoints()
    obj.writeGWL('blockxm.gwl')
    main_obj.addGWLobject(obj)

    obj = Parallelepiped()
    obj.e1_vec3 = [1,0,0]
    obj.e2_vec3 = [0,1,0]
    obj.e3_vec3 = [0,-e3_horiz,e3_vert]
    obj.size_vec3 = [size,width,height]
    obj.center_vec3 = [0,distFromCentre,0]
    obj.computePoints()
    obj.writeGWL('blockyp.gwl')
    main_obj.addGWLobject(obj)

    obj = Parallelepiped()
    obj.e1_vec3 = [1,0,0]
    obj.e2_vec3 = [0,1,0]
    obj.e3_vec3 = [0,e3_horiz,e3_vert]
    obj.size_vec3 = [size,width,height]
    obj.center_vec3 = [0,-distFromCentre,0]
    obj.computePoints()
    obj.writeGWL('blockym.gwl')
    main_obj.addGWLobject(obj)

    main_obj.writeGWL('tilted_box.gwl')

    return

def main():
  obj = TiltedGrating()
  #obj.writeGWL('tilted_grating.TopToBottom.gwl')
  obj.writeGWL('tilted_grating.BottomToTop.gwl')

if __name__ == "__main__":
  #main()
  #block_example()
  #block_example_2()

  foo = TiltedGrating()
  print(foo.getMeshData())
