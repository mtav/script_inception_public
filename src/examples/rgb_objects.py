#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bfdtd.bfdtd_parser import *

if __name__ == '__main__':

  sim = BFDTDobject()

  x = 0.5; y = 0.5; z = 0.5
  Block_r = Block(permittivity=pow(2,2)); Block_r.setCentro([x,y,z]); sim.geometry_object_list.append(Block_r)
  Block_g = Block(permittivity=pow(3,2)); Block_g.setCentro([x+2,y,z]); sim.geometry_object_list.append(Block_g)
  Block_b = Block(permittivity=pow(4,2)); Block_b.setCentro([x+2*2,y,z]); sim.geometry_object_list.append(Block_b)

  x = 0.5; y = 2.5; z = 0.5
  Distorted_r = Distorted(permittivity=pow(2,2)); Distorted_r.setCentro([x,y,z]); sim.geometry_object_list.append(Distorted_r)
  Distorted_g = Distorted(permittivity=pow(3,2)); Distorted_g.setCentro([x+2,y,z]); sim.geometry_object_list.append(Distorted_g)
  Distorted_b = Distorted(permittivity=pow(4,2)); Distorted_b.setCentro([x+2*2,y,z]); sim.geometry_object_list.append(Distorted_b)

  x = 0.5; y = 4.5; z = 0.5
  Cylinder_r = Cylinder(permittivity=pow(2,2)); Cylinder_r.setCentro([x,y,z]); sim.geometry_object_list.append(Cylinder_r)
  Cylinder_g = Cylinder(permittivity=pow(3,2)); Cylinder_g.setCentro([x+2,y,z]); sim.geometry_object_list.append(Cylinder_g)
  Cylinder_b = Cylinder(permittivity=pow(4,2)); Cylinder_b.setCentro([x+2*2,y,z]); sim.geometry_object_list.append(Cylinder_b)

  x = 0.5; y = 6.5; z = 0.5
  Sphere_r = Sphere(permittivity=pow(2,2)); Sphere_r.setCentro([x,y,z]); sim.geometry_object_list.append(Sphere_r)
  Sphere_g = Sphere(permittivity=pow(3,2)); Sphere_g.setCentro([x+2,y,z]); sim.geometry_object_list.append(Sphere_g)
  Sphere_b = Sphere(permittivity=pow(4,2)); Sphere_b.setCentro([x+2*2,y,z]); sim.geometry_object_list.append(Sphere_b)

  sim.writeGeoFile('rgb_objects.geo')
