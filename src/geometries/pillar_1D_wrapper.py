#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import tempfile
from geometries.pillar_1D import *
from geometries.rectangular_yagi import *
from geometries.triangular_yagi import *
from geometries.triangular_yagi_voxel import *
from geometries.triangular_yagi_voxel_sym import *

def cylinder(DSTDIR, bottomN, topN, excitationType, iterations, freq_snapshots):
  P = pillar_1D()
  print('======== cylinder START ============')
  
  n_Diamond = 2.4
  n_Air = 1

  P.DSTDIR = DSTDIR
  P.setIterations(iterations)
  P.print_holes_top = True
  P.print_holes_bottom = True
  P.setLambda(0.637)
  P.SNAPSHOTS_FREQUENCY = freq_snapshots
  
  P.HOLE_TYPE = 'cylinder'
  #P.setRadiusPillarYZ(0.150/2.0,0.150/2.0)
  P.setRadiusPillarYZ(0.5*P.getLambda()/(4*n_Air)+0.015,0.5*P.getLambda()/(4*n_Air)+0.015)
  P.print_podium = False;
  P.thickness_X_bottomSquare = P.getLambda()/n_Air;
  
  #P.d_holes_mum = 0.220; #mum
  #P.setRadiusHole(0.28*P.d_holes_mum,P.radius_Y_pillar_mum,0.28*P.d_holes_mum)
  P.d_holes_mum = P.getLambda()/(4*n_Air)+P.getLambda()/(4*n_Diamond)
  P.setRadiusHole(0.5*P.getLambda()/(4*n_Air),P.radius_Y_pillar_mum,0.5*P.getLambda()/(4*n_Air))
  
  P.bottom_N = bottomN; #no unit
  P.top_N = topN; #no unit
  
  #P.setDistanceBetweenDefectCentersInCavity(2*P.d_holes_mum) #mum
  # P.setDistanceBetweenDefectPairsInCavity(P.getDistanceBetweenDefectCentersInCavity() - P.d_holes_mum) # mum
  P.setDistanceBetweenDefectBordersInCavity(1*P.getLambda()/n_Diamond)

  delta_diamond = 0.5*P.getLambda()/(15*P.n_Substrate)
  P.setDeltaHole(delta_diamond,delta_diamond,delta_diamond)
  P.setDeltaSubstrate(delta_diamond,delta_diamond,0.5*delta_diamond)
  P.setDeltaOutside(delta_diamond,4*delta_diamond,4*delta_diamond)
  P.setDeltaCenter(delta_diamond,delta_diamond,delta_diamond)
  P.setDeltaBuffer(delta_diamond,delta_diamond,delta_diamond)
  P.setThicknessBuffer(4*delta_diamond,4*delta_diamond,4*delta_diamond)
  P.setRadiusCenter(2*P.delta_X_center,2*P.delta_Y_center,2*P.delta_Z_center)
  
  P.delta_X_bottomSquare = delta_diamond
  P.thickness_X_topBoxOffset = P.getLambda()/n_Air;

  P.Xmax = P.thickness_X_bottomSquare + P.getPillarHeight() + P.thickness_X_buffer + P.thickness_X_topBoxOffset; #mum
  P.Ymax = 5*2*P.radius_Y_pillar_mum;
  P.Zmax = 5*2*P.radius_Z_pillar_mum;
  
  P.setExcitationType(excitationType)
  P.BASENAME = P.HOLE_TYPE+'.bottomN_'+str(bottomN)+'.topN_'+str(topN)+'.excitationType_'+P.getExcitationTypeStr()

  P.write(P.DSTDIR,P.BASENAME)
  return P
  
