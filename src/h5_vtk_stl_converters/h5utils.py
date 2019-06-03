#!/usr/bin/env python2
# -*- coding: utf-8 -*-

'''
This module provides various utilities to work with the HDF5 format (and the VTK formats).

Automatic documentation cannot be generated at the moment, since we use python3 by default.

This script only runs with python2 because the python VTK module is not yet fully ported to python3.

.. note:: VTK numbering is in increasing X, then Y, then Z.

.. todo:: Use virtual void vtkSTLReader::MergingOff() 	[virtual] - Turn on/off merging of points/triangles.
.. todo:: Read in multiple separate STL files.
'''

from __future__ import division

import os
import sys
import vtk
import h5py
import time
import numpy
from numpy import array, zeros, sqrt, linspace
from numpy.linalg import norm
from vtk.util.numpy_support import numpy_to_vtk
import constants.physcon

# This value can be changed by the user for the whole module to change data precision.
vtkScalarArray = vtk.vtkFloatArray
#vtkScalarArray = vtk.vtkDoubleArray

class Lattice(object):
  '''
  The lattice class is normally used only for the geometry-lattice variable, and specifies the three lattice directions of the crystal and the lengths of the corresponding lattice vectors.

  lattice
      Properties: 

  basis1, basis2, basis3 [vector3]
      The three lattice directions of the crystal, specified in the cartesian basis. The lengths of these vectors are ignored--only their directions matter. The lengths are determined by the basis-size property, below. These vectors are then used as a basis for all other 3-vectors in the ctl file. They default to the x, y, and z directions, respectively. 

  basis-size [vector3]
      The components of basis-size are the lengths of the three basis vectors, respectively. They default to unit lengths. 

  size [vector3]
      The size of the lattice (i.e. the length of the lattice vectors Ri, in which the crystal is periodic) in units of the basis vectors. Thus, the actual lengths of the lattice vectors are given by the components of size multiplied by the components of basis-size. (Alternatively, you can think of size as the vector between opposite corners of the primitive cell, specified in the lattice basis.) Defaults to unit lengths. 

  resolution [number or vector3]
      Specifies the computational grid resolution, in pixels per lattice unit (a lattice unit is one basis vector in a given direction).
      If resolution is a vector3, then specifies a different resolution for each direction;
      otherwise the resolution is uniform.
      (The grid size is then the product of the lattice size and the resolution, rounded up to the next positive integer.)
      Defaults to 10.
    
  If any dimension has the special size no-size, then the dimensionality of the problem is reduced by one; strictly speaking, the dielectric function is taken to be uniform along that dimension. (In this case, the no-size dimension should generally be orthogonal to the other dimensions.) 
    
  .. todo:: This class still needs some work. But works to currently store necessary variables. Use with care.
  .. todo:: merge somehow with BFDTD meshing classes? (need proper definition for resolution, etc)
  '''
  def __init__(self):
    self.basis1 = array([1,0,0])
    self.basis2 = array([0,1,0])
    self.basis3 = array([0,0,1])
    self.basis_size = array([1,1,1])
    self.size = array([1,1,1])
    
    self.xmesh = [0,1]
    self.ymesh = [0,1]
    self.zmesh = [0,1]
    self.setResolution(10, 10, 10)
    
    return
  
  def __str__(self):
    ret = 'lattice:\n'
    ret += '  basis1 = {}\n'.format(self.basis1)
    ret += '  basis2 = {}\n'.format(self.basis2)
    ret += '  basis3 = {}\n'.format(self.basis3)
    ret += '  basis_size = {}\n'.format(self.basis_size)
    ret += '  size = {}'.format(self.size)
    return(ret)
  
  def getLatticeVectors(self):
    a1 = self.size[0]*self.basis_size[0]*self.basis1/norm(self.basis1)
    a2 = self.size[1]*self.basis_size[1]*self.basis2/norm(self.basis2)
    a3 = self.size[2]*self.basis_size[2]*self.basis3/norm(self.basis3)
    return (a1, a2, a3)
  
  def getBounds(self):
    (a1, a2, a3) = self.getLatticeVectors()

    Pmax = 0.5*a1 + 0.5*a2 + 0.5*a3
    Pmin = -Pmax

    xmin = Pmin[0]
    ymin = Pmin[1]
    zmin = Pmin[2]

    xmax = Pmax[0]
    ymax = Pmax[1]
    zmax = Pmax[2]
    
    return (xmin,xmax, ymin,ymax, zmin,zmax)
    
  def getXmeshDelta(self):
    return(numpy.diff(self.xmesh))
  def getYmeshDelta(self):
    return(numpy.diff(self.ymesh))
  def getZmeshDelta(self):
    return(numpy.diff(self.zmesh))
  def getMeshDelta(self):
    return(numpy.diff(self.xmesh),numpy.diff(self.ymesh),numpy.diff(self.zmesh))
    
  def getMinDeltas(self):
    dx = min(self.getXmeshDelta())
    dy = min(self.getYmeshDelta())
    dz = min(self.getZmeshDelta())
    return (dx,dy,dz)

  def getResolution(self):
    return [len(self.xmesh), len(self.ymesh), len(self.zmesh)]

  def getSpacing(self):
    (xmin,xmax, ymin,ymax, zmin,zmax) = self.getBounds()
    (Nx, Ny, Nz) = self.getResolution()
    dx = (xmax-xmin)/(Nx-1)
    dy = (ymax-ymin)/(Ny-1)
    dz = (zmax-zmin)/(Nz-1)
    return (dx,dy,dz)
        
  def setResolution(self, Nx, Ny, Nz):
    '''
    Sets up homogeneous X,Y,Z grids with Nx,Ny,Nz points.
    '''
    self.xmesh = linspace(-0.5, 0.5, Nx)
    self.ymesh = linspace(-0.5, 0.5, Ny)
    self.zmesh = linspace(-0.5, 0.5, Nz)
    return

  def getMesh(self):
    return (self.xmesh, self.ymesh, self.zmesh)

  def setXmesh(self, xmesh):
    self.xmesh = xmesh
    return

  def setYmesh(self, ymesh):
    self.ymesh = ymesh
    return

  def setZmesh(self, zmesh):
    self.zmesh = zmesh
    return

  def setSize(self, size):
    self.size = size

  def setBasisSize(self, basis_size):
    self.basis_size = basis_size

