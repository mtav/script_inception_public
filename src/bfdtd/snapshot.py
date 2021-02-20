#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This module defines the basic snapshots and some additional snapshot objects for convenience.

.. digraph:: snapshot_system_diagram

    "Snapshot" -> "FrequencySnapshot"
    "Snapshot" -> "TimeSnapshot"
    
    "FrequencySnapshot" -> "EnergySnapshot"
    "EnergySnapshot" -> "ModeVolumeBox"
    "ModeVolumeBox" -> "ModeVolumeBoxFull"

    "TimeSnapshot" -> "ModeFilteredProbe"
    "TimeSnapshot" -> "EpsilonSnapshot"
    
    "EpsilonSnapshot" -> "EpsilonBox"
    "EpsilonBox" -> "EpsilonBoxFull"

    "SnapshotBox" -> "SnapshotBoxXYZ"
    "SnapshotBox" -> "SnapshotBoxSurface"
    "SnapshotBox" -> "SnapshotBoxVolume"

Deprecated notes. To be updated at some point.:

  * IDEA:

    * main bfdtd class writer calls snap.write(file, mesh)
    * main snap class defines mainwrite(file, mesh, subwrite) (which writes one or multiple snap entries to file)
    * sub snap classes (freq,time,etc) define subwrite() (which just writes single snap entry to file)
    * sub snap classes define write(file, mesh) which calls mainwrite(file, mesh, subwrite)

  * NOTES:

    * When P1,P2 do not form a plane, a single snapshot is created at X1 if plane=1, Y1 if plane=2, Z1 if plane=3, i.e. P1 is used for positioning the slice.
    * When coordinates in P1 or P2 do not correspond to a mesh point, they are snapped to the closest one.
    * When X1>X2 or similar: Behaviour unknown!!! 

  * Writing methods:

    * single plane if (P1,P2) form a plane.
    * 6 planes, one on each side if (P1,P2) form a box.
    * N planes in X, Y or Z based on mesh if (P1,P2) form a box.
    * 3 planes (X,Y,Z) intersecting at (P1+P2)/2.

  * The main writing function should be the same for all snapshots and call the specific writing functions depending on an attribute defining which one is desired.

  * The specific writing functions of the base class should be overridden in the child classes.

.. todo:: Check snapshot behaviour when X1>X2 or similar.
.. todo:: add IDs and sub-IDs and maybe some new brackets in the generated .inp/.geo files to be able to group snapshots for post-processing (mode volume in particular). Extend comment syntax.
.. todo:: update doc
.. todo:: add name extensions again (X+,X-, etc)
.. todo:: indent entries? Put 3D vectors on a single line?
.. todo:: Figure out why "make html" for the doc crashes on TimeSnapshot import. "make clean html" works. Could be due to "import bfdtd.bfdtd_parser" in here (recursive import?).
.. todo:: add print functions

