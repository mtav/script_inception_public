#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import copy
import tempfile
import argparse
import subprocess
import numpy

from numpy import array, linspace, sqrt, zeros, ones, floor, ceil
from numpy.linalg.linalg import norm
from constants.physcon import get_c0
#from utilities.createGUI import createGUI
from meshing.meshing import linspaces, HeterogeneousMesh1D, HomogeneousMesh1D, HomogeneousMeshParameters1D, Mesh1D, Mesh3D, MultiMesh1D, checkMesh, truncateMeshList

from .BFDTDobject import *
from .bfdtd_parser import *
from .snapshot import *
from .probe import *
from .GeometryObjects import *
from .RCD import RCD_HexagonalLattice, FRD_HexagonalLattice
from .excitation import Excitation, ExcitationWithGaussianTemplate, ExcitationWithUniformTemplate
from .meshobject import MeshObject
from .RCD_waveguides import RCD_HexagonalLattice_ChiralWaveguide

class RCD_FRD_111_hybrid():
  '''Creates RCD crystals, FRD crystals and/or adds waveguides and/or defects to them.
  Mainly created to easily add a GUI to it using the createGUI() system.

  .. todo:: Automatically write a file with the used parser settings into the output directory. (will be easier once we have our own file format supporting classes and their attributes of course. + BFDTD&co wrappers to run them) (or finally the proper GUI editor...)
  '''
  def __init__(self):

    super().__init__()

    #####
    #self.no_mesh_check = True

    # to enable mesh-check
    #self.minimum_mesh_delta = 1e-3
    #self.maximum_mesh_delta_ratio = 2

    # to disable mesh-check
    self.minimum_mesh_delta = None
    self.maximum_mesh_delta_ratio = None
    #####

    #self.maximum_mesh_delta_ratio = pow(2, 1/3)

    #self.minimum_mesh_delta = None
    #self.maximum_mesh_delta_ratio = None

    #############
    # destination directory
    self.outdir = tempfile.gettempdir()

    # various .geo parameters
    self.cubic_unit_cell_size = 1 # cubic unit cell size

    # TODO?: normalize all dimensions? If cubic_unit_cell_size cannot be set, there is no problem...
    self.r_RCD = 0.05 #: RCD cylinder radius

    # TODO: implement later...
    self.size_defect_x = None #: defect size in X (for block: used as X size) (for cylinder: used as diametre) (for sphere: used as diametre)
    self.size_defect_y = None #: defect size in Y (for block: used as Y size) (for cylinder: unused) (for sphere: unused)
    self.size_defect_z = None #: defect size in Z (for block: used as Z size) (for cylinder: used as height) (for sphere: unused)

    self.n_defect = 10*1.52 #: defect refractive index
    self.n_RCD = 1.52 #: RCD cylinder refractive index
    self.n_backfill = 3.3 #: backfill index

    # various .inp parameters
    self.fmin_normalized = 0.443428693424095
    self.fmax_normalized = 0.47508917574114

    self.N_iterations = 2e6
    self.walltime = 360

    ##### OPTION: Number of periods
    # if you want a specific number of unit-cells
    self.Nx = 2
    self.Ny = 2
    self.Nz = 2
    #####

    #################

    self.defect_position = 0.5
    self.crystal_type = 'RCD'
    self.defect_type = 'block'

    self.skip_Ex_writing = False
    self.skip_Ey_writing = False
    self.skip_Ez_writing = False

    self.BASENAME = 'RCD'

    # X meshing parameters
    self.xmesh_Ncells_bottom = 1 #98
    self.xmesh_Ncells_RCD = 1 #int(self.r_RCD*100) #24
    self.xmesh_Ncells_top = 1 #91

    # Y meshing parameters
    self.ymesh_Ncells_bottom = 1 #103
    self.ymesh_Ncells_RCD = 1 #int(self.r_RCD*60) #15
    self.ymesh_Ncells_top = 1 #103

    # Z meshing parameters
    self.zmesh_Ncells_bottom = 1 #5
    self.zmesh_Ncells_RCD_1 = 1 #10 #self.r_RCD*60 #15
    self.zmesh_Ncells_RCD_2 = 1 #1 #self.r_RCD*60 #15
    self.zmesh_Ncells_top = 1 #6

    # length of the dipole
    self.dipole_length = 0.2/4*sqrt(3)/4*self.cubic_unit_cell_size
    #self.dipole_length = 0.5*sqrt(3)/4*self.cubic_unit_cell_size
    #self.dipole_length = 0.5*sqrt(3)/4*self.cubic_unit_cell_size*0.3

    # distance of the probes to the excitation centre
    ##self.probe_distance = sqrt(3)/4*self.cubic_unit_cell_size
    self.probe_distance = self.dipole_length*2

    # size of the box (MINUS BUFFERS) in microns
    self.dim_x = 10
    self.dim_y = 10
    self.dim_z = 10

    # distances from sim to box walls
    self.buffer_x = 1 + sqrt(3)/8
    self.buffer_y = 1 + sqrt(3)/8
    self.buffer_z = 1 + sqrt(3)/8

    ###
    # TODO: another hack...? need to spend time on proper interface and automeshing, but no time...
    # the defect object to use
    #self.defect = None
    # an additional "virtual defect object", only used as reference when meshing
    #self.defect_reference = None
    ###


    return

  def setPeriodsFromDimensions(self, dim_x, dim_y, dim_z, offset):

    RCD = RCD_HexagonalLattice()
    RCD.setCubicUnitCellSize(self.cubic_unit_cell_size)
    RCD.setUnitCellType(2)

    (u,v,w) = RCD.getLatticeVectors()

    self.Nx = int(round( (dim_x/norm(u)+1)/2 ))
    self.Ny = int(round( (dim_y/norm(v)+1)/2 ))
    self.Nz = int(round( (dim_z/norm(w)+1)/2 ))

    x_mesh = RCD.getXMesh_with_SpacingMax(self.Nx, self.Ny, self.Nz, numpy.inf).getGlobalCoordinates()
    y_mesh = RCD.getYMesh_with_SpacingMax(self.Nx, self.Ny, self.Nz, numpy.inf).getGlobalCoordinates()
    z_mesh = RCD.getZMesh_with_SpacingMax(self.Nx, self.Ny, self.Nz, numpy.inf).getGlobalCoordinates()

    x_lower = x_mesh[0] - RCD.location[0] + offset[0]
    x_upper = x_mesh[-1] - RCD.location[0] + offset[0]
    new_dim_x = 2*max(abs(x_lower), abs(x_upper))

    y_lower = y_mesh[0] - RCD.location[1] + offset[1]
    y_upper = y_mesh[-1] - RCD.location[1] + offset[1]
    new_dim_y = 2*max(abs(y_lower), abs(y_upper))

    z_lower = z_mesh[0] - RCD.location[2] + offset[2]
    z_upper = z_mesh[-1] - RCD.location[2] + offset[2]
    new_dim_z = 2*max(abs(z_lower), abs(z_upper))

    #new_dim_x = (2*self.Nx-1)*norm(u)
    #new_dim_y = (2*self.Ny-1)*norm(v)
    #new_dim_z = (2*self.Nz-1)*norm(w)
    return (new_dim_x, new_dim_y, new_dim_z)

  def get_argument_parser(self):
    parser = argparse.ArgumentParser(description = self.__doc__.split('\n')[0], fromfile_prefix_chars='@')
    parser.add_argument('-d','--outdir', action="store", dest="outdir", default=tempfile.gettempdir(), help='output directory')
    parser.add_argument('-b','--basename', action="store", dest="basename", default=self.BASENAME, help='output basename')
    BFDTDobject.add_arguments(self, parser)
    self.add_arguments(parser)
    return parser

  def add_arguments(self, parser):
    parser.add_argument("--defect_type", help="defect_type", type=str, choices=['cylinder', 'block', 'sphere'],  default=self.defect_type)
    parser.add_argument("--defect_position", help="defect_position", type=float, default=self.defect_position)

    parser.add_argument("--size_defect_x", help="size_defect_x (if 0, defaults to RCD cylinder dimensions)", type=float, default=0)
    parser.add_argument("--size_defect_y", help="size_defect_y (if 0, defaults to RCD cylinder dimensions)", type=float, default=0)
    parser.add_argument("--size_defect_z", help="size_defect_z (if 0, defaults to RCD cylinder dimensions)", type=float, default=0)

    parser.add_argument("--n_defect", help="n_defect", type=float, default=self.n_defect)
    parser.add_argument("--n_RCD", help="n_RCD", type=float, default=self.n_RCD)
    parser.add_argument("--n_backfill", help="n_backfill", type=float, default=self.n_backfill)

    parser.add_argument("--Nx", help="Nx", type=int, default=self.Nx)
    parser.add_argument("--Ny", help="Ny", type=int, default=self.Ny)
    parser.add_argument("--Nz", help="Nz", type=int, default=self.Nz)

    parser.add_argument("--r_RCD", help="r_RCD", type=float, default=self.r_RCD)
    parser.add_argument("--fmin_normalized", help="fmin_normalized", type=float, default=self.fmin_normalized)
    parser.add_argument("--fmax_normalized", help="fmax_normalized", type=float, default=self.fmax_normalized)

    parser.add_argument("--skip_Ex_writing", help="skip_Ex_writing", action="store_true", default=False)
    parser.add_argument("--skip_Ey_writing", help="skip_Ey_writing", action="store_true", default=False)
    parser.add_argument("--skip_Ez_writing", help="skip_Ez_writing", action="store_true", default=False)

    parser.add_argument("--xmesh_Ncells_bottom", help="xmesh_Ncells_bottom", type=int, default=self.xmesh_Ncells_bottom)
    parser.add_argument("--xmesh_Ncells_RCD", help="xmesh_Ncells_RCD", type=int, default=self.xmesh_Ncells_RCD)
    parser.add_argument("--xmesh_Ncells_top", help="xmesh_Ncells_top", type=int, default=self.xmesh_Ncells_top)
    parser.add_argument("--ymesh_Ncells_bottom", help="ymesh_Ncells_bottom", type=int, default=self.ymesh_Ncells_bottom)
    parser.add_argument("--ymesh_Ncells_RCD", help="ymesh_Ncells_RCD", type=int, default=self.ymesh_Ncells_RCD)
    parser.add_argument("--ymesh_Ncells_top", help="ymesh_Ncells_top", type=int, default=self.ymesh_Ncells_top)
    parser.add_argument("--zmesh_Ncells_bottom", help="zmesh_Ncells_bottom", type=int, default=self.zmesh_Ncells_bottom)
    parser.add_argument("--zmesh_Ncells_RCD_1", help="zmesh_Ncells_RCD_1", type=int, default=self.zmesh_Ncells_RCD_1)
    parser.add_argument("--zmesh_Ncells_RCD_2", help="zmesh_Ncells_RCD_2", type=int, default=self.zmesh_Ncells_RCD_2)
    parser.add_argument("--zmesh_Ncells_top", help="zmesh_Ncells_top", type=int, default=self.zmesh_Ncells_top)

    parser.add_argument("--dipole_length", help="dipole_length", type=float, default=self.dipole_length)
    parser.add_argument("--probe_distance", help="probe_distance", type=float, default=self.probe_distance)
    parser.add_argument("--dim_x", help="dim_x", type=float, default=self.dim_x)
    parser.add_argument("--dim_y", help="dim_y", type=float, default=self.dim_y)
    parser.add_argument("--dim_z", help="dim_z", type=float, default=self.dim_z)
    parser.add_argument("--buffer_x", help="buffer_x", type=float, default=self.buffer_x)
    parser.add_argument("--buffer_y", help="buffer_y", type=float, default=self.buffer_y)
    parser.add_argument("--buffer_z", help="buffer_z", type=float, default=self.buffer_z)

    return

  def writeFromParsedOptions(self, options):
    print ("Options: ", options)
    self.setAttributesFromParsedOptions(options)
    self.write()
    return

  def setAttributesFromParsedOptions(self, options):
    BFDTDobject.setAttributesFromParsedOptions(self, options)

    #for key, val in options.__dict__.items():
      ##print((key, val))
      #print('self.{0} = options.{0}'.format(key))

    self.outdir = options.outdir
    self.BASENAME = options.basename

    self.defect_type = options.defect_type
    self.defect_position = options.defect_position

    if options.size_defect_x > 0:
      self.size_defect_x = options.size_defect_x
    else:
      self.size_defect_x = None
    if options.size_defect_y > 0:
      self.size_defect_y = options.size_defect_y
    else:
      self.size_defect_y = None
    if options.size_defect_z > 0:
      self.size_defect_z = options.size_defect_z
    else:
      self.size_defect_z = None

    self.n_defect = options.n_defect
    self.n_RCD = options.n_RCD
    self.n_backfill = options.n_backfill

    self.Nx = options.Nx
    self.Ny = options.Ny
    self.Nz = options.Nz

    self.r_RCD = options.r_RCD
    self.fmin_normalized = options.fmin_normalized
    self.fmax_normalized = options.fmax_normalized

    self.skip_Ex_writing = options.skip_Ex_writing
    self.skip_Ey_writing = options.skip_Ey_writing
    self.skip_Ez_writing = options.skip_Ez_writing

    self.xmesh_Ncells_bottom = options.xmesh_Ncells_bottom
    self.xmesh_Ncells_RCD = options.xmesh_Ncells_RCD
    self.xmesh_Ncells_top = options.xmesh_Ncells_top
    self.ymesh_Ncells_bottom = options.ymesh_Ncells_bottom
    self.ymesh_Ncells_RCD = options.ymesh_Ncells_RCD
    self.ymesh_Ncells_top = options.ymesh_Ncells_top
    self.zmesh_Ncells_bottom = options.zmesh_Ncells_bottom
    self.zmesh_Ncells_RCD_1 = options.zmesh_Ncells_RCD_1
    self.zmesh_Ncells_RCD_2 = options.zmesh_Ncells_RCD_2
    self.zmesh_Ncells_top = options.zmesh_Ncells_top

    self.dipole_length = options.dipole_length
    self.probe_distance = options.probe_distance
    self.dim_x = options.dim_x
    self.dim_y = options.dim_y
    self.dim_z = options.dim_z
    self.buffer_x = options.buffer_x
    self.buffer_y = options.buffer_y
    self.buffer_z = options.buffer_z

    return

  def getRodLength(self):
    self.setupRCD()
    return self.RCD.getRodLength()

  def setupRCD(self):
    # create an RCD object

    ##### OPTION: RCD or FRD
    self.RCD = RCD_HexagonalLattice()
    #self.RCD = FRD_HexagonalLattice()
    #self.RCD.RCD_on = True
    #self.RCD.refractive_index_RCD = 1
    #self.RCD.FRD_on = True
    #self.RCD.refractive_index_FRD = 10
    #####

    self.RCD.setCubicUnitCellSize(self.cubic_unit_cell_size)
    self.RCD.setUnitCellType(2)
    self.RCD.setOuterRadius(self.r_RCD)
    self.RCD.setRefractiveIndex(self.n_RCD)
    return

  def setupMesh(self):
    print('=== MESHING START ===')
    Ncells = numpy.inf
    NCELLS_MAX = 10e6  # 2015-01-27
    #denom = 15 # 2015-01-27
    #NCELLS_MAX = 1e9
    denom = 50
    while(Ncells > NCELLS_MAX and denom >= 1):
      meshing_factor = 1/denom
      #meshing_factor = numpy.inf

      L = get_c0()/self.fmax
      self.xmesh_Ncells_box = meshing_factor*L/self.n_backfill
      self.xmesh_Ncells_RCDouter = meshing_factor*L/max(self.n_RCD,self.n_backfill)
      self.xmesh_Ncells_RCDinner = meshing_factor*L/max(self.n_RCD,self.n_backfill)
      self.xmesh_Ncells_defect = meshing_factor*L/self.n_defect

      self.ymesh_Ncells_box = meshing_factor*L/self.n_backfill
      self.ymesh_Ncells_RCDouter = meshing_factor*L/max(self.n_RCD,self.n_backfill)
      self.ymesh_Ncells_RCDinner = meshing_factor*L/max(self.n_RCD,self.n_backfill)
      self.ymesh_Ncells_defect = meshing_factor*L/self.n_defect

      self.zmesh_Ncells_box = meshing_factor*L/self.n_backfill
      self.zmesh_Ncells_RCDouter = meshing_factor*L/max(self.n_RCD,self.n_backfill)
      self.zmesh_Ncells_RCDinner = meshing_factor*L/max(self.n_RCD,self.n_backfill)
      self.zmesh_Ncells_defect = meshing_factor*L/self.n_defect

      self.X_mesh = self.getXmesh(self.sim, self.RCD, self.defect_reference_for_meshing, self.crystal_mesh_boundary.getLowerAbsolute()[0], self.crystal_mesh_boundary.getUpperAbsolute()[0])
      self.sim.mesh.setXmesh(self.X_mesh.getGlobalCoordinates())
      self.Y_mesh = self.getYmesh(self.sim, self.RCD, self.defect_reference_for_meshing, self.crystal_mesh_boundary.getLowerAbsolute()[1], self.crystal_mesh_boundary.getUpperAbsolute()[1])
      self.sim.mesh.setYmesh(self.Y_mesh.getGlobalCoordinates())
      self.Z_mesh = self.getZmesh(self.sim, self.RCD, self.defect_reference_for_meshing, self.crystal_mesh_boundary.getLowerAbsolute()[2], self.crystal_mesh_boundary.getUpperAbsolute()[2])
      self.sim.mesh.setZmesh(self.Z_mesh.getGlobalCoordinates())

      Ncells = self.sim.getNcells()
      #print((denom, meshing_factor, Ncells, Ncells > 10e6, denom >= 1))

      #break
      denom = denom - 0.1

    print('denom={}, meshing_factor={}, Ncells={}, Ncells > NCELLS_MAX={}: {}, denom >= 1: {}'.format(denom, meshing_factor, Ncells, NCELLS_MAX, Ncells > NCELLS_MAX, denom >= 1))

    # mesh check
    try:
      print('checking X_mesh')
      (delta_min, ratio_max, delta_min_idx, ratio_max_idx) = checkMesh(self.sim.mesh.getXmesh(), self.minimum_mesh_delta, self.maximum_mesh_delta_ratio)
      print('Xmesh: delta_min={}, ratio_max={}, delta_min_idx={}, ratio_max_idx={} at {}'.format(delta_min, ratio_max, delta_min_idx, ratio_max_idx, self.sim.mesh.getXmesh()[ratio_max_idx]))

      print('checking Y_mesh')
      (delta_min, ratio_max, delta_min_idx, ratio_max_idx) = checkMesh(self.sim.mesh.getYmesh(), self.minimum_mesh_delta, self.maximum_mesh_delta_ratio)
      print('Ymesh: delta_min={}, ratio_max={}, delta_min_idx={}, ratio_max_idx={} at {}'.format(delta_min, ratio_max, delta_min_idx, ratio_max_idx, self.sim.mesh.getYmesh()[ratio_max_idx]))

      print('checking Z_mesh')
      (delta_min, ratio_max, delta_min_idx, ratio_max_idx) = checkMesh(self.sim.mesh.getZmesh(), self.minimum_mesh_delta, self.maximum_mesh_delta_ratio)
      print('Zmesh: delta_min={}, ratio_max={}, delta_min_idx={}, ratio_max_idx={} at {}'.format(delta_min, ratio_max, delta_min_idx, ratio_max_idx, self.sim.mesh.getZmesh()[ratio_max_idx]))
    except:
      self.excitation.setEx()
      self.excitation.setSize([self.dipole_length, 0, 0])
      self.sim.writeTorqueJobDirectory(self.outdir+os.path.sep+'Ex')
      raise

    print('=== MESHING END ===')
    return

  def write(self):

    # set real fmin/fmax based on normalized frequencies
    self.fmin = self.fmin_normalized*get_c0()/self.cubic_unit_cell_size
    self.fmax = self.fmax_normalized*get_c0()/self.cubic_unit_cell_size

    self.setupRCD()

    # get lattice vectors
    (u,v,w) = self.RCD.getLatticeVectors()

    # print out number of periods
    print('Nx={} Ny={} Nz={}'.format(self.Nx,self.Ny,self.Nz))

    # create the desired array
    #self.RCD.createRectangularArraySymmetrical(self.Nx,self.Ny,self.Nz)

    # create a BFDTDobject
    self.sim = BFDTDobject()
    self.sim.setDefaultRefractiveIndex(self.n_backfill)
    self.sim.setSizeAndResolution([self.dim_x+2*self.buffer_x, self.dim_y+2*self.buffer_y, self.dim_z+2*self.buffer_z],[1,1,1])

    ##### OPTION: Position crystal
    # centre the RCD object in the simulation box

    #self.RCD.setLocation(self.sim.box.getCentro()) # cylinder centre = box centre
    #self.RCD.setLocation(self.sim.box.getCentro() + array([0, 0, 0.5*self.RCD.getRodLength()])) # cylinder end = box centre (sphere position)
    #self.RCD.setLocation(self.sim.box.getCentro() + array([0, 0, 1.5*self.RCD.getRodLength()])) # self.RCD unit cube centre = box centre
    self.RCD.setLocation(self.sim.box.getCentro() + array([0, 0, self.defect_position*self.RCD.getRodLength()]))
    #####

    xmin = self.buffer_x
    ymin = self.buffer_y
    zmin = self.buffer_z
    xmax = self.buffer_x + self.dim_x
    ymax = self.buffer_y + self.dim_y
    zmax = self.buffer_z + self.dim_z

    size_max_X = 2*max( abs(xmax - self.RCD.location[0]), abs(xmin - self.RCD.location[0]) )
    size_max_Y = 2*max( abs(ymax - self.RCD.location[1]), abs(ymin - self.RCD.location[1]) )
    size_max_Z = 2*max( abs(zmax - self.RCD.location[2]), abs(zmin - self.RCD.location[2]) )

    Nx_max = int(ceil( (size_max_X/norm(u)+1)/2 ))
    Ny_max = int(ceil( (size_max_Y/norm(v)+1)/2 ))
    Nz_max = int(ceil( (size_max_Z/norm(w)+1)/2 ))
    print('Nx_max={}, Ny_max={}, Nz_max={}'.format(Nx_max, Ny_max, Nz_max))

    self.Nx = Nx_max
    self.Ny = Ny_max
    self.Nz = Nz_max

    self.RCD.createRectangularArraySymmetrical(Nx_max, Ny_max, Nz_max)
    #RCD.createRectangularArraySymmetrical(1, 1, 2)

    #unit_cell_ref = BFDTDobject()
    #unit_cell1 = self.RCD.getCubicUnitCell()
    #unit_cell2 = self.RCD.getCubicUnitCell()
    #unit_cell2.translate([0, 0, self.RCD.getRodLength()])
    #unit_cell_ref.appendGeometryObject(unit_cell1)
    #unit_cell_ref.appendGeometryObject(unit_cell2)
    ##### OPTION: Show cubic unit cells (disable for simulations)
    #self.sim.appendGeometryObject(unit_cell1)
    #self.sim.appendGeometryObject(unit_cell2)
    #####

    # get list of objects
    geo_list = self.RCD.getGeoList()
    geo_list = truncateGeoList(geo_list, xmin, xmax, ymin, ymax, zmin, zmax)
    print((xmin, xmax, ymin, ymax, zmin, zmax))

    self.sim.appendGeometryObject(geo_list)

    crystal_geo_boundary = Block()
    crystal_geo_boundary.name = "crystal_geo_boundary"
    crystal_geo_boundary.setLowerAbsolute([xmin, ymin, zmin])
    crystal_geo_boundary.setUpperAbsolute([xmax, ymax, zmax])
    #self.sim.appendGeometryObject(crystal_geo_boundary)

    self.crystal_mesh_boundary = Block()
    self.crystal_mesh_boundary.name = "self.crystal_mesh_boundary"
    self.crystal_mesh_boundary.setLowerAbsolute([xmin-0.5*self.RCD.getRodLength(), ymin-0.5*self.RCD.getRodLength(), zmin-0.5*self.RCD.getRodLength()])
    self.crystal_mesh_boundary.setUpperAbsolute([xmax+0.5*self.RCD.getRodLength(), ymax+0.5*self.RCD.getRodLength(), zmax+0.5*self.RCD.getRodLength()])
    #self.sim.appendGeometryObject(self.crystal_mesh_boundary)

    # get and remove the defect
    #idx_defect = RCD.getIndexOf(0,0,0,'G2',0)
    #defect = geo_list.pop(idx_defect)

    ##### OPTION: Choose defect type and settings

    defect_reference = Block()

    if self.defect_type == 'cylinder':
      # create cylinder defect
      defect = Cylinder()
      if self.size_defect_z is None:
        defect.setHeight(self.RCD.getRodLength())
      else:
        defect.setHeight(self.size_defect_z)
      #defect.setAxis(array([1,0,0]))
      #defect.setAxis(array([0,1,0]))
      defect.setAxis(array([0,0,1]))
      #defect.setAxis(array([1,1,1]))
      #defect.setStartEndPoints(self.sim.box.getCentro()+array([-1,0,0]),self.sim.box.getCentro()+array([1,1,1]))
      if self.size_defect_x is None:
        defect.setOuterRadius(self.RCD.getOuterRadius())
      else:
        defect.setOuterRadius(0.5*self.size_defect_x)

      defect_reference.setSize([2*defect.getOuterRadius(), 2*defect.getOuterRadius(), defect.getHeight()])
      #defect_reference.setSize([2*self.RCD.getOuterRadius(), 2*self.RCD.getOuterRadius(), self.RCD.getRodLength()])

    elif self.defect_type == 'block':
      # create block defect
      defect = Block()
      #defect.setSize([4*self.r_defect, 5*self.r_defect, 6*self.r_defect])
      if self.size_defect_x is None:
        Sx = 2*self.RCD.getOuterRadius()
      else:
        Sx = self.size_defect_x

      if self.size_defect_y is None:
        Sy = 2*self.RCD.getOuterRadius()
      else:
        Sy = self.size_defect_y

      if self.size_defect_z is None:
        Sz = self.RCD.getRodLength()
      else:
        Sz = self.size_defect_z

      defect.setSize([Sx, Sy, Sz])
      defect_reference.setSize(defect.getSize())

    elif self.defect_type == 'sphere':
      # create sphere defect
      defect = Sphere()
      defect.setInnerRadius(0)
      R = self.RCD.getOuterRadius()
      H = self.RCD.getRodLength()
      V1 = numpy.pi*pow(R, 2)*H
      V2 = pow(2*R, 2)*H
      R1 = pow(V1, 1/3)
      R2 = pow(V2, 1/3)
      #defect.setOuterRadius(self.RCD.getOuterRadius())

      if self.size_defect_x is None:
        defect.setOuterRadius(H/2)
      else:
        defect.setOuterRadius(0.5*self.size_defect_x)
      #defect.setOuterRadius(R1)
      #defect.setOuterRadius(R2)

      defect_reference.setSize(defect.getSize())

    else:
      raise Exception('self.defect_type = {}'.format(self.defect_type))

    # another "virtual defect" hack for meshing...
    self.defect_reference_for_meshing = Block()
    self.defect_reference_for_meshing.setSize([self.RCD.getOuterRadius() ,self.RCD.getOuterRadius() , self.RCD.getRodLength()])
    #####

    # general settings
    defect.setLocation(self.sim.box.getCentro())
    defect_reference.setLocation(self.sim.box.getCentro())
    self.defect_reference_for_meshing.setLocation(self.sim.box.getCentro())
    defect.setRefractiveIndex(self.n_defect)
    defect.setName('defect')

    # re-add the defect
    #geo_list.append(defect) # add defect at end
    self.sim.appendGeometryObject(defect)
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

    #########################################################################
    ## waveguide
    #waveguide = self.RCD_HexagonalLattice_ChiralWaveguide()
    #waveguide.chirality = 'left'
    #waveguide.createRectangularArraySymmetrical(3,3,2)
    #waveguide.setRefractiveIndex(5)
    #(wg_u, wg_v, wg_w) = waveguide.getLatticeVectors()
    #waveguide.setLocation(self.RCD.getLocation())
    #waveguide.setLocation(self.RCD.getLocation() + 0.5*wg_w)

    #waveguide.use_spheres = True
    #waveguide.use_cylinders = True
    #waveguide.add_bottom_sphere = True
    #waveguide.relative_sphere_radius = 2
    #waveguide.relative_sphere_index = 2

    #self.sim.appendGeometryObject(waveguide)

    ########################################################################
    ## second RCD
    #foo = copy.deepcopy(self.RCD)
    #foo.setRefractiveIndex(20)
    #foo.setLocation(self.RCD.getLocation() + 0.5*wg_w)
    #foo.RCD_on = True
    #foo.refractive_index_RCD = 2
    #foo.FRD_on = True
    #foo.refractive_index_FRD = 3
    #foo.clearGeoList()
    #foo.createRectangularArraySymmetrical(1,1,1)

    ##self.sim.clearGeometry()
    #self.sim.appendGeometryObject(foo)
    #print(self.sim.getGeometryObjects())

    ##raise()

    ########################################################################
    # set simulation parameters
    self.sim.setIterations(self.N_iterations)
    self.sim.setFileBaseName(self.BASENAME)
    self.sim.setExecutable('fdtd64_2013')
    self.sim.setWallTime(self.walltime)

    #########################################################################
    ## WIP...
    ## RCD_mesh = self.RCD.getMeshObject(self.Nx, self.Ny, self.Nz)

    ## quick and dirty meshing...
    #(u,v,w) = self.RCD.getLatticeVectors()

    #RCD_size_x = (2*self.Nx-1+1/2)*norm(u)
    #RCD_size_y = (2*self.Ny-1+2/6)*norm(v)
    ##RCD_size_z = (2*self.Nz-1)*norm(w) + RCD.getRodLength()
    #RCD_size_z = (2*self.Nz-1)*norm(w)

    #RCD_min_x = -(self.Nx-1+1/2)*norm(u)
    #RCD_min_y = -(self.Ny-1+1/2+1/6)*norm(v)
    ##RCD_min_z = -(self.Nz-1)*norm(w) - RCD.__offset2__[2]*RCD.cubic_unit_cell_size - RCD.getRodLength()
    #RCD_min_z = -(self.Nz-1)*norm(w) - RCD.__offset2__[2]*RCD.cubic_unit_cell_size

    #RCD_delta_x = ((2*self.Nx-1)*2+1)*[norm(u)/2]
    #RCD_delta_y = ((2*self.Ny-1)*6+2)*[norm(v)/6]
    #RCD_delta_z = RCD_size_z
    ##(2*self.Nz-1)*3*[norm(w)/8, norm(w)/8, norm(w)/12]

    #RCD_mesh = MeshObject()
    #RCD_mesh.setXmeshDelta(RCD_delta_x)
    #RCD_mesh.setYmeshDelta(RCD_delta_y)
    #RCD_mesh.setZmeshDelta(RCD_delta_z)

    #xmesh = [0]
    #xmesh.extend(RCD.getLocation()[0] + RCD_min_x + array(RCD_mesh.getXmesh()))
    #xmesh.append(self.sim.box.getUpper()[0])

    #ymesh = [0]
    #ymesh.extend(RCD.getLocation()[1] + RCD_min_y + array(RCD_mesh.getYmesh()))
    #ymesh.append(self.sim.box.getUpper()[1])

    #zmesh = [0]
    #zmesh.extend(RCD.getLocation()[2] + RCD_min_z + array(RCD_mesh.getZmesh()))
    #zmesh.append(self.sim.box.getUpper()[2])

    #xmesh_Ncells = ones(len(xmesh)-1)
    #xmesh_Ncells[0] = self.xmesh_Ncells_bottom
    #xmesh_Ncells[1:-1] = self.xmesh_Ncells_RCD
    #xmesh_Ncells[-1] = self.xmesh_Ncells_top

    #ymesh_Ncells = ones(len(ymesh)-1)
    #ymesh_Ncells[0] = self.ymesh_Ncells_bottom
    #ymesh_Ncells[1:-1] = self.ymesh_Ncells_RCD
    #ymesh_Ncells[-1] = self.ymesh_Ncells_top

    #zmesh_Ncells = ones(len(zmesh)-1)
    #zmesh_Ncells[0] = self.zmesh_Ncells_bottom
    #zmesh_Ncells[1] = self.zmesh_Ncells_RCD_1
    ##for i in range(1, len(zmesh_Ncells)-1, 3):
      ##zmesh_Ncells[i] = self.zmesh_Ncells_RCD_1
      ##zmesh_Ncells[i+1] = self.zmesh_Ncells_RCD_1
      ##zmesh_Ncells[i+2] = self.zmesh_Ncells_RCD_2
    #zmesh_Ncells[-1] = self.zmesh_Ncells_top

    ##self.sim.mesh.setXmesh(linspaces(xmesh, xmesh_Ncells))
    ##self.sim.mesh.setYmesh(linspaces(ymesh, ymesh_Ncells))
    ##self.sim.mesh.setZmesh(linspaces(zmesh, zmesh_Ncells))
    ##self.sim.mesh.setZmesh(zmesh)

    ##print('{} cells'.format(self.sim.getNcells()))
    #########################################################################
    #RCDouter = RCD
    #RCDinner = copy.deepcopy(RCD)
    #RCDinner.createRectangularArraySymmetrical(1, 1, 1)

    ########################################################################
    #self.dipole_length = 2*1/15*(get_c0()/self.fmax)/self.n_defect
    #self.probe_distance = self.dipole_length*2
    self.probe_distance = min(defect_reference.getSize()) / 4

    # define excitation location
    P_input_excitation = defect.getLocation()

    # add excitation
    self.excitation = self.sim.appendExcitation(Excitation())
    self.excitation.setName('input')
    self.excitation.setFrequencyRange(self.fmin, self.fmax, autofix=True)
    self.excitation.setCentro(P_input_excitation)
    self.excitation.setTimeOffset()

    # add probes
    probe_defect = self.sim.appendProbe(Probe())
    probe_defect.setPosition(P_input_excitation)
    probe_defect.setName('probe_defect_Centro')
    probe_defect.setStep(1)

    probe_defect = self.sim.appendProbe(Probe())
    probe_defect.setPosition(P_input_excitation + self.probe_distance*array([1,0,0]))
    probe_defect.setName('probe_defect_X')
    probe_defect.setStep(1)

    probe_defect = self.sim.appendProbe(Probe())
    probe_defect.setPosition(P_input_excitation + self.probe_distance*array([0,1,0]))
    probe_defect.setName('probe_defect_Y')
    probe_defect.setStep(1)

    probe_defect = self.sim.appendProbe(Probe())
    probe_defect.setPosition(P_input_excitation + self.probe_distance*array([0,0,1]))
    probe_defect.setName('probe_defect_Z')
    probe_defect.setStep(1)

    ########################################################################
    self.setupMesh()
    ########################################################################

    #unit_cell_ref.writeGeoFile(self.outdir + os.sep + 'unit_cell_ref.geo')

    ########################################################################
    # write out simulation folders for Ex, Ey and Ez excitations
    # TODO: Create new Ex/Ey/Ez writing function since we do it all the time...
    # TODO: split this into separate function so user can more easily write geo, inp, etc only... (this class should really be a BFDTDobject or a GeometryObject subclass...)
    if not self.skip_Ex_writing:
      self.excitation.setEx()
      self.excitation.setSize([self.dipole_length, 0, 0])
      self.sim.writeTorqueJobDirectory(self.outdir+os.path.sep+'Ex')

    if not self.skip_Ey_writing:
      self.excitation.setEy()
      self.excitation.setSize([0, self.dipole_length, 0])
      self.sim.writeTorqueJobDirectory(self.outdir+os.path.sep+'Ey')

    if not self.skip_Ez_writing:
      self.excitation.setEz()
      self.excitation.setSize([0, 0, self.dipole_length])
      self.sim.writeTorqueJobDirectory(self.outdir+os.path.sep+'Ez')

    # open blender directly
    #subprocess.call(['import_BFDTD.sh','/tmp/Ex/RCD.in'])

    filepath = self.outdir + os.sep + 'Ex' + os.sep + self.BASENAME
    return self.sim, filepath, self.X_mesh, self.Y_mesh, self.Z_mesh

  def getXmesh(self, sim, RCD, defect, lower, upper):
    X_mesh_box = HomogeneousMeshParameters1D(pos_min = sim.box.getLower()[0], pos_max = sim.box.getUpper()[0])
    X_mesh_box.name = 'X_mesh_box'
    X_mesh_box.setSpacingMax(self.xmesh_Ncells_box)

    X_mesh_RCDouter = RCD.getXMesh_with_SpacingMax(self.Nx, self.Ny, self.Nz, self.xmesh_Ncells_RCDouter)
    X_mesh_RCDouter.name = 'X_mesh_RCDouter'
    X_mesh_RCDouter.mesh_list = truncateMeshList(X_mesh_RCDouter.mesh_list, lower, upper)

    X_mesh_RCDinner = RCD.getXMesh_with_SpacingMax(1, 1, 1, self.xmesh_Ncells_RCDinner)
    X_mesh_RCDinner.name = 'X_mesh_RCDinner'
    X_mesh_RCDinner.mesh_list = truncateMeshList(X_mesh_RCDinner.mesh_list, lower, upper)

    #X_mesh_defect.location = defect.getLocation()[0]

    #X_mesh_defect1 = HomogeneousMeshParameters1D(pos_min = defect.getLowerAbsolute()[0], pos_max = defect.getLocation()[0])
    #X_mesh_defect1.name = 'X_mesh_defect1'
    #X_mesh_defect1.setSpacingMax(self.xmesh_Ncells_defect)
    #X_mesh_defect1.nukeothers = True

    #X_mesh_defect2 = HomogeneousMeshParameters1D(pos_min = defect.getLocation()[0], pos_max = defect.getUpperAbsolute()[0])
    #X_mesh_defect2.name = 'X_mesh_defect2'
    #X_mesh_defect2.setSpacingMax(self.xmesh_Ncells_defect)
    #X_mesh_defect2.nukeothers = True

    defect_region_limits = [defect.getLowerAbsolute()[0],                     #0 setSpacingMax
                            #defect.getLocation()[0] - self.probe_distance,    #1 setNcellsMin(3)
                            #defect.getLocation()[0] - 0.5*self.dipole_length, #2 setNcellsMin(1)
                            defect.getLocation()[0],                          #3 setNcellsMin(1)
                            #defect.getLocation()[0] + 0.5*self.dipole_length, #4 setNcellsMin(3)
                            #defect.getLocation()[0] + self.probe_distance,    #5 setSpacingMax
                            defect.getUpperAbsolute()[0]]                     #6

    X_mesh_defect = MultiMesh1D()
    for idx in range(len(defect_region_limits)-1):
      m = HomogeneousMeshParameters1D(pos_min = defect_region_limits[idx], pos_max = defect_region_limits[idx+1])
      m.name = 'X_mesh_defect'
      #m.setSpacingMax(self.xmesh_Ncells_defect)
      m.setSpacingMax(numpy.inf)
      m.nukeothers = True
      X_mesh_defect.addChild(m)

    #print(self.xmesh_Ncells_defect)
    #raise
    for i in X_mesh_defect.mesh_list:
      i.setSpacingMax(self.xmesh_Ncells_defect)

    #X_mesh_defect.mesh_list[0].setSpacingMax(self.xmesh_Ncells_defect)
    #X_mesh_defect.mesh_list[1].setSpacingMax(self.xmesh_Ncells_defect)
    #X_mesh_defect.mesh_list[2].setSpacingMax(self.xmesh_Ncells_defect)
    #X_mesh_defect.mesh_list[3].setSpacingMax(self.xmesh_Ncells_defect)
    #X_mesh_defect.mesh_list[4].setSpacingMax(self.xmesh_Ncells_defect)
    #X_mesh_defect.mesh_list[5].setSpacingMax(self.xmesh_Ncells_defect)

    X_mesh = MultiMesh1D()
    X_mesh.name = 'X_mesh'
    X_mesh.addChild(X_mesh_box)
    X_mesh.addChild(X_mesh_RCDouter)
    X_mesh.addChild(X_mesh_RCDinner)
    X_mesh.addChild(X_mesh_defect)
    #if self.no_mesh_check:
      #X_mesh.maximum_mesh_delta_ratio = None
      #X_mesh.minimum_mesh_delta = None
    return(X_mesh)

  def getYmesh(self, sim, RCD, defect, lower, upper):
    Y_mesh_box = HomogeneousMeshParameters1D(pos_min = sim.box.getLower()[1], pos_max = sim.box.getUpper()[1])
    Y_mesh_box.name = 'Y_mesh_box'
    Y_mesh_box.setSpacingMax(self.ymesh_Ncells_box)

    Y_mesh_RCDouter = RCD.getYMesh_with_SpacingMax(self.Nx, self.Ny, self.Nz, self.ymesh_Ncells_RCDouter)
    Y_mesh_RCDouter.name = 'Y_mesh_RCDouter'
    Y_mesh_RCDouter.mesh_list = truncateMeshList(Y_mesh_RCDouter.mesh_list, lower, upper)

    Y_mesh_RCDinner = RCD.getYMesh_with_SpacingMax(1, 1, 1, self.ymesh_Ncells_RCDinner)
    Y_mesh_RCDinner.name = 'Y_mesh_RCDinner'
    Y_mesh_RCDinner.mesh_list = truncateMeshList(Y_mesh_RCDinner.mesh_list, lower, upper)

    #Y_mesh_defect.location = defect.getLocation()[1]

    #Y_mesh_defect1 = HomogeneousMeshParameters1D(pos_min = defect.getLowerAbsolute()[1], pos_max = defect.getLocation()[1])
    #Y_mesh_defect1.name = 'Y_mesh_defect1'
    #Y_mesh_defect1.setSpacingMax(self.ymesh_Ncells_defect)
    #Y_mesh_defect1.nukeothers = True
    #Y_mesh_defect1.forceEvenNumberOfCells = True

    #Y_mesh_defect2 = HomogeneousMeshParameters1D(pos_min = defect.getLocation()[1], pos_max = defect.getUpperAbsolute()[1])
    #Y_mesh_defect2.name = 'Y_mesh_defect2'
    #Y_mesh_defect2.setSpacingMax(self.ymesh_Ncells_defect)
    #Y_mesh_defect2.nukeothers = True
    #Y_mesh_defect2.forceEvenNumberOfCells = True

    defect_region_limits = [defect.getLowerAbsolute()[1],
                            defect.getLocation()[1] - self.probe_distance,
                            defect.getLocation()[1] - 0.5*self.dipole_length,
                            defect.getLocation()[1],
                            defect.getLocation()[1] + 0.5*self.dipole_length,
                            defect.getLocation()[1] + self.probe_distance,
                            defect.getUpperAbsolute()[1]]

    Y_mesh_defect = MultiMesh1D()
    for idx in range(len(defect_region_limits)-1):
      m = HomogeneousMeshParameters1D(pos_min = defect_region_limits[idx], pos_max = defect_region_limits[idx+1])
      m.name = 'Y_mesh_defect'
      #m.setSpacingMax(self.ymesh_Ncells_defect)
      m.setSpacingMax(numpy.inf)
      m.nukeothers = True
      Y_mesh_defect.addChild(m)

    #alt: .setNcellsMin(1)
    Y_mesh_defect.mesh_list[0].setSpacingMax(self.ymesh_Ncells_defect)
    Y_mesh_defect.mesh_list[1].setSpacingMax(self.ymesh_Ncells_defect)
    Y_mesh_defect.mesh_list[2].setSpacingMax(self.ymesh_Ncells_defect)
    Y_mesh_defect.mesh_list[3].setSpacingMax(self.ymesh_Ncells_defect)
    Y_mesh_defect.mesh_list[4].setSpacingMax(self.ymesh_Ncells_defect)
    Y_mesh_defect.mesh_list[5].setSpacingMax(self.ymesh_Ncells_defect)

    Y_mesh = MultiMesh1D()
    Y_mesh.name = 'Y_mesh'
    Y_mesh.addChild(Y_mesh_box)
    Y_mesh.addChild(Y_mesh_RCDouter)
    Y_mesh.addChild(Y_mesh_RCDinner)
    Y_mesh.addChild(Y_mesh_defect)
    #if self.no_mesh_check:
      #Y_mesh.maximum_mesh_delta_ratio = None
      #Y_mesh.minimum_mesh_delta = None
    return(Y_mesh)

  def getZmesh(self, sim, RCD, defect, lower, upper):
    Z_mesh_box = HomogeneousMeshParameters1D(pos_min = sim.box.getLower()[2], pos_max = sim.box.getUpper()[2])
    Z_mesh_box.name = 'Z_mesh_box'
    Z_mesh_box.setSpacingMax(self.zmesh_Ncells_box)

    Z_mesh_RCDouter = RCD.getZMesh_with_SpacingMax(self.Nx, self.Ny, self.Nz, self.zmesh_Ncells_RCDouter)
    Z_mesh_RCDouter.name = 'Z_mesh_RCDouter'
    #print('before (len={}): {}'.format(len(Z_mesh_RCDouter.mesh_list), Z_mesh_RCDouter.mesh_list))
    Z_mesh_RCDouter.mesh_list = truncateMeshList(Z_mesh_RCDouter.mesh_list, lower, upper)
    #print('after (len={}): {}'.format(len(Z_mesh_RCDouter.mesh_list), Z_mesh_RCDouter.mesh_list))

    Z_mesh_RCDinner = RCD.getZMesh_with_SpacingMax(1, 1, 1, self.zmesh_Ncells_RCDinner)
    Z_mesh_RCDinner.name = 'Z_mesh_RCDinner'
    Z_mesh_RCDinner.mesh_list = truncateMeshList(Z_mesh_RCDinner.mesh_list, lower, upper)

    #Z_mesh_defect.location = defect.getLocation()[2]

    #Z_mesh_defect1 = HomogeneousMeshParameters1D(pos_min = defect.getLowerAbsolute()[2], pos_max = defect.getLocation()[2])
    #Z_mesh_defect1.name = 'Z_mesh_defect1'
    #Z_mesh_defect1.setSpacingMax(self.zmesh_Ncells_defect)
    #Z_mesh_defect1.nukeothers = True
    #Z_mesh_defect1.forceEvenNumberOfCells = True

    #Z_mesh_defect2 = HomogeneousMeshParameters1D(pos_min = defect.getLocation()[2], pos_max = defect.getUpperAbsolute()[2])
    #Z_mesh_defect2.name = 'Z_mesh_defect2'
    #Z_mesh_defect2.setSpacingMax(self.zmesh_Ncells_defect)
    #Z_mesh_defect2.nukeothers = True
    #Z_mesh_defect2.forceEvenNumberOfCells = True

    defect_region_limits = [defect.getLowerAbsolute()[2],
                            defect.getLocation()[2] - self.probe_distance,
                            defect.getLocation()[2] - 0.5*self.dipole_length,
                            defect.getLocation()[2],
                            defect.getLocation()[2] + 0.5*self.dipole_length,
                            defect.getLocation()[2] + self.probe_distance,
                            defect.getUpperAbsolute()[2]]

    Z_mesh_defect = MultiMesh1D()
    for idx in range(len(defect_region_limits)-1):
      m = HomogeneousMeshParameters1D(pos_min = defect_region_limits[idx], pos_max = defect_region_limits[idx+1])
      m.name = 'Z_mesh_defect'
      #m.setSpacingMax(self.zmesh_Ncells_defect)
      m.setSpacingMax(numpy.inf)
      m.nukeothers = True
      Z_mesh_defect.addChild(m)

    Z_mesh_defect.mesh_list[0].setSpacingMax(self.zmesh_Ncells_defect)
    Z_mesh_defect.mesh_list[1].setSpacingMax(self.zmesh_Ncells_defect)
    Z_mesh_defect.mesh_list[2].setSpacingMax(self.zmesh_Ncells_defect)
    Z_mesh_defect.mesh_list[3].setSpacingMax(self.zmesh_Ncells_defect)
    Z_mesh_defect.mesh_list[4].setSpacingMax(self.zmesh_Ncells_defect)
    Z_mesh_defect.mesh_list[5].setSpacingMax(self.zmesh_Ncells_defect)

    Z_mesh = MultiMesh1D()
    Z_mesh.name = 'Z_mesh'
    Z_mesh.addChild(Z_mesh_box)
    Z_mesh.addChild(Z_mesh_RCDouter)
    Z_mesh.addChild(Z_mesh_RCDinner)
    Z_mesh.addChild(Z_mesh_defect)
    #if self.no_mesh_check:
      #Z_mesh.maximum_mesh_delta_ratio = None
      #Z_mesh.minimum_mesh_delta = None
    return(Z_mesh)

  def getLatticeVectors(self):
    return self.RCD.getLatticeVectors()