class FCClattice(Lattice):
  ''' Create a FCC lattice. '''
  def __init__(self):
    ''' Constructor '''
    super(FCClattice, self).__init__()
    # set up lattice
    self.basis1 = array([0, 1, 1])
    self.basis2 = array([1, 0, 1])
    self.basis3 = array([1, 1, 0])
    self.basis_size = array([sqrt(0.5), sqrt(0.5), sqrt(0.5)])

class BCClattice(Lattice):
  ''' Create a BCC lattice. '''
  def __init__(self):
    ''' Constructor '''
    super(BCClattice, self).__init__()
    # set up lattice
    self.basis1 = array([-1,  1,  1])
    self.basis2 = array([ 1, -1,  1])
    self.basis3 = array([ 1,  1, -1])
    self.basis_size = array([sqrt(3)/2, sqrt(3)/2, sqrt(3)/2])

def h5_getDataSets(HDF5_file_object):
  # create list of datasets
  #dataset_list = [k for k in HDF5_file_object.keys() if k not in ['description','lattice vectors', 'xmesh', 'ymesh', 'zmesh'] ]
  #print('=== Full content listing: ===')
  #def printname(name):
    #print name
  #HDF5_file_object.visit(printname)
  #print('======')
  dataset_list = []
  print('=== Contents: ===')
  def printname(name, obj):
    if isinstance(obj, h5py.Group):
      print('Group: {}'.format(name))
    elif isinstance(obj, h5py.Dataset):
      print('Dataset: {}'.format(name))
      if name not in ['description','lattice vectors', 'xmesh', 'ymesh', 'zmesh']:
        dataset_list.append(name)
  HDF5_file_object.visititems(printname)
  print('======')
  print('Available datasets: {}'.format(dataset_list))
  return(dataset_list)

