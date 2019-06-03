#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from configparser import ConfigParser, ExtendedInterpolation, BasicInterpolation
import tempfile
import unittest
from utilities.common import str2list, int_array

import bfdtd.bfdtd_parser as bfdtd
#from bfdtd.meshingparameters import MeshingParameters
from bfdtd.meshobject import *
from GWL.woodpile import *
from meshing.meshing import mergeMeshingParameters, HomogeneousMeshParameters1D

class weijeiWoodpile(BFDTDobject):
  '''
  .. todo:: Maybe merge with GWL/woodpile.py? (which already creates BFDTD output) (and worse: It already uses that class...)
  .. todo:: In the future, we'll probably want various types of objects and export them to BFDTD, GWL, MPB, MEEP, etc Should such objects inherit all the other ones or have them as attributes? Probably have as attributes, or retrievable objects.
  '''
  
  # WARNING: These attributes are bound to the class.
  # Calling something like **weijeiWoodpile.vertical_period=123**, will change the "default value" and any instance of the class created after that will have **vertical_period=123**.
  # It does however allow accessing the default values without having to create an instance, i.e. **weijeiWoodpile.vertical_period** works.
  # cf: http://stackoverflow.com/questions/2681243/how-should-i-declare-default-values-for-instance-variables-in-python
  vertical_period = 1
  refractive_index_defect = 2
  refractive_index_log = 3
  refractive_index_outer = 4
  excitation_direction = 1
  w_factor = 0.1

  defect_on = True
  defect_size_vec3 = [0.2, 0.3, 0.4]
  defect_offset_vec3 = [1, 2, 3]

  defect_envelope_on = True
  defect_envelope_size_vec3 = [0.4, 0.6, 0.8]
  defect_envelope_offset_vec3 = [0.2,0.5,0.7]

  shift_initial_layers = True

  # additional attributes, already in the other woodpile class (classes to be merged)
  interRodDistance = 0.4
  rod_height = 0.2
  rod_width = 0.1

  # some weijeiWoodpile-specific new default values for the BFDTDobject
  DEFAULT_ITERATIONS = 5000000
  DEFAULT_TIMESTEP = 0.95; #mus
  DEFAULT_ID_STRING = '_id_'
  
  def __init__(self):

    # BFDTDobject initialization
    BFDTDobject.__init__(self)

    # some weijeiWoodpile-specific new default values for the BFDTDobject
    self.flag.iterations = self.DEFAULT_ITERATIONS
    self.flag.timeStep = self.DEFAULT_TIMESTEP
    self.flag.id_string = self.DEFAULT_ID_STRING

    # hack variable to support the various defect types
    self.DEFECT_TYPE = 0 # 0 = old integer defects, 1 = defects with 0.25*d step
    self.Lambda = 0.637

  def createXYmesh(self, mid, defect, mesh_d, X_delta_2_nolog, X_delta_4, X_delta_3):
    # X+Y mesh

    MeshParamsList = []

    mid_MPxy = HomogeneousMeshParameters1D(mid[0], mid[0])
    mid_MPxy.setSpacingMax(numpy.inf)
    MeshParamsList.append(mid_MPxy)

    exc_MPxy = HomogeneousMeshParameters1D(mid[0]-mesh_d, mid[0]+mesh_d)
    #exc_MPxy.setSpacingMax(X_delta_0)
    exc_MPxy.setNcellsMin(2)
    MeshParamsList.append(exc_MPxy)

    box_MPxy = HomogeneousMeshParameters1D(self.box.lower[0], self.box.upper[0])
    box_MPxy.setSpacingMax(numpy.inf)
    MeshParamsList.append(box_MPxy)

    if self.DEFECT_TYPE == 0:
      defectsize = defect.getSize()[1]

      # TODO: MERGE_LEFT_OVER: Clean up merge leftover
      ##########
      ## v1: mid[0]+[-0.5*defectsize,+0.5*defectsize]
      #defect_MPxy = HomogeneousMeshParameters1D(mid[0]-0.5*defectsize, mid[0]+0.5*defectsize)
      #defect_MPxy.setNcellsMin(2*5)
      #MeshParamsList.append(defect_MPxy)
      ##########

      ##########
      ## v2: mid[0]+[-1.5*self.interRodDistance-0.5*self.rod_width,-1.5*self.interRodDistance,-0.5*self.interRodDistance,+0.5*self.interRodDistance,+1.5*self.interRodDistance,+1.5*self.interRodDistance+0.5*self.rod_width]
      #defect_MPxy = HomogeneousMeshParameters1D(mid[0]-1.5*self.interRodDistance-0.5*self.rod_width, mid[0]-1.5*self.interRodDistance)
      #defect_MPxy.setSpacingMax(mesh_d)
      #MeshParamsList.append(defect_MPxy)

      #defect_MPxy = HomogeneousMeshParameters1D(mid[0]-1.5*self.interRodDistance, mid[0]-0.5*self.interRodDistance)
      #defect_MPxy.setNcellsMin(2*11)
      #MeshParamsList.append(defect_MPxy)

      #defect_MPxy = HomogeneousMeshParameters1D(mid[0]-0.5*self.interRodDistance, mid[0]+0.5*self.interRodDistance)
      #defect_MPxy.setNcellsMin(2*11)
      #MeshParamsList.append(defect_MPxy)

      #defect_MPxy = HomogeneousMeshParameters1D(mid[0]+0.5*self.interRodDistance, mid[0]+1.5*self.interRodDistance)
      #defect_MPxy.setNcellsMin(2*11)
      #MeshParamsList.append(defect_MPxy)

      #defect_MPxy = HomogeneousMeshParameters1D(mid[0]+1.5*self.interRodDistance, mid[0]+1.5*self.interRodDistance+0.5*self.rod_width)
      #defect_MPxy.setSpacingMax(mesh_d)
      #MeshParamsList.append(defect_MPxy)
      ##########

      ##########
      ## v3: mid[0]+[-1.5*self.interRodDistance-0.5*self.rod_width,-1.5*self.interRodDistance,-0.5*self.interRodDistance,+0.5*self.interRodDistance,+1.5*self.interRodDistance,+1.5*self.interRodDistance+0.5*self.rod_width]
      defect_MPxy = HomogeneousMeshParameters1D(mid[0]-1.5*self.interRodDistance-0.5*self.rod_width, mid[0]-1.5*self.interRodDistance)
      defect_MPxy.setSpacingMax(mesh_d)
      MeshParamsList.append(defect_MPxy)

      defect_MPxy = HomogeneousMeshParameters1D(mid[0]-1.5*self.interRodDistance, mid[0]-0.5*defectsize)
      defect_MPxy.setNcellsMin(2*5)
      MeshParamsList.append(defect_MPxy)

      defect_MPxy = HomogeneousMeshParameters1D(mid[0]-0.5*defectsize, mid[0]-0.25*defectsize)
      defect_MPxy.setNcellsMin(3)
      MeshParamsList.append(defect_MPxy)

      defect_MPxy = HomogeneousMeshParameters1D(mid[0]-0.25*defectsize, mid[0])
      defect_MPxy.setNcellsMin(3)
      MeshParamsList.append(defect_MPxy)

      defect_MPxy = HomogeneousMeshParameters1D(mid[0], mid[0]+0.25*defectsize)
      defect_MPxy.setNcellsMin(3)
      MeshParamsList.append(defect_MPxy)

      defect_MPxy = HomogeneousMeshParameters1D(mid[0]+0.25*defectsize, mid[0]+0.5*defectsize)
      defect_MPxy.setNcellsMin(3)
      MeshParamsList.append(defect_MPxy)

      defect_MPxy = HomogeneousMeshParameters1D(mid[0]+0.5*defectsize, mid[0]+1.5*self.interRodDistance)
      defect_MPxy.setNcellsMin(2*5)
      MeshParamsList.append(defect_MPxy)

      defect_MPxy = HomogeneousMeshParameters1D(mid[0]+1.5*self.interRodDistance, mid[0]+1.5*self.interRodDistance+0.5*self.rod_width)
      defect_MPxy.setSpacingMax(mesh_d)
      MeshParamsList.append(defect_MPxy)
      ##########

    elif self.DEFECT_TYPE == 1:
      defect_edges = mid[0] + self.interRodDistance*numpy.arange(-0.5*1.75,1,0.5*0.25)
      for idx in range(len(defect_edges)-1):
        defect_MPxy = HomogeneousMeshParameters1D(defect_edges[idx],defect_edges[idx+1])
        defect_MPxy.setNcellsMin(3)
        MeshParamsList.append(defect_MPxy)

    for obj in self.geometry_object_list:
      if obj.name=='woodpile':
        WP_log_MPxy = HomogeneousMeshParameters1D(obj.getLowerAbsolute()[0], obj.getLowerAbsolute()[0]+0.25*self.rod_width)
        WP_log_MPxy.setNcellsMin(1)
        MeshParamsList.append(WP_log_MPxy)
        WP_log_MPxy = HomogeneousMeshParameters1D(obj.getLowerAbsolute()[0]+0.25*self.rod_width, obj.getLowerAbsolute()[0]+0.5*self.rod_width)
        WP_log_MPxy.setNcellsMin(1)
        MeshParamsList.append(WP_log_MPxy)
        WP_log_MPxy = HomogeneousMeshParameters1D(obj.getLowerAbsolute()[0]+0.5*self.rod_width, obj.getLowerAbsolute()[0]+0.75*self.rod_width)
        WP_log_MPxy.setNcellsMin(1)
        MeshParamsList.append(WP_log_MPxy)
        WP_log_MPxy = HomogeneousMeshParameters1D(obj.getLowerAbsolute()[0]+0.75*self.rod_width, obj.getUpperAbsolute()[0])
        WP_log_MPxy.setNcellsMin(1)
        MeshParamsList.append(WP_log_MPxy)

        if obj.getLowerAbsolute()[0]-3*X_delta_2_nolog > self.box.lower[0]+7*X_delta_4+5*X_delta_3:
          WP_nolog_MPxy = HomogeneousMeshParameters1D(obj.getLowerAbsolute()[0]-3*X_delta_2_nolog, obj.getLowerAbsolute()[0])
          WP_nolog_MPxy.setNcellsMin(3)
          MeshParamsList.append(WP_nolog_MPxy)

    intbuffer_MPxy = HomogeneousMeshParameters1D(self.box.upper[0]-7*X_delta_4-5*X_delta_3, self.box.upper[0]-7*X_delta_4)
    intbuffer_MPxy.setNcellsMin(5)
    MeshParamsList.append(intbuffer_MPxy)

    extbuffer_MPxy = HomogeneousMeshParameters1D(self.box.upper[0]-7*X_delta_4, self.box.upper[0])
    extbuffer_MPxy.setNcellsMin(7)
    MeshParamsList.append(extbuffer_MPxy)

    intbuffer_MPxy = HomogeneousMeshParameters1D(self.box.lower[0]+7*X_delta_4, self.box.lower[0]+7*X_delta_4+5*X_delta_3)
    intbuffer_MPxy.setNcellsMin(5)
    MeshParamsList.append(intbuffer_MPxy)

    extbuffer_MPxy = HomogeneousMeshParameters1D(self.box.lower[0], self.box.lower[0]+7*X_delta_4)
    extbuffer_MPxy.setNcellsMin(7)
    MeshParamsList.append(extbuffer_MPxy)

    self.mesh.xmesh = mergeMeshingParameters(MeshParamsList)
    self.mesh.ymesh = self.mesh.xmesh
    return

  def createZmesh(self, mid, defect, mesh_d, Z_delta_0, Z_delta_1, Z_delta_2_log, Z_delta_2_nolog, Z_delta_3, Z_delta_4):
    ###################################################################

    # Z mesh
    MeshParamsList = []

    mid_MPz = HomogeneousMeshParameters1D(mid[2], mid[2])
    mid_MPz.setSpacingMax(numpy.inf)
    MeshParamsList.append(mid_MPz)

    print(defect.getCentro())
    #print(ZL_D)
    C = defect.getCentro()[2]
    ##  sys.exit(0)

    ###
    #mid_MPz = HomogeneousMeshParameters1D(C-defect.getSize()[2]*0.5, C)
    #mid_MPz.setNcellsMin(6)
    #MeshParamsList.append(mid_MPz)

    #mid_MPz = HomogeneousMeshParameters1D(C, C+defect.getSize()[2]*0.5)
    #mid_MPz.setNcellsMin(6)
    #MeshParamsList.append(mid_MPz)

    ###
    mid_MPz = HomogeneousMeshParameters1D(C-defect.getSize()[2]*0.5, C-defect.getSize()[2]*0.25)
    mid_MPz.setNcellsMin(3)
    MeshParamsList.append(mid_MPz)

    mid_MPz = HomogeneousMeshParameters1D(C-defect.getSize()[2]*0.25, C)
    mid_MPz.setNcellsMin(3)
    MeshParamsList.append(mid_MPz)

    mid_MPz = HomogeneousMeshParameters1D(C, C+defect.getSize()[2]*0.25)
    mid_MPz.setNcellsMin(3)
    MeshParamsList.append(mid_MPz)

    mid_MPz = HomogeneousMeshParameters1D(C+defect.getSize()[2]*0.25, C+defect.getSize()[2]*0.5)
    mid_MPz.setNcellsMin(3)
    MeshParamsList.append(mid_MPz)
    ###

    exc_MPz = HomogeneousMeshParameters1D(mid[2]-mesh_d, mid[2]+mesh_d)
    #exc_MPz.setSpacingMax(Z_delta_0)
    exc_MPz.setNcellsMin(2)
    MeshParamsList.append(exc_MPz)
    ##
    box_MPz = HomogeneousMeshParameters1D(self.box.lower[2], self.box.upper[2])
    box_MPz.setSpacingMax(numpy.inf)
    MeshParamsList.append(box_MPz)

    #####
    # TODO: MERGE_LEFTOVER: Check necessity of this part:
    ##  if self.DEFECT_TYPE == 0:
    ##    defect_buffer_z = (self.vertical_period+0.5*rod_height)-(1.5*self.interRodDistance)
    ##
    ##    defect_MPz = HomogeneousMeshParameters1D(mid[2]-1.5*self.interRodDistance-defect_buffer_z, mid[2]-1.5*self.interRodDistance)
    ##    defect_MPz.setSpacingMax(mesh_d)
    ##    MeshParamsList.append(defect_MPz)
    ##
    ##    defect_MPz = HomogeneousMeshParameters1D(mid[2]-1.5*self.interRodDistance, mid[2]-0.5*self.interRodDistance)
    ##    defect_MPz.setNcellsMin(2*11)
    ##    MeshParamsList.append(defect_MPz)
    ##
    ##    defect_MPz = HomogeneousMeshParameters1D(mid[2]-0.5*self.interRodDistance, mid[2]+0.5*self.interRodDistance)
    ##    defect_MPz.setNcellsMin(2*11)
    ##    MeshParamsList.append(defect_MPz)
    ##
    ##    defect_MPz = HomogeneousMeshParameters1D(mid[2]+0.5*self.interRodDistance, mid[2]+1.5*self.interRodDistance)
    ##    defect_MPz.setNcellsMin(2*11)
    ##    MeshParamsList.append(defect_MPz)
    ##
    ##    defect_MPz = HomogeneousMeshParameters1D(mid[2]+1.5*self.interRodDistance, mid[2]+1.5*self.interRodDistance+defect_buffer_z)
    ##    defect_MPz.setSpacingMax(mesh_d)
    ##    MeshParamsList.append(defect_MPz)
    ##
    ##  elif self.DEFECT_TYPE == 1:
    ##    defect_edges = mid[2] + self.interRodDistance*numpy.arange(-0.5*1.75,1,0.5*0.25)
    ##    for idx in range(len(defect_edges)-1):
    ##      defect_MPz = HomogeneousMeshParameters1D(defect_edges[idx],defect_edges[idx+1])
    ##      defect_MPz.setNcellsMin(3)
    ##      MeshParamsList.append(defect_MPz)
    #####

    intbuffer_MPz = HomogeneousMeshParameters1D(self.box.upper[2]-7*Z_delta_4-5*Z_delta_3, self.box.upper[2]-7*Z_delta_4)
    intbuffer_MPz.setNcellsMin(5)
    MeshParamsList.append(intbuffer_MPz)

    extbuffer_MPz = HomogeneousMeshParameters1D(self.box.upper[2]-7*Z_delta_4, self.box.upper[2])
    extbuffer_MPz.setNcellsMin(7)
    MeshParamsList.append(extbuffer_MPz)

    intbuffer_MPz = HomogeneousMeshParameters1D(self.box.lower[2]+7*Z_delta_4, self.box.lower[2]+7*Z_delta_4+5*Z_delta_3)
    intbuffer_MPz.setNcellsMin(5)
    MeshParamsList.append(intbuffer_MPz)

    extbuffer_MPz = HomogeneousMeshParameters1D(self.box.lower[2], self.box.lower[2]+7*Z_delta_4)
    extbuffer_MPz.setNcellsMin(7)
    MeshParamsList.append(extbuffer_MPz)

    for obj in self.geometry_object_list:
      if obj.name=='woodpile':
        WP_log_MPz = HomogeneousMeshParameters1D(obj.getLowerAbsolute()[2], obj.getUpperAbsolute()[2])
        WP_log_MPz.setNcellsMin(5)
        MeshParamsList.append(WP_log_MPz)

    self.mesh.zmesh = mergeMeshingParameters(MeshParamsList)
    ###################################################################

  def addSnapshots(self, defect):
    # TODO: Somehow make stuff like this external. Pass frequency especially. Temporary hack to get same files as before.
    fsnap = self.addFrequencySnapshot('x',defect.getCentro()[0])
    fsnap.name = 'central.X.fsnap'
    fsnap.first = 32000
    fsnap.repetition = 65400
    fsnap.starting_sample = 6400
    fsnap.frequency_vector = [4.690217E+08]
    fsnap = self.addFrequencySnapshot('y',defect.getCentro()[1])
    fsnap.name = 'central.Y.fsnap'
    fsnap.first = 32000
    fsnap.repetition = 65400
    fsnap.starting_sample = 6400
    fsnap.frequency_vector = [4.690217E+08]
    fsnap = self.addFrequencySnapshot('z',defect.getCentro()[2])
    fsnap.name = 'central.Z.fsnap'
    fsnap.first = 32000
    fsnap.repetition = 65400
    fsnap.starting_sample = 6400
    fsnap.frequency_vector = [4.690217E+08]

  def addProbes(self, defect):
    # TODO: MERGE_LEFTOVER: Check which probes are necessary and which are not.
    #xp_1 = 0.5*box_size
    #yp_1 = 0.5*box_size
    #zp_1 = 0.5*box_size

    #xp_2 = 0.5*box_size+4*mesh_d
    #yp_2 = 0.5*box_size
    #zp_2 = 0.5*box_size

    #xp_3 = 0.5*box_size
    #yp_3 = 0.5*box_size+4*mesh_d
    #zp_3 = 0.5*box_size

    #xp_4 = 0.5*box_size
    #yp_4 = 0.5*box_size
    #zp_4 = 0.5*box_size-5*mesh_d

    #self.probe_list.append(bfdtd.Probe(position = [xp_1,yp_1,zp_1], name='probe 1 centro 0.5*box_size'))
    #self.probe_list.append(bfdtd.Probe(position = [xp_2,yp_2,zp_2], name='probe 2 X+ 0.5*box_size'))
    #self.probe_list.append(bfdtd.Probe(position = [xp_3,yp_3,zp_3], name='probe 3 Y+ 0.5*box_size'))
    #self.probe_list.append(bfdtd.Probe(position = [xp_4,yp_4,zp_4], name='probe 4 Z- 0.5*box_size'))

    xp_1 = defect.getCentro()[0]
    yp_1 = defect.getCentro()[1]
    zp_1 = defect.getCentro()[2]

    xp_2 = defect.getCentro()[0]+0.25*defect.getSize()[0]
    yp_2 = defect.getCentro()[1]
    zp_2 = defect.getCentro()[2]

    xp_3 = defect.getCentro()[0]
    yp_3 = defect.getCentro()[1]+0.25*defect.getSize()[1]
    zp_3 = defect.getCentro()[2]

    xp_4 = defect.getCentro()[0]
    yp_4 = defect.getCentro()[1]
    zp_4 = defect.getCentro()[2]-0.25*defect.getSize()[2]

    self.probe_list.append(bfdtd.Probe(position = [xp_1,yp_1,zp_1], name='probe 1 centro'))
    self.probe_list.append(bfdtd.Probe(position = [xp_2,yp_2,zp_2], name='probe 2 X+'))
    self.probe_list.append(bfdtd.Probe(position = [xp_3,yp_3,zp_3], name='probe 3 Y+'))
    self.probe_list.append(bfdtd.Probe(position = [xp_4,yp_4,zp_4], name='probe 4 Z-'))

    #xp_1 = defect.getCentro()[0]
    #yp_1 = defect.getCentro()[1]
    #zp_1 = defect.getCentro()[2]

    #xp_2 = xp_1+4*mesh_d
    #yp_2 = yp_1
    #zp_2 = zp_1

    #xp_3 = xp_1
    #yp_3 = yp_1+4*mesh_d
    #zp_3 = zp_1

    #xp_4 = xp_1
    #yp_4 = yp_1
    #zp_4 = zp_1-5*mesh_d

    #self.probe_list.append(bfdtd.Probe(position = [xp_1,yp_1,zp_1], name='probe 9 centro'))
    #self.probe_list.append(bfdtd.Probe(position = [xp_2,yp_2,zp_2], name='probe 10 X+'))
    #self.probe_list.append(bfdtd.Probe(position = [xp_3,yp_3,zp_3], name='probe 11 Y+'))
    #self.probe_list.append(bfdtd.Probe(position = [xp_4,yp_4,zp_4], name='probe 12 Z-'))
    return

  def addExcitation(self, defect, mesh_d):
  ##  if self.excitation_direction == 0:
  ##    xe_1 = 0.5*box_size-mesh_d
  ##    ye_1 = 0.5*box_size
  ##    ze_1 = 0.5*box_size
  ##    xe_2 = 0.5*box_size+mesh_d
  ##    ye_2 = 0.5*box_size
  ##    ze_2 = 0.5*box_size
  ##  elif self.excitation_direction == 1:
  ##    xe_1 = 0.5*box_size
  ##    ye_1 = 0.5*box_size-mesh_d
  ##    ze_1 = 0.5*box_size
  ##    xe_2 = 0.5*box_size
  ##    ye_2 = 0.5*box_size+mesh_d
  ##    ze_2 = 0.5*box_size
  ##  else:
  ##    xe_1 = 0.5*box_size
  ##    ye_1 = 0.5*box_size
  ##    ze_1 = 0.5*box_size-mesh_d
  ##    xe_2 = 0.5*box_size
  ##    ye_2 = 0.5*box_size
  ##    ze_2 = 0.5*box_size+mesh_d

    if self.excitation_direction == 0:
      xe_1 = defect.getCentro()[0]-mesh_d
      ye_1 = defect.getCentro()[1]
      ze_1 = defect.getCentro()[2]
      xe_2 = defect.getCentro()[0]+mesh_d
      ye_2 = defect.getCentro()[1]
      ze_2 = defect.getCentro()[2]
    elif self.excitation_direction == 1:
      xe_1 = defect.getCentro()[0]
      ye_1 = defect.getCentro()[1]-mesh_d
      ze_1 = defect.getCentro()[2]
      xe_2 = defect.getCentro()[0]
      ye_2 = defect.getCentro()[1]+mesh_d
      ze_2 = defect.getCentro()[2]
    else:
      xe_1 = defect.getCentro()[0]
      ye_1 = defect.getCentro()[1]
      ze_1 = defect.getCentro()[2]-mesh_d
      xe_2 = defect.getCentro()[0]
      ye_2 = defect.getCentro()[1]
      ze_2 = defect.getCentro()[2]+mesh_d

    excitation = bfdtd.Excitation()
    excitation.setExtension([xe_1,ye_1,ze_1],[xe_2,ye_2,ze_2])
    excitation.setLambda(self.Lambda)
    excitation.useForMeshing = False

    if self.excitation_direction == 0:
      excitation.E = [1,0,0]
    elif self.excitation_direction == 1:
      excitation.E = [0,1,0]
    else:
      excitation.E = [0,0,1]

    self.excitation_list.append(excitation)
    return

  def addGeometry(self):
    return

  def setupBFDTDobject(self):

    # TODO: Test with different number of layers, rods, defect sizes, defect positions, rod heights/widths, make symmetrical
    # TODO: allow layer shifting/rotating (cf GWL woodpile, or use GWL woodpile code)
    # TODO: fix meshing to geometry (i.e. the meshing part should be one line + a few custom meshbox definitions, rest defined during geometry setup)
    # TODO: fix symmetry
    # TODO: allow inverse creation (i.e. shift layers instead of defect)

    #############################
    # variable setup
    #############################

    self.interRodDistance = self.vertical_period/numpy.sqrt(2) # Distance between two adjacent logs
    #n_logs = 3 # number of logs in each layer
    #n_logs = 5 # number of logs in each layer
    n_logs = 13 # number of logs in each layer
    self.rod_width = self.w_factor*self.vertical_period # width of the logs
    rod_height = 0.25*self.vertical_period # heigth of logs (should be 1/4 for fcc to not overlap)

    layer_height = 0.25*self.vertical_period # Can be different from rod_height! Used to make sure the periodicity remains correct even if rod_height != self.vertical_period/4 (FCT structure, non-FCC)

    L = n_logs*self.interRodDistance + self.rod_width # Length of logs (should be > (n_logs-1)*self.interRodDistance + self.rod_width + 0.5*self.interRodDistance)

    eps_woodpile = numpy.power(self.refractive_index_log,2) # Dielectric constant of logs
    eps_defect = numpy.power(self.refractive_index_defect,2) # Dielectric constant of defect
    eps_back = numpy.power(self.refractive_index_outer,2) # Dielectric constant of background material
    #n_layers = 5 # Number of layers of logs required
    #n_layers = 37 # Number of layers of logs required
    n_layers = 38 # Number of layers of logs required

    #buffer = max(2*self.interRodDistance, self.vertical_period)
    buffer = 1.25
    box_size = max(L, n_layers*layer_height) + 2*buffer

    XL = 0 # Lower edge of the simulation domain in x direction.
    YL = 0 # Lower edge of the simulation domain in y direction.
    ZL = 0 # Lower edge of the simulation domain in z direction.

    XU = box_size # Upper edge of the simulation domain in x direction.
    YU = box_size # Upper edge of the simulation domain in y direction.
    ZU = box_size # Upper edge of the simulation domain in z direction.
    #############################

    # some complex undocumented code by Weijei, ported from Matlab...
    # basic idea: work layer by layer
    # the total number of logs will be n_logs*n_layers
    # each layer having n_logs logs, for each layer, we go from i*n_logs to (i+1)*n_logs => ((i+1)*n_logs)-(i*n_logs) = n_logs

    # lists of lower upper coordinates in the X, Y and Z directions
    xxL = numpy.array([-(n_logs-1)*0.5*self.interRodDistance-0.5*self.rod_width + i*self.interRodDistance for i in range(n_logs)])
    xxU = xxL + self.rod_width

    yyL = -L/2
    yyU = L/2

    zzL = numpy.array([-0.5*n_layers*layer_height + i*layer_height for i in range(n_layers)])
    zzU = zzL + rod_height

    # preparation of rod coordinates for a woodpile centered on [0,0,0]
    x_L = numpy.zeros(n_layers*n_logs)
    y_L = numpy.zeros(n_layers*n_logs)
    z_L = numpy.zeros(n_layers*n_logs)

    x_U = numpy.ones(n_layers*n_logs)
    y_U = numpy.ones(n_layers*n_logs)
    z_U = numpy.ones(n_layers*n_logs)

    # TODO: Adapt defect position to current geometry, depending on number of layers, rods/layer? Add offset for both defect and excitation? etc...
    # TODO: Add position specification by A,B,C,D layer info?
    # defect coordinates
    XL_D = 0.5*(XU-XL) - 0.5*self.defect_size_vec3[0] + self.defect_offset_vec3[0]
    XU_D = 0.5*(XU-XL) + 0.5*self.defect_size_vec3[0] + self.defect_offset_vec3[0]
    YL_D = 0.5*(YU-YL) - 0.5*self.defect_size_vec3[1] + self.defect_offset_vec3[1]
    YU_D = 0.5*(YU-YL) + 0.5*self.defect_size_vec3[1] + self.defect_offset_vec3[1]
    ZL_D = 0.5*(ZU-ZL) - 0.5*self.defect_size_vec3[2] + self.defect_offset_vec3[2]
    ZU_D = 0.5*(ZU-ZL) + 0.5*self.defect_size_vec3[2] + self.defect_offset_vec3[2]

    ########################
    # geometry setup
    ########################
    self.clearGeometry()
    self.clearAllSnapshots()
    self.clearProbes()

    self.box.lower = [XL,YL,ZL]
    self.box.upper = [XU,YU,ZU]

    self.setDefaultRelativePermittivity(eps_back)

    woodpile_obj = Woodpile()
    woodpile_obj.rod_width = self.rod_width
    woodpile_obj.rod_height = rod_height
    woodpile_obj.rod_type='block'
    woodpile_obj.adaptXYMinMax()
    woodpile_obj.Nlayers_Z = n_layers
    woodpile_obj.NRodsPerLayer_X = n_logs
    woodpile_obj.NRodsPerLayer_Y = n_logs
    woodpile_obj.interLayerDistance = layer_height
    woodpile_obj.interRodDistance = self.interRodDistance
    woodpile_obj.offset = [0.5*(XU-XL),0.5*(YU-YL),0.5*(ZU-ZL)-(0.5*n_layers*layer_height)+0.5*rod_height]
    #woodpile_obj.Xoffset = 10
    #woodpile_obj.Yoffset = 10
    woodpile_obj.Xmin = -0.5*L
    woodpile_obj.Xmax = 0.5*L
    woodpile_obj.Ymin = -0.5*L
    woodpile_obj.Ymax = 0.5*L

    #woodpile_obj.isSymmetrical = False
    woodpile_obj.isSymmetrical = True

    woodpile_obj.shiftInitialLayerType_X = True
    woodpile_obj.shiftInitialLayerType_Y = True

    # almost-inverse woodpile
    woodpile_obj.shiftInitialLayerType_X = self.shift_initial_layers
    woodpile_obj.shiftInitialLayerType_Y = self.shift_initial_layers

    woodpile_obj.BottomToTop = True
    woodpile_obj.Xoffset = 0.5*self.rod_width
    woodpile_obj.Yoffset = 0.5*self.rod_width

    (GWL_obj, BFDTD_obj) = woodpile_obj.getGWLandBFDTDobjects()

    for obj in BFDTD_obj.geometry_object_list:
      obj.setRefractiveIndex(self.refractive_index_log)
      obj.useForMeshing = False
      obj.name = 'woodpile'

    self.geometry_object_list.extend(BFDTD_obj.geometry_object_list)

    # defect envelope
    defect_envelope_size_vec3 = self.interRodDistance - 0.5*self.rod_width
    #defect_envelope_size_vec3 = self.interRodDistance
    #defect_envelope_size_vec3 = self.interRodDistance + 0.5*self.rod_width
    #defect_envelope_size_vec3 = self.interRodDistance + 1*self.rod_width
    #defect_envelope_size_vec3 = self.interRodDistance + 1.1*self.rod_width

    if self.defect_envelope_on:
      defect_envelope = bfdtd.Block()
      defect_envelope.setLowerAbsolute([0.5*(XU-XL)-0.5*defect_envelope_size_vec3,0.5*(YU-YL)-0.5*defect_envelope_size_vec3,ZL_D])
      defect_envelope.setUpperAbsolute([0.5*(XU-XL)+0.5*defect_envelope_size_vec3,0.5*(YU-YL)+0.5*defect_envelope_size_vec3,ZU_D])
      defect_envelope.setRelativePermittivity(eps_back)
      defect_envelope.setName('defect_envelope')
      defect_envelope.useForMeshing = False
      self.geometry_object_list.append(defect_envelope)

    # the defect is put in last
    defect = bfdtd.Block()
    defect.setLowerAbsolute([XL_D,YL_D,ZL_D])
    defect.setUpperAbsolute([XU_D,YU_D,ZU_D])
    defect.setRelativePermittivity(eps_defect)
    defect.setName('defect')

    defect.useForMeshing = False
    self.geometry_object_list.append(defect)

    ## TODO: Check if this is actually still necessary or used...
    #defect_meshbox = bfdtd.MeshBox(lower=defect.getLowerAbsolute(), upper=defect.getUpperAbsolute())
    #defect_meshbox.useForMeshing = True
    #defect_meshbox.xmesh_params[0].setNcellsMin(2)
    #defect_meshbox.ymesh_params[0].setNcellsMin(3)
    #defect_meshbox.zmesh_params[0].setNcellsMin(4)
    #self.geometry_object_list.append(defect_meshbox)

    ########################
    x_space = 0.5*box_size-L/2
    y_space = 0.5*box_size-L/2
    z_space = 0.5*box_size-rod_height*n_layers/2
    ########################
    mesh_d = 0.5*self.interRodDistance/11
    ########################
    X_L0 = 0.5*self.interRodDistance + mesh_d
    X_delta_0 = mesh_d

    X_L1 = 0.5*self.interRodDistance + 0.5*self.rod_width - X_L0
    X_delta_1 = 0.5*X_L1

    X_L2 = (n_logs-1)*0.5*self.interRodDistance
    X_delta_2_log = self.rod_width/4
    X_delta_2_nolog = (self.interRodDistance/2-self.rod_width)/3

    X_L3 = 5*self.rod_width/4
    X_delta_3 = self.rod_width/4

    X_L4 = x_space - X_L3
    X_delta_4 = 1/7*X_L4
    ########################
    Z_L0 = 0.5*self.interRodDistance
    Z_delta_0 = mesh_d

    Z_L1 = 1.5*layer_height-Z_L0
    Z_delta_1 = Z_L1

    Z_L2 = int((n_layers-3)/2)*layer_height
    Z_delta_2_log = rod_height/5
    Z_delta_2_nolog = X_delta_2_nolog # Shouldn't be used in principle. Added just in case (in case rod_height!=c/4 for example!).

    Z_L3 = layer_height
    Z_delta_3 = 1/5*Z_L3

    Z_L4 = z_space - Z_L3
    Z_delta_4 = 1/7*Z_L4
    ########################

    ########################
    # output setup
    ########################
    self.addProbes(defect)

    # Add snapshots
    #self.addSnapshots(defect)

    ########################
    # input setup
    ########################
    self.addExcitation(defect, mesh_d)
    ############################################

    ########################
    # meshing setup
    ########################
    mid = self.box.getCentro()
    self.createXYmesh(mid, defect, mesh_d, X_delta_2_nolog, X_delta_4, X_delta_3)
    self.createZmesh(mid, defect, mesh_d, Z_delta_0, Z_delta_1, Z_delta_2_log, Z_delta_2_nolog, Z_delta_3, Z_delta_4)

  def writeBFDTD(self, directory = '.', file_basename = 'woodpile', WALLTIME = 360):
    self.setupBFDTDobject()

    # write out files
    self.writeAll(directory, fileBaseName=file_basename)
    self.writeShellScript(directory+os.sep+file_basename+'.sh', WALLTIME = WALLTIME)

