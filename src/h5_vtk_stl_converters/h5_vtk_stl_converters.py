#!/usr/bin/env python2
# -*- coding: utf-8 -*-

###
# For VTK 6.1.0 with python2.7
# at work
#export PYTHONPATH=$HOME/opt/lib/python2.7/site-packages/
# at home/desktop
#export PYTHONPATH=$HOME/opt/VTK-6.1.0-Linux-64bit/lib/python2.7/site-packages/
#export LD_LIBRARY_PATH=$HOME/opt/lib:$HOME/opt/VTK-6.1.0-Linux-64bit/lib
###

# TODO: Write to .vti files
# TODO: improved h5tools + mpb-data mix. Multiple datasets, VTS, VTI, etc

from __future__ import division

import os
import sys
import subprocess
import argparse
import tempfile

import h5py

def dataset_to_h5(dataset, h5file):
  point_data = dataSet.GetPointData()
  array_name = point_data.GetArrayName(0)
  print('array_name = {}'.format(array_name))
  
  float_array = point_data.GetArray(0)
  print(float_array)

  print('float_array.GetNumberOfTuples() = {}'.format(float_array.GetNumberOfTuples()))
  
  Nx, Ny, Nz = dataSet.GetDimensions()
  
  S = zeros([Nx,Ny,Nz])
  print('=== dims ===')
  print(S.shape)
  
  for i in range(Nx):
    for j in range(Ny):
      for k in range(Nz):
        S[i,j,k] = float_array.GetTuple1(k*Nx*Ny + j*Nx + i)
  
  with h5py.File(h5file, "w") as f:
    print('writing to ' + h5file)
    
    dset = f.create_dataset('/S', S.shape, dtype='f')
    dset[...] = S

  return

def vtkImageData_vtkSampleFunction(implicit_function, outfile_basename, mylattice):
  
  dataset = vtk.vtkImageData()
  dataset.SetDimensions(mylattice.getResolution())
  (xmin,xmax, ymin,ymax, zmin,zmax) = mylattice.getBounds()
  dataset.SetOrigin([xmin, ymin, zmin])
  dataset.SetSpacing(mylattice.getSpacing())
  
  scalars = vtk.vtkFloatArray()

  for i in range(dataset.GetNumberOfPoints()):
    coord = dataset.GetPoint(i)
    if implicit_function.FunctionValue(coord)<=0:
      scalars.InsertNextValue(1)
    else:
      scalars.InsertNextValue(0)
  
  dataset.GetPointData().SetScalars(scalars)
  
  writer = vtk.vtkXMLImageDataWriter()
  writer.SetInputData(dataset)
  writer.SetFileName(outfile_basename + '.' + writer.GetDefaultFileExtension())
  writer.Write()
  
  return

def vtkRectilinearGrid_vtkSampleFunction(implicit_function, outfile_basename, mylattice):
  (Nx, Ny, Nz) = mylattice.getResolution()
  (xmin,xmax, ymin,ymax, zmin,zmax) = mylattice.getBounds()
  
  x = [ numpy.power(i,0.5) for i in range(Nx) ]
  y = [ numpy.power(i,2.5) for i in range(Ny) ]
  z = [ numpy.power(i,3) for i in range(Nz) ]
  
  x = [xmin + i/max(x)*(xmax-xmin) for i in x]
  y = [ymin + i/max(y)*(ymax-ymin) for i in y]
  z = [zmin + i/max(z)*(zmax-zmin) for i in z]
    
  xCoords = vtk.vtkFloatArray()
  for i in range(len(x)):
    xCoords.InsertNextValue(x[i])
  
  yCoords = vtk.vtkFloatArray()
  for i in range(len(y)):
    yCoords.InsertNextValue(y[i])
  
  zCoords = vtk.vtkFloatArray()
  for i in range(len(z)):
    zCoords.InsertNextValue(z[i])
  
  dataset = vtk.vtkRectilinearGrid()
  dataset.SetDimensions(Nx, Ny, Nz)
  dataset.SetXCoordinates(xCoords)
  dataset.SetYCoordinates(yCoords)
  dataset.SetZCoordinates(zCoords)
  
  scalars = vtk.vtkFloatArray()

  for i in range(dataset.GetNumberOfPoints()):
    coord = dataset.GetPoint(i)
    if implicit_function.FunctionValue(coord)<=0:
      scalars.InsertNextValue(1)
    else:
      scalars.InsertNextValue(0)
  
  dataset.GetPointData().SetScalars(scalars)

  writer = vtk.vtkXMLRectilinearGridWriter()
  writer.SetInputData(dataset)
  writer.SetFileName(outfile_basename + '.' + writer.GetDefaultFileExtension())
  writer.Write()
  
  return