def h5_setupLattice(HDF5_file_object, total_lattice_size=None, requested_dataset=[]):
  # get description
  description = None
  if 'description' in HDF5_file_object.keys():
    #description              Dataset {SCALAR}
    description = HDF5_file_object['description'][...].tostring().decode("ascii").strip('\0')
    print('description = {}'.format(description))

  complete_dataset_list = h5_getDataSets(HDF5_file_object)
  if requested_dataset:
    for i in requested_dataset:
      if i not in complete_dataset_list:
        raise Exception('Requested dataset not found: {}'.format(i))

  # choose first dataset if not specified
  if requested_dataset:
    selected_dataset = requested_dataset[0]
  else:
    selected_dataset = complete_dataset_list[0]

  # set up data, Nx, Ny, Nz
  # TODO: Might cause conflict with size read from x/y/z mesh values... Add warnings?
  print('Using dataset = {} to determine dimensions.'.format(selected_dataset))
  data = HDF5_file_object[selected_dataset]
  if len(data.shape) != 3:
    raise Exception('Data of dimension {}. Only 3D data supported at the moment.'.format(len(data.shape)))
  (Nx, Ny, Nz) = data.shape
  
  # set up lattice
  mylattice = Lattice()
  
  if 'lattice vectors' in HDF5_file_object.keys():
    #lattice\ vectors         Dataset {3, 3}
    lattice_vectors = HDF5_file_object['lattice vectors'][...]
    mylattice.basis1 = lattice_vectors[0]
    mylattice.basis2 = lattice_vectors[1]
    mylattice.basis3 = lattice_vectors[2]
    mylattice.setSize( [norm(mylattice.basis1), norm(mylattice.basis2), norm(mylattice.basis3)] )

  if total_lattice_size:
    mylattice.setSize(total_lattice_size)
  
  # generate homogeneous mesh by default
  mylattice.setResolution(Nx, Ny, Nz)

  if 'xmesh' in HDF5_file_object.keys():
    mylattice.setXmesh(HDF5_file_object['xmesh'][...])
  if 'ymesh' in HDF5_file_object.keys():
    mylattice.setYmesh(HDF5_file_object['ymesh'][...])
  if 'zmesh' in HDF5_file_object.keys():
    mylattice.setZmesh(HDF5_file_object['zmesh'][...])
  
  (a1, a2, a3) = mylattice.getLatticeVectors()
  (xmesh, ymesh, zmesh) = mylattice.getMesh()
  print('a1 = {}'.format(a1))
  print('a2 = {}'.format(a2))
  print('a3 = {}'.format(a3))
  print('data.shape = {} x {} x {}'.format(Nx, Ny, Nz))
  print('mesh.shape = {} x {} x {}'.format(len(xmesh), len(ymesh), len(zmesh)))
  if Nx != len(xmesh) or Ny != len(ymesh) or Nz != len(zmesh):
    raise Exception('Inconsistent number of cells between the dataset and the x/y/z meshs.')
  return (mylattice, complete_dataset_list)
    