def oldmain():
  '''
  test function
  .. todo:: Take what's useful from this one and then remove it
  '''
  # command-line option handling
  parser = argparse.ArgumentParser(description = 'write out the input files for a woodpile simulation', fromfile_prefix_chars='@')

  parser.add_argument('-v','--verbose', action="count", dest="verbosity", default=0, help='verbosity level')
  parser.add_argument('-d','--outdir', action="store", dest="outdir", default='/tmp/sims', help='output directory')
  parser.add_argument('-b','--basename', action="store", dest="basename", default=None, help='output basename')
  parser.add_argument('--walltime', type=int, default=360, help='walltime in hours (default: 360 hours = 15*24 hours = 15 days)')

  parser.add_argument('--verticalPeriod', type=float, default=1, help='interRodDistance d in microns')

  #disabled for the moment, as not needed
  parser.add_argument('--interRodDistance', type=float, default=1, help='interRodDistance d in microns')

  parser.add_argument('--offset-unit-is-microns', action="store_true", help='offset is specified in microns (default is as a multiple of the interRodDistance d)')

  parser.add_argument('--offset', type=float, default=[0,0,0], nargs=3, help='offset of the defect from the center as a multiple of the interRodDistance d (or in microns if --offset-unit-is-microns is specified)')
  parser.add_argument('--defectSizeVector', type=float, default=[1,1,1], nargs=3, help='defect size vector (cf --units option for used units)')

  arguments = parser.parse_args()

  if arguments.verbosity>0:
    print('---------')
    print(arguments)
    print('---------')

  if not arguments.offset_unit_is_microns:
    defect_offset_vec3 = numpy.array(arguments.offset)
  else:
    defect_offset_vec3 = numpy.array(arguments.offset)

  # interRodDistance = arguments.verticalPeriod/numpy.sqrt(2) # Distance between two adjacent logs

  # TODO: check if there is a direct way to do this.
  arguments.defectSizeVector = numpy.array(arguments.defectSizeVector)

  foo = weijeiWoodpile()
  foo.vertical_period = arguments.verticalPeriod
  foo.refractive_index_defect = 22
  foo.refractive_index_log = 1.52
  foo.refractive_index_outer = 3.5
  foo.excitation_direction = 2
  foo.directory = arguments.outdir
  foo.w_factor = 0.25
  foo.defect_size_vec3 = arguments.verticalPeriod/numpy.sqrt(2)*arguments.defectSizeVector
  foo.defect_offset_vec3 = defect_offset_vec3
  foo.shift_initial_layers = True

  foo.writeBFDTD('/tmp/sims','woodpile')

