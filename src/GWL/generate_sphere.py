#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from GWL.GWL_parser import *

if __name__ == "__main__":
  center = [0,0,0]
  diametro = float(sys.argv[1])
  HorizontalPointDistance = 0.050
  VerticalPointDistance = 0.100
  GWL_obj = GWLobject()
  GWL_obj.addSphere(center, 0.5*diametro, -1, HorizontalPointDistance, VerticalPointDistance, True)
  GWL_obj.write_GWL('sphere.diametro_'+str(diametro)+'.gwl')