def MPB_h5tovts(h5file, basepath, total_lattice_size=None, requested_dataset=[], verbosity=0):
  '''
  * total_lattice_size : total length of the lattice vectors, i.e. **size*basis-size** in MPB terms. Overrides any values obtained from reading the lattice vectors in the .h5 file.
  
  .. todo:: Emulate the -x/y/z options of mpb-data, i.e. create a periodic structure from a unit-cell.
  '''
  # read in .h5 file
  with h5py.File(h5file, "r") as HDF5_file_object:
    print('Reading from ' + h5file)
    
    (mylattice, complete_dataset_list) = h5_setupLattice(HDF5_file_object, total_lattice_size, requested_dataset)
    (Nx, Ny, Nz) = mylattice.getResolution()
    (a1, a2, a3) = mylattice.getLatticeVectors()
    (xmesh, ymesh, zmesh) = mylattice.getMesh()
    
    # create the vtkPoints structure for the coordinates
    points = vtk.vtkPoints()
    points.SetNumberOfPoints(Nx*Ny*Nz)
    
    if requested_dataset:
      dataset_list = requested_dataset
    else:
      dataset_list = complete_dataset_list
    
    # create the vtkScalarArray structures for the data
    dataset_dict = dict()
    for key in dataset_list:
      print('key = {}'.format(key))
      
      try:
        # We need flat 1D data for VTK structures (and for numpy_to_vtk). Equivalent ways of achieving this:
        #  A.reshape(-1, order='F')
        #  A.flatten(order='F')
        #  A.ravel(order='F')
        # ‘F’ means to read / write the elements using Fortran-like index order, with the first index changing fastest, and the last index changing slowest. (VTK style)
        #scalar = HDF5_file_object[key][...].transpose().reshape(-1,1) # OK
        #scalar = HDF5_file_object[key][...].reshape(-1,1, order='F') # fail
        #scalar = HDF5_file_object[key][...].reshape(-1, order='F') # OK
        scalar = HDF5_file_object[key][...].flatten(order='F') # OK
        #scalar = HDF5_file_object[key][...].ravel(order='F') # OK
      except:
        print('scalar = {}'.format(scalar))
        print('In case of this error: TypeError: CreateDataArray argument 1: an integer is required')
        print('Just make sure to use the --bfdtd option, until auto-detection arrives.')
        raise
      vtk_data = numpy_to_vtk(scalar)

      #vtk_data = vtkScalarArray()
      vtk_data.SetName(key)
      #vtk_data.SetNumberOfTuples(Nx*Ny*Nz)
      dataset_dict[key] = (HDF5_file_object[key], vtk_data, scalar)

    last_info_time = time.time()
    
    print('Starting loops')
    counter = 0
    # fill the vtkPoints and vtkScalarArray
    for k in range(Nz):
      for j in range(Ny):
        for i in range(Nx):
          offset = i + j*Nx + k*Nx*Ny

          # old system:
          #   coord = (i/(Nx-1) - 0.5)*a1 + (j/(Ny-1) - 0.5)*a2 + (k/(Nz-1) - 0.5)*a3
          # new system:
          coord = xmesh[i]*a1 + ymesh[j]*a2 + zmesh[k]*a3

          points.SetPoint(offset, coord)
          #for key in dataset_dict.keys():
            #dataset_dict[key][1].SetTuple1(offset, dataset_dict[key][0][i,j,k])
          
          #InsertTuples 	
          #virtual void vtkAbstractArray::InsertTuples 	( 	vtkIdList *  	dstIds,
          #vtkIdList *  	srcIds,
          #vtkAbstractArray *  	source 
          #) 		[pure virtual]

          if time.time() - last_info_time > 5:
            print('{} %'.format(100*offset/(Nx*Ny*Nz-1)))
            last_info_time = time.time()
  
          if verbosity>1:
            counter += 1
            progress_str = 'Progress: {}/{}'.format(counter, Nx*Ny*Nz)
            #print(progress_str, end='\r')
            print(progress_str)
            #subprocess.call(["printf", progress_str+'\r'])
    
    print('\nLoops done.')

    #for key in dataset_dict.keys():
      #h5_data = dataset_dict[key][0]
      #vtk_data = dataset_dict[key][1]
      #vtk_data.InsertTuples()
      #.SetTuple1(offset, [i,j,k])
    
    # create structured grid
    dataset_vts = vtk.vtkStructuredGrid()
    dataset_vts.SetDimensions(Nx, Ny, Nz)
    dataset_vts.SetPoints(points)
    
    # create vtkImageData
    dataset_vti = vtk.vtkImageData()
    dataset_vti.SetDimensions(Nx, Ny, Nz)
    (xmin,xmax, ymin,ymax, zmin,zmax) = mylattice.getBounds()
    dataset_vti.SetOrigin([xmin, ymin, zmin])
    dataset_vti.SetSpacing(mylattice.getSpacing())
    
    # add scalar data to the grids
    for key in dataset_dict.keys():
      dataset_vts.GetPointData().AddArray(dataset_dict[key][1])
      dataset_vti.GetPointData().AddArray(dataset_dict[key][1])
    
    dataset_vts.GetPointData().SetActiveScalars('data')
    dataset_vti.GetPointData().SetActiveScalars('data')

    # write out .vts file
    writer = vtk.vtkXMLStructuredGridWriter()
    writer.SetInputData(dataset_vts)
    writer.SetFileName(basepath + '.' + writer.GetDefaultFileExtension())
    writer.Write()

    # write out .vti file
    writer = vtk.vtkXMLImageDataWriter()
    writer.SetInputData(dataset_vti)
    writer.SetFileName(basepath + '.' + writer.GetDefaultFileExtension())
    writer.Write()

    return

