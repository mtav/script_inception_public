#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
.. note:: **Doc cleanup. Disregard this at the moment.**

.. todo:: mesh based on position instead of just thicknesses? More flexibility if ever needed... (like now :/)
.. todo:: Use arrays or lists? -> lists, because we are not dealing with vectors. And if we ever need vector-like behaviour, it is easy to switch to an array.

  * GENERIC 1-D MESH CLASSES:

    .. note:: This will go into external 1-D MeshObjects (of which there will be heterogeneous (arbitrary mesh) and homogeneous ones (meshing parameters)).
    .. note:: Each Geometry object will be able to have a set of MeshObjects of one or both types. HeteroMeshs can be created from sets of homo+hetero meshs.
    .. note:: There may be a parent generic MeshObject class.

    .. todo:: Ability somehow to mix 1D,2D,3D meshes (infinity thickness/delta value? new classes? "useForMeshing" attribute? <- sounds good)

  * Other:

    .. todo:: 3-D MESH CLASS
    .. todo:: Cleanup, get rid of deprecated mesh system, make sure everything works

    .. todo:: mesh merging functions + mesh conversion functions
    .. todo:: Generic 1-D function to merge meshing parameters of the form [lower, upper, maxDelta]
    .. todo:: Make BFDTD import show meshboxes + add X-ray option to .geo/.inp files + group objects from same file into one group"
    .. todo:: Add possibility to order meshboxes manually (ex: force to top, to bottom, to make one delta_max/N have priority over others)
    .. todo:: Add "dynamic meshboxes": ex: N=3 everywhere where that meshbox gains priority. ex: Meshbox(xmin=2, xmax=10, N=3). Other meshboxes split it into 4 regions. Make each region be split into N=3 regions.

.. todo:: sanitize class system:

  * class MeshBox(Geometry_object):
  * class MeshingParameters(object):
  * class MeshObject(object):

.. todo:: Allow delta specification directly or with factor where delta=factor*lambda/n (current system, easier to scale if needed)?
.. todo:: parameter in geometry objects to enable/disable use of meshing parameters + allow custom meshing parameters per geometry object

