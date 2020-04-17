#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import argparse
import tempfile
from GWL.woodpile import *

def createWoodpile_1(DSTDIR):
  a_over_Lambda = 0.93
  Lambda = 1.4
  Vperiod = a_over_Lambda*Lambda # Vertical period (1 period corresponding to 4 layers ABCD)
  Hperiod = Vperiod/numpy.sqrt(2) # Distance between two adjacent logs
  n_logs = 10 # number of logs in each layer
  w = 0.2*Vperiod # width of the logs
  h = 0.25*Vperiod # heigth of logs (should be 1/4 for fcc to not overlap)
  print('w = '+str(w))
  print('h = '+str(h))
  
  L = (n_logs-1)*Hperiod+w+Hperiod # Length of logs (should > (n_logs-1)*Hperiod+w)
  n_layers = 4*2 # Number of layers of logs required

  wall_thickness = 0
  XL = 0.5*wall_thickness # Lower edge of the simulation domain in x direction.
  YL = 0.5*wall_thickness # Lower edge of the simulation domain in y direction.
  ZL = 0 # Lower edge of the simulation domain in z direction.

  box_size = 11
  XU = XL+box_size # Upper edge of the simulation domain in x direction.
  YU = YL+box_size # Upper edge of the simulation domain in y direction.
  ZU = 4 # Upper edge of the simulation domain in z direction.

  Nlayers_Z = n_layers
  NRodsPerLayer_X = n_logs
  NRodsPerLayer_Y = n_logs

  substrate_height = 0
  hole_height = 0
  woodpile_Zoffset = substrate_height + 0.5*h + hole_height
  wall_height = n_layers*h
  
  leg_width = 5

  box = GWLobject()

  BottomToTop = False
  
  LineDistance_Box = 0.200
  
  for nVert in [1]:
    woodpile_obj = Woodpile()
    woodpile_obj.BottomToTop = 0
    woodpile_obj.Nlayers_Z = Nlayers_Z
    woodpile_obj.NRodsPerLayer_X = NRodsPerLayer_X
    woodpile_obj.NRodsPerLayer_Y = NRodsPerLayer_Y
    woodpile_obj.interRodDistance = Hperiod
    woodpile_obj.interLayerDistance = h

    woodpile_obj.LineDistance_Horizontal = 0.050
    woodpile_obj.LineNumber_Vertical = nVert #int(woodpile_obj.interLayerDistance/woodpile_obj.LineDistance_Vertical)
    woodpile_obj.LineDistance_Vertical = woodpile_obj.interLayerDistance/woodpile_obj.LineNumber_Vertical
    woodpile_obj.LineNumber_Horizontal = 1

    woodpile_obj.initialDirection = 0

    woodpile_obj.initialLayerType_X = 0
    woodpile_obj.initialLayerType_Y = 0

    woodpile_obj.Xmin = XL
    woodpile_obj.Xmax = XU
    woodpile_obj.Ymin = YL
    woodpile_obj.Ymax = YU

    woodpile_obj.Xoffset = 0.5*(w + woodpile_obj.interRodDistance)
    woodpile_obj.Yoffset = 0.5*(w + woodpile_obj.interRodDistance)

    woodpile_obj.isSymmetrical = False

    #subfilename = 'woodpile.interRodDist_'+'1.04'+'.NX_'+str(NRodsPerLayer_X)+'.NY_'+str(NRodsPerLayer_Y)+'.Nlayers_Z_'+str(Nlayers_Z)+'.nVert_'+str(woodpile_obj.LineNumber_Vertical)+'.gwl'

    #filename = DSTDIR + os.path.sep + subfilename
    #GWL_obj = woodpile_obj.getGWL()
    #GWL_obj.write_GWL(filename, writingOffset = [0,0,woodpile_Zoffset,0] )

    BASENAME = 'woodpile'
    woodpile_obj.writeGWL(DSTDIR+os.path.sep+BASENAME+'.gwl')
    woodpile_obj.writeBFDTD(DSTDIR+os.path.sep+BASENAME+'.geo')

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('DSTDIR', default=tempfile.gettempdir(), nargs='?')
  args = parser.parse_args()
  print(args.DSTDIR)

  createWoodpile_1(args.DSTDIR)

  #woodpile_obj = Woodpile()
  #BASENAME = 'woodpile'
  #woodpile_obj.write_GWL(DSTDIR+os.path.sep+BASENAME+'.gwl')
  #woodpile_obj.write_BFDTD(DSTDIR+os.path.sep+BASENAME+'.geo')

  print( 'Output in ' + args.DSTDIR)
    
if __name__ == "__main__":
  main()
