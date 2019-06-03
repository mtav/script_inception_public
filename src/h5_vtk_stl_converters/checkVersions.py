#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import vtk

def checkVersions():
  print('Python version:\n {}\n'.format(sys.version))
  print('VTK version:\n Source: {}\n Major: {}\n Minor: {}'.format(vtk.vtkVersion.GetVTKSourceVersion(), vtk.vtkVersion.GetVTKMajorVersion(), vtk.vtkVersion.GetVTKMinorVersion()))  
  return

if __name__ == '__main__':
  checkVersions()
