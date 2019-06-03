#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from GWL.GWL_parser import *

class foobarClass(GWLobject):
  def __init__(self):
    GWLobject.__init__(self)
  def setProperty(self, N):
    for i in range(N):
      self.GWL_voxels.append([[i,0,0],[i+0.5,0,0]])

if __name__ == "__main__":
  foo = foobarClass()
  foo.setProperty(3)
  print(foo.getMeshData())
