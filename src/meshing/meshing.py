#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''This module handles the new meshing system.

Currently only designed for BFDTD simulations, i.e. for a final heterogeneous rectilinear grid.
But it is completely independent of BFDTDobject or any other FDTD related code.
VTK-related code will be added to it later eventually.

The class design is as follows:

* **Mesh3D**: Consists of 3 *MultiMesh1D*, for the X, Y and Z directions.

  * **MultiMesh1D**: Contains a list of *Mesh1D* or *MultiMesh1D* objects.

    * **Mesh1D**: A generic parent class for 1D meshes.

      * **HeterogeneousMesh1D**: A heterogeneous mesh defined by its attribute *coordinates*.
      * **HomogeneousMesh1D**: A homogeneous mesh defined by its attributes *pos_min*, *pos_max*, *spacing_max*. *spacing_max* is used to determine the number of points/cells.
      
        * **HomogeneousMeshParameters1D**: A subclass of *HomogeneousMesh1D*, but for which the *MultiMesh1D::getLocalCoordinates()* function will take *spacing_max* into account to merge multiple *HomogeneousMeshParameters1D* in a smart way.
      
.. digraph:: meshing_system_diagram

   edge [style=dashed,color=red, dir=back];
   "Mesh3D" -> "MultiMesh1D" -> "Mesh1D";
   edge [style=solid,color=black, dir=back];
   "Mesh1D" -> {"HomogeneousMesh1D","HeterogeneousMesh1D"};
   "HomogeneousMesh1D" -> "HomogeneousMeshParameters1D"

.. todo:: Mesh3D might be left out completely. It means we have to give each geometric object 3 attributes, but allows for more flexibility. In any case, it's better to finish the mesh1D system first and deal with Mesh3D later.
.. todo:: MultiMesh3D?