.. todo:: Add unit tests...
'''

import os
import csv
import sys
import code
import copy
import numpy
import unittest
import tempfile

from numpy import array

import photonics.utilities.common
from photonics.utilities.common import fixLowerUpper, planeNumberName, float_array, findNearest, findNearestInSortedArray
from photonics.constants.physcon import get_c0
from photonics.utilities.brisFDTD_ID_info import numID_to_alphaID_TimeSnapshot, numID_to_alphaID_FrequencySnapshot, numID_to_alphaID_ModeFilteredProbe

from photonics.bfdtd.meshobject import MeshObject

#from .BFDTDobject import *
#from bfdtd.BFDTDobject import BFDTDobject

class Snapshot(object):
  '''
  Simple base class for all single-entry BFDTD snapshots.

  Attributes:
  
    * first: integer
    * repetition: integer
    * plane: integer
    * P1: 3D vector
    * P2: 3D vector
    * E: 3D vector
    * H: 3D vector
    * J: 3D vector
  
  .. note:: Plane snapshots will never output data for the upper edges of the simulation box.
  
            Example: Box from (0,0,0) to (1,1,1) with Z snapshot from (0,0) to (1,1) -> Snapshot output will not contain any points along the x=1 and y=1 lines.
            
            A Z snapshot at z=1 will however still output data!
  
  .. todo:: Add pictures and examples to this doc.
  
  .. todo:: Finish this... New problem: frequency snapshots with a frequency list. Solution: custom write function, which calls mainclass write for each frequency, which itself calls fsnap class write_entry function?
  .. todo:: Location + relative P1/P2 system like for blocks? Might make creating an aditional base class worth it?
  '''
  def __init__(self):
    ''' Constructor '''
    # define attributes and set default values

    # attributes common to most BFDTD objects
    # These variables might go into a main "bfdtd item" class used by geometry and measurement objects later on.
    # if self.name is None, the name is adapted based on the plane orientation (an additional comment item about the orientation might be added later)
    self.name = self.__class__.__name__
    self.layer = self.__class__.__name__
    self.group = self.__class__.__name__

    self.useForMeshing = True # set to False to disable use of this object during automeshing

    # main "measurement" properties
    self.first = 1 # crashes if = 0
    #self.repetition = 524200
    self.repetition = 500000
    self.E = [1,1,1]
    self.H = [1,1,1]
    self.J = [0,0,0]

    # main "geometric" properties
    self._plane = 'x' #1,2,3 for x,y,z
    # P1,P2 are internal variables (not to be used directly by the user) and could be replaced by size/centre or lower/upper in the future
    self.P1 = [0,0,0]
    self.P2 = [0,1,1]
    #self.snapshot_type = 'plane' # can be 'plane', 'box_surface' or 'box_volume'
    self.full_extension_bool = True # determines whether the snapshot should fully extend across the mesh or be limited to the specified P1,P2 points
    return

  def getTypeBasedOnAttributes(self):
    '''Returns class by default, but overloaded in the TimeSnapshot class to differentiate time and epsilon snapshots.'''
    return self.__class__

  def setStartingSample(self, starting_sample):
    '''
    dummy function, to be re-implemented in subclasses, such as FrequencySnapshot
    .. todo:: Why not just give it to all? no need for FrequencySnapshot defining it then...
    '''
    pass
    
  def setFullExtensionOn(self):
    self.full_extension_bool = True
    return

  def setFullExtensionOff(self):
    self.full_extension_bool = False
    return

  def setFromSnapshot(self, snapshot_in):
    '''
    Copies the properties from *snapshot_in*.

    .. todo:: Use loops over object dirs? Look for existing function in python? Should remove need for additional functions in subclasses.
    '''
    self.name = snapshot_in.name
    self.layer = snapshot_in.layer
    self.group = snapshot_in.group
    self.useForMeshing = snapshot_in.useForMeshing
    self.first = snapshot_in.first
    self.repetition = snapshot_in.repetition
    self.E = snapshot_in.E
    self.H = snapshot_in.H
    self.J = snapshot_in.J
    self.full_extension_bool = snapshot_in.full_extension_bool
    self.setExtensionFromSnapshot(snapshot_in)
    return

  def setExtensionFromSnapshot(self, snapshot_in):
    '''
    Copies the *P1*, *P2* and *plane* attributes from *snapshot_in*, i.e. the extension and the plane orientation.
    
    .. todo:: turn this into a constructor if possible.
    '''
    self.setExtension(*snapshot_in.getExtension())
    self.plane = snapshot_in.plane
    return

  @property
  def plane(self):
    """ orientation of the snapshot plane """
    return self._plane

  @plane.setter
  def plane(self, value):
    if not isinstance(value, str) or value.lower() not in ['x','y','z']:
      raise AttributeError("plane has to be 'x','y' or 'z'")
    self._plane = value.lower()

  def __str__(self):
    '''printing function'''
    ret = ''
    ret += 'name = ' + str(self.name) +'\n'
    ret += 'layer = ' + str(self.layer) +'\n'
    ret += 'group = ' + str(self.group) +'\n'
    ret += 'useForMeshing = ' + str(self.useForMeshing) +'\n'
    ret += 'first = ' + str(self.first) + '\n'
    ret += 'repetition = ' + str(self.repetition) + '\n'
    ret += 'plane = ' + str(self.plane) + '\n'
    ret += 'P1 = ' + str(self.P1) + '\n'
    ret += 'P2 = ' + str(self.P2) + '\n'    
    ret += 'E = ' + str(self.E) + '\n'
    ret += 'H = ' + str(self.H) + '\n'
    ret += 'J = ' + str(self.J)
    return ret

  def getName(self):
    return self.name
  
  def setName(self, name):
    self.name = name
  def setLayer(self, layer):
    self.layer = layer
  def setGroup(self, group):
    self.group = group
  def setUseForMeshing(self, useForMeshing):
    self.useForMeshing = useForMeshing

  def getFirst(self):
    return(self.first)

  def setFirst(self, first):
    self.first = first
    return(self.first)

  def getRepetition(self):
    return(self.repetition)
    
  def setRepetition(self, repetition):
    self.repetition = repetition
    return(self.repetition)
  
  def setEfield(self, E_vec3):
    self.E = list(E_vec3)
  def setHfield(self, H_vec3):
    self.H = list(H_vec3)
  def setJfield(self, J_vec3):
    self.J = list(J_vec3)

  def getEfield(self):
    return(list(self.E))
  def getHfield(self):
    return(list(self.H))
  def getJfield(self):
    return(list(self.J))

  def getPlaneBfdtdIndex(self):
    plane_letter = self.plane
    return [1,2,3][['x','y','z'].index(plane_letter.lower())]
  def setPlaneBfdtdIndex(self, bfdtd_index):
    self.plane = ['x','y','z'][bfdtd_index-1]
    return

  def getPlanePythonIndex(self):
    plane_letter = self.plane
    return ['x','y','z'].index(plane_letter.lower())
  def setPlanePythonIndex(self, python_index):
    self.plane = ['x','y','z'][python_index]
    return

  def getPlaneLetter(self):
    ''' return letter describing plane orientation ('x','y' or 'z') '''
    return self.plane
  def setPlaneLetter(self, plane_letter):
    ''' set plane orientation by passing 'x','y' or 'z' '''
    if plane_letter.lower() not in ['x', 'y', 'z']:
      raise Exception("plane_letter must be 'x','y' or 'z'")
    self.plane = plane_letter
    return

  def setPlaneOrientationX(self):
    self.plane = 'x'
  def setPlaneOrientationY(self):
    self.plane = 'y'
  def setPlaneOrientationZ(self):
    self.plane = 'z'
  
  def getCentro(self):
    return( 0.5*(array(self.P2) + array(self.P1)) )
    
  def getSize(self):
    return( array(self.P2) - array(self.P1) )
    
  def setCentro(self, centro_vec3):
    '''
    Reposition the snapshot so that ``(P1+P2)/2 = centro_vec3``, i.e. its centre is at *centro_vec3*.
    
    .. todo:: location or centre? centre is clearly defined, but location allows flexible positioning of the "origin of the object". But do we need that?
    '''
    size_vec3 = self.getSize()
    self.P1 = centro_vec3 - 0.5*size_vec3
    self.P2 = centro_vec3 + 0.5*size_vec3
        
  def setSize(self, size_vec3):
    '''
    Set the size of the snapshot, i.e. *[size_x, size_y, size_z] = P2 - P1*.
    
    :param size_vec3: A list or array of length 3, or a scalar int or float value. If a scalar *S* is passed, the size vector *[S, S, S]* will be used.
    '''
    if isinstance(size_vec3, (int, float)):
      size_vec3 = array([size_vec3, size_vec3, size_vec3])
    centro_vec3 = self.getCentro()
    self.P1 = centro_vec3 - 0.5*array(size_vec3)
    self.P2 = centro_vec3 + 0.5*array(size_vec3)
  
  def getLower(self):
    '''Returns the lower corner (P1).'''
    return array(self.P1)
  def getUpper(self):
    '''Returns the upper corner (P1).'''
    return array(self.P2)

  def getExtension(self):
    '''Returns the *extension*, i.e. *(lower, upper) = (P1,P2)*.'''
    self.P1, self.P2 = fixLowerUpper(self.P1, self.P2)
    return (array(self.P1), array(self.P2))

  def setExtension(self, lowerCorner_vec3, upperCorner_vec3):
    ''' Set the extension of the snapshot, i.e. its lower and upper corners.
    
    If you have an (L,U) tuple like the one you get from getExtension(), you can pass it directly via python's unpacking feature as follows::
    
      obj.setExtension(*sim.getExtension())
      
    .. todo:: Make above default behaviour? Support both?
    
    '''
    # if upperCorner is None and isinstance(f,tuple) and len()==2:
    #if lowerCorner_vec3 is None or upperCorner_vec3 is None:
      #self.P1 = lowerCorner_vec3
      #self.P2 = upperCorner_vec3
    #else:
    self.P1, self.P2 = fixLowerUpper(lowerCorner_vec3, upperCorner_vec3)
    self.P1 = numpy.array(self.P1)
    self.P2 = numpy.array(self.P2)
  
  def setExtensionX(self, x1, x2):
    self.P1[0] = min(x1, x2)
    self.P2[0] = max(x1, x2)
    return

  def setExtensionY(self, y1, y2):
    self.P1[1] = min(y1, y2)
    self.P2[1] = max(y1, y2)
    return

  def setExtensionZ(self, z1, z2):
    self.P1[2] = min(z1, z2)
    self.P2[2] = max(z1, z2)
    return
  
  def write_entry(self, FILE=sys.stdout, mesh=None):
    raise Exception('This function has to be implemented by child classes.')
    return

  def getMeshingParameters(self,xvec,yvec,zvec,epsx,epsy,epsz):
    objx = numpy.sort([self.P1[0],self.P2[0]])
    objy = numpy.sort([self.P1[1],self.P2[1]])
    objz = numpy.sort([self.P1[2],self.P2[2]])
    eps = 1
    xvec = numpy.vstack([xvec,objx])
    yvec = numpy.vstack([yvec,objy])
    zvec = numpy.vstack([zvec,objz])
    epsx = numpy.vstack([epsx,eps])
    epsy = numpy.vstack([epsy,eps])
    epsz = numpy.vstack([epsz,eps])
    return xvec,yvec,zvec,epsx,epsy,epsz

  def read_data(self, data3D, mesh=None, fsnap_numID=1, tsnap_numID=1, probe_ident='_id_', snap_time_number=0, dataPaths=['.'], testrun=False):
    '''
    .. todo:: Careful with dataPaths searching. Maybe add a warning + display full path. We don't want Matlab-like accidental random data loading...
    '''
    (filename_list, fsnap_numID_out, tsnap_numID_out) = self.getFileNames(fsnap_numID, tsnap_numID, probe_ident, snap_time_number)
    filename = filename_list[0]
    
    # locate file
    if not dataPaths:
      dataPaths = ['.']
    for p in dataPaths:
      filepath = os.path.join(p, filename)
      if os.path.exists(filepath):
        break
    
    print('{}.read_data fsnap_numID: {}->{} tsnap_numID = {}->{} filepath = {}'.format(self.__class__, fsnap_numID, fsnap_numID_out, tsnap_numID, tsnap_numID_out, filepath))
    
    if not os.path.exists(filepath):
      raise Exception('File not found: {}'.format(filepath))

    if testrun:
      return (data3D, fsnap_numID_out, tsnap_numID_out)

    # get fixed position
    plane_py_idx = self.getPlanePythonIndex()
    fixed_position = self.getCentro()[plane_py_idx]

    data2D = numpy.genfromtxt(filepath, names=True)
    header = data2D.dtype.names

    #print('header', header)
    #print('data2D', data2D)
    #print('data2D[material]', data2D['material'])

    #for k in header[2:]:
      #print(k)
    
    # read rows
    for row in data2D:
      if plane_py_idx == 0:
        x = fixed_position
        y = row['y']
        z = row['z']
      elif plane_py_idx == 1:
        x = row['x']
        y = fixed_position
        z = row['z']
      else:
        x = row['x']
        y = row['y']
        z = fixed_position
      #print(x, y, z, row['material'])
      (x_idx, y_idx, z_idx), (x_val, y_val, z_val) = mesh.getNearest([x,y,z])
      
      self.fillData(data3D, x_idx, y_idx, z_idx, header, row)
      
      #for k in header[2:]:
        #print(k)
        #print(row[k])
        #print(data3D[x_idx, y_idx, z_idx])
        #print(data3D[x_idx, y_idx, z_idx]['E'])
        #print(data3D[x_idx, y_idx, z_idx]['H'])
        #data3D[x_idx, y_idx, z_idx][k] = row[k]
      #data_epsilon[x_idx, y_idx, z_idx]['epsilon'] = row['material']
      #data_epsilon[x_idx, y_idx, z_idx] = row['material']
      
    return (data3D, fsnap_numID_out, tsnap_numID_out)

  def write_data(self, sampling_function, mesh=None, numID = 0, probe_ident = '_id_', snap_time_number = 0, destdir='.'):
    
    '''
    .. todo:: This function currently always assumes full snapshots. However, the snapshot area could be smaller, in which case, only part of the mesh should be looped through...
    .. todo:: Should be re-implemented by energy snapshots to increase processing speed by writing to two files at the same time.
    '''
    
    (filename_list, fsnap_numID, tsnap_numID) = self.getFileNames(numID, numID, probe_ident, snap_time_number)
    filename = filename_list[0]
    
    print('{}.write_data numID = {} filename = {}'.format(self.__class__, numID, filename))
    
    with open(os.path.join(destdir, filename), 'w', newline='') as csvfile:
      
      # set up csvwriter
      fieldnames = self.getOutputColumnHeaders()
      delimiter = ' '
      csvwriter = csv.DictWriter(csvfile, fieldnames, delimiter=delimiter)
      
      # write header
      csvfile.write('#')
      csvwriter.writeheader()
      
      # get fixed position
      plane_py_idx = self.getPlanePythonIndex()
      fixed_position = self.getCentro()[plane_py_idx]
      
      # write rows
      if plane_py_idx == 0:
        x = fixed_position
        for y in mesh.getYmesh():
          for z in mesh.getZmesh():
            self.write_data_row(csvwriter, sampling_function, x, y, z, 0)
          csvfile.write('\n')
          
      elif plane_py_idx == 1:
        y = fixed_position
        for x in mesh.getXmesh():
          for z in mesh.getZmesh():
            self.write_data_row(csvwriter, sampling_function, x, y, z, 0)
          csvfile.write('\n')
          
      else:
        z = fixed_position
        for x in mesh.getXmesh():
          for y in mesh.getYmesh():
            self.write_data_row(csvwriter, sampling_function, x, y, z, 0)
          csvfile.write('\n')
    
    return

class FrequencySnapshot(Snapshot):
  '''
  Simple base class for all single-entry BFDTD snapshots written as *FREQUENCY_SNAPSHOT* in .inp files.

  Attributes:
  
    * interpolate: 0 or 1
    * real_dft: 0 or 1
    * mod_only: 0 or 1
    * mod_all: 0 or 1
    * frequency_vector: float vector
    * starting_sample: integer

  The format of a frequency snapshot object is:
  
  * 1) first: iteration number for the first snapshot
  * 2) repetition: number of iterations between snapshots
  * 3) interpolate:
  
    * If set to 1 : the H field samples are interpolated to give the value at the plane of the E field nodes
    * If set to 2 : as above but the field values are multiplied by the area of the cell on the plane and interpolated
      to the centre of the square in the plane of the E field nodes..
    * If set to 3 : as above but the order of the field components in the output file is changed so that for the x,y
      and z planes the order is (yzx), (zxy) and (xyz) respectively instead of always being (xyz)
    * If set to 4 : as for 2 except that all 3 coordinates are given for each point
    
  * 4) real_dft: Set this if it is not required to write the imaginary component to file
  * 5) mod_only: Write only the modulus to file
  * 6) mod_all: Write the modulus AND the real and imaginary parts to file
  * 7) plane: 0=all, 1=x, 2=y, 3=z
  * 8-13) P1,P2: coordinates of the lower left and top right corners of the plane P1(x1,y1,z1), P2(x2,y2,z2)
  * 14) frequency_vector: frequency (in MHz! ). Will create a frequency snapshot for each frequency in the list/vector
  * 15) starting_sample: iteration number at which to start the running fourier transforms
  * 16-24) E,H,J: field components to be sampled E(Ex,Ey,Ez), H(Hx,Hy,Hz), J(Jx,Jy,Jz)

  The output file is of the same format as the snapshot “list format” and the naming is the same except that the time serial number starts at “00" instead of “aa”.

  Clarification on how *real_dft*, *mod_only* and *mod_all* work:
  
  * if mod_only or mod_all: output mod
  * if not(mod_only): output real part
  * if not(real_dft) and not(mod_only): output imaginary part

  Or in table form:

  ========  ========  =======  =========  ===========  ===========
  Inputs                       Output
  ---------------------------  -----------------------------------
  real_dft  mod_only  mod_all  \|field\|  real(field)  imag(field)
  ========  ========  =======  =========  ===========  ===========
  0         0         0        0          **1**        **1**
  0         0         **1**    **1**      **1**        **1**
  0         **1**     0        **1**      0            0    
  0         **1**     **1**    **1**      0            0    
  **1**     0         0        0          **1**        0    
  **1**     0         **1**    **1**      **1**        0    
  **1**     **1**     0        **1**      0            0    
  **1**     **1**     **1**    **1**      0            0    
  ========  ========  =======  =========  ===========  ===========
  
  .. note:: J output does not work at the moment. This is a Bristol FDTD related issue.

  .. todo:: Change frequency_vector to frequency_vector_Mhz?
  '''
  def __init__(self):
    ''' Constructor '''
    super().__init__()
    self.interpolate = 1
    self.real_dft = 0
    self.mod_only = 0
    self.mod_all = 1
    self.frequency_vector = [1]
    self.starting_sample = 0
    
    self.setFirst(self.getStartingSample() + self.getRepetition()) # crashes if = 0
    return

  def fillData(self, data3D, x_idx, y_idx, z_idx, header, row):
    # FrequencySnapshot data filling
    #print('FrequencySnapshot data filling')
    #for k in header[2:]:
      #print(k)
      #print(row[k])
      #print(data3D[x_idx, y_idx, z_idx])
      #print(data3D[x_idx, y_idx, z_idx]['E'])
      #print(data3D[x_idx, y_idx, z_idx]['H'])
      #data3D[x_idx, y_idx, z_idx][k] = row[k]
    #['Exmod', 'Exre', 'Exim', 'Eymod', 'Eyre', 'Eyim', 'Ezmod', 'Ezre', 'Ezim', 'Hxmod', 'Hxre', 'Hxim', 'Hymod', 'Hyre', 'Hyim', 'Hzmod', 'Hzre', 'Hzim']
    #-> E(vec3, complex), H(vec3, complex)
      
    #print(data3D[x_idx, y_idx, z_idx])
    #print(data3D[x_idx, y_idx, z_idx]['E'])
    #print(data3D[x_idx, y_idx, z_idx]['E'][0])
    #print(row[header.index('material')])
    if 'Exre' and 'Exim' in header: data3D[x_idx, y_idx, z_idx]['E'][0] = row[header.index('Exre')] + 1j*row[header.index('Exim')]
    if 'Eyre' and 'Eyim' in header: data3D[x_idx, y_idx, z_idx]['E'][1] = row[header.index('Eyre')] + 1j*row[header.index('Eyim')]
    if 'Ezre' and 'Ezim' in header: data3D[x_idx, y_idx, z_idx]['E'][2] = row[header.index('Ezre')] + 1j*row[header.index('Ezim')]

    if 'Hxre' and 'Hxim' in header: data3D[x_idx, y_idx, z_idx]['H'][0] = row[header.index('Hxre')] + 1j*row[header.index('Hxim')]
    if 'Hyre' and 'Hyim' in header: data3D[x_idx, y_idx, z_idx]['H'][1] = row[header.index('Hyre')] + 1j*row[header.index('Hyim')]
    if 'Hzre' and 'Hzim' in header: data3D[x_idx, y_idx, z_idx]['H'][2] = row[header.index('Hzre')] + 1j*row[header.index('Hzim')]

    #data_epsilon[x_idx, y_idx, z_idx]['epsilon'] = row['material']
    #data_epsilon[x_idx, y_idx, z_idx] = row['material']

    return

  def getFileNames(self, fsnap_numID = 1, tsnap_numID = 1, probe_ident = '_id_', snap_time_number = 0):
    (filename, alphaID, pair) = numID_to_alphaID_FrequencySnapshot(fsnap_numID, snap_plane = self.getPlaneLetter(), probe_ident = probe_ident, snap_time_number = snap_time_number)
    fsnap_numID += 1
    return ([filename], fsnap_numID, tsnap_numID)

  def getOutputColumnHeaders(self):
    column_headers = []
    plane = self.getPlaneLetter()
    if plane == 'x':
      column_headers.extend(['y', 'z'])
    elif plane == 'y':
      column_headers.extend(['x', 'z'])
    else:
      column_headers.extend(['x', 'y'])
    if self.E[0]:
      column_headers.extend(self.getOutputColumnHeadersSubFunction('Ex'))
    if self.E[1]:
      column_headers.extend(self.getOutputColumnHeadersSubFunction('Ey'))
    if self.E[2]:
      column_headers.extend(self.getOutputColumnHeadersSubFunction('Ez'))
    if self.H[0]:
      column_headers.extend(self.getOutputColumnHeadersSubFunction('Hx'))
    if self.H[1]:
      column_headers.extend(self.getOutputColumnHeadersSubFunction('Hy'))
    if self.H[2]:
      column_headers.extend(self.getOutputColumnHeadersSubFunction('Hz'))
    return(column_headers)

  def getOutputColumnHeadersSubFunction(self, field):
    column_headers = []
    if self.mod_only or self.mod_all:
      column_headers.append(field + 'mod')
    if not(self.mod_only):
      column_headers.append(field + 're')
    if not(self.real_dft) and not(self.mod_only):
      column_headers.append(field + 'im')
    return(column_headers)

  def getStartingSample(self):
    return self.starting_sample
    
  def setStartingSample(self, starting_sample):
    if starting_sample is not None:
      self.starting_sample = starting_sample
    return self.starting_sample

  def __str__(self):
    '''printing function'''
    ret = ''
    ret += super().__str__() + '\n'
    ret += 'interpolate = ' + str(self.interpolate) + '\n'
    ret += 'real_dft = ' + str(self.real_dft) + '\n'
    ret += 'mod_only = ' + str(self.mod_only) + '\n'
    ret += 'mod_all = ' + str(self.mod_all) + '\n'
    ret += 'frequency_vector = ' + str(self.frequency_vector) + '\n'
    ret += 'starting_sample = ' + str(self.starting_sample)
    return ret

  def setFromSnapshot(self, snapshot_in):
    '''
    Copies the properties from *snapshot_in*.
    
    .. todo:: Use loops over object dirs? Look for existing function in python?
    '''
    super().setFromSnapshot(snapshot_in)
    # We check for existing attributes to also enable copying from time/epsilon snapshots for example. Just checking for the type of *snapshot_in* might fail if classes change and is more limiting...
    if 'interpolate' in dir(snapshot_in): self.interpolate = snapshot_in.interpolate
    if 'real_dft' in dir(snapshot_in): self.real_dft = snapshot_in.real_dft
    if 'mod_only' in dir(snapshot_in): self.mod_only = snapshot_in.mod_only
    if 'mod_all' in dir(snapshot_in): self.mod_all = snapshot_in.mod_all
    if 'frequency_vector' in dir(snapshot_in): self.frequency_vector = snapshot_in.frequency_vector
    if 'starting_sample' in dir(snapshot_in): self.starting_sample = snapshot_in.starting_sample
    return

  def read_entry(self,entry):
    if entry.name:
      self.name = entry.name
    idx = 0
    self.first = int(float(entry.data[idx])); idx = idx+1
    self.repetition = int(float(entry.data[idx])); idx = idx+1
    self.interpolate = float(entry.data[idx]); idx = idx+1
    self.real_dft = float(entry.data[idx]); idx = idx+1
    self.mod_only = float(entry.data[idx]); idx = idx+1
    self.mod_all = float(entry.data[idx]); idx = idx+1
    self.setPlaneBfdtdIndex(int(float(entry.data[idx]))); idx = idx+1    
    self.P1 = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3
    self.P2 = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3
    self.frequency_vector = [float(entry.data[idx])]; idx = idx+1
    self.starting_sample = int(entry.data[idx]); idx = idx+1
    self.E = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3
    self.H = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3
    self.J = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3
    return(0)

  def write_entry(self, FILE=sys.stdout, mesh=None):
    '''.. todo:: mesh argument not used yet. Remove? Use explicit snap function instead? With snap by default if desired?'''

    #print('FrequencySnapshot.write_entry')

    #print(self)
    #print(FILE)
    #print(mesh)
    P1, P2 = self.getExtension()
    plane_ID = self.getPlaneBfdtdIndex()
    plane_name = self.getPlaneLetter()
  
    if mesh and self.full_extension_bool:
      S, N = mesh.getSizeAndResolution()
      centro = self.getCentro()
      if plane_name.lower() == 'x':
        P1 = [centro[0], 0, 0]
        P2 = [centro[0], S[1], S[2]]
      elif plane_name.lower() == 'y':
        P1 = [0, centro[1], 0]
        P2 = [S[0], centro[1], S[2]]
      else:
        P1 = [0, 0, centro[2]]
        P2 = [S[0], S[1], centro[2]]

    if self.getRepetition() <= 0:
      raise Exception('self.getRepetition() = {} <= 0'.format(self.getRepetition()))

    for idx, frequency in enumerate(self.frequency_vector):
      FILE.write('FREQUENCY_SNAPSHOT **name=' + self.name + '\n')
      FILE.write('{\n')
      FILE.write("%d **FIRST\n" % self.first)
      FILE.write("%d **REPETITION\n" % self.repetition)
      FILE.write("%d **interpolate?\n" % self.interpolate)
      FILE.write("%d **REAL DFT\n" % self.real_dft)
      FILE.write("%d **MOD ONLY\n" % self.mod_only)
      FILE.write("%d **MOD ALL\n" % self.mod_all)
      FILE.write("%d **PLANE %s\n" % (plane_ID, plane_name.upper()))
      FILE.write("%E **X1\n" % P1[0])
      FILE.write("%E **Y1\n" % P1[1])
      FILE.write("%E **Z1\n" % P1[2])
      FILE.write("%E **X2\n" % P2[0])
      FILE.write("%E **Y2\n" % P2[1])
      FILE.write("%E **Z2\n" % P2[2])
      FILE.write("{:.8E} **FREQUENCY (MHz if dimensions in mum) (c0/f = {:E})\n".format(frequency, get_c0()/frequency))
      FILE.write("%d **STARTING SAMPLE\n" % self.starting_sample)
      FILE.write("%d **EX\n" % self.E[0])
      FILE.write("%d **EY\n" % self.E[1])
      FILE.write("%d **EZ\n" % self.E[2])
      FILE.write("%d **HX\n" % self.H[0])
      FILE.write("%d **HY\n" % self.H[1])
      FILE.write("%d **HZ\n" % self.H[2])
      FILE.write("%d **JX\n" % self.J[0])
      FILE.write("%d **JY\n" % self.J[1])
      FILE.write("%d **JZ\n" % self.J[2])
      FILE.write('}\n')
      FILE.write('\n')
  
      #if self.P1[plane_ID-1] == self.P2[plane_ID-1]:
        #snapshot(self.name, plane_ID, self.P1, self.P2, self.frequency_vector[i])
      #else:
        #snapshot(self.name + ' X-', 1, [self.P1[0], self.P1[1], self.P1[2]], [self.P1[0], self.P2[1], self.P2[2]], self.frequency_vector[i])
        #snapshot(self.name + ' X+', 1, [self.P2[0], self.P1[1], self.P1[2]], [self.P2[0], self.P2[1], self.P2[2]], self.frequency_vector[i])
        #snapshot(self.name + ' Y-', 2, [self.P1[0], self.P1[1], self.P1[2]], [self.P2[0], self.P1[1], self.P2[2]], self.frequency_vector[i])
        #snapshot(self.name + ' Y+', 2, [self.P1[0], self.P2[1], self.P1[2]], [self.P2[0], self.P2[1], self.P2[2]], self.frequency_vector[i])
        #snapshot(self.name + ' Z-', 3, [self.P1[0], self.P1[1], self.P1[2]], [self.P2[0], self.P2[1], self.P1[2]], self.frequency_vector[i])
        #snapshot(self.name + ' Z+', 3, [self.P1[0], self.P1[1], self.P2[2]], [self.P2[0], self.P2[1], self.P2[2]], self.frequency_vector[i])

  def getLambda(self):
    '''
    Get the wavelength list.
    
    .. todo:: Rename to getWavelength()?
    '''
    return get_c0()/numpy.array(self.frequency_vector)
    
  def setWavelengths(self, wavelength_vector):
    if isinstance(wavelength_vector, (int, float)):
      wavelength_vector = [wavelength_vector]
    self.setFrequencies([get_c0()/L for L in wavelength_vector])
    return

  def getFrequencies(self):
    return(self.frequency_vector)

  def setFrequencies(self, frequency_vector):
    '''
    Set the frequencies of the frequency snapshot.
    
    .. todo:: setWavelength/Lambda functions? -> wavelength is clearer -> update all similar calls (ex: excitation)
    .. todo:: Support list and single item? Is that even good design? -> Probably not. Would be better to support multiple args and use arg unpacking. -> Make sure to update all other uses before doing this. Significant change.
    '''
    if frequency_vector:
      if isinstance(frequency_vector, (int, float)):
        self.frequency_vector = [frequency_vector]
      else:
        self.frequency_vector = frequency_vector
    return
  
  def write_data_row(self, csvwriter, sampling_function, x, y, z, t):

    (epsilon, E, H) = sampling_function(x, y, z, t)

    row_dict = dict()
    
    if 'x' in csvwriter.fieldnames: row_dict['x'] = x
    if 'y' in csvwriter.fieldnames: row_dict['y'] = y
    if 'z' in csvwriter.fieldnames: row_dict['z'] = z

    if 'Exmod' in csvwriter.fieldnames: row_dict['Exmod'] = abs(E[0])
    if 'Exre' in csvwriter.fieldnames: row_dict['Exre'] = E[0].real
    if 'Exim' in csvwriter.fieldnames: row_dict['Exim'] = E[0].imag
    if 'Eymod' in csvwriter.fieldnames: row_dict['Eymod'] = abs(E[1])
    if 'Eyre' in csvwriter.fieldnames: row_dict['Eyre'] = E[1].real
    if 'Eyim' in csvwriter.fieldnames: row_dict['Eyim'] = E[1].imag
    if 'Ezmod' in csvwriter.fieldnames: row_dict['Ezmod'] = abs(E[2])
    if 'Ezre' in csvwriter.fieldnames: row_dict['Ezre'] = E[2].real
    if 'Ezim' in csvwriter.fieldnames: row_dict['Ezim'] = E[2].imag

    if 'Hxmod' in csvwriter.fieldnames: row_dict['Hxmod'] = abs(H[0])
    if 'Hxre' in csvwriter.fieldnames: row_dict['Hxre'] = H[0].real
    if 'Hxim' in csvwriter.fieldnames: row_dict['Hxim'] = H[0].imag
    if 'Hymod' in csvwriter.fieldnames: row_dict['Hymod'] = abs(H[1])
    if 'Hyre' in csvwriter.fieldnames: row_dict['Hyre'] = H[1].real
    if 'Hyim' in csvwriter.fieldnames: row_dict['Hyim'] = H[1].imag
    if 'Hzmod' in csvwriter.fieldnames: row_dict['Hzmod'] = abs(H[2])
    if 'Hzre' in csvwriter.fieldnames: row_dict['Hzre'] = H[2].real
    if 'Hzim' in csvwriter.fieldnames: row_dict['Hzim'] = H[2].imag

    csvwriter.writerow(row_dict)

    return

class TimeSnapshot(Snapshot):
  '''
  Simple base class for all single-entry BFDTD snapshots written as *SNAPSHOT* in .inp files.
  
  Attributes:
  
    * power: 0 or 1
    * epsilon: 0 or 1

  One or more field components may be sampled over a specified plane in the structure after a specified number of iterations.
  It is possible to take snapshots after every “n” iterations by setting the “iterations between snapshots” parameter to “n”.
  
  For each snapshot requested a file is produced in one of two formats:
  
  * List format which has a filename of the form “x1idaa.prn”, where “x” is the plane over
    which the snapshot has been taken, “1"is the snapshot serial number. ie. the snaps are numbered in the order which
    they appear in the input file.. “id” in an identifier specified in the “flags” object. “aa" is the time serial number ie.
    if snapshots are asked for at every 100 iterations then the first one will have “aa, the second one “ab" etc
    The file consists of a single header line followed by columns of numbers, one for each field component wanted and
    two for the coordinates of the point which has been sampled. These files can be read into Gema.
  
  * Matrix format for each snapshot a file is produced for each requested field component with a name of the form
    “x1idaa_ex” where the “ex” is the field component being sampled. The rest of the filename is tha same as for the list
    format case. The file consists of a matrix of numbers the first column and first row or which, gives the position of
    the sample points in each direction. These files can be read into MathCad or to spreadsheet programs.
  
  The format of the snapshot object is as follows:
  
    * 1 : first: iteration number for the first snapshot
    * 2 : repetition: number of iterations between snapshots
    * 3 : plane: 1=x,2=y,3=z
    * 4-9 : P1, P2: coordinates of the lower left and top right corners of the plane P1(x1,y1,z1), P2(x2,y2,z2)
    * 10-18 : E, H, J: field components to be sampled E(Ex,Ey,Ez), H(Hx,Hy,Hz), J(Jx,Jy,Jz)
    * 19 : power: print power? =0/1
    * 20 : eps: create EPS (->epsilon->refractive index) snapshot? =0/1
    * 21 : ???: write an output file in “list” format (NOT IMPLEMENTED YET)(default is list format)
    * 22 : ???: write an output file in “matrix” format (NOT IMPLEMENTED YET)
  
  Mode filtered probe files (Requires a template for the first excitation object!):
  
    Mode filtered probe files are specified in the same way as a snapshot across the reference plane except that no field components are selected, i.e. E=H=J=power=eps=(0,0,0).
    In addition, the "repetition" parameter takes the role which the "step" parameter does on normal probes.
    
    The output will have the same form as a probe file and will consist of the inner product at each time step of the field distribution across the reference plane with the template specified for the first excitation object.
    This template will normally be the wanted mode of the guiding structure and, thus, the output of this probe will be the amplitude of just this mode.

    The effect of this is that the amplitude of the mode of interest is sampled across the whole waveguide cross-section.
    If a normal field probe had been used, then the unwanted effects of other modes would cause inaccuracies in the final result.

  .. note:: JX,JY,JZ output does not seem to work. (Bristol FDTD issue)
  
  The output columns are (assuming all columns were enabled):
  
    * For X planes::
            
        #y z Ex Ey Ez Hx Hy Hz Pow material 
      
    * For Y planes::
    
        #x z Ex Ey Ez Hx Hy Hz Pow material 
      
    * For Z planes::
    
        #x y Ex Ey Ez Hx Hy Hz Pow material 

  '''
  def __init__(self):
    ''' Constructor '''
    super(TimeSnapshot, self).__init__() # python 2+3 compatible super() call
    self.power = 0
    self.eps = 0
    return

  def __str__(self):
    '''printing function'''
    ret = ''
    ret += super().__str__() + '\n'
    ret += 'power = ' + str(self.power) + '\n'
    ret += 'eps = ' + str(self.eps)
    return ret

  def fillData(self, data3D, x_idx, y_idx, z_idx, header, row):
    # TimeSnapshot data filling
    #print('TimeSnapshot data filling')
    #for k in header[2:]:
      #print(k)
      #print(row[k])
      #print(data3D[x_idx, y_idx, z_idx])
      #print(data3D[x_idx, y_idx, z_idx]['E'])
      #print(data3D[x_idx, y_idx, z_idx]['H'])
      #data3D[x_idx, y_idx, z_idx][k] = row[k]
      #['Ex', 'Ey', 'Ez', 'Hx', 'Hy', 'Hz', 'Pow', 'material']
      #-> E(vec3, float), H(vec3, float), Pow(float), material(float)
      
    #print(data3D[x_idx, y_idx, z_idx])
    #print(data3D[x_idx, y_idx, z_idx]['E'])
    #print(data3D[x_idx, y_idx, z_idx]['E'][0])
    #print(row[header.index('material')])
    if 'Ex' in header: data3D[x_idx, y_idx, z_idx]['E'][0] = row[header.index('Ex')]
    if 'Ey' in header: data3D[x_idx, y_idx, z_idx]['E'][1] = row[header.index('Ey')]
    if 'Ez' in header: data3D[x_idx, y_idx, z_idx]['E'][2] = row[header.index('Ez')]
    if 'Hx' in header: data3D[x_idx, y_idx, z_idx]['H'][0] = row[header.index('Hx')]
    if 'Hy' in header: data3D[x_idx, y_idx, z_idx]['H'][1] = row[header.index('Hy')]
    if 'Hz' in header: data3D[x_idx, y_idx, z_idx]['H'][2] = row[header.index('Hz')]
    if 'Pow' in header: data3D[x_idx, y_idx, z_idx]['Pow'] = row[header.index('Pow')]
    if 'material' in header: data3D[x_idx, y_idx, z_idx]['material'] = row[header.index('material')]

    #data_epsilon[x_idx, y_idx, z_idx]['epsilon'] = row['material']
    #data_epsilon[x_idx, y_idx, z_idx] = row['material']

    return

  def getOutputColumnHeaders(self):

    if self.getTypeBasedOnAttributes() == ModeFilteredProbe:
      column_headers = ['Time', 'inner_product_e', 'inner_product_h', 'inner_product_poynting', 'sum', 'difference']
    else:
      column_headers = []
      
      plane = self.getPlaneLetter()
      if plane == 'x':
        column_headers.extend(['y', 'z'])
      elif plane == 'y':
        column_headers.extend(['x', 'z'])
      else:
        column_headers.extend(['x', 'y'])
      
      if self.E[0]:
        column_headers.append('Ex')
      if self.E[1]:
        column_headers.append('Ey')
      if self.E[2]:
        column_headers.append('Ez')
      
      if self.H[0]:
        column_headers.append('Hx')
      if self.H[1]:
        column_headers.append('Hy')
      if self.H[2]:
        column_headers.append('Hz')
      
      if self.getPower():
        column_headers.append('Pow')
      if self.getEpsilon():
        column_headers.append('material')
    
    return(column_headers)

  def getPower(self):
    return(self.power)

  def setPower(self, power):
    self.power = power
    return(self.power)
  
  def getEpsilon(self):
    return(self.eps)

  def setEpsilon(self, eps):
    self.eps = eps
    return(self.eps)

  def getTypeBasedOnAttributes(self):
    '''
    Returns the "type" of the snapshot based on the selected output columns (E, H, J, power and epsilon).
    
    * If all output columns are disabled: ModeFilteredProbe
    * If all output columns are disabled, except epsilon: EpsilonSnapshot
    * Else: TimeSnapshot

    Or in table form:

    ==========  ========  =======  =========  ===========  =================
    Attributes                                             Output
    -----------------------------------------------------  -----------------
    E           H         J        Power      Epsilon      Type
    ==========  ========  =======  =========  ===========  =================
    000         000       000      0          0            ModeFilteredProbe
    000         000       000      0          1            EpsilonSnapshot
    \*          \*        \*       \*         \*           TimeSnapshot
    ==========  ========  =======  =========  ===========  =================
    '''
    
    if (self.getEfield(), self.getHfield(), self.getJfield(), self.getPower()) == ([0,0,0], [0,0,0], [0,0,0], 0):
      if self.getEpsilon() == 0:
        return ModeFilteredProbe
      else:
        return EpsilonSnapshot
    else:
      return TimeSnapshot
    
    return

  def getFileNames(self, fsnap_numID = 1, tsnap_numID = 1, probe_ident = '_id_', snap_time_number = 0):
    if self.getTypeBasedOnAttributes() == ModeFilteredProbe:
      (filename, alphaID, pair) = numID_to_alphaID_ModeFilteredProbe(tsnap_numID, probe_ident = probe_ident, snap_time_number = snap_time_number)
    else:
      # Note the +1 in indexing for snap_time_number. BFDTD inconsistencies...
      (filename, alphaID, pair) = numID_to_alphaID_TimeSnapshot(tsnap_numID, snap_plane = self.getPlaneLetter(), probe_ident = probe_ident, snap_time_number = snap_time_number + 1)
    tsnap_numID += 1    
    return ([filename], fsnap_numID, tsnap_numID)

  def read_entry(self, entry):
    if entry.name:
      self.name = entry.name
    idx = 0
    self.first = int(float(entry.data[idx])); idx = idx+1
    self.repetition = int(float(entry.data[idx])); idx = idx+1
    self.setPlaneBfdtdIndex(int(float(entry.data[idx]))); idx = idx+1    
    self.P1 = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3
    self.P2 = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3
    self.E = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3
    self.H = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3
    self.J = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3
    self.power = float(entry.data[idx]); idx = idx+1
    if(len(entry.data)>idx): self.eps = int(float(entry.data[idx])); idx = idx+1
    return(0)

  def write_entry(self, FILE=sys.stdout, mesh=None):
    #print('TimeSnapshot.write_entry')
    
    P1, P2 = self.getExtension()
    plane_ID = self.getPlaneBfdtdIndex()
    plane_name = self.getPlaneLetter()
  
    if mesh and self.full_extension_bool:
      S, N = mesh.getSizeAndResolution()
      centro = self.getCentro()
      if plane_name.lower() == 'x':
        P1 = [centro[0], 0, 0]
        P2 = [centro[0], S[1], S[2]]
      elif plane_name.lower() == 'y':
        P1 = [0, centro[1], 0]
        P2 = [S[0], centro[1], S[2]]
      else:
        P1 = [0, 0, centro[2]]
        P2 = [S[0], S[1], centro[2]]
  
    FILE.write('SNAPSHOT **name=' + self.name + '\n')
    FILE.write('{\n')

    FILE.write("%d **FIRST\n" % self.first)
    FILE.write("%d **REPETITION\n" % self.repetition)
    FILE.write("{:d} **PLANE {}\n".format(plane_ID, plane_name.upper()))
    FILE.write("%E **X1\n" % P1[0])
    FILE.write("%E **Y1\n" % P1[1])
    FILE.write("%E **Z1\n" % P1[2])
    FILE.write("%E **X2\n" % P2[0])
    FILE.write("%E **Y2\n" % P2[1])
    FILE.write("%E **Z2\n" % P2[2])
    FILE.write("%d **EX\n" % self.E[0])
    FILE.write("%d **EY\n" % self.E[1])
    FILE.write("%d **EZ\n" % self.E[2])
    FILE.write("%d **HX\n" % self.H[0])
    FILE.write("%d **HY\n" % self.H[1])
    FILE.write("%d **HZ\n" % self.H[2])
    FILE.write("%d **JX\n" % self.J[0])
    FILE.write("%d **JY\n" % self.J[1])
    FILE.write("%d **JZ\n" % self.J[2])
    FILE.write("%d **POW\n" % self.power)
    FILE.write("%d **EPS\n" % self.eps)
    FILE.write('}\n')

    FILE.write('\n')
    
    return
  
    #if self.P1[plane_ID-1] == self.P2[plane_ID-1]:
      #snapshot(plane_ID, self.P1, self.P2, self.name)
      ##raise Exception('self.P1 = {}, self.P2 = {}, plane_ID={}, plane_name={}'.format(self.P1, self.P2, plane_ID, plane_name))
    #else:
      #snapshot(1, [self.P1[0], self.P1[1], self.P1[2]], [self.P1[0], self.P2[1], self.P2[2]], self.name + ' X-')
      #snapshot(1, [self.P2[0], self.P1[1], self.P1[2]], [self.P2[0], self.P2[1], self.P2[2]], self.name + ' X+')
      #snapshot(2, [self.P1[0], self.P1[1], self.P1[2]], [self.P2[0], self.P1[1], self.P2[2]], self.name + ' Y-')
      #snapshot(2, [self.P1[0], self.P2[1], self.P1[2]], [self.P2[0], self.P2[1], self.P2[2]], self.name + ' Y+')
      #snapshot(3, [self.P1[0], self.P1[1], self.P1[2]], [self.P2[0], self.P2[1], self.P1[2]], self.name + ' Z-')
      #snapshot(3, [self.P1[0], self.P1[1], self.P2[2]], [self.P2[0], self.P2[1], self.P2[2]], self.name + ' Z+')
  
  def write_data_row(self, csvwriter, sampling_function, x, y, z, t):
    '''
    .. todo:: Add support for power and ModeFilteredProbe columns.
    '''

    (epsilon, E, H) = sampling_function(x, y, z, t)

    row_dict = dict()
    
    if 'x' in csvwriter.fieldnames: row_dict['x'] = x
    if 'y' in csvwriter.fieldnames: row_dict['y'] = y
    if 'z' in csvwriter.fieldnames: row_dict['z'] = z

    if 'Ex' in csvwriter.fieldnames: row_dict['Ex'] = E[0]
    if 'Ey' in csvwriter.fieldnames: row_dict['Ey'] = E[1]
    if 'Ez' in csvwriter.fieldnames: row_dict['Ez'] = E[2]

    if 'Hx' in csvwriter.fieldnames: row_dict['Hx'] = H[0]
    if 'Hy' in csvwriter.fieldnames: row_dict['Hy'] = H[1]
    if 'Hz' in csvwriter.fieldnames: row_dict['Hz'] = H[2]

    if 'material' in csvwriter.fieldnames: row_dict['material'] = epsilon

    csvwriter.writerow(row_dict)

    return

class EpsilonSnapshot(TimeSnapshot):
  '''
  Child class of :py:class:`TimeSnapshot`, which disables all output columns except epsilon.

  .. todo:: Get rid of this class? It is possible to output E,H,J, power and eps with the same snapshot, i.e. an epsilon snapshot is not that special compared to a time snapshot... (apart from not changing in time)
  
  .. todo:: It might be possible to set the repetition to flag.iterations(+1?) on write instead of simply using a very large repetition number?
  '''
  def __init__(self):
    ''' Constructor '''
    super().__init__()
    self.setDefaults()
    return

  def setDefaults(self):
    '''
    Sets the following properties:
    
    * self.E = [0,0,0]
    * self.H = [0,0,0]
    * self.J = [0,0,0]
    * self.power = 0
    * self.eps = 1
    * self.first = 1
    * self.repetition = int(1e9)
    '''
    # to make it output epsilon only
    self.E = [0,0,0]
    self.H = [0,0,0]
    self.J = [0,0,0]
    self.power = 0
    self.eps = 1

    # to get a single snapshot directly at the start
    self.first = 1 # crashes if = 0
    self.repetition = int(1e9) # We just set this to an insanely high number by default in case the user forgets to set it. (TODO: Maybe something like -1 works. Check BFDTD manual.)
    return

  def setFromSnapshot(self, snapshot_in):
    '''
    Copies the properties from *snapshot_in*, but then calls :py:func:`EpsilonSnapshot.setDefaults`.
    '''
    super().setFromSnapshot(snapshot_in)
    self.setDefaults()
    return

class ModeFilteredProbe(TimeSnapshot):
  '''
  Child class of *TimeSnapshot*, which disables all output columns. This leads to a *mode filtered probe* behaviour.
  
  Unlike usual time and epsilon snapshots, the ModeFilteredProbe output filenames start with "i" instead of "x/y/z" and start with a 0 index instead of 1, i.e. the first ModeFilteredProbe output file will be "i1_id_00.prn" instead of "x1_id_01.prn".
  
  Requires a "template". The default template filename is "template.int".
  
  The output columns are always::

    #Time inner_product_e inner_product_h inner_product_poynting sum difference

  .. todo:: Understand and explain what is output into the files...
  .. todo:: Add template filename attribute...
  '''
  def __init__(self):
    ''' Constructor '''
    super().__init__()
    self.E = [0,0,0]
    self.H = [0,0,0]
    self.J = [0,0,0]
    self.power = 0
    self.eps = 0
    return

class SnapshotBox(object):
  '''A base class representing a snapshot box instead of a snapshot plane like the **Snapshot** class.
  
  It has one attribute:
    * baseSnapshot
  
  Its purpose is to be used by child classes implementing a **write_entry** function, which will write snapshot planes based on **baseSnapshot** in various ways.

  .. todo:: add name prefix? Or append to base snapshot name?
  .. todo:: At the moment, this class and its children do not have their own location/size/orientation info, taking it from the base snapshot instead.
            This means that one cannot do this::

              xyz=SnapshotBoxXYZ()
              xyz.setSize/LocationOrientation
              xyz.base=eps
              write
              xyz.base=fsnap
              write
              etc.

            Instead location/size/orientation have to be set for each base snapshot passed.
            Change system?
            **Allowing set functions for those properties in here can be misleading, since they actually modify the base snapshot!!!**
            **If the base snapshot is changed, they are lost!**
            What is the best solution?
            Should this class be a subclass of Snapshot?
  '''
  
  def __init__(self):
    ''' Constructor '''
    self.baseSnapshot = EpsilonSnapshot()

  def getName(self):
    return self.getBaseSnapshot().getName()

  def setBaseSnapshot(self, baseSnapshot):
    self.baseSnapshot = baseSnapshot

  def getBaseSnapshot(self):
    return self.baseSnapshot
    
  def setExtension(self, lowerCorner_vec3, upperCorner_vec3):
    self.baseSnapshot.setExtension(lowerCorner_vec3, upperCorner_vec3)
    return
    
  def getExtension(self):
    return self.baseSnapshot.getExtension()

  def write_entry(self, FILE=sys.stdout, mesh=None):
    raise Exception('This function has to be implemented by child classes.')
    return
    
  def setStartingSample(self, starting_sample):
    self.getBaseSnapshot().setStartingSample(starting_sample)
  def setFirst(self, starting_sample):
    self.getBaseSnapshot().setFirst(starting_sample)
  def setRepetition(self, starting_sample):
    self.getBaseSnapshot().setRepetition(starting_sample)

class SnapshotBoxXYZ(SnapshotBox):
  
  def __init__(self):
    ''' Constructor '''
    super().__init__()
    #self.baseSnapshot = EpsilonSnapshot()
    self.sides = [1,1,1] # x,y,z
    self.intersection_point = None
    return

  def getIntersectionPoint(self):
    return self.intersection_point
    
  def setIntersectionPoint(self, point):
    self.intersection_point = array(point)
    return
    
  def write_entry(self, FILE=sys.stdout, mesh=None):

    added_snapshots = []

    if self.intersection_point is None:
      self.intersection_point = self.baseSnapshot.getCentro()
    lower, upper = self.baseSnapshot.getExtension()
    snapshot_size = self.baseSnapshot.getSize()

    snapshot_x = copy.deepcopy(self.baseSnapshot)
    snapshot_x.plane = 'x'
    snapshot_x.setExtensionX(self.intersection_point[0], self.intersection_point[0])
    snapshot_x.write_entry(FILE, mesh)
    added_snapshots.append(snapshot_x)
    
    snapshot_y = copy.deepcopy(self.baseSnapshot)
    snapshot_y.plane = 'y'
    snapshot_y.setExtensionY(self.intersection_point[1], self.intersection_point[1])
    snapshot_y.write_entry(FILE, mesh)
    added_snapshots.append(snapshot_y)

    snapshot_z = copy.deepcopy(self.baseSnapshot)
    snapshot_z.plane = 'z'
    snapshot_z.setExtensionZ(self.intersection_point[2], self.intersection_point[2])
    snapshot_z.write_entry(FILE, mesh)
    added_snapshots.append(snapshot_z)
    
    return added_snapshots

class SnapshotBoxSurface(SnapshotBox):
  '''
  A utility class to easily create 6 snapshots on the surface of a box.
  
  Dilemma:
    * create boxsurface, boxvolume, etc classes which then write various snapshot types
    * or different snapshot types, which can then be written using boxsurface, boxvolume, etc writing functions?
  
  |  Solution 1 seems better. One or more snapshot classes could be passed to the writing function or as attribute...
  |  Also writing functions are more likely to increase, compared to the relatively static BFDTD.
  |  And if BFDTD does add new snapshot types, we should be able to derive them relatively easily from the base classes.
  |  Base classes should remain as simple as possible.
    
  |  problem: redefining all attributes and passing them...
  |  Maybe we should still go with including functions in the base Snapshot class?
  |  No, just inherit from Snapshot and redefine the writing function.
  |  But how to deal with the different types of snapshots?
  |  This would mean N*M classes for N snapshots and M writing methods.
  |  Better to pass a prepared snapshot to the writing classes, leading to N+M classes, but allowing for the same N*M behaviours!
    
  |  Snapping to the mesh should be done by the user outside this module.
  |  This gives more flexibility while keeping this module simple.
  |  Some utilities for snapping already exist ion the mesh class or elsewhere and more can be added.
  |  Once the meshing system is properly developed, all objects can easily access such functions to snap to the mesh or other similar operations. (ex: 50 snaps, but all on mesh, centered on snap i...)
  '''
  def __init__(self):
    ''' Constructor '''
    super().__init__()
    #self.baseSnapshot = EpsilonSnapshot()
    self.sides = [1, 1, 1, 1, 1, 1] # x-,x+,y-,y+,z-,z+
    return
  
  def write_entry(self, FILE=sys.stdout, mesh=None):

    added_snapshots = []

    lower, upper = self.baseSnapshot.getExtension()
    snapshot_centro = self.baseSnapshot.getCentro()
    snapshot_size = self.baseSnapshot.getSize()

    snapshot_x_lower = copy.deepcopy(self.baseSnapshot)
    snapshot_x_lower.plane = 'x'
    snapshot_x_lower.setExtensionX(lower[0], lower[0])
    snapshot_x_lower.write_entry(FILE, mesh)
    added_snapshots.append(snapshot_x_lower)

    snapshot_x_upper = copy.deepcopy(self.baseSnapshot)
    snapshot_x_upper.plane = 'x'
    snapshot_x_upper.setExtensionX(upper[0], upper[0])
    snapshot_x_upper.write_entry(FILE, mesh)
    added_snapshots.append(snapshot_x_upper)

    snapshot_y_lower = copy.deepcopy(self.baseSnapshot)
    snapshot_y_lower.plane = 'y'
    snapshot_y_lower.setExtensionY(lower[1], lower[1])
    snapshot_y_lower.write_entry(FILE, mesh)
    added_snapshots.append(snapshot_y_lower)

    snapshot_y_upper = copy.deepcopy(self.baseSnapshot)
    snapshot_y_upper.plane = 'y'
    snapshot_y_upper.setExtensionY(upper[1], upper[1])
    snapshot_y_upper.write_entry(FILE, mesh)
    added_snapshots.append(snapshot_y_upper)

    snapshot_z_lower = copy.deepcopy(self.baseSnapshot)
    snapshot_z_lower.plane = 'z'
    snapshot_z_lower.setExtensionZ(lower[2], lower[2])
    snapshot_z_lower.write_entry(FILE, mesh)
    added_snapshots.append(snapshot_z_lower)

    snapshot_z_upper = copy.deepcopy(self.baseSnapshot)
    snapshot_z_upper.plane = 'z'
    snapshot_z_upper.setExtensionZ(upper[2], upper[2])
    snapshot_z_upper.write_entry(FILE, mesh)
    added_snapshots.append(snapshot_z_upper)
    
    return added_snapshots
    
class SnapshotBoxVolume(SnapshotBox):
  '''Fill the volume corresponding to the box defined by (P1,P2) with snapshots based on the given baseSnapshot.'''
  def __init__(self):
    ''' Constructor '''
    super().__init__()
    #self.baseSnapshot = EpsilonSnapshot()

  #def setBaseSnapshot(self, baseSnapshot):
    #self.baseSnapshot = baseSnapshot

  #def getBaseSnapshot(self):
    #return self.baseSnapshot
    
  #def setExtension(self, lowerCorner_vec3, upperCorner_vec3):
    #self.baseSnapshot.setExtension(lowerCorner_vec3, upperCorner_vec3)
    #return
    
  #def getExtension(self):
    #return self.baseSnapshot.getExtension()

  # these are not in the base class, because XYZ and surface boxes do not need them.
  def setPlaneOrientationX(self):
    self.baseSnapshot.setPlaneOrientationX()
  def setPlaneOrientationY(self):
    self.baseSnapshot.setPlaneOrientationY()
  def setPlaneOrientationZ(self):
    self.baseSnapshot.setPlaneOrientationZ()

  def setupSnapshots(self, mesh=None):
    if mesh is None:
      mesh = MeshObject()

    added_snapshots = []

    lower, upper = self.baseSnapshot.getExtension()

    if self.baseSnapshot.getPlaneLetter() == 'x':
      position_list = mesh.getXmesh()
      for position in position_list:
        if lower[0] <= position <= upper[0]:
          snapshot = copy.deepcopy(self.baseSnapshot)
          snapshot.setExtension([position, lower[1], lower[2]],
                                [position, upper[1], upper[2]])
          #snapshot.write_entry(FILE, mesh)
          added_snapshots.append(snapshot)

    elif self.baseSnapshot.getPlaneLetter() == 'y':
      position_list = mesh.getYmesh()
      for position in position_list:
        if lower[1] <= position <= upper[1]:
          snapshot = copy.deepcopy(self.baseSnapshot)
          snapshot.setExtension([lower[0], position, lower[2]],
                                [upper[0], position, upper[2]])
          #snapshot.write_entry(FILE, mesh)
          added_snapshots.append(snapshot)

    else:
      position_list = mesh.getZmesh()
      for position in position_list:
        if lower[2] <= position <= upper[2]:
          snapshot = copy.deepcopy(self.baseSnapshot)
          snapshot.setExtension([lower[0], lower[1], position],
                                [upper[0], upper[1], position])
          #snapshot.write_entry(FILE, mesh)
          added_snapshots.append(snapshot)
      
    return (mesh, added_snapshots)

  def write_entry(self, FILE=sys.stdout, mesh=None):
    (mesh, added_snapshots) = self.setupSnapshots(mesh)
    for snapshot in added_snapshots:
      snapshot.write_entry(FILE, mesh)
    return added_snapshots

  def write_data(self, sampling_function, mesh=None, numID = 0, probe_ident = '_id_', snap_time_number = 0, destdir='.'):
    (mesh, added_snapshots) = self.setupSnapshots(mesh)
    print(added_snapshots)
    for idx, snapshot in enumerate(added_snapshots):
      snapshot.write_data(sampling_function, mesh, numID+idx, probe_ident, snap_time_number, destdir=destdir)
    return added_snapshots

#class SnapshotBoxVolumeMeshIndependent(object):
  #pass

class EnergySnapshot(FrequencySnapshot):
  def __init__(self):
    ''' Constructor '''
    super().__init__()
    self.epsilon_repetition = int(1e9)
    return

  def setFromSnapshot(self, snapshot_in):
    super().setFromSnapshot(snapshot_in)
    if 'epsilon_repetition' in dir(snapshot_in):
      self.epsilon_repetition = snapshot_in.epsilon_repetition
    return

  def setupEpsilonSnapshot(self):
    #print('EnergySnapshot.write_entry')
    
    # create an epsilon snapshot
    epsilon_snapshot = EpsilonSnapshot()
    epsilon_snapshot.setFromSnapshot(self)
    #epsilon_snapshot.setExtensionFromSnapshot(self)
    epsilon_snapshot.first = 1
    epsilon_snapshot.repetition = self.epsilon_repetition
    
    #print(epsilon_snapshot.getPlaneLetter())
    #print(epsilon_snapshot.getExtension())
    return(epsilon_snapshot)

  def getSplitSnapshots(self):
    '''
    Returns the epsilon and frequency snapshots that would be used.
    '''
    epsilon_snapshot = self.setupEpsilonSnapshot()
    frequency_snapshot = FrequencySnapshot()
    frequency_snapshot.setFromSnapshot(self)
    return [epsilon_snapshot, frequency_snapshot]

  def write_entry(self, FILE=sys.stdout, mesh=None):
    
    epsilon_snapshot = self.setupEpsilonSnapshot()
    
    # write the epsilon snapshot
    epsilon_snapshot.write_entry(FILE, mesh)
    
    # write the frequency snapshot using the FrequencySnapshot.write_entry function
    FrequencySnapshot.write_entry(self, FILE, mesh)

    return

  def write_data(self, sampling_function, mesh=None, numID = 0, probe_ident = '_id_', snap_time_number = 0, destdir='.'):
    '''
    .. todo:: The speed could be improved here by writing epsilon and frequency snapshots at the same time, since we need to compute the sample function on both for the same points. Is it worth optimizing the sampling for tests?
    '''
    epsilon_snapshot = self.setupEpsilonSnapshot()
    epsilon_snapshot.write_data(sampling_function, mesh, numID, probe_ident, snap_time_number, destdir=destdir)
    FrequencySnapshot.write_data(self, sampling_function, mesh, numID, probe_ident, snap_time_number, destdir=destdir)
    return

#-----------------------------------------------------------------------
# Are those really necessary? Their only function is to make P1,P2 cover the whole mesh easier. Why not simply use setExtension? Or easy setXfull(), etc functions in the base Snapshot class?
#class FrequencySnapshotFull(FrequencySnapshot):
  #pass

#class TimeSnapshotFull(TimeSnapshot):
  #pass

#class ModeFilteredProbeFull(ModeFilteredProbe):
  #pass

#class EpsilonSnapshotFull(EpsilonSnapshot):
  #pass
#-----------------------------------------------------------------------

class EpsilonBox(EpsilonSnapshot):
  def __init__(self):
    ''' Constructor '''
    super().__init__()
    self.setExtension([0,0,0],[1,1,1])
    self.setFullExtensionOff()

  def write_entry(self, FILE=sys.stdout, mesh=None):
    #print('EpsilonBox.write_entry')

    base_snapshot = EpsilonSnapshot()
    base_snapshot.setFromSnapshot(self)

    snapshot_box = SnapshotBoxVolume()
    snapshot_box.setBaseSnapshot(base_snapshot)
    snapshot_box.write_entry(FILE, mesh)
    
    return

class EpsilonBoxFull(EpsilonBox):
  def __init__(self):
    ''' Constructor '''
    super().__init__()
    self.setFullExtensionOn()

  def write_entry(self, FILE=sys.stdout, mesh=None):
    if mesh is None:
      mesh = MeshObject()
    self.setExtension(*mesh.getExtension())
    EpsilonBox.write_entry(self, FILE, mesh)
    return

class TimeSnapshotBox(TimeSnapshot):
  def __init__(self):
    ''' Constructor '''
    super().__init__()
    self.setExtension([0,0,0],[1,1,1])
    self.setFullExtensionOff()
    
  def setupSnapshotBox(self):
    base_snapshot = TimeSnapshot()
    base_snapshot.setFromSnapshot(self)

    snapshot_box = SnapshotBoxVolume()
    snapshot_box.setBaseSnapshot(base_snapshot)
    return(snapshot_box)

  def write_entry(self, FILE=sys.stdout, mesh=None):
    snapshot_box = self.setupSnapshotBox()
    snapshot_box.write_entry(FILE, mesh)
    return
  
  def write_data(self, sampling_function, mesh=None, numID = 0, probe_ident = '_id_', snap_time_number = 0, destdir='.'):
    snapshot_box = self.setupSnapshotBox()
    snapshot_box.write_data(sampling_function, mesh, numID, probe_ident, snap_time_number, destdir=destdir)
    return

class TimeSnapshotBoxFull(TimeSnapshotBox):
  '''
    Example usage::
    
      Tbox=TimeSnapshotBoxFull()
      sim.appendSnapshot(Tbox)
  '''
  def __init__(self):
    ''' Constructor '''
    super().__init__()
    self.setFullExtensionOn()

  def write_entry(self, FILE=sys.stdout, mesh=None):
    if mesh is None:
      mesh = MeshObject()
    self.setExtension(*mesh.getExtension())
    TimeSnapshotBox.write_entry(self, FILE, mesh)
    return

class ModeVolumeBox(EnergySnapshot):
  '''
  This one is definitely necessary and should be as easy to use as possible.
  
  The other necessity is an EpsilonBox for geometry checking. Perhaps with Nx,Ny,Nz specification for mesh independence.
  
  .. todo:: need to make sure BFDTD does no weird auto-snap to mesh
  
  '''
  def __init__(self):
    ''' Constructor '''
    super().__init__()
    self.setExtension([0,0,0],[1,1,1])
    self.setFullExtensionOff()
    #self.epsilon_repetition = int(1e9)
    #self.baseSnapshot = EpsilonSnapshot()
    #FrequencySnapshot.__init__(self)
    #self.name = self.__class__.__name__
    #self.layer = self.__class__.__name__
    #self.group = self.__class__.__name__

  def setupEnergySnapshotBox(self):
    #print('ModeVolumeBox.write_entry')

    base_snapshot = EnergySnapshot()
    base_snapshot.setFromSnapshot(self)

    energy_snapshot_box = SnapshotBoxVolume()
    energy_snapshot_box.setBaseSnapshot(base_snapshot)
    return(energy_snapshot_box)

  def write_entry(self, FILE=sys.stdout, mesh=None):
    energy_snapshot_box = self.setupEnergySnapshotBox()
    energy_snapshot_box.write_entry(FILE, mesh)
    return
  
  def write_data(self, sampling_function, mesh=None, numID = 0, probe_ident = '_id_', snap_time_number = 0, destdir='.'):
    energy_snapshot_box = self.setupEnergySnapshotBox()
    energy_snapshot_box.write_data(sampling_function, mesh, numID, probe_ident, snap_time_number, destdir=destdir)
    return


class ModeVolumeBoxFull(ModeVolumeBox):
  '''
    Example usage::
    
      MV=ModeVolumeBoxFull()
      sim.appendSnapshot(MV)
  '''
  def __init__(self):
    ''' Constructor '''
    super().__init__()
    self.setFullExtensionOn()
  
  def setup(self, mesh=None):
    '''
    to call before using
    .. todo:: mesh keeps having to be passed arround. Define as attribute?
    '''
    if mesh is None:
      mesh = MeshObject()
    self.setExtension(*mesh.getExtension())
    return
    
  def getEnergySnapshots(self, mesh=None):
    '''
    Returns the energy snapshots that would be written. Useful for counting the resulting number of snapshots and split-writing.
    .. todo:: create this function at a lower level, so it works for other boxes, etc + make use of it when finally writing
    '''
    energy_snapshot_list = []
    self.setup(mesh=mesh)
    energy_snapshot_box = self.setupEnergySnapshotBox()
    (used_mesh, energy_snapshot_list) = energy_snapshot_box.setupSnapshots(mesh=mesh)
    return energy_snapshot_list
    
  def getSplitSnapshots(self, mesh=None):
    energy_snapshot_list = self.getEnergySnapshots(mesh=mesh)
    epsilon_snapshot_list = []
    frequency_snapshot_list = []
    for energy_snapshot in energy_snapshot_list:
      esnap, fsnap = energy_snapshot.getSplitSnapshots()
      epsilon_snapshot_list.append(esnap)
      frequency_snapshot_list.append(fsnap)
    return (epsilon_snapshot_list, frequency_snapshot_list)

  def write_entry(self, FILE=sys.stdout, mesh=None):
    self.setup(mesh=mesh)
    ModeVolumeBox.write_entry(self, FILE, mesh=mesh)
    return

    # TODO: solve inf recursion
    #base_epsilon_snapshot = EpsilonSnapshot
    #base_snapshot.setExtensionFromSnapshot(self)
    #snapshot_stats

    #SnapshotBoxVolume.write_entry(self, FILE, mesh)

    #return
    #energy_snapshot_box = SnapshotBoxVolume()
    #energy_snapshot_box.setBaseSnapshot(self)
    
    
    #self.write_entry(FILE, mesh)

    #epsilon_snapshot_box = SnapshotBoxVolume()
    #epsilon_snapshot_box.setBaseSnapshot(self)
    #epsilon_snapshot_box.getBaseSnapshot().first = 1
    #epsilon_snapshot_box.getBaseSnapshot().repetition = self.epsilon_repetition

    #frequency_snapshot_box = SnapshotBoxVolume()
    #frequency_snapshot_box.setBaseSnapshot(self)
    
    #epsilon_snapshot_box.write_entry(FILE, mesh)
    #FrequencySnapshot.write_entry(self, FILE, mesh)
    #frequency_snapshot_box
    #return

    #esnap = EpsilonSnapshot()
    #esnap.plane = self.plane

    #fsnap = FrequencySnapshot()
    #fsnap.plane = self.plane
    #fsnap.setFrequencies(self.frequency_vector)

    ## TODO: It seems we could use a fsnap+esnap combo as well...

    #if self.plane == 1:
      #xmin_idx, xmin_val = findNearest(mesh.getXmesh(), self.P1[0])
      #xmax_idx, xmax_val = findNearest(mesh.getXmesh(), self.P2[0])
      #ymin = self.P1[1]
      #zmin = self.P1[2]
      #ymax = self.P2[1]
      #zmax = self.P2[2]
      #for idx in range(xmin_idx, xmax_idx+1):
        #x = mesh.getXmesh()[idx]
        #esnap.setExtension([x, ymin, zmin], [x, ymax, zmax])
        #esnap.write_entry(FILE, mesh)
        #fsnap.setExtension([x, ymin, zmin], [x, ymax, zmax])
        #fsnap.write_entry(FILE, mesh)
    
    #findNearest(mesh.getXmesh(), self.P1[0])
    #findNearest(mesh.getYmesh(), self.P1[1])
    #findNearest(mesh.getZmesh(), self.P1[2])
    #snapped_P1 = mesh.getNearest(self.P1)
    #snapped_P2 = mesh.getNearest(self.P2)
    #print(snapped_P1)
    #print(snapped_P2)
    
    #return

  #def setSnapshotTypeToPlane(self):
    #self.snapshot_type = 'plane'
  #def setSnapshotTypeToBoxSurface(self):
    #self.snapshot_type = 'box_surface'
  #def setSnapshotTypeToBoxVolume(self):
    #self.snapshot_type = 'box_volume'
  
  #def setFullExtension(self, full_extension_bool):
    #self.full_extension_bool = full_extension_bool
  
  #def writePlane(self, mesh_object=None):
    #raise Exception('This function has to be implemented by child classes.')
    #return

  #def writeBoxSurface(self, mesh_object=None):
    #raise Exception('This function has to be implemented by child classes.')
    #return

  #def writeBoxVolume(self, mesh_object=None):
    #raise Exception('This function has to be implemented by child classes.')
    #return
  
  #def write(self, mesh_object=None):
    #'''
    #* Uses write_entry function from the subclass calling it.
    #* If mesh is None, it simply creates a single snapshot, otherwise, depending on the other attributes, it writes multiple snapshots based on the mesh
    #* To increase speed (ex: when a lot of snapshots are written), we should directly pass computed information like the mesh size.
    #* No attributes should be modified by this function!
    #'''
    #if self.snapshot_type == 'plane':
      #self.writePlane(mesh_object)
    #elif self.snapshot_type == 'box_surface':
      #self.writeBoxSurface(mesh_object)
    #elif self.snapshot_type == 'box_volume':
      #self.writeBoxVolume(mesh_object)
    #else:
      #print('ERROR: Invalid snapshot type.', file=sys.stderr)
      #sys.exit(-1)

    #if self.plane 
    
    ##if mesh_object:
      ##(mesh_size, mesh_resolution) = mesh_object.getSizeAndResolution()

    ## extension
    #if self.full_extension_bool:
      #self.P1 = [0,0,0]
      #self.P2 = mesh_size

    #if self.name is None:
      #planeIdx_bfdtd2letter(self.plane).upper()
      
      #self.name = ['X','Y','Z']'X '+self.__name__

    #centro_vec3 = self.getCentro()
    
    #if self.plane == 1:
      #if self.name is None:
        #self.name = 'X '+self.__name__
      #self.P1[0] = centro_vec3[0]
    #elif self.plane == 2:
      #if self.name is None:
        #self.name = 'Y '+self.__name__
      #self.P1[1] = centro_vec3[1]
    #elif self.plane == 3:
      #if self.name is None:
        #self.name = 'Z '+self.__name__
      #self.P1[2] = centro_vec3[2]
    #else:
      #print(('ERROR: Invalid plane : ',plane))
      #sys.exit(1)
    #S = snapshot_class(name=name, plane=plane_bfdtdidx, P1=L, P2=U)
    #self.snapshot_list.append(S)
    #return S

  #def __init__(self):
    #self.location = array([0.5, 0.5, 0.5])
    #self.dimensions = array([1, 1, 1])
  #def getLocation(self):
    #return self.location
  #def getSize(self):
    #return self.dimensions
  #def setLocation(self, location):
    #self.location = location
  #def setSize(self, dimensions):
    #self.dimensions = dimensions

  #def getLowerAbsolute(self):
    #return self.location - 0.5*self.dimensions
  #def getUpperAbsolute(self):
    #return self.location + 0.5*self.dimensions

  #def setLowerAbsolute(self):
    #P2 = self.getUpperAbsolute()
    #return self.location - 0.5*self.dimensions
  #def setUpperAbsolute(self):
    #return self.location + 0.5*self.dimensions
  
  #pass

def test_interactive():
  # read in ~/.pystartup to have all the desired modules
  pystartup = os.path.expanduser("~/.pystartup")
  with open(pystartup) as f:
    code_object = compile(f.read(), pystartup, 'exec')
    exec(code_object)

  s = Snapshot()
  print(s)
  #s.write_entry()
  
  f = FrequencySnapshot()
  print(f)
  f.write_entry()

  t = TimeSnapshot()
  print(t)
  t.write_entry()

  e = EpsilonSnapshot()
  print(e)
  e.write_entry()

  m = ModeFilteredProbe()
  print(m)
  m.write_entry()

  code.interact(local=locals())

if __name__ == '__main__':
  unittest.main()