def BFDTD_h5_to_vts(h5file, basepath, total_lattice_size=None, requested_dataset=[], verbosity=0, x_relative_range=[0,1], y_relative_range=[0,1], z_relative_range=[0,1], real_units=False, dry_run=False):
  '''
    Converts BFDTD h5 files to VTS files.
    .. todo:: need py2-compatible bfdtd-parser for direct creation
    .. todo:: when selecting a smaller mesh region for speed, we also need to change the size of the VTS grid (but keep coords correct)...
  '''
  
  requested_arrays = ['material', 'E', 'electric_energy_density']
  #requested_arrays = []
  #x_relative_range = [1/3, 2/3]
  #y_relative_range = [1/3, 2/3]
  #z_relative_range = [1/3, 2/3]
  print('x_relative_range: {}'.format(x_relative_range))
  print('y_relative_range: {}'.format(y_relative_range))
  print('z_relative_range: {}'.format(z_relative_range))
  
  print('{} -> {}.vts'.format(h5file, basepath))
  
  # read in .h5 file
  with h5py.File(h5file, "r") as HDF5_file_object:
    print('Reading from ' + h5file)
    
    (mylattice, complete_dataset_list) = h5_setupLattice(HDF5_file_object, total_lattice_size, requested_dataset)
    (Nx, Ny, Nz) = mylattice.getResolution()
    (a1, a2, a3) = mylattice.getLatticeVectors()
    (xmesh, ymesh, zmesh) = mylattice.getMesh()
    Npoints = Nx*Ny*Nz
    
    # create the vtkPoints structure for the coordinates
    #points = vtk.vtkPoints()
    #points.SetNumberOfPoints(Npoints)

    if requested_dataset:
      dataset_list = requested_dataset
    else:
      dataset_list = complete_dataset_list

    material_data = None
    for dataset_name in dataset_list:
      current_data = HDF5_file_object[dataset_name]
      if 'material' in current_data.dtype.names:
        material_data = current_data
        break
        
    if material_data:
      print('Found material data in: {}'.format(material_data.name))
    else:
      print('Warning: No material data found. No electric energy density data can be calculated.')

    for dataset_name in dataset_list:
      data = HDF5_file_object[dataset_name]

      # create VTK data arrays
      print('Creating VTK data arrays...')
      available_arrays = []
      
      if data.dtype.names == ('E', 'H', 'Pow', 'material'):
        print('time snapshot mode')
        if 'E' in requested_arrays:
          E_array = createvtkArray('E', Npoints, ('x', 'y', 'z'))
          available_arrays.append(E_array)
        if 'H' in requested_arrays:
          H_array = createvtkArray('H', Npoints, ('x', 'y', 'z'))
          available_arrays.append(H_array)
        if 'Pow' in requested_arrays:
          Pow_array = createvtkArray('Pow', Npoints, ('Pow',))
          available_arrays.append(Pow_array)
        if 'material' in requested_arrays:
          material_array = createvtkArray('material', Npoints, ('material',))
          available_arrays.append(material_array)
        #available_arrays = (E_array, H_array, Pow_array, material_array)
      
      elif data.dtype.names == ('E', 'H'):
        print('frequency snapshot mode')
        if 'E' in requested_arrays:
          (E_re_array, E_im_array, E_mod_array, E_phase_array) = createComplexArrays('E', Npoints)
          available_arrays.extend([E_re_array, E_im_array, E_mod_array, E_phase_array])
        if 'H' in requested_arrays:
          (H_re_array, H_im_array, H_mod_array, H_phase_array) = createComplexArrays('H', Npoints)
          available_arrays.extend([H_re_array, H_im_array, H_mod_array, H_phase_array])
        if 'S' in requested_arrays:
          (S_re_array, S_im_array, S_mod_array, S_phase_array) = createComplexArrays('S', Npoints)
          available_arrays.extend([S_re_array, S_im_array, S_mod_array, S_phase_array])
        #available_arrays = [E_re_array, E_im_array, E_mod_array, E_phase_array,
                            #H_re_array, H_im_array, H_mod_array, H_phase_array,
                            #S_re_array, S_im_array, S_mod_array, S_phase_array]
        if material_data:
          if 'electric_energy_density' in requested_arrays:
            electric_energy_density_array = createvtkArray('electric_energy_density', Npoints, ('electric_energy_density',))
            available_arrays.append(electric_energy_density_array)
          if 'magnetic_energy_density' in requested_arrays:
            magnetic_energy_density_array = createvtkArray('magnetic_energy_density', Npoints, ('magnetic_energy_density',))
            available_arrays.append(magnetic_energy_density_array)

      else:
        raise Exception('Unsupported data type.')

      print('...done')
            
      last_info_time = time.time()
      
      x_range = range( int(round(x_relative_range[0]*Nx)), int(round(x_relative_range[1]*Nx)) )
      y_range = range( int(round(y_relative_range[0]*Ny)), int(round(y_relative_range[1]*Ny)) )
      z_range = range( int(round(z_relative_range[0]*Nz)), int(round(z_relative_range[1]*Nz)) )
      Nx_partial = len(x_range)
      Ny_partial = len(y_range)
      Nz_partial = len(z_range)
      Npoints_partial = Nx_partial*Ny_partial*Nz_partial
      
      print( 'Range to fill:' )
      print( 'x: {} -> size={}/{}'.format((x_range[0], x_range[-1]), Nx_partial, Nx) )
      print( 'y: {} -> size={}/{}'.format((y_range[0], y_range[-1]), Ny_partial, Ny) )
      print( 'z: {} -> size={}/{}'.format((z_range[0], z_range[-1]), Nz_partial, Nz) )
      print( 'total points to fill: {}/{}'.format(Npoints_partial, Npoints) )
      
      if dry_run:
        return
      
      print('Starting loops')
      # fill the vtkPoints and vtkScalarArray
      for k in z_range: #range(Nz):
        for j in y_range: #range(Ny):
          for i in x_range: #range(Nx):
      #for k in range(Nz):
        #for j in range(Ny):
          #for i in range(Nx):
            
            offset = i + j*Nx + k*Nx*Ny
            #coord = xmesh[i]*a1 + ymesh[j]*a2 + zmesh[k]*a3
            #points.SetPoint(offset, coord)

            if 'E' in data.dtype.names:
              E = data[i, j, k]['E']
            if 'H' in data.dtype.names:
              H = data[i, j, k]['H']
            if 'Pow' in data.dtype.names:
              if 'Pow' in requested_arrays:
                Pow_array.SetTuple1(offset, data[i, j, k]['Pow'])
            if 'material' in data.dtype.names:
              if 'material' in requested_arrays:
                material_array.SetTuple1(offset, data[i, j, k]['material'])

            if data.dtype.names == ('E', 'H', 'Pow', 'material'):
              if 'E' in requested_arrays:
                E_array.SetTuple3(offset, *E)
              if 'H' in requested_arrays:
                H_array.SetTuple3(offset, *H)
            
            elif data.dtype.names == ('E', 'H'):
              S = numpy.cross(E, numpy.conj(H))
              
              if 'E' in requested_arrays:
                E_mod = setTupleComplex(offset, E, E_re_array, E_im_array, E_mod_array, E_phase_array)
              if 'H' in requested_arrays:
                H_mod = setTupleComplex(offset, H, H_re_array, H_im_array, H_mod_array, H_phase_array)
              if 'S' in requested_arrays:
                S_mod = setTupleComplex(offset, S, S_re_array, S_im_array, S_mod_array, S_phase_array)

              if material_data:
                # We could use numpy.vdot(a,a) for the conjugate dot product with real/absolute, but since we use absolute() before anyway, we may as well use the resulting |Ei| values.
                if 'electric_energy_density' in requested_arrays:
                  if real_units:
                    epsilon = material_data[i, j, k]['material']*constants.physcon.value('elec-const')
                  else:
                    epsilon = material_data[i, j, k]['material']
                  electric_energy_density = epsilon*numpy.dot(E_mod, E_mod)
                  electric_energy_density_array.SetTuple1(offset, electric_energy_density)
                if 'magnetic_energy_density' in requested_arrays:
                  if real_units:
                    mu = constants.physcon.value('magn-const')
                  else:
                    mu = 1
                  magnetic_energy_density = mu*numpy.dot(H_mod, H_mod)
                  magnetic_energy_density_array.SetTuple1(offset, magnetic_energy_density)

            else:
              raise Exception('Unsupported data type.')
            
            if time.time() - last_info_time > 5 or verbosity > 1:
              #print('Progress: {}/{} = {} %'.format(offset+1, Npoints, 100*(offset+1)/Npoints))
              offset_partial = (i-x_range[0]) + (j-y_range[0])*Nx_partial + (k-z_range[0])*Nx_partial*Ny_partial
              print('Progress: {}/{} = {} %'.format(offset_partial+1, Npoints_partial, 100*(offset_partial+1)/Npoints_partial))
              last_info_time = time.time()
      
      print('Loops done.')
      
      # create structured grid
      #dataset_vts = vtk.vtkStructuredGrid()
      #dataset_vts.SetDimensions(Nx, Ny, Nz)
      #dataset_vts.SetPoints(points)

      # create rectilinear grid
      xCoords = vtkScalarArray()
      for i in range(len(xmesh)):
        xCoords.InsertNextValue(xmesh[i])
      
      yCoords = vtkScalarArray()
      for i in range(len(ymesh)):
        yCoords.InsertNextValue(ymesh[i])
      
      zCoords = vtkScalarArray()
      for i in range(len(zmesh)):
        zCoords.InsertNextValue(zmesh[i])

      dataset_vtr = vtk.vtkRectilinearGrid()
      dataset_vtr.SetDimensions(len(xmesh),len(ymesh),len(zmesh))
      dataset_vtr.SetXCoordinates(xCoords)
      dataset_vtr.SetYCoordinates(yCoords)
      dataset_vtr.SetZCoordinates(zCoords)
      
      for A in available_arrays:
        dataset_vtr.GetPointData().AddArray(A)
      
      # write out VTK file(s)
      basepath_snapshot = basepath + data.name.replace('/','_')

      #writer_vts = vtk.vtkXMLStructuredGridWriter()
      #writer_vts.SetFileName(basepath_snapshot + '.' + writer_vts.GetDefaultFileExtension())
      #writer_vts.SetInputData(dataset_vts)
      #writer_vts.Write()
      
      writer_vtr = vtk.vtkXMLRectilinearGridWriter()
      writer_vtr.SetFileName(basepath_snapshot + '.' + writer_vtr.GetDefaultFileExtension())
      writer_vtr.SetInputData(dataset_vtr)
      writer_vtr.Write()

      print('{} -> {}'.format(data.name, writer_vtr.GetFileName()))

    return

