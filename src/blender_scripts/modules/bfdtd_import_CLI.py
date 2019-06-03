#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# EXPERIMENTAL

# To make Blender happy:
bl_info = {"name":"bfdtd_import_CLI - EXPERIMENTAL",
            "category": "Import-Export",
            "warning": "Under construction!"
            }

import Blender

if __name__ == '__main__':

  print(Blender.Get('scriptsdir'))
  Blender.Run(Blender.Get('scriptsdir')+'/layer_manager.py',1323)
