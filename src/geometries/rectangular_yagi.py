#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import tempfile
from geometries.pillar_1D import *

def rectangular_yagi(bottomN, topN, excitationType, iterations, freq_snapshots, CavityScalingFactor, RadiusPillar_Y_mum=0.5, RadiusPillar_Z_mum=0.5, n_Eff = 2.2, radius_Z_piercer_mum = 0.100):
  P = pillar_1D()
  #print('======== rectangular_yagi START ============')
  #print('======== rectangular_yagi_LambdaOver2Cavity START ============')
  #P.DSTDIR = DSTDIR
  P.setIterations(iterations)
  P.print_holes_top = True
  P.print_holes_bottom = True
  P.setLambda(0.637)
  P.SNAPSHOTS_FREQUENCY = freq_snapshots

  P.Nvoxels = 10;
  
  P.HOLE_TYPE = 'rectangular_yagi'
  
  #n_Eff = 2.2
  n_Diamond = 2.4
  n_Air = 1
  
  # refractive indices
  P.n_Substrate = n_Diamond
  P.n_Defect = n_Diamond
  #P.n_Defect = n_Air
  P.n_Outside = n_Air
  P.n_bottomSquare = n_Diamond
  
  P.setRadiusPillarYZ(RadiusPillar_Y_mum, RadiusPillar_Z_mum)
  P.print_podium = True
  P.print_pillar = True
  
  P.d_holes_mum = P.getLambda()/(2*n_Eff);#mum
  #radius_Z_piercer_mum = 0.100
  P.setRadiusHole((P.getLambda()/(4*P.n_Defect))/2,P.radius_Y_pillar_mum,P.radius_Z_pillar_mum-radius_Z_piercer_mum)
  #P.setRadiusHole((P.getLambda()/(4*n_Eff))/2,P.radius_Y_pillar_mum,P.radius_Z_pillar_mum-radius_Z_piercer_mum)
  
  P.bottom_N = bottomN; #no unit
  P.top_N = topN; #no unit
  
  P.setDistanceBetweenDefectBordersInCavity(CavityScalingFactor*P.getLambda()/n_Eff)
  
  delta_diamond = P.getLambda()/(10*P.n_Substrate);
  delta_defect = P.getLambda()/(10*P.n_Substrate);
  P.delta_X_bottomSquare = delta_diamond
  P.setDeltaHole(delta_defect,delta_defect,delta_defect)
  P.setDeltaSubstrate(delta_diamond,delta_diamond,delta_diamond)
  P.setDeltaOutside(P.getLambda()/(4*P.n_Defect),P.getLambda()/(4*P.n_Defect),P.getLambda()/(4*P.n_Defect))
  P.setDeltaCenter(delta_diamond,delta_diamond,delta_diamond)
  P.setDeltaBuffer(delta_diamond,delta_diamond,delta_diamond)
  P.setThicknessBuffer(32*delta_diamond,4*delta_diamond,12*delta_diamond)
  P.setRadiusCenter(2*P.delta_X_center,2*P.delta_Y_center,2*P.delta_Z_center)
  
  P.thickness_X_bottomSquare = 0.5 # mum #bottom square thickness
  P.thickness_X_topBoxOffset = 1
  
  P.Xmax = P.thickness_X_bottomSquare + P.getPillarHeight() + P.thickness_X_buffer + P.thickness_X_topBoxOffset; #mum
  P.Ymax = 2*(P.radius_Y_pillar_mum + 4*delta_diamond + 4*P.delta_Y_outside); #mum
  P.Zmax = 2*(P.radius_Z_pillar_mum + 4*delta_diamond + 4*P.delta_Z_outside); #mum

  P.setExcitationType(excitationType)
  #P.BASENAME = P.HOLE_TYPE+'.bottomN_'+str(bottomN)+'.topN_'+str(topN)+'.excitationType_'+P.getExcitationTypeStr() #+'.DistanceBetweenDefectBordersInCavity_'+P.getDistanceBetweenDefectBordersInCavity()
  #P.BASENAME = 'rectangular_yagi_LambdaOver2Cavity' + '.bottomN_'+str(bottomN)+'.topN_'+str(topN)+'.excitationType_'+P.getExcitationTypeStr() #+'.DistanceBetweenDefectBordersInCavity_'+P.getDistanceBetweenDefectBordersInCavity()

  #P.verbose = True
  #dumpObj(P)
  #P.write()
  return P

