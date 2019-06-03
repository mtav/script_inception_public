#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import *
import time
import sys
import os
import numpy
from GWL.GWL_parser import *

def createSubstrate(DSTDIR,
  NAME = 'Substrate.gwl',
  box_size = 10,
  substrate_height = 1,
  LineDistance_Horizontal = 0.350,
  LineDistance_Vertical = 0.350,
  BottomToTop = False,
  writingOffset = [0,0,0,0]):
  
  LineNumber_Horizontal = int(box_size/LineDistance_Horizontal)+1
  LineNumber_Vertical = int(substrate_height/LineDistance_Vertical)+1
  
  box = GWLobject()
  box.addXblock([-0.5*box_size,0,0.5*substrate_height], [0.5*box_size,0,0.5*substrate_height], LineNumber_Horizontal, LineDistance_Horizontal, LineNumber_Vertical, LineDistance_Vertical, BottomToTop)
  box.write_GWL(DSTDIR + os.path.sep + NAME, writingOffset = writingOffset )
  return
  
def createLegs(DSTDIR,
  NAME = 'Legs.gwl',
  wall_thickness = 1,
  leg_height = 3,
  hole_width = 4,
  box_size = 10,
  overshoot = 1,
  LineDistance_Horizontal = 0.350,
  LineDistance_Vertical = 0.350,
  BottomToTop = False,
  writingOffset = [0,0,0,0]):

  LineNumber_Horizontal = int(wall_thickness/LineDistance_Horizontal)+1
  LineNumber_Vertical = int(leg_height/LineDistance_Vertical)+1
  A = 0.5*hole_width
  B = 0.5*box_size + overshoot
  C = 0.5*box_size
  Z = 0.5*leg_height
  
  box = GWLobject()

  # top
  box.addXblock([ B, C, Z], [ A, C, Z], LineNumber_Horizontal, LineDistance_Horizontal, LineNumber_Vertical, LineDistance_Vertical, BottomToTop)
  box.addXblock([-A, C, Z], [-B, C, Z], LineNumber_Horizontal, LineDistance_Horizontal, LineNumber_Vertical, LineDistance_Vertical, BottomToTop)

  # left
  box.addYblock([-C, B, Z], [-C, A, Z], LineNumber_Horizontal, LineDistance_Horizontal, LineNumber_Vertical, LineDistance_Vertical, BottomToTop)
  box.addYblock([-C,-A, Z], [-C,-B, Z], LineNumber_Horizontal, LineDistance_Horizontal, LineNumber_Vertical, LineDistance_Vertical, BottomToTop)

  # bottom
  box.addXblock([-B,-C, Z], [-A,-C, Z], LineNumber_Horizontal, LineDistance_Horizontal, LineNumber_Vertical, LineDistance_Vertical, BottomToTop)
  box.addXblock([ A,-C, Z], [ B,-C, Z], LineNumber_Horizontal, LineDistance_Horizontal, LineNumber_Vertical, LineDistance_Vertical, BottomToTop)

  # right
  box.addYblock([ C,-B, Z], [ C,-A, Z], LineNumber_Horizontal, LineDistance_Horizontal, LineNumber_Vertical, LineDistance_Vertical, BottomToTop)
  box.addYblock([ C, A, Z], [ C, B, Z], LineNumber_Horizontal, LineDistance_Horizontal, LineNumber_Vertical, LineDistance_Vertical, BottomToTop)

  box.write_GWL(DSTDIR + os.path.sep + NAME, writingOffset = writingOffset )
  return

def createSimpleBox(DSTDIR,  
  NAME = 'SimpleBox.gwl',
  box_size = 10,
  wall_height = 5,
  wall_thickness = 0,
  overshoot = 3,
  LineDistance_Horizontal = 0.350,
  LineDistance_Vertical = 0.350,
  BottomToTop = False,
  writingOffset = [0,0,0,0]):

  LineNumber_Horizontal = int(wall_thickness/LineDistance_Horizontal)+1
  LineNumber_Vertical = int(wall_height/LineDistance_Vertical)+1
  A = 0.5*box_size
  B = 0.5*box_size+overshoot
  Z = 0.5*wall_height

  box = GWLobject()
  box.addXblock([-B,-A,Z], [B,-A,Z], LineNumber_Horizontal, LineDistance_Horizontal, LineNumber_Vertical, LineDistance_Vertical, BottomToTop)
  box.addYblock([A,-B,Z], [A,B,Z], LineNumber_Horizontal, LineDistance_Horizontal, LineNumber_Vertical, LineDistance_Vertical, BottomToTop)
  box.addXblock([-B,A,Z], [B,A,Z], LineNumber_Horizontal, LineDistance_Horizontal, LineNumber_Vertical, LineDistance_Vertical, BottomToTop)
  box.addYblock([-A,-B,Z], [-A,B,Z], LineNumber_Horizontal, LineDistance_Horizontal, LineNumber_Vertical, LineDistance_Vertical, BottomToTop)
  box.write_GWL(DSTDIR + os.path.sep + NAME, writingOffset = writingOffset )
  return

def createElevatedBoxWithSubstrate(DSTDIR):
  box_size = 10
  substrate_height = 1
  leg_height = 3
  wall_height = 5
  wall_thickness = 1
  hole_width = 6
  overshoot = 0.5*wall_thickness
  LineDistance_Horizontal = 0.350
  LineDistance_Vertical = 0.350
  BottomToTop = False
  writingOffset = numpy.array([0,0,0,0])
  createSubstrate(DSTDIR,NAME='ElevatedBoxWithSubstrate.substrate.gwl',box_size=box_size+wall_thickness,substrate_height=substrate_height)
  createLegs(DSTDIR,NAME='ElevatedBoxWithSubstrate.legs.gwl',box_size=box_size,leg_height=leg_height,hole_width=hole_width,wall_thickness=wall_thickness,overshoot=overshoot,writingOffset=writingOffset+numpy.array([0,0,substrate_height,0]))
  createSimpleBox(DSTDIR,NAME='ElevatedBoxWithSubstrate.box.gwl',box_size=box_size,wall_height=wall_height,wall_thickness=wall_thickness,overshoot=overshoot,writingOffset=writingOffset+numpy.array([0,0,substrate_height+leg_height,0]))
  return

def main():
  time_start = time.time()

  if len(sys.argv)>1:
    DSTDIR = sys.argv[1]
  else:
    DSTDIR = os.getcwd()

  createSubstrate(DSTDIR)
  createLegs(DSTDIR)
  createSimpleBox(DSTDIR)
  createElevatedBoxWithSubstrate(DSTDIR)
  
  print( 'Output in ' + DSTDIR)

  print("My Script Finished: %.4f sec" % (time.time() - time_start))

if __name__ == "__main__":
  main()