def cylinder_mission3(DSTDIR, bottomN, topN, excitationType, iterations, freq_snapshots):
  P = pillar_1D()
  print('======== cylinder_mission3 START ============')
  P.DSTDIR = DSTDIR
  P.setIterations(iterations)
  P.print_holes_top = True
  P.print_holes_bottom = True
  P.setLambda(0.637)
  P.SNAPSHOTS_FREQUENCY = freq_snapshots

  P.HOLE_TYPE = 'cylinder'

  n_Eff = 2.2
  n_Diamond = 2.4
  n_Air = 1

  # refractive indices
  P.n_Substrate = n_Diamond
  P.n_Defect = n_Air
  P.n_Outside = n_Air
  P.n_bottomSquare = n_Diamond

  P.setRadiusPillarYZ(0.5,0.5)
  P.print_podium = True
  P.thickness_X_bottomSquare = 0.5 # mum #bottom square thickness

  P.d_holes_mum = P.getLambda()/(2*n_Eff);#mum
  radius_Z_piercer = 0.100
  P.setRadiusHole((P.getLambda()/(4*P.n_Defect))/2,P.radius_Y_pillar_mum,P.radius_Z_pillar_mum-radius_Z_piercer)

  P.bottom_N = bottomN; #no unit
  P.top_N = topN; #no unit

  P.setDistanceBetweenDefectBordersInCavity(P.getLambda()/n_Eff)
  # P.setDistanceBetweenDefectPairsInCavity(P.getDistanceBetweenDefectCentersInCavity() - P.d_holes_mum) # mum
  delta_diamond = P.getLambda()/(10*P.n_Substrate);
  P.setDeltaHole(delta_diamond,delta_diamond,delta_diamond)
  P.setDeltaSubstrate(delta_diamond,delta_diamond,delta_diamond)
  P.setDeltaOutside(P.getLambda()/(4*P.n_Substrate),P.getLambda()/(4*P.n_Substrate),P.getLambda()/(4*P.n_Substrate))
  P.setDeltaCenter(delta_diamond,delta_diamond,delta_diamond)
  P.setDeltaBuffer(delta_diamond,delta_diamond,delta_diamond)
  P.setThicknessBuffer(32*delta_diamond, 4*delta_diamond, radius_Z_piercer)
  P.setRadiusCenter(2*P.delta_X_center,2*P.delta_Y_center,2*P.delta_Z_center)

  P.delta_X_bottomSquare = delta_diamond
  P.thickness_X_topBoxOffset = 1

  P.Xmax = P.thickness_X_bottomSquare + P.getPillarHeight() + P.thickness_X_buffer + P.thickness_X_topBoxOffset; #mum
  P.Ymax = 2*(P.radius_Y_pillar_mum + 4*delta_diamond + 4*P.delta_Y_outside); #mum
  P.Zmax = 2*(P.radius_Z_pillar_mum + 4*delta_diamond + 4*P.delta_Z_outside); #mum

  P.setExcitationType(excitationType)
  P.BASENAME = P.HOLE_TYPE+'.bottomN_'+str(bottomN)+'.topN_'+str(topN)+'.excitationType_'+P.getExcitationTypeStr()

  dumpObj(P)
  P.verbose = True
  P.write(P.DSTDIR,P.BASENAME)

