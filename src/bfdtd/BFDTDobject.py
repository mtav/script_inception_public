#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import math
import numpy
import tempfile
import warnings
import configparser

from numpy.linalg import norm
from numpy import array, rad2deg, cross, dot, sqrt, ceil, floor

import photonics.utilities as utilities
from photonics.utilities.common import *
import photonics.utilities.brisFDTD_ID_info
from photonics.meshing.meshing import subGridMultiLayer

from photonics.constants.physcon import get_c0, get_e, get_eV, get_epsilon0, get_mu0, get_h, get_h_eVs, get_hb, get_me

from .BFDTDentry import BFDTDentry
from .excitation import *
from .meshobject import MeshObject, MeshingParameters
from .snapshot import TimeSnapshot, ModeFilteredProbe, EpsilonSnapshot, FrequencySnapshot, EpsilonBox, EpsilonBoxFull, SnapshotBoxSurface, SnapshotBox, ModeVolumeBoxFull
from .probe import Probe

# .. todo:: fix these globbed imports?
from .bristolFDTD_generator_functions import *
from .GeometryObjects import *

class BFDTDobject(object):
  '''
  .. todo:: add addSnapshot, addProbe, etc functions to BFDTDobject to make adding stuff easier (should copy value from last similar)
  .. todo:: beware of the multiple snapshot lists! reduce duplicate info and add set/get functions
  .. todo:: implement "orientation" thingie from triangular_prism.py to easily exchange axes.
  .. todo:: objects should be able to have parents, etc. (try to follow structure similar to what is in Blender)
  .. todo:: We might want to add a more generic .inp object combining snapshots, probes, etc instead of all those different lists?
  .. todo:: We need "periodic objects" to reduce RAM usage in case of crystal/periodic structures.
  
  .. todo:: DESIGN: Debate advantage of using single lists for objects or per-type lists + epsilon/MF-probe/time-snapshots distinctions.
  
    * single list:
    
      * advantages: Ability to write out objects in arbitrary orders, including same as originally imported/read file. -> User could use custom object write functions if he wants to do that. Non-canonical ordering should be discouraged anyway. (and not matter to the simulation) Geo objects will be ordered in any case as that is the only place order matters.
      * disadvantages: Need to loop through list to get specific types of object. -> Except for geo objects, it is unlikely that there will be more than ~2000 objects. And if size becomes a problem, it should be possible to hack in something custom for extreme cases.
      
    * multiples lists:
    
      * advantages: Faster access to specific types of objects. Easy to write things out in a canonical order. -> Writing out in canonical order can also be done with single lists and some filtering.
      * disadvantages: lots of attributes and what if we add new objects? -> it should be ok to limit ourselves to geo, exc, (probe, tsnap, fsnap). Any additional objects can be subclasses and if really different, a new list. get/set() functions can be added as needed. They are also needed with single lists anyway. So no change from user point of view.
  
  .. todo:: append* functions do not check the type of the appended object. It would also be possible to assign object to the various lists based on their type. cf design todo...
  '''
  def __init__(self):
    
    # read configuration options from a config file
    # if it does not exist, use defaults and create the config file
    config = configparser.ConfigParser({
                                          'SafetyChecks': 'True',
                                          'autoset_FrequencySnapshotSettings': 'True',
                                          'autoset_N_FrequencySnapshots': '1',
                                          'autoset_ExcitationStartTime': 'True',
                                          'AutoFix': 'True',
                                          'MaxTimeSnapshots': '99',
                                          'MaxFrequencySnapshots': '99',
                                          'RepetitionFactor_MaxPeriod': '100',
                                          'RepetitionFactor_ExcitationEndTime': '10',
                                          'RepetitionMode': '3',
                                        })
    
    configdir = os.path.join(utilities.getuserdir.getuserdir(), '.config', 'script_inception_public')
    os.makedirs(configdir, exist_ok=True)
    configfile_name = os.path.join(configdir, 'BFDTDobject.ini')
    #print('configfile_name = ', configfile_name)
    configfiles_read = config.read(configfile_name)
    #print('configfiles_read = ', configfiles_read)
    self.SafetyChecks = config['DEFAULT'].getboolean('SafetyChecks')
    self.autoset_FrequencySnapshotSettings = config['DEFAULT'].getboolean('autoset_FrequencySnapshotSettings')
    self.autoset_N_FrequencySnapshots = config['DEFAULT'].getint('autoset_N_FrequencySnapshots')
    self.autoset_ExcitationStartTime = config['DEFAULT'].getboolean('autoset_ExcitationStartTime')
    self.AutoFix = config['DEFAULT'].getboolean('AutoFix')
    self.MaxTimeSnapshots = config['DEFAULT'].getint('MaxTimeSnapshots')
    self.MaxFrequencySnapshots = config['DEFAULT'].getint('MaxFrequencySnapshots')
    self.RepetitionFactor_MaxPeriod = config['DEFAULT'].getint('RepetitionFactor_MaxPeriod')
    self.RepetitionFactor_ExcitationEndTime = config['DEFAULT'].getint('RepetitionFactor_ExcitationEndTime')
    self.RepetitionMode = config['DEFAULT'].getint('RepetitionMode')
    
    if not configfiles_read:
      print('No config file found. Creating {}'.format(configfile_name))
      with open(configfile_name, 'w') as configfile:
        config.write(configfile)
    
    # enable/disable safety checks:
    # TODO: Use  warnings.warn() + warnings.simplefilter() to change behaviour? -> but we would like it to be specific to this module and not affect others...
    #self.checkSimulation = True
    #self.setSafetyChecks(True)
    
    # enable/disable automatic value settings:
    #self.autoset_FrequencySnapshotSettings = True
    #self.autoset_N_FrequencySnapshots = 1
    #self.autoset_ExcitationStartTime = True
    
    # mandatory objects
    self.mesh = MeshObject()
    self.flag = Flag()
    self.boundaries = Boundaries()
    self.box = Box()
    
    # geometry objects
    self.geometry_object_list = []
    self.sphere_list = []
    self.block_list = []
    self.distorted_list = []
    self.cylinder_list = []
    self.global_rotation_list = []
    
    # excitation objects
    self.excitation_list = []
    
    # measurement objects
    #self.measurement_object_list = [] # TODO: make sure fully unused + not necessary and remove? use subclasses, etc...
    self.snapshot_list = []
    self.time_snapshot_list = []
    self.frequency_snapshot_list = []
    self.probe_list = []

    # excitation template list
    self.excitation_template_list = []
    self.mesh_object_list = []

    # special
    self.fileList = []
    
    # excitation object meshes
    self.fitMeshToExcitations = True
    self.fitMeshToProbes = False
    self.fitMeshToSnapshots = False
    
    self.verboseMeshing = False
    
    self.verbosity = 1
    
    # default properties for writing files
    # executable to use for shellscripts, running, etc
    self.BFDTD_executable = 'fdtd'
    self.fileBaseName = 'sim'
    self.WORKDIR = '$JOBDIR'
    self.WALLTIME = 12
    
    # default material properties
    self.default_permittivity = 1
    self.default_conductivity = 0
    
    # data input/output
    # TODO: Decide on proper names/organization
    self.dataPaths = ['.']
    #self.data = None
    self.data_time_snapshots = dict()
    self.data_frequency_snapshots = dict()
    #self.data_epsilon = None
    #self.data_fields_frequency_domain_list = []
    #self.data_fields_time_domain_list = []
    #self.data_fields_time_domain_list = []
    
  def disableSafetyChecks(self):
    self.SafetyChecks = False
  
  def enableSafetyChecks(self):
    self.SafetyChecks = True
  
  def disableAutoFix(self):
    self.AutoFix = False
  
  def enableAutoFix(self):
    self.AutoFix = True
  
  def setSafetyChecks(self, val):
    '''
    .. todo:: Finish safety check features...
    
    Because safety checks are essential, they currently always raise exceptions.
    Will decide later which way to go.
    '''
    raise Exception('DO NOT USE AT THE MOMENT')
    if val:
      warnings.simplefilter("error")
    else:
      warnings.simplefilter("always")
  
  #################
  def getExcitationInfos(self):
    '''
    Loops over all excitations and returns the tuple (StartTimeMin, EndTimeMax, FrequencyMin, FrequencyMax).
    '''
    StartTimeMin = numpy.inf
    EndTimeMax = -numpy.inf
    FrequencyMin = numpy.inf
    FrequencyMax = -numpy.inf
    
    for E in self.getExcitations():
      if E.getStartTime() < StartTimeMin:
        StartTimeMin = E.getStartTime()
      if E.getEndTime() > EndTimeMax:
        EndTimeMax = E.getEndTime()
      if E.getFrequencyMin() < FrequencyMin:
        FrequencyMin = E.getFrequencyMin()
      if E.getFrequencyMax() > FrequencyMax:
        FrequencyMax = E.getFrequencyMax()
    
    return (StartTimeMin, EndTimeMax, FrequencyMin, FrequencyMax)
  
  def getExcitationStartTimeMin(self):
    '''Returns the smallest "start time" of all excitations.'''
    (StartTimeMin, EndTimeMax, FrequencyMin, FrequencyMax) = self.getExcitationInfos()
    return(StartTimeMin)
  
  def getExcitationEndTimeMax(self):
    '''Returns the biggest "end time" of all excitations.'''
    (StartTimeMin, EndTimeMax, FrequencyMin, FrequencyMax) = self.getExcitationInfos()
    return(EndTimeMax)

  def getExcitationFrequencyMin(self):
    '''Returns the smallest "start freqency" of all excitations.'''
    (StartTimeMin, EndTimeMax, FrequencyMin, FrequencyMax) = self.getExcitationInfos()
    return(FrequencyMin)
  
  def getExcitationFrequencyMax(self):
    '''Returns the biggest "end frequency" of all excitations.'''
    (StartTimeMin, EndTimeMax, FrequencyMin, FrequencyMax) = self.getExcitationInfos()
    return(FrequencyMax)
    
  def getExcitationFrequencyRange(self):
    '''Returns the total frequency range covered by all excitations.'''
    (StartTimeMin, EndTimeMax, FrequencyMin, FrequencyMax) = self.getExcitationInfos()
    return (FrequencyMin, FrequencyMax)
  #################

  def setAutosetExcitationStartTime(self, val):
    self.autoset_ExcitationStartTime = val

  def setAutosetFrequencySnapshotSettings(self, val):
    self.autoset_FrequencySnapshotSettings = val

  def setAutosetNFrequencySnapshots(self, Nsnaps):
    self.autoset_N_FrequencySnapshots = Nsnaps

  # .. todo:: safety check/autoset combo function?

  def autosetExcitationStartTime(self):
    for E in self.getExcitations():
      if E.getStartTime() < 0:
        print('WARNING: Fixing excitation start time!')
        E.setStartTime(0)

  def autosetFrequencySnapshotSettings(self, mode):
    '''
    Automatically sets frequency snapshots parameters.
    
    mode = 0:
      repetition = (MaxIterations - start)/self.autoset_N_FrequencySnapshots
    mode = 1:
      repetition = RepetitionFactor*period_max
    mode = 2:
      repetition = RepetitionFactor*ExcitationEndTimeMax
    mode = 3:
      repetition = biggest repetition between mode 1 and 2
      
    start = ExcitationEndTimeMax
    first = start + repetition
    '''
    
    if len(self.getExcitations()) <= 0:
      raise Exception('At least one excitation is required for automatic snapshot configuration.')
    
    timestep = self.getTimeStep()
    
    Nstart = int(ceil(self.getExcitationEndTimeMax()/timestep))
    
    ############
    ##### choose repetition value
    
    # fixed number of snapshots
    repetition_0 = int(floor((self.getIterations() - Nstart)/self.autoset_N_FrequencySnapshots))
    
    # multiple of max period
    period_max = 1 / self.getExcitationFrequencyMin()
    repetition_1 =  int(ceil( self.RepetitionFactor_MaxPeriod * period_max / timestep ))
    
    # multiple of excitation end time
    repetition_2 = int(ceil( self.RepetitionFactor_ExcitationEndTime * self.getExcitationEndTimeMax() / timestep ))
    
    if mode == 0:
      repetition = repetition_0
    elif mode == 1:
      repetition = repetition_1
    elif mode == 2:
      repetition = repetition_2
    else:
      repetition = max(repetition_1, repetition_2)
      
    # additional min limit
    repetition = max(repetition, 24*60*60)
    ############
    
    Nfirst = Nstart + repetition
    Nsnaps = int(floor( ( (self.getIterations() - Nfirst) / repetition ) + 1 ))
    Nlast = Nstart + Nsnaps*repetition
    
    print('----------------------------------')
    print('Nstart = {}'.format(Nstart))
    print('Nfirst = {}'.format(Nfirst))
    print('Nlast = {}'.format(Nlast))
    print('repetition = {}'.format(repetition))
    print('Nsnaps = {}'.format(Nsnaps))
    print('Niterations = {}'.format(self.getIterations()))
    print('----------------------------------')
    print('repetition_0 = {}'.format(repetition_0))
    print('repetition_1 = {}'.format(repetition_1))
    print('repetition_2 = {}'.format(repetition_2))
    print('----------------------------------')
    print('t_start = {}'.format(Nstart*timestep))
    print('t_first = {}'.format(Nfirst*timestep))
    print('t_last = {}'.format(Nlast*timestep))
    print('t_repetition = {}'.format(repetition*timestep))
    print('t_Niterations = {}'.format(self.getIterations()*timestep))
    print('----------------------------------')
    
    # configure frequency snapshots only
    for snap in self.getFrequencySnapshots():
      snap.setStartingSample(Nstart)
      snap.setFirst(Nfirst)
      snap.setRepetition(repetition)
    
    return

  def setDataPaths(self, path_list):
    self.dataPaths = path_list

  def getFlag(self):
    return(self.flag)
  def getBoundaries(self):
    return(self.boundaries)

  def getIdString(self):
    return(self.getFlag().getIdString())
  def setIdString(self, id_string):
    return(self.getFlag().setIdString(id_string))

  def add_arguments(self, parser):
    '''
    .. todo:: implement
    '''

    #group_WritingSettings = parser.add_argument_group('GWL writing settings')
    #group_WritingSettings.add_argument("--set-lower-to-origin", help='offset structure so that its "lower corner" is moved to the (0,0,0) coordinates. This will make all coordinates positive.', action="store_true")
    #group_WritingSettings.add_argument("--write-power", help="Write power values using the power compensation (PC) parameters.", action="store_true")
    #group_WritingSettings.add_argument("--reverse_line_order_on_write", help="reverse line order on write", action="store_true")
    #group_WritingSettings.add_argument("--reverse_voxel_order_per_line_on_write", help="reverse voxel order per line on write", action="store_true")

    #group_PowerCompensation = parser.add_argument_group('GWL power compensation', 'LP(Z) = (1+K*(Z-interfaceAt))*LP(0) if bool_InverseWriting=False or LP(Z) = (1+K*((H-Z)+interfaceAt))*LP(0) if bool_InverseWriting=True') # TODO: nicely formatted help/description?
    #group_PowerCompensation.add_argument("--PC_laser_power_at_z0", help="PC: laser power at z0", type=float, default=100)
    #group_PowerCompensation.add_argument("--PC_slope", help="PC: power compensation slope", type=float, default=0)
    #group_PowerCompensation.add_argument("--PC_interfaceAt", help="PC: interface position", type=float, default=0)
    #group_PowerCompensation.add_argument("--PC_bool_InverseWriting", help="PC: To write a file designed for use with the InvertZAxis command", action="store_true", default=False)
    #group_PowerCompensation.add_argument("--PC_float_height", help='PC: "substrate height", in practice just a value added to the interfaceAt value', type=float, default=0)
    #group_PowerCompensation.add_argument("--PC_bool_LaserPowerCommand", help="PC: Use the LaserPower command instead of a 4th coordinate for power.", action="store_true", default=False)

    return
    
  def setAttributesFromParsedOptions(self, options):
    '''Sets the object's attributes based on the ones from the *options* object (usually an argparse.ArgumentParser instance).
    
    See also: :py:func:`add_arguments`
    
    .. todo:: implement
    '''
    #self.set_lower_to_origin = options.set_lower_to_origin
    #self.write_power = options.write_power
    #self.reverse_line_order_on_write = options.reverse_line_order_on_write
    #self.reverse_voxel_order_per_line_on_write = options.reverse_voxel_order_per_line_on_write
    #self.PC_laser_power_at_z0 = options.PC_laser_power_at_z0
    #self.PC_slope = options.PC_slope
    #self.PC_interfaceAt = options.PC_interfaceAt
    #self.PC_bool_InverseWriting = options.PC_bool_InverseWriting
    #self.PC_float_height = options.PC_float_height
    #self.PC_bool_LaserPowerCommand = options.PC_bool_LaserPowerCommand
    return
    
  def setVerbosity(self, verbosity):
    self.verbosity = verbosity
    return
  
  def setExecutable(self, BFDTD_executable):
    self.BFDTD_executable = BFDTD_executable
  def getExecutable(self):
    return(self.BFDTD_executable)
    
  def setFileBaseName(self, fileBaseName, set_default_filelist=True):
    self.fileBaseName = fileBaseName
    if set_default_filelist:
      self.fileList = [self.fileBaseName+'.inp', self.fileBaseName+'.geo']

  def getFileBaseName(self):
    return(self.fileBaseName)

  def setWorkDir(self, WORKDIR):
    self.WORKDIR = WORKDIR
  
  def setWallTime(self, WALLTIME):
    '''set the walltime to use for torque job shellscripts'''
    self.WALLTIME = WALLTIME

  def getWallTime(self):
    '''get the walltime to use for torque job shellscripts'''
    return(self.WALLTIME)
  
  def set2D(self):
    self.flag.set2D()
  def set3D(self):
    self.flag.set3D()
    
  def setBoundaryConditionsToPML(self, number_of_layers=8, grading_index=2, min_reflection_coeff=1e-3, thickness=None):
    '''
    Sets all boundaries to PML.
    You can specify the thickness either directly in meters/micrometers/etc or as a number of layers.
    If *thickness* == None, *number_of_layers* will be used
    else *number_of_layers* will be set so that the specified *thickness* is obtained (even if *number_of_layers* is already specified!).
    '''
    number_of_layers_Xpos = number_of_layers_Xneg = number_of_layers_Ypos = number_of_layers_Yneg = number_of_layers_Zpos = number_of_layers_Zneg = number_of_layers

    if thickness is not None:
      (idx_Xneg, val) = findNearestInSortedArray(self.mesh.xmesh, self.mesh.xmesh[0]+thickness, 0)
      (idx_Xpos, val) = findNearestInSortedArray(self.mesh.xmesh, self.mesh.xmesh[-1]-thickness, 0)
      number_of_layers_Xneg = idx_Xneg
      number_of_layers_Xpos = len(self.mesh.xmesh)-1 - idx_Xpos

      (idx_Yneg, val) = findNearestInSortedArray(self.mesh.ymesh, self.mesh.ymesh[0]+thickness, 0)
      (idx_Ypos, val) = findNearestInSortedArray(self.mesh.ymesh, self.mesh.ymesh[-1]-thickness, 0)
      number_of_layers_Yneg = idx_Yneg
      number_of_layers_Ypos = len(self.mesh.ymesh)-1 - idx_Ypos

      (idx_Zneg, val) = findNearestInSortedArray(self.mesh.zmesh, self.mesh.zmesh[0]+thickness, 0)
      (idx_Zpos, val) = findNearestInSortedArray(self.mesh.zmesh, self.mesh.zmesh[-1]-thickness, 0)
      number_of_layers_Zneg = idx_Zneg
      number_of_layers_Zpos = len(self.mesh.zmesh)-1 - idx_Zpos

    self.boundaries.setBoundaryConditionsXnegToPML(number_of_layers_Xneg, grading_index, min_reflection_coeff)
    self.boundaries.setBoundaryConditionsXposToPML(number_of_layers_Xpos, grading_index, min_reflection_coeff)
    self.boundaries.setBoundaryConditionsYnegToPML(number_of_layers_Yneg, grading_index, min_reflection_coeff)
    self.boundaries.setBoundaryConditionsYposToPML(number_of_layers_Ypos, grading_index, min_reflection_coeff)
    self.boundaries.setBoundaryConditionsZnegToPML(number_of_layers_Zneg, grading_index, min_reflection_coeff)
    self.boundaries.setBoundaryConditionsZposToPML(number_of_layers_Zpos, grading_index, min_reflection_coeff)

  def setTimeStepFactor(self, timeStepFactor):
    self.flag.setTimeStepFactor(timeStepFactor)

  def getTimeStepFactor(self):
    return self.flag.getTimeStepFactor()

  def getTimeStepMax(self):
    '''
    Returns the maxmimum acceptable timestep for stable simulations defined by::
    
      timeStepMax = 1/(c0*sqrt(1/dx^2+1/dy^2+1/dz^2))
    
    '''
    (dx,dy,dz) = self.mesh.getMinDeltas()
    timeStepMax = 1/(get_c0()*sqrt(1/dx**2+1/dy**2+1/dz**2))
    return(timeStepMax)

  def getTimeStep(self):
    '''
    Returns the timestep in:
    
      * seconds if dimensions are in meters
      * microseconds if dimensions are in micrometers
      * etc
    
    The simulation timestep is given by::
    
      timeStep = timeStepFactor/(c0*sqrt(1/dx^2+1/dy^2+1/dz^2))
    
    '''
    #(dx,dy,dz) = self.mesh.getMinDeltas()
    #timeStep = self.flag.timeStepFactor/(get_c0()*sqrt(1/dx**2+1/dy**2+1/dz**2))
    timeStep = self.flag.timeStepFactor*self.getTimeStepMax()
    return(timeStep)
  
  def setTimeStep(self, timeStep):
    '''Sets the timestep to *timeStep* indirectly by setting the timeStepFactor.'''
    #(dx,dy,dz) = self.mesh.getMinDeltas()
    #self.flag.setTimeStepFactor( timeStep*(get_c0()*sqrt(1/dx**2+1/dy**2+1/dz**2)) )
    self.flag.setTimeStepFactor( timeStep/self.getTimeStepMax() )
    return
  
  def setIterations(self, iterations, AfterSources=False):
    '''
    Sets the number of iterations.
    If AfterSources=True, the number of iterations is set so that all sources finish running and then adds **iterations** iterations after that.
    '''
    if AfterSources:
      self.setSimulationTime()
      Nmin = self.getIterations()
      self.flag.setIterations(Nmin + iterations)
    else:
      self.flag.setIterations(iterations)
    return self.getIterations()

  def getIterations(self):
    '''Returns the number of iterations.'''
    return(self.flag.getIterations())

  def setSimulationTime(self, maxtime=None, AfterSources=False):
    '''
    Sets the number of iterations to ceil(maxtime/timestep).
    '''
    if maxtime:
      self.setIterations(ceil(maxtime/self.getTimeStep()))
    else:
      if len(self.getExcitations())==0:
        sys.stderr.write('WARNING: No excitation specified. Adding default excitation.\n')
        self.addDefaultExcitation()
      self.setSimulationTime(self.getExcitationEndTimeMax())

  def addDefaultExcitation(self):
    '''Simply adds a default excitation centered in the simulation box, of excitation_size = box_size/10.'''
    default_excitation = Excitation()
    default_excitation.setCentro(self.getCentro())
    default_excitation.setSize([self.getSize()[0]/10, 0, 0])
    self.appendExcitation(default_excitation)

  def getSimulationTime(self):
    '''Returns the total simulation time based on the mesh and the number of iterations.
    
    .. todo:: Implement parsing of BFDTD output to give the current simulation time (and eventually progress bar).
    '''
    return self.getIterations()*self.getTimeStep()

  def appendExcitation(self, excitation):
    '''
    Add one or more Excitation objects to the simulation.

    :param obj: Excitation or list of Excitation instances
    '''
    if isinstance(excitation, (list, tuple)):
      self.excitation_list.extend(excitation)
    else:
      self.excitation_list.append(excitation)
    return(excitation)

  def appendGeometryObject(self, obj):
    '''
    Add one or more geometry objects to the simulation.

    :param obj: GeometryObject or list of GeometryObject instances
    '''
    if isinstance(obj, (list, tuple)):
      self.geometry_object_list.extend(obj)
    else:
      self.geometry_object_list.append(obj)
    return(obj)

  def appendSnapshot(self, obj):
    '''
    Add one or more snapshot objects to the simulation.

    :param obj: Snapshot or list of Snapshot instances
    '''
    if isinstance(obj, list):
      self.snapshot_list.extend(obj)
    else:
      self.snapshot_list.append(obj)
    return(obj)

  def appendProbe(self, obj):
    '''
    Add one or more Probe objects to the simulation.

    :param obj: Probe or list of Probe instances
    '''
    if isinstance(obj, list):
      self.probe_list.extend(obj)
    else:
      self.probe_list.append(obj)
    return(obj)

  def setSizeAndResolution(self, size_vec3, N_vec3, Ncells_per_unit=False):
    '''
    Sets the size and resolution (number of cells in the x,y and z directions) of the simulation.
    
    See also: :py:func:`bfdtd.meshobject.MeshObject.setSizeAndResolution`
    '''
    self.box.setExtension([0,0,0],size_vec3)
    return self.mesh.setSizeAndResolution(size_vec3, N_vec3, Ncells_per_unit)

  def getSizeAndResolution(self):
    return self.getMesh().getSizeAndResolution()
    
  def getBox(self):
    return self.box

  def getSize(self):
    return self.getBox().getSize()
    
  def getExtension(self):
    return self.getBox().getExtension()

  def getLower(self):
    return self.getBox().getLower()

  def getUpper(self):
    return self.getBox().getUpper()
    
  def printInfo(self):
    timestep = self.getTimeStep()
    print('Ncells = {}'.format(self.getNcells()))
    print('Iterations = {}'.format(self.getIterations()))
    print('SimulationTime = {}'.format(self.getSimulationTime()))
    print('TimeStep = {}'.format(self.getTimeStep()))
    print('StartTimeMin = {}'.format(self.getExcitationStartTimeMin()))
    print('EndTimeMax = {}'.format(self.getExcitationEndTimeMax()))
    
    iter_start = floor(self.getExcitationStartTimeMin()/timestep)
    if numpy.isfinite(iter_start):
      iter_start = int(iter_start)
    print('StartTimeMin/timestep = {}'.format( iter_start))

    iter_end = ceil(self.getExcitationEndTimeMax()/timestep)
    if numpy.isfinite(iter_end):
      iter_end = int(iter_end)
    print('EndTimeMax/timestep = {}'.format( iter_end ))
    
    print('probes:', len(self.getProbes()))
    print('frequency snapshots:', len(self.getFrequencySnapshots(split=True)))
    print('time snapshots:', len(self.getTimeSnapshots()))
    print('epsilonSnapshot:', len(self.getEpsilonSnapshots(split=True)))
    print('mode filtered probes:', len(self.getModeFilteredProbes()))
    
  def __str__(self):
      ret = '--->snapshot_list\n'
      for i in range(len(self.snapshot_list)):
          ret += '-->snapshot '+str(i)+':\n'
          ret += self.snapshot_list[i].__str__()+'\n'

      ret += '--->time_snapshot_list\n'
      for i in range(len(self.time_snapshot_list)):
          ret += '-->time_snapshot '+str(i)+':\n'
          ret += self.time_snapshot_list[i].__str__()+'\n'

      ret += '--->frequency_snapshot_list\n'
      for i in range(len(self.frequency_snapshot_list)):
          ret += '-->frequency_snapshot '+str(i)+':\n'
          ret += self.frequency_snapshot_list[i].__str__()+'\n'

      ret += '--->excitation_list\n'
      for i in range(len(self.excitation_list)):
          ret += '-->excitation '+str(i)+':\n'
          ret += self.excitation_list[i].__str__()+'\n'
      
      ret += '--->delta_X_vector\n'+self.mesh.getXmeshDelta().__str__()+'\n'+\
      '--->delta_Y_vector\n'+self.mesh.getYmeshDelta().__str__()+'\n'+\
      '--->delta_Z_vector\n'+self.mesh.getZmeshDelta().__str__()+'\n'+\
      '--->flag\n'+self.flag.__str__()+'\n'+\
      '--->boundaries\n'+self.boundaries.__str__()+'\n'+\
      '--->box\n'+self.box.__str__()+'\n'
      
      ret += '--->probe_list\n'
      for i in range(len(self.probe_list)):
          ret += '-->probe '+str(i)+':\n'
          ret += self.probe_list[i].__str__()+'\n'

      ret += '--->sphere_list\n'
      for i in range(len(self.sphere_list)):
          ret += '-->sphere '+str(i)+':\n'
          ret += self.sphere_list[i].__str__()+'\n'
      
      ret += '--->block_list\n'
      for i in range(len(self.block_list)):
          ret += '-->block '+str(i)+':\n'
          ret += self.block_list[i].__str__()+'\n'

      ret += '--->distorted_list\n'
      for i in range(len(self.distorted_list)):
          ret += '-->distorted '+str(i)+':\n'
          ret += self.distorted_list[i].__str__()+'\n'

      ret += '--->cylinder_list\n'
      for i in range(len(self.cylinder_list)):
          ret += '-->cylinder '+str(i)+':\n'
          ret += self.cylinder_list[i].__str__()+'\n'

      ret += '--->global_rotation_list\n'
      for i in range(len(self.global_rotation_list)):
          # ret += '\n'
          ret += '-->rotation '+str(i)+':\n'
          ret += self.global_rotation_list[i].__str__()+'\n'

      ret += '--->geometry_object_list\n'
      for i in range(len(self.geometry_object_list)):
          ret += '-->geometry_object '+str(i)+':\n'
          ret += self.geometry_object_list[i].__str__()+'\n'
          
      return ret
  
  def getCentro(self):
    return self.box.getCentro()
  
  def getNcells(self):
    return self.mesh.getNcells()

  ##############
  # backfill/default material related functions
  def setDefaultRefractiveIndex(self,n):
    self.default_permittivity = pow(n,2)

  def getDefaultRefractiveIndex(self):
    return numpy.sqrt(self.default_permittivity)

  def setDefaultRelativePermittivity(self, permittivity):
    self.default_permittivity = permittivity

  def setDefaultRelativeConductivity(self, conductivity):
    self.default_conductivity = conductivity

  def getDefaultRelativePermittivity(self):
    return(self.default_permittivity)

  def getDefaultRelativeConductivity(self):
    return(self.default_conductivity)
  ##############

  def addCentralXYZSnapshots(self, location, freqlist, withEpsilon=True):
    for f in freqlist:
      self.addFrequencySnapshot('X', location[0], frequency_list=[f], name='Central X snapshot for f={}'.format(f))
      self.addFrequencySnapshot('Y', location[1], frequency_list=[f], name='Central Y snapshot for f={}'.format(f))
      self.addFrequencySnapshot('Z', location[2], frequency_list=[f], name='Central Z snapshot for f={}'.format(f))
    if withEpsilon:
      self.addEpsilonSnapshot('X', location[0])
      self.addEpsilonSnapshot('Y', location[1])
      self.addEpsilonSnapshot('Z', location[2])
      
    return

  def addBoxFrequencySnapshots(self):
    '''
    This should be called after the box and mesh have been defined. Else the box size might be incorrect.
    
    Returns the "base snapshot".
    
    .. todo:: Upgrade using new snapshot system? (and what does a normal snapshot do now when L,U forms a box...?)
    .. todo:: Add SnapshotBoxSurfaceFull ? (or a "full extension" boolean like for Snapshot?)
    '''
    #L = [self.box.lower[0], self.box.lower[1], self.box.lower[2]]
    #U = [self.box.upper[0], self.box.upper[1], self.box.upper[2]]
    #F = FrequencySnapshot()
    #F.setName('Box frequency snapshot')
    #F.setExtension(L,U)
    #self.snapshot_list.append(F)
    
    F = FrequencySnapshot()
    F.setName('Box frequency snapshot')
    fbox = SnapshotBoxSurface()
    fbox.setBaseSnapshot(F)
    fbox.setExtension(*self.getExtension())
    self.appendSnapshot(fbox)

    return fbox.getBaseSnapshot()

  def addEpsilonBox(self):
    eps = EpsilonBoxFull()
    return self.appendSnapshot(eps)

  def addSnapshot(self, snapshot_class, plane, position_input, name=None):
    '''Adds a snapshot of class "snapshot_class".
    
    :param snapshot_class: One of the snapshot classes or a custom snapshot class derived from them.
    :param plane: 'x', 'y' or 'z'
    :param position_input: float or list/array of size 3
    :param name: Name of the snapshot to add. If None, will be set to a string of the form "X/Y/Z snapshot_class.__name__"

    .. todo:: use x,y,z or vectors wherever possible instead of 1,2,3/0,1,2 to avoid confusion DONE?
    .. todo:: support multiple types for position argument (int/float or array) DONE?
    .. todo:: Create function to readapt size of snapshots to sim box? Or fit them when writing out the files? Maybe store only their orientation and position?
    .. todo:: Create equivalent of addObject for .in and .inp files? or addProbe, addSnapshot, etc?
    .. todo:: create generic plane adding function and call it from the specific functions
    '''
    
    # Forcing switch to x,y,z by exiting on numeric indices.
    if not isinstance(plane, str):
      raise TypeError('Plane argument should be of type \'str\', but is of type {}\nIf you are still using numeric indices (0,1,2 or 1,2,3), please switch to letter indices: \'x\',\'y\',\'z\'.'.format(type(position_input)))

    # force lower case
    plane = plane.lower()

    if plane not in ['x','y','z']:
      raise Exception('ERROR: Invalid plane value. plane must be \'x\',\'y\' or \'z\'')
    
    # determine position
    position = 0
    if isinstance(position_input, list) or isinstance(position_input, numpy.ndarray):
      position = position_input[['x','y','z'].index(plane)]
    else:
      position = position_input
      
    # data type check
    if not isinstance(position,int) and not isinstance(position,float) and not isinstance(position, numpy.int64):
      raise Exception('ERROR: position argument is not int or float, but is {}'.format(type(position)))
    
    #vec, alpha = getVecAlphaDirectionFromVar(plane)
    if plane == 'x':
      if name is None:
        name='X '+snapshot_class.__name__
      L = [position, self.box.lower[1], self.box.lower[2]]
      U = [position, self.box.upper[1], self.box.upper[2]]
    elif plane == 'y':
      if name is None:
        name='Y '+snapshot_class.__name__
      L = [self.box.lower[0], position, self.box.lower[2]]
      U = [self.box.upper[0], position, self.box.upper[2]]
    elif plane == 'z':
      if name is None:
        name='Z '+snapshot_class.__name__
      L = [self.box.lower[0], self.box.lower[1], position]
      U = [self.box.upper[0], self.box.upper[1], position]
    else:
      raise Exception('ERROR: Invalid plane : {}'.format(plane))
    
    S = snapshot_class()
    S.name = name
    S.plane = plane
    S.P1 = L
    S.P2 = U
    self.snapshot_list.append(S)
    return S
  
  def addFrequencySnapshot(self, plane, position, frequency_list=None, name=None):
    '''Add a frequency snapshot.
    
    :param plane: The X, Y or Z plane.
    :param position: the X, Y or Z (depending on the value of *plane*) position or simply a set of 3D coordinates (ex:``[5.3, 6.4, 7.6]``).
    :type position: float or list/array of size 3
    :param frequency_list: a list of frequencies
    :type frequency_list: a list of floats (ex: [1.2, 2.3, 3.4])
    :param string name: string
    
    See also: :py:func:`addSnapshot`
    '''
    F = self.addSnapshot(FrequencySnapshot, plane, position, name=name)
    F.setFrequencies(frequency_list)
    return(F)
  
  def addTimeSnapshot(self, plane, position, name=None):
    return self.addSnapshot(TimeSnapshot, plane, position, name=name)

  def addModeFilteredProbe(self, plane, position, name=None):
    return self.addSnapshot(ModeFilteredProbe, plane, position, name=name)

  def addEpsilonSnapshot(self, plane, position, name=None):
    eps_snapshot = self.addSnapshot(EpsilonSnapshot, plane, position, name=name)
    # We set repetition to the max iteration number, so that only one epsilon snapshot is generated.
    eps_snapshot.repetition = self.getIterations()
    eps_snapshot.first = 1
    return eps_snapshot

  def clearTimeSnapshots(self):
    '''
    Remove all time snapshots.
    
    .. todo:: Should distinguish time snapshots based on their attributes?
    .. todo:: Some "sorting" function should be created to sort snapshots based on their attributes? And could be used on import. -> Beware feature creep!!!
    '''
    self.snapshot_list = [ s for s in self.snapshot_list if ( not isinstance(s,TimeSnapshot) or isinstance(s,EpsilonSnapshot) or isinstance(s,ModeFilteredProbe) ) ]
    self.time_snapshot_list[:] = []

  def clearFrequencySnapshots(self):
    '''Remove all frequency snapshots.'''
    self.snapshot_list = [ s for s in self.snapshot_list if not isinstance(s,FrequencySnapshot) ]
    self.frequency_snapshot_list[:] = []

  def clearEpsilonSnapshots(self):
    '''Remove all epsilon snapshots.'''
    self.snapshot_list = [ s for s in self.snapshot_list if not isinstance(s,EpsilonSnapshot) ]

  def clearModeFilteredProbes(self):
    '''Remove all "mode filtered probe" snapshots.'''
    self.snapshot_list = [ s for s in self.snapshot_list if not isinstance(s,ModeFilteredProbe) ]

  def clearAllSnapshots(self):
    '''Remove all snapshots (time, frequency, etc).'''
    self.snapshot_list[:] = []
    self.time_snapshot_list[:] = []
    self.frequency_snapshot_list[:] = []

  def clearProbes(self):
    '''Clear the list of probes.'''
    self.probe_list[:] = []

  def clearGeometry(self):
    '''Clear the list of geometry objects.'''
    self.geometry_object_list[:] = []

  def clearExcitationList(self):
    '''Clear the list of Excitation objects.'''
    self.excitation_list[:] = []

  def clearFileList(self):
    ''' Clears the filelist. '''
    self.fileList[:] = []

  def getFileList(self):
    return(self.fileList)

  def setFileList(self, fileList):
    '''
    Sets the filelist.
    ..todo:: appendFileList()? (but make sure always a single box in geo file and that it is at the end)
    '''
    self.fileList = fileList
    return(fileList)

  def getObjects(self):
    '''Returns the list of excitations and geometry objects.'''    
    object_list = []
    object_list.extend(self.getExcitations())
    object_list.extend(self.getGeometryObjects())
    #object_list.extend(self.getProbes())
    return object_list

  def getGeometryObjects(self):
    '''Returns the list of geometry objects.'''
    return(self.geometry_object_list)

  def setGeometryObjects(self, geometry_object_list):
    '''Returns the list of geometry objects.'''
    self.geometry_object_list = geometry_object_list
    return(self.geometry_object_list)

  def getGeometryObjectsByName(self, name):
    '''Returns the list of geometry objects matching the name **name**.
    
    :param name: string (ex: ``'defect'``)
    
    .. todo:: case-insensitive matching, regex matching, globbing and/or partial matching
    '''
    return [ i for i in self.geometry_object_list if i.name==name ]
    
  def getGeometryObjectsByType(self, class_or_type_or_tuple):
    '''Returns the list of geometry objects of type/class **class_or_type_or_tuple**.
    
    The filtering is done by ``isinstance(object, class_or_type_or_tuple)``.
    
    :param class_or_type_or_tuple: An FDTD object class like :py:class:`Block` or a tuple of such classes like ``(Block, Cylinder)``, in which case it will match if it is an instance of any of the classes in the tuple.
    '''
    return [ i for i in self.getGeometryObjects() if isinstance(i, class_or_type_or_tuple) ]

  def getSnapshots(self, split=False):
    ''' Returns a list of all snapshots. '''
    if split:
      snapshot_list = []
      for s in self.snapshot_list:
        if isinstance(s, ModeVolumeBoxFull):
          esnap_list, fsnap_list = s.getSplitSnapshots(self.getMesh())
          snapshot_list.extend(esnap_list + fsnap_list)
        else:
          snapshot_list.append(s)
      return snapshot_list
    else:
      return(self.snapshot_list)

  def setSnapshots(self, obj):
    '''
    Removes all existing snapshots and replaces them with the elements from  the list of snapshots *obj* (or *[obj]* if *obj* is not a list, for convenience).
    
    Ex::
      
      sim.setSnapshots(EpsilonBoxFull()) # single snapshot
      sim.setSnapshots(100*[EpsilonSnapshot()]) # list of 100 snapshots
    
    :param obj: Snapshot or list of Snapshot instances
    '''
    self.clearAllSnapshots()
    if isinstance(obj, list):
      self.snapshot_list = obj
    else:
      self.snapshot_list = [obj]
    
    return(self.snapshot_list)

  def getAllTimeSnapshots(self, filterBasedOnClass=False, split=False):
    '''
    Returns the time snapshots sorted into lists based on their type:
    
    * all_time_snapshots
    * time_snapshots
    * epsilon_snapshots
    * mode_filtered_probes

    The classifications are exclusive, i.e.::
    
      len(all_time_snapshots) = len(time_snapshots) + len(epsilon_snapshots) + len(mode_filtered_probes)
    
    :param filterBasedOnClass: Boolean. If True, the snapshot type will be determined based on its current class type, else it will be determined based on its attributes. Default: False.
    :return: (all_time_snapshots, time_snapshots, epsilon_snapshots, mode_filtered_probes) - tuple of lists
        
    .. seealso::
    
      * :py:func:`getTimeSnapshots`
      * :py:func:`getEpsilonSnapshots`
      * :py:func:`getModeFilteredProbes`
      * :py:func:`bfdtd.snapshot.TimeSnapshot.getTypeBasedOnAttributes`
    
    .. warning:: The *SnapshotBox* subclasses are not yet supported by this system and will not be returned even if they generate *TimeSnapshot* entries.
    
    .. todo:: Support *SnapshotBox* subclasses?
    .. todo:: frequency snapshots, etc? split probe objects into different attributes again? -> Need to be carefull with output file numbering! Data read-in depends on it!
    '''
    
    all_time_snapshots = []
    time_snapshots = []
    epsilon_snapshots = []
    mode_filtered_probes = []

    for s in self.getSnapshots(split):
      if isinstance(s, TimeSnapshot):
        all_time_snapshots.append(s)

        if filterBasedOnClass:
          if isinstance(s, ModeFilteredProbe):
            mode_filtered_probes.append(s)
          elif isinstance(s, EpsilonSnapshot):
            epsilon_snapshots.append(s)
          else:
            time_snapshots.append(s)
        else:
          t = s.getTypeBasedOnAttributes()
          if t == ModeFilteredProbe:
            mode_filtered_probes.append(s)
          elif t == EpsilonSnapshot:
            epsilon_snapshots.append(s)
          else:
            time_snapshots.append(s)

    return (all_time_snapshots, time_snapshots, epsilon_snapshots, mode_filtered_probes)

  def getTimeSnapshots(self, filterBasedOnClass=False):
    '''
    Returns all "time snapshots".
    
    .. seealso:: :py:func:`getAllTimeSnapshots`
    '''
    (all_time_snapshots, time_snapshots, epsilon_snapshots, mode_filtered_probes) = self.getAllTimeSnapshots(filterBasedOnClass)
    return time_snapshots
    
  def getModeFilteredProbes(self, filterBasedOnClass=False):
    '''
    Returns all "mode filtered probes".
    
    .. seealso:: :py:func:`getAllTimeSnapshots`
    '''
    (all_time_snapshots, time_snapshots, epsilon_snapshots, mode_filtered_probes) = self.getAllTimeSnapshots(filterBasedOnClass)
    return mode_filtered_probes

  def getEpsilonSnapshots(self, filterBasedOnClass=False, split=False):
    '''
    Returns all "epsilon snapshots".
    
    .. seealso:: :py:func:`getAllTimeSnapshots`
    '''
    (all_time_snapshots, time_snapshots, epsilon_snapshots, mode_filtered_probes) = self.getAllTimeSnapshots(filterBasedOnClass, split=split)
    return epsilon_snapshots

  def getFrequencySnapshots(self, split=False):
    '''
    Returns a list of the frequency snapshots.
    .. todo:: improve "super-snapshot" handling... (boxes, etc) -> one problem is that it depends on the mesh of course...
    '''
    frequency_snapshot_list = [ s for s in self.getSnapshots(split) if isinstance(s, FrequencySnapshot) ]
    #if not split:
      #frequency_snapshot_list = [ s for s in self.snapshot_list if isinstance(s, FrequencySnapshot) ]
    #else:
      #frequency_snapshot_list = []
      #for s in self.snapshot_list:
        #if isinstance(s, FrequencySnapshot):
          #if isinstance(s, ModeVolumeBoxFull):
            #esnap_list, fsnap_list = s.getSplitSnapshots(self.getMesh())
            #frequency_snapshot_list.extend(fsnap_list)
          #else:
            #frequency_snapshot_list.append(s)
    return frequency_snapshot_list
  
  def getProbes(self):
    return(self.probe_list)
  
  def getExcitations(self):
    return(self.excitation_list)
  def setExcitations(self, excitation_list):
    if not isinstance(excitation_list, list):
      excitation_list = [excitation_list]
    self.excitation_list = excitation_list

  def getRefractiveIndexSet(self):
    '''
    Returns a set of unique refractive indices used in the objects.
    '''
    n_set = set()
    for obj in self.getGeometryObjects():
      n_set.add(obj.getRefractiveIndex())
    return(n_set)

  def getExcitationFrequencySet(self):
    '''
    Returns a set of unique frequencies used in the excitations.
    '''
    frequency_set = set()
    for E in self.getExcitations():
      frequency_set.add(E.getFrequency())
    return(frequency_set)

  def getSnapshotFrequencySet(self):
    '''
    Returns a set of unique frequencies used in the frequency snapshots.
    '''
    frequency_set = set()
    for freq_snap in self.getFrequencySnapshots():
      for freq in freq_snap.frequency_vector:
        frequency_set.add(freq)
    return(frequency_set)

  def getSnapshotFirstMax(self):
    first_set = set()
    for s in self.getSnapshots():
      first_set.add(s.getFirst())
    return(max(first_set))

  def clearMesh():
    ''' Resets the mesh to the default. '''
    self.mesh = MeshObject()
  
  def getMesh(self):
    return(self.mesh)
  def setMesh(self, mesh):
    self.mesh = mesh

  def getXmesh(self):
    return(self.getMesh().getXmesh())

  def getYmesh(self):
    return(self.getMesh().getYmesh())

  def getZmesh(self):
    return(self.getMesh().getZmesh())
  
  def readBristolFDTD(self, *filename):
    '''
    Reads in one or multiple BFDTD input files (.in (=>.inp+.geo), .geo or .inp) and adds their contents to the BFDTDobject.
    
    Examples::
    
      sim.readBristolFDTD('sim.in')
      sim.readBristolFDTD('sim.geo')
      sim.readBristolFDTD('sim.inp')
      sim.readBristolFDTD('sim1.in','sim2.in','sim3.geo')
      sim.readBristolFDTD('sim.geo','sim.inp')
    
    * Returns 0 on success.
    * Returns -1 on failure.
    '''
    
    for current_filename in filename:
    
      if self.verbosity > 0:
        print('-> Processing generic file : ' + current_filename)
      
      if not os.path.isfile(current_filename):
        raise Exception('ERROR: Not a file: {}'.format(current_filename))
        #print('ERROR: Not a file: {}'.format(current_filename), file=sys.stderr)
        return(-1)
      
      (root, extension) = os.path.splitext(current_filename)
      if extension == '.in':
        if self.verbosity>0: print('.in file detected')
        self.readFileList(current_filename)
      elif extension == '.inp':
        if self.verbosity>0: print('.inp file detected')
        self.readInputFile(current_filename)
      elif extension == '.geo':
        if self.verbosity>0: print('.geo file detected')
        self.readInputFile(current_filename)
      elif extension == '.prn':
        raise Exception('.prn file detected: Not supported yet')
      else:
        raise Exception('Unknown file format: {}'.format(extension))
    
    return(0)

  def readInputFile(self, filename):
      '''
      read GEO or INP file
      
      .. todo:: Determine if a time snapshot is an epsilon or mode filtered snapshot during file reading (useful for easier processing of the snapshots later on). (cf snapshot getTypeByAttributes function in snapshot.py...)
      .. todo:: Store full comment as attribute of object
      .. todo:: This parsing system may need to be rewritten because rotation entries should apply to the previous entry... (partially done, but may cause problems in case of multiple rotations)
      .. todo:: separation of snapshots into correct classes on read-in by checking attributes (+ later MVboxes, etc of course, using special comment system)
      .. todo:: proper validation of entries (number and type of arguments), with output of lines on which errors occur.
      '''
      if self.verbosity>0: print('Processing ' + filename)
      box_read = False
      xmesh_read = False
      
      # open file
      input_stream = open(filename)
      # read the whole file as one string
      fulltext = input_stream.read()
      # close file
      input_stream.close()
  
      # print fulltext
  
      # remove comments
      # TODO: Add more generic system for functional comments (to add layer, scene and group for example)
      pattern_stripcomments = re.compile("\*\*(?!name=).*\n")
      cleantext = pattern_stripcomments.sub("\n", fulltext)
      #print(cleantext)
  
      # pattern_objects = re.compile("^(?<Type>\w+).*?\{(?<data>[^\{\}]*?)\}")
      #pattern_objects = re.compile("(?P<Type>\w+)\s*(?P<name>(?<=\*\*name=)[^{}]*)?{(?P<data>[^{}]*)}",re.DOTALL)
      pattern_objects = re.compile("(?P<Type>\w+)\s*(?P<nameblob>[^{}]+)?{(?P<data>[^{}]*)}",re.DOTALL)
      objects = [m.groupdict() for m in pattern_objects.finditer(cleantext)]
    
      entries = []
      # process objects
      for i in range(len(objects)):
          Type = objects[i]['Type']
          name = ''
          if 'nameblob' in objects[i].keys():
            #print objects[i]['nameblob']
            if objects[i]['nameblob']:
              #print 'OK'
              pattern_nameblob = re.compile("\*\*name=(.*)")
              m = pattern_nameblob.match(objects[i]['nameblob'])
              if m:
                name = m.group(1).strip()
            #else:
              #print 'NOT OK'
              #name = ''
          #else:
            #print 'NO NAME'
            #name = ''
          data = objects[i]['data']
          
          # convert Type to upper case and strip it
          Type = Type.upper().strip()
          # split data by spaces and new lines
          data = re.split('\s+',data)
          # remove empty lines from data
          #data = filter(None, data)
          data = list(filter(None, data))
          #print('data = '+str(data))
          
          entry = Entry()
          entry.Type = Type
          entry.name = name
          entry.data = data
          entries.append(entry)

          try:
            # mandatory objects
            if entry.Type == 'XMESH':
                self.mesh.setXmeshDelta(float_array(entry.data))
                xmesh_read = True
            elif entry.Type == 'YMESH':
                self.mesh.setYmeshDelta(float_array(entry.data))
            elif entry.Type == 'ZMESH':
                self.mesh.setZmeshDelta(float_array(entry.data))
            elif entry.Type == 'FLAG':
                self.flag.read_entry(entry)
            elif entry.Type == 'BOUNDARY':
                self.boundaries.read_entry(entry)
            elif entry.Type == 'BOX':
                self.box.read_entry(entry)
                box_read = True
                    
            # geometry objects
            elif entry.Type == 'SPHERE':
                sphere = Sphere()
                sphere.read_entry(entry)
                self.sphere_list.append(sphere)
                self.geometry_object_list.append(sphere)
            elif entry.Type == 'BLOCK':
                block = Block()
                block.read_entry(entry)
                self.block_list.append(block)
                self.geometry_object_list.append(block)
            elif entry.Type == 'DISTORTED':
                distorted = Distorted()
                distorted.read_entry(entry)
                self.distorted_list.append(distorted)
                self.geometry_object_list.append(distorted)
            elif entry.Type == 'CYLINDER':
                cylinder = Cylinder()
                cylinder.read_entry(entry)
                self.cylinder_list.append(cylinder)
                self.geometry_object_list.append(cylinder)
                
            elif entry.Type == 'ROTATION':
                rotation = Rotation()
                rotation.read_entry(entry)
                self.global_rotation_list.append(rotation)
                self.geometry_object_list[-1].rotation_list.append(rotation) # append rotation to previous object (pb of course, if multiple rotations...)
            
            # excitation objects
            elif entry.Type == 'EXCITATION':
                current_excitation = Excitation()
                current_excitation.read_entry(entry)
                self.excitation_list.append(current_excitation)
            
            # measurement objects
            elif entry.Type == 'FREQUENCY_SNAPSHOT':
                frequency_snapshot = FrequencySnapshot()
                frequency_snapshot.read_entry(entry)
                frequency_snapshot.setFullExtensionOff()
                self.frequency_snapshot_list.append(frequency_snapshot)
                self.snapshot_list.append(frequency_snapshot)
            elif entry.Type == 'SNAPSHOT':
                time_snapshot = TimeSnapshot()
                time_snapshot.read_entry(entry)
                time_snapshot.setFullExtensionOff()
                self.time_snapshot_list.append(time_snapshot)
                self.snapshot_list.append(time_snapshot)
            elif entry.Type == 'PROBE':
                probe = Probe()
                probe.read_entry(entry)
                self.probe_list.append(probe)
    
            else:
                print('Unknown Type: ', entry.Type)

          except:
            if self.verbosity > 0:
              print('Failed to read the following entry:')
              print(objects[i])
              print('Entry number: {}'.format(i))
              print('Type: {}'.format(objects[i]['Type']))
              print('nameblob: {}'.format(objects[i]['nameblob']))
              print('data:')
              for i in objects[i]['data'].splitlines():
                print('  {}'.format(i))
            
            raise

      return [ xmesh_read, box_read ]

  def readFileList(self, filename):
      ''' read .in file '''
      if self.verbosity>0: print('->Processing .in file : ', filename)
      
      box_read = False
      xmesh_read = False
      
      with open(filename, 'r') as f:
        for line in f:
            if line.strip(): # only process line if it is not empty
              if self.verbosity>0: print(('os.path.dirname(filename): ', os.path.dirname(filename))) # directory of .in file
              if self.verbosity>0: print(('line.strip()=', line.strip())) # remove any \n or similar
              self.fileList.append(line.strip())
              # this is done so that you don't have to be in the directory containing the .geo/.inp files
              #subfile = os.path.join(os.path.dirname(filename),os.path.basename(line.strip())) # converts absolute paths to relative
              subfile = os.path.join(os.path.dirname(filename),line.strip()) # uses absolute paths if given
              if self.verbosity>0: print(('subfile: ', subfile))
              if (not xmesh_read): # as long as the mesh hasn't been read, .inp is assumed as the default extension
                  subfile_ext = addExtension(subfile,'inp')
              else:
                  subfile_ext = addExtension(subfile,'geo')
                  if not os.path.isfile(subfile_ext):
                    subfile_ext = addExtension(subfile,'inp')
              [ xmesh_read_loc, box_read_loc ] = self.readInputFile(subfile_ext)
              if xmesh_read_loc:
                  xmesh_read = True
              if box_read_loc:
                  box_read = True
      
      if (not xmesh_read):
          print('WARNING: mesh not found')
      if (not box_read):
          print('WARNING: box not found')
  
  def writeDatFiles(self, directory, overwrite=True):
    '''Generate template .dat file for a plane excitation'''
    for obj in self.excitation_template_list:
      warnings.warn('WARNING: Passing the mesh not supported yet!!! Use generated .dat file at your own risk (as always of course).')
      #obj.writeDatFile(directory+os.sep+obj.fileName, self.mesh, overwrite=overwrite)
      obj.writeDatFile(directory+os.sep+obj.fileName, overwrite=overwrite)
    return

  def writeCtlFile(self, fileName, withGeom=True, overwrite=True, withBox=True, no_offset=False):
    
    ''' Generate .ctl file '''
    #Cylinder.write_entry = Cylinder.writeCTL
    #self.writeGeoFile(fileName, withGeom, overwrite, withBox)
    
    if no_offset:
      offset = numpy.array([0,0,0])
    else:
      offset = -self.getCentro()
    
    # check if file already exists
    if not overwrite and os.path.exists(fileName):
      raise UserWarning('File already exists: ' + fileName)
    
    if self.verbosity > 1:
      print('Writing to {}'.format(fileName))
    
    # open file
    with open(fileName, 'w') as out:
      if withBox:
        #write box
        self.box.writeCTL(out)
      
      out.write('(set! geometry (list\n')
      
      if withGeom:
        # write geometry objects
        #print('len(self.geometry_object_list) = '+len(self.geometry_object_list))
        
        # now loop through the geometry objects and write them to the file
        for obj in self.geometry_object_list:
          #print obj.name
          #print obj.__class__.__name__
          obj.writeCTL(out, offset)

      out.write('))\n')
      
      # close file
      out.close()
    return
  
  def writeGeoFile(self, fileName, withGeom=True, overwrite=True, withBox=True, call_makedirs=False):
    ''' Generate .geo file '''
    # check if file already exists
    if not overwrite and os.path.exists(fileName):
      raise UserWarning('File already exists: ' + fileName)
    
    if self.verbosity > 1:
      print('Writing to {}'.format(fileName))
    
    # create dirs if needed
    if call_makedirs:
      if not os.path.exists(os.path.dirname(fileName)):
        os.makedirs(os.path.dirname(fileName))
    
    # open file
    with open(fileName, 'w') as out:
      
      # write header
      out.write('**GEOMETRY FILE\n')
      out.write('\n')
      
      # first add a backfill block if necessary
      if self.default_permittivity != 1 or self.default_conductivity != 0:
        backfill = Block()
        backfill.setRelativePermittivity(self.default_permittivity)
        backfill.setRelativeConductivity(self.default_conductivity)
        backfill.setLowerAbsolute(self.box.getLower())
        backfill.setUpperAbsolute(self.box.getUpper())
        backfill.setName('backfill')
        backfill.write_entry(out)
      
      if withGeom:
        # write geometry objects
        #print('len(self.geometry_object_list) = '+len(self.geometry_object_list))
        
        # now loop through the geometry objects and write them to the file
        for obj in self.geometry_object_list:
          #print obj.name
          #print obj.__class__.__name__
          obj.write_entry(out)

      if withBox:
        #write box
        self.box.write_entry(out)
      
      # write footer
      out.write('end\n'); #end the file
    
      # close file
      out.close()

    return

  def fixSimulation(self):
    '''
    Automatically fix common mistakes.
    
    .. todo:: Fix AutoFix/autoset*, etc redundancy here and in sub-objects like Excitation. Streamline fixing/checking/warning/exception procedures.
    
    .. todo:: set probe steps to 1? -> check+fix
    .. todo:: probe step vs smallest excitation period... -> check+fix
    .. todo:: time step vs smallest excitation period... -> check+fix
    '''
    
    if self.getFlag().getIdString() != '_id_':
      self.getFlag().setIdString('_id_')
    
    # make sure there is at least one excitation. Otherwise Bristol FDTD will crash.
    if len(self.getExcitations())==0:
      sys.stderr.write('WARNING: No excitation specified. Adding default excitation.\n')
      self.addDefaultExcitation()
    
    if self.autoset_ExcitationStartTime:
      self.autosetExcitationStartTime()
    
    for E in self.getExcitations():
      E.fix()
    
    for p in self.getProbes():
      p.setStep(1)
    
    if self.autoset_FrequencySnapshotSettings:
      self.autosetFrequencySnapshotSettings(mode=self.RepetitionMode)
  
  def checkSimulation(self, output_checks=True):
    '''
    Supposed to make sure we don't write out too many probes/snapshots...
    
    * Problem: snapshot boxes and other compound objects will not get counted properly...
    * Solution: Best to count objects after writing (maybe use tmp, sys.stdout, file buffer or similar to allow count without actual file output).
    
    .. todo:: Check that frequency of fsnaps is within excitation range?
    .. todo:: check that repetition not too big or too small
    .. todo:: check that not too many snaps will be generated based on repetition value
    .. todo:: create function to quickly access number of generated snaps based on repetition value (+ setter functions for repetition/iterations? also based on time intervals, time/iter conversion functions?)
    '''
    if self.verbosity > 0:
      self.printInfo()
    
    if self.getFlag().getIdString() != '_id_':
      raise Exception("Please use '_id_' as ID string, not '{}'".format(self.getFlag().getIdString()))
    
    if len(self.getExcitations())==0:
      raise Exception('No excitation specified.')
    
    if output_checks:
      (all_time_snapshots, time_snapshots, epsilon_snapshots, mode_filtered_probes) = self.getAllTimeSnapshots(split=True)
      
      if len(all_time_snapshots) > utilities.brisFDTD_ID_info.TIMESNAPSHOT_MAX:
        raise Exception('Your simulation contains too many time snapshots!!! Either split it up into multiple simulations or reduce your number of snapshots. N(TimeSnapshots)={} > TIMESNAPSHOT_MAX={}'.format(len(all_time_snapshots), utilities.brisFDTD_ID_info.TIMESNAPSHOT_MAX))
      if len(all_time_snapshots) > self.MaxTimeSnapshots:
        raise Exception('Your simulation contains too many time snapshots!!! Either split it up into multiple simulations or reduce your number of snapshots. N(TimeSnapshots)={} > MaxTimeSnapshots={}'.format(len(all_time_snapshots), self.MaxTimeSnapshots))
      
      if len(self.getFrequencySnapshots(True)) > utilities.brisFDTD_ID_info.FREQUENCYSNAPSHOT_MAX:
        raise Exception('Your simulation contains too many frequency snapshots!!! Either split it up into multiple simulations or reduce your number of snapshots. N(FrequencySnapshots)={} > FREQUENCYSNAPSHOT_MAX={}'.format(len(self.getFrequencySnapshots(True)), utilities.brisFDTD_ID_info.FREQUENCYSNAPSHOT_MAX))
      if len(self.getFrequencySnapshots(True)) > self.MaxFrequencySnapshots:
        raise Exception('Your simulation contains too many frequency snapshots!!! Either split it up into multiple simulations or reduce your number of snapshots. N(FrequencySnapshots)={} > MaxFrequencySnapshots={}'.format(len(self.getFrequencySnapshots(True)), self.MaxFrequencySnapshots))
    
    #FREQUENCYSNAPSHOT_MAX
    #TIMESNAPSHOT_MAX
    #PROBE_MAX
    #MODEFILTEREDPROBE_MAX
    #warnings.warn('BAD SIM!!!')
    
    # already included in excitation check
    #if self.getExcitationStartTimeMin() < 0:
      #raise Exception('self.getExcitationStartTimeMin()={} < 0'.format(self.getExcitationStartTimeMin()))
    
    if self.getIterations() <= 0:
      raise Exception('self.getIterations()={} <= 0'.format(self.getIterations()) )
    
    if self.getIterations() > 1:
      if self.getExcitationEndTimeMax() > self.getSimulationTime():
        raise Exception('self.getExcitationEndTimeMax()={} >= self.getSimulationTime()={}'.format(self.getExcitationEndTimeMax(), self.getSimulationTime()) )
    
    # time/iteration after which the excitations have stopped
    t_Estop = self.getExcitationEndTimeMax()
    N_Estop = int(numpy.ceil(t_Estop/self.getTimeStep()))
    if self.verbosity > 0:
      print('Excitation stop time = {}'.format(t_Estop))
      print('Excitation stop iteration = {}'.format(N_Estop))
    
    for snapshot in self.getSnapshots():
      if isinstance(snapshot, SnapshotBox):
        s = snapshot.getBaseSnapshot()
      else:
        s = snapshot
      
      if s.getFirst() > self.getIterations():
        raise Exception('Snapshots with s.getFirst()={} > self.getIterations()={}'.format(s.getFirst(), self.getIterations()))
      if s.getRepetition() <= 0:
        raise Exception('Snapshots with negative or zero repetition value! : s.getRepetition() = {}, s.__class__ = {}, s.getTypeBasedOnAttributes() = {}\n-->s:\n{}'.format(s.getRepetition(), s.__class__, s.getTypeBasedOnAttributes(), s))
    
      if isinstance(s, FrequencySnapshot):
        
        # TODO: Why these limitations? to always have enough snapshots + enough iterations in each?
        if s.getRepetition() > 5e5:
          raise Exception('repetition = {} > 5e5'.format(s.getRepetition()))
        if s.getRepetition() < 24*60*60:
          raise Exception('repetition = {} < 24*60*60'.format(s.getRepetition()))
        
        if s.getStartingSample() > self.getIterations():
          raise Exception('Snapshots with s.getStartingSample()={} > self.getIterations()={}'.format(s.getStartingSample(), self.getIterations()))
        if s.getFirst() < s.getStartingSample() + s.getRepetition():
          raise Exception('Frequency snapshot "first" value smaller than "starting sample" + "repetition": {} < {}+{}={}'.format(s.getFirst(), s.getStartingSample(), s.getRepetition(), s.getStartingSample() + s.getRepetition()))
        if s.getStartingSample() < N_Estop:
          raise Exception('Frequency snapshot "starting sample" < "excitation end": {} < {}'.format(s.getStartingSample(), N_Estop))
    
    # .. todo:: Add check functions for each object, so those can be called instead?
    for exc in self.getExcitations():
      exc.check()
      #if exc.getPeriod() > exc.getTimeConstant():
        #raise Exception('exc.getPeriod()={} > exc.getTimeConstant()={}'.format(exc.getPeriod(), exc.getTimeConstant()))
    
    for p in self.getProbes():
      if p.getStep() != 1:
        raise Exception('probe step={} != 1'.format(p.getStep()))
    
    # check that all snapshot frequencies are within excitation range
    mini, maxi = self.getExcitationFrequencyRange()
    for f in self.getSnapshotFrequencySet():
      if f < mini or maxi < f:
        raise Exception('Snapshot frequency {} is outside the excited frequency range {} - {}'.format(f, mini, maxi))
    
    return

  def writeExcitationsToFile(self, fileName, overwrite=True, append=False, call_makedirs=False):

    # create dirs if needed
    if call_makedirs:
      if not os.path.exists(os.path.dirname(fileName)):
        os.makedirs(os.path.dirname(fileName))
    
    if not overwrite:
      mode = 'x' # open for exclusive creation, failing if the file already exists
    elif append:
      mode = 'a' # open for writing, appending to the end of the file if it exists
    else:
      mode = 'w' # open for writing, truncating the file first
    
    with open(fileName, mode=mode) as fid:
      for e in self.getExcitations():
        e.write_entry(fid)
    
    return

  def writeProbesToFile(self, fileName, overwrite=True, append=False, call_makedirs=False):

    # create dirs if needed
    if call_makedirs:
      if not os.path.exists(os.path.dirname(fileName)):
        os.makedirs(os.path.dirname(fileName))
    
    if not overwrite:
      mode = 'x' # open for exclusive creation, failing if the file already exists
    elif append:
      mode = 'a' # open for writing, appending to the end of the file if it exists
    else:
      mode = 'w' # open for writing, truncating the file first
    
    with open(fileName, mode=mode) as fid:
      for p in self.getProbes():
        p.write_entry(fid)
    
    return
  
  def writeInpFile(self, fileName=None, overwrite=True):
    '''
    Generate .inp file
    
    .. todo:: Should take a file object to enable writing to sys.stdout... (useful for counting final number of items and test runs)
    '''
    
    # defaults
    if fileName is None:
      fileName = self.fileBaseName + '.inp'
    
    if self.verbosity > 1:
      print('self.AutoFix = {}'.format(self.AutoFix))
      print('self.autoset_FrequencySnapshotSettings = {}'.format(self.autoset_FrequencySnapshotSettings))
      print('self.autoset_N_FrequencySnapshots = {}'.format(self.autoset_N_FrequencySnapshots))
      print('self.autoset_ExcitationStartTime = {}'.format(self.autoset_ExcitationStartTime))
      print('self.SafetyChecks = {}'.format(self.SafetyChecks))
    
    # autofix
    if self.AutoFix:
      self.fixSimulation()
    
    # safety checks
    if self.SafetyChecks:
      self.checkSimulation()
    
    # check if file already exists
    if not overwrite and os.path.exists(fileName):
      raise UserWarning('File already exists: ' + fileName)
    
    # open file
    with open(fileName, 'w') as out:
  
      for obj in self.getExcitations():
        #obj.directory = os.path.dirname(fileName)
        obj.mesh = self.getMesh()
        # .. todo:: reduce check/fix calls... : no need to call here + in excitation write...
        obj.write_entry(out, AutoFix=self.AutoFix, SafetyChecks=self.SafetyChecks)
      #print(self.boundaries)
      self.getBoundaries().write_entry(out)
      self.getFlag().write_entry(out)
      self.getMesh().write_entry(out)
            
      for obj in self.snapshot_list:
        #print('Now calling write using obj = {}'.format(obj.__repr__()))
        obj.write_entry(out, self.getMesh())
        
      for obj in self.probe_list:
        obj.write_entry(out)
      
      #write footer
      out.write('end\n') #end the file
      #close file
      out.close()
    return
        
  def writeFileList(self, fileName, fileList=None, overwrite=True, use_relpath=False):
    ''' Generate .in file '''
    # leaving it external at the moment since it might be practical to use it without having to create a Bfdtd object
    #if self.fileList is None:
      #self.fileList = [fileBaseName+'.inp',fileBaseName+'.geo']
    if fileList is None:
      fileList = self.fileList
    print('fileName = '+fileName)
    #print('fileList = '+str(fileList))
    GEOin(fileName, fileList, overwrite=overwrite, use_relpath=use_relpath)
    return
    
  def writeCondorScript(self, fileName, BASENAME=None):
    ''' Generate fileName.cmd file for Condor using BASENAME.in, BASENAME.geo, BASENAME.inp '''
    # leaving it external at the moment since it might be practical to use it without having to create a Bfdtd object
    if BASENAME is None:
      BASENAME = os.path.splitext(os.path.basename(fileName))[0]
    GEOcommand(fileName, BASENAME)
    return
    
  def writeShellScript(self, fileName, EXE='fdtd', WORKDIR='$JOBDIR', overwrite=True):
    ''' Generate .sh file '''
    
    #if BASENAME is None:
      #BASENAME = os.path.splitext(os.path.basename(fileName))[0]
    #GEOshellscript(fileName, BASENAME, EXE, WORKDIR, self.WALLTIME, overwrite=overwrite)
    GEOshellscript(fileName, self.getFileBaseName(), EXE, WORKDIR, self.getWallTime(), overwrite=overwrite)
    
    #probe_col = 0
    #if self.excitation.E == [1,0,0]:
      #probe_col = 2
    #elif self.excitation.E == [0,1,0]:
      #probe_col = 3
    #elif self.excitation.E == [0,0,1]:
      #probe_col = 4
    #else:
      #print('ERROR : Unknown Excitation type')
      #sys.exit(-1)
    #GEOshellscript_advanced(fileName, BASENAME, probe_col, EXE, WORKDIR, WALLTIME)
    return
    
  def getMemoryRequirements(self):
    '''
    Return an estimate of the required memory to run the simulation.
    
    At the moment, this is based on a fit of the data returned by Gema3 for various simulations and only depends on the number of cells.
    In reality, the memory used (and the speed) will also depend on the number of probes and snapshots used and is likely to be much higher.
    
    ``memory required in Bytes = p1*x + p0``, where x = number of cells, with:

      * p1 = 37.74864
      * p0 = 14153702.89349
    '''
    x = self.getNcells()
    p1 = 37.747
    p0 = 1.4147e+07
    required_memory = p1*x + p0
    return(required_memory)
    
  def runSimulation(self, simdir='.', simname=None, verbosity=None):
    '''Writes the simulation files into simdir and runs a simulation there.'''
    if verbosity is None:
      verbosity = self.verbosity
    inFileName = self.writeAll(simdir, simname)
    runSimulation(self.BFDTD_executable, inFileName, verbosity=verbosity)

  def getOutputFileNames(self, fsnap_time_number=0, tsnap_time_number=0):
    '''
    Print out names of all output files that will be generated.
    '''
    fsnapshot_file_names = []
    tsnapshot_file_names = []
    esnapshot_file_names = []
    probe_file_names = []

    probe_ident = self.getIdString()
    mesh = self.getMesh()
    fsnap_numID = 1
    tsnap_numID = 1

    for snapshot in self.getFrequencySnapshots():
      (snap_list, fsnap_numID, tsnap_numID) = snapshot.getFileNames(fsnap_numID, tsnap_numID, probe_ident, fsnap_time_number)
      fsnapshot_file_names.extend(snap_list)

    # We need to filter based on class, because there is no difference between time and epsilon snapshots when numbering
    for snapshot in self.getTimeSnapshots(filterBasedOnClass=True):
      (snap_list, fsnap_numID, tsnap_numID) = snapshot.getFileNames(fsnap_numID, tsnap_numID, probe_ident, tsnap_time_number)
      if snapshot.getTypeBasedOnAttributes() == EpsilonSnapshot:
        esnapshot_file_names.extend(snap_list)
      else:
        tsnapshot_file_names.extend(snap_list)
    
    return (fsnapshot_file_names, tsnapshot_file_names, esnapshot_file_names, probe_file_names)
  
  def getLatestFrequencySnapTimeNumber(self, Nmax=100):
    '''
    Returns the highest snap_time_number for which all output files have been generated.
    
    .. note:: It does this by incrementing snap_time_number from 0 and stopping as soon as all output files for the current snap_time_number cannot be found.
      This means that if snapshots for earlier snap_time_number values have been deleted, the result might not be what you expect.
    
    If it cannot find output files for snap_time_number=0, it will return -1.
    '''
    
    if not self.getFrequencySnapshots():
      raise Exception('No frequency snapshots defined.')
    
    latest = -1
    for N in range(Nmax):
      (fsnapshot_file_names, tsnapshot_file_names, esnapshot_file_names, probe_file_names) = self.getOutputFileNames(fsnap_time_number=N)
      if all([os.path.exists(i) for i in fsnapshot_file_names]):
        latest = N
        
    if latest < 0 and self.verbosity > 3:
      print('No frequency snapshots found with SnapTimeNumber <= (Nmax={}).'.format(Nmax))
      
    return(latest)
      
    #N = 0
    #if self.verbosity > 3:
      #print('self.getOutputFileNames({})[0] = {}'.format(N, self.getOutputFileNames(N)[0]))
    
    #while all([os.path.exists(i) for i in self.getOutputFileNames(N)[0]]):
      #N += 1
      #if N > 100:
        #print('No frequency snapshots found with SnapTimeNumber <= 100.')
        #return(-1)
        #break
    #return(N-1)
  
  def sampleFunction(self, sampling_function, destdir='.'):
    '''
    Sample a function over the current mesh, i.e. generate .prn output files based on a sampling function of the form (epsilon, E, H) = f(x,y,z,t).
    
    This is mainly for testing postprocessing tools with known input but can of course be used for anything else.
    
    .. todo:: Should take in time via physical time? iteration index? "snapshot repetition index"?
    '''
    mesh = self.getMesh()
    for snapshot in self.getSnapshots():
      snapshot.write_data(sampling_function, mesh=mesh, numID = 1, probe_ident = self.getIdString(), snap_time_number = 0, destdir=destdir)
    return

  #def readDataEpsilon(self, snap_time_number=0):
    
    #mesh = self.getMesh()
    #probe_ident = self.getIdString()

    #fsnap_numID = 1
    #tsnap_numID = 1
    
    #for snapshot in self.getSnapshots():
      #if isinstance(snapshot, TimeSnapshot):
        #if snapshot.eps == 1:
          #(self.data_epsilon, fsnap_numID, tsnap_numID) = snapshot.read_data(self.data_epsilon, mesh, fsnap_numID, tsnap_numID, probe_ident, snap_time_number, self.dataPaths)
        #else:
          ## TODO: properly get number of snapshots
          #tsnap_numID += 1        
      #pass

    #print(self.data_epsilon)

    #return

  #def readData(self, snap_time_number=0, testrun=False):
    #'''
    #.. todo:: Automatically determine snap_time_number_max...
    #'''
    #Nx = len(self.getXmesh())
    #Ny = len(self.getYmesh())
    #Nz = len(self.getZmesh())

    ##self.data_epsilon = numpy.zeros([Nx,Ny,Nz], dtype=float)
    #data_tsnap = numpy.zeros([Nx,Ny,Nz], dtype=[('E', float, 3), ('H', float, 3), ('Pow', float), ('material', float)])
    #data_fsnap = numpy.zeros([Nx,Ny,Nz], dtype=[('E', complex, 3), ('H', complex, 3)])
    
    #mesh = self.getMesh()
    #probe_ident = self.getIdString()
    
    #(all_time_snapshots, time_snapshots, epsilon_snapshots, mode_filtered_probes) = self.getAllTimeSnapshots(filterBasedOnClass=False)

    #fsnap_numID = 1
    #tsnap_numID = 1

    #for idx, snapshot in enumerate(all_time_snapshots):
      #(data_tsnap, fsnap_numID, tsnap_numID) = snapshot.read_data(data_tsnap, mesh, fsnap_numID, tsnap_numID, probe_ident, snap_time_number, self.dataPaths, testrun)

    #for idx, snapshot in enumerate(self.getFrequencySnapshots()):
      #(data_fsnap, fsnap_numID, tsnap_numID) = snapshot.read_data(data_fsnap, mesh, fsnap_numID, tsnap_numID, probe_ident, snap_time_number, self.dataPaths, testrun)

    ##for snapshot in self.getSnapshots():
      ##(self.data, fsnap_numID, tsnap_numID) = snapshot.read_data(self.data, mesh, fsnap_numID, tsnap_numID, probe_ident, snap_time_number, self.dataPaths)
      ##if isinstance(snapshot, TimeSnapshot):
        ##if snapshot.getTypeBasedOnAttributes() == 
      ##if isinstance(snapshot, FrequencySnapshot):
          ##(self.data_epsilon, fsnap_numID, tsnap_numID) = snapshot.read_data(self.data_epsilon, mesh, fsnap_numID, tsnap_numID, probe_ident, snap_time_number, self.dataPaths)
      ##pass

    #self.data_time_snapshots = [data_tsnap]
    #self.data_frequency_snapshots = [data_fsnap]
    
    ##print('time data')
    ##print(data_tsnap)

    ##print('frequency data')
    ##print(data_fsnap)
    
    ##print(self.data)

    #return

  def readDataTimeSnapshots(self, snap_time_number=0, testrun=False):
    Nx = len(self.getXmesh())
    Ny = len(self.getYmesh())
    Nz = len(self.getZmesh())
    mesh = self.getMesh()
    probe_ident = self.getIdString()

    data_tsnap = numpy.zeros([Nx,Ny,Nz], dtype=[('E', float, 3), ('H', float, 3), ('Pow', float), ('material', float)])
    
    (all_time_snapshots, time_snapshots, epsilon_snapshots, mode_filtered_probes) = self.getAllTimeSnapshots(filterBasedOnClass=False)

    fsnap_numID = 1
    tsnap_numID = 1

    Nsnaps = len(all_time_snapshots)
    for idx, snapshot in enumerate(all_time_snapshots):
      print('reading snapshot {}/{}'.format(idx+1, Nsnaps))
      (data_tsnap, fsnap_numID, tsnap_numID) = snapshot.read_data(data_tsnap, mesh, fsnap_numID, tsnap_numID, probe_ident, snap_time_number, self.dataPaths, testrun)

    self.data_time_snapshots[snap_time_number] = data_tsnap

    return

  def readDataFrequencySnapshots(self, snap_time_number=0, testrun=False):
    Nx = len(self.getXmesh())
    Ny = len(self.getYmesh())
    Nz = len(self.getZmesh())
    mesh = self.getMesh()
    probe_ident = self.getIdString()

    data_fsnap = numpy.zeros([Nx,Ny,Nz], dtype=[('E', complex, 3), ('H', complex, 3)])
    
    fsnap_numID = 1
    tsnap_numID = 1

    all_freq_snapshots = self.getFrequencySnapshots()
    Nsnaps = len(all_freq_snapshots)
    for idx, snapshot in enumerate(all_freq_snapshots):
      print('reading snapshot {}/{}'.format(idx+1, Nsnaps))
      (data_fsnap, fsnap_numID, tsnap_numID) = snapshot.read_data(data_fsnap, mesh, fsnap_numID, tsnap_numID, probe_ident, snap_time_number, self.dataPaths, testrun)

    self.data_frequency_snapshots[snap_time_number] = data_fsnap
    
    return

  def writeHDF5(self, h5file):
    import h5py
    with h5py.File(h5file, "w") as f:
      
      print('writing to ' + h5file)

      #dset = f.create_dataset("description", (), dtype="S29")
      #dset[...] = 'dielectric function, epsilon'

      dset = f.create_dataset("description", data = numpy.string_('Bristol FDTD data'))
      
      #description = 'Bristol FDTD data'
      ##dset = f.create_dataset("description", (), dtype='S{}'.format(len(description)))
      #dset = f.create_dataset("description", (), dtype='S18')
      #dset[...] = description

      #dset = f.create_dataset("description", data='Bristol FDTD data')
      #dset[...] = 'Bristol FDTD data'

      a1 = array([1,0,0])
      a2 = array([0,1,0])
      a3 = array([0,0,1])
      lattice_vectors = numpy.array([a1, a2, a3])
      dset = f.create_dataset('/lattice vectors', data=lattice_vectors)

      dset = f.create_dataset('/xmesh', data=self.getXmesh())
      dset = f.create_dataset('/ymesh', data=self.getYmesh())
      dset = f.create_dataset('/zmesh', data=self.getZmesh())
      
      probe_group = f.create_group("/probes")
      tsnap_group = f.create_group("/time_snapshots")
      fsnap_group = f.create_group("/frequency_snapshots")
      
      if self.data_time_snapshots:
        for snap_time_number, tsnap in self.data_time_snapshots.items():
          dset = tsnap_group.create_dataset('tsnap_{:03d}'.format(snap_time_number), data=tsnap)

      if self.data_frequency_snapshots:
        for snap_time_number, fsnap in self.data_frequency_snapshots.items():
          dset = fsnap_group.create_dataset('fsnap_{:03d}'.format(snap_time_number), data=fsnap)
        
      #dset = f.create_dataset('/epsilon', data=self.data_epsilon)
          
    return

  def writeTorqueJobDirectory(self, destdir, overwrite=True):
    '''
    Generate .in, .inp, .geo and .sh files in directory *destdir* (it will be created if it doesn't exist).
    
    This function was created as a replacement for writeAll and makes it easier to generate the desired .sh file to be submitted with qsub.
    
    .. note:: The destination directory will be created if it does not exist.
    '''

    geoFile = destdir + os.sep + self.fileBaseName+'.geo'
    inpFile = destdir + os.sep + self.fileBaseName+'.inp'
    inFile = destdir + os.sep + self.fileBaseName+'.in'
    shFile = destdir + os.sep + self.fileBaseName+'.sh'

    if not overwrite:
      msg = 'These files already exist in ' + destdir + ' :\n'
      files_exist = False
      for i in [geoFile, inpFile, inFile, shFile]:
        if os.path.exists(i):
          msg += '- ' + os.path.basename(i) + '\n'
          files_exist = True
      if files_exist:
        raise UserWarning(msg)
      
    self.writeAll(destdir, fileBaseName=self.fileBaseName, overwrite=overwrite)
    #self.writeShellScript(shFile, BASENAME=self.fileBaseName, EXE=self.BFDTD_executable, WORKDIR=self.WORKDIR, WALLTIME=self.WALLTIME, overwrite=overwrite)
    self.writeShellScript(shFile, EXE=self.BFDTD_executable, WORKDIR=self.WORKDIR, overwrite=overwrite)
    return
  
  def writeAll(self, newDirName, fileBaseName=None, withGeom=True, writeShellScriptFunction=None, overwrite=True):
    '''
    Generate .in,.inp,.geo,.cmd,.sh files in directory newDirName (it will be created if it doesn't exist)
    
    .. note:: Please use writeTorqueJobDirectory if you wish to prepare a job directory for submission with qsub.
    '''
    
    newDirName = os.path.expanduser(newDirName).rstrip('/') # replace ~ or similar and remove any trailing '/'
    
    #use_makedirs=False
    if not os.path.isdir(newDirName):
      os.makedirs(newDirName)
      #if use_makedirs:
        #os.makedirs(newDirName)
      #else:
        #os.mkdir(newDirName)

    if fileBaseName is None:
      fileBaseName = self.fileBaseName
      #fileBaseName = os.path.basename(os.path.abspath(newDirName))
    
    #print('fileBaseName = '+fileBaseName)
    
    geoFileName = newDirName+os.sep+fileBaseName+'.geo'
    inpFileName = newDirName+os.sep+fileBaseName+'.inp'
    inFileName = newDirName+os.sep+fileBaseName+'.in'
    cmdFileName = newDirName+os.sep+fileBaseName+'.cmd'
    shFileName = newDirName+os.sep+fileBaseName+'.sh'

    if not self.fileList:
      self.fileList = [fileBaseName+'.inp',fileBaseName+'.geo']
    
    self.writeGeoFile(geoFileName, withGeom = withGeom, overwrite=overwrite)
    self.writeInpFile(inpFileName, overwrite=overwrite)
    self.writeFileList(inFileName, self.fileList, overwrite=overwrite)
    self.writeDatFiles(newDirName, overwrite=overwrite)
    
    if writeShellScriptFunction:
      writeShellScriptFunction(shFileName, overwrite=overwrite)
      #self.writeCondorScript(cmdFileName)
    
    return(inFileName)
  
  def fitBox(self, vec6):
    ''' Changes the limits of the box to fit the geometry. Moves all other things as necessary to have box min be [0,0,0] (necessary?).
    
    .. todo:: Finish this function.
    '''
    raise Exception('fitBox not working yet')
    return
  
  def calculateMeshingParameters(self, minimum_mesh_delta_vector3):
    '''
    Returns a MeshingParameters object that can be used for meshing.
    
    It uses the *getMeshingParameters()* function and *useForMeshing* attribute of the various BFDTD objects.
    
    minimum_mesh_delta_vector3 : smallest cell size acceptable in the mesh. Because too small cells can cause Bristol FDTD to crash.
    
    meshing_parameters attributes:
    
      * meshing_parameters.maxPermittivityVector_X
      * meshing_parameters.thicknessVector_X
      * meshing_parameters.maxPermittivityVector_Y
      * meshing_parameters.thicknessVector_Y
      * meshing_parameters.maxPermittivityVector_Z
      * meshing_parameters.thicknessVector_Z
    '''

    (simMinX, simMinY, simMinZ) = self.box.lower
    (simMaxX, simMaxY, simMaxZ) = self.box.upper

    # Xvec, Yvec, Zvec are arrays of size (N,2) containing a list of (lower,upper) pairs corresponding to the meshing subdomains defined by the various geometrical objects.
    # epsX, epsY, epsZ are arrays of size (N,1) containing a list of epsilon values corresponding to the meshing subdomains defined by the various geometrical objects.
    # The (lower,upper) pairs from Xvec,Yvec,Zvec are associated with the corresponding epsilon values from epsX,epsY,epsZ to determine an appropriate mesh in the X,Y,Z directions respectively.

    # box mesh
    Xvec = numpy.array([[simMinX, simMaxX]])
    Yvec = numpy.array([[simMinY, simMaxY]])
    Zvec = numpy.array([[simMinZ, simMaxZ]])
    
    epsX = numpy.array([[1]])
    epsY = numpy.array([[1]])
    epsZ = numpy.array([[1]])

    # geometry object meshes
    for obj in self.geometry_object_list:
      if obj.useForMeshing:
        if self.verboseMeshing:
          print(obj.name)
          print((Xvec,Yvec,Zvec,epsX,epsY,epsZ))
        Xvec,Yvec,Zvec,epsX,epsY,epsZ = obj.getMeshingParameters(Xvec,Yvec,Zvec,epsX,epsY,epsZ)
        if self.verboseMeshing:
          print((Xvec,Yvec,Zvec,epsX,epsY,epsZ))

    # mesh object meshes
    for obj in self.mesh_object_list:
      if obj.useForMeshing:
        Xvec,Yvec,Zvec,epsX,epsY,epsZ = obj.getMeshingParameters(Xvec,Yvec,Zvec,epsX,epsY,epsZ)

    # excitation object meshes
    if self.fitMeshToExcitations:
      for obj in self.excitation_list:
        if obj.useForMeshing:
          Xvec,Yvec,Zvec,epsX,epsY,epsZ = obj.getMeshingParameters(Xvec,Yvec,Zvec,epsX,epsY,epsZ)

    # probe object meshes
    if self.fitMeshToProbes:
      for obj in self.probe_list:
        if obj.useForMeshing:
          Xvec,Yvec,Zvec,epsX,epsY,epsZ = obj.getMeshingParameters(Xvec,Yvec,Zvec,epsX,epsY,epsZ)

    # snapshot object meshes
    if self.fitMeshToSnapshots:
      for obj in self.snapshot_list:
        if obj.useForMeshing:
          Xvec,Yvec,Zvec,epsX,epsY,epsZ = obj.getMeshingParameters(Xvec,Yvec,Zvec,epsX,epsY,epsZ)
    
    # postprocess the meshes
    Xvec[Xvec<simMinX] = simMinX
    Xvec[Xvec>simMaxX] = simMaxX
    Yvec[Yvec<simMinY] = simMinY
    Yvec[Yvec>simMaxY] = simMaxY
    Zvec[Zvec<simMinZ] = simMinZ
    Zvec[Zvec>simMaxZ] = simMaxZ

    ##
    VX = numpy.unique(numpy.sort(numpy.vstack([Xvec[:,0],Xvec[:,1]])))
    MX = numpy.zeros((Xvec.shape[0],len(VX)))

    for m in range(Xvec.shape[0]):
      indmin = numpy.nonzero(VX==Xvec[m,0])[0][0]
      indmaX = numpy.nonzero(VX==Xvec[m,1])[0][0]
      eps = epsX[m,0]
      vv = numpy.zeros(len(VX))
      vv[indmin:indmaX] = eps
      MX[m,:] = vv
  
    thicknessVX = numpy.diff(VX)
    epsVX = MX[:,0:MX.shape[1]-1]
    epsVX = epsVX.max(0)

    ##
    VY = numpy.unique(numpy.sort(numpy.vstack([Yvec[:,0],Yvec[:,1]])))
    MY = numpy.zeros((Yvec.shape[0],len(VY)))

    for m in range(Yvec.shape[0]):
      indmin = numpy.nonzero(VY==Yvec[m,0])[0][0]
      indmax = numpy.nonzero(VY==Yvec[m,1])[0][0]
      eps = epsY[m,0]
      vv = numpy.zeros(len(VY))
      vv[indmin:indmax] = eps
      MY[m,:] = vv
  
    thicknessVY = numpy.diff(VY)
    epsVY = MY[:,0:MY.shape[1]-1]
    epsVY = epsVY.max(0)

    ##
    VZ = numpy.unique(numpy.sort(numpy.vstack([Zvec[:,0],Zvec[:,1]])))
    MZ = numpy.zeros((Zvec.shape[0],len(VZ)))

    for m in range(Zvec.shape[0]):
      indmin = numpy.nonzero(VZ==Zvec[m,0])[0][0]
      indmax = numpy.nonzero(VZ==Zvec[m,1])[0][0]
      eps = epsZ[m,0]
      vv = numpy.zeros(len(VZ))
      vv[indmin:indmax] = eps
      MZ[m,:] = vv
  
    thicknessVZ = numpy.diff(VZ)
    epsVZ = MZ[:,0:MZ.shape[1]-1]
    epsVZ = epsVZ.max(0)
        
    ##############################################
    meshing_parameters = MeshingParameters()
    meshing_parameters.maxPermittivityVector_X = []
    meshing_parameters.thicknessVector_X = []
    meshing_parameters.maxPermittivityVector_Y = []
    meshing_parameters.thicknessVector_Y = []
    meshing_parameters.maxPermittivityVector_Z = []
    meshing_parameters.thicknessVector_Z = []
    
    # TODO: use (thickness, epsilon) tuples so that filter() and similar functions can be used. Also prevents errors if lists have different lengths.
    # ex: t = filter(lambda x: x>=1, t)
    # filter out parts smaller than minimum_mesh_delta_vector3[i]
    for idx in range(len(thicknessVX)):
      if thicknessVX[idx] >= minimum_mesh_delta_vector3[0]:
        meshing_parameters.maxPermittivityVector_X.append(epsVX[idx])
        meshing_parameters.thicknessVector_X.append(thicknessVX[idx])
    for idx in range(len(thicknessVY)):
      if thicknessVY[idx] >= minimum_mesh_delta_vector3[1]:
        meshing_parameters.maxPermittivityVector_Y.append(epsVY[idx])
        meshing_parameters.thicknessVector_Y.append(thicknessVY[idx])
    for idx in range(len(thicknessVZ)):
      if thicknessVZ[idx] >= minimum_mesh_delta_vector3[2]:
        meshing_parameters.maxPermittivityVector_Z.append(epsVZ[idx])
        meshing_parameters.thicknessVector_Z.append(thicknessVZ[idx])
    
    return meshing_parameters
  
  def autoMeshGeometryWithMaxNumberOfCells(self, Lambda, MAXCELLS = 1e7, a_min = 1, a_step = 1, a_start = 10):
    '''
    Calls autoMeshGeometry(Lambda/a) until it finds the biggest value of *a* (i.e. smallest cell size) so that Ncells < MAXCELLS.
    
    Returns the final value used for a.
    '''
    a = a_start
    self.autoMeshGeometry(Lambda/a)
    #print(self.getNcells()<MAXCELLS)
    while( self.getNcells() < MAXCELLS ):
      #print(a)
      a = a + a_step
      self.autoMeshGeometry(Lambda/a)
    while( self.getNcells() > MAXCELLS and a - a_step >= a_min ):
      a = a - a_step
      self.autoMeshGeometry(Lambda/a)
    return(a)
    
  def autoMeshGeometry(self, meshing_factor, minimum_mesh_delta_vector3 = [1e-3,1e-3,1e-3]):
    ''' Automatically mesh geometry so that the max cell size is meshing_factor*1/n in each object. '''
    meshing_parameters = self.calculateMeshingParameters(minimum_mesh_delta_vector3)
    if self.verboseMeshing:
      print('=== meshing_parameters ===')
      print(meshing_parameters)
      print('meshing_factor*1./numpy.sqrt(meshing_parameters.maxPermittivityVector_X) = '+str(meshing_factor*1./numpy.sqrt(meshing_parameters.maxPermittivityVector_X)))
      print('meshing_factor*1./numpy.sqrt(meshing_parameters.maxPermittivityVector_Y) = '+str(meshing_factor*1./numpy.sqrt(meshing_parameters.maxPermittivityVector_Y)))
      print('meshing_factor*1./numpy.sqrt(meshing_parameters.maxPermittivityVector_Z) = '+str(meshing_factor*1./numpy.sqrt(meshing_parameters.maxPermittivityVector_Z)))
      print('==========================')
    delta_X_vector, local_delta_X_vector = subGridMultiLayer(meshing_factor*1./numpy.sqrt(meshing_parameters.maxPermittivityVector_X), meshing_parameters.thicknessVector_X)
    delta_Y_vector, local_delta_Y_vector = subGridMultiLayer(meshing_factor*1./numpy.sqrt(meshing_parameters.maxPermittivityVector_Y), meshing_parameters.thicknessVector_Y)
    delta_Z_vector, local_delta_Z_vector = subGridMultiLayer(meshing_factor*1./numpy.sqrt(meshing_parameters.maxPermittivityVector_Z), meshing_parameters.thicknessVector_Z)
    self.mesh.setXmeshDelta(delta_X_vector)
    self.mesh.setYmeshDelta(delta_Y_vector)
    self.mesh.setZmeshDelta(delta_Z_vector)
    if self.verboseMeshing > 10:
      print('=== mesh ===')
      print(self.mesh)
      print('============')
    return
  
  def rotate(self, axis_point, axis_direction, angle_degrees):
    # .. todo:: Will only work for cylinders at the moment. (objects currently need to call parent class rotate function)
    for obj in self.geometry_object_list:
      obj.rotate(axis_point, axis_direction, angle_degrees)
    return
    
  def translate(self, vec3):
    # .. todo:: translate rotations? (assuming they remain separate from the object they apply to, which really, they should not)
    for obj in self.geometry_object_list:
      obj.translate(vec3)
    return
    
  def applyTransformationMatrix(self, M):
    # .. todo:: finish this
    return