def setTupleComplex(offset, value, A_re_array, A_im_array, A_mod_array, A_phase_array):
  A_re_array.SetTuple3(offset, *numpy.real(value))
  A_im_array.SetTuple3(offset, *numpy.imag(value))
  A_mod = numpy.absolute(value)
  A_mod_array.SetTuple3(offset, *A_mod)
  A_phase_array.SetTuple3(offset, *numpy.angle(value))
  return(A_mod)

def createvtkArray(name, number_of_tuples, component_names):
  ''' ..todo:: Check if vtkScalarArray does not already allow this... '''
  A = vtkScalarArray()
  A.SetName(name)
  A.SetNumberOfComponents(len(component_names))
  A.SetNumberOfTuples(number_of_tuples) # must be done after SetNumberOfComponents
  for idx, s in enumerate(component_names):
    A.SetComponentName(idx, s)
    A.FillComponent(idx, 0)
  return A
  
def createComplexArrays(name, number_of_tuples):
  #A_re = createvtkArray(name+'_re', number_of_tuples, (name+'_re_x', name+'_re_y', name+'_re_z'))
  #A_im = createvtkArray(name+'_im', number_of_tuples, (name+'_im_x', name+'_im_y', name+'_im_z'))
  #A_mod = createvtkArray(name+'_mod', number_of_tuples, (name+'_mod_x', name+'_mod_y', name+'_mod_z'))
  #A_phase = createvtkArray(name+'_phase', number_of_tuples, (name+'_phase_x', name+'_phase_y', name+'_phase_z'))
  A_re = createvtkArray(name+'_re', number_of_tuples, ('x', 'y', 'z'))
  A_im = createvtkArray(name+'_im', number_of_tuples, ('x', 'y', 'z'))
  A_mod = createvtkArray(name+'_mod', number_of_tuples, ('x', 'y', 'z'))
  A_phase = createvtkArray(name+'_phase', number_of_tuples, ('x', 'y', 'z'))
  return (A_re, A_im, A_mod, A_phase)

