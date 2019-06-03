#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import getopt
import fnmatch
import os, os.path
import string
from optparse import OptionParser
import glob
import re
#from sets import Set
from subprocess import call
from special_ops.SO_reportGenerator import reportGenerator

class Foo:
  def __init__(self, filename):
    self.Filename = filename
    pattern = re.compile("([xyz]).+id..\.E.mod\.max_([\d.]+)\.lambda\(nm\)_([\d.]+)\.freq\(Mhz\)_([\d.]+)\.pos\(mum\)_([\d.]+)\.png")
    m = pattern.match(self.Filename)
    #print m
    if m:
      #print m.groups()
      self.Plane = m.group(1)
      self.MaxValue = float(m.group(2))
      self.Lambda = float(m.group(3))
      self.Freq = float(m.group(4))
      self.Pos = float(m.group(5))
    else:
      print('ERROR: NO MATCH : ', filename)
      sys.exit(-1)

      #Xpos_set.add(pos)
      #freq_set.add(freq)
      #lambda_set.add(Lambda)

    #self.r = realpart
    #self.i = imagpart

def mergePictures(directory,FirstPic):
  owd = os.getcwd()

  os.chdir(directory)
  
  print(('os.getcwd() = ',os.getcwd()))
  plane_filenames = glob.glob('[xyz]*.png')
  print(('plane_filenames = ',plane_filenames))
  
  plane_list=[]
  
  Xpos_set=set([])
  Ypos_set=set([])
  Zpos_set=set([])
  freq_set=set([])
  lambda_set=set([])
  
  for filename in plane_filenames:
    p = Foo(filename)
    plane_list.append(p)
    if p.Plane=='x':
      Xpos_set.add(p.Pos)
    elif p.Plane=='y':
      Ypos_set.add(p.Pos)
    else:
      Zpos_set.add(p.Pos)
    freq_set.add(p.Freq)
    lambda_set.add(p.Lambda)
  
  Xpos_set=sorted(list(Xpos_set))
  Ypos_set=sorted(list(Ypos_set))
  Zpos_set=sorted(list(Zpos_set))
  lambda_set=sorted(list(lambda_set))
  
  print(('Xpos_set = ', Xpos_set))
  print(('Ypos_set = ', Ypos_set))
  print(('Zpos_set = ', Zpos_set))
  print(('lambda_set = ', lambda_set))
  
  if len(Xpos_set)!=3 and len(Xpos_set)!=1:
    print('WARNING: len(Xpos_set)=',len(Xpos_set))
    os.chdir(owd)
    return(1)
    #sys.exit(-1)
  
  if len(Ypos_set)!=3 and len(Ypos_set)!=1:
    print('WARNING: len(Ypos_set)=',len(Ypos_set))
    os.chdir(owd)
    return(1)
    #sys.exit(-1)
  
  if len(Zpos_set)!=3 and len(Zpos_set)!=1:
    print('WARNING: len(Zpos_set)=',len(Zpos_set))
    os.chdir(owd)
    return(1)
    #sys.exit(-1)
    
  if len(Xpos_set)==1:
    Xmid = 0
  else:
    Xmid = 1
  if len(Ypos_set)==1:
    Ymid = 0
  else:
    Ymid = 1
  if len(Zpos_set)==1:
    Zmid = 0
  else:
    Zmid = 1
     
  outFile_list = []
  print('=== To merge: ===')
  for Lambda in lambda_set:
    for p in plane_list:
      if p.Plane=='x' and p.Pos==Xpos_set[Xmid] and p.Lambda==Lambda:
        #print 'BIP 1'
        p1=p
      if p.Plane=='y' and p.Pos==Ypos_set[Ymid] and p.Lambda==Lambda:
        #print 'BIP 2'
        p2=p
      if p.Plane=='z' and p.Pos==Zpos_set[Zmid] and p.Lambda==Lambda:
        #print 'BIP 3'
        p3=p
    print(p1.Filename+' + '+p2.Filename+' + '+p3.Filename+' -> '+str(Lambda)+'.png')
    outFile = str(Lambda)+'.png'
    cmd=['convert', p1.Filename, '(', p2.Filename, p3.Filename, '-append', ')', '-gravity', 'center', '+append', outFile]
    outFile_list.append(outFile)
    print(cmd)
    call(cmd)
  
  infiles = glob.glob('*.in')
  if not infiles:
    print('no infile found')
  else:
    base = os.path.splitext(infiles[0])[0]

  title = base
  texfile = base+'.report.tex'

  #texfile = 'tmp.tex'
  #picture_list = ['p001id.png']
  picture_list = [FirstPic]
  picture_list.extend(outFile_list)
  title_list = [title]*len(picture_list)
  
  print('texfile = ', texfile)
  print('title_list = ', title_list)
  print('picture_list = ', picture_list)
  reportGenerator(texfile, title_list, picture_list)
  
  print('=== To delete: ===')
  for p in plane_list:
    print(p.Filename)
    os.remove(p.Filename)
    #if p.Plane=='x' and p.Pos==Xpos_set[0] or p.Pos==Xpos_set[2]:
      #print p.Filename
      #os.remove(p.Filename)
    
  os.chdir(owd)
  return(0)
  #sys.exit(0)

if __name__ == '__main__':
  # temp main
  # loop recursively through dirs
  print(('sys.argv[1] = ',sys.argv[1]))
  mergePictures(sys.argv[1],sys.argv[2])
  for root, dirs, files in os.walk(sys.argv[1]):
    for d in dirs:
      localdir = os.path.join(root,d)
      print('localdir = ', localdir)
      mergePictures(localdir,sys.argv[2])
