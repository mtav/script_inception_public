#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Functions returning vertex, edge, face lists in the form:
([(x,y,z),...], [(0,1),...], [[0,1,2],...])
'''

bl_info = {"name":"mesh - MODULE - NOT ADDON", "category": "Module", 'warning': 'MODULE - NOT ADDON'}

import numpy

def block(centro_vec3, size_vec3):
  
  verts = [(+0.5, +0.5, -0.5),
           (+0.5, -0.5, -0.5),
           (-0.5, -0.5, -0.5),
           (-0.5, +0.5, -0.5),
           (+0.5, +0.5, +0.5),
           (+0.5, -0.5, +0.5),
           (-0.5, -0.5, +0.5),
           (-0.5, +0.5, +0.5)]
  
  # cf: https://docs.scipy.org/doc/numpy/user/basics.broadcasting.html
  verts = numpy.array(centro_vec3) + numpy.array(size_vec3)*numpy.array(verts)
  
  edges = []
  
  faces = [(0, 1, 2, 3),
           (4, 7, 6, 5),
           (0, 4, 5, 1),
           (1, 5, 6, 2),
           (2, 6, 7, 3),
           (4, 0, 3, 7),
          ]
  
  return (verts, edges, faces)

if __name__ == '__main__':
  print(block([0,0,0], [1,1,1]))
