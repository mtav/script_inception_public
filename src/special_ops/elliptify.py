#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bfdtd.ellipsoid import *
import copy

def elliptifyPillar(DSTDIR, elliptify=False, excitation_direction='x', airblocks=False, depth_factor=2):

  #DSTDIR = sys.argv[1]
  if not os.path.isdir(DSTDIR):
    os.mkdir(DSTDIR)

  N = 51 # number of blocks per elliptical cylinder

  Dx = 3.15 # X diametre of an elliptical cylinder
  Dz = 3 # Z diametre of an elliptical cylinder
  block_direction = 'x' # direction of the blocks in an elliptical cylinder

  #depth_factor = 7 # the airblocks will be depth_factor*mirror_pair_height deep
  thickness = 0.200 # transversal thickness of the airblocks

  sim = readBristolFDTD('qedc3_2_05.in')

  first = True

  BASENAME = "ellipsoid.x%.2f.z%.2f" % (Dx,Dz)

  C = [0,0,0]
  radius = 0
  mirror_pair_height = 0

  Nlayers = 0

  podium_size = [0,0,0]

  for i in range(len(sim.geometry_object_list)):
    obj = sim.geometry_object_list[i]
    
    if isinstance(obj,Block):
      podium_size = obj.getSize()
    
    if isinstance(obj,Cylinder):
      
      C_current = obj.getCentro()
      upper_current = obj.getUpper()

      if Nlayers<2:
        mirror_pair_height += obj.height

      Nlayers += 1
      
      if upper_current[1]>C[1]:
        C = [C_current[0],upper_current[1],C_current[2]]

      if elliptify:
        ellipsoid = Ellipsoid()
        ellipsoid.setCentro(obj.getCentro())
        size = obj.getSize()
        ellipsoid.setSize([Dx,obj.height,Dz])
        ellipsoid.permittivity = obj.permittivity
        ellipsoid.conductivity = obj.conductivity
        ellipsoid.mesh.setSizeAndResolution(ellipsoid.getSize(),[N,N,N])
        ellipsoid.block_direction = block_direction
        sim.geometry_object_list[i] = ellipsoid
        #print(id(obj))

      if first:
        first=False
        radius = obj.outer_radius
        if elliptify:
          ref=BFDTDobject()
          ref.box = sim.box
          ref.geometry_object_list.append(obj)
          ref.geometry_object_list.append(ellipsoid)
          ref.writeGeoFile(DSTDIR+os.sep+BASENAME+'.ref.geo')

  if airblocks:
    depth = depth_factor*mirror_pair_height

    block_xminus = Block()
    block_xminus.name = 'airblock'
    block_xminus.setRefractiveIndex(1)
    block_xminus.setSize([thickness,depth,Dz])
    block_xminus.setCentro([C[0]-(0.5*Dx-0.5*thickness),C[1]-0.5*depth,C[2]])

    block_xplus = Block()
    block_xplus.name = 'airblock'
    block_xplus.setRefractiveIndex(1)
    block_xplus.setSize([thickness,depth,Dz])
    block_xplus.setCentro([C[0]+(0.5*Dx-0.5*thickness),C[1]-0.5*depth,C[2]])

    sim.geometry_object_list.extend([block_xminus, block_xplus])

  excitation_orig = sim.excitation_list[0]
  excitation_new = copy.deepcopy(excitation_orig)

  sim.box.lower = [0,0,0]
  if excitation_direction == 'z':
    
    sim.boundaries.Xpos_bc = 2
    sim.boundaries.Ypos_bc = 2
    sim.boundaries.Zpos_bc = 1
    sim.boundaries.Xneg_bc = 2
    sim.boundaries.Yneg_bc = 2
    sim.boundaries.Zneg_bc = 2
    
    sim.box.upper[0] = podium_size[0]
    sim.box.upper[2] = C[2]
    
    excitation_new.P1[0] = excitation_orig.P1[2]
    excitation_new.P1[2] = excitation_orig.P1[0]
    excitation_new.P2[0] = excitation_orig.P2[2]
    excitation_new.P2[2] = excitation_orig.P2[0]
    
    excitation_new.E = [0,0,1]
    
    frequency_vector = sim.frequency_snapshot_list[0].frequency_vector
    
    sim.clearAllSnapshots()
    
    for p in sim.probe_list:
      tmp = p.position[0]
      p.position[0] = p.position[2]
      p.position[2] = tmp
    #sim.clearProbes()
    
    P1, P2 = fixLowerUpper(excitation_new.P1, excitation_new.P2);
    
    snapshot = sim.addFrequencySnapshot('x',excitation_new.P1[0]); snapshot.first = 65400; snapshot.repetition = 524200; snapshot.frequency_vector = frequency_vector
    snapshot = sim.addFrequencySnapshot('y',excitation_new.P1[1]); snapshot.first = 65400; snapshot.repetition = 524200; snapshot.frequency_vector = frequency_vector
    snapshot = sim.addFrequencySnapshot('z',excitation_new.P1[2]); snapshot.first = 65400; snapshot.repetition = 524200; snapshot.frequency_vector = frequency_vector
    snapshot = sim.addTimeSnapshot('x',excitation_new.P1[0]); snapshot.first = 65400; snapshot.repetition = 524200;
    snapshot = sim.addTimeSnapshot('y',excitation_new.P1[1]); snapshot.first = 65400; snapshot.repetition = 524200;
    snapshot = sim.addTimeSnapshot('z',excitation_new.P1[2]); snapshot.first = 65400; snapshot.repetition = 524200;

  print('podium_size = '+str(podium_size))

  sim.excitation_list = [excitation_new]

  Lambda = excitation_new.getLambda()
  # define mesh
  a = 10

  #sim.mesh = MeshObject()

  sim.autoMeshGeometry(Lambda/a)
  #MAXCELLS=8000000;
  MAXCELLS=1000000;
  #MAXCELLS=100000;
  while(sim.getNcells()>MAXCELLS and a>1):
    a = a-1
    sim.autoMeshGeometry(Lambda/a)

  #sim.writeGeoFile('ellipsoid.Yx.geo')
  #sim.writeInpFile('ellipsoid.Yx.inp')
  sim.fileList = []
  print('number of geometry objects = '+str(N*len(sim.geometry_object_list)))

  #sim.flag.iterations = 10

  sim.writeAll(DSTDIR,BASENAME)
  sim.writeShellScript(DSTDIR+os.path.sep+BASENAME+'.sh', WALLTIME=360)