def stltoh5(stlfile, basepath, epsilon_inside, epsilon_outside, lattice=Lattice(), verbosity=0):
  
  if not os.path.exists(stlfile):
    if sys.version_info.major == 2:
      raise IOError('No such file or directory: {}'.format(stlfile)) # py2
    else:
      raise FileNotFoundError('No such file or directory: {}'.format(stlfile)) # py3
  
  print('--> timer start')
  time_start = time.time()

  # read in .stl file
  reader = vtk.vtkSTLReader()
  reader.SetFileName(stlfile)
  reader.Update()
  polydata = reader.GetOutput()

  # write .vtp file
  writer = vtk.vtkXMLPolyDataWriter()
  writer.SetInputData(polydata)
  writer.SetFileName(basepath + '.' + writer.GetDefaultFileExtension())
  writer.Write()

  # set up implicit_function
  implicit_function = vtk.vtkImplicitPolyDataDistance()
  implicit_function.SetInput(polydata)

  print("--> Elapsed time: %.4f sec" % (time.time() - time_start))
  
  stl_to_vts_and_h5(implicit_function, basepath, lattice, epsilon_inside, epsilon_outside)
  print("--> Elapsed time: %.4f sec" % (time.time() - time_start))
  return

def stl_to_vts_and_h5(implicit_function, outfile_basename, lattice, epsilon_inside, epsilon_outside):
  (Nx, Ny, Nz) = lattice.getResolution()
  (a1, a2, a3) = lattice.getLatticeVectors()
  
  points = vtk.vtkPoints()
  points.SetNumberOfPoints(Nx*Ny*Nz)

  scalars_vtk = vtkScalarArray()
  scalars_vtk.SetNumberOfTuples(Nx*Ny*Nz)
  scalars_numpy = zeros([Nx,Ny,Nz])

  print('=== dims ===')
  print(scalars_numpy.shape)
  
  last_info_time = time.time()

  print('=== Loop start ===')
  for k in range(Nz):
    for j in range(Ny):
      for i in range(Nx):
        coord = (i/(Nx-1) - 0.5)*a1 + (j/(Ny-1) - 0.5)*a2 + (k/(Nz-1) - 0.5)*a3
        offset = i + j*Nx + k*Nx*Ny
        points.SetPoint(offset, coord)
        if implicit_function.FunctionValue(coord) <= 0:
          value = epsilon_inside
        else:
          value = epsilon_outside
        scalars_vtk.SetTuple1(offset, value)
        scalars_numpy[i, j, k] = value
        
        if time.time() - last_info_time > 5:
          print('{} %'.format(100*offset/(Nx*Ny*Nz-1)))
          last_info_time = time.time()
  
  print('=== Loop end ===')

  dataset = vtk.vtkStructuredGrid()
  dataset.SetDimensions(Nx, Ny, Nz)
  dataset.SetPoints(points)
  dataset.GetPointData().SetScalars(scalars_vtk)

  writer = vtk.vtkXMLStructuredGridWriter()
  writer.SetInputData(dataset)
  writer.SetFileName(outfile_basename + '.' + writer.GetDefaultFileExtension())
  writer.Write()
  
  h5file = outfile_basename + '.h5'
  with h5py.File(h5file, "w") as HDF5_file_object:
    print('writing to ' + h5file)
    
    dset = HDF5_file_object.create_dataset('/data', scalars_numpy.shape, dtype=numpy.float64)
    dset[...] = scalars_numpy

    dset = HDF5_file_object.create_dataset("description", (), dtype="S29")
    dset[...] = 'dielectric function, epsilon'
    
    lattice_vectors = numpy.array([a1, a2, a3])
    print(lattice_vectors)

    dset = HDF5_file_object.create_dataset('/lattice vectors', lattice_vectors.shape, dtype=numpy.float64)
    dset[...] = lattice_vectors
    
    # TODO: Add these fields:
    #epsilon.xx               Dataset {100, 100, 100}
    #epsilon.xy               Dataset {100, 100, 100}
    #epsilon.xz               Dataset {100, 100, 100}
    #epsilon.yy               Dataset {100, 100, 100}
    #epsilon.yz               Dataset {100, 100, 100}
    #epsilon.zz               Dataset {100, 100, 100}
    #epsilon_inverse.xx       Dataset {100, 100, 100}
    #epsilon_inverse.xy       Dataset {100, 100, 100}
    #epsilon_inverse.xz       Dataset {100, 100, 100}
    #epsilon_inverse.yy       Dataset {100, 100, 100}
    #epsilon_inverse.yz       Dataset {100, 100, 100}
    #epsilon_inverse.zz       Dataset {100, 100, 100}
  
  return

if __name__ == '__main__':
	pass
