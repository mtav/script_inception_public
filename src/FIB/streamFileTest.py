#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import math
import sys
import os
import getopt
import numpy

if __name__ == '__main__':

  #projectName='r2';
  ## projectName='29Oct10KXSm_206_800_150pA_m0.5';
  ## folder=['ANONYMIZED\MyMatlab\myPhotonicsPackage\FIB\',projectName,'\'];
  #folder=['.',filesep,projectName,filesep];
  #mkdir(folder);

  spotSizes={1:8,\
  4: 12,\
  11: 15,\
  70: 25,\
  150: 35,\
  350: 55,\
  1000: 80,\
  2700: 120,\
  6600: 270,\
  11500: 500}

  scanType='s';  #  Can be 'v' or 'h' or 's'

  #sr=0.42; #The sputter rate µm3/nC 
  mag=36000;
  rep=1;
  bC=150; #Beam current.
  overlap=0.5;
  #depth=1000; #depth of trench (nm)

  h=0.040
  c=0.080
  t=0.011667
  w=0.080

  A=numpy.array([h])

  R=numpy.array([h+w+c+t,h+w*2+c*2+t*3,h+w*3+c*3+t*6,h+w*4+c*4+t*10,h+w*5+c*5+t*15,h+w*6+c*6+t*21])

  r=numpy.array([h+w,h+w*2+c+t,h+w*3+c*2+t*3,h+w*4+c*3+t*6,h+w*5+c*4+t*10,h+w*6+c*5+t*15])

  spotSize=spotSizes[bC]*1e-3;

  HFW=304000/mag; # Width of the horizontal scan-Horizontal Field Width-(um) 
  reso=HFW/4096; # size of each pixel (um).
  BeamStep=round((spotSize-spotSize/2*overlap)/reso);

  Asq=(A/reso)**2
  Rsq=(R/reso)**2
  rsq=(r/reso)**2

  #print 2.5*max(R)
  #print HFW
  if (2.5*max(R)>HFW):
      disp('R is too big to fit to the screen')
      sys.exit(-1)

  Q1=numpy.zeros((320,240));
  #Q1=zeros((3335,3900));
  #print Q1

  cy=0.5*Q1.shape[0];
  cx=0.5*Q1.shape[1];

  Npoints=0;

  print('Creating Q1 matrix')
  for m in range(Q1.shape[0]):
    print(('m/Q1.shape[0] = ',m/Q1.shape[0]))
    #print(('m/size(Q1,1) = ',m/Q1.shape[0]))
    for n in range(Q1.shape[1]):
      distsq=(m-cy)**2+(n-cx)**2;
      #distsq=(n-cx)**2;
      if (distsq<Asq):
        Q1[m,n] = 1; Npoints = Npoints + 1;
      for idx in range(len(R)):
        if (distsq<Rsq[idx] and distsq>rsq[idx]):
          Q1[m,n]=1; Npoints = Npoints+1;

  sys.exit(0)

  #disp('Creating xpar,ypar')
  #xpar=zeros(1,Npoints);
  #ypar=zeros(1,Npoints);
  #idx=1;
  #for n=1:size(Q1,2)
      #for m=1:size(Q1,1)
              #if Q1(m,n)==1
                  #xpar(idx) = n;
                  #ypar(idx) = m;
                  #idx = idx+1;
              #end
      #end
  #end

  #disp('Writing stream file')
  #dwell = 100;
  #fid=fopen(['test.str'],'w+');
  #fprintf(fid,'s\r\n%i\r\n%i\r\n',rep,length(xpar));
  #fprintf(fid,[num2str(dwell),' %i %i\r\n'],[xpar;ypar]);
  #fclose(fid);

  #imagesc(Q1)
  #pause(1)

  #return

  ### Crop from top
          #numCropCellsV=0;
          #o=1;
          #while (sum(Q1(o,:))==0)
              #o=o+1;            
          #end
          #Q1=Q1(o:end,:);
          #numCropCellsV=o-1;
  ### Crop from bottom
          #o=size(Q1,1);
          #while (sum(Q1(o,:))==0)
              #o=o-1;            
          #end
          #Q1=Q1(1:o,:);
  ### Crop from left
          #numCropCellsH=0;
          #o=1;
          #while (sum(Q1(:,o))==0)
              #o=o+1;            
          #end
          #Q1=Q1(:,o:end);
          #numCropCellsH=o-1;

  ### Crop from right
          #o=size(Q1,2);
          #while (sum(Q1(:,o))==0)
              #o=o-1;            
          #end
          #Q1=Q1(:,1:o);
  #[X,Y]=imageToEtchPath(Q1,BeamStep,0,'rough',0);

  #X=X+numCropCellsH;
  #Y=Y+numCropCellsH;

  #save([folder,projectName,'.mat'],'X','Y');

  #figure
  #plot(X,Y);