if __name__ == "__main__":
  
  if len(sys.argv)>1:
      DSTDIR = sys.argv[1]
  else:
      DSTDIR = os.getcwd()

  if not os.path.isdir(DSTDIR):
    os.mkdir(DSTDIR)

  elliptifyPillar(DSTDIR+os.sep+'cylindrical_Ex', elliptify=False, excitation_direction='x', airblocks=False, depth_factor=2)
  elliptifyPillar(DSTDIR+os.sep+'cylindrical_Ez', elliptify=False, excitation_direction='z', airblocks=False, depth_factor=2)
  elliptifyPillar(DSTDIR+os.sep+'elliptical_Ex', elliptify=True, excitation_direction='x', airblocks=False, depth_factor=2)
  elliptifyPillar(DSTDIR+os.sep+'elliptical_Ez', elliptify=True, excitation_direction='z', airblocks=False, depth_factor=2)
  
  for depth_factor in [2, 3.5, 5.5, 7]:
    elliptifyPillar(DSTDIR+os.sep+'elliptical_Ex_withAirBlocks_depth_'+str(depth_factor)+'mp', elliptify=True, excitation_direction='x', airblocks=True, depth_factor=depth_factor)
    elliptifyPillar(DSTDIR+os.sep+'elliptical_Ez_withAirBlocks_depth_'+str(depth_factor)+'mp', elliptify=True, excitation_direction='z', airblocks=True, depth_factor=depth_factor)

  print( 'Output in ' + DSTDIR)