def square_holes(DSTDIR, bottomN, topN, excitationType, iterations, freq_snapshots):
  P = pillar_1D()
  print('======== square_holes START ============')
  P.DSTDIR = DSTDIR
  P.setIterations(iterations)
  P.print_holes_top = True
  P.print_holes_bottom = True
  P.setLambda(0.637)
  P.SNAPSHOTS_FREQUENCY = freq_snapshots
  
  P.HOLE_TYPE = 'square_holes'
  
  P.setRadiusPillarYZ(0.200,1)
  P.print_podium = True
  P.thickness_X_bottomSquare = 0.5 # mum #bottom square thickness
  
  P.d_holes_mum = P.getLambda()/(4*P.n_Substrate)+P.getLambda()/(4*P.n_Defect);#mum
  
  P.setRadiusHole((P.getLambda()/(4*P.n_Defect))/2,P.radius_Y_pillar_mum,P.radius_Z_pillar_mum - (P.d_holes_mum-2*P.radius_X_hole))
  
  P.bottom_N = bottomN; #no unit
  P.top_N = topN; #no unit
  P.setDistanceBetweenDefectCentersInCavity(P.getLambda()/P.n_Substrate + 2*P.radius_X_hole) #mum
  # P.setDistanceBetweenDefectPairsInCavity(P.getDistanceBetweenDefectCentersInCavity() - P.d_holes_mum) # mum
  delta_diamond = P.getLambda()/(10*P.n_Substrate)
  P.setDeltaHole(delta_diamond,delta_diamond,delta_diamond)
  P.setDeltaSubstrate(delta_diamond,delta_diamond,delta_diamond)
  P.setDeltaOutside(P.getLambda()/(4*P.n_Defect),P.getLambda()/(4*P.n_Defect),P.getLambda()/(4*P.n_Defect))
  P.setDeltaCenter(delta_diamond,delta_diamond,delta_diamond)
  P.setDeltaBuffer(delta_diamond,delta_diamond,delta_diamond)
  P.setThicknessBuffer(32*delta_diamond,4*delta_diamond,4*delta_diamond)
  P.setRadiusCenter(2*P.delta_X_center,2*P.delta_Y_center,2*P.delta_Z_center)
  
  P.delta_X_bottomSquare = delta_diamond
  P.thickness_X_topBoxOffset = 1
  
  P.Xmax = P.thickness_X_bottomSquare + P.getPillarHeight() + P.thickness_X_buffer + P.thickness_X_topBoxOffset; #mum
  P.Ymax = 2*(P.radius_Y_pillar_mum + 4*delta_diamond + 4*P.delta_Y_outside); #mum
  P.Zmax = 2*(P.radius_Z_pillar_mum + 4*delta_diamond + 4*P.delta_Z_outside); #mum

  #dumpObj(P)
  #P.verbose = True

  P.setExcitationType(excitationType)
  P.BASENAME = P.HOLE_TYPE+'.bottomN_'+str(bottomN)+'.topN_'+str(topN)+'.excitationType_'+P.getExcitationTypeStr()

  P.write(P.DSTDIR,P.BASENAME)

def rectangular_holes(DSTDIR, bottomN, topN, excitationType, iterations, freq_snapshots):
  P = pillar_1D()
  print('======== rectangular_holes START ============')
  P.DSTDIR = DSTDIR
  P.setIterations(iterations)
  P.print_holes_top = True
  P.print_holes_bottom = True
  P.setLambda(0.637)
  P.SNAPSHOTS_FREQUENCY = freq_snapshots
  
  P.HOLE_TYPE = 'rectangular_holes'
  
  n_Eff = 2.2
  n_Diamond = 2.4
  n_Air = 1
  
  # refractive indices
  P.n_Substrate = n_Diamond
  P.n_Defect = n_Air
  P.n_Outside = n_Air
  P.n_bottomSquare = n_Diamond
  
  P.setRadiusPillarYZ(0.5,0.5)

  P.print_podium = True
  
  P.d_holes_mum = P.getLambda()/(4*P.n_Substrate)+P.getLambda()/(4*P.n_Defect);#mum
  
  P.setRadiusHole((P.getLambda()/(4*P.n_Defect))/2, P.radius_Y_pillar_mum, P.radius_Z_pillar_mum - (50e-3))
  
  P.bottom_N = bottomN; #no unit
  P.top_N = topN; #no unit
  P.setDistanceBetweenDefectBordersInCavity(0.280) #mum
  # P.setDistanceBetweenDefectPairsInCavity(P.getDistanceBetweenDefectCentersInCavity() - P.d_holes_mum) # mum
  delta_diamond = P.getLambda()/(10*P.n_Substrate)
  P.delta_X_bottomSquare = delta_diamond
  
  P.setDeltaHole(delta_diamond,delta_diamond,delta_diamond)
  P.setDeltaSubstrate(delta_diamond,delta_diamond,delta_diamond)
  P.setDeltaOutside(P.getLambda()/(4*P.n_Defect),P.getLambda()/(4*P.n_Defect),P.getLambda()/(4*P.n_Defect))
  P.setDeltaCenter(delta_diamond/2,delta_diamond/2,delta_diamond/2)
  P.setDeltaBuffer(delta_diamond,delta_diamond,delta_diamond)
  P.setThicknessBuffer(32*delta_diamond,4*delta_diamond,4*delta_diamond)
  P.setRadiusCenter(2*P.delta_X_center,2*P.delta_Y_center,2*P.delta_Z_center)

  P.thickness_X_topBoxOffset = 1
  P.thickness_X_bottomSquare = 0.5 # mum #bottom square thickness

  P.Xmax = P.thickness_X_bottomSquare + P.getPillarHeight() + P.thickness_X_buffer + P.thickness_X_topBoxOffset; #mum
  P.Ymax = 2*(P.radius_Y_pillar_mum + 4*delta_diamond + 4*P.delta_Y_outside); #mum
  P.Zmax = 2*(P.radius_Z_pillar_mum + 4*delta_diamond + 4*P.delta_Z_outside); #mum

  P.setExcitationType(excitationType)
  P.BASENAME = P.HOLE_TYPE+'.bottomN_'+str(bottomN)+'.topN_'+str(topN)+'.excitationType_'+P.getExcitationTypeStr()

  #P.verbose = True
  P.write(P.DSTDIR,P.BASENAME)
  #dumpObj(P)

