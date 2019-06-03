#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# create a theoretical dipole "energy distribution"
# cf "Introduction to electrodynamics" by David J. Griffiths, p444-451

import numpy as np
import h5py
import subprocess

def cart2sph(X, Y, Z):
  X = np.array(X)
  Y = np.array(Y)
  Z = np.array(Z)
  
  azimuth = np.zeros(X.shape)
  elevation = np.zeros(X.shape)
  radius = np.zeros(X.shape)

  xy = X**2 + Y**2
  radius = np.sqrt(xy + Z**2)
  elevation = np.arctan2(np.sqrt(xy), Z) # for elevation angle defined from Z-axis down
  elevation = np.arctan2(Z, np.sqrt(xy)) # for elevation angle defined from XY plane
  azimuth = np.arctan2(Y, X)

  return (azimuth, elevation, radius)

def prettyprint(name, data):
  print('=== ' + name + ' ===')
  for i in range(data.shape[2]):
    print(data[:,:,i])

def main():
  x = np.linspace(-1, 1, 100)
  y = x
  z = x

  [X, Y, Z] = np.meshgrid(x,y,z)

  (azimuth, elevation, radius) = cart2sph(X,Y,Z)

  theta = elevation - np.pi/2
  S = ((np.sin(theta))**2)/(radius**2)
  log_S = np.log(S)

  #prettyprint('X', X)
  #prettyprint('Y', Y)
  #prettyprint('Z', Z)
  #prettyprint('azimuth', azimuth)
  #prettyprint('elevation', elevation)
  #prettyprint('radius', radius)

  h5file = 'dipole.h5'

  with h5py.File(h5file, "w") as f:
    print('writing to ' + h5file)

    dset = f.create_dataset('/X', X.shape, dtype='f')
    dset[...] = X

    dset = f.create_dataset('/Y', Y.shape, dtype='f')
    dset[...] = Y

    dset = f.create_dataset('/Z', Z.shape, dtype='f')
    dset[...] = Z

    dset = f.create_dataset('/azimuth', azimuth.shape, dtype='f')
    dset[...] = azimuth

    dset = f.create_dataset('/elevation', elevation.shape, dtype='f')
    dset[...] = elevation

    dset = f.create_dataset('/radius', radius.shape, dtype='f')
    dset[...] = radius
    
    dset = f.create_dataset('/S', S.shape, dtype='f')
    dset[...] = S

    dset = f.create_dataset('/log_S', log_S.shape, dtype='f')
    dset[...] = log_S
    
  subprocess.call(['h5tovtk','-o','dipole.X.vtk', 'dipole.h5:X'])
  subprocess.call(['h5tovtk','-o','dipole.Y.vtk', 'dipole.h5:Y'])
  subprocess.call(['h5tovtk','-o','dipole.Z.vtk', 'dipole.h5:Z'])

  subprocess.call(['h5tovtk','-o','dipole.azimuth.vtk', 'dipole.h5:azimuth'])
  subprocess.call(['h5tovtk','-o','dipole.elevation.vtk', 'dipole.h5:elevation'])
  subprocess.call(['h5tovtk','-o','dipole.radius.vtk', 'dipole.h5:radius'])

  subprocess.call(['h5tovtk','-o','dipole.S.vtk', 'dipole.h5:S'])
  subprocess.call(['h5tovtk','-o','dipole.log_S.vtk', 'dipole.h5:log_S'])

  return 0

if __name__ == '__main__':
	main()

