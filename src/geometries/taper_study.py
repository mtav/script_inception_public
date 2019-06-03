#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import tempfile

from utilities.common import *
from rectangular_yagi_with_taper import *

valid_defect_types = ['cylinder_holes',
                      'block_holes',
                      'cylinder_layers',
                      'grating']

def custom_taper():
  
  # Warning: The cavity is actually ~lambda/2 here and lambda0 is not 1 as originally intended... But the pictures look good for illustrations.
  # .. todo:: fix so we get the intended lambda/4 DBRs + lambda cavity
  
  parser = argparse.ArgumentParser()
  parser.add_argument('-d','--destdir', dest='DSTDIR', default=tempfile.gettempdir())
  args = parser.parse_args()  
  print(args.DSTDIR)

  Lambda_mum = 0.637
  nHigh = 2.4
  nLow = 1
  Lambda_avg = Lambda_mum*(1/nHigh + 1/nLow)

  Nbottom = 6
  Ntop = 3
  doubleLayer_DBR = [1/2]
  doubleLayer_DBR_bottom = Nbottom*doubleLayer_DBR
  doubleLayer_DBR_top = Ntop*doubleLayer_DBR
  doubleLayer_taper_bottom = [1/3, 1/4, 1/5]
  doubleLayer_taper_top = list(reversed(doubleLayer_taper_bottom))
  doubleLayer_cavity = [1]  
  
  doubleLayer_size = Nbottom*doubleLayer_DBR + doubleLayer_taper_bottom + doubleLayer_cavity + doubleLayer_taper_top + Ntop*doubleLayer_DBR
  print(doubleLayer_size)

  k = Lambda_avg / numpy.array(doubleLayer_size)
  print(k)
  
  layer_size_all = []
  for L in doubleLayer_DBR_bottom:
    k = Lambda_avg / L
    dH = Lambda_mum/(k*nHigh)
    dL = Lambda_mum/(k*nLow)
    layer_size_all.extend([dH, dL])
  #print(layer_size_all)

  #layer_size_all = []
  for L in doubleLayer_taper_bottom:
    k = Lambda_avg / L
    dH = Lambda_mum/(k*nHigh)
    dL = Lambda_mum/(k*nLow)
    layer_size_all.extend([dH, dL])
  #print(layer_size_all)

  #layer_size_all = []
  # .. todo:: This should get special handling because it is only one layer so Lambda_avg should be different.
  for L in doubleLayer_cavity:
    k = Lambda_avg / L
    dH = Lambda_mum/(k*nHigh)
    dL = Lambda_mum/(k*nLow)
    layer_size_all.extend([dH])
  #print(layer_size_all)

  #layer_size_all = []
  for L in doubleLayer_taper_top:
    k = Lambda_avg / L
    dH = Lambda_mum/(k*nHigh)
    dL = Lambda_mum/(k*nLow)
    layer_size_all.extend([dL, dH])
  #print(layer_size_all)
  
  #layer_size_all = []
  for L in doubleLayer_DBR_top:
    k = Lambda_avg / L
    dH = Lambda_mum/(k*nHigh)
    dL = Lambda_mum/(k*nLow)
    layer_size_all.extend([dL, dH])
  print(layer_size_all)
  
  excitation_cavity = [0]*len(layer_size_all)
  
  taper_name = 'custom_taper'
  pillar_diametro = 0.5
  defect_type_list = valid_defect_types
  PML = False
  
  for defect_type in defect_type_list:
    SUBDSTDIR = os.path.join(args.DSTDIR, str(taper_name))
    if not os.path.isdir(SUBDSTDIR):
      os.makedirs(SUBDSTDIR)
    BASENAME = defect_type
    rectangularYagiWithTaper(SUBDSTDIR, BASENAME, nHigh, nLow, Lambda_mum, layer_size_all, excitation_cavity, PML, pillar_diametro, defect_type)

