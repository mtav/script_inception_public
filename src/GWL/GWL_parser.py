#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import numpy
import argparse
import tempfile
import warnings
from numpy import floor, ceil
from numpy.linalg import norm
from utilities.common import *
from utilities import TransformationMatrix

# TODO: get voxelsize in any direction based on a 3D ellipsoid...

# TODO: Somehow get voxel size based on scanspeed/power/dwelltime/defocusfactor/etc
DEFAULT_VOXEL_WIDTH = 0.100 # in mum
DEFAULT_VOXEL_HEIGHT = 0.200 # in mum
DEFAULT_OVERLAP_HORIZONTAL = 0.5
DEFAULT_OVERLAP_VERTICAL = 0.5

# TODO: Start creating external GWL object classes like blocks, spheres, etc which can be added to a main GWL object (similar to BFDTD)

# TODO: Add options or new functions to allow other desired systems like extremity points always separated by length, or always fill so that it touches the extremities, etc
# TODO: Document with pictures. Check how to do that with doxygen or similar.
# TODO: Start generating code documentation.
def calculateNvoxelsAndInterVoxelDistance(Length, Voxelsize, Overlap):
  '''
  Calulates the number of voxels and the distance between them so that they fit into length "Length" with an overlap "Overlap", i.e. so that:
  
  * InterVoxelDistance = (1-Overlap)*Voxelsize
  * (Nvoxels-1)*InterVoxelDistance + Voxelsize <= Length
  '''

  if Overlap < 0 or Overlap >= 1:
    raise Exception('ERROR: Invalid Overlap = {}'.format(Overlap))

  if Voxelsize == 0:
    raise Exception('ERROR: Invalid Voxelsize = {}'.format(Voxelsize))

  InterVoxelDistance = (1-Overlap)*Voxelsize
  #Nvoxels = math.floor( ((Length-Voxelsize)/InterVoxelDistance) + 1 )

  # Same formula as above, but seems to work better in some cases (gave expected floor(3.0)=3 instead of floor(2.999...)=2 in one case for instance...)
  Nvoxels = math.floor( ((Length-Overlap*Voxelsize)/InterVoxelDistance) )

  if(Nvoxels) <= 0:
    Nvoxels = 1
    sys.stderr.write('WARNING: Voxel too big for specified length.\n')

  return (Nvoxels, InterVoxelDistance)

