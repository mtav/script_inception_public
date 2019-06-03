#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bfdtd.bfdtd_parser import *

# test function for quickly creating certain geometries
def createExcitationSpiral():
  # The death spiral!
  sim = BFDTDobject()
  #x1=0;y1=0;z1=0
  #x2=0;y2=0;z2=0
  sim.excitation_list.append(Excitation(P1=[0,0,0], P2=[1,0,0], name='X'))
  sim.excitation_list.append(Excitation(P1=[0,0,0], P2=[0,1,0], name='Y'))
  sim.excitation_list.append(Excitation(P1=[0,0,0], P2=[0,0,1], name='Z'))
  sim.excitation_list.append(Excitation(P1=[0,0,0], P2=[1,1,1], name='XYZ'))
  for i in range(10*36):
  #for i in range(2):
    x1=math.cos(math.radians(10*i))
    y1=math.sin(math.radians(10*i))
    z1=(10.*i)/360.
    x2=math.cos(math.radians(10*(i+1)))
    y2=math.sin(math.radians(10*(i+1)))
    z2=(10.*(i+1))/360.
    P1=[x1,y1,z1]
    P2=[x2,y2,z2]
    print('P1 = '+str(P1))
    print('P2 = '+str(P2))
    E = Excitation(P1=P1,P2=P2)
    E.fixLowerUpperAtWrite = False
    sim.excitation_list.append(E)
    #sim.probe_list.append(Probe(P2))
    #x1=x2;y1=y2;z1=z2
  return sim

if __name__ == '__main__':
  sim = createExcitationSpiral()
  sim.writeInpFile('excitation_spiral.inp')
