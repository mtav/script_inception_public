#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import division
import utilities.ellipse

if __name__ == '__main__':
  rod_info = utilities.ellipse.EllipticalRod()
  rod_info.setEllipsoidWidth(1)
  rod_info.setCylinderDiameterBig(1)
  rod_info.plot()
  try:
    import FreeCAD
    FreeCAD.Console.PrintMessage('{}\n'.format(rod_info))
  except:
    print(rod_info)