.. note:: **The following class names are all temporary and subject to change!**
'''

from __future__ import division

import sys
import numpy
import warnings
from numpy import array, ceil

from photonics.meshing.meshing import subGridMultiLayer, increaseResolution
from photonics.utilities.common import findNearestInSortedArray

from .BFDTDentry import BFDTDentry
from .meshobject import *

class MeshObject(BFDTDentry):
  '''
  3D mesh class.
  
  Just an object to store xmesh,ymesh,zmesh values, with various related utility functions like writeMesh(FILE)
  Each BFDTDobject uses a single such MeshObject.
  
  .. todo:: Make it 1D? Or put 3D in the name?
  
  attributes:
  
    * xmesh: list of the position (not a thickness list!) of each line of the mesh in the x direction
    * ymesh: list of the position (not a thickness list!) of each line of the mesh in the y direction
    * zmesh: list of the position (not a thickness list!) of each line of the mesh in the z direction
  
  Example:
  
    xmesh = [0, 0.25, 0.5, 0.75, 1] will create a [0.25, 0.25, 0.25, 0.25] thickness sequence in the XMESH object of the .inp file.
  
  '''
  def __init__(self):
    self.name = 'mesh'
    self.xmesh = numpy.array([0,1])
    self.ymesh = numpy.array([0,1])
    self.zmesh = numpy.array([0,1])
  
  def setXmesh(self,xmesh):
    self.xmesh = xmesh
  def setYmesh(self,ymesh):
    self.ymesh = ymesh
  def setZmesh(self,zmesh):
    self.zmesh = zmesh
  def setMesh(self,xmesh,ymesh,zmesh):
    self.xmesh = xmesh
    self.ymesh = ymesh
    self.zmesh = zmesh
    
  def getXmesh(self):
    return(self.xmesh)
  def getYmesh(self):
    return(self.ymesh)
  def getZmesh(self):
    return(self.zmesh)
  def getMesh(self):
    return(self.xmesh,self.ymesh,self.zmesh)

  def setXmeshDelta(self,xmesh_delta):
    self.xmesh = numpy.cumsum(numpy.hstack((0,xmesh_delta)))
  def setYmeshDelta(self,ymesh_delta):
    self.ymesh = numpy.cumsum(numpy.hstack((0,ymesh_delta)))
  def setZmeshDelta(self,zmesh_delta):
    self.zmesh = numpy.cumsum(numpy.hstack((0,zmesh_delta)))
  def setMeshDelta(self,xmesh_delta,ymesh_delta,zmesh_delta):
    self.xmesh = numpy.cumsum(numpy.hstack((0,xmesh_delta)))
    self.ymesh = numpy.cumsum(numpy.hstack((0,ymesh_delta)))
    self.zmesh = numpy.cumsum(numpy.hstack((0,zmesh_delta)))
  
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

  def setSizeAndResolution(self, size_vec3, N_vec3, Ncells_per_unit=False):
    '''
    Sets the size and resolution in all 3 directions.
    
    The **Ncells_per_unit=True** option can be used to obtain MEEP/MPB-like behaviour, i.e. resolution will be in cells per distance unit, i.e. cells/micron or cells/metre.
    In this case, the number of cells in a given direction is set to **N[i] = ceil(N_vec3[i] * size_vec3[i])**, i.e. increased resolution is preferred if size is not integer.
    '''
    if Ncells_per_unit:
      Nx = N_vec3[0] * size_vec3[0]
      Ny = N_vec3[1] * size_vec3[1]
      Nz = N_vec3[2] * size_vec3[2]
    else:
      Nx = N_vec3[0]
      Ny = N_vec3[1]
      Nz = N_vec3[2]
    
    # just making sure they are all "integers" (ceil returns floats if input is float), even though linspace accepts floats
    Nx = int(ceil(Nx))
    Ny = int(ceil(Ny))
    Nz = int(ceil(Nz))
    self.xmesh = numpy.linspace(0, size_vec3[0], Nx + 1)
    self.ymesh = numpy.linspace(0, size_vec3[1], Ny + 1)
    self.zmesh = numpy.linspace(0, size_vec3[2], Nz + 1)
    return (size_vec3, (Nx,Ny,Nz))

  def getXmeshCentres(self):
    return [ 0.5*(self.xmesh[i+1]+self.xmesh[i]) for i in range(len(self.xmesh)-1)]

  def getYmeshCentres(self):
    return [ 0.5*(self.ymesh[i+1]+self.ymesh[i]) for i in range(len(self.ymesh)-1)]

  def getZmeshCentres(self):
    return [ 0.5*(self.zmesh[i+1]+self.zmesh[i]) for i in range(len(self.zmesh)-1)]

  def getNcells(self):
    ''' Returns the number of cells in the mesh. '''
    return len(self.getXmeshDelta())*len(self.getYmeshDelta())*len(self.getZmeshDelta())

  def getSizeAndResolution(self):
    return ([self.xmesh[-1], self.ymesh[-1], self.zmesh[-1]],[len(self.getXmeshDelta()),len(self.getYmeshDelta()),len(self.getZmeshDelta())])

  def getExtension(self):
    return ([self.xmesh[0], self.ymesh[0], self.zmesh[0]], [self.xmesh[-1], self.ymesh[-1], self.zmesh[-1]])

  def getNearest(self, P, direction=0):
    x_idx, x_val = findNearestInSortedArray(self.getXmesh(), P[0], direction)
    y_idx, y_val = findNearestInSortedArray(self.getYmesh(), P[1], direction)
    z_idx, z_val = findNearestInSortedArray(self.getZmesh(), P[2], direction)
    return (x_idx, y_idx, z_idx), (x_val, y_val, z_val)

  def getIndexRange(self, lower, upper, direction=0):
    '''
    Convenience function to get absolute and relative index ranges based on a given real coordinates based block volume.
    
    Returns (idx_L, idx_U, relative_index_range_x, relative_index_range_y, relative_index_range_z)
    '''
    idx_L, val_L = self.getNearest(lower, direction)
    idx_U, val_U = self.getNearest(upper, direction)
    size, res = self.getSizeAndResolution()
    relative_index_range_x = (idx_L[0]/res[0], idx_U[0]/res[0])
    relative_index_range_y = (idx_L[1]/res[1], idx_U[1]/res[1])
    relative_index_range_z = (idx_L[2]/res[2], idx_U[2]/res[2])
    return (idx_L, idx_U, relative_index_range_x, relative_index_range_y, relative_index_range_z)

  def writeMesh(self, FILE=sys.stdout):
    warnings.warn("writeMesh() is deprecated, please use write_entry() instead.", DeprecationWarning)
    self.write_entry(FILE=FILE)
    return
    
  def write_entry(self, FILE=sys.stdout):
    '''
    writes mesh to FILE
    .. todo:: should be renamed to write_entry() for better standardization... (+ choose better name than write_entry() for all, like write(), writeEntry()?)
    '''
    # mesh X
    FILE.write('XMESH **name='+self.name+'\n')
    FILE.write('{\n')
    for i in range(len(self.getXmeshDelta())):
      FILE.write("%E\n" % self.getXmeshDelta()[i])
    FILE.write('}\n')
    FILE.write('\n')
  
    # mesh Y
    FILE.write('YMESH **name='+self.name+'\n')
    FILE.write('{\n')
    for i in range(len(self.getYmeshDelta())):
      FILE.write("%E\n" % self.getYmeshDelta()[i])
    FILE.write('}\n')
    FILE.write('\n')
  
    # mesh Z
    FILE.write('ZMESH **name='+self.name+'\n')
    FILE.write('{\n')
    for i in range(len(self.getZmeshDelta())):
      FILE.write("%E\n" % self.getZmeshDelta()[i])
    FILE.write('}\n')
    FILE.write('\n')
    return

class MeshingParameters(object):
  '''
  Object containing parameters that can be used for meshing (with the *subGridMultiLayer()* function for example).
  The *getMeshingParameters()* of the various BFDTD objects return such an object for example.
  
  List of attributes:
    * maximum permittivity lists
      * maxPermittivityVector_X
      * maxPermittivityVector_Y
      * maxPermittivityVector_Z
    * thickness lists
      * thicknessVector_X
      * thicknessVector_Y
      * thicknessVector_Z
    * limit lists
      * limits_X
      * limits_Y
      * limits_Z
  
  .. todo::
            Think about the best way to design this class and then do it.
  
              Might be better to really have delta+thickness for each object and then some global MeshingParameters with addMeshingParameters function.
              
              Permittivity to delta conversion could be specified differently for each object.
              
              * thickness <-> limits
              * delta <-factor*1/sqrt(permittivity)-> permittivity <-sqrt-> refractive index
  
  .. todo:: Combine with MeshObject? Create way to merge 2 or more existing meshes (i.e. MeshObject objects)? Create MeshObject from set of MeshingParameters? Don't forget about MEEP and BFDTD subgridding.
  .. todo:: support 1-D, 2-D (n-D?) meshing parameters as well
  '''
  
  def __init__(self):
    self.maxPermittivityVector_X = [1]
    self.thicknessVector_X = [1]
    self.maxPermittivityVector_Y = [1]
    self.thicknessVector_Y = [1]
    self.maxPermittivityVector_Z = [1]
    self.thicknessVector_Z = [1]
    self.limits_X = [0,1]
    self.limits_Y = [0,1]
    self.limits_Z = [0,1]
    
  def __str__(self):
    ret = 'maxPermittivityVector_X = '+str(self.maxPermittivityVector_X)+'\n'
    ret += 'thicknessVector_X = '+str(self.thicknessVector_X)+'\n'
    ret += 'maxPermittivityVector_Y = '+str(self.maxPermittivityVector_Y)+'\n'
    ret += 'thicknessVector_Y = '+str(self.thicknessVector_Y)+'\n'
    ret += 'maxPermittivityVector_Z = '+str(self.maxPermittivityVector_Z)+'\n'
    ret += 'thicknessVector_Z = '+str(self.thicknessVector_Z)+'\n'
    ret += 'limits_X = '+str(self.limits_X)+'\n'
    ret += 'limits_Y = '+str(self.limits_Y)+'\n'
    ret += 'limits_Z = '+str(self.limits_Z)
    return ret
  
  def addLimits_X(self,limits,permittivity):
    #print(limits)
    #print(permittivity)
    #print(limits.shape)
    #print(permittivity.shape)
    
    self.limits_X = numpy.vstack([self.limits_X,limits])
    self.maxPermittivityVector_X = numpy.vstack([self.maxPermittivityVector_X,permittivity])
    
  def addLimits_Y(self,limits,permittivity):
    self.limits_Y = numpy.vstack([self.limits_Y,limits])
    self.maxPermittivityVector_Y = numpy.vstack([self.maxPermittivityVector_Y,permittivity])
    
  def addLimits_Z(self,limits,permittivity):
    self.limits_Z = numpy.vstack([self.limits_Z,limits])
    self.maxPermittivityVector_Z = numpy.vstack([self.maxPermittivityVector_Z,permittivity])

def increaseResolution3D(mesh_orig, Nx, Ny, Nz):
  '''
  Applies increaseResolution() to all three directions and return a new MeshObject.
  '''
  mesh_new = MeshObject()
  mesh_new.setXmesh(increaseResolution(mesh_orig.getXmesh(), Nx))
  mesh_new.setYmesh(increaseResolution(mesh_orig.getYmesh(), Ny))
  mesh_new.setZmesh(increaseResolution(mesh_orig.getZmesh(), Nz))
  return mesh_new

if __name__ == "__main__":
  pass