idea: Make various meshing algorithms available and allow user-created ones (ex: structure-specific meshing algorithms, tests of meshing on simulation results).
'''

import os
import sys
import copy
import tempfile
import unittest
import numpy
from numpy import linspace, array

class Mesh3D():
  '''A rectilinear structured 3D mesh/grid.'''

  def __init__(self):
    '''constructor'''
    self.name = self.__class__.__name__ #: a name for easier debugging
    self.parent = None
    self.location = array([0,0,0])
    
    self.xmesh = MultiMesh1D() #: the 1D mesh in the X direction
    self.ymesh = MultiMesh1D() #: the 1D mesh in the Y direction
    self.zmesh = MultiMesh1D() #: the 1D mesh in the Z direction
    return

  #@property
  #def location(self):
    #return array([self.xmesh.location, self.ymesh.location, self.zmesh.location])

  #@location.setter
  #def location(self, value):
    #self.xmesh.location = value[0]
    #self.ymesh.location = value[1]
    #self.zmesh.location = value[2]

  #@property
  #def parent(self):
    #return array([self.xmesh.location, self.ymesh.location, self.zmesh.location])

  #@parent.setter
  #def parent(self, value):
    #self.xmesh.parent = value.xmesh
    #self.ymesh.parent = value.ymesh
    #self.zmesh.parent = value.zmesh

  def getGlobalLocation(self):
    if self.parent is None:
      return self.location
    else:
      return self.location + self.parent.getGlobalLocation()

  def PrintSelf(self, indent=''):
    '''printing function with indent'''
    ret = ''
    ret += indent + 'name = ' + self.name + '\n'
    ret += indent + 'location = {}'.format(self.location) + '\n'
    if self.parent:
      ret += indent + 'parent.id = {}'.format(self.parent.__repr__()) + '\n'
      ret += indent + 'parent.name = {}'.format(self.parent.name) + '\n'
    else:
      ret += indent + 'parent.id = None' + '\n'
    ret += indent + 'xmesh:\n' + self.xmesh.PrintSelf(indent+' ') + '\n' +\
    indent + 'ymesh:\n' + self.ymesh.PrintSelf(indent+' ') + '\n' +\
    indent + 'zmesh:\n' + self.zmesh.PrintSelf(indent+' ')
    return ret

  def __str__(self):
    '''printing function'''
    return self.PrintSelf()

  def setUseForMeshing(self, bool_value):
    '''Set the *useForMeshing* attribute to *bool_value* for xmesh, ymesh and zmesh.'''
    self.xmesh.setUseForMeshing(bool_value)
    self.ymesh.setUseForMeshing(bool_value)
    self.zmesh.setUseForMeshing(bool_value)
    return

  def setAllowResolutionScaling(self, bool_value):
    '''Set the *allowResolutionScaling* attribute to *bool_value* for xmesh, ymesh and zmesh.'''
    self.xmesh.setAllowResolutionScaling(bool_value)
    self.ymesh.setAllowResolutionScaling(bool_value)
    self.zmesh.setAllowResolutionScaling(bool_value)
    return

  def setResolutionScalingFactor(self, float_value):
    '''Set the *resolutionScalingFactor* attribute to *bool_value* for xmesh, ymesh and zmesh.'''
    self.xmesh.setResolutionScalingFactor(float_value)
    self.ymesh.setResolutionScalingFactor(float_value)
    self.zmesh.setResolutionScalingFactor(float_value)
    return

  def getGlobalXCoordinates(self):
    '''get the grid coordinates in the x-direction.'''
    return self.getGlobalLocation()[0] + array(self.xmesh.getGlobalCoordinates())

  def getGlobalYCoordinates(self):
    '''get the grid coordinates in the y-direction.'''
    return self.getGlobalLocation()[1] + array(self.ymesh.getGlobalCoordinates())

  def getGlobalZCoordinates(self):
    '''get the grid coordinates in the z-direction.'''
    return self.getGlobalLocation()[2] + array(self.zmesh.getGlobalCoordinates())

class MultiMesh1D():
  '''An object consisting of multiple **Mesh1D** or **MultiMesh1D** objects.
  
  The idea is to for example create one main mesh for the FDTD simulation consisiting of multiple submeshes for each FDTD object in the simulation.
  Each of these object submeshes can then also consist of multiple submeshes, again being either **Mesh1D** or **MultiMesh1D**.
  
  *getLocalCoordinates()* will go through all those meshes recursively and return a single merged one.
  
  The extension of that system to 3 or more or less dimensions is then straightforward and done via the **Mesh3D** class.
  
  .. todo:: Use the submesh order when merging the submeshes as a "priority system".
  '''

  def __init__(self):
    '''constructor'''
    self.name = self.__class__.__name__ #: a name for easier debugging
    self.location = 0
    self.parent = None
    
    self.mesh_list = [] #: The list of **Mesh1D** or **MultiMesh1D** objects.
    
    self.minimum_mesh_delta = 1e-3 #: The minimum cell size allowed. This is used when merging the various submeshes. Default: 1e-3. Set to ``None`` to disable.
    self.maximum_mesh_delta_ratio = 2 #: For creating a smooth mesh. Neighboring cell sizes should not exceed a factor of *maximum_mesh_delta_ratio*. Default: 2. Set to ``None`` to disable.
    self.maximum_mesh_delta_vacuum = None #: If set, the mesh will be checked for any cells larger than ``maximum_mesh_delta_vacuum * spacing_max`` (*spacing_max* set to 1 if the *Mesh1D* object does not provide it). Default: None. Set to ``None`` to disable.

    # for vol ratio max = 2
    # TODO: make default? (after submitting RCD jobs)
    #self.maximum_mesh_delta_ratio = pow(2,1/3)    

    return

  # TODO: Looks like things are getting out of hand again. Do we really need such a flexible/complicated system???
  def addChild(self, m):
    self.mesh_list.append(m)
    m.parent = self
    
  def makeAllSubMeshesChildren(self):
    for m in self.mesh_list:
      m.parent = self

  def getGlobalLocation(self):
    if self.parent is None:
      return self.location
    else:
      return self.location + self.parent.getGlobalLocation()

  def PrintSelf(self, indent=''):
    '''printing function with indent'''
    ret = ''
    ret += indent + 'name = ' + self.name + '\n'
    ret += indent + 'location = {}'.format(self.location) + '\n'
    if self.parent:
      ret += indent + 'parent.id = {}'.format(self.parent.__repr__()) + '\n'
      ret += indent + 'parent.name = {}'.format(self.parent.name) + '\n'
    else:
      ret += indent + 'parent.id = None' + '\n'
    ret += indent + 'minimum_mesh_delta = ' + str(self.minimum_mesh_delta) + '\n'
    ret += indent + 'maximum_mesh_delta_ratio = ' + str(self.maximum_mesh_delta_ratio) + '\n'
    ret += indent + 'maximum_mesh_delta_vacuum = ' + str(self.maximum_mesh_delta_vacuum) + '\n'

    if self.mesh_list:
      ret += indent + 'mesh_list:\n'
      for idx, submesh in enumerate(self.mesh_list):
        ret += submesh.PrintSelf(indent + ' ')
        ret += '\n'
        if idx < len(self.mesh_list)-1:
          ret += '\n'
    else:
      ret += indent + 'mesh_list: ' + str(self.mesh_list)
    
    return ret

  def __str__(self):
    '''printing function'''
    return self.PrintSelf()
    
  def setUseForMeshing(self, bool_value):
    '''Set the *useForMeshing* attribute to *bool_value* for all submeshes.'''
    for m in self.mesh_list:
      m.setUseForMeshing(bool_value)
    return

  def setAllowResolutionScaling(self, bool_value):
    '''Set the *allowResolutionScaling* attribute to *bool_value* for all submeshes.'''
    for m in self.mesh_list:
      m.setAllowResolutionScaling(bool_value)
    return

  def setResolutionScalingFactor(self, float_value):
    '''Set the *resolutionScalingFactor* attribute to *float_value* for all submeshes.'''
    for m in self.mesh_list:
      m.setResolutionScalingFactor(float_value)
    return
    
  def getMesh1DList(self):
    '''Converts the submesh list into one containing only Mesh1D objects by iterating through the submeshes recursively.'''
    
    mesh1D_list = []
    
    for submesh in self.mesh_list:
      if isinstance(submesh, MultiMesh1D):
        mesh1D_list.extend(submesh.getMesh1DList())
      elif isinstance(submesh, Mesh1D):
        mesh1D_list.append(submesh)
      else:
        raise TypeError( 'Invalid mesh type: {}'.format(type(submesh)) )
    
    return mesh1D_list

  def getGlobalCoordinates(self):
    coords = self.getLocalCoordinates()
    return(self.getGlobalLocation() + array(coords))
    
  def getLocalCoordinates(self):
    '''Returns the list of merged and sorted coordinates from all submeshes.
    
    .. note:: Meshes of type *HomogeneousMesh1D* are handled in a special way, in the sense that their *spacing_max* values are compared to choose the smallest one in case of overlap.
        
    '''
    
    # The list of coordinates that will be returned at the end.
    merged_coordinates = []
    
    # list of only mesh1D objects
    mesh1D_list = self.getMesh1DList()
    
    # list of "meshing parameters" which need to be merged in a smart way.
    meshing_parameters_list = []
    
    # list of normal meshes that can be merged directly.
    direct_mesh_list = []
    
    # loop through the Mesh1D objects
    for submesh in mesh1D_list:
      if not isinstance(submesh, Mesh1D):
        raise TypeError( 'Invalid mesh type: {}'.format(type(submesh)) )
      
      if isinstance(submesh, HomogeneousMeshParameters1D):
        meshing_parameters_list.append(submesh)
      else:
        direct_mesh_list.append(submesh)
    
    if meshing_parameters_list:
      
      # quick hack to submit RCD111 jobs...
      meshing_parameters_list = hackMesh(meshing_parameters_list)
      
      # create a direct mesh from the meshing parameters
      coords = mergeMeshingParameters(meshing_parameters_list)
      merged_parametrized_meshes = HeterogeneousMesh1D(coords)    
      
      # add the new direct mesh to direct_mesh_list
      direct_mesh_list.append(merged_parametrized_meshes)
    
    # merge the direct meshes together (sort->unique)
    for submesh in direct_mesh_list:
      merged_coordinates.extend(submesh.getGlobalCoordinates())
    
    merged_coordinates = sorted(set(merged_coordinates))
    
    # TODO: re-enable this, once new RCD structures are submitted?
    #checkMesh(merged_coordinates, self.minimum_mesh_delta, self.maximum_mesh_delta_ratio)
    
    #thickness_list = numpy.diff(merged_coordinates)
    #for (idx, thickness) in enumerate(thickness_list):
      #if self.minimum_mesh_delta:
        #if thickness < self.minimum_mesh_delta:
          #raise Exception('(thickness={}) < (minimum_mesh_delta={})'.format(thickness, self.minimum_mesh_delta))
      #if self.maximum_mesh_delta_ratio:
        #if idx+1 < len(thickness_list):
          #t0 = thickness_list[idx]
          #t1 = thickness_list[idx+1]
          #if max(t0,t1)/min(t0,t1) > self.maximum_mesh_delta_ratio:
            #raise Exception('max(t0,t1)={}/min(t0,t1)={} > self.maximum_mesh_delta_ratio={}'.format(max(t0,t1), min(t0,t1), self.maximum_mesh_delta_ratio))
    
    return merged_coordinates

  def renderInBlender(self, location=None, group='meshes'):
    if location is None:
      location = self.getGlobalLocation()
    
    for m in self.mesh_list:
      m.renderInBlender(location, group)
    return

  def renderXMesh1D(self, location=None, group='meshes'):
    if location is None:
      location = self.getGlobalLocation()
    
    for m in self.mesh_list:
      m.renderXMesh1D(location, group)
    return

  def renderYMesh1D(self, location=None, group='meshes'):
    if location is None:
      location = self.getGlobalLocation()
    
    for m in self.mesh_list:
      m.renderYMesh1D(location, group)
    return

  def renderZMesh1D(self, location=None, group='meshes'):
    if location is None:
      location = self.getGlobalLocation()
    
    for m in self.mesh_list:
      m.renderZMesh1D(location, group)
    return

def hackMesh(meshing_parameters_list):
  
  nuke_list = []
  lower = numpy.inf
  upper = -numpy.inf
  for submesh in meshing_parameters_list:
    if submesh.nukeothers:
      nuke_list.append(submesh)
      L = min( submesh.pos_min, submesh.pos_max)
      U = max( submesh.pos_min, submesh.pos_max)
      if L < lower:
        lower = L
      if U > upper:
        upper = U

  if len(nuke_list) == 0:
    return meshing_parameters_list

  new_list = nuke_list

  for submesh in meshing_parameters_list:
    if not submesh.nukeothers:
      if max(submesh.pos_min, submesh.pos_max) <= lower:
        new_list.append(submesh)
      elif min(submesh.pos_min, submesh.pos_max) >= upper:
        new_list.append(submesh)
      else:
        if lower <= submesh.pos_min <= upper and lower <= submesh.pos_max <= upper:
          pass
        elif lower <= submesh.pos_min <= upper and upper < submesh.pos_max:
          submesh.pos_min = upper
          new_list.append(submesh)
        elif submesh.pos_min < lower and lower <= submesh.pos_max <= upper:
          submesh.pos_max = lower
          new_list.append(submesh)
        elif submesh.pos_min < lower and upper < submesh.pos_max:
          submesh1 = copy.deepcopy(submesh)
          submesh2 = copy.deepcopy(submesh)
          submesh1.pos_max = lower
          submesh2.pos_min = upper
          new_list.append(submesh1)
          new_list.append(submesh2)
        else:
          raise Exception('submesh: {} {}\nlower: {} upper: {}'.format(submesh.pos_min, submesh.pos_max, lower, upper))
      
  return new_list

class Mesh1D():
  '''Generic parent class for 1D meshes.
  It is used for *HeterogeneousMesh1D* and *HomogeneousMesh1D*.
  Other mesh types like a logarithmic mesh for example, could be added later.
  
  Subclasses must all re-implement the following functions:
  
  * *getLocalCoordinates()*
  
  :ivar bool useForMeshing: If true, it will be used to create the final mesh. Default: True.
  :ivar bool allowResolutionScaling: If true, changing the resolution settings to increase or decrease the number of cells will be allowed. Default: True.
  :ivar float resolutionScalingFactor: Allows increasing or decreasing the number of total cells in the mesh (if the mesh class supports it). Default: 1.
  
  '''
  def __init__(self):
    '''constructor'''

    self.name = self.__class__.__name__ #: a name for easier debugging
    self.location = 0
    self.parent = None

    self.useForMeshing = True #: If true, it will be used to create the final mesh. Default: True.
    self.allowResolutionScaling = True #: If true, changing the resolution settings to increase or decrease the number of cells will be allowed. Default: True.
    self.resolutionScalingFactor = 1 #: Allows increasing or decreasing the number of total cells in the mesh (if the mesh class supports it). Default: 1.
    return

  def getGlobalLocation(self):
    if self.parent is None:
      return self.location
    else:
      return self.location + self.parent.getGlobalLocation()
  
  def PrintSelf(self, indent=''):
    '''printing function with indent'''
    ret = ''
    ret += indent + 'name = {}'.format(self.name) + '\n'
    ret += indent + 'location = {}'.format(self.location) + '\n'
    if self.parent:
      ret += indent + 'parent.id = {}'.format(self.parent.__repr__()) + '\n'
      ret += indent + 'parent.name = {}'.format(self.parent.name) + '\n'
    else:
      ret += indent + 'parent.id = None' + '\n'
    ret += indent + 'useForMeshing = {}'.format(self.useForMeshing) + '\n'
    ret += indent + 'allowResolutionScaling = {}'.format(self.allowResolutionScaling) + '\n'
    ret += indent + 'resolutionScalingFactor = {}'.format(self.resolutionScalingFactor)
    return ret
    
  def __str__(self):
    '''printing function'''
    return self.PrintSelf()
  
  def setUseForMeshing(self, bool_value):
    '''Set the *useForMeshing* attribute to *bool_value*.'''
    self.useForMeshing = bool_value
    return

  def setAllowResolutionScaling(self, bool_value):
    '''Set the *allowResolutionScaling* attribute to *bool_value*.'''
    self.allowResolutionScaling = bool_value
    return

  def setResolutionScalingFactor(self, float_value):
    '''Set the *resolutionScalingFactor* attribute to *float_value*.'''
    self.resolutionScalingFactor = float_value
    return
  
  def getGlobalCoordinates(self):
    coords = self.getLocalCoordinates()
    return(self.getGlobalLocation() + array(coords))
  
  def getLocalCoordinates(self):
    '''Returns the list of coordinates. **Must be re-implemented.**
    
    .. note:: Do not forget to take into account the Mesh1D attributes when implementing *getLocalCoordinates()*.
    '''
    raise Exception("You should not use Mesh1D::getLocalCoordinates directly. It must be re-implemented in a subclass instead.")

  def getBounds(self):
    '''Returns the minimum and maximum values of the coordinates in the form (pos_min, pos_max).'''
    coordinates = self.getLocalCoordinates()
    return (min(coordinates), max(coordinates))

  def getThicknessList(self):
    '''Returns a list of the thicknesses of each section.'''
    return( list(numpy.diff(self.getLocalCoordinates())) )

class LogMesh1D(Mesh1D):
  '''A logarithmic mesh.'''

  def __init__(self):
    '''constructor'''
    self.start = 0
    self.stop = 1
    self.num = 50
    self.endpoint = True
    self.base = 10.0
    self.dtype = None
    return

class HeterogeneousMesh1D(Mesh1D):
  '''Very basic class storing parameters for a heterogeneous 1D mesh.'''

  def __init__(self, coordinates=None):
    '''constructor'''
    
    # call any parent's class constructor.
    super().__init__()
    
    if coordinates is None: coordinates = [0, 1]
    self.coordinates = coordinates #: list of the position of mesh lines. Type: List of floats. Default: [0, 1]
    
    return

  def PrintSelf(self, indent=''):
    '''printing function with indent'''
    ret = ''
    ret += super().PrintSelf(indent) + '\n'
    ret += indent + 'coordinates = ' + str(self.coordinates)
    return ret
    
  def __str__(self):
    '''printing function'''
    return self.PrintSelf()

  def getLocalCoordinates(self):
    '''Returns the list of coordinates.'''
    return self.coordinates

  def createFromThicknessList(self, pos_min, ThicknessList):
    '''Creates a list of coordinates of the form:
    
    * pos_min
    * pos_min + ThicknessList[0]
    * pos_min + ThicknessList[0] + ThicknessList[1]
    * ...
    '''
    self.coordinates = list(numpy.cumsum(numpy.hstack((pos_min, ThicknessList))))
    return

class HomogeneousMesh1D(Mesh1D):
  '''
  Class storing parameters for a homogeneous 1D mesh.

  This class uses *spacing_max* as main attribute instead of a given number of cells for more flexibility.
  This is useful when merging meshes (cf: :py:class:`HomogeneousMeshParameters1D`).
  But when a thickness or position list is requested, we simply switch to "N" as main, i.e. we create a homogeneous mesh.
    
  In general, for FDTD, we want: ``spacing_max < F*lambda*1/n``, with ``n=sqrt(epsilon_r)``.
  
  Since the factor *F* (usually around 1/15) and *lambda* are the only "geometry independent" settings, we bind them together into the *resolutionScalingFactor*.
  
  So we use the remaining "geometry dependent" terms *n* (refractive index) and *epsilon_r* (relative permittivity) to define *spacing_max*.
  
  Thus we define the following "terms" for use in this class and the meshing system:
  
  * **refractive index** *n*: ``1/spacing_max``
  * **relative permittivity** *epsilon_r*: ``(1/spacing_max)^2``
  * **resolutionScalingFactor**: ``1/(F*lambda)`` (so that increasing it, decreases *spacing_max* and therefore increases *NcellsMin*)
  * **Minimum number of cells** *NcellsMin* : ``ceil( abs(pos_max-pos_min)/spacing_max )``

  *spacing_max* can then be set via:
  
  * setSpacingMax(spacing_max)
  * setRefractiveIndexMin(n)
  * setRelativePermittivityMin(epsilon_r)
  * setNcellsMin(NcellsMin)
  
  Corresponding *get* functions are also available.

  .. note:: **resolutionScalingFactor** is only used when getLocalCoordinates() is called!

  :param float pos_min: minimum position
  :param float pos_max: maximum position
  :param float spacing_max: maximum *delta*, i.e. cell thickness.
  
  '''

  def __init__(self, pos_min = None, pos_max = None, spacing_max = None):
    '''constructor'''

    # call any parent's class constructor.
    super().__init__()

    if pos_min is None: pos_min = 0
    if pos_max is None: pos_max = 1
    if spacing_max is None: spacing_max = numpy.inf
    
    self.pos_min = min(pos_min, pos_max)
    self.pos_max = max(pos_min, pos_max)
    self.spacing_max = spacing_max

    self.nukeothers = False
    self.forceEvenNumberOfCells = False

    return

  def PrintSelf(self, indent=''):
    '''printing function with indent'''
    ret = ''
    ret += super().PrintSelf(indent) + '\n'
    ret += indent + 'pos_min = ' + str(self.pos_min) + '\n'
    ret += indent + 'pos_max = ' + str(self.pos_max) + '\n'
    ret += indent + 'spacing_max = ' + str(self.spacing_max)
    return ret
    
  def __str__(self):
    '''printing function'''
    return self.PrintSelf()

  def getLocalCoordinates(self):
    '''Returns the list of coordinates. It takes into account **Mesh1D::resolutionScalingFactor**.
    
    .. todo:: Possible code duplication reduction.
    '''
    
    if self.allowResolutionScaling:
      # mesh extension
      Delta = abs(self.pos_max - self.pos_min)
      # We take the absolute value to avoid problems with linspace and the ceiling because it is a minimum value.
      NcellsMin = numpy.ceil( abs( self.resolutionScalingFactor * Delta / self.spacing_max ) )
    else:
      NcellsMin = self.getNcellsMin()
    
    # Make sure we have at least one cell.
    if NcellsMin < 1:
      NcellsMin = 1
    
    #raise
    #if self.forceEvenNumberOfCells:
      #raise
      #if NcellsMin%2 == 1:
        #NcellsMin += 1
    
    return numpy.linspace(self.pos_min, self.pos_max, NcellsMin + 1)

  def setExtension(self, pos_min, pos_max):
    '''set the extension'''
    self.pos_min = min(pos_min, pos_max)
    self.pos_max = max(pos_min, pos_max)
    return

  def setSpacingMax(self, spacing_max):
    ''' set the maximum spacing '''
    self.spacing_max = spacing_max
    
  def getSpacingMax(self):
    ''' get the maximum spacing '''
    return(self.spacing_max)

  def setNcellsMin(self, NcellsMin):
    ''' set the minimum number of "cells" in the mesh (NOT the number of "positions", which is ``NcellsMin + 1``) '''
    self.spacing_max = abs(self.pos_max - self.pos_min) / float(NcellsMin)
    return

  def getNcellsMin(self):
    ''' get the minimum number of "cells" in the mesh (NOT the number of "positions", which is ``NcellsMin + 1``) '''
    NcellsMin = numpy.ceil(abs(self.pos_max-self.pos_min)/float(self.spacing_max))
    
    if NcellsMin < 1:
      NcellsMin = 1
    return(NcellsMin)
  
  def setRelativePermittivityMin(self, epsilon_r):
    ''' set the minimum "relative permittivity" defined as ``(1/spacing_max)^2`` '''
    self.spacing_max = 1./numpy.sqrt(epsilon_r)
    return
    
  def getRelativePermittivityMin(self):
    ''' get the minimum "relative permittivity" defined as ``(1/spacing_max)^2`` '''
    return( numpy.power(1./self.spacing_max, 2) )

  def setRefractiveIndexMin(self, RefractiveIndexMin):
    ''' set the minimum "refractive index" defined as ``1/spacing_max`` '''
    self.spacing_max = 1./RefractiveIndexMin
    return
    
  def getRefractiveIndexMin(self):
    ''' get the minimum "refractive index" defined as ``1/spacing_max`` '''
    return( 1./self.spacing_max )
  
  def renderInBlender(self, location=None, group='meshes'):
    import bpy
    import bmesh
    from mathutils import Vector
    from bpy_extras import object_utils #Blender 2.63
        
    if location is None:
      location = self.getGlobalLocation()
    
    coords = self.getLocalCoordinates()
    mesh = bpy.data.meshes.new(self.name)
    bm = bmesh.new()
    for (idx, x) in enumerate(coords):
      if 0 < idx and idx < len(coords)-1:
        h = 0.5
      else:
        h = 1
      bm.verts.new([x, 0, 0])
      bm.verts.new([x, h, 0])
      bm.edges.new([bm.verts[2*idx], bm.verts[2*idx+1]])
    bm.to_mesh(mesh)
    mesh.update()
    object_utils.object_data_add(bpy.context, mesh)
    
    obj = bpy.context.active_object
    obj.name = self.name
    obj.location = Vector(location)

    if not group in bpy.data.groups: bpy.ops.group.create(name=group)
    bpy.ops.object.group_link(group=group)

    return(obj)
    
  def renderXMesh1D(self, location=None, group='meshes'):
    import bpy
    import bmesh
    from mathutils import Vector
    from bpy_extras import object_utils #Blender 2.63
        
    if location is None:
      location = self.getGlobalLocation()
    
    coords = self.getLocalCoordinates()
    mesh = bpy.data.meshes.new(self.name)
    bm = bmesh.new()
    for (idx, x) in enumerate(coords):
      if 0 < idx and idx < len(coords)-1:
        h = 0.5
      else:
        h = 1
      bm.verts.new([x, 0, 0])
      bm.verts.new([x, h, 0])
      bm.verts.new([x, 0, h])
      bm.edges.new([bm.verts[3*idx], bm.verts[3*idx+1]])
      bm.edges.new([bm.verts[3*idx], bm.verts[3*idx+2]])
    bm.to_mesh(mesh)
    mesh.update()
    object_utils.object_data_add(bpy.context, mesh)
    
    obj = bpy.context.active_object
    obj.name = self.name
    obj.location = Vector(location)

    if not group in bpy.data.groups: bpy.ops.group.create(name=group)
    bpy.ops.object.group_link(group=group)

    return(obj)
    
  def renderYMesh1D(self, location=None, group='meshes'):
    import bpy
    import bmesh
    from mathutils import Vector
    from bpy_extras import object_utils #Blender 2.63
        
    if location is None:
      location = self.getGlobalLocation()
    
    coords = self.getLocalCoordinates()
    mesh = bpy.data.meshes.new(self.name)
    bm = bmesh.new()
    for (idx, y) in enumerate(coords):
      if 0 < idx and idx < len(coords)-1:
        h = 0.5
      else:
        h = 1
      bm.verts.new([0, y, 0])
      bm.verts.new([h, y, 0])
      bm.verts.new([0, y, h])
      bm.edges.new([bm.verts[3*idx], bm.verts[3*idx+1]])
      bm.edges.new([bm.verts[3*idx], bm.verts[3*idx+2]])
    bm.to_mesh(mesh)
    mesh.update()
    object_utils.object_data_add(bpy.context, mesh)
    
    obj = bpy.context.active_object
    obj.name = self.name
    obj.location = Vector(location)

    if not group in bpy.data.groups: bpy.ops.group.create(name=group)
    bpy.ops.object.group_link(group=group)

    return(obj)
    
  def renderZMesh1D(self, location=None, group='meshes'):
    import bpy
    import bmesh
    from mathutils import Vector
    from bpy_extras import object_utils #Blender 2.63
        
    if location is None:
      location = self.getGlobalLocation()
    
    coords = self.getLocalCoordinates()
    mesh = bpy.data.meshes.new(self.name)
    bm = bmesh.new()
    for (idx, z) in enumerate(coords):
      if 0 < idx and idx < len(coords)-1:
        h = 0.5
      else:
        h = 1
      bm.verts.new([0, 0, z])
      bm.verts.new([h, 0, z])
      bm.verts.new([0, h, z])
      bm.edges.new([bm.verts[3*idx], bm.verts[3*idx+1]])
      bm.edges.new([bm.verts[3*idx], bm.verts[3*idx+2]])
    bm.to_mesh(mesh)
    mesh.update()
    object_utils.object_data_add(bpy.context, mesh)
    
    obj = bpy.context.active_object
    obj.name = self.name
    obj.location = Vector(location)

    if not group in bpy.data.groups: bpy.ops.group.create(name=group)
    bpy.ops.object.group_link(group=group)

    return(obj)
    
class HomogeneousMeshParameters1D(HomogeneousMesh1D):
  '''
  A subclass of *HomogeneousMesh1D*, but for which the *MultiMesh1D::getLocalCoordinates()* function will take *spacing_max* into account to merge multiple *HomogeneousMeshParameters1D* in a smart way.
  '''
  pass

def linspaces(part_limits, Ncells_per_part):
  '''
  Return evenly spaced numbers over specified intervals.
  
  Example::
  
    >>> linspaces([0,1,2,3,4], [2,3,4,5])
    [0.0, 0.5, # 2 cells on [0,1]
    1.0, 1.3333333333333333, 1.6666666666666665, # 3 cells on [1,2]
    2.0, 2.25, 2.5, 2.75, # 4 cells on [2,3]
    3.0, 3.2000000000000002, 3.3999999999999999, 3.6000000000000001, 3.7999999999999998, # 5 cells on [3,4]
    4.0]
  
  '''
  # part_limits: length N+1
  # Ncells_per_part: length N
  mesh_position_list = []
  first = True
  for (idx, Ncells) in enumerate(Ncells_per_part):
    if part_limits[idx] < part_limits[idx+1]:
      foo = linspace(part_limits[idx], part_limits[idx+1], Ncells+1)
      if first:
        mesh_position_list.extend(foo)
        first = False
      else:
        mesh_position_list.extend(foo[1:])
  return mesh_position_list

def subGridMultiLayer(Section_MaxDeltaVector_in = [1.76, 2.1385, 2.3535, 1], Section_ThicknessVector_in = [1, 0.5, 1, 1]):
  ''' Create a list of thicknesses for meshing
  
  Usage::
  
    [Mesh_ThicknessVector, Section_FinalDeltaVector] = subGridMultiLayer(Section_MaxDeltaVector_in, Section_ThicknessVector_in)
  
  :param Section_ThicknessVector_in: list of the thickness of each section
  :param Section_MaxDeltaVector_in: list of maximum allowed deltas in each section
  
  :return: [Mesh_ThicknessVector, Section_FinalDeltaVector] where:
    * Mesh_ThicknessVector = thickness vector of the mesh
    * Section_FinalDeltaVector = list of final deltas used in the mesh
  
  Example::
  
    subGridMultiLayer([0.4,0.6,1], [2,3,5])
    
  This would return::
  
    Mesh_ThicknessVector = [ 0.4,  0.4,  0.4,  0.4,  0.4,
                             0.6,  0.6,  0.6,  0.6,  0.6,
                             1. , 1. ,  1. ,  1. ,  1. ]
    Section_FinalDeltaVector = [ 0.4,  0.6,  1. ]
  
  .. note:: If you are switching from the old to the new subGridMultiLayer version, replace the arguments as follows:
  
    * Section_MaxDeltaVector(new) = lambda(old)/16./indexVector(old)
    * Section_ThicknessVector(new) = thicknessVector(old)

  .. todo:: Make it work with Section_MaxDelta = numpy.inf as well.

  '''
  
  # check lengths
  if len(Section_ThicknessVector_in)!=len(Section_MaxDeltaVector_in):
    raise Exception('FATAL ERROR: len(Section_ThicknessVector_in)!=len(Section_MaxDeltaVector_in)\n')
    
  #if 0 in Section_ThicknessVector_in:
    #print('WARNING: Section_ThicknessVector_in contains zeroes')
  
  Section_ThicknessVector = []
  Section_MaxDeltaVector = []
  for i in range(len(Section_ThicknessVector_in)):
    if Section_ThicknessVector_in[i]!=0:
      Section_ThicknessVector.append(Section_ThicknessVector_in[i])
      Section_MaxDeltaVector.append(Section_MaxDeltaVector_in[i])
      
  # check for zeroes
  if 0 in Section_MaxDeltaVector:
    print(('FATAL ERROR: Section_MaxDeltaVector contains zeroes : '+str(Section_MaxDeltaVector)))
    sys.exit(-1)
  
  Section_MaxDeltaVector = numpy.array(Section_MaxDeltaVector)
  Section_ThicknessVector = numpy.array(Section_ThicknessVector)
  
  if len(Section_MaxDeltaVector) != len(Section_ThicknessVector) :
    raise Exception('FATAL ERROR: The 2 input vectors do not have the same size.')

  if min(Section_MaxDeltaVector)<0:
    raise Exception('FATAL ERROR: Section_MaxDeltaVector contains negative values: '+str(Section_MaxDeltaVector))

  if min(Section_ThicknessVector)<0:
    raise Exception('FATAL ERROR: Section_ThicknessVector contains negative values: '+str(Section_ThicknessVector))

  totalHeight = sum(Section_ThicknessVector);

  nLayers = len(Section_ThicknessVector);

  nCellsV = numpy.ceil( Section_ThicknessVector.astype(float) / Section_MaxDeltaVector.astype(float) )
  #print('nCellsV')
  #print(nCellsV)
  #sys.exit(-1)
  for i in range(len(nCellsV)):
    if nCellsV[i]==0:
      nCellsV[i]=1
    
  Section_FinalDeltaVector = Section_ThicknessVector.astype(float) / nCellsV.astype(float)

  Mesh_ThicknessVector = [];
  for m in range(nLayers):
    Mesh_ThicknessVector = numpy.concatenate( ( Mesh_ThicknessVector, Section_FinalDeltaVector[m]*numpy.ones(int(nCellsV[m])) ) )

  return(Mesh_ThicknessVector, Section_FinalDeltaVector)

def mergeMeshingParameters(MeshParamsList, minimum_mesh_delta = 1e-3):
  '''
  Returns a mesh based on a list of *MeshParams* objects.
  
  Original plan:
  
  * Return parameters that can be used for meshing with subGridMultiLayer.
  * Use in calculateMeshingParameters() function.
  '''

  #print(('MeshParamsList', MeshParamsList))

  N = len(MeshParamsList)
  
  # Xvec is an array of size (N,2) containing a list of (lower,upper) pairs corresponding to the meshing subdomains defined by the various geometrical objects.
  # epsX is an array of size (N,1) containing a list of epsilon values corresponding to the meshing subdomains defined by the various geometrical objects.
  # The (lower,upper) pairs from Xvec are associated with the corresponding epsilon values from epsX to determine an appropriate mesh in the X direction.
  Xvec = numpy.zeros([N,2])
  epsX = numpy.zeros([N,1])

  for mesh_params_idx in range(N):
    mesh_params = MeshParamsList[mesh_params_idx]
    Xvec[mesh_params_idx,0] = mesh_params.pos_min + mesh_params.getGlobalLocation()
    Xvec[mesh_params_idx,1] = mesh_params.pos_max + mesh_params.getGlobalLocation()
    epsX[mesh_params_idx,0] = mesh_params.getSpacingMax()
  
  VX = numpy.unique(numpy.sort(numpy.vstack([Xvec[:,0],Xvec[:,1]])))
  MX = numpy.inf*numpy.ones((Xvec.shape[0],len(VX))) # We fill with numpy.inf so that when we take the min(), those values get discarded.

  # Fill MX so that each line is filled with the eps for that line, but only in the ranges where it should apply.
  for m in range(Xvec.shape[0]):
    indmin = numpy.nonzero(VX==Xvec[m,0])[0][0] # index in VX of Xvec[m,0] (=pos_min)
    indmaX = numpy.nonzero(VX==Xvec[m,1])[0][0] # index in VX of Xvec[m,1] (=pos_max)
    MX[m,indmin:indmaX] = epsX[m,0]

  #print(('VX',VX))
  #print(('MX',MX))

  #VX, MX = nukeMesh(VX, MX, nuke_lower, nuke_upper)

  # Compute thickness vector from position vector
  thicknessVX = numpy.diff(VX)
    
  # epsVX = MX minus the last column
  epsVX = MX[:,0:MX.shape[1]-1]
  #print(('epsVX', epsVX))

  epsVX = epsVX.min(0) # different from current implementation in bfdtd_parser automesher!
  
  #print(('epsVX', epsVX))
  
  maxPermittivityVector_X = []
  thicknessVector_X = []
  
  # TODO: use (thickness, epsilon) tuples so that filter() and similar functions can be used. Also prevents errors if lists have different lengths.
  # ex: t = filter(lambda x: x>=1, t)
  # filter out parts smaller than minimum_mesh_delta_vector3[i]
  # NOTE: This might lead to errors because we never make up for the eliminated layers.
  # TODO: Fix by merging close lines instead of simply ignoring the corresponding layers.
  offset = 0
  for idx in range(len(thicknessVX)):
    if thicknessVX[idx] >= minimum_mesh_delta:
      maxPermittivityVector_X.append(epsVX[idx])
      thicknessVector_X.append(thicknessVX[idx] +  offset)
      offset = 0
    else:
      offset += thicknessVX[idx]
      #raise Exception('TODO: Handle this case properly.')
  
  ## TODO: Do the smoothing here.
  #spacing_max_new = []
  #thickness_new = []
  #maximum_mesh_delta_ratio = 2
  #for idx in range(len(maxPermittivityVector_X)):
    #delta_current = maxPermittivityVector_X[idx]
    #left_ok = True
    #right_ok = True
    
    #if idx-1 > 0:
      #if delta_current > maximum_mesh_delta_ratio*maxPermittivityVector_X[idx-1]:
        #left_ok = False
    #if idx+1 < len(maxPermittivityVector_X):
      #if delta_current > maximum_mesh_delta_ratio*maxPermittivityVector_X[idx+1]:
        #right_ok = False
        
    #if left_ok and right_ok:
      #spacing_max_new.append(maxPermittivityVector_X[idx])
      #thickness_new.append(thicknessVector_X[idx])
    #else:
      #pass # TODO: finish this
      
  #print(maxPermittivityVector_X, thicknessVector_X)
  #print(spacing_max_new, thickness_new)
  
  delta_X_vector, local_delta_X_vector = subGridMultiLayer(maxPermittivityVector_X, thicknessVector_X)

  mesh = numpy.cumsum(numpy.hstack((VX[0],delta_X_vector)))
  
  return mesh

def checkMesh(mesh, minimum_mesh_delta, maximum_mesh_delta_ratio):
  # validate the mesh (min cell size, max cell size and smoothness)
  # TODO: later
  
  minimum_mesh_delta_in_mesh = numpy.inf
  minimum_mesh_delta_in_mesh_idx = None
  maximum_mesh_delta_ratio_in_mesh = 0
  maximum_mesh_delta_ratio_in_mesh_idx = None
  
  thickness_list = numpy.diff(mesh)
  for (idx, thickness) in enumerate(thickness_list):
    if thickness < minimum_mesh_delta_in_mesh:
      minimum_mesh_delta_in_mesh = thickness
      minimum_mesh_delta_in_mesh_idx = idx
    if minimum_mesh_delta and thickness < minimum_mesh_delta:
      raise Exception('at idx={} mesh[idx]={}: (thickness={}) < (minimum_mesh_delta={})'.format(idx, mesh[idx], thickness, minimum_mesh_delta))
    if idx+1 < len(thickness_list):
      t0 = thickness_list[idx]
      t1 = thickness_list[idx+1]
      local_ratio = max(t0,t1)/min(t0,t1)
      if local_ratio > maximum_mesh_delta_ratio_in_mesh:
        maximum_mesh_delta_ratio_in_mesh = local_ratio
        maximum_mesh_delta_ratio_in_mesh_idx = idx
      if maximum_mesh_delta_ratio and local_ratio > maximum_mesh_delta_ratio:
        raise Exception('at idx={} mesh[idx]={}: (max(t0,t1)={}/min(t0,t1)={}) = {} > maximum_mesh_delta_ratio={}'.format(idx, mesh[idx], max(t0,t1), min(t0,t1), local_ratio, maximum_mesh_delta_ratio))
  
  return (minimum_mesh_delta_in_mesh, maximum_mesh_delta_ratio_in_mesh, minimum_mesh_delta_in_mesh_idx, maximum_mesh_delta_ratio_in_mesh_idx)

def truncateMeshList(mesh_list, lower, upper):
  ''' remove all submeshes where pos_min or pos_max are outside of [lower, upper] '''
  
  #default return value
  new_mesh_list = []
  
  #print('lower={} upper={}'.format(lower, upper))
  for mesh in mesh_list:
    #print('mesh.pos_min={} mesh.pos_max={}'.format(mesh.pos_min, mesh.pos_max))
    if lower <= mesh.pos_min <= upper and lower <= mesh.pos_max <= upper:
      #print('OK')
      new_mesh_list.append(mesh)

  return new_mesh_list

def increaseResolution(mesh_orig, N):
  '''
  Increase the resolution of a mesh by dividing each cell into N equal cells.
  This means that a mesh with C cells and P = C+1 points will turn into a mesh with C' = N*C cells and P' = N*C+1 = P+(P-1)*(N-1) = P*N-(N-1) points.
  '''
  return linspaces(mesh_orig, N*numpy.ones(len(mesh_orig)-1))
  #P = len(mesh_orig)
  #C = P-1
  #Pp = N*C+1
  #mesh_new = numpy.zeros(Pp)
  #for idx in range(P-1):
    #mesh_new[N*idx] = mesh_orig[idx]
    
  #return mesh_new

class test_Meshing(unittest.TestCase):
  
  def setUp(self):
    import warnings
    warnings.simplefilter("error")

  def test_printing(self):
    ''' test and example of the meshing system '''
    
    param = HomogeneousMeshParameters1D()
    print(param.PrintSelf('fdsjhfsdjkh --->'))
    
    # basic printing tests
    obj = Mesh3D()
    print(obj)
    hetero = HeterogeneousMesh1D()
    print(hetero)
    hetero = HeterogeneousMesh1D([1,2,3,4])
    print(hetero)
    homo = HomogeneousMesh1D()
    print(homo)
    homo = HomogeneousMesh1D(12)
    print(homo)
    homo = HomogeneousMesh1D(12, 245)
    print(homo)
    homo = HomogeneousMesh1D(12, 245, 20)
    print(homo)
    param = HomogeneousMeshParameters1D()
    print(param)
    param = HomogeneousMeshParameters1D(12)
    print(param)
    param = HomogeneousMeshParameters1D(12, 245)
    print(param)
    param = HomogeneousMeshParameters1D(12, 245, 20)
    print(param)
    multi = MultiMesh1D()
    print(multi)
    
    print('=== PART 1 =======')
    obj.xmesh.mesh_list = [homo, hetero, multi]
    print(obj)
    print('==========')
    #c = obj.getLocalXCoordinates() # Currently broken. Do we need it?
    c = obj.getGlobalXCoordinates()
    print(c)
    print('==========')

    print('=== PART 2 =======')
    obj.xmesh.mesh_list = [homo, hetero, multi, param]
    print(obj)
    #print('==========')
    #print(obj.PrintSelf(5*'^'))
    print('=== get =======')
    c = obj.getGlobalXCoordinates()
    print('=== print =======')
    print(c)
    print('==========')
    
    #print(param.PrintSelf('hello =>'))
    
    return

  def test_linspaces(self):
    print()
    part_limits = [0,1,2,3,4]
    Ncells_per_part = [2,3,4,5]
    mesh_position_list = linspaces(part_limits, Ncells_per_part)
    
    print(('part_limits', part_limits))
    print(('Ncells_per_part', Ncells_per_part))
    print(('mesh_position_list', mesh_position_list))

  def test_subGridMultiLayer(self):
    Mesh_ThicknessVector, Section_FinalDeltaVector = subGridMultiLayer([1,2,3,4,5],[5,4,3,2,1])
    print(('Mesh_ThicknessVector = '+str(Mesh_ThicknessVector)))
    print(('Section_FinalDeltaVector = '+str(Section_FinalDeltaVector)))
    return

  def test_mergeMeshingParameters(self):
    MeshParamsList = []

    mesh = HomogeneousMeshParameters1D()
    mesh.setExtension(0, 4)
    mesh.setSpacingMax(0.25)
    MeshParamsList.append(mesh)

    mesh = HomogeneousMeshParameters1D()
    mesh.setExtension(0.5, 1.5)
    mesh.setSpacingMax(0.20)
    MeshParamsList.append(mesh)

    mesh = HomogeneousMeshParameters1D()
    mesh.setExtension(3.25, 4.25)
    mesh.setSpacingMax(0.10)
    MeshParamsList.append(mesh)

    mesh = HomogeneousMeshParameters1D()
    mesh.setExtension(2, 3.25)
    mesh.setSpacingMax(0.15)
    MeshParamsList.append(mesh)

    mesh = HomogeneousMeshParameters1D()
    mesh.setExtension(-10, 10)
    mesh.setSpacingMax(1)
    MeshParamsList.append(mesh)

    mesh = HomogeneousMeshParameters1D()
    mesh.setExtension(-5, -1)
    mesh.setSpacingMax(numpy.inf)
    MeshParamsList.append(mesh)

    mesh = HomogeneousMeshParameters1D()
    mesh.setExtension(0, 2)
    mesh.setSpacingMax(numpy.inf)
    MeshParamsList.append(mesh)

    mesh = HomogeneousMeshParameters1D()
    mesh.setExtension(100, 200)
    mesh.setSpacingMax(numpy.inf)
    MeshParamsList.append(mesh)

    merged = mergeMeshingParameters(MeshParamsList)

    for idx in range(len(MeshParamsList)):
      print('== mesh %d =='%idx)
      print(MeshParamsList[idx])

    print('== merged ==')
    print(merged)
    return

  def test_parenting(self):
    
    grandpa = Mesh3D()
    grandpa.name = 'grandpa'
    grandpa.location = -99
    grandpa.xmesh.mesh_list = []
    grandpa.ymesh.mesh_list = []
    grandpa.zmesh.mesh_list = []
    
    papa = HeterogeneousMesh1D([0,5,6,7,8])
    papa.name = 'papa'
    papa.location = -9
    
    child = HeterogeneousMesh1D([0,1,2,3,4])
    child.name = 'child'
    child.parent = papa
    child.location = 42

    subchild = HeterogeneousMesh1D([0,12,-2,-43,-84])
    subchild.name = 'subchild'
    subchild.parent = child
    subchild.location = 18

    print('=====')
    print(papa)
    print('local: {}'.format(papa.getLocalCoordinates()))
    print('global: {}'.format(papa.getGlobalCoordinates()))

    print('=====')
    print(child)
    print('local: {}'.format(child.getLocalCoordinates()))
    print('global: {}'.format(child.getGlobalCoordinates()))

    print('=====')
    print(subchild)
    print('local: {}'.format(subchild.getLocalCoordinates()))
    print('global: {}'.format(subchild.getGlobalCoordinates()))
    
    return

  def test_MeshPostprocessing(self):
    
    mesh1 = HomogeneousMeshParameters1D(0, 1)
    mesh1.setSpacingMax(0.1)
    mesh2 = HomogeneousMeshParameters1D(1, 2)
    mesh2.setSpacingMax(0.3)
    mesh3 = HomogeneousMeshParameters1D(2, 3)
    mesh3.setSpacingMax(0.1)
    
    multi = MultiMesh1D()
    #multi.maximum_mesh_delta_ratio = None
    multi.mesh_list.append(mesh1)
    multi.mesh_list.append(mesh2)
    multi.mesh_list.append(mesh3)
    
    print(multi.getGlobalCoordinates())
    
    return

  def test_nuke(self):
    #.nukeothers
    return

if __name__ == '__main__':
  unittest.main()
