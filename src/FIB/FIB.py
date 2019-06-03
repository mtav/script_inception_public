#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Definitions:
#  HFW : "Horizontal Field Width", i.e. horizontal size of the sample visible on the screen -> varies with magnification
#  HFW_at_mag1 : HFW when the magnification is set to 1, i.e. no magnification. Corresponds to the horizontal size of the screen -> is constant.
#  mag : magnification = HFW_at_mag1_mum / HFW_mum
#  HFW_mum : HFW in micrometers
#  HFW_at_mag1_mum : HFW_at_mag1 in micrometers

HFW_at_mag1_mum = 304000
ScreenWidth_pxl = 4096

def getResolution(mag):
  '''
  returns (res_mum_per_pxl, HFW_mum) where:
  res_mum_per_pxl : resolution in micrometers per pixel
  HFW_mum : size in micrometers of the area of the sample visible on the screen.
  '''
  HFW_mum = HFW_at_mag1_mum / mag # Width of the horizontal scan (mum).
  res_mum_per_pxl = HFW_mum / ScreenWidth_pxl # size of each pixel (mum/pxl).
  return(res_mum_per_pxl, HFW_mum)

def getPixelsPerMicron(mag):
  '''
  returns the number of pixels per micrometer for the given magnification "mag".
  '''
  (res_mum_per_pxl, HFW_mum) = getResolution(mag)
  return(1./res_mum_per_pxl)

def getMagFromScreenSizeInMicrons(HFW_mum):
  '''
  HFW_mum : size in micrometers of the area of the sample visible on the screen.
  '''
  mag = HFW_at_mag1_mum / HFW_mum
  return(mag)

def getSpotSize(beamCurrent):
  ''' function spotSize_mum = getSpotSize(beamCurrent) '''
  
  # size of circles in nm (1e-9m) as a function of the beamcurrent in pA (1e-12 A)
  spotSizes_nm = {1 : 8,
  4 : 12,
  11 : 15,
  70 : 25,
  150 : 35,
  350 : 55,
  1000 : 80,
  2700 : 120,
  6600 : 270,
  11500 : 500}
  if beamCurrent in spotSizes_nm.keys():
    spotSize_mum = spotSizes_nm[beamCurrent_idx]*1e-3
  else:
    sys.stderr.write('Invalid beamCurrent. Valid values are:\n')
    for (k,v) in spotSizes_nm.items():
      sys.stderr.write('beamCurrent = {} spotSizes_nm = {}\n'.format(k,v))
    sys.exit(-1)
  
  return(spotSize_mum)

# FIB distance estimation functions. Might be used in FIB picture postprocessing program eventually. Or in Gimp through a plugin...
# TODO: At the moment those formulas are only for distances in the Y (vertical) direction of the picture. Need to add support for any sort of line on the picture.
# Functions could be tested against FIB measurement tool. Method: Project (X,Y) points along Z axis onto arbitrary plane and corresponding normal.

def FIBdistanceHorizontal(tilt_deg, magnification, distance_on_picture_pxl, angle_to_horizontal_deg = 90, horizontal_width_of_picture_pxl = 1024):
  '''
  Returns the horizontal distance in mum based on the visible distance in pixels on the picture.
  Warning: formula for angled segments hasn't been fully verified yet.
  distance_on_picture_pxl, angle_to_horizontal_deg : Properties of the segment to measure on the picture, as given by the Gimp measurement tool for example.
  tilt_deg : Tilt of the sample relative to the FIB. Can be read from the picture legend.
  '''
  
  W_mum = HFW_at_mag1_mum/float(magnification); # Width of the horizontal scan (mum). (HFW = Horizontal Field Width)
  resolution = W_mum/horizontal_width_of_picture_pxl; # size of each pixel (mum/pxl).
  
  lx_visible_pxl = distance_on_picture_pxl*numpy.cos(numpy.deg2rad(angle_to_horizontal_deg))
  ly_visible_pxl = distance_on_picture_pxl*numpy.sin(numpy.deg2rad(angle_to_horizontal_deg))
  Lx_sample_pxl = lx_visible_pxl
  Ly_sample_pxl = ly_visible_pxl/numpy.cos(numpy.deg2rad(tilt_deg))
  L_sample_pxl = numpy.sqrt(pow(Lx_sample_pxl,2)+pow(Ly_sample_pxl,2))
  L_sample_mum = L_sample_pxl*resolution
  return L_sample_mum

def FIBdistanceVertical(tilt_deg, magnification, distance_on_picture_pxl, horizontal_width_of_picture_pxl = 1024):
  '''
  Returns the vertical distance in mum based on the visible distance in pixels on the picture. 
  Warning: Always assumes a vertical pixel distance measurement (because it's the only thing making sense assuming an orthographic projection)
  tilt_deg : Tilt of the sample relative to the FIB. Can be read from the picture legend.
  '''
  
  W_mum = HFW_at_mag1_mum/float(magnification); # Width of the horizontal scan (mum). (HFW = Horizontal Field Width)
  resolution = W_mum/horizontal_width_of_picture_pxl; # size of each pixel (mum/pxl).
  
  L_sample_mum = (distance_on_picture_pxl*resolution)/numpy.sin(numpy.deg2rad(tilt_deg))
  return L_sample_mum

# The stream file format:
#  s
#  REPETITIONS
#  Npoints
#  DWELL X Y
#  ...
#  DWELL X Y

#class StreamFile(object):
  #def __init__(self):
    #self.verbosity = 0
    #self.GWL_voxels = []

def readStrFile(filename):
  with open(filename, 'r') as f:
    f.readline()
    repetitions = int(f.readline())
    Npoints = int(f.readline())
    pointlist = Npoints*[0]
    for i in range(Npoints):
      line = f.readline().split()
      dwell = float(line[0])
      x = float(line[1])
      y = float(line[2])
      pointlist[i] = (dwell,x,y)
  return (repetitions, pointlist)

    #read_data = f.read()
#s\n

#s
#10
#0

if __name__ == '__main__':
  pass

