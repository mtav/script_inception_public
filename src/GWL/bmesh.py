#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Quick re-implementation Blender BMesh class
# TODO: Check if there is a way to access Blender classes from outside Blender.

class BMVert():
  def __init__(self, co=(0,0,0)):
    self.co = co
    
#class BMEdge():
#class BMFace():

class BMVertSeq():
  def __init__(self):
    self.verts = []
  def new(self, v_co):
    v = BMVert(v_co)
    self.verts.append(v)
    return(v)

class BMEdgeSeq():
  def __init__(self):
    self.edges = []
  def new(self, v_list):
    self.edges.append(v_list)

class BMFaceSeq():
  def __init__(self):
    self.faces = []
  def new(self, v_list):
    self.faces.append(v_list)

class BMesh():
  def __init__(self):
    self.verts = BMVertSeq()
    self.edges = BMEdgeSeq()
    self.faces = BMFaceSeq()

def new():
  return BMesh()

if __name__ == "__main__":
  bmesh_cube = new()

  C0 = bmesh_cube.verts.new((0, 0, 0))
  C1 = bmesh_cube.verts.new((1, 0, 0))
  C2 = bmesh_cube.verts.new((1, 1, 0))
  C3 = bmesh_cube.verts.new((0, 1, 0))
  C4 = bmesh_cube.verts.new((0, 0, 1))
  C5 = bmesh_cube.verts.new((1, 0, 1))
  C6 = bmesh_cube.verts.new((1, 1, 1))
  C7 = bmesh_cube.verts.new((0, 1, 1))

  bmesh_cube.faces.new((C0, C3, C2, C1))
  bmesh_cube.faces.new((C4, C5, C6, C7))
  bmesh_cube.faces.new((C0, C1, C5, C4))
  bmesh_cube.faces.new((C1, C2, C6, C5))
  bmesh_cube.faces.new((C2, C3, C7, C6))
  bmesh_cube.faces.new((C3, C0, C4, C7))