def main(argv=None):
  parser =  argparse.ArgumentParser()

  default_basename = 'rectangular_yagi.CavityScalingFactor_%CSF.bottomN_%BOTTOMN.topN_%TOPN.excitationType_%EXCITATIONTYPESTR' #.DistanceBetweenDefectBordersInCavity_%DISTANCEBETWEENDEFECTBORDERSINCAVITY'

  #default_destdir = os.getenv('TESTDIR')
  default_destdir = tempfile.gettempdir()
  
  parser.add_argument("-d", "--destdir", action="store", type=str, dest="destdir", default=default_destdir, help="destination directory")
  parser.add_argument("-i", "--iterations", type=int, dest="iterations", default=65400+524200+524200, help="number of iterations")
  parser.add_argument("-b", "--N_bottom", type=int, dest="N_bottom", default=9, help="number of holes at the bottom")
  parser.add_argument("-t", "--N_top", type=int, dest="N_top", default=7, help="number of holes at the top")
  parser.add_argument("-e", "--excitationTypeStr", type=str, dest="excitationTypeStr", default='Zm1', help="excitationType: Ym1,Ym2,Zm1,Zm2")
  parser.add_argument("-f", "--frequency", type=str, dest="FrequencyList", default='', help="frequency of the frequency snapshots: ex: \"100.1,150.2,200.3,250.4\"")
  parser.add_argument("--FrequencyListFile", type=str, dest="FrequencyListFile", default='', help="file containing a list of frequencies for the frequency snapshots: ex: freq_list.txt")
  parser.add_argument("-c", "--CavityScalingFactor", type=float, dest="CavityScalingFactor", default=1, help="cavity height = CavityScalingFactor*lambda/n_Eff")
  parser.add_argument("--RadiusPillar_Y_mum", type=float, dest="RadiusPillar_Y_mum", default=0.5, help="RadiusPillar_Y_mum")
  parser.add_argument("--RadiusPillar_Z_mum", type=float, dest="RadiusPillar_Z_mum", default=0.5, help="RadiusPillar_Z_mum")
  parser.add_argument("--n_Eff", type=float, dest="n_Eff", default=2.2, help="n_Eff")
  parser.add_argument("--radius_Z_piercer_mum", type=float, dest="radius_Z_piercer_mum", default=0.100, help="radius_Z_piercer_mum")
  parser.add_argument("--baseName", type=str, dest="baseName", default=default_basename, help="baseName")
  
  options = parser.parse_args()
  
  print(('destdir = ',options.destdir))
  print(('iterations = ',options.iterations))
  print(('N_bottom = ',options.N_bottom))
  print(('N_top = ',options.N_top))
  print(('excitationTypeStr = ',options.excitationTypeStr))
  print(('FrequencyList = ',options.FrequencyList))
  print(('CavityScalingFactor = ',options.CavityScalingFactor))
  
  freq_snapshots = []
  
  # create at least one snapshot of each for the resonance rerun
  if len(options.FrequencyListFile) == 0 and len(options.FrequencyList) == 0:
    freq_snapshots = [get_c0()/0.637]

  if len(options.FrequencyListFile) != 0:
    freq_snapshots += getFrequencies(options.FrequencyListFile)
  if len(options.FrequencyList) != 0:
    freq_snapshots += [float(x) for x in options.FrequencyList.split(',')]

  print(freq_snapshots)
  #sys.exit()

  excitationType = -1
  if options.excitationTypeStr == 'Ym1':
    excitationType = 0
  elif options.excitationTypeStr == 'Zm1':
    excitationType = 1
  elif options.excitationTypeStr == 'Ym2':
    excitationType = 2
  elif options.excitationTypeStr == 'Zm2':
    excitationType = 3
  print(('excitationType = ', excitationType))

  print(options)

  P = rectangular_yagi(options.N_bottom, options.N_top, excitationType, options.iterations, freq_snapshots, options.CavityScalingFactor, options.RadiusPillar_Y_mum, options.RadiusPillar_Z_mum, options.n_Eff, options.radius_Z_piercer_mum)

  baseName_substituted = options.baseName
  baseName_substituted = baseName_substituted.replace('%CSF',str(options.CavityScalingFactor))
  baseName_substituted = baseName_substituted.replace('%RADIUS_Z_PIERCER_MUM',str(options.radius_Z_piercer_mum))
  baseName_substituted = baseName_substituted.replace('%N_EFF',str(options.n_Eff))

  P.verbose = True
  #P.writeAll(options.destdir,baseName_substituted)
  P.write(options.destdir,baseName_substituted)
  
  # TODO: put this in P.write()
  #if os.path.isdir(options.destdir):
  #else:
    #print('options.destdir = ' + options.destdir + ' is not a directory')

      #rectangular_yagi(options.destdir,,,,1)
      #rectangular_yagi_LambdaOver2Cavity(options.destdir,options.N_bottom,options.N_top,excitationType,options.iterations,freq_snapshots,0.5)

if __name__ == "__main__":
  main()