class GWLobject(object):
  '''This is the main class used to read/write/create GWL files for the Nanoscribe.
  
  Basic usage example::
  
    #!/usr/bin/env python3
    from GWL.GWL_parser import GWLobject
    
    obj = GWLobject()
    obj.addVoxel([10, 20, 30, 40])
    obj.addVoxel([11, 21, 31, 41])
    obj.addVoxel([12, 22, 32, 42])
    obj.startNewVoxelSequence()
    obj.addVoxel([5, 6, 7])
    obj.addVoxel([8, 9, 10])
    obj.addVoxel([5, 6, 7])
    obj.addVoxel([8, 9, 10])
    obj.startNewVoxelSequence()
    obj.addVoxel([5, 6, 7])
    obj.addVoxel([8, 9, 10])
    obj.writeGWL('foo.gwl')
    
  This should produce a file named 'foo.gwl' containing::
  
    10.000  20.000  30.000  40.000
    11.000  21.000  31.000  41.000
    12.000  22.000  32.000  42.000
    Write
    5.000   6.000   7.000
    8.000   9.000   10.000
    5.000   6.000   7.000
    8.000   9.000   10.000
    Write
    5.000   6.000   7.000
    8.000   9.000   10.000
    Write

  **Attributes**:
  
  * Writing settings:
    
  :ivar set_lower_to_origin: If true, offsets the structure so that the lower corner is at (0,0,0). Defaults to False.
  :ivar write_power: Write out power values. Defaults to False.

  * Power compensation settings (set the slope to zero for a constant power):
    
  :ivar PC_laser_power_at_z0:      PC_laser_power_at_z0. Defaults to 100.
  :ivar PC_slope:                  PC_slope (set the slope to zero for a constant power). Defaults to 0.
  :ivar PC_interfaceAt:            PC_interfaceAt. Defaults to 0.
  :ivar PC_float_height:           PC_float_height. Defaults to 0.
  :ivar PC_bool_InverseWriting:    PC_bool_InverseWriting. Defaults to False.
  :ivar PC_bool_LaserPowerCommand: PC_bool_LaserPowerCommand.  Defaults to False.
  
  .. note:: They currently only have an effect when :py:func:`writeGWLWithPowerCompensation` is used. Not when :py:func:`writeGWL` is used.

  **Inner workings**:
  
    The voxels are stored in **GWL_voxels**.
    This is the most important attribute.
    It stores all voxels in a list of the form [ write_sequence_0, write_sequence_1, ... ] where:
    
    * the write_sequence_i are of the form [voxel_0, voxel_1, ...]
    * the voxel_i of the form [x, y, z] or [x, y, z, power].

  .. todo:: Needs to be rewritten to support new GWL commands, but also non-voxel/Write commands in general...
  .. todo:: Document all attributes using ivar and #:
  .. todo:: Use vtkpolydata or similar for paraview visualization, boolean operations, etc
  .. todo:: Maybe add a vtk-like Update() function which would do all the things which are currently done during writing? Writing would then call update before doing a very basic write call. Issues: Speed... Doing everything in VTK, using filters, etc, might speed up the process.
  '''
  
  def __init__(self):
    '''Constructor'''
    self.verbosity = 0
    self.GWL_voxels = [] #: "List of lists of voxels".
    self.voxel_offset = [0,0,0,0]
    self.FindInterfaceAt = [0,0,0,0]
    self.stage_position = [0,0,0,0]
    self.LineNumber = 1
    self.LineDistance = 0
    self.PowerScaling = 1
    self.LaserPower = 100
    self.ScanSpeed = 200
    self.Repeat = 1
    self.path_substitutes = []
    self.writingTimeInSeconds = 0
    self.writingDistanceInMum = 0
    self.DwellTime = 200 #: in ms = 1e-3 seconds
    self.minDistanceBetweenLines = 1000 #: shortest distance from end of one line to start of next one
    self.maxDistanceBetweenLines = 0 #: maximum acceptable distance from end of one line to start of next one
    self.LastVoxel = [0,0,0,0]
    self.LastVoxelSet = False
    self.out_of_range = False

    self.overlap_horizontal = DEFAULT_OVERLAP_HORIZONTAL
    self.overlap_vertical = DEFAULT_OVERLAP_VERTICAL
    self.voxel_width_mum = DEFAULT_VOXEL_WIDTH
    self.voxel_height_mum = DEFAULT_VOXEL_HEIGHT

    self.PositionMinimum = 4*[0] #: Minimum of X, Y, Z and power. Updated with updateLimits() and retrievable with getLimits().
    self.PositionMaximum = 4*[0] #: Maximum of X, Y, Z and power. Updated with updateLimits() and retrievable with getLimits().

    # writing settings
    self.set_lower_to_origin = False #: If true, offsets the structure so that the lower corner is at (0,0,0)
    self.write_power = False #: write out power values
    self.reverse_line_order_on_write = False #: If True, the order of the lines will be reversed **during writing**. See also: :py:func:`reverse`
    self.reverse_voxel_order_per_line_on_write = False #: If True, the order of the voxels in each line will be reversed **during writing**. See also: :py:func:`reverse`

    # power compensation settings 
    self.PC_laser_power_at_z0 = 100 #: PC_laser_power_at_z0
    self.PC_slope = 0 #: PC_slope (set the slope to zero for a constant power)
    self.PC_interfaceAt = 0 #: PC_interfaceAt
    self.PC_float_height = 0 #: PC_float_height
    self.PC_bool_InverseWriting = False #: PC_bool_InverseWriting
    self.PC_bool_LaserPowerCommand = False #: PC_bool_LaserPowerCommand
  
  def setVoxels(self, L):
    ''' Set the voxels as a list of the form [[v0,v1,...], [vA,vB,...], ...] where v* are voxel coordinates, i.e. [X,Y,Z] or [X,Y,Z,power]. '''
    self.GWL_voxels = L
    return
    
  def getVoxels(self, L):
    ''' Returns a list of the voxels in the form specified in :py:func:`setVoxels`. '''
    return(self.GWL_voxels)
  
  def appendVoxels(L):
    ''' "append" a "line of voxels" '''
    self.GWL_voxels.append(L)
    
  def extendVoxels(L):
    ''' "extend" with multiple "lines of voxels" '''
    self.GWL_voxels.extend(L)
  
  def reverse(self, reverse_line_order=True, reverse_voxel_order_per_line=True):
    '''Reverse the order of the voxels. Unlike  :py:attr:`reverse_line_order_on_write` and :py:attr:`reverse_voxel_order_per_line_on_write`, this applies directly.
    
    :param reverse_line_order: If True, the order of the lines will be reversed, i.e.::
    
        voxel0
        voxel1
        voxel2
        Write
        voxel3
        voxel4
        voxel5
        Write
      
      becomes::

        voxel3
        voxel4
        voxel5
        Write
        voxel0
        voxel1
        voxel2
        Write

    :param reverse_voxel_order_per_line: If True, the order of the voxels in each line will be reversed, i.e.::
    
        voxel0
        voxel1
        voxel2
        Write
        voxel3
        voxel4
        voxel5
        Write
      
      becomes::

        voxel2
        voxel1
        voxel0
        Write
        voxel5
        voxel4
        voxel3
        Write
    
    :return: None
    '''
    if reverse_line_order:
      self.GWL_voxels.reverse()
    
    if reverse_voxel_order_per_line:
      for write_sequence in self.GWL_voxels:
        write_sequence.reverse()
    
    return
  
  def add_arguments(self, parser):
    '''Adds GWLobject related arguments to the given *parser* (an argparse.ArgumentParser instance).
    
    See also: :py:func:`setAttributesFromParsedOptions`
    
    .. todo:: Make argparseui create something in the interface to separate groups.
    '''

    group_WritingSettings = parser.add_argument_group('GWL writing settings')
    group_WritingSettings.add_argument("--set-lower-to-origin", help='offset structure so that its "lower corner" is moved to the (0,0,0) coordinates. This will make all coordinates positive.', action="store_true")
    group_WritingSettings.add_argument("--write-power", help="Write power values using the power compensation (PC) parameters.", action="store_true")
    group_WritingSettings.add_argument("--reverse_line_order_on_write", help="reverse line order on write", action="store_true")
    group_WritingSettings.add_argument("--reverse_voxel_order_per_line_on_write", help="reverse voxel order per line on write", action="store_true")

    group_PowerCompensation = parser.add_argument_group('GWL power compensation', 'LP(Z) = (1+K*(Z-interfaceAt))*LP(0) if bool_InverseWriting=False or LP(Z) = (1+K*((H-Z)+interfaceAt))*LP(0) if bool_InverseWriting=True') # TODO: nicely formatted help/description?
    group_PowerCompensation.add_argument("--PC_laser_power_at_z0", help="PC: laser power at z0", type=float, default=100)
    group_PowerCompensation.add_argument("--PC_slope", help="PC: power compensation slope", type=float, default=0)
    group_PowerCompensation.add_argument("--PC_interfaceAt", help="PC: interface position", type=float, default=0)
    group_PowerCompensation.add_argument("--PC_bool_InverseWriting", help="PC: To write a file designed for use with the InvertZAxis command", action="store_true", default=False)
    group_PowerCompensation.add_argument("--PC_float_height", help='PC: "substrate height", in practice just a value added to the interfaceAt value', type=float, default=0)
    group_PowerCompensation.add_argument("--PC_bool_LaserPowerCommand", help="PC: Use the LaserPower command instead of a 4th coordinate for power.", action="store_true", default=False)

    return

  def get_argument_parser(self):
    parser = argparse.ArgumentParser(description = self.__doc__.split('\n')[0], fromfile_prefix_chars='@')
    parser.add_argument('-d','--outdir', action="store", dest="outdir", default=tempfile.gettempdir(), help='output directory')
    parser.add_argument('-b','--basename', action="store", dest="basename", default=self.__class__.__name__, help='output basename')
    self.add_arguments(parser)
    return parser

  def setAttributesFromParsedOptions(self, options):
    '''Sets the object's attributes based on the ones from the *options* object (usually an argparse.ArgumentParser instance).
    
    See also: :py:func:`add_arguments`
    '''
    self.set_lower_to_origin = options.set_lower_to_origin
    self.write_power = options.write_power
    self.reverse_line_order_on_write = options.reverse_line_order_on_write
    self.reverse_voxel_order_per_line_on_write = options.reverse_voxel_order_per_line_on_write
    self.PC_laser_power_at_z0 = options.PC_laser_power_at_z0
    self.PC_slope = options.PC_slope
    self.PC_interfaceAt = options.PC_interfaceAt
    self.PC_bool_InverseWriting = options.PC_bool_InverseWriting
    self.PC_float_height = options.PC_float_height
    self.PC_bool_LaserPowerCommand = options.PC_bool_LaserPowerCommand
    return

  def getMinDistanceBetweenVoxels():
    '''
    .. todo:: finish implementing...
    '''
    return(0)

  def updateLimits(self):
    ''' Updates the PositionMinimum and PositionMaximum attributes.

    See also getLimits().
    
    :return: (PositionMinimum, PositionMaximum) where PositionMinimum and PositionMaximum are lists of size 4 containing [Xmin, Ymin, Zmin, Pmin] and [Xmax, Ymax, Zmax, Pmax] respectively.
    '''
    self.PositionMinimum = 4*[0]
    self.PositionMaximum = 4*[0]
    first = True
    for write_sequence in self.GWL_voxels:
      for voxel in write_sequence:
        if first:
            for i in range(len(voxel)):
                self.PositionMinimum[i] = voxel[i]
                self.PositionMaximum[i] = voxel[i]
            first = False
        else:
            for i in range(len(voxel)):
                if voxel[i] < self.PositionMinimum[i]:
                    self.PositionMinimum[i] = voxel[i]
                if self.PositionMaximum[i] < voxel[i]:
                    self.PositionMaximum[i] = voxel[i]

    return (self.PositionMinimum, self.PositionMaximum)

  def getLimits(self, update_limits=True):
    ''' This function returns the minimum and maximum x,y,z coordinates.

    To optimize speed, it only returns the currently stored limits, which should be computed while adding voxels.
    To update the limits, call updateLimits().

    :param bool update_limits: If true, updateLimits() will be called.

    :return: (PositionMinimum, PositionMaximum) where PositionMinimum and PositionMaximum are lists of size 4 containing [Xmin, Ymin, Zmin, Pmin] and [Xmax, Ymax, Zmax, Pmax] respectively.
    '''
    if update_limits:
      self.updateLimits()
    return (self.PositionMinimum, self.PositionMaximum)
    
  def getMeshData(self, position = [0,0,0]):
    verts_loc = []
    edges = []
    faces = []
    last_voxel_index = 0
    for write_sequence in self.GWL_voxels:
      local_vertex_counter = -1
      for voxel in write_sequence:
        x = position[0]+voxel[0]
        y = position[1]+voxel[1]
        z = position[2]+voxel[2]
        verts_loc.append([x,y,z])
      if len(write_sequence)>0:
        #edges.append(range(last_voxel_index, last_voxel_index + len(write_sequence)))
        #edges.append(list(range(last_voxel_index, last_voxel_index + len(write_sequence))))
        edges.extend( [ [i,i+1] for i in range(last_voxel_index, last_voxel_index + len(write_sequence) - 1 ) ] )
        last_voxel_index = last_voxel_index + len(write_sequence)
    return((verts_loc, edges, faces))

  # TODO: maybe create an iterator for voxels, to make operations on all voxels as easy as for v in voxels: ...
  def applyOffset(self, offset):
    for write_sequence in self.GWL_voxels:
      for voxel in write_sequence:
        for i in range(len(offset)):
          # TODO: URGENT/EASY: check that this works correctly for when voxel and offset don't have the same length...
          if i<len(voxel):
            voxel[i] = voxel[i] + offset[i]
          else:
            voxel.append(offset[i])
    return

  def getPower(self, z, PC_laser_power_at_z0=None, PC_slope=None, PC_interfaceAt=None, PC_bool_InverseWriting=None, PC_float_height=None):
    '''calculate power for a given z position'''
    
    if PC_laser_power_at_z0 is None: PC_laser_power_at_z0 = self.PC_laser_power_at_z0
    if PC_slope is None: PC_slope = self.PC_slope
    if PC_interfaceAt is None: PC_interfaceAt = self.PC_interfaceAt
    if PC_bool_InverseWriting is None: PC_bool_InverseWriting = self.PC_bool_InverseWriting
    if PC_float_height is None: PC_float_height = self.PC_float_height
    
    if PC_bool_InverseWriting:
      power = (1 + PC_slope*((PC_float_height - z) + PC_interfaceAt)) * PC_laser_power_at_z0
    else:
      power = (1 + PC_slope*(z - PC_interfaceAt)) * PC_laser_power_at_z0
    
    if power<0: power=0
    if power>100: power=100
    
    return power    

  def addPowerCompensation(self, laser_power_at_z0, K, interfaceAt=0, bool_InverseWriting=False, float_height=0):
    '''
    Add a 4th power component to voxels based on the formula:
    
    * LP(Z) = (1+K*(Z-interfaceAt))*LP(0) if bool_InverseWriting=False
    * LP(Z) = (1+K*((H-Z)+interfaceAt))*LP(0) if bool_InverseWriting=True
    
    .. todo:: This function loops through all voxels again. It might be worth creating an addVoxel() function, so that any other functions creating the voxel lists directly add the power compensation as well.
    .. todo:: use in export GWL script (requires following TODO done first)
    .. todo:: Add option to use LaserPower command instead of 4th power voxel coordinate. Requires changing the way GWL info is stored. (or separate writeGWL function)
    .. todo:: Document this properly with an easy to understand image...
    '''
    for write_sequence_idx in range(len(self.GWL_voxels)):
      write_sequence = self.GWL_voxels[write_sequence_idx]
      for voxel_idx in range(len(write_sequence)):
        voxel = write_sequence[voxel_idx]
        voxel = list(voxel)

        if len(voxel)<4:
          #voxel[:] = numpy.append(voxel,0)
          voxel.append(0)

        # calculate power for current voxel
        voxel[3] = self.getPower(voxel[2], PC_laser_power_at_z0=laser_power_at_z0, PC_slope=K, PC_interfaceAt=interfaceAt, PC_bool_InverseWriting=bool_InverseWriting, PC_float_height=float_height)
        
        write_sequence[voxel_idx] = voxel

      self.GWL_voxels[write_sequence_idx] = write_sequence

    return

  def getLastVoxel(self):
    found = False
    voxel = [0,0,0,0]
    for i in range(len(self.GWL_voxels)):
        write_sequence = self.GWL_voxels[-i]
        if len(write_sequence)>0:
            voxel = write_sequence[-1]
            found = True
            break
    return (voxel,found)

  def getNvoxels():
    print('ok')

  def clear(self):
    self.GWL_voxels = []
    self.voxel_offset = [0,0,0,0]

  def addLine(self, P1, P2, power=-1):
    write_sequence = [P1,P2]
    self.GWL_voxels.append(write_sequence)

  # HACK: quick hack to create "flat lines"
  def addFlatLine(self, P1, P2, line_distance, line_number, power=-1):
    z = numpy.array([0,0,1])
    #print('===============AD',P1)
    P1 = numpy.array(P1)
    #print('===============BD',P1)
    P2 = numpy.array(P2)
    u = P2 - P1
    v = numpy.cross(u,z)
    v = v/norm(v,2)

    L = line_distance * (line_number-1)
    delta_list = numpy.linspace(-0.5*L, 0.5*L, line_number)

    for i in range(line_number):
      A = P1 + delta_list[i]*v
      B = P2 + delta_list[i]*v
      #print('flatline: ',(A,B))

      #koko = 'ROFL===D: '
      #print(koko+'{} {} {}'.format(A[0],A[1],A[2]))
      #print(koko+'{} {} {}'.format(B[0],B[1],B[2]))
      #print(koko+'Write')

      write_sequence = [A,B]
      self.GWL_voxels.append(write_sequence)

  def addLineCylinder(self, P1, P2, power, inner_radius, outer_radius, PointDistance_r, PointDistance_theta):
    # prepare some variables
    v = numpy.array(P2)-numpy.array(P1) # vector to rotate
    #print(('v=',v))
    centro = 0.5*(numpy.array(P2)+numpy.array(P1)) # center of LineCylinder
    #print(('centro=',centro))
    u = numpy.array([0,0,1]) # direction of standard TubeWithVerticalLines
    #print(('u=',u))

    theta = Angle(u,v) # angle by which to rotate
    #print(('theta=',theta))

    rotation_axis = numpy.cross(u,v) # axis around which to rotate
    #print(('rotation_axis=',rotation_axis))

    height = numpy.linalg.norm(v)
    #print(('height=',height))

    # build a basis from the P1-P2 direction
    k = v
    i = Orthogonal(k)
    j = numpy.cross(k,i)

    #print(('i=',i))
    #print(('j=',j))
    #print(('k=',k))

    i = i/numpy.linalg.norm(i)
    j = j/numpy.linalg.norm(j)
    k = k/numpy.linalg.norm(k)

    #print(('i=',i))
    #print(('j=',j))
    #print(('k=',k))

    # transformation matrix from (x,y,z) into (i,j,k)
    P = numpy.transpose(numpy.matrix([i,j,k]))
    #print(P)
    #print(P.T)
    #print(P*P.T)

    # create a vertical tube and rotate it
    tube = GWLobject()
    origin = [0,0,0]
    tube.addTubeWithVerticalLines(origin, inner_radius, outer_radius, height, power, PointDistance_r, PointDistance_theta, downwardWriting=False)
    #print(('tube.GWL_voxels=',tube.GWL_voxels))
    #tube.writeGWL('test.gwl')

    #print(P)
    #print(('centro=',centro))
    tube.applyTransformationMatrix(P, centro)
    #print(('tube.GWL_voxels=',tube.GWL_voxels))
    self.addGWLobject(tube)


    ## prepare some variables
    #v = numpy.array(P2)-numpy.array(P1) # vector to rotate
    #centro = 0.5*(numpy.array(P2)+numpy.array(P1)) # center of LineCylinder
    #u = numpy.array([0,0,1]) # direction of standard TubeWithVerticalLines
    #theta = Angle(u,v) # angle by which to rotate
    #rotation_axis = numpy.cross(u,v) # axis around which to rotate
    #height = numpy.linalg.norm(v)

    ## build a basis from the P1-P2 direction
    #i = v
    #j = Orthogonal(i)
    #k = numpy.cross(i,j)

    #i = i/numpy.linalg.norm(i)
    #j = j/numpy.linalg.norm(j)
    #k = k/numpy.linalg.norm(k)

    ## transformation matrix from (x,y,z) into (i,j,k)
    #P = numpy.transpose(numpy.matrix([i,j,k]))
    #print(P)
    #print(P.T)
    #print(P*P.T)

    ## create a vertical tube and rotate it
    #tube = GWLobject()
    #tube.addTubeWithVerticalLines(centro, inner_radius, outer_radius, height, power, PointDistance_r, PointDistance_theta, downwardWriting=False)
    #tube.applyTransformationMatrix(P.getI(), centro)
    #self.addGWLobject(tube)
    return

  def addGWLobject(self, obj):
    self.GWL_voxels += obj.GWL_voxels
    #for write_sequence in tube.GWL_voxels:
          #self.GWL_voxels.append(write_sequence)

      #for voxel in write_sequence:
        #for i in range(len(voxel)):
          #value = voxel[i] + writingOffset[i]
          #if i!=3: #coordinates
            #file_object.write( str( "%.3f" % (value) ) )
          #else: #power
            #if 0<=value and value<=100:
              #file_object.write( str( "%.3f" % (value) ) )
          ## add tab or line ending
          #if i<len(voxel)-1:
            #file_object.write('\t')
          #else:
            #file_object.write('\n')


      #self.addWrite()

    #for write_sequence in obj.GWL_voxels:
      #for voxel in write_sequence:
        #self.add

        #voxel = write_sequence[i]
        #location = [voxel[0],voxel[1],voxel[2]]
        #if len(voxel)>3:
          #power = voxel[3]
        #else:
          #power = -1
        ##point = point - centro
        #location = P.getI()*numpy.transpose(numpy.matrix(location))
        #location = centro + location
        #write_sequence[i] = [location[0],location[1],location[2],power]


  def addTubeWithVerticalLines(self, centro, inner_radius, outer_radius, height, power, PointDistance_r, PointDistance_theta, downwardWriting=True, zigzag=True):
    # counter value used to determine the writing direction: 0=down->top 1=top->down
    counter = int(downwardWriting)

    # TODO: optimize with zigzag writing
    for radius in numpy.linspace(inner_radius, outer_radius, float(1+(outer_radius - inner_radius)/PointDistance_r)):
      if radius < 0.5*PointDistance_theta:
        # TODO: power argument could probably be passed through centro?
        P = numpy.array([centro[0],centro[1],centro[2],power])
        if counter%2==1:
          self.addLine(P+0.5*height*numpy.array([0,0,1,0]),P-0.5*height*numpy.array([0,0,1,0]), power) # Downward writing
        else:
          self.addLine(P-0.5*height*numpy.array([0,0,1,0]),P+0.5*height*numpy.array([0,0,1,0]), power) # Upward writing
        if zigzag: counter+=1
      else:
        alphaStep = 2*numpy.arcsin(PointDistance_theta/float(2*radius))
        N = int(2*numpy.pi/alphaStep)
        for i in range(N):
          P = numpy.array([centro[0]+radius*numpy.cos(i*2*numpy.pi/float(N)),centro[1]+radius*numpy.sin(i*2*numpy.pi/float(N)),centro[2],power])
          if counter%2==1:
            self.addLine(P+0.5*height*numpy.array([0,0,1,0]),P-0.5*height*numpy.array([0,0,1,0]), power) # Downward writing
          else:
            self.addLine(P-0.5*height*numpy.array([0,0,1,0]),P+0.5*height*numpy.array([0,0,1,0]), power) # Upward writing
          if zigzag: counter+=1
    return

  def rotate(self, axis_point, axis_direction, angle_degrees):
    #print('@@@@@@@@@@@@@@@@@@@@@@')
    M = TransformationMatrix.rotationMatrix(axis_point, axis_direction, angle_degrees)
    for write_sequence in self.GWL_voxels:
      for i in range(len(write_sequence)):
        #print('@@@@@@@@@@@@@@@@@@@@@@')
        write_sequence[i] = TransformationMatrix.applyTransformation(M,write_sequence[i])
    return

  # TODO: Use better names/transformation system to implement translations
  def applyTransformationMatrix(self, P, centro):
    for write_sequence in self.GWL_voxels:
      for i in range(len(write_sequence)):
        voxel = write_sequence[i]
        #print(voxel)
        location = [voxel[0],voxel[1],voxel[2]]
        if len(voxel)>3:
          power = voxel[3]
        else:
          power = -1
        #point = point - centro
        location = P*numpy.transpose(numpy.matrix(location))
        location = numpy.asarray(location).reshape(-1) #numpy.array(numpy.transpose(M))[0]
        location = centro + location
        #print(('location=',location))
        write_sequence[i] = [location[0],location[1],location[2],power]
    return

  def addHorizontalGrating(self, P1, P2, LineNumber, LineDistance):
    u = numpy.array(P2)-numpy.array(P1)
    u = u*1.0/numpy.sqrt(pow(u[0],2)+pow(u[1],2)+pow(u[2],2))
    v = numpy.array([-u[1],u[0],0])
    L = (LineNumber-1)*LineDistance
    P1_min = P1 - 0.5*L*v

    plist = []
    for k in range(LineNumber):
        A = P1_min + k*LineDistance*v
        B = A + (P2-P1)
        plist.append((A,B))

    counter = 0
    for (A,B) in plist:
      if counter%2 == 0:
        self.GWL_voxels.append([A,B])
      else:
        self.GWL_voxels.append([B,A])
      counter = counter + 1

  def addZGrating(self, P1, P2, LineNumber, LineDistance, BottomToTop = False):
    Zcenter = 0.5*(P1[2] + P2[2])
    zlist = []
    L = (LineNumber-1)*LineDistance
    if BottomToTop:
      zlist = numpy.linspace(Zcenter-0.5*L, Zcenter+0.5*L, LineNumber)
    else:
      zlist = numpy.linspace(Zcenter+0.5*L, Zcenter-0.5*L, LineNumber)
    #if LineNumber%2: #odd LineNumber
      #zlist = numpy.linspace(Zcenter-0.5*L, Zcenter+0.5*L, LineNumber)
    #else: #even LineNumber
      #zlist = numpy.arange(Zcenter-LineNumber/2*LineDistance, Zcenter+((LineNumber-1)/2+1)*LineDistance, LineDistance)
    counter = 0
    for z in zlist:
      A = [P1[0],P1[1],z]
      B = [P2[0],P2[1],z]
      if counter%2 == 0:
        self.GWL_voxels.append([A,B])
      else:
        self.GWL_voxels.append([B,A])
      counter = counter + 1

  def addBlockCentroSize(self, centro, size, LineDistance_Horizontal=DEFAULT_VOXEL_WIDTH, LineDistance_Vertical=DEFAULT_VOXEL_HEIGHT, BottomToTop = False, direction=None):
    centro = numpy.array(centro)
    size = numpy.array(size)
    lower = centro - 0.5*size
    upper = centro + 0.5*size
    self.addBlockLowerUpper(lower, upper, LineDistance_Horizontal, LineDistance_Vertical, BottomToTop, direction)

  ## TODO: API: Was it a good idea to specify the other blocks in terms of LineNumber* in the first place?
  def addBlockLowerUpper(self, lower, upper, LineDistance_Horizontal=DEFAULT_VOXEL_WIDTH, LineDistance_Vertical=DEFAULT_VOXEL_HEIGHT, BottomToTop = False, direction=None):
    (lower,upper) = fixLowerUpper(lower,upper)
    #print(lower)
    #print(upper)
    dim = [ abs(upper[i]-lower[i]) for i in [0,1,2] ]
    #print(dim)

    # TODO: will fix later
    #self.addXblock(lower, upper, LineDistance_Horizontal=LineDistance_Horizontal, LineDistance_Vertical=LineDistance_Vertical, BottomToTop=BottomToTop)

    if direction is None:
      if dim[0]>=dim[1] and dim[0]>=dim[2]:
        direction = 'X'
      elif dim[1]>=dim[0] and dim[1]>=dim[2]:
        direction = 'Y'
      else: #dim[2]>=dim[0] and dim[2]>=dim[1]:
        direction = 'Z'

    if direction == 'X':
      self.addXblock(lower, upper, LineDistance_Horizontal=LineDistance_Horizontal, LineDistance_Vertical=LineDistance_Vertical, BottomToTop=BottomToTop)
    elif direction == 'Y':
      self.addYblock(lower, upper, LineDistance_Horizontal=LineDistance_Horizontal, LineDistance_Vertical=LineDistance_Vertical, BottomToTop=BottomToTop)
    elif direction == 'Z':
      self.addZblock(lower, upper, LineDistance_X=LineDistance_Horizontal, LineDistance_Y=LineDistance_Horizontal)
    else:
      raise Exception("ERROR: Invalid direction. Should be 'X','Y' or 'Z'")

  def addXblock(self, P1, P2, LineNumber_Horizontal = None, LineDistance_Horizontal = DEFAULT_VOXEL_WIDTH, LineNumber_Vertical = None, LineDistance_Vertical = DEFAULT_VOXEL_HEIGHT, BottomToTop = False):

    # TODO: Should use calculateNvoxelsAndInterVoxelDistance()? And overlap? -> Other block functions should require overlap/linenumber args?
    if LineNumber_Horizontal is None: LineNumber_Horizontal = math.floor( (abs(P2[1]-P1[1])/LineDistance_Horizontal) + 1 )
    if LineNumber_Vertical is None: LineNumber_Vertical = math.floor( (abs(P2[2]-P1[2])/LineDistance_Vertical) + 1 )

    Xcenter = 0.5*(P1[0] + P2[0])
    Ycenter = 0.5*(P1[1] + P2[1])
    Zcenter = 0.5*(P1[2] + P2[2])
    #print Zcenter
    #print LineNumber_Vertical

    ylist = []
    L = (LineNumber_Horizontal-1)*LineDistance_Horizontal
    ylist = numpy.linspace(Ycenter-0.5*L, Ycenter+0.5*L, LineNumber_Horizontal)

    zlist = []
    L = (LineNumber_Vertical-1)*LineDistance_Vertical
    if BottomToTop:
      zlist = numpy.linspace(Zcenter-0.5*L, Zcenter+0.5*L, LineNumber_Vertical)
    else:
      zlist = numpy.linspace(Zcenter+0.5*L, Zcenter-0.5*L, LineNumber_Vertical)

    counter = 0
    for z in zlist:
      for y in ylist:
        A = [P1[0],y,z]
        B = [P2[0],y,z]
        if counter%2 == 0:
          self.GWL_voxels.append([A,B])
        else:
          self.GWL_voxels.append([B,A])
        counter = counter + 1

  def addYblock(self, P1, P2, LineNumber_Horizontal = None, LineDistance_Horizontal = DEFAULT_VOXEL_WIDTH, LineNumber_Vertical = None, LineDistance_Vertical = DEFAULT_VOXEL_HEIGHT, BottomToTop = False):

    if LineNumber_Horizontal is None: LineNumber_Horizontal = math.floor( (abs(P2[0]-P1[0])/LineDistance_Horizontal) + 1 )
    if LineNumber_Vertical is None: LineNumber_Vertical = math.floor( (abs(P2[2]-P1[2])/LineDistance_Vertical) + 1 )

    Xcenter = 0.5*(P1[0] + P2[0])
    Ycenter = 0.5*(P1[1] + P2[1])
    Zcenter = 0.5*(P1[2] + P2[2])

    xlist = []
    L = (LineNumber_Horizontal-1)*LineDistance_Horizontal
    xlist = numpy.linspace(Xcenter-0.5*L, Xcenter+0.5*L, LineNumber_Horizontal)

    zlist = []
    L = (LineNumber_Vertical-1)*LineDistance_Vertical
    if BottomToTop:
      zlist = numpy.linspace(Zcenter-0.5*L, Zcenter+0.5*L, LineNumber_Vertical)
    else:
      zlist = numpy.linspace(Zcenter+0.5*L, Zcenter-0.5*L, LineNumber_Vertical)

    counter = 0
    for z in zlist:
      for x in xlist:
        A = [x,P1[1],z]
        B = [x,P2[1],z]
        if counter%2 == 0:
          self.GWL_voxels.append([A,B])
        else:
          self.GWL_voxels.append([B,A])
        counter = counter + 1

  # TODO: API improvement: use P1,P2 to specify BottomToTop? Leave in BottomToTop? Pass just x, y or z coordinates instead of [x,y,z]? X,Y,Z functions should be more or less the same if possible.
  def addZblock(self, P1, P2, LineNumber_X = None, LineDistance_X = DEFAULT_VOXEL_WIDTH, LineNumber_Y = None, LineDistance_Y = DEFAULT_VOXEL_WIDTH):

    if LineNumber_X is None: LineNumber_X = math.floor( (abs(P2[0]-P1[0])/LineDistance_X) + 1 )
    if LineNumber_Y is None: LineNumber_Y = math.floor( (abs(P2[1]-P1[1])/LineDistance_Y) + 1 )

    Xcenter = 0.5*(P1[0] + P2[0])
    Ycenter = 0.5*(P1[1] + P2[1])
    Zcenter = 0.5*(P1[2] + P2[2])

    xlist = []
    L = (LineNumber_X-1)*LineDistance_X
    xlist = numpy.linspace(Xcenter-0.5*L, Xcenter+0.5*L, LineNumber_X)

    ylist = []
    L = (LineNumber_Y-1)*LineDistance_Y
    ylist = numpy.linspace(Ycenter-0.5*L, Ycenter+0.5*L, LineNumber_Y)

    counter = 0
    for y in ylist:
      for x in xlist:
        A = [x,y,P1[2]]
        B = [x,y,P2[2]]
        if counter%2 == 0:
          self.GWL_voxels.append([A,B])
        else:
          self.GWL_voxels.append([B,A])
        counter = counter + 1

  # TODO: Improve by just passing a min/max PointDistance and choosing the distance so that it gives a nice integer number of points to fit the desired circle arc?
  # TODO: different functions for this? func options?
  def addHorizontalCircle(self, center, radius, power, PointDistance_max, startAngle=0, endAngle=2*numpy.pi, closed_loop=False):
    write_sequence = []
    if radius < 0.5*PointDistance_max:
      write_sequence.append(center)
    else:
      alphaStep_max = 2*numpy.arcsin(PointDistance_max/(2*radius))
      angleRange = abs(endAngle-startAngle)
      Npoints_min = int(ceil( angleRange/alphaStep_max + 1 ))
      alphaStep = angleRange/(Npoints_min-1)
      if closed_loop:
        N = Npoints_min
      else:
        N = Npoints_min - 1
      for i in range(N):
        currentAngle = startAngle + i*alphaStep
        if 0<=power and power<=100:
          P = [center[0]+radius*numpy.cos(currentAngle), center[1]+radius*numpy.sin(currentAngle), center[2],power]
        else:
          P = [center[0]+radius*numpy.cos(currentAngle), center[1]+radius*numpy.sin(currentAngle), center[2]]
        write_sequence.append(P)
    self.GWL_voxels.append(write_sequence)

  def addHorizontalDisk(self, center, radius, power, PointDistance):
    N = int(radius/float(PointDistance))
    #print(('N = ',N))
    for i in range(N+1):
      if i==0:
        self.addHorizontalCircle(center, 0, power, PointDistance)
        ##print center
        #self.GWL_voxels.append([center])
      else:
        self.addHorizontalCircle(center, i*radius/float(N), power, PointDistance)

  def addSphere(self, center, radius, power, HorizontalPointDistance, VerticalPointDistance, solid = False):

    PointDistance = numpy.sqrt(pow(HorizontalPointDistance,2)+pow(VerticalPointDistance,2))
    #print PointDistance
    if radius == 0:
      self.GWL_voxels.append([center])
    else:
      alphaStep = 2*numpy.arcsin(PointDistance/float(2*radius))
      N = int(0.5*numpy.pi/alphaStep)
      zlist = []
      for i in range(N+1):
        #print(('i = ',i,' N = ',N))
        z = radius*numpy.cos(i*0.5*numpy.pi/float(N))
        zlist.append(z)

      # symetrify list
      zlist = zlist + [ -i for i in zlist[len(zlist)-2::-1] ]

      for z in sorted(zlist, reverse=True):
        local_radius = numpy.sqrt(pow(radius,2)-pow(z,2))
        #print(('local_radius 1 = ',local_radius))
        #local_radius = radius*numpy.sin(i*numpy.pi/float(N))
        #print(('local_radius 2 = ',local_radius))
        if solid:
          self.addHorizontalDisk([center[0],center[1],center[2]+z], local_radius, power, HorizontalPointDistance)
        else:
          self.addHorizontalCircle([center[0],center[1],center[2]+z], local_radius, power, HorizontalPointDistance)

    #N = int(radius/float(VerticalPointDistance))
    #for i in range(-N,N+1):
      #z = i*radius/float(N)
      #local_radius = numpy.sqrt(pow(radius,2)-pow(z,2))
      ##print 'local_radius = ', local_radius
      #if solid:
        #self.addHorizontalDisk([center[0],center[1],center[2]+z], local_radius, power, HorizontalPointDistance)
      #else:
        #self.addHorizontalCircle([center[0],center[1],center[2]+z], local_radius, power, HorizontalPointDistance)

  def startNewVoxelSequence(self):
    '''
    Starts a new voxel sequence, i.e. "adds a Write command" if you already had a "voxel sequence" before it when creating the .gwl file.
    '''
    write_sequence = []
    self.GWL_voxels.append(write_sequence)
    return

  # Completely disabling deprecated function, but leaving warning syntax as example.
  #def addWrite(self):
    #'''
    #DEPRECATED: Replaced by :py:func:`startNewVoxelSequence`.
    #'''
    #warnings.warn('DEPRECATED: addWrite() has been replaced by startNewVoxelSequence().', DeprecationWarning)
    #raise
    #return

  def addVoxel(self, voxel):
    '''
    Adds a voxel to the last "writing sequence". If there is none, a new one will be created.
    Equivalent to adding a line of the form "x y z [power]" in your .gwl file.
    '''

    if len(self.GWL_voxels)>0:
      self.GWL_voxels[-1].append(voxel)
    else:
      self.GWL_voxels.append([voxel])

    # update min/max values
    for i in range(len(voxel)):
      if voxel[i] < self.PositionMinimum[i]:
        self.PositionMinimum[i] = voxel[i]
      if self.PositionMaximum[i] < voxel[i]:
        self.PositionMaximum[i] = voxel[i]
    
    return

  def readSubstitutes(self, subsFile):
    print(('Reading substitution pairs from '+subsFile))
    self.path_substitutes = []
    try:
      with open(subsFile, 'r') as file_object:
        for line in file_object:
          t = line.strip().split('->')
          if len(t)==2:
            old = t[0].strip()
            new = t[1].strip()
            old = old.replace('\\',os.path.sep).replace('/',os.path.sep)
            new = new.replace('\\',os.path.sep).replace('/',os.path.sep)
            print((old+' -> '+new))
            self.path_substitutes.append((old,new))
    #TODO: reimplement nice exception system
    #except IOError as (errno, strerror):
    except:
      #print "I/O error({0}): {1}".format(errno, strerror)
      msg = 'Failed to open {}\n'.format(subsFile)
      sys.stderr.write(msg)
      raise
      # raise Exception(msg)

    return self.path_substitutes

  def readGWL(self, filename):
    Nvoxels = 0
    write_sequence = []
    try:
      with open(filename, 'r') as file_object:
        try:
          for line in file_object:
            #print line
            line_stripped = line.strip()
            # TODO: handle comments and other commands
            if len(line_stripped)>0 and line_stripped[0]!='%':
              #print 'pre-split: ', line_stripped
              #cmd = re.split('[^a-zA-Z0-9_+-.]+',line_stripped)
              #cmd = re.split('[^a-zA-Z0-9_+-.:\\/]+',line_stripped)
              #cmd = re.split('[ \t]',line_stripped)
              cmd = re.split('\s+',line_stripped)
              #cmd = [ i.lower() for i in cmd ]
              #print 'post-split: ', cmd
              stopRepeat = True
              for i in range(self.Repeat):
                if re.match(r"[a-zA-Z]",cmd[0][0]) or cmd[0]=='-999' or cmd[0].lower()=='-999.000':
                  if cmd[0].lower()=='-999' or cmd[0].lower()=='-999.000':
                    #print('match 999')
                    if cmd[1]=='-999' or cmd[1].lower()=='-999.000':
                      self.GWL_voxels.append(write_sequence)
                      write_sequence = []
                      self.writingTimeInSeconds = self.writingTimeInSeconds + 1e-3*self.DwellTime
                      self.maxDistanceBetweenLines = self.ScanSpeed*1e-3*self.DwellTime
                  else:
                    #print('other match')
                    if cmd[0].lower()=='write':
                      self.GWL_voxels.append(write_sequence)
                      write_sequence = []
                      self.writingTimeInSeconds = self.writingTimeInSeconds + 1e-3*self.DwellTime
                      self.maxDistanceBetweenLines = self.ScanSpeed*1e-3*self.DwellTime
                    elif cmd[0].lower()=='include':
                      print(('line_stripped = ' + line_stripped))
                      file_to_include = re.split('\s+',line_stripped,1)[1]
                      print(('including file_to_include = ' + file_to_include))
                      print('Fixing file separators')
                      file_to_include = file_to_include.replace('\\',os.path.sep).replace('/',os.path.sep)
                      print(('including file_to_include = ' + file_to_include))
                      file_to_include_fullpath = os.path.normpath(os.path.join(os.path.dirname(filename), os.path.expanduser(file_to_include)))
                      print(file_to_include_fullpath)
                      if not os.path.isfile(file_to_include_fullpath):
                        print('WARNING: File not found. Attempting path substitutions')
                        for (old,new) in self.path_substitutes:
                          file_to_try = file_to_include.replace(old,new)
                          #print('file_to_try = ',file_to_try)
                          #print('filename = ',filename)
                          #print('os.path.dirname(filename) = ',os.path.dirname(filename))
                          file_to_try = os.path.normpath(os.path.join(os.path.dirname(filename), os.path.expanduser(file_to_try)))
                          if self.verbosity > 10:
                            print(('old = ' + old))
                            print(('new = ' + new))
                            print(('file_to_include = ' + file_to_include))
                            print(('filename = ' + filename))
                          print(('Trying file_to_try = ' + file_to_try))
                          if os.path.isfile(file_to_try):
                            file_to_include_fullpath = file_to_try
                            break
                      self.readGWL(file_to_include_fullpath)

                    elif cmd[0].lower()=='movestagex':
                      print(('Moving X by '+cmd[1]))
                      try:
                        self.stage_position[0] = self.stage_position[0] + float(cmd[1])
                      except ValueError as e:
                        warnings.warn('{}'.format(e))
                    elif cmd[0].lower()=='movestagey':
                      print(('Moving Y by '+cmd[1]))
                      try:
                        self.stage_position[1] = self.stage_position[1] + float(cmd[1])
                      except ValueError as e:
                        warnings.warn('{}'.format(e))

                    elif cmd[0].lower()=='addxoffset':
                      print('Adding X offset of '+cmd[1])
                      self.voxel_offset[0] = self.voxel_offset[0] + float(cmd[1])
                    elif cmd[0].lower()=='addyoffset':
                      print('Adding Y offset of '+cmd[1])
                      self.voxel_offset[1] = self.voxel_offset[1] + float(cmd[1])
                    elif cmd[0].lower()=='addzoffset':
                      print('Adding Z offset of '+cmd[1])
                      self.voxel_offset[2] = self.voxel_offset[2] + float(cmd[1])

                    elif cmd[0].lower()=='xoffset':
                      print('Setting X offset to '+cmd[1])
                      self.voxel_offset[0] = float(cmd[1])
                    elif cmd[0].lower()=='yoffset':
                      print('Setting Y offset to '+cmd[1])
                      self.voxel_offset[1] = float(cmd[1])
                    elif cmd[0].lower()=='zoffset':
                      print('Setting Z offset to '+cmd[1])
                      self.voxel_offset[2] = float(cmd[1])

                    elif cmd[0].lower()=='linenumber':
                      print('Setting LineNumber to '+cmd[1])
                      self.LineNumber = float(cmd[1])
                    elif cmd[0].lower()=='linedistance':
                      print('Setting LineDistance to '+cmd[1])
                      self.LineDistance = float(cmd[1])
                    elif cmd[0].lower()=='powerscaling':
                      print('Setting PowerScaling to '+cmd[1])
                      self.PowerScaling = float(cmd[1])
                    elif cmd[0].lower()=='laserpower':
                      if self.verbosity > 5:
                        print('Setting LaserPower to '+cmd[1])
                      self.LaserPower = float(cmd[1])
                    elif cmd[0].lower()=='scanspeed':
                      print('Setting ScanSpeed to '+cmd[1])
                      try:
                        self.ScanSpeed = float(cmd[1])
                      except:
                        sys.stderr.write('Failed to do something...\n') # .. todo:: check var type before and later implement a real parser...

                    elif cmd[0].lower()=='repeat':
                      print('Repeating next command '+cmd[1]+' times.')
                      self.Repeat = int(cmd[1])
                      stopRepeat = False

                    #elif cmd[0].lower()=='defocusfactor':
                      #print 'defocusfactor'

                    elif cmd[0].lower()=='findinterfaceat':
                      print('Setting FindInterfaceAt to '+cmd[1])
                      try:
                        self.FindInterfaceAt = [0,0,float(cmd[1]),0]
                      except ValueError as e:
                        warnings.warn('{}'.format(e))

                    elif cmd[0].lower()=='dwelltime':
                      print('Setting DwellTime to '+cmd[1])
                      self.DwellTime = float(cmd[1])


                    else:
                      print(('UNKNOWN COMMAND: '+cmd[0]))
                      #sys.exit(-1)
                else:
                  #print '=>VOXEL'
                  voxel = []
                  for i in range(len(cmd)):
                    piezo_position = float(cmd[i]) + self.voxel_offset[i]
                    if piezo_position<0 or piezo_position>300:
                      if not self.out_of_range:
                        errmsg = 'ERROR: voxel out of range! len(voxel) = '+str(len(voxel))+' piezo_position = '+str(piezo_position)+' i = '+str(i)+'\n'
                        errmsg += 'piezo_position = float(cmd[i]) + self.voxel_offset[i]'+'\n'
                        errmsg += str(piezo_position)+' = '+str(float(cmd[i]))+' + '+str(self.voxel_offset[i])+'\n'
                        errmsg += 'filename = '+str(filename)+'\n'
                        errmsg += 'cmd = '+str(cmd)
                        sys.stderr.write(errmsg+'\n')
                        self.out_of_range = True

                    voxel.append( piezo_position + self.stage_position[i] - self.FindInterfaceAt[i] )
                  #voxel = [ float(i) for i in cmd ]
                  (last_voxel,found_last_voxel) = self.getLastVoxel()
                  write_sequence.append(voxel)
                  if len(write_sequence)>=2:
                      a = write_sequence[-2][0:3]
                      b = write_sequence[-1][0:3]
                      newDist = numpy.linalg.norm(numpy.array(b)-numpy.array(a))
                      newTime = newDist/self.ScanSpeed
                      self.writingTimeInSeconds = self.writingTimeInSeconds + newTime
                      self.writingDistanceInMum = self.writingDistanceInMum + newDist
                  elif found_last_voxel:
                      a = last_voxel[0:3]
                      b = write_sequence[-1][0:3]
                      newDist = numpy.linalg.norm(numpy.array(b)-numpy.array(a))
                      newTime = newDist/self.ScanSpeed
                      self.writingTimeInSeconds = self.writingTimeInSeconds + newTime
                      self.writingDistanceInMum = self.writingDistanceInMum + newDist

                  Nvoxels = Nvoxels + 1

              # reset repeat
              if stopRepeat:
                  self.Repeat = 1
        except UnicodeDecodeError as err:
          warnings.warn('{}'.format(err)) 
    except IOError as xxx_todo_changeme:
      (errno, strerror) = xxx_todo_changeme.args
      print("I/O error({0}): {1}".format(errno, strerror))
      print('Failed to open '+filename)
      raise

    print(('Nvoxels = '+str(Nvoxels)))
    if self.verbosity >= 0:
      print(('self.writingTimeInSeconds = '+str(self.writingTimeInSeconds)))
      print(('self.writingTimeInMinutes = '+str(self.writingTimeInSeconds/60.)))
      print(('self.writingTimeInHours = '+str(self.writingTimeInSeconds/(60.*60.))))
      print(('self.writingDistanceInMum = '+str(self.writingDistanceInMum)))
    #return GWL_voxels
    return

  def writeGWL(self, filename, writingOffset = [0,0,0,0], bool_LaserPowerCommand = False):
    '''
    Writes out the GWL file.
    This function is old and does not use the new power compensation attributes.
    
    See also: :py:func:`writeGWLWithPowerCompensation`
    '''

    print('GWLobject.writeGWL')

    print(('Writing GWL to '+filename))

    lastPower = None

    with open(filename, 'w') as file_object:
      for write_sequence in self.GWL_voxels:
        for voxel in write_sequence:

          # TODO: add options to enable/disable warnings for coords/power out of range or invalid voxel sizes
          # TODO: Make voxels always have 4 coordinates and set 4th to None if undesired? Should make things easier... (but take up more RAM)
          # TODO: rewrite this with single-line write commands instead of complex for loops... (unless we expect voxels with arbitrary lengths)

          #lastPower = writeVoxel(f, voxel, laser_power_at_z0, K, interfaceAt, bool_LaserPowerCommand, lastPower)

          if len(voxel)>3:
            power = voxel[3] + writingOffset[3]
          else:
            power = None

          if bool_LaserPowerCommand and power != lastPower:
            file_object.write("LaserPower %.3f\n" % power)

          ## only for standard voxels (length 3 or 4)
          #if len(voxel)>4:
            #print('ERROR: voxel with more than 4 parameters',file=stderr)
            #sys.exit(-1)
          #print(voxel)
          #print(range(len(voxel)))
          for i in range(len(voxel)):
            value = voxel[i] + writingOffset[i]
            if i!=3: #coordinates
              #print('COORD')
              file_object.write( str( "%.3f" % (value) ) )
            else: #power
              #print('POWER')
              if not bool_LaserPowerCommand:
                if 0<=value and value<=100:
                  file_object.write( str( "%.3f" % (value) ) )
            # add tab or line ending
            if i<len(voxel)-1:
              file_object.write('\t')
            else:
              file_object.write('\n')

          lastPower = power

          ## general method for voxels of any length
          #for i in range(len(voxel)):
            #file_object.write( str( "%.3f" % (voxel[i] + writingOffset[i]) ) )
            #if i<len(voxel)-1:
              #file_object.write('\t')
            #else:
              #file_object.write('\n')

        file_object.write('Write\n')

  def writeGWLWithPowerCompensation(self, filename):
    '''
    Writes out the GWL file, but using the GWLobject's attributes related to power compensation.
    
    .. note:: The latest Nanowrite software supports new commands allowing easy changes to the power compensation (power slope, etc).
              Please test and use those instead. If they work, it will make functions like this one mostly obsolete.
              The new GWL commands are: psPowerProfile, psLoadPowerProfiles, psPowerSlope
              
              Example::
              
                FindInterfaceAt 0.5
                PowerScaling 1.5
                LaserPower 3
                psPowerSlope 2
                0 0 0
                0 0 10
                Write

              This should be equivalent to the old::

                0 0 0 3
                0 0 10 90.0 % = 3 * 1 * (1 + 2*(z-0.5))*1.5
                Write

              The formula used is::
              
                LPeff = LaserPower * eta(|nu|) * mu(z)
                
              with::
              
                eta(|nu|) = 1
                mu(z) = (1 + psPowerSlope*(z-FindInterfaceAt))*PowerScaling

    .. todo:: write power coords if they exist, even if self.write_power is False. This will allow local power specifications, even if Z-based power compensation is used. Maybe add another attribute/function to write voxels without power. relative powers could also be used to combine them with power compensation. (although the PowerScaling command exists exactly for this purpose, so no real need for that)
    .. todo:: X/Y-based power compensation? Not really necessary... But if the *User* wants flexibility, his own power compensation function (now that's more useful), etc...
    '''
    print('GWLobject.writeGWLWithPowerCompensation')
    print(('Writing GWL to '+filename))
    
    last_power = None

    with open(filename, 'w') as file_object:

      if self.reverse_line_order_on_write:
        GWL_voxels_iterator = reversed(self.GWL_voxels)
      else:
        GWL_voxels_iterator = self.GWL_voxels
         
      for write_sequence in GWL_voxels_iterator:

        if self.reverse_voxel_order_per_line_on_write:
          write_sequence_iterator = reversed(write_sequence)
        else:
          write_sequence_iterator = write_sequence

        for voxel in write_sequence_iterator:
          x = voxel[0]
          y = voxel[1]
          z = voxel[2]
          if self.set_lower_to_origin:
            x = x - self.PositionMinimum[0]
            y = y - self.PositionMinimum[1]
            z = z - self.PositionMinimum[2]
          
          if not self.write_power:
            file_object.write('{:.3f}\t{:.3f}\t{:.3f}\n'.format(x,y,z))
          else:
            power = self.getPower(z)
            if not self.PC_bool_LaserPowerCommand:
              file_object.write('{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\n'.format(x,y,z,power))
            else:
              if power != last_power:
                file_object.write("LaserPower {:.3f}\n".format(power))
              file_object.write('{:.3f}\t{:.3f}\t{:.3f}\n'.format(x,y,z))
          
            last_power = power

        file_object.write('Write\n')
    return

