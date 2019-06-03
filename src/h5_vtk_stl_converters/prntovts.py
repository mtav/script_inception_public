#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: solve the problem of bfdtd parsing being py3 and vtk being py2 only... :/
# current quick sol: prn->h5 in py3 and h5tovts in py2

import os
import h5py
import numpy
import bfdtd.bfdtd_parser as bfdtd

def main():
  DATADIR = 'ANONYMIZED'
  raise
  BASENAME_fsnap = 'qedc3_2_05'
  BASENAME_esnap = 'qedc3_2_05_epsilon'

  geofile_fsnap = os.path.join(DATADIR, BASENAME_fsnap + '.geo')
  inpfile_fsnap = os.path.join(DATADIR, BASENAME_fsnap + '.inp')
  inpfile_esnap = os.path.join(DATADIR, BASENAME_esnap + '.inp')
  #h5file = os.path.join(DATADIR, BASENAME_fsnap + '.h5')
  h5file = os.path.join('/tmp', BASENAME_fsnap + '.h5')

  sim = bfdtd.BFDTDobject()
  sim.readBristolFDTD(geofile_fsnap)
  sim.readBristolFDTD(inpfile_fsnap)
  sim.readBristolFDTD(inpfile_esnap)

  fsnap_list = sim.getFrequencySnapshots()
  esnap_list = sim.getEpsilonSnapshots()
  
  
  N_fsnap = len(fsnap_list)
  N_esnap = len(esnap_list)
  
  print('N_fsnap = {}'.format(N_fsnap))
  print('N_esnap = {}'.format(N_esnap))
  
  
  with h5py.File(h5file, "w") as f:
    print('writing to ' + h5file)
    
    xmesh = sim.getXmesh()
    ymesh = sim.getYmesh()
    zmesh = sim.getZmesh()
    
    dset = f.create_dataset('/xmesh', xmesh.shape, dtype=numpy.float64)
    dset[...] = xmesh

    dset = f.create_dataset('/ymesh', ymesh.shape, dtype=numpy.float64)
    dset[...] = ymesh

    dset = f.create_dataset('/zmesh', zmesh.shape, dtype=numpy.float64)
    dset[...] = zmesh
    
    epsilon_group = f.create_group("epsilon_snapshots")
    fsnap_group = f.create_group("frequency_snapshots")

    for idx in range(N_esnap):
      fsnap = fsnap_list[idx]
      esnap = esnap_list[idx]
      f_plane = fsnap.plane
      e_plane = esnap.plane
      
      letter = ['x','y','z'][e_plane-1]
      plane_pos = list(set([
                          fsnap.P1[f_plane-1],
                          fsnap.P2[f_plane-1],
                          esnap.P1[e_plane-1],
                          esnap.P2[e_plane-1]
                        ]))
      plane_pos = plane_pos[0]
      print('{} = {}'.format(letter, plane_pos))

      dset = f.create_dataset('/epsilon_snapshots/idx={:0{fill_width}d}_{}={}'.format(idx, letter, plane_pos, fill_width = len(str(N_esnap))), ymesh.shape, dtype=numpy.float64)
      dset = f.create_dataset('/frequency_snapshots/idx={:0{fill_width}d}_{}={}'.format(idx, letter, plane_pos, fill_width = len(str(N_esnap))), ymesh.shape, dtype=numpy.float64)

  # set up argument parser
  
  # read in BFDTD input files to make sense of the .prn files
  
  # create a vts the size of the mesh
  
  # read in the .prn files
  
  # fill in the vts and HDF arrays
  
  # write the .vts file
  
  # write the .h5 file
  return 0

if __name__ == '__main__':
  main()