def test(DSTDIR,bottomN,topN):
  P = pillar_1D()
  P.DSTDIR = DSTDIR
  P.bottom_N = bottomN
  P.top_N = topN
  for i in range(4):
    P.setExcitationType(i)
    P.HOLE_TYPE = 'cylinder'
    P.BASENAME = P.HOLE_TYPE+'.bottomN_'+str(bottomN)+'.topN_'+str(topN)+'.excitationType_'+P.getExcitationTypeStr()
    P.write()
    P.HOLE_TYPE = 'square_holes'
    P.BASENAME = P.HOLE_TYPE+'.bottomN_'+str(bottomN)+'.topN_'+str(topN)+'.excitationType_'+P.getExcitationTypeStr()
    P.write()
    P.HOLE_TYPE = 'rectangular_holes'
    P.BASENAME = P.HOLE_TYPE+'.bottomN_'+str(bottomN)+'.topN_'+str(topN)+'.excitationType_'+P.getExcitationTypeStr()
    P.write()
    P.HOLE_TYPE = 'rectangular_yagi'
    P.BASENAME = P.HOLE_TYPE+'.bottomN_'+str(bottomN)+'.topN_'+str(topN)+'.excitationType_'+P.getExcitationTypeStr()
    P.write()
    P.HOLE_TYPE = 'triangular_yagi'
    P.BASENAME = P.HOLE_TYPE+'.bottomN_'+str(bottomN)+'.topN_'+str(topN)+'.excitationType_'+P.getExcitationTypeStr()
    P.write()
    P.HOLE_TYPE = 'triangular_yagi_voxel'
    P.BASENAME = P.HOLE_TYPE+'.bottomN_'+str(bottomN)+'.topN_'+str(topN)+'.excitationType_'+P.getExcitationTypeStr()
    P.write()

def test2(DSTDIR):
  P = pillar_1D()
  P.DSTDIR = DSTDIR
  print('======== default START ============')
  P.write()
  
  for i in range(4):
    cylinder(DSTDIR,12,12,i)
    cylinder(DSTDIR,20,10,i)
    square_holes(DSTDIR,6,3,i)
    square_holes(DSTDIR,20,10,i)
    rectangular_holes(DSTDIR,6,3,i)
    rectangular_holes(DSTDIR,6,4,i)
    rectangular_holes(DSTDIR,7,4,i)
    rectangular_holes(DSTDIR,7,5,i)
    rectangular_holes(DSTDIR,8,6,i)
    rectangular_yagi(DSTDIR,20,10,i,1)
    triangular_yagi(DSTDIR,20,10,i)
    triangular_yagi_voxel(DSTDIR,20,10,i)

