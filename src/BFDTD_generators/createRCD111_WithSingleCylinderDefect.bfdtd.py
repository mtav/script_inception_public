#!/usr/bin/env python3

import os
import sys
import tempfile
from numpy.linalg.linalg import norm
from bfdtd.bfdtd_parser import BFDTDobject
from bfdtd.probe import Probe
from bfdtd.GeometryObjects import Cylinder, Rotation, Sphere, Block
from bfdtd.RCD import RCD_HexagonalLattice
from bfdtd.excitation import Excitation, ExcitationWithGaussianTemplate, ExcitationWithUniformTemplate
from constants.physcon import get_c0
from numpy import array, linspace, sqrt, zeros, ones
from bfdtd.meshobject import MeshObject
from meshing.meshing import linspaces

if __name__ == '__main__':

  # destination directory
  if len(sys.argv) > 1:
    DSTDIR = '.'
  else:
    DSTDIR = tempfile.gettempdir()

  # various .geo parameters
  cubic_unit_cell_size = 1 # cubic unit cell size
  r_RCD = 0.1 # RCD cylinder radius
  n_RCD = 2 # RCD cylinder refractive index
  r_defect = 0.2 # defect radius
  n_defect = 3 # defect refractive index
  n_backfill = 1 # backfill index

  # various .inp parameters
  fmin_normalized = 0.514079
  fmax_normalized = 0.55633
  fmin = fmin_normalized*get_c0()/cubic_unit_cell_size
  fmax = fmax_normalized*get_c0()/cubic_unit_cell_size
  N_iterations = 5e6
  walltime = 360

  # X meshing parameters
  xmesh_Ncells_bottom = 1
  xmesh_Ncells_RCD = 3
  xmesh_Ncells_top = 1

  # Y meshing parameters
  ymesh_Ncells_bottom = 1
  ymesh_Ncells_RCD = 3
  ymesh_Ncells_top = 1

  # Z meshing parameters
  zmesh_Ncells_bottom = 1
  zmesh_Ncells_RCD_1 = 3
  zmesh_Ncells_RCD_2 = 3
  zmesh_Ncells_top = 1

  # length of the dipole
  dipole_length = 0.5*sqrt(3)/4*cubic_unit_cell_size

  # distance of the probes to the excitation centre
  probe_distance = sqrt(3)/4*cubic_unit_cell_size

  # sizes in microns
  dim_x = 3
  dim_y = 3
  dim_z = 3

  # distances from sim to box walls
  buffer_x = 1
  buffer_y = 1
  buffer_z = 1

  # create an RCD object
  RCD = RCD_HexagonalLattice()
  RCD.setCubicUnitCellSize(cubic_unit_cell_size)
  RCD.setUnitCellType(2)
  RCD.setOuterRadius(r_RCD)
  RCD.setRefractiveIndex(n_RCD)

  # get lattice vectors
  (u,v,w) = RCD.getLatticeVectors()

  # get number of periods for a symmetrical woodpile within the desired dimensions
  Nx = int((dim_x/norm(u)+1)/2)
  Ny = int((dim_y/norm(v)+1)/2)
  Nz = int((dim_z/norm(w)+1)/2)

  # if you want a specific number of unit-cells
  #Nx = 2
  #Ny = 2
  #Nz = 2

  # print out number of periods
  print('Nx={} Ny={} Nz={}'.format(Nx,Ny,Nz))

  # create the desired array
  RCD.createRectangularArraySymmetrical(Nx,Ny,Nz)

  # create a BFDTDobject
  sim = BFDTDobject()
  sim.setDefaultRefractiveIndex(n_backfill)
  sim.setSizeAndResolution([dim_x+2*buffer_x, dim_y+2*buffer_y, dim_z+2*buffer_z],[1,1,1])
  sim.appendGeometryObject(RCD)

  # centre the RCD object in the simulation box
  RCD.setLocation(sim.box.getCentro())

  # get and remove the defect
  idx_defect = RCD.getIndexOf(0,0,0,'G2',0)
  geo_list = RCD.getGeoList()
  defect = geo_list.pop(idx_defect)

  # modify the defect
  defect.setRefractiveIndex(n_defect)
  defect.setOuterRadius(r_defect)
  defect.setName('defect')

  # re-add the defect
  geo_list.append(defect) # add defect at end
  #geo_list.insert(0, defect) # add defect at beginning

  # TODO: will probably require reworking the rotation system properly
  ## get some info in case you want to create your own custom defect
  #defect_location = defect.getLocation()
  #defect_rotation = defect.getRotation()
  #defect_size = defect.getSize()
  #new_defect = Block()
  #new_defect.setLocation(defect_location)
  #new_defect.setRotation(defect_rotation)
  #new_defect.setSize(defect_size)
  #geo_list.append(new_defect) # add defect at end

  # set simulation parameters
  sim.setIterations(N_iterations)
  sim.setFileBaseName('RCD')
  sim.setExecutable('fdtd64_2013')
  sim.setWallTime(walltime)

  ############
  # quick and dirty meshing...
  RCD_size_x = (2*Nx-1+1/2)*norm(u)
  RCD_size_y = (2*Ny-1+2/6)*norm(v)
  RCD_size_z = (2*Nz-1)*norm(w)

  RCD_min_x = -(Nx-1+1/2)*norm(u)
  RCD_min_y = -(Ny-1+1/2+1/6)*norm(v)
  RCD_min_z = -(Nz-1)*norm(w) - RCD.__offset2__[2]*cubic_unit_cell_size

  RCD_delta_x = ((2*Nx-1)*2+1)*[norm(u)/2]
  RCD_delta_y = ((2*Ny-1)*6+2)*[norm(v)/6]
  RCD_delta_z = (2*Nz-1)*3*[norm(w)/8, norm(w)/8, norm(w)/12]

  RCD_mesh = MeshObject()
  RCD_mesh.setXmeshDelta(RCD_delta_x)
  RCD_mesh.setYmeshDelta(RCD_delta_y)
  RCD_mesh.setZmeshDelta(RCD_delta_z)

  xmesh = [0]
  xmesh.extend(sim.box.getCentro()[0] + RCD_min_x + array(RCD_mesh.getXmesh()))
  xmesh.append(sim.box.getUpper()[0])

  ymesh = [0]
  ymesh.extend(sim.box.getCentro()[1] + RCD_min_y + array(RCD_mesh.getYmesh()))
  ymesh.append(sim.box.getUpper()[1])

  zmesh = [0]
  zmesh.extend(sim.box.getCentro()[2] + RCD_min_z + array(RCD_mesh.getZmesh()))
  zmesh.append(sim.box.getUpper()[2])

  xmesh_Ncells = ones(len(xmesh)-1)
  xmesh_Ncells[0] = xmesh_Ncells_bottom
  xmesh_Ncells[1:-1] = xmesh_Ncells_RCD
  xmesh_Ncells[-1] = xmesh_Ncells_top

  ymesh_Ncells = ones(len(ymesh)-1)
  ymesh_Ncells[0] = ymesh_Ncells_bottom
  ymesh_Ncells[1:-1] = ymesh_Ncells_RCD
  ymesh_Ncells[-1] = ymesh_Ncells_top

  zmesh_Ncells = ones(len(zmesh)-1)
  zmesh_Ncells[0] = zmesh_Ncells_bottom
  for i in range(1, len(zmesh_Ncells)-1, 3):
    zmesh_Ncells[i] = zmesh_Ncells_RCD_1
    zmesh_Ncells[i+1] = zmesh_Ncells_RCD_1
    zmesh_Ncells[i+2] = zmesh_Ncells_RCD_2
  zmesh_Ncells[-1] = zmesh_Ncells_top

  sim.mesh.setXmesh(linspaces(xmesh, xmesh_Ncells))
  sim.mesh.setYmesh(linspaces(ymesh, ymesh_Ncells))
  sim.mesh.setZmesh(linspaces(zmesh, zmesh_Ncells))

  print('{} cells'.format(sim.getNcells()))
  ############

  # define excitation location
  P_input_excitation = defect.getLocation()

  # add excitation
  excitation = sim.appendExcitation(Excitation())
  excitation.setName('input')
  excitation.setFrequencyRange(fmin,fmax)
  excitation.setCentro(P_input_excitation)

  # add probes
  probe_defect = sim.appendProbe(Probe())
  probe_defect.setPosition(P_input_excitation)
  probe_defect.setName('probe_defect_Centro')
  probe_defect.setStep(1)

  probe_defect = sim.appendProbe(Probe())
  probe_defect.setPosition(P_input_excitation + probe_distance*array([1,0,0]))
  probe_defect.setName('probe_defect_X')
  probe_defect.setStep(1)

  probe_defect = sim.appendProbe(Probe())
  probe_defect.setPosition(P_input_excitation + probe_distance*array([0,1,0]))
  probe_defect.setName('probe_defect_Y')
  probe_defect.setStep(1)

  probe_defect = sim.appendProbe(Probe())
  probe_defect.setPosition(P_input_excitation + probe_distance*array([0,0,1]))
  probe_defect.setName('probe_defect_Z')
  probe_defect.setStep(1)

  # write out simulation folders for Ex, Ey and Ez excitations
  excitation.setEx()
  excitation.setSize([dipole_length, 0, 0])
  sim.writeTorqueJobDirectory(DSTDIR+os.path.sep+'Ex')

  excitation.setEy()
  excitation.setSize([0, dipole_length, 0])
  sim.writeTorqueJobDirectory(DSTDIR+os.path.sep+'Ey')

  excitation.setEz()
  excitation.setSize([0, 0, dipole_length])
  sim.writeTorqueJobDirectory(DSTDIR+os.path.sep+'Ez')
