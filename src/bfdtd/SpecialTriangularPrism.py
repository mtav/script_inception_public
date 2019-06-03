#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import division
import copy
import numpy

from .BFDTDobject import BFDTDobject
from .GeometryObjects import GeometryObject, Sphere, Block, Distorted, Parallelepiped, Cylinder, Rotation, MeshBox

class SpecialTriangularPrism(GeometryObject):
  '''
  Creates prism with 45 degree mirrors. Should have support for arbitrarily angled mirrors at some point.
  
  .. todo:: non 45 degree faces, i.e. generic version which would also allow creation of parallel-sided prism
  .. todo:: It would be simpler to use the generic Distorted block... In any case: Better to "voxelize" in the "FDTD voxelizing engine" somehow.
  .. todo:: Should support same things as other geometry objects, in particular: rotation, bounding box... -> Find easy+flexible+extensible way to do this for compound objects like this one.
  '''
  
  def __init__(self,
    name = 'SpecialTriangularPrism',
    layer = 'SpecialTriangularPrism',
    group = 'SpecialTriangularPrism',
    lower = [0,0,0],
    upper = [1,1,1],
    permittivity = 1,# vacuum by default
    conductivity = 0,
    NvoxelsX = 10,
    NvoxelsY = 10,
    NvoxelsZ = 10,
    orientation = [0,1,2]):

    '''
    Constructor
    '''

    GeometryObject.__init__(self)
    self.name = name
    self.layer = layer
    self.group = group
    self.lower = lower
    self.upper = upper
    self.permittivity = permittivity
    self.conductivity = conductivity
    self.NvoxelsX = NvoxelsX
    self.NvoxelsY = NvoxelsY
    self.NvoxelsZ = NvoxelsZ
    self.orientation = orientation
    self.COMMENT = 'SpecialTriangularPrism'
    
    self.mirror1 = True
    self.mirror2 = True
    
  '''printer function'''
  def __str__(self):
    ret  = 'name = '+self.name+'\n'
    ret += 'lower = '+str(self.lower)+'\n'
    ret += 'upper = '+str(self.upper)+'\n'
    ret += 'permittivity = '+str(self.permittivity)+'\n'
    ret += 'conductivity = '+str(self.conductivity)+'\n'
    ret += 'NvoxelsX = '+str(self.NvoxelsX)+'\n'
    ret += 'NvoxelsY = '+str(self.NvoxelsY)+'\n'
    ret += 'NvoxelsZ = '+str(self.NvoxelsZ)+'\n'
    ret += 'orientation = '+str(self.orientation)+'\n'
    ret += Geometry_object.__str__(self)
    return ret
    
  #def read_entry(self,entry):
    #if entry.name:
      #self.name = entry.name
    #self.lower = float_array(entry.data[0:3])
    #self.upper = float_array(entry.data[3:6])
    #self.permittivity = float(entry.data[6])
    #self.conductivity = float(entry.data[7])
    
  '''returns voxels'''
  def getVoxels(self):
    #meshing_parameters = MeshingParameters()
    voxel_list = []
    ####################################
    # X = triangle size
    # Y = triangle peak
    # Z = prism length
    ####################################
    mini = [0,0,0]
    maxi = [0,0,0]
    mini[0] = self.lower[self.orientation.index(0)]
    mini[1] = self.lower[self.orientation.index(1)]
    mini[2] = self.lower[self.orientation.index(2)]
    maxi[0] = self.upper[self.orientation.index(0)]
    maxi[1] = self.upper[self.orientation.index(1)]
    maxi[2] = self.upper[self.orientation.index(2)]
    #print mini[0],maxi[0]
    #print mini[1],maxi[1]
    #print mini[2],maxi[2]
    DX = maxi[0] - mini[0]
    DY = maxi[1] - mini[1]
    DZ = maxi[2] - mini[2]
    R = 0.5*(maxi[0]-mini[0])
    NX = self.NvoxelsX
    NY = self.NvoxelsY
    NZ = self.NvoxelsZ
    #print DX,DY,DZ
    voxel_radius_X = R/( 2.*self.NvoxelsX + 1.)
    
    base_block = Block()
    base_block.setName(self.COMMENT)
    base_block.setRelativePermittivity(self.permittivity)
    base_block.setRelativeConductivity(self.conductivity)

    for iX in range(self.NvoxelsX):
      for iY in range(iX+1):
        # X- blocks
        L = [ mini[0]+2*R*(iX)/(2*NX+1), mini[1]+DY*(iY)/(NX+1.), mini[2]+DY*(iY)/(NX+1.)]
        U = [ mini[0]+2*R*(iX + 1)/(2*NX+1), mini[1]+DY*(iY + 1.)/(NX+1.), maxi[2]-DY*(iY)/(NX+1.)]
        LL = [ L[self.orientation[0]],L[self.orientation[1]],L[self.orientation[2]] ]
        UU = [ U[self.orientation[0]],U[self.orientation[1]],U[self.orientation[2]] ]
        self.meshing_parameters.addLimits_X(numpy.sort([LL[0],UU[0]]),self.permittivity)
        self.meshing_parameters.addLimits_Y(numpy.sort([LL[1],UU[1]]),self.permittivity)
        self.meshing_parameters.addLimits_Z(numpy.sort([LL[2],UU[2]]),self.permittivity)
        obj = copy.copy(base_block)
        obj.setLowerAbsolute(LL)
        obj.setUpperAbsolute(UU)
        voxel_list.append(obj)
        # X+ blocks
        L = [ mini[0]+2*R*((2*NX+1)-(iX))/(2*NX+1), mini[1]+DY*(iY)/(NX+1.), mini[2]+DY*(iY)/(NX+1.)]
        U = [ mini[0]+2*R*((2*NX+1)-(iX + 1))/(2*NX+1), mini[1]+DY*(iY + 1.)/(NX+1.), maxi[2]-DY*(iY)/(NX+1.)]
        LL = [ L[self.orientation[0]],L[self.orientation[1]],L[self.orientation[2]] ]
        UU = [ U[self.orientation[0]],U[self.orientation[1]],U[self.orientation[2]] ]
        self.meshing_parameters.addLimits_X(numpy.sort([LL[0],UU[0]]),self.permittivity)
        self.meshing_parameters.addLimits_Y(numpy.sort([LL[1],UU[1]]),self.permittivity)
        self.meshing_parameters.addLimits_Z(numpy.sort([LL[2],UU[2]]),self.permittivity)
        obj = copy.copy(base_block)
        obj.setLowerAbsolute(LL)
        obj.setUpperAbsolute(UU)
        voxel_list.append(obj)
      ## middle block
      L = [ mini[0]+2*R*(NX)/(2*NX+1), mini[1]+DY*(iX)/(NX+1.), mini[2]+DY*(iX)/(NX+1.)]
      U = [ mini[0]+2*R*(NX + 1)/(2*NX+1), mini[1]+DY*(iX+1)/(NX+1.), maxi[2]-DY*(iX)/(NX+1.)]
      LL = [ L[self.orientation[0]],L[self.orientation[1]],L[self.orientation[2]] ]
      UU = [ U[self.orientation[0]],U[self.orientation[1]],U[self.orientation[2]] ]
      self.meshing_parameters.addLimits_X(numpy.sort([LL[0],UU[0]]),self.permittivity)
      self.meshing_parameters.addLimits_Y(numpy.sort([LL[1],UU[1]]),self.permittivity)
      self.meshing_parameters.addLimits_Z(numpy.sort([LL[2],UU[2]]),self.permittivity)
      obj = copy.copy(base_block)
      obj.setLowerAbsolute(LL)
      obj.setUpperAbsolute(UU)
      voxel_list.append(obj)
    ## middle block
    L = [ mini[0]+2*R*(NX)/(2*NX+1), mini[1]+DY*(NX)/(NX+1.), mini[2]+DY*(NX)/(NX+1.)]
    U = [ mini[0]+2*R*(NX + 1)/(2*NX+1), mini[1]+DY, maxi[2]-DY*(NX)/(NX+1.)]
    LL = [ L[self.orientation[0]],L[self.orientation[1]],L[self.orientation[2]] ]
    UU = [ U[self.orientation[0]],U[self.orientation[1]],U[self.orientation[2]] ]
    self.meshing_parameters.addLimits_X(numpy.sort([LL[0],UU[0]]),self.permittivity)
    self.meshing_parameters.addLimits_Y(numpy.sort([LL[1],UU[1]]),self.permittivity)
    self.meshing_parameters.addLimits_Z(numpy.sort([LL[2],UU[2]]),self.permittivity)
    obj = copy.copy(base_block)
    obj.setLowerAbsolute(LL)
    obj.setUpperAbsolute(UU)
    voxel_list.append(obj)
    ####################################
    #return (voxel_list, meshing_parameters)
    return voxel_list

  def write_entry(self, FILE):
    '''
    writes the voxels to the file corresponding to the FILE handle
    '''
    voxels = self.getVoxels()
    for v in voxels:
      v.write_entry(FILE)
  
  '''returns the centre of the bounding box of the prism'''
  def getBoundingBoxCentre(self):
    C = [ 0.5*(self.lower[0]+self.upper[0]), 0.5*(self.lower[1]+self.upper[1]), 0.5*(self.lower[2]+self.upper[2]) ]
    return(C)

  '''returns the barycentre of the prism'''
  def getGeoCentre(self):
    (A1,B1,C1,A2,B2,C2) = self.getLocalEnvelopPoints()
    G = (A1+B1+C1+A2+B2+C2)/6.0
    GG = [ G[self.orientation[0]],G[self.orientation[1]],G[self.orientation[2]] ]
    return(GG)

  '''returns the envelop points (A1,B1,C1,A2,B2,C2) in global coordinates'''
  def getGlobalEnvelopPoints(self):
    (A1_local,B1_local,C1_local,A2_local,B2_local,C2_local) = self.getLocalEnvelopPoints()
    A1_global = self.local2global(A1_local)
    B1_global = self.local2global(B1_local)
    C1_global = self.local2global(C1_local)
    A2_global = self.local2global(A2_local)
    B2_global = self.local2global(B2_local)
    C2_global = self.local2global(C2_local)
    return(A1_global,B1_global,C1_global,A2_global,B2_global,C2_global)
  
  '''returns the envelop points (A1,B1,C1,A2,B2,C2) in local coordinates'''
  def getLocalEnvelopPoints(self):
    ####################################
    # X = triangle size
    # Y = triangle peak
    # Z = prism length
    ####################################
    mini = [0,0,0]
    maxi = [0,0,0]
    mini[0] = self.lower[self.orientation.index(0)]
    mini[1] = self.lower[self.orientation.index(1)]
    mini[2] = self.lower[self.orientation.index(2)]
    maxi[0] = self.upper[self.orientation.index(0)]
    maxi[1] = self.upper[self.orientation.index(1)]
    maxi[2] = self.upper[self.orientation.index(2)]
    DX = maxi[0] - mini[0]
    DY = maxi[1] - mini[1]
    DZ = maxi[2] - mini[2]
    print('Prism dimensions = ',[DX,DY,DZ])
    #x
    #mini[0]
    #0.5*(maxi[0]+mini[0])
    #maxi[0]

    #y
    #mini[1]
    #maxi[1]
    
    #z
    #mini[2]
    #mini[2]+DY
    #maxi[2]-DY
    #maxi[2]
    
    #bottom triangle
    A1 = numpy.array([mini[0],mini[1],mini[2]])
    B1 = numpy.array([0.5*(maxi[0]+mini[0]),maxi[1],mini[2]+DY])
    C1 = numpy.array([maxi[0],mini[1],mini[2]])
    #top triangle
    A2 = numpy.array([mini[0],mini[1],maxi[2]])
    B2 = numpy.array([0.5*(maxi[0]+mini[0]),maxi[1],maxi[2]-DY])
    C2 = numpy.array([maxi[0],mini[1],maxi[2]])

    return(A1,B1,C1,A2,B2,C2)
  
  '''convert from global to local coordinates'''
  def global2local(self, P_global):
    P_local = numpy.array([ P_global[self.orientation.index(0)], P_global[self.orientation.index(1)], P_global[self.orientation.index(2)] ])
    return P_local
    
  '''convert from local to global coordinates'''
  def local2global(self, P_local):
    P_global = numpy.array([ P_local[self.orientation[0]],P_local[self.orientation[1]],P_local[self.orientation[2]] ])
    return P_global
    
  '''returns the radius (i.e. sidelength/2) of a square inscribed inside the prism cross-section'''
  def getInscribedSquarePlaneRadius(self, G_global):
    G_local = self.global2local(G_global)
    G = numpy.matrix([ [G_local[0]], [G_local[1]] ])
    (A1,B1,C1,A2,B2,C2) = self.getLocalEnvelopPoints()
    B = numpy.matrix([ [B1[0]], [B1[1]] ])
    C = numpy.matrix([ [C1[0]], [C1[1]] ])
    v = numpy.matrix([ [-1], [-1] ])
    BC = C-B
    print('v = '+str(v))
    print('B = '+str(B))
    print('C = '+str(C))
    print('G = '+str(G))
    
    M = numpy.hstack((v,BC))
    print(M)
    kl = M.getI() * (G-B)
    k = kl[0,0]
    radius = abs(k)
    return(radius)

  '''returns the meshing parameters for the prism'''
  def getMeshingParameters(self,xvec,yvec,zvec,epsx,epsy,epsz):
    #meshing_parameters = MeshingParameters()
    voxel_list = self.getVoxels()
    #voxel_list, meshing_parameters = self.getVoxels()
    xvec = numpy.vstack([xvec,self.meshing_parameters.limits_X])
    yvec = numpy.vstack([yvec,self.meshing_parameters.limits_Y])
    zvec = numpy.vstack([zvec,self.meshing_parameters.limits_Z])
    epsx = numpy.vstack([epsx,self.meshing_parameters.maxPermittivityVector_X])
    epsy = numpy.vstack([epsy,self.meshing_parameters.maxPermittivityVector_Y])
    epsz = numpy.vstack([epsz,self.meshing_parameters.maxPermittivityVector_Z])
    return xvec,yvec,zvec,epsx,epsy,epsz

  '''returns the dimension of a single voxel in global coordinates as [dX,dY,dZ]'''
  def getVoxelDimensions(self):
    #dX = self.meshing_parameters.limits_X[1]-self.meshing_parameters.limits_X[0]
    #dY = self.meshing_parameters.limits_Y[1]-self.meshing_parameters.limits_Y[0]
    #dZ = self.meshing_parameters.limits_Z[1]-self.meshing_parameters.limits_Z[0]
        ##meshing_parameters = MeshingParameters()
    #voxel_list = []
    #####################################
    ## X = triangle size
    ## Y = triangle peak
    ## Z = prism length
    #####################################
    mini = self.global2local(self.lower)
    maxi = self.global2local(self.upper)
    ##maxi = [0,0,0]
    ##mini[0] = self.lower[self.orientation.index(0)]
    ##mini[1] = self.lower[self.orientation.index(1)]
    ##mini[2] = self.lower[self.orientation.index(2)]
    ##maxi[0] = self.upper[self.orientation.index(0)]
    ##maxi[1] = self.upper[self.orientation.index(1)]
    ##maxi[2] = self.upper[self.orientation.index(2)]
    ##print mini[0],maxi[0]
    ##print mini[1],maxi[1]
    ##print mini[2],maxi[2]
    DX = maxi[0] - mini[0]
    DY = maxi[1] - mini[1]
    DZ = maxi[2] - mini[2]
    NX = self.NvoxelsX
    NY = self.NvoxelsY
    NZ = self.NvoxelsZ
    ##print DX,DY,DZ
    # TODO: Correct this
    dX = DX/( 2.*self.NvoxelsX + 1.)
    dY = DY/(self.NvoxelsY)
    dZ = DZ/(self.NvoxelsZ)
    voxeldim_local = [dX,dY,dZ]
    voxeldim_global = self.local2global(voxeldim_local)
    return voxeldim_global
    
  '''moves the prism so that its barycentre is at position P'''
  def setGeoCentre(self,P):
    current = self.getGeoCentre()
    print('self.getGeoCentre() = ',current)
    self.lower = numpy.array(self.lower) + (numpy.array(P) - current)
    self.upper = numpy.array(self.upper) + (numpy.array(P) - current)

if __name__ == "__main__":
  foo = TriangularPrism()
  foo.getVoxels()
  #foo.write_entry()
