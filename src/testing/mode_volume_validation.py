#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# generate some .prn files of a known integratable function to validate mode volume calculations

import os
import argparse
import tempfile

import sys
import code
import numpy
from numpy import array, pi, cos, sin, sqrt
import itertools
from numpy.linalg.linalg import norm
from bfdtd.bfdtd_parser import BFDTDobject
from bfdtd.snapshot import ModeVolumeBox, ModeVolumeBoxFull
from meshing.meshing import linspaces

'''
.. todo:: Change the way we calculate MV, by using all snapshots, but doing trapezoidal integration.
.. todo:: Check how BFDTD generates epsilon snapshots (symmetry of sphere for instance)

.. todo:: finish improving the data_write functions
.. todo:: finish testing the data_write functions

.. todo:: finish MV calc improvement using "centered cells"
.. todo:: finish testing MV calc improvement

.. todo:: MV.setLambda + sim.setX/Y/Zmesh functions

.. todo:: theoretical MV of dipole emission in homogeneous material?

'''

def example_function_0(x, y, z, t):
  '''
  MV=24
  homogeneous

  mode_volume_mum3 should be exactly Dx*Dy*Dz = 2*3*4 = 24.

  calculateMV function finds::

    allFilesFound =  1
    TotalEnergy =  3.0300
    MaximumEnergyDensity =  3
    mode_volume_mum3 =  1.0100 = 1+1/100 -> because we added the snapshot on the edge of the cube * dx, with dx=1/100...
    normalized_mode_volume = NaN
    Lambda_mum =  299792458
    f0_MHz =  1
    first =  1
    snap_time_number = 0
    repetition =  524200
    Niterations =  1
    refractive_index_defect = NaN  

  new algo results:
    Dx,Dy,Dz=1,1,1 + non-homogeneous mesh:
      /tmp/MV-ref-full-2/example_function_0/X -> 1
      /tmp/MV-ref-full-2/example_function_0/Y -> 1
      /tmp/MV-ref-full-2/example_function_0/Z -> 1
  
  '''
  epsilon = 1
  E = array([1,1,1], dtype=complex)
  H = array([1,1,1], dtype=complex)
  return (epsilon, E, H)

def example_function_1(x, y, z, t):
  '''
  MV=?
  integrable

  mode_volume_mum3 should be exactly 14099/18585 = 0.75862 (for Dx=Dy=Dz=1)
  .. todo:: calculate in general case
  .. todo:: x,y,z linear function
  
  calculateMV function finds::
  
    allFilesFound =  1
    TotalEnergy =  2.1205
    MaximumEnergyDensity =  2.7528
    mode_volume_mum3 =  0.77031
    normalized_mode_volume = NaN
    Lambda_mum =  299792458
    f0_MHz =  1
    first =  1
    snap_time_number = 0
    repetition =  524200
    Niterations =  1
    refractive_index_defect = NaN
  '''
  epsilon = 1
  Exmod = abs((x-0.5) + (y-0.5)**2 + (z-0.5)**3)
  E = array([Exmod,1,1], dtype=complex)
  H = array([1,1,1], dtype=complex)
  return (epsilon, E, H)

def example_function_2(x, y, z, t):
  '''
  MV=3
  square cos

  mode_volume_mum3 should be exactly (1/2)^3*(lambda/(2*n))^3 = 0.12500.  (for Dx=Dy=Dz=1)
  for Dx,Dy,Dz=2,3,4: MV = 2*3*4*( (1/2)^3*(lambda/(2*n))^3 ) = 3
  
  calculateMV function finds::

    allFilesFound =  1
    TotalEnergy =  57.000
    MaximumEnergyDensity =  456
    mode_volume_mum3 =  0.12500
    normalized_mode_volume = NaN
    Lambda_mum =  299792458
    f0_MHz =  1
    first =  1
    snap_time_number = 0
    repetition =  524200
    Niterations =  1
    refractive_index_defect = NaN
  '''
  centro = numpy.array([0.5, 0.5, 0.5])
  epsilon = 456
  n = 2
  Lambda = 4
  k = 2*pi*n/Lambda
  Emod = abs(cos(k*(x-centro[0])))*abs(cos(k*(y-centro[1])))*abs(cos(k*(z-centro[2])))
  E = array([Emod,0,0], dtype=complex)
  H = array([0,0,0], dtype=complex)
  return (epsilon, E, H)