def main():
  '''
  Main function to generate woodpiles based on .ini files.
  
  .. todo:: The output directory could be created based on the .ini filename, section and/or an additional path key.
  .. todo:: It would be nice to support simple formulas as values in the .ini files. Ideally using an existing safe eval parser.
  .. todo:: Try out the ConfigParser dictionery readers.
  .. todo:: The object classes could offer .ini reader functions? (related to general object instance save/loading features, maybe even easy custom object, multi/meta-object creation for re-use in scripts)
  '''
  
  # command-line option handling
  parser = argparse.ArgumentParser(description = 'Create one or more woodpiles based on settings read from .ini files.')
  parser.add_argument('-v','--verbose', action="count", dest="verbosity", default=0, help='verbosity level')
  parser.add_argument('-d','--outdir', action="store", dest="outdir", default=tempfile.mkdtemp(), help='output directory')
  parser.add_argument('-b','--basename', action="store", dest="basename", default='woodpile', help='output basename')
  parser.add_argument('--walltime', type=int, default=360, help='walltime in hours (default: 360 hours = 15*24 hours = 15 days)')
  parser.add_argument('--parameterFileList', default=[], nargs='+', help='add list of parameter files', metavar='INIFILE')
  parser.add_argument('--parameterFile', default=[], action='append', help='add single parameter file', metavar='INIFILE')
  parser.add_argument('moreParameterFiles', nargs=argparse.REMAINDER, help='even more parameter files...', metavar='INIFILE')

  arguments = parser.parse_args()

  if arguments.verbosity>0:
    print('---------')
    print(arguments)
    print('---------')

  # NOTE: This is a bit silly, but makes for a very flexible CLI usage...
  for INIfile in arguments.parameterFile + arguments.parameterFileList + arguments.moreParameterFiles:
    config = ConfigParser(interpolation=ExtendedInterpolation(), inline_comment_prefixes = '#')
    print('==>Processing', INIfile)
    # Note: config.read() will ignore missing files, but does return a list of filenames which were successfully parsed.
    # config.read_file(open('example.ini')) would be an alternative which causes an error on open/read failure.
    # The advantage of the current way is that it continues after missing files.
    if config.read(INIfile):
      print(config.sections())
      for section in config.sections():
        print('-->{} : section = {}'.format(INIfile, section))
        current_section = config[section]
        #for key in current_section:
          #print(key)
        refractive_index_defect = current_section.getfloat('refractive_index_defect', fallback=weijeiWoodpile.refractive_index_defect)
        refractive_index_log = current_section.getfloat('refractive_index_log', fallback=weijeiWoodpile.refractive_index_log)
        refractive_index_outer = current_section.getfloat('refractive_index_outer', fallback=weijeiWoodpile.refractive_index_outer)
        vertical_period = current_section.getfloat('vertical_period', fallback=weijeiWoodpile.vertical_period)
        w_factor = current_section.getfloat('w_factor', fallback=weijeiWoodpile.w_factor)
        iterations = current_section.getint('iterations', fallback=weijeiWoodpile.DEFAULT_ITERATIONS)
        shift_initial_layers = current_section.getboolean('shift_initial_layers', fallback=weijeiWoodpile.shift_initial_layers)
        
        # custom conversions
        excitation_direction_list = int_array(str2list(current_section.get('excitation_direction_list', fallback='[0,1,2]'), array=False)[0])
        defect_size_vec3 = str2list(current_section.get('defect_size_vec3', fallback=str(weijeiWoodpile.defect_size_vec3)))[0]
        defect_offset_vec3 = str2list(current_section.get('defect_offset_vec3', fallback=str(weijeiWoodpile.defect_offset_vec3)))[0]

        print('refractive_index_defect = ' + str(refractive_index_defect))
        print('refractive_index_log = ' + str(refractive_index_log))
        print('refractive_index_outer = ' + str(refractive_index_outer))
        print('vertical_period = ' + str(vertical_period))
        print('w_factor = ' + str(w_factor))
        print('iterations = ' + str(iterations))
        print('shift_initial_layers = ' + str(shift_initial_layers))
        print('excitation_direction_list = ' + str(excitation_direction_list))
        print('defect_size_vec3 = ' + str(defect_size_vec3))
        print('defect_offset_vec3 = ' + str(defect_offset_vec3))

        excitation_direction_string = ['Ex','Ey','Ez']

        for excitation_direction in excitation_direction_list:
          foo = weijeiWoodpile()
          foo.vertical_period = vertical_period
          foo.refractive_index_defect = refractive_index_defect
          foo.refractive_index_log = refractive_index_log
          foo.refractive_index_outer = refractive_index_outer
          foo.w_factor = w_factor
          foo.defect_size_vec3 = defect_size_vec3
          foo.defect_offset_vec3 = defect_offset_vec3
          foo.shift_initial_layers = shift_initial_layers
          foo.flag.iterations = iterations

          foo.excitation_direction = excitation_direction
          foo.writeBFDTD(arguments.outdir + os.sep + excitation_direction_string[excitation_direction], arguments.basename, arguments.walltime)

    else:
      print('ERROR: Failed to read '+INIfile,file=sys.stderr)

class test_weijeiWoodpile(unittest.TestCase):
  '''
  To run the unittest, use::
  
    python3 -m unittest weijeiWoodpile
  '''
  
  def setUp(self):
    import warnings
    warnings.simplefilter("error")
  
  def test_writeBFDTD(self):
    foo = weijeiWoodpile()
    foo.writeBFDTD(tempfile.mkdtemp())
    return

if __name__ == "__main__":
  main()
  #unittest.main()
