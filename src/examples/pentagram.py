#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from numpy import pi, cos, sin, array
from GWL.GWL_parser import GWLobject

def main():
  alpha = 2*pi/5
  r_outer = 1
  r_inner = r_outer*cos(alpha)/cos(alpha/2)
  #r_inner = 0.5
  
  P_outer = 5*[0]
  P_inner = 5*[0]
  pentagram = []
  pentagram_star = []
  for idx in range(5):
    theta_outer = pi/2 + idx*alpha
    P_outer[idx] = r_outer*array([cos(theta_outer), sin(theta_outer),0])
    theta_inner = -pi/2 - 2*alpha + idx*alpha
    P_inner[idx] = r_inner*array([cos(theta_inner), sin(theta_inner),0])
    pentagram_star.append(P_outer[idx])
    pentagram_star.append(P_inner[idx])

  pentagram_star.append(P_outer[0])
  pentagram_star.append(P_inner[0])
  
  pentagram = [P_outer[0], P_outer[3], P_outer[1], P_outer[4], P_outer[2], P_outer[0]]

  obj = GWLobject()
  obj.setVoxels([P_outer,
                  P_inner,
                  pentagram_star,
                  pentagram,
                  ])
  obj.writeGWL('pentagram.gwl')

  return 0

if __name__ == '__main__':
  main()