def example_function_3(x, y, z, t):
  '''
  gaussian

  mode_volume_mum3 should be exactly (pi/8)^(3/2)*(Lambda/(2*n))^3 = 5.7515e-04

  calculateMV function finds::
  
    allFilesFound =  1
    TotalEnergy =  0.0070456
    MaximumEnergyDensity =  12.250
    mode_volume_mum3 =    5.7515e-04
    normalized_mode_volume = NaN
    Lambda_mum =  299792458
    f0_MHz =  1
    first =  1
    snap_time_number = 0
    repetition =  524200
    Niterations =  1
    refractive_index_defect = NaN
    
  .. todo:: Update exact result based on new x,y,z Emod
  '''
  #centro = numpy.array([0.2, 0.3, 0.4])
  centro = numpy.array([0.5, 0.5, 0.5])
  epsilon = 12.25
  n = 1/2
  #Lambda = 0.637
  Lambda = 0.250
  r = norm(numpy.array([x,y,z]) - centro)
  Emod = numpy.exp( -4 * pow(r / (Lambda/(2*n)), 2) )
  Ex = 2*Emod
  Ey = 3*Emod
  Ez = 4*Emod
  E = array([Ex,Ey,Ez], dtype=complex)
  H = array([0,0,0], dtype=complex)  
  return (epsilon, E, H)

def example_function_4(x, y, z, t):
  '''
  sphere

  mode_volume_mum3 should be exactly (4/3)*pi*r^3 = 0.065450
  
  calculateMV function finds::

    allFilesFound =  1
    TotalEnergy =  1.8266
    MaximumEnergyDensity =  28
    mode_volume_mum3 =  0.065237
    normalized_mode_volume = NaN
    Lambda_mum =  299792458
    f0_MHz =  1
    first =  1
    snap_time_number = 0
    repetition =  524200
    Niterations =  1
    refractive_index_defect = NaN
  '''
  centro = numpy.array([0.5, 0.5, 0.5])
  radius = 0.25
  if norm(numpy.array([x,y,z]) - centro) <= radius:
    epsilon = 2
    E = array([1,2,3], dtype=complex)
    H = array([4,5,6], dtype=complex)
  else:
    epsilon = 1
    E = array([0,0,0], dtype=complex)
    H = array([0,0,0], dtype=complex)
  return (epsilon, E, H)

def example_function_5(x, y, z, t):
  '''
  E^2 = Dz - z
  
  MV should be Dx*Dy*(Dz^2/2)
  
  '''
  Dz = 4
  epsilon = 1
  E = array([0, 0, sqrt(Dz - z)], dtype=complex)
  H = array([0, 0, 0], dtype=complex)
  return (epsilon, E, H)

def example_function_6(x, y, z, t):
  '''
  gaussian

  mode_volume_mum3 should be exactly (pi/8)^(3/2)*(Lambda/(2*n))^3 = 5.7515e-04

    ((pi/8)^(3/2))*(0.25)^3
    ans =  0.0038451

  calculateMV function finds::
  
    allFilesFound =  1
    TotalEnergy =  0.0070456
    MaximumEnergyDensity =  12.250
    mode_volume_mum3 =    5.7515e-04
    normalized_mode_volume = NaN
    Lambda_mum =  299792458
    f0_MHz =  1
    first =  1
    snap_time_number = 0
    repetition =  524200
    Niterations =  1
    refractive_index_defect = NaN

  new algo results:
    Dx,Dy,Dz=1,1,1 + non-homogeneous mesh:
      /tmp/MV-ref-full-2/example_function_6/X -> 0.0038466
      /tmp/MV-ref-full-2/example_function_6/Y -> 0.0038466
      /tmp/MV-ref-full-2/example_function_6/Z -> 0.0038466
    
  .. todo:: Update exact result based on new x,y,z Emod
  '''
  centro = numpy.array([1, 1, 1])/2
  epsilon = 12.25
  n = 1/2
  Lambda = 0.25
  r = norm(numpy.array([x,y,z]) - centro)
  Emod = numpy.exp( -4 * pow(r / (Lambda/(2*n)), 2) )
  Ex = 2*Emod
  Ey = 3*Emod
  Ez = 4*Emod
  E = array([Ex,Ey,Ez], dtype=complex)
  H = array([0,0,0], dtype=complex)  
  return (epsilon, E, H)