def blender_debug():
  # Designed to be used with RCD_mesh_debug.blend (requires the bpy module, which can only be imported from within blender (unless recompiled as module))

  obj = RCD_FRD_111_hybrid()
  obj.n_defect = 2.4
  obj.n_RCD = 1
  obj.n_backfill = 2.4

  RCD = RCD_HexagonalLattice()
  RCD.setCubicUnitCellSize(obj.cubic_unit_cell_size)
  RCD.setUnitCellType(2)
  (u,v,w) = RCD.getLatticeVectors()

  max_size = 10

  obj.Nx = int(round( (max_size/norm(u)+1)/2 ))
  obj.Ny = int(round( (max_size/norm(v)+1)/2 ))
  obj.Nz = int(round( (max_size/norm(w)+1)/2 ))

  obj.defect_position = 0
  obj.defect_type = 'sphere'

  sim, filepath, X_mesh, Y_mesh, Z_mesh = obj.write()
  print(filepath)
  #return

  from blender_scripts.modules.bfdtd_import import BristolFDTDimporter
  importer = BristolFDTDimporter()
  importer.import_cylinders = False
  importer.import_blocks = False
  importer.importBristolFDTD(filepath + '.in', GUI_loaded=True)

  import bpy
  from blender_scripts.modules.FDTDGeometryObjects import GEOmesh1D, GEOmesh1D_bmesh, renderXMesh1D, renderYMesh1D, renderZMesh1D

  if not 'Xmesh' in bpy.data.groups: bpy.ops.group.create(name='Xmesh')
  renderXMesh1D(name=X_mesh.name, coords=X_mesh.getLocalCoordinates(), location=[X_mesh.getGlobalLocation(), -1, -1])
  bpy.ops.object.group_link(group='Xmesh')

  for idx, m in enumerate(X_mesh.mesh_list, 2):
    #m.maximum_mesh_delta_ratio = None
    #GEOmesh1D_bmesh(name=m.name, coords=m.getLocalCoordinates(), location=[m.getGlobalLocation(), -idx, 0])
    #bpy.ops.object.group_link(group='meshes')
    m.renderXMesh1D(location=[m.getGlobalLocation(), -idx, -idx], group='Xmesh')

  if not 'Ymesh' in bpy.data.groups: bpy.ops.group.create(name='Ymesh')
  renderYMesh1D(name=Y_mesh.name, coords=Y_mesh.getLocalCoordinates(), location=[-1, Y_mesh.getGlobalLocation(), -1])
  bpy.ops.object.group_link(group='Ymesh')

  for idx, m in enumerate(Y_mesh.mesh_list, 2):
    #m.maximum_mesh_delta_ratio = None
    #GEOmesh1D_bmesh(name=m.name, coords=m.getLocalCoordinates(), location=[m.getGlobalLocation(), -idx, 0])
    #bpy.ops.object.group_link(group='meshes')
    m.renderYMesh1D(location=[-idx, m.getGlobalLocation(), -idx], group='Ymesh')

  if not 'Zmesh' in bpy.data.groups: bpy.ops.group.create(name='Zmesh')
  renderZMesh1D(name=Z_mesh.name, coords=Z_mesh.getLocalCoordinates(), location=[-1, -1, Z_mesh.getGlobalLocation()])
  bpy.ops.object.group_link(group='Zmesh')

  for idx, m in enumerate(Z_mesh.mesh_list, 2):
    #m.maximum_mesh_delta_ratio = None
    #GEOmesh1D_bmesh(name=m.name, coords=m.getLocalCoordinates(), location=[m.getGlobalLocation(), -idx, 0])
    #bpy.ops.object.group_link(group='meshes')
    m.renderZMesh1D(location=[-idx, -idx, m.getGlobalLocation()], group='Zmesh')

  print('=====> {} cells'.format(sim.getNcells()))
  print(obj.Nx, obj.Ny, obj.Nz)
  print(norm(w))
  print('DONE')
  return

if __name__ == '__main__':
  pass
  #createGUI(RCD_FRD_111_hybrid())
  #blender_debug()