def vtkStructuredGrid_vtkSampleFunction(implicit_function, outfile_basename, mylattice):
  (Nx, Ny, Nz) = mylattice.getResolution()
  (a1, a2, a3) = mylattice.getLatticeVectors()
  
  points = vtk.vtkPoints()
  points.SetNumberOfPoints(Nx*Ny*Nz)
  
  for i in range(Nx):
    for j in range(Ny):
      for k in range(Nz):
        coord = (i/(Nx-1) - 0.5)*a1 + (j/(Ny-1) - 0.5)*a2 + (k/(Nz-1) - 0.5)*a3
        offset = i + j*Nx + k*Nx*Ny
        points.SetPoint(offset, coord)
  
  dataset = vtk.vtkStructuredGrid()
  dataset.SetDimensions(Nx, Ny, Nz)
  dataset.SetPoints(points)

  scalars = vtk.vtkFloatArray()

  for i in range(dataset.GetNumberOfPoints()):
    coord = dataset.GetPoint(i)
    if implicit_function.FunctionValue(coord)<=0:
      scalars.InsertNextValue(1)
    else:
      scalars.InsertNextValue(0)
  
  dataset.GetPointData().SetScalars(scalars)

  writer = vtk.vtkXMLStructuredGridWriter()
  writer.SetInputData(dataset)
  writer.SetFileName(outfile_basename + '.' + writer.GetDefaultFileExtension())
  writer.Write()

  return

  #dataset = vtk.vtkImageData()
  #dataset.SetDimensions(mylattice.getResolution())
  #(xmin,xmax, ymin,ymax, zmin,zmax) = mylattice.getBounds()
  #dataset.SetOrigin([xmin, ymin, zmin])
  #dataset.SetSpacing(mylattice.getSpacing())
  
  #scalars = vtk.vtkFloatArray()

  #for i in range(dataset.GetNumberOfPoints()):
    #coord = dataset.GetPoint(i)
    #if implicit_function.FunctionValue(coord)<=0:
      #scalars.InsertNextValue(1)
    #else:
      #scalars.InsertNextValue(0)
  
  #dataset.GetPointData().SetScalars(scalars)
  

    
    
    ## add scalar data to the grid
    #for i in range(Nx):
      #for j in range(Ny):
        #for k in range(Nz):
          #offset = k*Nx*Ny + j*Nx + i
          #scalars0.SetTuple1(offset, offset)
          #scalars1.SetTuple1(offset, i)
          #scalars2.SetTuple1(offset, j)
          #scalars3.SetTuple1(offset, k)


    
    #dataset_list = []
    #for key in dataset_key_list:
      #h5_data = f[key]
      #(Nx, Ny, Nz) = h5_data.shape
      #vtk_data = vtk.vtkFloatArray()
      #vtk_data.SetName(key)
      #vtk_data.SetNumberOfTuples(Nx*Ny*Nz)
      #dataset_list.append((vtk_data))
      #{'h5_key': key, 'h5_data': 4139, 'vtk_key': key, 'vtk_data': vtk_data}
      
    
    #dataset_
    #data = f['data'][...]
    #epsilon_xx = f['epsilon.xx'][...]
    #epsilon_xy = f['epsilon.xy'][...]
    #epsilon_xz = f['epsilon.xz'][...]
    #epsilon_yy = f['epsilon.yy'][...]
    #epsilon_yz = f['epsilon.yz'][...]
    #epsilon_zz = f['epsilon.zz'][...]
    #epsilon_inverse_xx = f['epsilon_inverse.xx'][...]
    #epsilon_inverse_xy = f['epsilon_inverse.xy'][...]
    #epsilon_inverse_xz = f['epsilon_inverse.xz'][...]
    #epsilon_inverse_yy = f['epsilon_inverse.yy'][...]
    #epsilon_inverse_yz = f['epsilon_inverse.yz'][...]
    #epsilon_inverse_zz = f['epsilon_inverse.zz'][...]


  #scalars0 = vtk.vtkFloatArray()
  #scalars0.SetName('offset')
  #scalars0.SetNumberOfTuples(dataset.GetNumberOfPoints())

  #scalars1 = vtk.vtkFloatArray()
  #scalars1.SetName('i')
  #scalars1.SetNumberOfTuples(dataset.GetNumberOfPoints())

  #scalars2 = vtk.vtkFloatArray()
  #scalars2.SetName('j')
  #scalars2.SetNumberOfTuples(dataset.GetNumberOfPoints())

  #scalars3 = vtk.vtkFloatArray()
  #scalars3.SetName('k')
  #scalars3.SetNumberOfTuples(dataset.GetNumberOfPoints())

  #for i in range(Nx):
    #for j in range(Ny):
      #for k in range(Nz):
        #offset = k*Nx*Ny + j*Nx + i
        #scalars0.SetTuple1(offset, offset)
        #scalars1.SetTuple1(offset, i)
        #scalars2.SetTuple1(offset, j)
        #scalars3.SetTuple1(offset, k)
  
  ##dataset.GetPointData().SetScalars(scalars)
  #dataset.GetPointData().AddArray(scalars0)
  #dataset.GetPointData().AddArray(scalars1)
  #dataset.GetPointData().AddArray(scalars2)
  #dataset.GetPointData().AddArray(scalars3)

  #return  