# mandatory objects
class Flag(BFDTDentry):
  '''
  * iterationMethod: Set to 1 if FDTD/PEEC is wanted
  * propagationConstant: Propagation constant for two dimensional runs
  * flagOne: Set to 1 to use the Celuch method for dealing with curved dielectrics
  * flagTwo: Set to:
  
    1. Set to specify a two dimensional simulation
    2. Specify Static Field Solutions for metal strips
    3. Specify Pre-calculated Correction Factors for metal strips
    4. Specify MAMPs
  
  * iterations: Number of iterations required
  * timeStepFactor: Time step as a proportion of the maximum allowed
  * id_string: Probe identifier, “id”
  * 8: Set to 1 to ask for a file to be produced for input to the POVRAY ray tracing program
  
  .. todo:: This class could easily be integrated into the BFDTDobject class...
  '''
  def __init__(self):
    self.name = 'flag'
    self.layer = 'flag'
    self.group = 'flag'
    self.iterationMethod = 5
    self.propagationConstant = 0
    self.flagOne = 0
    self.flagTwo = 0
    self.iterations = 1
    self.timeStepFactor = 0.9; #mus
    self.id_string = '_id_'
  
  def getIdString(self):
    return(self.id_string)
  def setIdString(self, id_string):
    self.id_string = id_string
  
  def setIterations(self, iterations):
    '''Sets the number of iterations.'''
    self.iterations = int(iterations)

  def getIterations(self):
    '''Returns the number of iterations.'''
    return(int(self.iterations))
    
  def set2D(self):
    self.flagTwo = 1
    self.propagationConstant = 1
    return
  def set3D(self):
    self.flagTwo = 0
    return
    
  def setTimeStepFactor(self, timeStepFactor):
    if timeStepFactor > 1:
      raise Exception('timeStepFactor = {} > 1'.format(timeStepFactor))
    self.timeStepFactor = timeStepFactor
    return

  def getTimeStepFactor(self):
    return self.timeStepFactor
  
  def __str__(self):
    ret  = 'name = '+self.name+'\n'
    ret += 'iMethod = ' + str(self.iterationMethod) + '\n' +\
    'propCons = ' + str(self.propagationConstant) + '\n' +\
    'flagOne = ' + str(self.flagOne) + '\n' +\
    'flagTwo = ' + str(self.flagTwo) + '\n' +\
    'iterations = ' + str(self.iterations) + '\n' +\
    'timeStepFactor = ' + str(self.timeStepFactor) + '\n' +\
    'id = ' + self.id_string
    return ret
  def read_entry(self, entry):
    if entry.name:
      self.name = entry.name
    self.iterationMethod = float(entry.data[0])
    self.propagationConstant = float(entry.data[1])
    self.flagOne = float(entry.data[2])
    self.flagTwo = float(entry.data[3])
    self.iterations = int(float(entry.data[4])) # is there a more direct way to convert to int? :/
    self.timeStepFactor = float(entry.data[5])
    self.id_string = entry.data[6].strip('"')
  def write_entry(self, FILE=sys.stdout):
    
    # BFDTD does not run if more than 5.5e11~2^39  iterations?
    #   184624273416 = 1.8462e+11 -> no run
    #   5.5e11 -> runs ok???
    # .. todo:: figure out these weird BFDTD bugs... Contact Railton...
    if self.getIterations() > 1e9:
      raise Exception('Too many iterations requested. BFDTD may not run any in this case... Also, do you really want that many?')
    
    if self.timeStepFactor > 1:
      raise Exception('self.timeStepFactor = {} > 1'.format(self.timeStepFactor))
    
    FILE.write('FLAG  **name='+self.name+'\n')
    FILE.write('{\n')
    FILE.write("%d **ITERATION METHOD\n" % self.iterationMethod)
    FILE.write("%E **PROPAGATION CONSTANT (IGNORED IN 3D MODEL)\n" % self.propagationConstant)
    FILE.write("%d **FLAG ONE\n" % self.flagOne)
    FILE.write("%d **FLAG TWO\n" % self.flagTwo)
    FILE.write("%d **ITERATIONS\n" % self.iterations)
    FILE.write("%E **TIMESTEP as a proportion of the maximum allowed\n" % self.timeStepFactor)
    FILE.write("\"%s\" **ID CHARACTER (ALWAYS USE QUOTES)\n" % self.id_string.strip('"'))
    FILE.write('}\n')
    FILE.write('\n')

