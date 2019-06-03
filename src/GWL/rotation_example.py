#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# rotation example
from GWL.GWL_parser import GWLobject

if __name__ == '__main__':
  axis_point = [1,2,3]
  axis_direction = [1,1,1]
  angle_degrees = 45

  filename_in = 'woodpile06um.gwl'
  filename_out = 'rotated.gwl'

  obj = GWLobject()
  obj.readGWL(filename_in)
  obj.rotate(axis_point, axis_direction, angle_degrees)
  obj.write_GWL(filename_out)