def test1():
  #GWL_obj = GWLobject()
  #GWL_obj.readGWL(sys.argv[1])
  ##print GWL_obj.GWL_voxels
  #GWL_obj.writeGWL('copy.gwl')

  GWL_obj = GWLobject()
  GWL_obj.addXblock([0,0,0],[1,0,0],2,0.050,3,0.100)
  GWL_obj.addXblock([0,0,1.5],[1,0,1.5],2,0.050,3,0.100)
  GWL_obj.addXblock([0,0,2.75],[1,0,2.75],2,0.050,3,0.100)
  z = 7.1038825; GWL_obj.addXblock([0,0,z],[1,0,z],2,0.050,3,0.100)

  power = 75

  center = [0,0,3]
  HorizontalPointDistance = 0.050
  VerticalPointDistance = 0.100
  radius = 1

  #print 'addHorizontalCircle'
  GWL_obj.addHorizontalCircle(center, radius, power, HorizontalPointDistance)
  #print 'addHorizontalDisk'
  GWL_obj.addHorizontalDisk([center[0],center[1],center[2]+1], radius, power, HorizontalPointDistance)
  #print 'addSphere non-solid'
  GWL_obj.addSphere([center[0],center[1],center[2]+1+11], radius, power, HorizontalPointDistance, VerticalPointDistance, False)
  #print 'addSphere solid'
  GWL_obj.addSphere([center[0],center[1],center[2]+1+22], radius, power, HorizontalPointDistance, VerticalPointDistance, True)

  HorizontalPointDistance = 0.100
  VerticalPointDistance = 0.200
  center = [10,0,3]
  radius = 2
  GWL_obj.addHorizontalCircle(center, radius, power, HorizontalPointDistance)
  GWL_obj.addHorizontalDisk([center[0],center[1],center[2]+1], radius, power, HorizontalPointDistance)
  GWL_obj.addSphere([center[0],center[1],center[2]+1+11], radius, power, HorizontalPointDistance, VerticalPointDistance, False)
  GWL_obj.addSphere([center[0],center[1],center[2]+1+22], radius, power, HorizontalPointDistance, VerticalPointDistance, True)

  HorizontalPointDistance = 1
  VerticalPointDistance = 0.5
  center = [30,0,3]
  radius = 3
  GWL_obj.addHorizontalCircle(center, radius, power, HorizontalPointDistance)
  GWL_obj.addHorizontalDisk([center[0],center[1],center[2]+1], radius, power, HorizontalPointDistance)
  GWL_obj.addSphere([center[0],center[1],center[2]+1+11], radius, power, HorizontalPointDistance, VerticalPointDistance, False)
  GWL_obj.addSphere([center[0],center[1],center[2]+1+22], radius, power, HorizontalPointDistance, VerticalPointDistance, True)

  HorizontalPointDistance = 1
  VerticalPointDistance = 1
  center = [40,0,3]
  radius = 3
  GWL_obj.addHorizontalCircle(center, radius, power, HorizontalPointDistance)
  GWL_obj.addHorizontalDisk([center[0],center[1],center[2]+1], radius, power, HorizontalPointDistance)
  GWL_obj.addSphere([center[0],center[1],center[2]+1+11], radius, power, HorizontalPointDistance, VerticalPointDistance, False)
  GWL_obj.addSphere([center[0],center[1],center[2]+1+22], radius, power, HorizontalPointDistance, VerticalPointDistance, True)

  HorizontalPointDistance = 1
  VerticalPointDistance = 2
  center = [50,0,3]
  radius = 3
  GWL_obj.addHorizontalCircle(center, radius, power, HorizontalPointDistance)
  GWL_obj.addHorizontalDisk([center[0],center[1],center[2]+1], radius, power, HorizontalPointDistance)
  GWL_obj.addSphere([center[0],center[1],center[2]+1+11], radius, power, HorizontalPointDistance, VerticalPointDistance, False)
  GWL_obj.addSphere([center[0],center[1],center[2]+1+22], radius, power, HorizontalPointDistance, VerticalPointDistance, True)

  print('300')
  HorizontalPointDistance = 0.050
  VerticalPointDistance = 0.100
  center = [60,0,3]
  radius = 0.5*0.300
  GWL_obj.addHorizontalCircle(center, radius, power, HorizontalPointDistance)
  GWL_obj.addHorizontalDisk([center[0],center[1],center[2]+1], radius, power, HorizontalPointDistance)
  GWL_obj.addSphere([center[0],center[1],center[2]+1+11], radius, power, HorizontalPointDistance, VerticalPointDistance, False)
  GWL_obj.addSphere([center[0],center[1],center[2]+1+22], radius, power, HorizontalPointDistance, VerticalPointDistance, True)

  print('350')
  center = [70,0,3]
  radius = 0.5*0.350
  GWL_obj.addHorizontalCircle(center, radius, power, HorizontalPointDistance)
  GWL_obj.addHorizontalDisk([center[0],center[1],center[2]+1], radius, power, HorizontalPointDistance)
  GWL_obj.addSphere([center[0],center[1],center[2]+1+11], radius, power, HorizontalPointDistance, VerticalPointDistance, False)
  GWL_obj.addSphere([center[0],center[1],center[2]+1+22], radius, power, HorizontalPointDistance, VerticalPointDistance, True)

  print('400')
  center = [80,0,3]
  radius = 0.5*0.400
  GWL_obj.addHorizontalCircle(center, radius, power, HorizontalPointDistance)
  GWL_obj.addHorizontalDisk([center[0],center[1],center[2]+1], radius, power, HorizontalPointDistance)
  GWL_obj.addSphere([center[0],center[1],center[2]+1+11], radius, power, HorizontalPointDistance, VerticalPointDistance, False)
  GWL_obj.addSphere([center[0],center[1],center[2]+1+22], radius, power, HorizontalPointDistance, VerticalPointDistance, True)


  GWL_obj.writeGWL('xblock.gwl')

  GWL_obj.clear()
  GWL_obj.addXblock([0,0,2.75],[10,0,2.75],5,0.050,8,0.100)
  GWL_obj.addYblock([1,0,2.75],[1,20,2.75],5,0.050,8,0.100)
  GWL_obj.writeGWL('xblock2.gwl')

