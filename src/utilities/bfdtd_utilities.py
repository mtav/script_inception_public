#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def rerun_with_new_excitation(src, dst, excitation_wavelength_nm, excitation_time_constant):
  ''' Copy src to dst, only changing excitation_wavelength_nm and excitation_time_constant'''
  src = os.path.abspath(src).rstrip(os.sep)
  dst = os.path.abspath(dst).rstrip(os.sep)
  if os.path.isdir(src):
    print(src +' is a directory')
    FDTDobj = bfdtd.readBristolFDTD(src+os.sep+os.path.basename(src)+'.in')
    fileBaseName = os.path.basename(src)
  else:
    print(src +' is not a directory')
    FDTDobj = bfdtd.readBristolFDTD(src)
    fileBaseName = os.path.splitext(os.path.basename(src))[0]
    
  FDTDobj.excitation_list[0].setTimeConstant(excitation_time_constant)
  FDTDobj.excitation_list[0].setLambda(1e-3*excitation_wavelength_nm)
    
  FDTDobj.writeAll(dst,fileBaseName)
  bfdtd.GEOshellscript(dst+os.sep+fileBaseName+'.sh', fileBaseName,'$HOME/bin/fdtd', '$JOBDIR', WALLTIME = 360)

def copyBFDTD(src,dst):
  ''' Copy src to dst '''
  src = src.rstrip(os.sep)
  dst = dst.rstrip(os.sep)
  if os.path.isdir(src):
    print(src +' is a directory')
    FDTDobj = bfdtd.readBristolFDTD(src+os.sep+os.path.basename(src)+'.in')
    fileBaseName = os.path.basename(src)
  else:
    print(src +' is not a directory')
    FDTDobj = bfdtd.readBristolFDTD(src)
    fileBaseName = os.path.splitext(os.path.basename(src))[0]
  
  FDTDobj.writeAll(dst,fileBaseName)
  bfdtd.GEOshellscript(dst+os.sep+fileBaseName+'.sh', fileBaseName,'$HOME/bin/fdtd', '$JOBDIR', WALLTIME = 360)

def efficiency_run(src, dst):
  ''' Copy src to dst while removing the geometry '''
  src = os.path.abspath(src).rstrip(os.sep)
  dst = os.path.abspath(dst).rstrip(os.sep)
  if os.path.isdir(src):
    print(src +' is a directory')
    FDTDobj = bfdtd.readBristolFDTD(src+os.sep+os.path.basename(src)+'.in')
    fileBaseName = os.path.basename(src)
  else:
    print(src +' is not a directory')
    FDTDobj = bfdtd.readBristolFDTD(src)
    fileBaseName = os.path.splitext(os.path.basename(src))[0]
    
  FDTDobj.geometry_object_list[:] = []
  FDTDobj.writeAll(dst,fileBaseName)