def example_function_7(x, y, z, t):
  '''
  E^2 = (a*x+b) + (c*y+d) + (e*z+f)
  int(E^2) = ((a*Dx/2 + b) + (c*Dy/2 + d) + (e*Dz/2 + f))*(Dx*Dy*Dz)
  
  expected:
    TotalEnergy = 13.5
    MaximumEnergyDensity = 18 at x,y,z=1,0,1
    mode_volume_mum3 = 13.5/18 = 0.75
    
  new algo results:
    Dx,Dy,Dz=1,1,1 + non-homogeneous mesh:
    /tmp/MV-ref-full-2/example_function_7/X -> 0.75
    /tmp/MV-ref-full-2/example_function_7/Y -> 0.75
    /tmp/MV-ref-full-2/example_function_7/Z -> 0.75  
  '''
  a = 1
  b = 2
  c = -3
  d = 4
  e = 5
  f = 6
  epsilon = 1
  E = array([sqrt(a*x+b), sqrt(c*y+d), sqrt(e*z+f)], dtype=complex)
  H = array([0, 0, 0], dtype=complex)
  return (epsilon, E, H)

def example_function_7_theory():
  a = 1
  b = 2
  c = -3
  d = 4
  e = 5
  f = 6
  Dx = 1
  Dy = 1
  Dz = 1  
  return ((a*Dx/2 + b) + (c*Dy/2 + d) + (e*Dz/2 + f))*(Dx*Dy*Dz)

def UniverseIsFullOfBalls(x, y, z, t):
  balls = [((2,2,2), 1, 2),
           ((5,2,2), 1, 5),
           ((8,2,2), 1, 8),
          ]

  epsilon = 1
  Ex = 0
  Ey = 0
  Ez = 0
  Hx = 0
  Hy = 0
  Hz = 0
  for c_ball, r_ball, eps_ball in balls:
    r = norm(array([x,y,z]) - array(c_ball))
    if r <= r_ball:
      epsilon = eps_ball*(10**0)
      Ex = eps_ball*(10**1)
      Ey = eps_ball*(10**2)
      Ez = eps_ball*(10**3)
      Hx = eps_ball*(10**4)
      Hy = eps_ball*(10**5)
      Hz = eps_ball*(10**6)
  
  E = array([Ex, Ey, Ez], dtype=complex)
  H = array([Hx, Hy, Hz], dtype=complex)
  return (epsilon, E, H)

def gaussian3D(x, y, z, t, centro = numpy.array([0.5, 0.5, 0.5]), alpha=1, sphere_radius=1, epsilon_outside=10, epsilon_inside=1):
  '''
  TODO: epsilon would be easier to deal with if we simply used objects? -> but requires FDTD run, so maybe not
  '''
  r = norm(numpy.array([x,y,z]) - centro)
  if r > sphere_radius:
    epsilon = epsilon_outside
  else:
    epsilon = epsilon_inside
  Emod2 = numpy.exp( -alpha * pow(r, 2) )
  Emod = numpy.sqrt(Emod2)
  E = array([Emod,0,0], dtype=complex)
  H = array([0,0,0], dtype=complex)
  return (epsilon, E, H)

def generateInpAndPrnFiles(dstdir, BFDTD_object, E_field_function, H_field_function, permittivity_field_function):
  
  BFDTD_object.writeInpFile(dstdir + BFDTD_object.getFileBaseName() + '.inp')

  xmesh = BFDTD_object.getXmesh()
  ymesh = BFDTD_object.getYmesh()
  zmesh = BFDTD_object.getZmesh()
  
  #for snap in snapshots:
    
    #fsnap.getData()
    
    #data = zeros(Ni, Nj, Nk)
    #for i in range(Ni):
      #data(x,y,z) = distribution_function(x,y,z)
    #fnsap.writePrnFile()
    
  return

def test():
  sim = BFDTDobject()
  sim.setSizeAndResolution([1,1,1],[200, 200, 200])
  MV = sim.appendSnapshot(ModeVolumeBox())
  #MV.setExtension(*sim.getExtension())
  MV.setExtension([0.12,0.45,0.78],[0.88,0.66,0.99])
  MV.setFrequencies([1])
  MV.setPlaneOrientationX()
  generateInpAndPrnFiles('/tmp/MV_validation/', sim, example_function_1, example_function_2, example_function_3)