def test2():
  obj = GWLobject()

  N=5

  for i in range(N):
    obj.addVoxel([i,0,0])
  obj.startNewVoxelSequence()

  for i in range(N):
    obj.addVoxel([0,i,0])
  obj.startNewVoxelSequence()

  for i in range(N):
    obj.addVoxel([0,0,i])
  obj.startNewVoxelSequence()

  for i in range(N):
    obj.addVoxel([-i,0,0])
  obj.startNewVoxelSequence()

  for i in range(N):
    obj.addVoxel([0,-i,0])
  obj.startNewVoxelSequence()

  for i in range(N):
    obj.addVoxel([0,0,-i])
  obj.startNewVoxelSequence()

  obj.set_lower_to_origin = True
  obj.write_power = True
  obj.PC_laser_power_at_z0 = 1
  obj.PC_slope = 0.1
  obj.PC_interfaceAt = 1
  obj.PC_float_height = 1
  obj.PC_bool_InverseWriting = True
  obj.PC_bool_LaserPowerCommand = False

  
  obj.writeGWLWithPowerCompensation(os.path.join(tempfile.gettempdir(), 'test2.gwl'))
  return

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile')
  parser.add_argument('-W', '--just-warn', action='store_true', help='Continue in case of warnings. (The default is to raise it as an error.)')
  parser.add_argument('-v', '--verbose', action="count", dest="verbosity", default=0, help='verbosity level')
  args = parser.parse_args()
  print(args)
  
  if args.just_warn:
    warnings.simplefilter("default")
  else:
    warnings.simplefilter("error")
  
  obj = GWLobject()
  obj.readGWL(args.infile)

  return 0


if __name__ == "__main__":
  # .. todo:: Add tests to test suite
  # test1()
  # test2()
  main()
