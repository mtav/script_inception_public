#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bfdtd.bfdtd_parser import *
from numpy import array, cos, sin, tan, degrees, radians, arccos, arcsin, arctan, floor, ceil, ones, zeros, pi, linspace, log10

def spiral(sim, spiral_origin):
  #spiral_origin = [0,0,0]
  
  spiral_radius_x = 0.3
  spiral_radius_y = 0.6
  points_per_turn = 10
  z_step_per_turn = 3
  turns = 2
  cylinder_radius = 0.2
  
  theta_step = 2*pi/points_per_turn
  z_step = z_step_per_turn/points_per_turn

  x_previous, y_previous, z_previous = 0,0,0
  pos_previous = array([0,0,0])
    
  for idx in range(turns*points_per_turn):
    
    theta = idx*theta_step    
    x = spiral_origin[0] + spiral_radius_x*cos(theta)
    y = spiral_origin[1] + spiral_radius_y*sin(theta)
    z = spiral_origin[2] + idx*z_step
    
    dx = -spiral_radius_x*sin(theta)*theta_step
    dy = spiral_radius_y*cos(theta)*theta_step
    dz = z_step_per_turn*theta_step/(2*pi)
  
    print((x,y,z,dx,dy,dz))

    pos = array([x,y,z])

    if idx > 0:
      obj = Cylinder()
      #obj.setLocation((pos + pos_previous)/2)
      #obj.setAxis(pos - pos_previous)
      #obj.setHeight(norm(pos - pos_previous))
      obj.setStartEndPoints(pos_previous, pos)
      obj.setOuterRadius(cylinder_radius)
    
      sim.appendGeometryObject(obj)
      
    pos_previous = array(pos)
  
def main():
	
  sim = BFDTDobject()
  
  xstep = 2
  ystep = 3
  
  for i in range(1):
    for j in range(1):
      spiral(sim, [i*xstep,j*ystep,0])
  
  sim.writeGeoFile('foo.geo')
  return 0

if __name__ == '__main__':
  main()
