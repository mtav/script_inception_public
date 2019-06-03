#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from GWL.GWL_parser import *

if __name__ == "__main__":
  if len(sys.argv)>1:
      DSTDIR = sys.argv[1]
  else:
      DSTDIR = os.getcwd()

  centro=[0,0,0]
  inner_radius = 1
  outer_radius = 2
  height = 10
  power = -1
  PointDistance_r = 0.1
  PointDistance_theta = 0.1

  obj1 = GWLobject()
  obj1.addTubeWithVerticalLines(centro, inner_radius, outer_radius, height, power, PointDistance_r, PointDistance_theta, downwardWriting=True, zigzag=False)
  obj1.write_GWL(DSTDIR + os.path.sep + 'cylinder1.gwl', writingOffset = [0,0,0,0] )

  obj2 = GWLobject()
  obj2.addTubeWithVerticalLines(centro, inner_radius, outer_radius, height, power, PointDistance_r, PointDistance_theta, downwardWriting=True, zigzag=True)
  obj2.write_GWL(DSTDIR + os.path.sep + 'cylinder2.gwl', writingOffset = [0,0,0,0] )

  up = GWLobject()
  up.addTubeWithVerticalLines(centro, 0, 0, height, power, PointDistance_r, PointDistance_theta, downwardWriting=False, zigzag=True)
  up.write_GWL(DSTDIR + os.path.sep + 'up.gwl', writingOffset = [0,0,0,0] )

  down = GWLobject()
  down.addTubeWithVerticalLines(centro, 0, 0, height, power, PointDistance_r, PointDistance_theta, downwardWriting=True, zigzag=True)
  down.write_GWL(DSTDIR + os.path.sep + 'down.gwl', writingOffset = [0,0,0,0] )

  print( 'Output in ' + DSTDIR)
