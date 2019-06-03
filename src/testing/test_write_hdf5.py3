#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def main():
  import h5py
  import numpy
  from utilities.common import unitVector
  
  h5file = '/tmp/test.h5'
  Nx,Ny,Nz = 30,40,50
  with h5py.File(h5file, "w") as f:
    data_tsnap = numpy.zeros([Nx,Ny,Nz], dtype=[('E', float, 3), ('H', float, 3), ('Pow', float), ('material', float)])
    data_fsnap = numpy.zeros([Nx,Ny,Nz], dtype=[('E', complex, 3), ('H', complex, 3)])
    for i in range(Nx):
      for j in range(Ny):
        for k in range(Nz):
          data_tsnap[i, j, k]['E'][0] = i
          data_tsnap[i, j, k]['E'][1] = j
          data_tsnap[i, j, k]['E'][2] = k
          data_tsnap[i, j, k]['H'][0] = i
          data_tsnap[i, j, k]['H'][1] = j
          data_tsnap[i, j, k]['H'][2] = k
          data_tsnap[i, j, k]['Pow'] = i+j+k

          xc=0.25
          yc=0
          zc=0
          x=-1/2+i*1/(Nx-1)
          y=-1/2+j*1/(Ny-1)
          z=-1/2+k*1/(Nz-1)
          dx = x-xc
          dy = y-yc
          dz = z-zc
          mag = numpy.sqrt(dx**2+dy**2+dz**2)
          angle_x = numpy.arctan2(dz,dy)
          angle_y = numpy.arctan2(dx,dz)
          angle_z = numpy.arctan2(dy,dx)
          
          e_r = unitVector([dx, dy, dz])
          e_theta = unitVector([-dy, dx, 0])
          e_phi = numpy.cross(e_r, e_theta)
          
          if mag < 0.25:
            data_tsnap[i, j, k]['material'] = 2
          else:
            data_tsnap[i, j, k]['material'] = 1
          
          #data_fsnap[i, j, k]['E'][0] = k*(i + 1j*j) + 0
          #data_fsnap[i, j, k]['E'][1] = k*(i + 1j*j) + 1
          #data_fsnap[i, j, k]['E'][2] = k*(i + 1j*j) + 2
          #data_fsnap[i, j, k]['E'][0] = abs(dx) * numpy.exp(1j*angle_x)
          #data_fsnap[i, j, k]['E'][1] = abs(dy) * numpy.exp(1j*angle_y)
          #data_fsnap[i, j, k]['E'][2] = abs(dz) * numpy.exp(1j*angle_z)
          
          #data_fsnap[i, j, k]['H'][0] = k*(i + 1j*j) + 3
          #data_fsnap[i, j, k]['H'][1] = k*(i + 1j*j) + 4
          #data_fsnap[i, j, k]['H'][2] = k*(i + 1j*j) + 5

          data_fsnap[i, j, k]['E'][0] = mag*e_theta[0]
          data_fsnap[i, j, k]['E'][1] = mag*e_theta[1]
          data_fsnap[i, j, k]['E'][2] = mag*e_theta[2]

          data_fsnap[i, j, k]['H'][0] = mag*e_phi[0]
          data_fsnap[i, j, k]['H'][1] = mag*e_phi[1]
          data_fsnap[i, j, k]['H'][2] = mag*e_phi[2]
    
    dset = f.create_dataset('data_tsnap', data=data_tsnap)
    dset = f.create_dataset('data_fsnap', data=data_fsnap)
    print('data written to {}'.format(h5file))
    
if __name__ == '__main__':
  main()