class Boundaries(BFDTDentry):
  '''
  The following ABC algorithms are available in the FDTD program:
  
    * 0. Magnetic Wall
    * 1. Metal wall. -> "symmetry wall"
    * 2. Mur 1st. -> default setting
    * 6. Dispersive.
    * 7. Higdon 1st.
    * 9. Higdon 2nd
    * 10. PML
  
  The parameters are for the second order and Perfectly Matched Layer boundary conditions and have the following meanings:
  
    * i. Dispersive ABC Parameter 1 and parameter2 are the values of effective permittivity for which perfect absorption may be expected
    * ii. Higdon ABC Parameter 1 and parameter 2 are the values for the angle of incidence ( in degrees ) at which perfect absorption may be expected
    * iii. PML Parameter 1 is the number of layers in the PML region, parameter 2 is the grading index, normally 2, parameter 3 is the minimum reflection coefficient, try 0.01 - 0.001. This is not critical.

  If you want to make the BFDTD simulations run faster, you can exploit the symmetry of the structure by putting the simulation box over only one half of the pillar and use a metallic wall at the symmetry boundary.
    
  .. todo:: "ABC" = Absorbing Boundary Conditions?
  .. todo:: Integrate in BFDTDobject?
  .. todo:: Add support for alphabetic names like 'PML', 'Metal wall', etc for code clarity. + setBoundaryConditionsZneg(ABC), etc functions
  '''
  def __init__(self):
    self.name = 'boundaries'
    self.layer = 'boundaries'
    self.group = 'boundaries'

    # PML=10, symmetry=1, normal=2
    self.setBoundaryConditionsNormal()
    
  def setBoundaryConditionsXposToPML(self, number_of_layers=8, grading_index=2, min_reflection_coeff=1e-3):
    self.Xpos_bc = 10
    self.Xpos_param = [ number_of_layers, grading_index, min_reflection_coeff ]
  def setBoundaryConditionsYposToPML(self, number_of_layers=8, grading_index=2, min_reflection_coeff=1e-3):
    self.Ypos_bc = 10
    self.Ypos_param = [ number_of_layers, grading_index, min_reflection_coeff ]
  def setBoundaryConditionsZposToPML(self, number_of_layers=8, grading_index=2, min_reflection_coeff=1e-3):
    self.Zpos_bc = 10
    self.Zpos_param = [ number_of_layers, grading_index, min_reflection_coeff ]
  def setBoundaryConditionsXnegToPML(self, number_of_layers=8, grading_index=2, min_reflection_coeff=1e-3):
    self.Xneg_bc = 10
    self.Xneg_param = [ number_of_layers, grading_index, min_reflection_coeff ]
  def setBoundaryConditionsYnegToPML(self, number_of_layers=8, grading_index=2, min_reflection_coeff=1e-3):
    self.Yneg_bc = 10
    self.Yneg_param = [ number_of_layers, grading_index, min_reflection_coeff ]
  def setBoundaryConditionsZnegToPML(self, number_of_layers=8, grading_index=2, min_reflection_coeff=1e-3):
    self.Zneg_bc = 10
    self.Zneg_param = [ number_of_layers, grading_index, min_reflection_coeff ]
    
  def setBoundaryConditionsToPML(self, number_of_layers=8, grading_index=2, min_reflection_coeff=1e-3):
    '''
    Sets all boundaries to PML.
    '''
    self.setBoundaryConditionsXnegToPML(number_of_layers, grading_index, min_reflection_coeff)
    self.setBoundaryConditionsYnegToPML(number_of_layers, grading_index, min_reflection_coeff)
    self.setBoundaryConditionsZnegToPML(number_of_layers, grading_index, min_reflection_coeff)
    self.setBoundaryConditionsXposToPML(number_of_layers, grading_index, min_reflection_coeff)
    self.setBoundaryConditionsYposToPML(number_of_layers, grading_index, min_reflection_coeff)
    self.setBoundaryConditionsZposToPML(number_of_layers, grading_index, min_reflection_coeff)

  def setBoundaryConditionsNormal(self):
    self.Xpos_bc = 2
    self.Ypos_bc = 2
    self.Zpos_bc = 2
    self.Xneg_bc = 2
    self.Yneg_bc = 2
    self.Zneg_bc = 2

    self.Xpos_param = [1,1,0]
    self.Ypos_param = [1,1,0]
    self.Zpos_param = [1,1,0]
    self.Xneg_param = [1,1,0]
    self.Yneg_param = [1,1,0]
    self.Zneg_param = [1,1,0]
    
  def __str__(self):
    ret  = 'name = '+self.name+'\n'
    ret += 'X+: Type = '+str(self.Xpos_bc)+' parameters = '+str(self.Xpos_param)+'\n'
    ret += 'Y+: Type = '+str(self.Ypos_bc)+' parameters = '+str(self.Ypos_param)+'\n'
    ret += 'Z+: Type = '+str(self.Zpos_bc)+' parameters = '+str(self.Zpos_param)+'\n'
    ret += 'X-: Type = '+str(self.Xneg_bc)+' parameters = '+str(self.Xneg_param)+'\n'
    ret += 'Y-: Type = '+str(self.Yneg_bc)+' parameters = '+str(self.Yneg_param)+'\n'
    ret += 'Z-: Type = '+str(self.Zneg_bc)+' parameters = '+str(self.Zneg_param)
    return ret
  def read_entry(self,entry):
    if entry.name:
      self.name = entry.name
    i = 0
    if len(entry.data) == 6:
      self.Xpos_bc = int(entry.data[i]); self.Xpos_param = float_array([1,1,0]); i+=1
      self.Ypos_bc = int(entry.data[i]); self.Ypos_param = float_array([1,1,0]); i+=1
      self.Zpos_bc = int(entry.data[i]); self.Zpos_param = float_array([1,1,0]); i+=1
      self.Xneg_bc = int(entry.data[i]); self.Xneg_param = float_array([1,1,0]); i+=1
      self.Yneg_bc = int(entry.data[i]); self.Yneg_param = float_array([1,1,0]); i+=1
      self.Zneg_bc = int(entry.data[i]); self.Zneg_param = float_array([1,1,0]); i+=1
    elif len(entry.data) == 24:
      self.Xpos_bc = int(entry.data[4*i]); self.Xpos_param = float_array(entry.data[1+4*i:4+4*i]); i+=1
      self.Ypos_bc = int(entry.data[4*i]); self.Ypos_param = float_array(entry.data[1+4*i:4+4*i]); i+=1
      self.Zpos_bc = int(entry.data[4*i]); self.Zpos_param = float_array(entry.data[1+4*i:4+4*i]); i+=1
      self.Xneg_bc = int(entry.data[4*i]); self.Xneg_param = float_array(entry.data[1+4*i:4+4*i]); i+=1
      self.Yneg_bc = int(entry.data[4*i]); self.Yneg_param = float_array(entry.data[1+4*i:4+4*i]); i+=1
      self.Zneg_bc = int(entry.data[4*i]); self.Zneg_param = float_array(entry.data[1+4*i:4+4*i]); i+=1
    else:
      print('ERROR: incorrect number of elements in boundary object')
      sys.exit(-1)
    return(0)
  def write_entry(self, FILE=sys.stdout):
    FILE.write('BOUNDARY  **name='+self.name+'\n')
    FILE.write('{\n')
    FILE.write("%d %E %E %E **X+\n" % (self.Xpos_bc, self.Xpos_param[0], self.Xpos_param[1], self.Xpos_param[2]))
    FILE.write("%d %E %E %E **Y+\n" % (self.Ypos_bc, self.Ypos_param[0], self.Ypos_param[1], self.Ypos_param[2]))
    FILE.write("%d %E %E %E **Z+\n" % (self.Zpos_bc, self.Zpos_param[0], self.Zpos_param[1], self.Zpos_param[2]))
    FILE.write("%d %E %E %E **X-\n" % (self.Xneg_bc, self.Xneg_param[0], self.Xneg_param[1], self.Xneg_param[2]))
    FILE.write("%d %E %E %E **Y-\n" % (self.Yneg_bc, self.Yneg_param[0], self.Yneg_param[1], self.Yneg_param[2]))
    FILE.write("%d %E %E %E **Z-\n" % (self.Zneg_bc, self.Zneg_param[0], self.Zneg_param[1], self.Zneg_param[2]))
    FILE.write('}\n')
    FILE.write('\n')