def mission1(DSTDIR,excitationType,iterations,freq_snapshots):
  if not os.path.isdir(DSTDIR):
    os.mkdir(DSTDIR)
  rectangular_holes(DSTDIR,6,3,excitationType,iterations,freq_snapshots)
  rectangular_holes(DSTDIR,6,4,excitationType,iterations,freq_snapshots)
  rectangular_holes(DSTDIR,7,4,excitationType,iterations,freq_snapshots)
  rectangular_holes(DSTDIR,7,5,excitationType,iterations,freq_snapshots)
  rectangular_holes(DSTDIR,8,6,excitationType,iterations,freq_snapshots)

def mission2(DSTDIR,excitationType,iterations,freq_snapshots):
  if not os.path.isdir(DSTDIR):
    os.mkdir(DSTDIR)
  P = rectangular_yagi(20,10,excitationType,iterations,freq_snapshots,1)
  P.write(DSTDIR,'rectangular_yagi.CavityScalingFactor_1.bottomN_%BOTTOMN.topN_%TOPN.excitationType_%EXCITATIONTYPESTR')
  
def mission3(DSTDIR,excitationType,iterations,freq_snapshots):
  if not os.path.isdir(DSTDIR):
    os.mkdir(DSTDIR)
  cylinder(DSTDIR,12,12,excitationType,iterations,freq_snapshots)
  cylinder(DSTDIR,20,10,excitationType,iterations,freq_snapshots)

def mission4(DSTDIR,excitationType,iterations,freq_snapshots):
  if not os.path.isdir(DSTDIR):
    os.mkdir(DSTDIR)
  triangular_yagi(DSTDIR,20,10,excitationType,iterations,freq_snapshots)
  triangular_yagi_voxel(DSTDIR,20,10,excitationType,iterations,freq_snapshots)
  triangular_yagi_voxel_sym(DSTDIR,20,10,excitationType,iterations,freq_snapshots)

#def loncar_cylinder(BASENAME, DSTDIR, iterations, print_holes_top, print_holes_bottom, HOLE_TYPE, pillar_radius_mum, EXCITATION_FREQUENCY, SNAPSHOTS_FREQUENCY,excitation_type):

#def loncar_structure(BASENAME, DSTDIR, iterations, print_holes_top, print_holes_bottom, HOLE_TYPE, pillar_radius, EXCITATION_FREQUENCY, SNAPSHOTS_FREQUENCY):

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-d", "--destdir", action="store", dest="destdir", default=tempfile.gettempdir(), help="destination directory")
  parser.add_argument("-i", type=int, dest="iterations", default=65400+524200+524200, help="number of iterations")
  args = parser.parse_args()
  print(args.destdir)
  print(args.iterations)
  print(args)

  if os.path.isdir(args.destdir):
    freq_snapshots = [get_c0()/0.637]
    excitationType = 0 #Ym1
    #P = cylinder(options.destdir, 3, 3, excitationType, options.iterations, freq_snapshots)
    #print((P.getNcells()))
    for excitationType in range(4):
      mission1(args.destdir+os.sep+'mission1', excitationType, args.iterations, freq_snapshots)
      mission2(args.destdir+os.sep+'mission2', excitationType, args.iterations, freq_snapshots)
      mission3(args.destdir+os.sep+'mission3', excitationType, args.iterations, freq_snapshots)
      mission4(args.destdir+os.sep+'mission4', excitationType, args.iterations, freq_snapshots)
  else:
    print(('options.destdir = ' + options.destdir + ' is not a directory'))

if __name__ == "__main__":
  main()
