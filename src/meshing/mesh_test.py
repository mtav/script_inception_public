#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import bpy
import numpy
from blender_scripts.FDTDGeometryObjects import GEOmesh1D, GEOmesh1D_bmesh

from meshing.meshing import HeterogeneousMesh1D, HomogeneousMesh1D, HomogeneousMeshParameters1D, Mesh3D, MultiMesh1D

def testInBlender():

  hetero = HeterogeneousMesh1D([1.18, 3.23, 4.58, 7.41])
  hetero.location = 0.1
  print(hetero)

  homo = HomogeneousMesh1D(1.2, 10.5, 0.43)
  homo.location = 0.2
  print(homo)

  param = HomogeneousMeshParameters1D(3, 5, 0.134)
  param.location = 0.3
  print(param)

  hetero2 = HeterogeneousMesh1D([-1.42, 3.23, -4.58, 7.1])
  hetero2.location = 0.4
  print(hetero)

  homo2 = HomogeneousMesh1D(4, 7.8, 0.23)
  homo2.location = 0.5
  print(homo)

  param2 = HomogeneousMeshParameters1D(3, 7, 0.18)
  param2.location = 0.6
  print(param)

  multi = MultiMesh1D()
  multi.location = 0.7
  multi.maximum_mesh_delta_ratio = numpy.inf
  multi.mesh_list = [homo2, hetero2, param2]
  multi.makeAllSubMeshesChildren()
  print(multi)

  obj = Mesh3D()
  obj.location = [4,5,6]
  obj.xmesh.mesh_list = [homo, hetero, multi, param]
  obj.xmesh.makeAllSubMeshesChildren()
  #obj.xmesh.mesh_list = [homo]
  print('ratio before:')
  print(obj.xmesh.maximum_mesh_delta_ratio)
  #obj.xmesh.maximum_mesh_delta_ratio = numpy.inf
  obj.xmesh.maximum_mesh_delta_ratio = None
  print('ratio after:')
  print(obj.xmesh.maximum_mesh_delta_ratio)
  print(obj)
  #print('==========')
  #print(obj.PrintSelf(5*'^'))
  print('=== get =======')
  c = obj.getGlobalXCoordinates()
  print('=== print =======')
  print(c)
  print('==========')
  
  #print(param.PrintSelf('hello =>'))
  
  #bpy.ops.mesh.primitive_monkey_add()
  
  #GEOmesh1D(name='KOKO_manual', coords=[1,2,3,42], location=[5,6,7])
  #GEOmesh1D_bmesh(name='KOKO_bmesh', coords=[1,2,3,42], location=[5,6,7])
  
  GEOmesh1D_bmesh(name='hetero', coords=hetero.getLocalCoordinates(), location=[hetero.getGlobalLocation(), 1, 0])
  GEOmesh1D_bmesh(name='homo', coords=homo.getLocalCoordinates(), location=[homo.getGlobalLocation(), 2, 0])
  GEOmesh1D_bmesh(name='param', coords=param.getLocalCoordinates(), location=[param.getGlobalLocation(), 3, 0])
  GEOmesh1D_bmesh(name='hetero2', coords=hetero2.getLocalCoordinates(), location=[hetero2.getGlobalLocation(), 4, 0])
  GEOmesh1D_bmesh(name='homo2', coords=homo2.getLocalCoordinates(), location=[homo2.getGlobalLocation(), 5, 0])
  GEOmesh1D_bmesh(name='param2', coords=param2.getLocalCoordinates(), location=[param2.getGlobalLocation(), 6, 0])
  GEOmesh1D_bmesh(name='multi', coords=multi.getLocalCoordinates(), location=[multi.getGlobalLocation(), 7, 0])
  GEOmesh1D_bmesh(name='obj', coords=obj.getGlobalXCoordinates(), location=[obj.getGlobalLocation()[0], 0, 0])
  
  print('=== DONE ===')
  return

def test2():
  print('=== START ===')
  hetero = HeterogeneousMesh1D([0, 1.18, 3.23, 4.58, 7.41])
  hetero.location = 1
  print(hetero)

  multi = MultiMesh1D()
  multi.location = 2
  multi.maximum_mesh_delta_ratio = None
  multi.mesh_list = [hetero]
  multi.makeAllSubMeshesChildren()
  print(multi)

  GEOmesh1D_bmesh(name='hetero', coords=hetero.getLocalCoordinates(), location=[hetero.getGlobalLocation(), 1, 0])
  GEOmesh1D_bmesh(name='multi', coords=multi.getLocalCoordinates(), location=[multi.getGlobalLocation(), 0, 0])

  print('=== END ===')
  return

if __name__ == '__main__':
  #testInBlender()
  test2()
