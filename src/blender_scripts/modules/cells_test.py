#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# To make Blender happy:
bl_info = {"name":"cells_test", "category": "User"}

"""
Name: 'cells test'
Blender: 243
Group: 'Add'
Tooltip: 'parent a cube to a series of vertices'
"""

import Blender; from Blender import *

import math

Vector    = Mathutils.Vector

def BlenderBlock(name, center, outer_radius):
  scene = Blender.Scene.GetCurrent()
  mesh = Blender.Mesh.Primitives.Cube(1.0)
  
  obj = scene.objects.new(mesh, name)
  pos = center
  diag = 2*outer_radius
  obj.SizeX = abs(diag)
  obj.SizeY = abs(diag)
  obj.SizeZ = abs(diag)
  obj.setLocation(pos[0], pos[1], pos[2])
  return obj

if __name__ == "__main__":
  cell = BlenderBlock('voxel',Vector(0,0,0),1)

  mesh_new = Mesh.New("newmesh")
  mesh_new.verts = None
  
  verts = [Vector(0,0,0),Vector(1,1,1),Vector(2,2,2)]
  mesh_new.verts.extend(verts)

  scene = Scene.GetCurrent()
        
  object_new = scene.objects.new(mesh_new,"newobject")

  cell.layers = object_new.layers
  scene.update()
  object_new.makeParent([cell])
  object_new.enableDupVerts = True
  
