#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# To make Blender happy:
bl_info = {"name":"import_multiformat", "category": "User"}

##!BPY

#"""
#Name: 'Import filelist (*.in)'
#Blender: 249
#Group: 'Import'
#Tooltip: 'Import list of GWL and/or BFDTD files'
#"""

# utility script to load list of diverse files
# Meant for CLI usage as follows:
#  blender -P $HOME/.blender/scripts/bfdtd_import.py -- "$@"

from bfdtd.bfdtd_parser import *

import bpy
import os
import sys
from blender_scripts.bfdtd_import import *
from blender_scripts.GWL_import import *

if __name__ == "__main__":
  filename = sys.argv[-1]

  print('->Processing .in file : ', filename)
  
  fileList = []
  f_handle = open(filename, 'r')
  for line in f_handle:
      print('os.path.dirname(filename): ', os.path.dirname(filename)) # directory of .in file
      print('line.strip()=', line.strip()) # remove any \n or similar
      # this is done so that you don't have to be in the directory containing the .geo/.inp files
      #subfile = os.path.join(os.path.dirname(filename),os.path.basename(line.strip()))
      subfile = os.path.join(os.path.dirname(filename),line.strip())
      print('subfile: ', subfile)
      fileList.append(subfile)
  f_handle.close()
  print(fileList)
  
  for file in fileList:
    ext = getExtension(file)
    if ext == 'gwl':
      importGWL(file)
    elif ext == 'geo' or ext == 'inp' or ext == 'in':
      importBristolFDTD(file)
    else:
      print(('ERROR: Unknown file extension: '+ext))
      sys.exit()