class Box(object):
  '''
  .. todo:: It might make sense to make the box some sort of subclass of Block, or fully integrate it into the BFDTDobject since there can only be one box anyway.
  '''
  def __init__(self,
    name = None,
    layer = None,
    group = None,
    lower = None,
    upper = None):

    if name is None: name = 'box'
    if layer is None: layer = 'box',
    if group is None: group = 'box',
    if lower is None: lower = numpy.array([0,0,0])
    if upper is None: upper = numpy.array([1,1,1])
    
    self.name = name
    self.layer = layer
    self.group = group
    self.lower = lower
    self.upper = upper
  
  def setLower(self, lower):
    self.lower = numpy.array(lower)
  
  def setUpper(self, upper):
    self.upper = numpy.array(upper)
  
  def __str__(self):
    ret  = 'name = '+self.name+'\n'
    ret += 'lower = '+str(self.lower)+'\n'
    ret += 'upper = '+str(self.upper)
    return ret
  
  def read_entry(self,entry):
    if entry.name:
      self.name = entry.name
    self.lower = float_array(entry.data[0:3])
    self.upper = float_array(entry.data[3:6])
  
  def write_entry(self, FILE=sys.stdout):
    self.lower, self.upper = fixLowerUpper(self.lower, self.upper)
    FILE.write('BOX  **name='+self.name+'\n')
    FILE.write('{\n')
    FILE.write("%E **XL\n" % self.lower[0])
    FILE.write("%E **YL\n" % self.lower[1])
    FILE.write("%E **ZL\n" % self.lower[2])
    FILE.write("%E **XU\n" % self.upper[0])
    FILE.write("%E **YU\n" % self.upper[1])
    FILE.write("%E **ZU\n" % self.upper[2])
    FILE.write('}\n')
    FILE.write('\n')

  def writeCTL(self, FILE=sys.stdout):
    FILE.write('(set! geometry-lattice (make lattice (size {} {} {})))\n\n'.format(*self.getSize()))
    return
    
  def translate(self, vec3):
    self.lower = numpy.array(self.lower)
    self.upper = numpy.array(self.upper)
    self.lower = self.lower + vec3
    self.upper = self.upper + vec3

  def getCentro(self):
    return numpy.array([ 0.5*(self.lower[0]+self.upper[0]), 0.5*(self.lower[1]+self.upper[1]), 0.5*(self.lower[2]+self.upper[2]) ])
  
  def setCentro(self, nova_centro):
    nova_centro = numpy.array(nova_centro)    
    nuna_centro = self.getCentro()
    self.translate(nova_centro - nuna_centro)
  
  def setExtension(self,lower,upper):
    self.setLower(lower)
    self.setUpper(upper)
    
  def getExtension(self):
    return (self.getLower(), self.getUpper())
      
  def getSize(self):
    return numpy.array(self.upper)-numpy.array(self.lower)
  
  def setSize(self, size_vec3):
    C = self.getCentro()
    self.lower = C - 0.5*numpy.array(size_vec3)
    self.upper = C + 0.5*numpy.array(size_vec3)
    return
    
  # convenience get functions, to get numpy arrays directly
  def getLower(self):
    return numpy.array(self.lower)
  def getUpper(self):
    return numpy.array(self.upper)

class Entry(object):
  def __init__(self):
    self.name = 'default_entry'
    self.layer = 'default_layer'
    self.scene = 'default_scene'
    self.group = 'default_group'
    self.Type = ''
    self.data = [] # .. todo:: Will this ever be used?

if __name__ == '__main__':
	pass
