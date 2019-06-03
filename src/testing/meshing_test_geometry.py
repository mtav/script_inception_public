#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import re
import os
import numpy

from bfdtd.meshobject import *
import bfdtd.bfdtd_parser as bfdtd

if __name__ == '__main__':

  # basic sim object
  sim=bfdtd.BFDTDobject()
  sim.box.setLower([0,0,0])
  sim.box.setUpper([20,30,40])

  # basic meshbox
  meshbox = bfdtd.MeshBox()
  meshbox.setMeshParams(sim.box.lower,sim.box.upper,[numpy.inf,numpy.inf,numpy.inf])
  sim.geometry_list.append(meshbox)

  # meshbox setNmin test
  meshbox = bfdtd.MeshBox()
  meshbox.setLower([7,8,9])
  meshbox.setUpper([10,11,12])
  meshbox.xmesh_params[0].setNmin(4)
  meshbox.ymesh_params[0].setNmin(5)
  meshbox.zmesh_params[0].setNmin(6)
  sim.geometry_list.append(meshbox)

  # block setNmin test
  block = bfdtd.Block()
  block.setLower([7,8,9])
  block.setUpper([10,11,12])
  block.xmesh_params[0].setNmin(4)
  block.ymesh_params[0].setNmin(5)
  block.zmesh_params[0].setNmin(6)
  sim.geometry_list.append(block)

  # meshbox setDeltaMax test
  meshbox = bfdtd.MeshBox()
  meshbox.setLower([7,8,9])
  meshbox.setUpper([10,11,12])
  meshbox.xmesh_params[0].setDeltaMax(4)
  meshbox.ymesh_params[0].setDeltaMax(5)
  meshbox.zmesh_params[0].setDeltaMax(6)
  sim.geometry_list.append(meshbox)

  # block setDeltaMax test
  block = bfdtd.Block()
  block.setLower([7,8,9])
  block.setUpper([10,11,12])
  block.xmesh_params[0].setDeltaMax(4)
  block.ymesh_params[0].setDeltaMax(5)
  block.zmesh_params[0].setDeltaMax(6)
  sim.geometry_list.append(block)

  # meshbox multiple meshparam test
  meshbox = bfdtd.MeshBox()
  meshbox.setLower([7,8,9])
  meshbox.setUpper([10,11,12])

  meshbox.xmesh_params = []
  MP = MeshParams(1,2)
  MP.setNmin(2)
  meshbox.xmesh_params.append(MP)
  MP = MeshParams(1,2)
  MP.setDeltaMax(3)
  meshbox.xmesh_params.append(MP)
  MP = MeshParams(1,2)
  MP.setDeltaMax(3)
  meshbox.xmesh_params.append(MP)

  meshbox.ymesh_params = []
  MP = MeshParams(1,2)
  MP.setNmin(2)
  meshbox.ymesh_params.append(MP)
  MP = MeshParams(1,2)
  MP.setDeltaMax(3)
  meshbox.ymesh_params.append(MP)
  MP = MeshParams(1,2)
  MP.setDeltaMax(3)
  meshbox.ymesh_params.append(MP)

  meshbox.zmesh_params = []
  MP = MeshParams(1,2)
  MP.setNmin(2)
  meshbox.zmesh_params.append(MP)
  MP = MeshParams(1,2)
  MP.setDeltaMax(3)
  meshbox.zmesh_params.append(MP)
  MP = MeshParams(1,2)
  MP.setDeltaMax(3)
  meshbox.zmesh_params.append(MP)

  sim.geometry_list.append(meshbox)

  # block multiple meshparam test
  block = bfdtd.Block()
  block.setLower([7,8,9])
  block.setUpper([10,11,12])

  block.xmesh_params = []
  MP = MeshParams(1,2)
  MP.setNmin(2)
  block.xmesh_params.append(MP)
  MP = MeshParams(1,2)
  MP.setDeltaMax(3)
  block.xmesh_params.append(MP)
  MP = MeshParams(1,2)
  MP.setDeltaMax(3)
  block.xmesh_params.append(MP)

  block.ymesh_params = []
  MP = MeshParams(1,2)
  MP.setNmin(2)
  block.ymesh_params.append(MP)
  MP = MeshParams(1,2)
  MP.setDeltaMax(3)
  block.ymesh_params.append(MP)
  MP = MeshParams(1,2)
  MP.setDeltaMax(3)
  block.ymesh_params.append(MP)

  block.zmesh_params = []
  MP = MeshParams(1,2)
  MP.setNmin(2)
  block.zmesh_params.append(MP)
  MP = MeshParams(1,2)
  MP.setDeltaMax(3)
  block.zmesh_params.append(MP)
  MP = MeshParams(1,2)
  MP.setDeltaMax(3)
  block.zmesh_params.append(MP)

  sim.geometry_list.append(block)

  # automesh
  sim.autoMeshGeometryNew()

  # write
  sim.writeAll('/tmp/test')