def h5tovtk(infile, outfile):
  
  return

def vtktoh5(infile, outfile):
  return

def h5tostl(infile, outfile):
  return

def stltoh5(infile, outfile):
  return

def stltovtk(infile, outfile):
  return

def vtktostl(infile, outfile):
  return

# TODO: Check the i,j,k order and offset. There is a mistake currently.
# VTK doc says numbering is in increasing X, Y, then Z.
def test_reshape():
  #my_array = array()
  #for i in range(Nx):
    #for j in range(Ny):
      #for k in range(Nz):
        ##pass
        #offset = i + j*Nx + k*Nx*Ny
        #coord = (i/(Nx-1) - 0.5)*a1 + (j/(Ny-1) - 0.5)*a2 + (k/(Nz-1) - 0.5)*a3
        #points[offset] = coord
  
  #lol = array([
  #[1,2
  #34
  
  #5,6
  #7,8
    #]
  #4,5,6
  #7,8,9
  #10,11,12
  
  #]
  #)
  
  #la.transpose().reshape(1,-1)
  
  myarray = array([[[ 2.,  6.],
                    [ 4.,  8.]],
                   [[ 3.,  7.],
                    [ 5.,  9.]]])

  scalar = myarray.transpose().reshape(-1,1)
  
  print(scalar)
  vtk_data = numpy_to_vtk(scalar)
  print(vtk_data)
  for i in range(vtk_data.GetNumberOfTuples()):
    print(vtk_data.GetTuple(i))
  
  #vtk_data = vtk.vtkFloatArray()
  ##vtk_data.SetVoidArray(scalar, 2*2*2, 1)  
  #vtk_data.SetName('mamamia')
  #vtk_data.SetNumberOfTuples(2*2*2)
  ##vtk_data.InsertTuples(array(range(8)), array(range(8)), scalar)

  #Nx,Ny,Nz = myarray.shape
  #for i in range(Nx):
    #for j in range(Ny):
      #for k in range(Nz):
        ##pass
        #offset = i + j*Nx + k*Nx*Ny
        #vtk_data.SetTuple1(offset, 2*offset)
        ##coord = (i/(Nx-1) - 0.5)*a1 + (j/(Ny-1) - 0.5)*a2 + (k/(Nz-1) - 0.5)*a3
        ##points.SetPoint(offset, coord)
        ##for key in dataset_dict.keys():
          ##dataset_dict[key][1].SetTuple1(offset, dataset_dict[key][0][i,j,k])
  
  #print(vtk_data)
  #for i in range(vtk_data.GetNumberOfTuples()):
    #print(vtk_data.GetTuple(i))
  
  # create vtkImageData
  dataset_vti = vtk.vtkImageData()
  dataset_vti.SetDimensions(2, 2 ,2)
  #(xmin,xmax, ymin,ymax, zmin,zmax) = mylattice.getBounds()
  #dataset_vti.SetOrigin([xmin, ymin, zmin])
  #dataset_vti.SetSpacing(mylattice.getSpacing())

  dataset_vti.GetPointData().AddArray(vtk_data)

  # write out .vti file
  writer = vtk.vtkXMLImageDataWriter()
  writer.SetInputData(dataset_vti)
  writer.SetFileName('axis_test-epsilon.vti')
  writer.Write()
  
  return

if __name__ == '__main__':
  #main()
  h5tovts_argparse()
  #test_reshape()