def test2(destdir):
  sim = BFDTDobject()
  #sim.setSizeAndResolution([1,1,1], [5,5,5])
  #sim.setSizeAndResolution([1,1,1], [53,5,5])
  #sim.setSizeAndResolution([1,1,1], [438,1,1])
  #sim.setSizeAndResolution([1,1,1], [40, 50, 60])
  #sim.setSizeAndResolution([2,3,4], [100, 100, 100])
  sim.setSizeAndResolution([2,3,4], [20, 30, 40])
  MV = sim.appendSnapshot(ModeVolumeBoxFull())
  MV.setPlaneOrientationX()
  #TODO: MV.setLambda
  
  test_function = example_function_3
  
  MV.setPlaneOrientationX()
  subdir = os.path.join(destdir, 'X')
  sim.writeTorqueJobDirectory(subdir)
  sim.sampleFunction(test_function, subdir)
  
  MV.setPlaneOrientationY()
  subdir = os.path.join(destdir, 'Y')
  sim.writeTorqueJobDirectory(subdir)
  sim.sampleFunction(test_function, subdir)
  
  MV.setPlaneOrientationZ()  
  subdir = os.path.join(destdir, 'Z')
  sim.writeTorqueJobDirectory(subdir)
  sim.sampleFunction(test_function, subdir)
  
  #sim.sampleFunction(example_function_1, destdir)
  #sim.sampleFunction(example_function_2, destdir)
  #sim.sampleFunction(example_function_3, destdir)
  #sim.sampleFunction(example_function_4, destdir)
  #for i in sim.getOutputFileNames():
    #print(i)

def test3(destdir):
  # generate all possible time snapshot columns
  sim = BFDTDobject()
  sim.appendProbe(2*[Probe()])
  sim.appendSnapshot(3*[FrequencySnapshot()])
  sim.appendSnapshot(4*[TimeSnapshot()])
  sim.appendSnapshot(5*[EpsilonSnapshot()])
  sim.appendSnapshot(6*[ModeFilteredProbe()])
  sim.checkSimulation()

  code.interact(local=locals())

  return

def test4(destdir):
  sim = BFDTDobject()
  S = sim.appendSnapshot(TimeSnapshot())
  S.setEfield([0,0,0])
  S.setHfield([0,0,0])
  S.setJfield([0,0,0])
  S.setPower(0)
  S.setEpsilon(0)  
  print('=====')
  #print(S)
  subdir = '{}{}{}-{}{}{}-{}{}{}-{}-{}'.format(S.E[0],S.E[1],S.E[2], S.H[0],S.H[1],S.H[2], S.J[0],S.J[1],S.J[2], S.power, S.eps)
  print(subdir, S.getTypeBasedOnAttributes())
  sim.runSimulation(os.path.join(destdir, subdir))
  for i in range(11):
    (S.E[0],S.E[1],S.E[2], S.H[0],S.H[1],S.H[2], S.J[0],S.J[1],S.J[2], S.power, S.eps) = i*[0]+[1]+(10-i)*[0]
    print('=====')
    subdir = '{}{}{}-{}{}{}-{}{}{}-{}-{}'.format(S.E[0],S.E[1],S.E[2], S.H[0],S.H[1],S.H[2], S.J[0],S.J[1],S.J[2], S.power, S.eps)
    print(subdir, S.getTypeBasedOnAttributes())
    sim.runSimulation(os.path.join(destdir, subdir))
  return

def test5(destdir):
  sim = BFDTDobject()
  S = sim.appendSnapshot(TimeSnapshot())
  
  for plane in ['x','y','z']:
    for E in itertools.product(range(2),repeat=3):
      for H in itertools.product(range(2),repeat=3):
        for J in itertools.product(range(2),repeat=3):
          for power in [0,1]:
            for eps in [0,1]:
              print(plane, E, H, J, power, eps)
              S.setPlaneLetter(plane)
              S.setEfield(E)
              S.setHfield(H)
              S.setJfield(J)
              S.setPower(power)
              S.setEpsilon(eps)
              sim.runSimulation(destdir)
              #print(S)
              #print(S.getTypeBasedOnAttributes())
              if S.getTypeBasedOnAttributes() == ModeFilteredProbe:
                outfile = 'i1_id_00.prn'
              else:
                outfile = plane + '1_id_01.prn'
              #print('outfile =', outfile)
              with open(os.path.join(destdir, outfile)) as f:
                print(f.readline())
              
  #sim.writeTorqueJobDirectory(destdir)  
  #sim.runSimulation(destdir)
  return

