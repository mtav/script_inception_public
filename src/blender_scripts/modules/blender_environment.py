#!/usr/bin/env python
# -*- coding: utf-8 -*-

# To make Blender happy:
bl_info = {"name":"blender_environment", "category": "User"}

import os

if __name__ == '__main__':
  #print('\1 = '+str(os.getenv('\1')))

  print('BLENDERDATADIR = '+str(os.getenv('BLENDERDATADIR')))

  print('BLENDER_USER_SCRIPTS = '+str(os.getenv('BLENDER_USER_SCRIPTS')))
    #BLENDER_USER_SCRIPTS
    #BLENDER_USER_CONFIG
    #BLENDER_USER_SCRIPTS
    #BLENDER_SYSTEM_SCRIPTS
    #BLENDER_USER_DATAFILES
    #BLENDER_SYSTEM_DATAFILES
    #BLENDER_SYSTEM_PYTHON
    #TMP
    #TMPDIR
    #SDL_AUDIODRIVER
    #PYTHONHOME