def main():
  '''
  example: 
  ./taper_study.py -d /tmp/foo ./taper_study_part.txt
  '''
  parser = argparse.ArgumentParser()
  parser.add_argument('-d','--destdir', dest='DSTDIR', default=tempfile.gettempdir())
  parser.add_argument('INFILE')
  args = parser.parse_args()  
  print(args.DSTDIR)
  
  Nsims = 0
  if not os.path.isdir(args.DSTDIR):
    os.mkdir(args.DSTDIR)

  with open(args.INFILE, 'r') as f:
    for line in f:
      if len(line.strip())>0:
        tab = line.strip().split('\t')
        #print tab
        
        ###############
        # get taper parameters
        taper_name = tab[0]
        print('=== {} ==='.format(taper_name))
        denominator_factor_DBR_left_nHigh = float(tab[1])
        denominator_factor_DBR_left_nLow = float(tab[2])
        
        denominator_factor_taper_left = []
        for s in tab[3:9]:
          if len(s) != 0:
            denominator_factor_taper_left.append(float(s))
        
        denominator_factor_cavity = float(tab[9])
        
        denominator_factor_taper_right = []
        for s in tab[10:16]:
          if len(s) != 0:
            denominator_factor_taper_right.append(float(s))
        
        denominator_factor_DBR_right_nLow = float(tab[16])
        denominator_factor_DBR_right_nHigh = float(tab[17])
        ###############
  
        nHigh = 2.4
        nLow = 1
        Lambda_mum = 0.637
      
        #[0.65,0.675,0.70,0.71,0.725,0.72,0.73,0.74,0.75,0.775,0.80,0.84,1.0,1.25,1.50,1.66,1.75,2.0,2.5]
        #[0.340,0.5,0.65,0.675,0.70,0.71,0.725,0.72,0.73,0.74,0.75,0.775,0.80,0.84,1.0,1.25,1.50,1.66,1.75,2.0,2.5]
        #for pillar_diametro in [0.340,0.5,1]:
    
        taper_type = 0
        PML = False
  
        #defect_type_list = ['cylinder_holes','block_holes','grating']
        #pillar_diametro_list = [0.340,0.5,0.65,0.675,0.70,0.71,0.725,0.72,0.73,0.74,0.75,0.775,0.80,0.84,1.0,1.25,1.50,1.66,1.75,2.0,2.5]
        #Npair_list = [(33,24),(33,25),(33,26),(33,27),(33,28),(4,4),(30,25),(25,25)]
  
        #defect_type_list = ['cylinder_holes','block_holes','grating']
        defect_type_list = valid_defect_types
        #pillar_diametro_list = [0.340,0.5,0.65,0.675,0.70,0.71,0.725,0.72,0.73,0.74,0.75,0.775,0.80,0.84,1.0,1.25,1.50,1.66,1.75,2.0,2.5]
        pillar_diametro_list = [0.5]
        #Npair_list = [(33,24)]
        Npair_list = [(6, 3)]
        
        for defect_type in defect_type_list:
          for pillar_diametro in pillar_diametro_list:
            for (Nbottom,Ntop) in Npair_list:
                Nsims = Nsims + 1
                #break
                #SUBDSTDIR = os.path.join(args.DSTDIR, defect_type, str(pillar_diametro), str(Nbottom)+'_'+str(Ntop), str(taper_name))
                SUBDSTDIR = os.path.join(args.DSTDIR, str(taper_name))
                if not os.path.isdir(SUBDSTDIR):
                  os.makedirs(SUBDSTDIR)
                layer_size_all, excitation_cavity = calculateLayerSizes(taper_type, Nbottom, Ntop, Lambda_mum, nHigh, nLow,
                  denominator_factor_DBR_left_nHigh, denominator_factor_DBR_left_nLow, denominator_factor_taper_left,
                  denominator_factor_cavity,
                  denominator_factor_taper_right, denominator_factor_DBR_right_nLow, denominator_factor_DBR_right_nHigh)
                #BASENAME = 'rectangularYagiWithTaper.Lambda_'+str(Lambda_mum)+'.Nbottom_'+str(Nbottom)+'.Ntop_'+str(Ntop)+'.PML_'+str(PML)+'.taper_type_'+str(taper_type)+'.pillar_diametro_'+str(pillar_diametro)
                #BASENAME = 'taper_study'
                BASENAME = defect_type
                rectangularYagiWithTaper(SUBDSTDIR, BASENAME, nHigh, nLow, Lambda_mum, layer_size_all, excitation_cavity, PML, pillar_diametro, defect_type)

  print('Nsims = '+str(Nsims))
  print('len(defect_type_list) = '+str(len(defect_type_list)))
  print('len(pillar_diametro_list) = '+str(len(pillar_diametro_list)))
  print('len(Npair_list) = '+str(len(Npair_list)))

if __name__ == "__main__":
  custom_taper()
  #main()