def test6(destdir):
  sim = BFDTDobject()
  sim.setSizeAndResolution([20,30,40],[2, 3, 4])

  S = sim.appendSnapshot(FrequencySnapshot())
  
  for plane in ['x','y','z']:
    for E in itertools.product(range(2),repeat=3):
      for H in itertools.product(range(2),repeat=3):
        for J in itertools.product(range(2),repeat=3):
          for power in [0,1]:
            for eps in [0,1]:
              print(plane, E, H, J, power, eps)
              S.setPlaneLetter(plane)
              S.setEfield(E)
              S.setHfield(H)
              S.setJfield(J)
              S.setPower(power)
              S.setEpsilon(eps)
              sim.runSimulation(destdir)
              #print(S)
              #print(S.getTypeBasedOnAttributes())
              if S.getTypeBasedOnAttributes() == ModeFilteredProbe:
                outfile = 'i1_id_00.prn'
              else:
                outfile = plane + '1_id_01.prn'
              #print('outfile =', outfile)
              with open(os.path.join(destdir, outfile)) as f:
                print(f.readline())

  return

def generate_MV_refs_partial(destdir):
  sim = BFDTDobject()
  sim.setSizeAndResolution([1,1,1], [4, 4, 4])
  MV = sim.appendSnapshot(ModeVolumeBox())
  mx = sim.getXmesh()
  my = sim.getYmesh()
  mz = sim.getZmesh()

  #test_function_name = 'example_function_0'
  #test_function = example_function_0

  MV.setPlaneOrientationZ()
  
  #subdir = os.path.join(destdir, test_function_name, 'Z')

  MV.setExtension([mx[1], my[1], mz[0]], [mx[-2], my[-2], mz[-1]])
  subdir = os.path.join(destdir, 'partial-centro', 'Z')
  sim.runSimulation(subdir)

  MV.setExtension([mx[0], my[0], mz[0]], [mx[-2], my[-2], mz[-1]])
  subdir = os.path.join(destdir, 'partial-bottom-left', 'Z')
  sim.runSimulation(subdir)

  MV.setExtension([mx[1], my[0], mz[0]], [mx[-1], my[-2], mz[-1]])
  subdir = os.path.join(destdir, 'partial-bottom-right', 'Z')
  sim.runSimulation(subdir)

  MV.setExtension([mx[0], my[1], mz[0]], [mx[-2], my[-1], mz[-1]])
  subdir = os.path.join(destdir, 'partial-top-left', 'Z')
  sim.runSimulation(subdir)

  MV.setExtension([mx[1], my[1], mz[0]], [mx[-1], my[-1], mz[-1]])
  subdir = os.path.join(destdir, 'partial-top-right', 'Z')
  sim.runSimulation(subdir)

  MV.setExtension([mx[0], my[0], mz[0]], [mx[-1], my[-1], mz[-1]])
  subdir = os.path.join(destdir, 'full', 'Z')
  sim.runSimulation(subdir)
  
  #sim.writeTorqueJobDirectory(subdir)
  #sim.sampleFunction(test_function, subdir)
  
  return

def generate_MV_refs(destdir):
  '''
  .. todo:: Warn if using to many snapshots to avoid BFDTD output mess.
  '''
  sim = BFDTDobject()
  sim.disableSafetyChecks()
  #sim.setSizeAndResolution([1,1,1], [100, 90, 80])
  sim.setSizeAndResolution([10, 5, 4], [5, 5, 5], True)
  
  Niterations = sim.setIterations(1, AfterSources=True) # adds default excitation + appropriate sim time + 1 iteration
  print('Niterations = {}'.format(Niterations))
  #sim.setSizeAndResolution([10, 4, 4], [5,5,5], True)

  #mesh = sim.getMesh()
  #mesh.setXmesh(linspaces([0, 0.2, 0.5, 0.7, 1], [20, 30, 40, 50]))
  #mesh.setYmesh(linspaces([0, 0.25, 0.52, 0.67, 1], [60, 31, 42, 51]))
  #mesh.setZmesh(linspaces([0, 0.23, 0.6, 0.75, 1], [22, 33, 44, 55]))

  #mesh.setXmesh(linspaces([0, 0.2, 0.5, 0.7, 1], [21, 22, 23, 24]))
  #mesh.setYmesh(linspaces([0, 0.25, 0.52, 0.67, 1], [25, 26, 27, 28]))
  #mesh.setZmesh(linspaces([0, 0.23, 0.6, 0.75, 1], [29, 30, 31, 42]))

  #sim.setSizeAndResolution([1,1,1], [5,5,5])
  #sim.setSizeAndResolution([1,1,1], [53,5,5])
  #sim.setSizeAndResolution([1,1,1], [438,1,1])
  #sim.setSizeAndResolution([1,1,1], [40, 50, 60])
  
  #sim.setSizeAndResolution([2,3,1], [100, 100, 100])
  #sim.setSizeAndResolution([1,1,1], [20, 30, 40])

  MV = sim.appendSnapshot(ModeVolumeBoxFull())
  #MV.setWavelengths(0.637)
  MV.setWavelengths(0.250)
  
  test_function_list = [
    #('example_function_0', example_function_0),
    #('example_function_1', example_function_1),
    #('example_function_2', example_function_2),
    #('example_function_3', example_function_3),
    #('example_function_4', example_function_4),
    #('example_function_5', example_function_5),
    #('example_function_6', example_function_6),
    #('example_function_7', example_function_7),
    ('UniverseIsFullOfBalls', UniverseIsFullOfBalls),
    ]
  
  for test_function_name, test_function in test_function_list:
    print('===>', test_function_name, test_function)
  
    MV.setPlaneOrientationX()
    subdir = os.path.join(destdir, test_function_name, 'X')
    sim.writeTorqueJobDirectory(subdir)
    sim.sampleFunction(test_function, subdir)
    
    MV.setPlaneOrientationY()
    subdir = os.path.join(destdir, test_function_name, 'Y')
    sim.writeTorqueJobDirectory(subdir)
    sim.sampleFunction(test_function, subdir)
    
    MV.setPlaneOrientationZ()
    subdir = os.path.join(destdir, test_function_name, 'Z')
    sim.writeTorqueJobDirectory(subdir)
    sim.sampleFunction(test_function, subdir)
  
  return

def generate_MV_refs_LowIndexCavity(destdir):
  sim = BFDTDobject()
  sim.disableSafetyChecks()
  #sim.setSizeAndResolution([1,1,1], [100, 90, 80])
  sim.setSizeAndResolution([10, 10, 10], [100, 100, 100], False)
  Niterations = sim.setIterations(1, AfterSources=True) # adds default excitation + appropriate sim time + 1 iteration
  print('Niterations = {}'.format(Niterations))
  MV = sim.appendSnapshot(ModeVolumeBoxFull())
  MV.setPlaneOrientationZ() # current default in calcMV script...
  
  myfunc_low = lambda x, y, z, t: gaussian3D(x, y, z, t, centro=sim.getCentro(), epsilon_outside=10, epsilon_inside=1)
  myfunc_equal = lambda x, y, z, t: gaussian3D(x, y, z, t, centro=sim.getCentro(), epsilon_outside=1, epsilon_inside=1)
  myfunc_high = lambda x, y, z, t: gaussian3D(x, y, z, t, centro=sim.getCentro(), epsilon_outside=1, epsilon_inside=10)

  subdir = os.path.join(destdir, 'low_index')
  sim.writeTorqueJobDirectory(subdir)
  sim.sampleFunction(myfunc_low, subdir)

  subdir = os.path.join(destdir, 'equal_index')
  sim.writeTorqueJobDirectory(subdir)
  sim.sampleFunction(myfunc_equal, subdir)

  subdir = os.path.join(destdir, 'high_index')
  sim.writeTorqueJobDirectory(subdir)
  sim.sampleFunction(myfunc_high, subdir)

  return

def main():
  # read in ~/.pystartup to have all the desired modules
  pystartup = os.path.expanduser("~/.pystartup")
  with open(pystartup) as f:
    code_object = compile(f.read(), pystartup, 'exec')
    exec(code_object)

  parser = argparse.ArgumentParser()
  parser.add_argument('DSTDIR', default=tempfile.gettempdir(), nargs='?')
  args = parser.parse_args()
  print(args)
  
  destdir = args.DSTDIR
  if not os.path.isdir(destdir):
    os.mkdir(destdir)

  #if len(sys.argv)>1:
    #destdir = os.path.join('/tmp', sys.argv[1])
  #else:
    #destdir = tempfile.mkdtemp()

  #test2(destdir)
  #test3(destdir)
  #test5(destdir)
  #test6(destdir)

  generate_MV_refs(destdir)
  generate_MV_refs_LowIndexCavity(destdir)
  #print(example_function_7_theory())
  
  #generate_MV_refs_partial(destdir)
  
  print('destdir = ', destdir)
  return

if __name__ == "__main__":
  main()
