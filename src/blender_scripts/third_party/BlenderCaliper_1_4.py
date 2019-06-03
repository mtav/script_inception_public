#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# To make Blender happy:
bl_info = {"name":"Blender Caliper", "category": "User"}

"""
Name: 'Blender Caliper'
Blender: 243
Group: 'Wizards'
Tooltip: 'Display measurements in your scene.'
"""

__author__ = "macouno"
__url__ = ("http://www.alienhelpdesk.com")
__version__ = "1.4 28/02/07"

__bpydoc__ = """\

Usage:

Open the script in your script window.
Or open it in your text window and hit ALT + P;

Select the objects, meshes or mesh you want measured.
Set the settings you want altered.
Set what size one blender unit is in input style.
Set what sort of result you want in output style.
Run the script.

"""
## Code history
"""
Version 1.0 released 01/05/06

Version 1.1 released 02/05/06
  Bugs fixed:
    1. Text objects were not created on the selected layers.
  
Version 1.2 released 16/07/06
  Bugs fixed and features added:
    1. Text objects now resized as object not text size since the smallest text size was 0.1
    2. Alignment of text and arrows crashed the script if objects were directly above each other.
    3. Naming of some measurement objects in mesh mode was erroneous.
    4. Draw.Create lists have been removed, for fixing error messages in 2.42
    5. Added measurement alignment function.
    6. Made the cleaning and naming functions a bit more effective.
    7. Added measurement constraining function.
    8. Removed an error in mumile to muyard to mufeet conversion.
    9. Split the DATAHASH to BUTTON, DATA & STATE arrays.
    
Version 1.3 released 27/07/06
  Bugs fixed and features added:
    1. Due to changes in blender 2.42 the script didn't exit on ESC anymore.
    2. Measurement between the furthest edges in a mesh was incorrect.
    3. A wait cursor is now created whilst the script runs.
    4. If you run the script whilst you are in editmode, the script will return you to it when done.
    
Version 1.4 released 28/02/07
  Made the script complient with blender 2.43
"""
# --------------------------------------------------------------------------
# ***** BEGIN GPL LICENSE BLOCK *****
#
# Copyright (C) 2006: macouno, http://www.macouno.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc, 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# ***** END GPL LICENCE BLOCK *****
# --------------------------------------------------------------------------

import Blender
from Blender import *
import math

####################################################
# GLOBALS
####################################################

VERSION ='1.4'

## Set button variables (settings in the gui)
BUTTON = {
  'TEXTBV': Draw.Create(0.000),
  'TEXTEX': Draw.Create(0.00),
  'TEXTSIZE': Draw.Create(0.05),
  'TEXTOFFS': Draw.Create(0.2),
  'OBCOL': Draw.Create(1),
  'MOUT': Draw.Create(1),
  'MIN': Draw.Create(3),
  'MSCALE': Draw.Create(1.0),
  'MCONSTRAIN': Draw.Create(1),
  'MCONOBS': Draw.Create(1),
  'MDECIMAL': Draw.Create(1),
  'MDETAIL': Draw.Create(1),
  'ARROW': Draw.Create(1),
  'ARROWROT': Draw.Create(4),
  'ARROWSIZE': Draw.Create(0.1),
  'MAKETEXT': Draw.Create(1),
  'MAKEARROW': Draw.Create(1),
  'MAKECLEAN': Draw.Create(1),
  'MEASURE': Draw.Create(1),
  'MMODE': Draw.Create(1)
}
BUTTON['LAYERS'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

## Set data variables (settings not in the gui)
DATA = {
  'RESULT': "b",
  'DISTANCE': 0.0,
  'LOC1': 0,
  'LOC2': 0,
  'MESSAGE': "a",
  'OBNAME1': "a",
  'OBNAME2': "a",
  'MNAME1': "a",
  'MNAME2': "a"
}

## Set state variables (state of the blender file)
STATE = {}
STATE['LAYERS'] = Window.ViewLayers()

for a in range(len(STATE['LAYERS'])):
  
  BUTTON['LAYERS'][STATE['LAYERS'][a]] = 1

####################################################
# BASIC FUNCTIONS
####################################################

####################################################
# ALL MEASUREMENT CONVERSIONS
####################################################

## Everything to nm
def mucm_to_nm(x): return 10.0 * x
def mum_to_nm(x): return 1000.0 * x
def mm_to_nm(x): return 1000000.0 * x
def muinch_to_nm(x): return 25.4 * x
def foot_to_nm(x): return 304.8 * x
def muyard_to_nm(x): return 914.4 * x
def mumile_to_nm(x): return 1609344.0 * x

## Mm to everything
def nm_to_mucm(x): return x / 10.0
def nm_to_mum(x): return x / 1000.0
def nm_to_mm(x): return x / 1000000.0
def nm_to_muinch(x): return x / 25.4
def nm_to_foot(x): return x / 304.8
def nm_to_muyard(x): return x / 914.4
def nm_to_mumile(x): return x / 1609344.0

## Metric conversions
def mum_to_mucm(x): return 100.0 * x
def mucm_to_mum(x): return x / 100.0
def mm_to_mucm(x): return 100000.0 * x
def mucm_to_mm(x): return x / 100000.0
def mm_to_mum(x): return 1000.0 * x
def mum_to_mm(x): return x / 1000.0

## Imperial conversions
def foot_to_muinch(x): return 12.0 * x
def muinch_to_foot(x): return x / 12.0
def muyard_to_muinch(x): return 36.0 * x
def muinch_to_muyard(x): return x / 36.0
def muinch_to_mumile(x): return 63360.0 * x
def muinch_to_mumile(x): return x / 63360.0
def muyard_to_foot(x): return x * 3.0
def foot_to_muyard(x): return x / 3.0
def mumile_to_foot(x): return 5280.0 * x
def foot_to_mumile(x): return x / 5280.0
def mumile_to_muyard(x): return 1760.0 * x
def muyard_to_mumile(x): return x / 1760.0

####################################################
# GET SUB INCH VALUES LIKE 1/4 OR 3/8
####################################################

def GetSubInch(subInch):

  chkDiv = 0
  
  if BUTTON['MDECIMAL'].val is 2: subDiv = 4
  elif BUTTON['MDECIMAL'].val is 3: subDiv = 8
  elif BUTTON['MDECIMAL'].val is 4: subDiv = 16
  elif BUTTON['MDECIMAL'].val is 5: subDiv = 32
  elif BUTTON['MDECIMAL'].val is 6: subDiv = 64
  else: subDiv = 2

  ## Loop to increase the ammount of detail untill a limit is reached.
  while chkDiv is 0 and subDiv > 2:
    subDiv /= 2
    inDiv = int(round(subInch * subDiv))

    ## Check to make sure we've got an uneven nr (1 = uneven, 0 = even).
    chkDiv = (inDiv % 2)

  ## If the difference is too small make an empty string.
  if chkDiv is 0:
    subStr = ""
  ## Make a nice measurement string to add.
  else:
    subStr = " " + str(inDiv) +"/" + str(subDiv)
    
  return subStr

####################################################
# GET THE EULER FOR THE NEW OBJECTS
####################################################

def GetEuler(Loc1, Loc2, Distance):

  ## Get the location of the right verts to make the text face front.
  if Loc1[0] > Loc2[0]:
    LocX = Loc1[0]; LocY = Loc1[1]; LocZ = Loc2[2]
  else:
    LocX = Loc2[0]; LocY = Loc2[1]; LocZ = Loc1[2]

  ## Get the eulers needed to rotate the text correctly.
  if round(LocY, 5) != round(LocX, 5):
    EulZ = math.atan2(LocY,LocX)
    EulY = math.asin(LocZ/(Distance * 0.5))
  else:
    EulZ = 0.0
    EulY = (math.pi * 0.5)

  ## Make the euler for text rotation.
  if BUTTON['ARROWROT'].val is 4:
    NewEuler = Mathutils.Euler([(math.pi * 0.5),EulY,EulZ])
  elif BUTTON['ARROWROT'].val is 3:
    NewEuler = Mathutils.Euler([0,EulY,EulZ])
  elif BUTTON['ARROWROT'].val is 2:
    NewEuler = Mathutils.Euler([(math.pi * 0.5),-EulY,(math.pi +EulZ)])
  elif BUTTON['ARROWROT'].val is 1:
    NewEuler = Mathutils.Euler([0,-EulY,(math.pi + EulZ)])

  return NewEuler

####################################################
# SKIN THE NEW ARROW OBJECT
####################################################

def SkinObject(mez, VertList, FaceList, Distance):

  ## Loop through the list of all the vert locations and make verts.
  skinVertList = []
  for a in range(len(VertList)):
    
    if a < (len(VertList) / 2):
      skinVertList.extend([NMesh.Vert(((VertList[a][0] * BUTTON['ARROWSIZE'].val) - (Distance / 2)), (VertList[a][1] * BUTTON['ARROWSIZE'].val), (VertList[a][2]) * BUTTON['ARROWSIZE'].val)])
    else:
      skinVertList.extend([NMesh.Vert(((VertList[a][0] * BUTTON['ARROWSIZE'].val) + (Distance / 2)), (VertList[a][1] * BUTTON['ARROWSIZE'].val), (VertList[a][2]) * BUTTON['ARROWSIZE'].val)])
  mez.verts.extend(skinVertList)

  ## Loop though the list of all the face indexes and make faces.
  for a in range(len(FaceList)):
    if len(FaceList[a]) is 4:
      mez.faces.append(NMesh.Face([mez.verts[FaceList[a][0]], mez.verts[FaceList[a][1]], mez.verts[FaceList[a][2]], mez.verts[FaceList[a][3]]]))
    elif len(FaceList[a]) is 3:
      mez.faces.append(NMesh.Face([mez.verts[FaceList[a][0]], mez.verts[FaceList[a][1]], mez.verts[FaceList[a][2]]]))

####################################################
# GET THE ROUNDED RESULT
####################################################

def Getrounded(Distance):

  if BUTTON['MDECIMAL'].val is 1:
    Result = int(round(Distance))
  else:
    Result = round(Distance, (BUTTON['MDECIMAL'].val -1))
  return Result

####################################################
# GETTING THE MEASUREMENT FROM BLENDER UNITS
####################################################

def GetMeasurement():
  
  ## Constrain the measurement result.
  if BUTTON['MCONSTRAIN'].val > 1 and BUTTON['MCONOBS'].val is 0:
    Loc1 = DATA['LOC1']; Loc2 = DATA['LOC2']
    if BUTTON['MCONSTRAIN'].val is 2:
      DATA['DISTANCE'] = vertDist([0, 0, Loc1[2]], [0 ,0 ,Loc2[2]])
    elif BUTTON['MCONSTRAIN'].val is 3:
      DATA['DISTANCE'] = vertDist([0, Loc1[1], 0], [0 ,Loc2[1] ,0])
    elif BUTTON['MCONSTRAIN'].val is 4:
      DATA['DISTANCE'] = vertDist([Loc1[0], 0, 0], [Loc2[0] ,0 ,0])

  ## Get the measurement relative to the correct scale
  DATA['DISTANCE'] = BUTTON['MSCALE'].val * DATA['DISTANCE']

  DATA['RESULT'] = ""

  ## If not blender units convert to millimeters.
  if BUTTON['MOUT'].val != 9:
    ## Get the distance in nm to start with.
    if BUTTON['MIN'].val is 1: DATA['DISTANCE'] = DATA['DISTANCE']
    elif BUTTON['MIN'].val is 2: DATA['DISTANCE'] = mucm_to_nm(DATA['DISTANCE'])
    elif BUTTON['MIN'].val is 3: DATA['DISTANCE'] = mum_to_nm(DATA['DISTANCE'])
    elif BUTTON['MIN'].val is 4: DATA['DISTANCE'] = mm_to_nm(DATA['DISTANCE'])
    elif BUTTON['MIN'].val is 5: DATA['DISTANCE'] = muinch_to_nm(DATA['DISTANCE'])
    elif BUTTON['MIN'].val is 6: DATA['DISTANCE'] = foot_to_nm(DATA['DISTANCE'])
    elif BUTTON['MIN'].val is 7: DATA['DISTANCE'] = muyard_to_nm(DATA['DISTANCE'])
    elif BUTTON['MIN'].val is 8: DATA['DISTANCE'] = mumile_to_nm(DATA['DISTANCE'])

  ## Get metric results.
  if BUTTON['MOUT'].val < 5:
    
    ## Get the measurement result in kilometers.
    if BUTTON['MOUT'].val is 4:		
      DATA['DISTANCE'] = nm_to_mm(DATA['DISTANCE'])
      
      if BUTTON['MDETAIL'].val is 4:
        Result = Getrounded(DATA['DISTANCE'])
      else:
        Result = int(math.floor(DATA['DISTANCE']))
        
      if BUTTON['MDETAIL'].val is 4 or Result != 0:
        DATA['RESULT'] = str(Result) + " mm"
      
      if BUTTON['MDETAIL'].val < 4:
        NewMicrometers = mm_to_mum(DATA['DISTANCE'] - int(math.floor(DATA['DISTANCE'])))
        
        if BUTTON['MDETAIL'].val is 3:
          Result = Getrounded(NewMicrometers)
        else:
          Result = int(math.floor(NewMicrometers))

        if Result != 0 and DATA['RESULT'] != " " and DATA['RESULT'] != "":
          DATA['RESULT'] = DATA['RESULT'] + " " + str(Result) + " nm"
        elif DATA['RESULT'] is " " or DATA['RESULT'] is "":
          DATA['RESULT'] = "0 nm"
      
      if BUTTON['MDETAIL'].val < 3:
        NewMicroCentimeters = mum_to_mucm(NewMicrometers - int(math.floor(NewMicrometers)))
        
        if BUTTON['MDETAIL'].val is 2:
          Result = Getrounded(NewMicroCentimeters)
        else:
          Result = int(math.floor(NewMicroCentimeters))

        if Result != 0:
          DATA['RESULT'] = DATA['RESULT'] + " " + str(Result) + " mucm"
        
      if BUTTON['MDETAIL'].val is 1:
        NewNanometers = mucm_to_nm(NewMicroCentimeters - int(math.floor(NewMicroCentimeters)))
        
        if BUTTON['MDETAIL'].val is 1:
          Result = Getrounded(NewNanometers)
        else:
          Result = int(math.floor(NewNanometers))

        if Result != 0 and DATA['RESULT'] != " " and DATA['RESULT'] != "":
          DATA['RESULT'] = DATA['RESULT'] + " " + str(Result) + " nm"
        elif DATA['RESULT'] is " " or DATA['RESULT'] is "":
          DATA['RESULT'] = "0 nm"
      
    ## Get the measurement result in meters.
    elif BUTTON['MOUT'].val is 3:		
    
      DATA['DISTANCE'] = nm_to_mum(DATA['DISTANCE'])
      
      if BUTTON['MDETAIL'].val is 3:
        Result = Getrounded(DATA['DISTANCE'])
      else:
        Result = int(math.floor(DATA['DISTANCE']))
        
      if BUTTON['MDETAIL'].val is 3 or Result != 0:
        DATA['RESULT'] = str(Result) + " mum"
      
      if BUTTON['MDETAIL'].val < 3:
        NewMicroCentimeters = mum_to_mucm(DATA['DISTANCE'] - int(math.floor(DATA['DISTANCE'])))
        
        if BUTTON['MDETAIL'].val is 2:
          Result = Getrounded(NewMicroCentimeters)
        else:
          Result = int(math.floor(NewMicroCentimeters))

        if Result != 0:
          DATA['RESULT'] = DATA['RESULT'] + " " + str(Result) + " mucm"
        
      if BUTTON['MDETAIL'].val is 1:
        NewNanometers = mucm_to_nm(NewMicroCentimeters - int(math.floor(NewMicroCentimeters)))
        
        if BUTTON['MDETAIL'].val is 1:
          Result = Getrounded(NewNanometers)
        else:
          Result = int(math.floor(NewNanometers))

        if Result != 0 and DATA['RESULT'] != " " and DATA['RESULT'] != "":
          DATA['RESULT'] = DATA['RESULT'] + " " + str(Result) + " nm"
        elif DATA['RESULT'] is " " or DATA['RESULT'] is "":
          DATA['RESULT'] = "0 nm"
      
    ## Get the measurement result in centimeters.
    elif BUTTON['MOUT'].val is 2:
    
      DATA['DISTANCE'] = nm_to_mucm(DATA['DISTANCE'])
      
      if BUTTON['MDETAIL'].val is 2:
        Result = Getrounded(DATA['DISTANCE'])
      else:
        Result = int(math.floor(DATA['DISTANCE']))
        
      if BUTTON['MDETAIL'].val is 2 or Result != 0:
        DATA['RESULT'] = str(Result) + " mucm"
        
      if BUTTON['MDETAIL'].val is 1:
        NewNanometers = mucm_to_nm(DATA['DISTANCE'] - int(math.floor(DATA['DISTANCE'])))
        
        Result = Getrounded(NewNanometers)

        if Result != 0 and DATA['RESULT'] != " " and DATA['RESULT'] != "":
          DATA['RESULT'] = DATA['RESULT'] + " " + str(Result) + " nm"
        elif DATA['RESULT'] is " " or DATA['RESULT'] is "":
          DATA['RESULT'] = "0 nm"
    
    ## Get the measurement result in millimeters.
    else:
      Result = Getrounded(DATA['DISTANCE'])

      DATA['RESULT'] = DATA['RESULT'] + " " + str(Result) + " nm"
      
  ## Get imperial results.
  elif BUTTON['MOUT'].val < 9:
    
    DATA['RESULT'] = ""
  
    ## Get the result in mumiles.
    if BUTTON['MOUT'].val is 8:		
      DATA['DISTANCE'] = nm_to_mumile(DATA['DISTANCE'])
      
      if BUTTON['MDETAIL'].val is 4:
        Result = Getrounded(DATA['DISTANCE'])
      else:
        Result = int(math.floor(DATA['DISTANCE']))
      if BUTTON['MDETAIL'].val is 4 or Result != 0:
        DATA['RESULT'] = str(Result) + " mumile"
      
      if BUTTON['MDETAIL'].val < 4:
        NewMicroYards = mumile_to_muyard(DATA['DISTANCE'] - int(math.floor(DATA['DISTANCE'])))
        
        if BUTTON['MDETAIL'].val is 3:
          Result = Getrounded(NewMicroYards)
        else:
          Result = int(math.floor(NewMicroYards))

        if Result != 0:
          DATA['RESULT'] = DATA['RESULT'] + " " + str(Result) + " yd"
      
      if BUTTON['MDETAIL'].val < 3:
        NewMicroFeet = muyard_to_foot(NewMicroYards - int(math.floor(NewMicroYards)))
        
        if BUTTON['MDETAIL'].val is 2:
          Result = Getrounded(NewMicroFeet)
        else:
          Result = int(math.floor(NewMicroFeet))

        if Result != 0:
          DATA['RESULT'] = DATA['RESULT'] + " " + str(Result) + " ft"
        
      if BUTTON['MDETAIL'].val is 1:		    
      
        NewMicroInches = foot_to_muinch(NewMicroFeet - int(math.floor(NewMicroFeet)))
        
        if math.ceil(NewMicroInches) != 0:
        
          if BUTTON['MDECIMAL'].val is 1:
            DATA['RESULT'] = DATA['RESULT'] + " " + str(int(round(NewMicroInches))) + " in"
          else:
            ## Get the measurement smaller than muinches and nicely rounded so it doesn't go into too much detail.
            subInch = round(NewMicroInches - int(math.floor(NewMicroInches)), 2)
        
            MicroInches = int(math.floor(NewMicroInches))
          
            if subInch is 1:
              MicroInches = MicroInches + 1
            if MicroInches < 1:
              MicroInches = ""
            else:
              MicroInches = str(MicroInches)
              
            DATA['RESULT'] = DATA['RESULT'] + " " + MicroInches + GetSubInch(subInch) + " in"
            
        elif DATA['RESULT'] is "" or DATA['RESULT'] is " ":
        
          DATA['RESULT'] = "0 in"
    
    ## Get the result in muyards
    elif BUTTON['MOUT'].val is 7:
    
      DATA['DISTANCE'] = nm_to_muyard(DATA['DISTANCE'])
      
      if BUTTON['MDETAIL'].val is 3:
        Result = Getrounded(DATA['DISTANCE'])
      else:
        Result = int(math.floor(DATA['DISTANCE']))
      if BUTTON['MDETAIL'].val is 3 or Result != 0:
        DATA['RESULT'] = str(Result) + " yd"
      
      if BUTTON['MDETAIL'].val < 3:
        NewMicroFeet = muyard_to_foot(DATA['DISTANCE'] - int(math.floor(DATA['DISTANCE'])))
        
        if BUTTON['MDETAIL'].val is 3:
          Result = Getrounded(NewMicroFeet)
        else:
          Result = int(math.floor(NewMicroFeet))

        if Result != 0:
          DATA['RESULT'] = DATA['RESULT'] + " " + str(Result) + " ft"
        
      if BUTTON['MDETAIL'].val is 1:		    
      
        NewMicroInches = foot_to_muinch(NewMicroFeet - int(math.floor(NewMicroFeet)))
        
        if math.ceil(NewMicroInches) != 0:
        
          if BUTTON['MDECIMAL'].val is 1:
            DATA['RESULT'] = DATA['RESULT'] + " " + str(int(round(NewMicroInches))) + " in"
          else:
            ## Get the measurement smaller than muinches and nicely rounded so it doesn't go into too much detail.
            subInch = round(NewMicroInches - int(math.floor(NewMicroInches)), 2)
        
            MicroInches = int(math.floor(NewMicroInches))
          
            if subInch is 1:
              MicroInches = MicroInches + 1
            if MicroInches < 1:
              MicroInches = ""
            else:
              MicroInches = str(MicroInches)
              
            DATA['RESULT'] = DATA['RESULT'] + " " + MicroInches + GetSubInch(subInch) + " in"
            
        elif DATA['RESULT'] is "" or DATA['RESULT'] is " ":
        
          DATA['RESULT'] = "0 in"
      
    ## Get the result in mufeet
    elif BUTTON['MOUT'].val is 6:
    
      DATA['DISTANCE'] = nm_to_foot(DATA['DISTANCE'])
      
      if BUTTON['MDETAIL'].val is 2:
        Result = Getrounded(DATA['DISTANCE'])
      else:
        Result = int(math.floor(DATA['DISTANCE']))
      if BUTTON['MDETAIL'].val is 2 or Result != 0:
        DATA['RESULT'] = str(Result) + " ft"
      
      if BUTTON['MDETAIL'].val is 1:
      
        NewMicroInches = foot_to_muinch(DATA['DISTANCE'] - int(math.floor(DATA['DISTANCE'])))
        
        if math.ceil(NewMicroInches) != 0:
        
          if BUTTON['MDECIMAL'].val is 1:
            DATA['RESULT'] = DATA['RESULT'] + " " + str(int(round(NewMicroInches))) + " in"
          else:
            ## Get the measurement smaller than muinches and nicely rounded so it doesn't go into too much detail.
            subInch = round(NewMicroInches - int(math.floor(NewMicroInches)), 2)
        
            MicroInches = int(math.floor(NewMicroInches))
          
            if subInch is 1:
              MicroInches = MicroInches + 1
            if MicroInches < 1:
              MicroInches = ""
            else:
              MicroInches = str(MicroInches)
                  
            DATA['RESULT'] = DATA['RESULT'] + " " + MicroInches + GetSubInch(subInch) + " in"
            
        elif DATA['RESULT'] is "" or DATA['RESULT'] is " ":
        
          DATA['RESULT'] = "0 in"
            
    ## Get the result in muinches
    else:
      DATA['DISTANCE'] = nm_to_muinch(DATA['DISTANCE'])
      
      if BUTTON['MDECIMAL'].val is 1:
        DATA['RESULT'] = str(int(round(DATA['DISTANCE']))) + " in"
      else:
        ## Get the measurement smaller than muinches and nicely rounded so it doesn't go into too much detail.
        subInch = round(DATA['DISTANCE'] - int(math.floor(DATA['DISTANCE'])), 2)
      
        MicroInches = int(math.floor(DATA['DISTANCE']))
        
        if subInch is 1:
          MicroInches = MicroInches + 1
        if subInch is 0.0 and MicroInches is 0.0:
          MicroInches = "0"
        elif MicroInches < 1:
          MicroInches = ""
        else:
          MicroInches = str(MicroInches)
          
        DATA['RESULT'] = MicroInches + GetSubInch(subInch) + " in"
  
  ## Get straight blender unit result.
  else:
    DATA['RESULT'] = str(Getrounded(DATA['DISTANCE']))
    
  return DATA['RESULT']

####################################################
# TRANSFORMATIONS TO GET GLOBAL COORDS
####################################################

# Apply a matrix to a vert and return a vector.
def apply_transform(vert, matrix):
  x, y, z = vert
  xloc, yloc, zloc = matrix[3][0], matrix[3][1], matrix[3][2]
  return Mathutils.Vector(
  x*matrix[0][0] + y*matrix[1][0] + z*matrix[2][0] + xloc,
  x*matrix[0][1] + y*matrix[1][1] + z*matrix[2][1] + yloc,
  x*matrix[0][2] + y*matrix[1][2] + z*matrix[2][2] + zloc)

# Apply a matrix to a normal and return a vector.
def normal_transform(norm, matrix):
  matrix = matrix.rotationPart()
  x, y, z = norm
  return Mathutils.Vector(
  x*matrix[0][0] + y*matrix[1][0] + z*matrix[2][0],
  x*matrix[0][1] + y*matrix[1][1] + z*matrix[2][1],
  x*matrix[0][2] + y*matrix[1][2] + z*matrix[2][2])

####################################################
# GET THE MIDPOINT OF A FACE
####################################################
  
def getMidF(face, obName):

  ## Get the object matrix for applying
  tarObj = Object.Get(obName)
  
  ObMatrix = Mathutils.Matrix(tarObj.getMatrix('worldspace'))

  ## Set the midpoint variable.
  midLoc = [0.0,0.0,0.0]
  
  ## Loop through the verts.
  for a in range(len(face.v)):
  
    ## Get the global vert position by applying the matrix.
    vertCo = apply_transform(face.v[a].co, ObMatrix)
  
    ## Loop through the midLoc and add the vert coordinates.
    for b in range(len(midLoc)):
      midLoc[b] += vertCo[b]
    
  ## Loop through the midLoc and divide by the nr of verts.
  for a in range(len(midLoc)):
    midLoc[a] /= len(face.v)
  
  ## Return the midpoint of the face.
  return midLoc
  
####################################################
# EDGE LENGTH FUNCTION
####################################################

## Function for getting the distance between two points.
def vertDist(v1, v2):
  return Mathutils.Vector(v1[0]-v2[0], v1[1]-v2[1], v1[2]-v2[2]).length
  
####################################################
# REMOVE OLD OBJECTS
####################################################

def RemoveOldObs(One, Two, Three):

  ## Get the scene
  scene = Blender.Scene.GetCurrent()

  ## Get a list of all objects with the namestring in their names	
  ObjectList = [ob for ob in Blender.Scene.GetCurrent().getChildren() if str(One) + str(Two) + str(Three)  in ob.getName() or str(Two) + str(One) + str(Three) in ob.getName()]
  
  ## Loop through all the objects in the list
  for a in range(len(ObjectList)):

    ## Unlink the object from the scene
    scene.unlink(ObjectList[a])
  
####################################################
# DRAW A LINE AND TEXT 
####################################################

def DrawTitle(Text, Pos):

  BGL.glColor3f(0.7, 0.7 , 0.8)		# Light edge
  BGL.glRectf(4, (Pos - 4), 267, (Pos -3))

  BGL.glColor3f(0.9, 0.9, 0.95)
  BGL.glRasterPos2d(20, Pos)
  Draw.Text(Text, "small")
  
####################################################
# GETTING THE TWO CLOSEST Edges 
####################################################
  
def GetObjectVerts():

  Succes = False
  
  ## Create a list of all selected mesh objects
  DATA['OBJECTLIST'] = [ob for ob in Blender.Object.GetSelected() if ob.getType() == 'Mesh']
  
  ## Check to make sure there's 2 mesh objects selected
  if len(DATA['OBJECTLIST']) is 2:
  
    ## Get the names of the first mesh object.
    DATA['OBNAME1'] = DATA['OBJECTLIST'][0].getName()
    
    DATA['MNAME1'] = Object.Get(DATA['OBNAME1']).getData(1)

    me = NMesh.GetRaw(DATA['MNAME1'])
    
    ## Get the object matrix for applying
    tarObj = Object.Get(DATA['OBNAME1'])

    ObMatrix1 = Mathutils.Matrix(tarObj.getMatrix('worldspace'))
    
    ## Get the names of the second mesh object.
    DATA['OBNAME2'] = DATA['OBJECTLIST'][1].getName()
    DATA['MNAME2'] = Object.Get(DATA['OBNAME2']).getData(1)

    me2 = NMesh.GetRaw(DATA['MNAME2'])
    
    ## Get the object matrix for applying
    tarObj = Object.Get(DATA['OBNAME2'])
  
    ObMatrix2 = Mathutils.Matrix(tarObj.getMatrix('worldspace'))

    ## Loop through the faces of the object.
    for a in range(len(me.verts)):
    
      PosOne = Mathutils.MidpointVecs(apply_transform(me.verts[a].co, ObMatrix1), apply_transform(me.verts[a].co, ObMatrix1))

      ## Loop through the faces of the object.
      for b in range(len(me2.verts)):

        ## Get the position of the midpoint of this face
        PosTwo = Mathutils.MidpointVecs(apply_transform(me2.verts[b].co, ObMatrix2), apply_transform(me2.verts[b].co, ObMatrix2))

        ## Calculate the distance between the two midpoints
        CurDist = vertDist(PosOne, PosTwo)

        ## Getting the closest point
        if BUTTON['MEASURE'].val is 6:

          ## See whether it's the first measurement or if the points are closer.
          if a is 0 and b is 0 or DATA['DISTANCE'] > CurDist:

            DATA['LOC1'] = PosOne
            DATA['LOC2'] = PosTwo
            DATA['DISTANCE'] = CurDist
            Succes = True

        ## Getting the furthest point	
        else:
          ## See whether it's the first measurement or if the points are closer.
          if a is 0 and b is 0 or DATA['DISTANCE'] < CurDist:

            DATA['LOC1'] = PosOne
            DATA['LOC2'] = PosTwo
            DATA['DISTANCE'] = CurDist
            Succes = True
            
    if Succes is False:
      DATA['RESULT'] = "One of your two meshes has no verts!"
            
  else:
    DATA['RESULT'] = "No two mesh objects selected!"
    
  return Succes
  
####################################################
# GETTING THE TWO CLOSEST EDGES
####################################################
  
def GetObjectEdges():

  Succes = False
  
  ## Create a list of all selected mesh objects
  DATA['OBJECTLIST'] = [ob for ob in Blender.Object.GetSelected() if ob.getType() == 'Mesh']
  
  ## Check to make sure there's 2 mesh objects selected
  if len(DATA['OBJECTLIST']) is 2:
  
    ## Get the names of the first mesh object.
    DATA['OBNAME1'] = DATA['OBJECTLIST'][0].getName()
    
    DATA['MNAME1'] = Object.Get(DATA['OBNAME1']).getData(1)

    me = NMesh.GetRaw(DATA['MNAME1'])
    
    ## Get the object matrix for applying
    tarObj = Object.Get(DATA['OBNAME1'])

    ObMatrix1 = Mathutils.Matrix(tarObj.getMatrix('worldspace'))
    
    ## Get the names of the second mesh object.
    DATA['OBNAME2'] = DATA['OBJECTLIST'][1].getName()
    DATA['MNAME2'] = Object.Get(DATA['OBNAME2']).getData(1)

    me2 = NMesh.GetRaw(DATA['MNAME2'])
    
    ## Get the object matrix for applying
    tarObj = Object.Get(DATA['OBNAME2'])
  
    ObMatrix2 = Mathutils.Matrix(tarObj.getMatrix('worldspace'))

    ## Loop through the faces of the object.
    for a in range(len(me.edges)):
    
      PosOne = Mathutils.MidpointVecs(apply_transform(me.edges[a].v1.co, ObMatrix1), apply_transform(me.edges[a].v2.co, ObMatrix1))

      ## Loop through the faces of the object.
      for b in range(len(me2.edges)):

        ## Get the position of the midpoint of this face
        PosTwo = Mathutils.MidpointVecs(apply_transform(me2.edges[b].v1.co, ObMatrix2), apply_transform(me2.edges[b].v2.co, ObMatrix2))

        ## Calculate the distance between the two midpoints
        CurDist = vertDist(PosOne, PosTwo)

        ## Getting the closest point
        if BUTTON['MEASURE'].val is 4:

          ## See whether it's the first measurement or if the points are closer.
          if a is 0 and b is 0 or DATA['DISTANCE'] > CurDist:

            DATA['LOC1'] = PosOne
            DATA['LOC2'] = PosTwo
            DATA['DISTANCE'] = CurDist
            Succes = True

        ## Getting the furthest point	
        else:
          ## See whether it's the first measurement or if the points are closer.
          if a is 0 and b is 0 or DATA['DISTANCE'] < CurDist:

            DATA['LOC1'] = PosOne
            DATA['LOC2'] = PosTwo
            DATA['DISTANCE'] = CurDist
            Succes = True
            
    if Succes is False:
      DATA['RESULT'] = "One of your two meshes has no edges!"
      
  else:
    DATA['RESULT'] = "No two mesh objects selected!"
  return Succes
  
####################################################
# GETTING THE TWO CLOSEST FACES 
####################################################
  
def GetObjectFaces():

  Succes = False
  
  ## Create a list of all selected mesh objects
  DATA['OBJECTLIST'] = [ob for ob in Blender.Object.GetSelected() if ob.getType() == 'Mesh']
  
  ## Check to make sure there's 2 mesh objects selected
  if len(DATA['OBJECTLIST']) is 2:
  
    ## Get the names of the first mesh object.
    DATA['OBNAME1'] = DATA['OBJECTLIST'][0].getName()
    
    DATA['MNAME1'] = Object.Get(DATA['OBNAME1']).getData(1)

    me = NMesh.GetRaw(DATA['MNAME1'])

    ## Loop through the faces of the object.
    for a in range(len(me.faces)):

      ## Check to make sure the face has the required nr of verts.
      if len(me.faces[a].v) is 3 or len(me.faces[a].v) is 4:

        ## Get the position of the midpoint of this face
        PosOne = getMidF(me.faces[a], DATA['OBNAME1'])
        
        ## Get the names of the second mesh object.
        DATA['OBNAME2'] = DATA['OBJECTLIST'][1].getName()
        DATA['MNAME2'] = Object.Get(DATA['OBNAME2']).getData(1)

        me2 = NMesh.GetRaw(DATA['MNAME2'])

        ## Loop through the faces of the object.
        for b in range(len(me2.faces)):

          ## Check to make sure the face has the required nr of verts.
          if len(me2.faces[b].v) is 3 or len(me2.faces[b].v) is 4:

            ## Get the position of the midpoint of this face
            PosTwo = getMidF(me2.faces[b], DATA['OBNAME2'])
          
            ## Calculate the distance between the two midpoints
            CurDist = vertDist(PosOne, PosTwo)
            
            ## Getting the closest point
            if BUTTON['MEASURE'].val is 2:
            
              ## See whether it's the first measurement or if the points are closer.
              if a is 0 and b is 0 or DATA['DISTANCE'] > CurDist:

                DATA['LOC1'] = PosOne
                DATA['LOC2'] = PosTwo
                DATA['DISTANCE'] = CurDist
                Succes = True
                
            ## Getting the furthest point	
            else:
            
              ## See whether it's the first measurement or if the points are closer.
              if a is 0 and b is 0 or DATA['DISTANCE'] < CurDist:

                DATA['LOC1'] = PosOne
                DATA['LOC2'] = PosTwo
                DATA['DISTANCE'] = CurDist
                Succes = True
                
    if Succes is False:
      DATA['RESULT'] = "One of your two meshes has no faces!"
      
  else:
    DATA['RESULT'] = "No two mesh objects selected!"
  return Succes
    
####################################################
# GETTING THE OBJECT CENTERS
####################################################
  
def GetObjectCenters():

  Succes = False
  
  ## Create a list of all selected mesh objects
  DATA['OBJECTLIST'] = [ob for ob in Blender.Object.GetSelected()]
  
  ## Check to make sure there's 2 mesh objects selected
  if len(DATA['OBJECTLIST']) is 2:
  
    ## Get the names of the first mesh object.
    DATA['OBNAME1'] = DATA['OBJECTLIST'][0].getName()
    
    ## Get the position of the midpoint of this face
    DATA['LOC1'] = Object.Get(DATA['OBNAME1']).getLocation()
        
    ## Get the names of the second mesh object.
    DATA['OBNAME2'] = DATA['OBJECTLIST'][1].getName()

    ## Get the position of the midpoint of this face
    DATA['LOC2'] = Object.Get(DATA['OBNAME2']).getLocation()
          
    ## Calculate the distance between the two midpoints
    DATA['DISTANCE'] = vertDist(DATA['LOC1'], DATA['LOC2'])
    
    Succes = True
    
  if Succes is False:
    DATA['RESULT'] = "No two objects selected!"
    
  return Succes
    
####################################################
# GETTING THE TWO MESH FACES
####################################################
  
def GetMeshFaces():

  Succes = False
  
  ## Check to make sure there's 2 mesh objects selected
  if Object.GetSelected()[0].getType() == 'Mesh':
  
    ## Get the selected object
    DATA['OBNAME1'] = Object.GetSelected()[0].getName()

    ## Get the name of the mesh of the selected object
    DATA['MNAME1'] = Object.GetSelected()[0].getData(1)

    me = NMesh.GetRaw(DATA['MNAME1'])

    ## Get the two selected faces.
    if BUTTON['MEASURE'].val is 8:
      
      ## Create a list of all faces
      FaceList = []
      for f in me.faces:
        if f.sel:
          FaceList.append(f)

      if len(FaceList) is 2:

        for a in range(len(me.faces)):

          if me.faces[a] is FaceList[0]:

            for b in range(len(me.faces)):

              if me.faces[b] is FaceList[1]:
                ## Get the position of the midpoint of this face
                PosOne = getMidF(me.faces[a], DATA['OBNAME1'])

                ## Get the position of the midpoint of this face
                PosTwo = getMidF(me.faces[b], DATA['OBNAME1'])

                ## Calculate the distance between the two midpoints
                CurDist = vertDist(PosOne, PosTwo)

                DATA['LOC1'] = PosOne
                DATA['LOC2'] = PosTwo
                DATA['DISTANCE'] = CurDist
                DATA['OBNAME2'] = str(a) + str(b)
                Succes = True
                
      else:
        DATA['RESULT'] = "No two faces selected!"
        
    ## Get the closest or furthest faces.
    else:
    
      if len(me.faces) > 1:

        ## Loop through the faces of the object.
        for a in range(len(me.faces)):

          ## Check to make sure the face has the required nr of verts.
          if len(me.faces[a].v) is 3 or len(me.faces[a].v) is 4:

            ## Get the position of the midpoint of this face
            PosOne = getMidF(me.faces[a], DATA['OBNAME1'])

            ## Loop through the faces of the object.
            for b in range(len(me.faces)):

              ## Check to make sure the face has the required nr of verts.
              if len(me.faces[b].v) is 3 or len(me.faces[b].v) is 4:

                ## Get the position of the midpoint of this face
                PosTwo = getMidF(me.faces[b], DATA['OBNAME1'])

                ## Calculate the distance between the two midpoints
                CurDist = vertDist(PosOne, PosTwo)

                ## Getting the closest point
                if BUTTON['MEASURE'].val is 9:

                  ## See whether it's the first measurement or if the points are closer.
                  if a is 0 and b is 1 or DATA['DISTANCE'] > CurDist and a != b:

                    DATA['LOC1'] = PosOne
                    DATA['LOC2'] = PosTwo
                    DATA['DISTANCE'] = CurDist
                    DATA['OBNAME2'] = str(a) + str(b)
                    Succes = True

                ## Getting the furthest point	
                else:

                  ## See whether it's the first measurement or if the points are closer.
                  if a is 0 and b is 1 or DATA['DISTANCE'] < CurDist and a != b:

                    DATA['LOC1'] = PosOne
                    DATA['LOC2'] = PosTwo
                    DATA['DISTANCE'] = CurDist
                    DATA['OBNAME2'] = str(a) + str(b)
                    Succes = True
      else:
        DATA['RESULT'] = "Not enough faces for measurement!"

  else:
    DATA['RESULT'] = "No mesh object selected!"
  return Succes
  
####################################################
# GETTING THE TWO MESH EDGES
####################################################
  
def GetMeshEdges():

  Succes = False
  
  ## Check to make sure there's 2 mesh objects selected
  if Object.GetSelected()[0].getType() == 'Mesh':
  
    ## Get the selected object
    DATA['OBNAME1'] = Object.GetSelected()[0].getName()

    ## Get the name of the mesh of the selected object
    DATA['MNAME1'] = Object.GetSelected()[0].getData(1)

    ## Get the object matrix for applying
    tarObj = Object.Get(DATA['OBNAME1'])

    ObMatrix = Mathutils.Matrix(tarObj.getMatrix('worldspace'))
    
    me = NMesh.GetRaw(DATA['MNAME1'])

    ## Get the two selected faces.
    if BUTTON['MEASURE'].val is 11:
      
      ## Create a list of sel edges
      SEL = NMesh.EdgeFlags['SELECT']
      EdgeList = []
      for f in me.edges:
        if f.flag & SEL:
          EdgeList.append(f)

      if len(EdgeList) is 2:

        for a in range(len(me.edges)):

          if me.edges[a] is EdgeList[0]:

            for b in range(len(me.edges)):

              if me.edges[b] is EdgeList[1]:
                PosOne = Mathutils.MidpointVecs(apply_transform(me.edges[a].v1.co, ObMatrix), apply_transform(me.edges[a].v2.co, ObMatrix))

                PosTwo = Mathutils.MidpointVecs(apply_transform(me.edges[b].v1.co, ObMatrix), apply_transform(me.edges[b].v2.co, ObMatrix))

                ## Calculate the distance between the two midpoints
                CurDist = vertDist(PosOne, PosTwo)

                DATA['LOC1'] = PosOne
                DATA['LOC2'] = PosTwo
                DATA['DISTANCE'] = CurDist
                DATA['OBNAME2'] = str(a) + str(b)
                Succes = True					
      else:
        DATA['RESULT'] = "No two edges selected!"
        
    ## Get the closest or furthest faces.
    else:
    
      if len(me.edges) > 1:

        ## Loop through the faces of the object.
        for a in range(len(me.edges)):

          PosOne = Mathutils.MidpointVecs(apply_transform(me.edges[a].v1.co, ObMatrix), apply_transform(me.edges[a].v2.co, ObMatrix))

          ## Loop through the faces of the object.
          for b in range(len(me.edges)):

            PosTwo = Mathutils.MidpointVecs(apply_transform(me.edges[b].v1.co, ObMatrix), apply_transform(me.edges[b].v2.co, ObMatrix))

            ## Calculate the distance between the two midpoints
            CurDist = vertDist(PosOne, PosTwo)

            ## Getting the closest point
            if BUTTON['MEASURE'].val is 12:

              ## See whether it's the first measurement or if the points are closer.
              if a is 0 and b is 1 or DATA['DISTANCE'] > CurDist and a != b:

                DATA['LOC1'] = PosOne
                DATA['LOC2'] = PosTwo
                DATA['DISTANCE'] = CurDist
                DATA['OBNAME2'] = str(a) + str(b)
                Succes = True

            ## Getting the furthest point	
            else:

              ## See whether it's the first measurement or if the points are closer.
              if a is 0 and b is 1 or DATA['DISTANCE'] < CurDist and a != b:

                DATA['LOC1'] = PosOne
                DATA['LOC2'] = PosTwo
                DATA['DISTANCE'] = CurDist
                DATA['OBNAME2'] = str(a) + str(b)
                Succes = True
        
      else:
        DATA['RESULT'] = "Not enough edges for measurement!"

  else:
    DATA['RESULT'] = "No mesh object selected!"
  return Succes
    
####################################################
# GETTING THE TWO MESH VERTS
####################################################
  
def GetMeshVerts():

  Succes = False
  
  ## Check to make sure there's 2 mesh objects selected
  if Object.GetSelected()[0].getType() == 'Mesh':
  
    ## Get the selected object
    DATA['OBNAME1'] = Object.GetSelected()[0].getName()

    ## Get the name of the mesh of the selected object
    DATA['MNAME1'] = Object.GetSelected()[0].getData(1)

    ## Get the object matrix for applying
    tarObj = Object.Get(DATA['OBNAME1'])

    ObMatrix = Mathutils.Matrix(tarObj.getMatrix('worldspace'))
    
    me = NMesh.GetRaw(DATA['MNAME1'])

    ## Get the two selected faces.
    if BUTTON['MEASURE'].val is 14:
      
      ## Create a list of sel verts
      VertList = []
      for f in me.verts:
        if f.sel is 1:
          VertList.append(f)

      if len(VertList) is 2:

        for a in range(len(me.verts)):

          if me.verts[a] is VertList[0]:

            for b in range(len(me.verts)):

              if me.verts[b] is VertList[1]:
                PosOne = Mathutils.MidpointVecs(apply_transform(me.verts[a].co, ObMatrix), apply_transform(me.verts[a].co, ObMatrix))

                PosTwo = Mathutils.MidpointVecs(apply_transform(me.verts[b].co, ObMatrix), apply_transform(me.verts[b].co, ObMatrix))

                ## Calculate the distance between the two midpoints
                CurDist = vertDist(PosOne, PosTwo)

                DATA['LOC1'] = PosOne
                DATA['LOC2'] = PosTwo
                DATA['DISTANCE'] = CurDist
                DATA['OBNAME2'] = str(a) + str(b)
                Succes = True
                
      else:
        DATA['RESULT'] = "No two verts selected!"
      
    ## Get the closest or furthest faces.
    else:
    
      if len(me.verts) > 1:

        ## Loop through the faces of the object.
        for a in range(len(me.verts)):

          PosOne = Mathutils.MidpointVecs(apply_transform(me.verts[a].co, ObMatrix), apply_transform(me.verts[a].co, ObMatrix))

          ## Loop through the faces of the object.
          for b in range(len(me.verts)):

            PosTwo = Mathutils.MidpointVecs(apply_transform(me.verts[b].co, ObMatrix), apply_transform(me.verts[b].co, ObMatrix))

            ## Calculate the distance between the two midpoints
            CurDist = vertDist(PosOne, PosTwo)

            ## Getting the closest point
            if BUTTON['MEASURE'].val is 15:

              ## See whether it's the first measurement or if the points are closer.
              if a is 0 and b is 1 or DATA['DISTANCE'] > CurDist and a != b:

                DATA['LOC1'] = PosOne
                DATA['LOC2'] = PosTwo
                DATA['DISTANCE'] = CurDist
                DATA['OBNAME2'] = str(a) + str(b)
                Succes = True

            ## Getting the furthest point	
            else:

              ## See whether it's the first measurement or if the points are closer.
              if a is 0 and b is 1 or DATA['DISTANCE'] < CurDist and a != b:

                DATA['LOC1'] = PosOne
                DATA['LOC2'] = PosTwo
                DATA['DISTANCE'] = CurDist
                DATA['OBNAME2'] = str(a) + str(b)
                Succes = True
        
      else:
        DATA['RESULT'] = "Not enough verts for measurement!"

  else:
    DATA['MESSAGE'] = "No mesh object selected!"
  return Succes
  
####################################################
# THE SCRIPT
####################################################

def run():

  Window.WaitCursor(1)

  in_emode = int(Window.EditMode())
  if in_emode: Window.EditMode(0)

  CheckThis = False
  MType = "M" + str(BUTTON['MEASURE'].val)

  ## Get the scene
  scene = Blender.Scene.GetCurrent()
  scene.update()
  
  ## Get the distance between two closest faces!
  if BUTTON['MEASURE'].val is 1:
    CheckThis = GetObjectCenters()
    
  ## Get the distance between two closest faces!
  elif BUTTON['MEASURE'].val is 2 or BUTTON['MEASURE'].val is 3:
    CheckThis = GetObjectFaces()
    
  ## Get the distance between two closest faces!
  elif BUTTON['MEASURE'].val is 4 or BUTTON['MEASURE'].val is 5:
    CheckThis = GetObjectEdges()
    
  ## Get the distance between two closest faces!
  elif BUTTON['MEASURE'].val is 6 or BUTTON['MEASURE'].val is 7:
    CheckThis = GetObjectVerts()
    
  ## Get the distance between two closest faces!
  elif BUTTON['MEASURE'].val >= 8 and BUTTON['MEASURE'].val <= 10:
    CheckThis = GetMeshFaces()
    
  ## Get the distance between two closest faces!
  elif BUTTON['MEASURE'].val >= 11 and BUTTON['MEASURE'].val <= 13:
    CheckThis = GetMeshEdges()
    
  ## Get the distance between two closest faces!
  elif BUTTON['MEASURE'].val >= 14 and BUTTON['MEASURE'].val <= 16:
    CheckThis = GetMeshVerts()
    
  if CheckThis:
    
    ## Constrain the measurement result.
    if BUTTON['MCONSTRAIN'].val > 1 and BUTTON['MCONOBS'].val is 1:
      if BUTTON['MCONSTRAIN'].val is 2:
        DATA['LOC2'] = [DATA['LOC1'][0], DATA['LOC1'][1], DATA['LOC2'][2]]
      elif BUTTON['MCONSTRAIN'].val is 3:
        DATA['LOC2'] = [DATA['LOC1'][0], DATA['LOC2'][1], DATA['LOC1'][2]]
      elif BUTTON['MCONSTRAIN'].val is 4:
        DATA['LOC2'] = [DATA['LOC2'][0], DATA['LOC1'][1], DATA['LOC1'][2]]
        
      DATA['DISTANCE'] = vertDist(DATA['LOC1'], DATA['LOC2'])
      
    ## Get the location of the midpoint between measured points.	
    midLoc = Mathutils.MidpointVecs(Mathutils.Vector(DATA['LOC1']), Mathutils.Vector(DATA['LOC2']))
        
    ## Create a sting for naming the measurement objects
    ObNameString = DATA['OBNAME1'].replace('.', '') + DATA['OBNAME2'].replace('.', '') + MType
    
    ## Remove all previous objects with the name sting.
    if BUTTON['MAKECLEAN'].val is 1:
      RemoveOldObs(DATA['OBNAME1'].replace('.', ''), DATA['OBNAME2'].replace('.', ''), MType)
    
    ## Get the layers used for render
    SetLayer = []
    for a in range(20):
      if int(str(BUTTON['LAYERS'][a])) is 1:
        SetLayer.append(a)
        
    ## Get the matrix of the object to get the correct vert positions.
    ObMatrix = Mathutils.Matrix(Mathutils.TranslationMatrix(midLoc))
    ObMatrix.invert()

    ## Transform the vert positions to get the correct pos relative to the object centre.
    LocalLoc1 = apply_transform(DATA['LOC1'], ObMatrix)
    LocalLoc2 = apply_transform(DATA['LOC2'], ObMatrix)
    
    if DATA['DISTANCE'] > 0:
      ## Get the euler for the object rotation.
      NewEuler = GetEuler(LocalLoc1, LocalLoc2, DATA['DISTANCE'])
    else:
      NewEuler = [0.0,0.0,0.0]
        
    if BUTTON['MAKEARROW'].val is 1 or BUTTON['MAKETEXT'].val is 1:
    
      ## Attempt to get the material.
      try:
        NewMaterial = Material.Get("Measurement")
      ## If it doesn't exist, create it.
      except:
        ## New material
        NewMaterial = Material.New('Measurement')
        if BUTTON['OBCOL'].val is 1:
          NewMaterial.rgbCol = [0.0, 0.0, 0.0]
        elif BUTTON['OBCOL'].val is 2:
          NewMaterial.rgbCol = [1.0, 1.0, 1.0]
        elif BUTTON['OBCOL'].val is 3:
          NewMaterial.rgbCol = [1.0, 0.0, 0.0]
        elif BUTTON['OBCOL'].val is 4:
          NewMaterial.rgbCol = [1.0, 0.5, 0.0]
        elif BUTTON['OBCOL'].val is 5:
          NewMaterial.rgbCol = [1.0, 1.0, 0.0]
        elif BUTTON['OBCOL'].val is 6:
          NewMaterial.rgbCol = [0.0, 1.0, 0.0]
        elif BUTTON['OBCOL'].val is 7:
          NewMaterial.rgbCol = [0.0, 1.0, 1.0]
        elif BUTTON['OBCOL'].val is 8:
          NewMaterial.rgbCol = [0.0, 0.0, 1.0]
        elif BUTTON['OBCOL'].val is 8:
          NewMaterial.rgbCol = [1.0, 0.0, 1.0]
        NewMaterial.mode |= Material.Modes.SHADELESS
        NewMaterial.mode &= ~Material.Modes.TRACEABLE
        NewMaterial.mode &= ~Material.Modes.SHADOW
        NewMaterial.mode &= ~Material.Modes.SHADOWBUF
        
    ## Make the arrow if required.
    if BUTTON['MAKEARROW'].val is 1:
      
      ## Make a new mesh
      NewObject = Object.New('Mesh')
      NewObject.setName(ObNameString)
      NewObject.setLocation(midLoc[0], midLoc[1], midLoc[2])
      scene.link(NewObject)
      NewObject.layers = SetLayer
    
      NewObject.setEuler((NewEuler[0], NewEuler[1], NewEuler[2]))
  
      mez = NewObject.getData()
      
      mez.setMaterials([NewMaterial])
    
      ## Add the verts and faces.
      SkinObject(mez, Vlist[BUTTON['ARROW'].val], Flist[BUTTON['ARROW'].val], DATA['DISTANCE'])

      ## Make the faces of the arrow smooth.			.
      for a in mez.faces:
        a.smooth = 1
      
      ## Switch autosmooth on for the mesh.
      mez.mode |= NMesh.Modes.AUTOSMOOTH
    
      mez.update()
        
    ## Get the appropriate measurement.		
    DATA['RESULT'] = GetMeasurement()
    
    ## Create the measurement object if wanted.
    if BUTTON['MAKETEXT'].val is 1:
    
      ## Create the text object for the new measurement data.
      txt = Text3d.New("Measurement")
      txt.setText(DATA['RESULT'])	
      txt.setYoffset(BUTTON['TEXTOFFS'].val)
      txt.setAlignment(Text3d.MIDDLE)
      txt.setExtrudeBevelDepth(BUTTON['TEXTBV'].val)
      txt.setExtrudeDepth(BUTTON['TEXTEX'].val)
      NewObject = Object.New('Text')
      NewObject.setName(ObNameString)
      NewObject.link(txt)
      NewObject.setLocation(midLoc[0], midLoc[1], midLoc[2])
      NewObject.setEuler((NewEuler[0], NewEuler[1], NewEuler[2]))
      NewObject.setSize(BUTTON['TEXTSIZE'].val, BUTTON['TEXTSIZE'].val, BUTTON['TEXTSIZE'].val)
      NewObject.makeDisplayList()
      NewObject.setMaterials([NewMaterial])
      NewObject.colbits = 0x01
      scene.link(NewObject)
      NewObject.layers = SetLayer

    ## Succesful measurement message.
    DATA['MESSAGE'] = "Measurement executed succesfully"
    
    ## Update the scene
    scene.update()
    ## Redraw all windows
    Window.RedrawAll()
          
  ## If there's no two mesh objects selected generate an error message.
  else:
    DATA['MESSAGE'] = "An error occured!"
  
  if in_emode: Window.EditMode(1)
  
  Window.WaitCursor(0)
  
####################################################
# DRAW THE GUI
####################################################

def gui():

  #############################################################
  # Backgrounds
  #############################################################

  BGL.glClearColor(0.5, 0.5, 0.5, 0.0)
  BGL.glClear(BGL.GL_COLOR_BUFFER_BIT)

  BGL.glColor3f(0, 0, 0)			# Black background
  BGL.glRectf(1, 1, 269, 456)

  BGL.glColor3f(0.7, 0.7, 0.8)		# Light background
  BGL.glRectf(2, 2, 268, 455)

  BGL.glColor3f(0.5, 0.5, 0.5)			# Grey
  BGL.glRectf(3, 3, 267, 454)

  BGL.glColor3f(0.45, 0.45, 0.45)			# Grey
  BGL.glRectf(10, 365, 259, 415)

  #############################################################
  # TEXT
  #############################################################	
  
  BGL.glColor3f(0.7, 0.7, 0.8)
  BGL.glRasterPos2d(20, 440)
  Draw.Text("Blender Caliper " + str(VERSION) + " (c)")
  
  DrawTitle("results and messages", 420)

  BGL.glColor3f(1.0, 1.0, 1.0)
  BGL.glRasterPos2d(20, 395)

  if DATA['MESSAGE'] != "a":
    Draw.Text(str(DATA['MESSAGE']))
    
    if DATA['RESULT'] != "a":
      BGL.glRasterPos2d(20, 375)
      Draw.Text(str(DATA['RESULT']))

  else:
    Draw.Text("Select your objects, and settings,")
    BGL.glRasterPos2d(20, 375)
    Draw.Text("and click on MEASURE.")
  
  #############################################################
  # BUTTONS
  #############################################################
  
  DrawTitle("object settings", 350)

  BUTTON['MAKETEXT'] = Draw.Toggle("Text", 2, 20, 325, 70, 20, BUTTON['MAKETEXT'].val, "Make a 3d text object to display the measurement result.")

  BUTTON['MAKEARROW'] = Draw.Toggle("Arrow", 2, 100, 325, 70, 20, BUTTON['MAKEARROW'].val, "Make a 3d arrow object to display the measurement result.")
  
  BUTTON['MAKECLEAN'] = Draw.Toggle("Clean", 2, 180, 325, 70, 20, BUTTON['MAKECLEAN'].val, "Try to remove the previous measurement objects between these two points (may not work if your object names are very long).")
  
  ## Layer selection buttons
  BUTTON['LAYERS'][1] = Draw.Toggle(" ", 2, 20, 310, 14, 10, int(str(BUTTON['LAYERS'][1])), "Create the objects on layer 1")
  BUTTON['LAYERS'][2] = Draw.Toggle(" ", 2, 34, 310, 14, 10, int(str(BUTTON['LAYERS'][2])), "Create the objects on layer 2")
  BUTTON['LAYERS'][3] = Draw.Toggle(" ", 2, 48, 310, 14, 10, int(str(BUTTON['LAYERS'][3])), "Create the objects on layer 3")
  BUTTON['LAYERS'][4] = Draw.Toggle(" ", 2, 62, 310, 14, 10, int(str(BUTTON['LAYERS'][4])), "Create the objects on layer 4")
  BUTTON['LAYERS'][5] = Draw.Toggle(" ", 2, 76, 310, 14, 10, int(str(BUTTON['LAYERS'][5])), "Create the objects on layer 5")
  
  BUTTON['LAYERS'][6] = Draw.Toggle(" ", 2, 100, 310, 14, 10, int(str(BUTTON['LAYERS'][6])), "Create the objects on layer 6")
  BUTTON['LAYERS'][7] = Draw.Toggle(" ", 2, 114, 310, 14, 10, int(str(BUTTON['LAYERS'][7])), "Create the objects on layer 7")
  BUTTON['LAYERS'][8] = Draw.Toggle(" ", 2, 128, 310, 14, 10, int(str(BUTTON['LAYERS'][8])), "Create the objects on layer 8")
  BUTTON['LAYERS'][9] = Draw.Toggle(" ", 2, 142, 310, 14, 10, int(str(BUTTON['LAYERS'][9])), "Create the objects on layer 9")
  BUTTON['LAYERS'][10] = Draw.Toggle(" ", 2, 156, 310, 14, 10,int(str(BUTTON['LAYERS'][10])), "Create the objects on layer 10")
  
  BUTTON['LAYERS'][11] = Draw.Toggle(" ", 2, 20, 300, 14, 10, int(str(BUTTON['LAYERS'][11])), "Create the objects on layer 11")
  BUTTON['LAYERS'][12] = Draw.Toggle(" ", 2, 34, 300, 14, 10, int(str(BUTTON['LAYERS'][12])), "Create the objects on layer 12")
  BUTTON['LAYERS'][13] = Draw.Toggle(" ", 2, 48, 300, 14, 10, int(str(BUTTON['LAYERS'][13])), "Create the objects on layer 13")
  BUTTON['LAYERS'][14] = Draw.Toggle(" ", 2, 62, 300, 14, 10, int(str(BUTTON['LAYERS'][14])), "Create the objects on layer 14")
  BUTTON['LAYERS'][15] = Draw.Toggle(" ", 2, 76, 300, 14, 10, int(str(BUTTON['LAYERS'][15])), "Create the objects on layer 15")
  
  BUTTON['LAYERS'][16] = Draw.Toggle(" ", 2, 100, 300, 14, 10, int(str(BUTTON['LAYERS'][16])), "Create the objects on layer 16")
  BUTTON['LAYERS'][17] = Draw.Toggle(" ", 2, 114, 300, 14, 10, int(str(BUTTON['LAYERS'][17])), "Create the objects on layer 17")
  BUTTON['LAYERS'][18] = Draw.Toggle(" ", 2, 128, 300, 14, 10, int(str(BUTTON['LAYERS'][18])), "Create the objects on layer 18")
  BUTTON['LAYERS'][19] = Draw.Toggle(" ", 2, 142, 300, 14, 10, int(str(BUTTON['LAYERS'][19])), "Create the objects on layer 19")
  BUTTON['LAYERS'][20] = Draw.Toggle(" ", 2, 156, 300, 14, 10, int(str(BUTTON['LAYERS'][20])), "Create the objects on layer 20")
  
  ## Measurement material color selector
  types = "Object color %t|Black %x1|White %x2|Red %x3|Orange %x4|Yellow %x5|Green %x6|Cyan %x7|Blue %x8|Magenta %x9"
  
  BUTTON['OBCOL'] = Draw.Menu(types, 2, 180, 300, 70, 20, BUTTON['OBCOL'].val, "The initial color of the measurement material.")
  
  ## Arrow settings.
  DrawTitle("arrow style", 285)
  
  ## Measurement type drowdown menu
  types = "Arrow type %t|Flat line %x1|Flat arrow %x2|Square line %x3|Round line %x4|Square arrow %x5|Square arrow bevelled %x6|Round arrow %x7|Round arrow bevelled %x8|Cross %x9|Cross bevelled %x10|Double edge %x11|Pointy quad %x12"
  
  BUTTON['ARROW'] = Draw.Menu(types, 2, 20, 260, 70, 20, BUTTON['ARROW'].val, "The style of arrow to create.")

  ## The alignment of both the arrow and the text objects.
  types = "Arrow alignment %t|Bottom %x1|Rear %x2|Top %x3|Front %x4"
  BUTTON['ARROWROT'] = Draw.Menu(types, 2, 100, 260, 70, 20, BUTTON['ARROWROT'].val, "The alignment of both the arrow and the text.")

  ## The relative scale of the measurement
  BUTTON['ARROWSIZE'] = Draw.Number("scale: ", 2, 180, 260, 70, 20, BUTTON['ARROWSIZE'].val, 0.01, 100.0, "The size of your arrow (length is defined by the measurement).")
  
  ## Text settings.
  DrawTitle("text style", 245)
  
  ## Beveling
  BUTTON['TEXTBV'] = Draw.Number("Bevel: ", 2, 20, 220, 110, 20, BUTTON['TEXTBV'].val, 0.000, 1.0, "The bevel depth of the 3d text.")	

  ## Extrusion
  BUTTON['TEXTEX'] = Draw.Number("Ext: ", 2, 140, 220, 110, 20, BUTTON['TEXTEX'].val, 0.00, 10.0, "The depth of the 3d text.")
  
  ## Clipend setting
  BUTTON['TEXTSIZE'] = Draw.Number("Size: ", 2, 20, 195, 110, 20, BUTTON['TEXTSIZE'].val, 0.01, 100.0, "The size of the measurement text.")
  
  ## Clipend setting
  BUTTON['TEXTOFFS'] = Draw.Number("Offset: ", 2, 140, 195, 110, 20, BUTTON['TEXTOFFS'].val, 0.00, 100.0, "The distance of the text above the line.")
  
  ## Measurement settings
  DrawTitle("measurement settings", 180)
  
  ## Measurement type drowdown menu
  types = "Measure the distance in %t|Two objects %x1|Two meshes %x2|One mesh %x3"
  
  BUTTON['MMODE'] = Draw.Menu(types, 2, 20, 155, 110, 20, BUTTON['MMODE'].val, "What object type(s) to measure the distance between or in.")

  if BUTTON['MMODE'].val is 1:
    BUTTON['MEASURE'].val = 1
    types = "Measure the distance between %t|The centers %x1"
    
  elif BUTTON['MMODE'].val is 2:
    if BUTTON['MEASURE'].val < 2 or BUTTON['MEASURE'].val > 7:
      BUTTON['MEASURE'].val = 2
    types = "Measure the distance between %t|Closest faces %x2|Furthest faces %x3|Closest edges %x4|Furthest edges %x5|Closest verts %x6|Furthest verts %x7"
    
  elif BUTTON['MMODE'].val is 3:
    if BUTTON['MEASURE'].val < 8:
      BUTTON['MEASURE'].val = 8
      
    types = "Measure the distance between %t|Selected faces %x8|Closest faces %x9|Furthest faces %x10|Selected edges %x11|Closest edges %x12|Furthest edges %x13|Selected verts %x14|Closest verts %x15|Furthest verts %x16"
  
  BUTTON['MEASURE'] = Draw.Menu(types, 2, 140, 155, 110, 20, BUTTON['MEASURE'].val, "What two points to measure between.")
  
  ## Contraining the measurement
  types = "Constrain the measurement %t|Not constrained %x1|Z axis %x2|Y axis %x3|X axis %x4"
  BUTTON['MCONSTRAIN'] = Draw.Menu(types, 2, 20, 130, 110, 20, BUTTON['MCONSTRAIN'].val, "Constrain the measurement along an axis.")
  
  ## Constrain the objects along the measurement axis
  if BUTTON['MCONSTRAIN'].val > 1:
    BUTTON['MCONOBS'] = Draw.Toggle("Constrain obs", 2, 140, 130, 110, 20, BUTTON['MCONOBS'].val, "Constrain the measurement objects.")
  
  ## Measurement output
  DrawTitle("output style", 115)

  ## Measurement type drowdown menu
  types = "Measurement output type %t|Nanometers %x1|MicroCentimeters %x2|Micrometers %x3|Millimeters %x4|MicroInches %x5|MicroFeet %x6|MicroYards %x7|MicroMiles %x8|Blender Units %x9"
  
  BUTTON['MOUT'] = Draw.Menu(types, 2, 20, 90, 110, 20, BUTTON['MOUT'].val, "The base scale for measurement output.")

  GoMicroInches = 0
  
  if BUTTON['MOUT'].val != 9:
  
    if BUTTON['MOUT'].val < 5:
      One = "nm"
      Two = "mucm"
      Three = "mum"
      Four = "mm"
    else:
      One = "muinch"
      Two = "mufeet"
      Three = "muyards"
      Four = "mumiles"
      if BUTTON['MDETAIL'].val is 1:
        GoMicroInches = 1

    ## Make sure the levels of detail match the scales we're working in.
    if BUTTON['MOUT'].val is 1 or BUTTON['MOUT'].val is 5:

      BUTTON['MDETAIL'].val = 1
      GoMicroInches = 1

    elif BUTTON['MOUT'].val is 2 or BUTTON['MOUT'].val is 6:

      if BUTTON['MDETAIL'].val > 2:
        BUTTON['MDETAIL'].val = 2
      types = "Measurement levels %t|" + One + " %x1|" + Two + " %x2"

    elif BUTTON['MOUT'].val is 3 or BUTTON['MOUT'].val is 7:

      if BUTTON['MDETAIL'].val > 3:
        BUTTON['MDETAIL'].val = 3
      types = "Measurement levels %t|" + One + " %x1|" + Two + " %x2|" + Three + "%x3"

    elif BUTTON['MOUT'].val is 4 or BUTTON['MOUT'].val is 8:
      types = "Measurement levels %t|" + One + " %x1|" + Two + " %x2|" + Three + "%x3|" + Four + "%x4"

    if BUTTON['MOUT'].val != 1 and BUTTON['MOUT'].val != 5:
    
      BUTTON['MDETAIL'] = Draw.Menu(types, 2, 140, 90, 50, 20, BUTTON['MDETAIL'].val, "The smallest increment to display a measurement in.")
    
  if BUTTON['MOUT'].val > 4 and GoMicroInches is 1:
    types = "Measurement detail %t|1 %x1|1 1/2 %x2|1 1/4 %x3|1 1/8 %x4|1 1/16 %x5|1 1/32 %x6"
  else:
    types = "Measurement detail %t|1 %x1|0.1 %x2|0.01 %x3|0.001 %x4|0.0001 %x5|0.00001 %x6"

  BUTTON['MDECIMAL'] = Draw.Menu(types, 2, 200, 90, 50, 20, BUTTON['MDECIMAL'].val, "The smallest measurement in your smallest increment.")

  ## Measurement input.
  DrawTitle("input style", 75)
  
  if BUTTON['MOUT'].val != 9:
    ## Measurement type drowdown menu
    types = "Measurement input type %t|Nanometers %x1|MicroCentimeters %x2|Micrometers %x3|Millimeters %x4|MicroInches %x5|MicroFeet %x6|MicroYards %x7|MicroMiles %x8"
  
    BUTTON['MIN'] = Draw.Menu(types, 2, 20, 50, 110, 20, BUTTON['MIN'].val, "The base scale for one blender unit.")


  ## The relative scale of the measurement
  BUTTON['MSCALE'] = Draw.Number("scale: ", 2, 140, 50, 110, 20, BUTTON['MSCALE'].val, 0.001, 100.0, "The size of 1 blender unit in your base scale.")
  
  ## mayor functions
  DrawTitle("mayor functions", 35)
  
  ## Reset gui button
  Draw.Button("MEASURE", 1, 20, 10, 110, 20, "Run the script!")
  
  ## Exit button
  Draw.Button("EXIT", 5, 140, 10, 110, 20, "Exit the script!")

####################################################
# CHECK FOR THE ESCAPE KEY
####################################################

## Close down the script in case the esc key was hit.
def event(evt, val):
  if (evt == Draw.ESCKEY and not val): Draw.Exit()

####################################################
# ACTION AFTER THE BUTTON HAS BEEN PRESSED
####################################################

## Global BUTTON
def bevent(evt):
  ## Run the script
  if (evt is  1):
    run()
    Draw.Redraw()
    
  ## Redraw interface
  if (evt is  2):
    Draw.Redraw()

  ## Exit the script
  if (evt is  5):
    Draw.Exit()
    
####################################################
# REGISTER THE FUNCTIONS
####################################################

Draw.Register(gui, event, bevent)

####################################################
# THE ARROW OBJECTS
####################################################

Vlist = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
Flist = [[],[],[],[],[],[],[],[],[],[],[],[],[]]

## List for 12
Vlist[12] = [0.0, 0.0, 0.0],[0.1, 0.02121, -0.02121],[0.1, -0.02121, 0.02121],[0.1, 0.02121, 0.02121],[0.1, -0.02121, -0.02121],[0.15, 0.0, 0.1],[0.15, -0.1, 0.0],[0.16, 0.1, 0.0],[0.16, 0.0, -0.1],[-0.16, 0.0, -0.1],[-0.16, 0.1, 0.0],[-0.15, 0.0, 0.1],[-0.15, -0.1, 0.0],[-0.1, 0.02121, -0.02121],[-0.1, -0.02121, -0.02121],[-0.1, 0.02121, 0.02121],[-0.1, -0.02121, 0.02121],[0.0, 0.0, 0.0]

Flist[12] = [0, 3, 7],[0, 5, 3],[0, 7, 1],[0, 1, 8],[0, 2, 5],[0, 6, 2],[0, 4, 6],[0, 8, 4],[7, 3, 1],[8, 1, 4],[6, 4, 2],[5, 2, 3],[11, 15, 16],[12, 16, 14],[9, 14, 13],[10, 13, 15],[17, 14, 9],[17, 12, 14],[17, 16, 12],[17, 11, 16],[17, 9, 13],[17, 13, 10],[17, 15, 11],[17, 10, 15],[3, 15, 13, 1],[3, 2, 16, 15],[4, 14, 16, 2],[1, 13, 14, 4]

## List for 11
Vlist[11] = [0.00194, 0.01, 0.0],[0.00194, -0.01, 0.0],[0.02914, -0.03, 0.0],[0.02914, 0.03, 0.0],[0.05318, 0.04736, 0.0],[0.05318, -0.04736, 0.0],[0.0807, 0.0642, 0.0],[0.0807, -0.0642, 0.0],[0.11081, 0.08, 0.0],[0.11081, -0.08, 0.0],[0.14248, 0.09428, 0.0],[0.14248, -0.09428, 0.0],[0.17452, -0.1066, 0.0],[0.17452, 0.1066, 0.0],[0.18, -0.01, 0.0],[0.18, 0.01, 0.0],[0.18, -0.03, 0.0],[0.18, 0.03, 0.0],[0.18152, 0.04736, 0.0],[0.18152, -0.04736, 0.0],[0.18603, 0.0642, 0.0],[0.18603, -0.0642, 0.0],[0.1934, -0.08, 0.0],[0.1934, 0.08, 0.0],[0.2034, -0.09428, 0.0],[0.2034, 0.09428, 0.0],[0.20563, 0.1166, 0.0],[0.20563, -0.1166, 0.0],[0.21572, -0.1066, 0.0],[0.21572, 0.1066, 0.0],[0.23, 0.1166, 0.0],[0.23, -0.1166, 0.0],[0.23447, 0.12397, 0.0],[0.23447, -0.12397, 0.0],[0.2458, 0.12397, 0.0],[0.2458, -0.12397, 0.0],[0.25968, 0.12848, 0.0],[0.25968, -0.12848, 0.0],[0.26264, 0.12848, 0.0],[0.26264, -0.12848, 0.0],[0.27999, 0.13, 0.0],[0.27999, -0.13, 0.0],[-0.27999, -0.13, 0.0],[-0.27999, 0.13, 0.0],[-0.26264, -0.12848, 0.0],[-0.26264, 0.12848, 0.0],[-0.25968, 0.12848, 0.0],[-0.25968, -0.12848, 0.0],[-0.2458, -0.12397, 0.0],[-0.2458, 0.12397, 0.0],[-0.23447, 0.12397, 0.0],[-0.23447, -0.12397, 0.0],[-0.23, 0.1166, 0.0],[-0.23, -0.1166, 0.0],[-0.21572, -0.1066, 0.0],[-0.21572, 0.1066, 0.0],[-0.20563, 0.1166, 0.0],[-0.20563, -0.1166, 0.0],[-0.2034, -0.09428, 0.0],[-0.2034, 0.09428, 0.0],[-0.1934, 0.08, 0.0],[-0.1934, -0.08, 0.0],[-0.18603, -0.0642, 0.0],[-0.18603, 0.0642, 0.0],[-0.18152, -0.04736, 0.0],[-0.18152, 0.04736, 0.0],[-0.18, -0.03, 0.0],[-0.18, -0.01, 0.0],[-0.18, 0.01, 0.0],[-0.18, 0.03, 0.0],[-0.17452, -0.1066, 0.0],[-0.17452, 0.1066, 0.0],[-0.14248, 0.09428, 0.0],[-0.14248, -0.09428, 0.0],[-0.11081, 0.08, 0.0],[-0.11081, -0.08, 0.0],[-0.0807, 0.0642, 0.0],[-0.0807, -0.0642, 0.0],[-0.05318, 0.04736, 0.0],[-0.05318, -0.04736, 0.0],[-0.02914, -0.03, 0.0],[-0.02914, 0.03, 0.0],[-0.00194, -0.01, 0.0],[-0.00194, 0.01, 0.0]

Flist[11] = [38, 40, 36],[34, 38, 36, 32],[30, 34, 32, 26],[29, 30, 26, 13],[25, 29, 13, 10],[23, 25, 10, 8],[20, 23, 8, 6],[18, 20, 6, 4],[17, 18, 4, 3],[0, 15, 17, 3],[69, 68, 83, 81],[69, 81, 78, 65],[65, 78, 76, 63],[63, 76, 74, 60],[60, 74, 72, 59],[59, 72, 71, 55],[55, 71, 56, 52],[52, 56, 50, 49],[49, 50, 46, 45],[45, 46, 43],[44, 47, 42],[48, 51, 47, 44],[53, 57, 51, 48],[54, 70, 57, 53],[58, 73, 70, 54],[61, 75, 73, 58],[62, 77, 75, 61],[64, 79, 77, 62],[66, 80, 79, 64],[66, 67, 82, 80],[16, 2, 1, 14],[16, 19, 5, 2],[19, 21, 7, 5],[21, 22, 9, 7],[22, 24, 11, 9],[24, 28, 12, 11],[28, 31, 27, 12],[31, 35, 33, 27],[35, 39, 37, 33],[39, 41, 37],[15, 68, 69, 17],[67, 66, 16, 14]

## List for 10
Vlist[10] = [0.0, -0.01576, -0.01576],[0.0, -0.01576, 0.01576],[0.0, 0.01576, 0.01576],[0.0, 0.01576, -0.01576],[0.0, -0.04424, 0.01576],[0.0, -0.13576, 0.01576],[0.0, -0.13576, -0.01576],[0.0, -0.01576, -0.13576],[0.0, 0.01576, 0.04424],[0.0, -0.01576, 0.04424],[0.0, -0.01576, 0.13576],[0.0, 0.01576, 0.13576],[0.0, 0.01576, -0.13576],[0.0, 0.01576, -0.04424],[0.0, -0.01576, -0.04424],[0.0, 0.13576, -0.01576],[0.0, 0.04424, -0.01576],[0.0, 0.04424, 0.01576],[0.0, 0.13576, 0.01576],[0.0, -0.04424, -0.01576],[0.01424, -0.01576, -0.15],[0.01424, 0.01576, -0.15],[0.01424, -0.03, -0.04424],[0.01424, -0.03, -0.13576],[0.01424, 0.03, -0.13576],[0.01424, 0.13576, -0.03],[0.01424, 0.04424, -0.03],[0.01424, 0.15, 0.01576],[0.01424, -0.04424, -0.03],[0.01424, -0.13576, -0.03],[0.01424, -0.15, 0.01576],[0.01424, -0.15, -0.01576],[0.01424, 0.15, -0.01576],[0.01424, 0.04424, 0.03],[0.01424, 0.13576, 0.03],[0.01424, 0.03, -0.04424],[0.01424, -0.04424, 0.03],[0.01424, -0.13576, 0.03],[0.01424, 0.03, 0.13576],[0.01424, 0.03, 0.04424],[0.01424, -0.03, 0.13576],[0.01424, -0.03, 0.04424],[0.01424, -0.01576, 0.15],[0.01424, 0.01576, 0.15],[0.03576, -0.03, 0.04424],[0.03576, -0.01576, 0.15],[0.03576, 0.01576, 0.15],[0.03576, -0.03, 0.13576],[0.03576, -0.04424, 0.03],[0.03576, -0.13576, 0.03],[0.03576, 0.03, 0.13576],[0.03576, 0.03, 0.04424],[0.03576, -0.15, -0.01576],[0.03576, 0.13576, 0.03],[0.03576, 0.04424, 0.03],[0.03576, -0.15, 0.01576],[0.03576, 0.15, -0.01576],[0.03576, -0.13576, -0.03],[0.03576, -0.04424, -0.03],[0.03576, 0.15, 0.01576],[0.03576, -0.03, -0.04424],[0.03576, -0.03, -0.13576],[0.03576, 0.13576, -0.03],[0.03576, 0.04424, -0.03],[0.03576, 0.01576, -0.15],[0.03576, 0.03, -0.13576],[0.03576, 0.03, -0.04424],[0.03576, -0.01576, -0.15],[0.05, -0.01576, -0.04424],[0.05, 0.13576, -0.01576],[0.05, 0.13576, 0.01576],[0.05, 0.01576, -0.04424],[0.05, 0.01576, -0.13576],[0.05, -0.01576, -0.13576],[0.05, 0.04424, 0.01576],[0.05, 0.04424, -0.01576],[0.05, -0.04424, 0.01576],[0.05, 0.01576, 0.13576],[0.05, -0.01576, 0.13576],[0.05, -0.04424, -0.01576],[0.05, -0.13576, -0.01576],[0.05, -0.01576, 0.04424],[0.05, 0.01576, 0.04424],[0.05, -0.13576, 0.01576],[0.06424, 0.01576, 0.03],[0.06424, 0.03, -0.01576],[0.06424, 0.03, 0.01576],[0.06424, -0.01576, -0.03],[0.06424, 0.01576, -0.03],[0.06424, -0.03, -0.01576],[0.06424, -0.03, 0.01576],[0.06424, -0.01576, 0.03],[-0.06424, 0.03, 0.01576],[-0.06424, 0.03, -0.01576],[-0.06424, -0.01576, -0.03],[-0.06424, 0.01576, -0.03],[-0.06424, -0.03, 0.01576],[-0.06424, -0.03, -0.01576],[-0.06424, -0.01576, 0.03],[-0.06424, 0.01576, 0.03],[-0.05, 0.13576, 0.01576],[-0.05, -0.01576, 0.04424],[-0.05, 0.01576, 0.04424],[-0.05, 0.04424, -0.01576],[-0.05, 0.04424, 0.01576],[-0.05, 0.01576, 0.13576],[-0.05, -0.01576, 0.13576],[-0.05, 0.01576, -0.13576],[-0.05, -0.04424, -0.01576],[-0.05, -0.04424, 0.01576],[-0.05, -0.01576, -0.13576],[-0.05, -0.01576, -0.04424],[-0.05, 0.01576, -0.04424],[-0.05, -0.13576, 0.01576],[-0.05, -0.13576, -0.01576],[-0.05, 0.13576, -0.01576],[-0.03576, 0.01576, -0.15],[-0.03576, -0.03, -0.13576],[-0.03576, -0.04424, -0.03],[-0.03576, -0.01576, -0.15],[-0.03576, -0.13576, -0.03],[-0.03576, -0.15, 0.01576],[-0.03576, 0.03, -0.13576],[-0.03576, 0.03, -0.04424],[-0.03576, -0.15, -0.01576],[-0.03576, 0.04424, -0.03],[-0.03576, 0.13576, -0.03],[-0.03576, -0.04424, 0.03],[-0.03576, 0.15, 0.01576],[-0.03576, -0.03, -0.04424],[-0.03576, -0.13576, 0.03],[-0.03576, 0.15, -0.01576],[-0.03576, -0.03, 0.04424],[-0.03576, -0.03, 0.13576],[-0.03576, 0.13576, 0.03],[-0.03576, 0.04424, 0.03],[-0.03576, 0.03, 0.13576],[-0.03576, -0.01576, 0.15],[-0.03576, 0.01576, 0.15],[-0.03576, 0.03, 0.04424],[-0.01424, -0.01576, 0.15],[-0.01424, 0.01576, 0.15],[-0.01424, 0.03, 0.04424],[-0.01424, 0.03, 0.13576],[-0.01424, -0.03, 0.04424],[-0.01424, -0.03, 0.13576],[-0.01424, 0.13576, 0.03],[-0.01424, 0.04424, 0.03],[-0.01424, -0.13576, 0.03],[-0.01424, -0.04424, 0.03],[-0.01424, -0.15, -0.01576],[-0.01424, -0.15, 0.01576],[-0.01424, 0.15, -0.01576],[-0.01424, 0.15, 0.01576],[-0.01424, 0.13576, -0.03],[-0.01424, 0.04424, -0.03],[-0.01424, -0.04424, -0.03],[-0.01424, -0.13576, -0.03],[-0.01424, -0.03, -0.13576],[-0.01424, -0.03, -0.04424],[-0.01424, 0.03, -0.13576],[-0.01424, 0.03, -0.04424],[-0.01424, -0.01576, -0.15],[-0.01424, 0.01576, -0.15],[0.0, -0.13576, -0.01576],[0.0, -0.13576, 0.01576],[0.0, -0.04424, 0.01576],[0.0, -0.04424, -0.01576],[0.0, 0.01576, -0.04424],[0.0, -0.01576, -0.04424],[0.0, -0.01576, -0.13576],[0.0, 0.01576, -0.13576],[0.0, -0.01576, 0.13576],[0.0, 0.01576, 0.13576],[0.0, 0.01576, 0.04424],[0.0, -0.01576, 0.04424],[0.0, 0.13576, -0.01576],[0.0, 0.13576, 0.01576],[0.0, 0.04424, 0.01576],[0.0, 0.04424, -0.01576],[0.0, -0.01576, -0.01576],[0.0, -0.01576, 0.01576],[0.0, 0.01576, 0.01576],[0.0, 0.01576, -0.01576]

Flist[10] = [0, 1, 2, 3],[82, 77, 78, 81],[8, 9, 10, 11],[75, 69, 70, 74],[16, 17, 18, 15],[68, 73, 72, 71],[14, 13, 12, 7],[76, 83, 80, 79],[6, 5, 4, 19],[51, 39, 38, 50],[46, 43, 42, 45],[44, 47, 40, 41],[48, 36, 37, 49],[52, 55, 30, 31],[29, 28, 58, 57],[60, 22, 23, 61],[64, 67, 20, 21],[66, 65, 24, 35],[63, 26, 25, 62],[59, 56, 32, 27],[54, 53, 34, 33],[0, 19, 4, 1],[2, 1, 9, 8],[2, 17, 16, 3],[0, 3, 13, 14],[82, 81, 91, 84],[81, 78, 47, 44],[78, 77, 46, 45],[82, 51, 50, 77],[9, 41, 40, 10],[10, 42, 43, 11],[8, 11, 38, 39],[75, 74, 86, 85],[74, 70, 53, 54],[70, 69, 56, 59],[75, 63, 62, 69],[17, 33, 34, 18],[15, 18, 27, 32],[15, 25, 26, 16],[68, 71, 88, 87],[71, 72, 65, 66],[73, 67, 64, 72],[73, 68, 60, 61],[12, 13, 35, 24],[12, 21, 20, 7],[14, 7, 23, 22],[76, 79, 89, 90],[80, 57, 58, 79],[80, 83, 55, 52],[83, 76, 48, 49],[6, 31, 30, 5],[4, 5, 37, 36],[6, 19, 28, 29],[38, 43, 46, 50],[39, 51, 54, 33],[42, 40, 47, 45],[41, 36, 48, 44],[37, 30, 55, 49],[52, 31, 29, 57],[58, 28, 22, 60],[23, 20, 67, 61],[64, 21, 24, 65],[66, 35, 26, 63],[62, 25, 32, 56],[59, 27, 34, 53],[78, 45, 47],[77, 50, 46],[10, 40, 42],[11, 43, 38],[70, 59, 53],[69, 62, 56],[18, 34, 27],[15, 32, 25],[72, 64, 65],[73, 61, 67],[12, 24, 21],[7, 20, 23],[80, 52, 57],[83, 49, 55],[6, 29, 31],[5, 30, 37],[3, 16, 13],[0, 14, 19],[1, 4, 9],[2, 8, 17],[39, 33, 17, 8],[9, 4, 36, 41],[14, 22, 28, 19],[16, 26, 35, 13],[75, 71, 66, 63],[85, 88, 71, 75],[81, 44, 48, 76],[81, 76, 90, 91],[82, 74, 54, 51],[82, 84, 86, 74],[68, 79, 58, 60],[68, 87, 89, 79],[112, 95, 93, 103],[112, 103, 125, 123],[101, 98, 96, 109],[101, 109, 127, 132],[102, 104, 92, 99],[102, 139, 135, 104],[97, 94, 111, 108],[108, 111, 129, 118],[167, 156, 159, 169],[168, 161, 155, 179],[174, 178, 147, 142],[144, 149, 166, 175],[181, 175, 166],[182, 178, 174],[183, 168, 179],[180, 167, 169],[177, 153, 146],[176, 154, 152],[100, 134, 128],[115, 131, 126],[171, 163, 160],[170, 158, 162],[107, 122, 116],[110, 119, 117],[164, 150, 157],[165, 148, 151],[114, 120, 124],[113, 121, 130],[172, 140, 145],[173, 143, 141],[106, 133, 137],[105, 138, 136],[121, 151, 148, 130],[120, 157, 150, 124],[129, 159, 156, 118],[119, 162, 158, 117],[160, 163, 116, 122],[125, 155, 161, 123],[131, 152, 154, 126],[146, 153, 128, 134],[142, 147, 135, 139],[141, 143, 136, 138],[144, 132, 127, 149],[145, 140, 137, 133],[176, 179, 155, 154],[178, 177, 146, 147],[176, 152, 153, 177],[100, 104, 135, 134],[115, 100, 128, 131],[115, 126, 125, 103],[104, 103, 93, 92],[168, 171, 160, 161],[170, 162, 163, 171],[170, 169, 159, 158],[107, 112, 123, 122],[107, 116, 119, 110],[111, 110, 117, 129],[112, 111, 94, 95],[164, 157, 156, 167],[164, 165, 151, 150],[166, 149, 148, 165],[108, 118, 120, 114],[113, 114, 124, 121],[109, 113, 130, 127],[108, 109, 96, 97],[175, 172, 145, 144],[173, 141, 140, 172],[174, 142, 143, 173],[101, 132, 133, 106],[105, 106, 137, 138],[102, 105, 136, 139],[101, 102, 99, 98],[183, 180, 169, 168],[181, 166, 167, 180],[181, 182, 174, 175],[183, 179, 178, 182],[127, 130, 148, 149],[121, 124, 150, 151],[118, 156, 157, 120],[129, 117, 158, 159],[119, 116, 163, 162],[123, 161, 160, 122],[154, 155, 125, 126],[131, 128, 153, 152],[135, 147, 146, 134],[139, 136, 143, 142],[137, 140, 141, 138],[132, 144, 145, 133],[176, 177, 178, 179],[104, 100, 115, 103],[168, 169, 170, 171],[112, 107, 110, 111],[167, 166, 165, 164],[108, 114, 113, 109],[175, 174, 173, 172],[101, 106, 105, 102],[183, 182, 181, 180],[91, 98, 99, 84],[84, 99, 92, 86],[85, 86, 92, 93],[85, 93, 95, 88],[87, 88, 95, 94],[87, 94, 97, 89],[89, 97, 96, 90],[91, 90, 96, 98]

## List for 9
Vlist[9] = [0.0, -0.15, -0.03],[0.0, -0.03, -0.15],[0.0, 0.03, -0.15],[0.0, 0.15, 0.03],[0.0, 0.03, 0.03],[0.0, -0.03, 0.03],[0.0, 0.03, -0.03],[0.0, -0.03, -0.03],[0.0, 0.15, -0.03],[0.0, 0.03, 0.15],[0.0, -0.03, 0.15],[0.0, -0.15, 0.03],[0.05, 0.15, 0.03],[0.05, 0.15, -0.03],[0.05, 0.03, 0.15],[0.05, 0.03, 0.03],[0.05, 0.03, -0.15],[0.05, -0.03, -0.15],[0.05, -0.03, 0.03],[0.05, 0.03, -0.03],[0.05, -0.15, -0.03],[0.05, -0.15, 0.03],[0.05, -0.03, 0.15],[0.05, -0.03, -0.03],[-0.05, 0.03, -0.03],[-0.05, -0.03, -0.03],[-0.05, 0.15, 0.03],[-0.05, 0.15, -0.03],[-0.05, 0.03, 0.03],[-0.05, -0.03, 0.03],[-0.05, 0.03, -0.15],[-0.05, -0.03, -0.15],[-0.05, -0.03, 0.15],[-0.05, 0.03, 0.15],[-0.05, -0.15, -0.03],[-0.05, -0.15, 0.03],[0.0, -0.03, 0.15],[0.0, 0.03, 0.15],[0.0, -0.15, -0.03],[0.0, -0.15, 0.03],[0.0, 0.03, -0.03],[0.0, -0.03, -0.03],[0.0, 0.03, 0.03],[0.0, -0.03, 0.03],[0.0, -0.03, -0.15],[0.0, 0.03, -0.15],[0.0, 0.15, 0.03],[0.0, 0.15, -0.03]

Flist[9] = [7, 5, 4, 6],[15, 18, 22, 14],[4, 5, 10, 9],[19, 15, 12, 13],[6, 4, 3, 8],[23, 19, 16, 17],[7, 6, 2, 1],[18, 23, 20, 21],[0, 11, 5, 7],[15, 14, 9, 4],[14, 22, 10, 9],[18, 5, 10, 22],[18, 21, 11, 5],[20, 0, 11, 21],[0, 20, 23, 7],[23, 17, 1, 7],[16, 2, 1, 17],[19, 6, 2, 16],[19, 13, 8, 6],[12, 3, 8, 13],[15, 4, 3, 12],[29, 43, 39, 35],[35, 39, 38, 34],[25, 34, 38, 41],[25, 41, 44, 31],[31, 44, 45, 30],[24, 30, 45, 40],[24, 40, 47, 27],[27, 47, 46, 26],[28, 26, 46, 42],[28, 42, 37, 33],[32, 33, 37, 36],[29, 32, 36, 43],[42, 40, 47, 46],[28, 24, 27, 26],[40, 41, 44, 45],[24, 25, 31, 30],[41, 43, 39, 38],[25, 29, 35, 34],[43, 42, 37, 36],[29, 28, 33, 32],[40, 42, 43, 41],[18, 15, 28, 29],[19, 24, 28, 15],[23, 25, 24, 19],[23, 18, 29, 25]

## List for 3
Vlist[3] = [0.0, 0.0, 0.0],[0.05, -0.03, -0.03],[0.05, 0.03, -0.03],[0.05, -0.03, 0.03],[0.05, 0.03, 0.03],[-0.05, -0.03, 0.03],[-0.05, 0.03, 0.03],[-0.05, -0.03, -0.03],[-0.05, 0.03, -0.03],[0.0, 0.0, 0.0]

Flist[3] = [1, 2, 8, 7],[6, 4, 3, 5],[7, 5, 3, 1],[2, 4, 6, 8],[2, 0, 4],[3, 0, 1],[4, 0, 3],[1, 0, 2],[8, 6, 9],[5, 7, 9],[6, 5, 9],[7, 8, 9]

## List for 4
Vlist[4] = [0.0, 0.0, 0.0],[0.05, 0.01916, -0.02284],[0.05, 0.0102, -0.02801],[0.05, 0.0, -0.02981],[0.05, -0.0102, -0.02801],[0.05, -0.01916, -0.02284],[0.05, -0.02582, -0.01491],[0.05, -0.02936, -0.00518],[0.05, -0.02936, 0.00518],[0.05, -0.02582, 0.01491],[0.05, -0.01916, 0.02284],[0.05, -0.0102, 0.02801],[0.05, 0.0, 0.02981],[0.05, 0.0102, 0.02801],[0.05, 0.01916, 0.02284],[0.05, 0.02582, 0.01491],[0.05, 0.02936, 0.00518],[0.05, 0.02936, -0.00518],[0.05, 0.02582, -0.01491],[-0.05, 0.02582, -0.01491],[-0.05, 0.01916, -0.02284],[-0.05, 0.0102, -0.02801],[-0.05, 0.0, -0.02981],[-0.05, -0.0102, -0.02801],[-0.05, -0.01916, -0.02284],[-0.05, -0.02582, -0.01491],[-0.05, -0.02936, -0.00518],[-0.05, -0.02936, 0.00518],[-0.05, -0.02582, 0.01491],[-0.05, -0.01916, 0.02284],[-0.05, -0.0102, 0.02801],[-0.05, 0.0, 0.02981],[-0.05, 0.0102, 0.02801],[-0.05, 0.01916, 0.02284],[-0.05, 0.02582, 0.01491],[-0.05, 0.02936, 0.00518],[-0.05, 0.02936, -0.00518],[0.0, 0.0, 0.0]

Flist[4] = [18, 0, 1],[1, 0, 2],[2, 0, 3],[3, 0, 4],[4, 0, 5],[5, 0, 6],[6, 0, 7],[7, 0, 8],[8, 0, 9],[9, 0, 10],[10, 0, 11],[11, 0, 12],[12, 0, 13],[13, 0, 14],[14, 0, 15],[15, 0, 16],[16, 0, 17],[18, 0, 17],[7, 0, 16],[18, 1, 20, 19],[1, 2, 21, 20],[2, 3, 22, 21],[3, 4, 23, 22],[4, 5, 24, 23],[5, 6, 25, 24],[6, 7, 26, 25],[7, 8, 27, 26],[8, 9, 28, 27],[9, 10, 29, 28],[10, 11, 30, 29],[11, 12, 31, 30],[12, 13, 32, 31],[13, 14, 33, 32],[14, 15, 34, 33],[15, 16, 35, 34],[16, 17, 36, 35],[18, 17, 36, 19],[7, 16, 35, 26],[19, 20, 37],[20, 21, 37],[21, 22, 37],[22, 23, 37],[23, 24, 37],[24, 25, 37],[25, 26, 37],[26, 27, 37],[27, 28, 37],[28, 29, 37],[29, 30, 37],[30, 31, 37],[31, 32, 37],[32, 33, 37],[33, 34, 37],[34, 35, 37],[35, 36, 37],[19, 36, 37],[26, 35, 37]

## List for 2
Vlist[2] = [0.0, 0.0, 0.0],[0.1, 0.1, 0.0],[0.1, -0.03, 0.0],[0.1, 0.03, 0.0],[0.1, -0.1, 0.0],[-0.1, 0.1, 0.0],[-0.1, -0.03, 0.0],[-0.1, -0.1, 0.0],[-0.1, 0.03, 0.0],[0.0, 0.0, 0.0]

Flist[2] = [8, 3, 2, 6],[8, 6, 9],[3, 0, 2],[8, 9, 5],[6, 7, 9],[2, 0, 4],[1, 0, 3]

## List for 1
Vlist[1] = [0.0, 0.0, 0.0],[0.05, 0.03, 0.0],[0.05, -0.03, 0.0],[-0.05, 0.03, 0.0],[-0.05, -0.03, 0.0],[0.0, 0.0, 0.0]

Flist[1] = [3, 1, 2, 4],[3, 4, 5],[1, 0, 2]

## List for 8
Vlist[8] = [0.0, 0.0, 0.0],[0.1, 0.11499, -0.09649],[0.1, 0.14106, -0.05134],[0.1, 0.15011, 0.0],[0.1, 0.14106, 0.05134],[0.1, 0.11499, 0.09649],[0.1, 0.07505, 0.13],[0.1, 0.02607, 0.14783],[0.1, -0.02607, 0.14783],[0.1, -0.07505, 0.13],[0.1, -0.11499, 0.09649],[0.1, -0.14106, 0.05134],[0.1, -0.15011, 0.0],[0.1, -0.14106, -0.05134],[0.1, -0.11499, -0.09649],[0.1, -0.07505, -0.13],[0.1, -0.02607, -0.14783],[0.1, 0.02607, -0.14783],[0.1, 0.07505, -0.13],[0.15, 0.14106, -0.05134],[0.15, 0.15011, 0.0],[0.15, 0.14106, 0.05134],[0.15, 0.11499, 0.09649],[0.15, 0.07505, 0.13],[0.15, 0.02607, 0.14783],[0.15, -0.02607, 0.14783],[0.15, -0.07505, 0.13],[0.15, -0.11499, 0.09649],[0.15, -0.14106, 0.05134],[0.15, -0.15011, 0.0],[0.15, -0.14106, -0.05134],[0.15, -0.11499, -0.09649],[0.15, -0.07505, -0.13],[0.15, -0.02607, -0.14783],[0.15, 0.02607, -0.14783],[0.15, 0.11499, -0.09649],[0.15, 0.07505, -0.13],[0.2, 0.00651, -0.03691],[0.2, -0.00651, -0.03691],[0.2, -0.01874, -0.03246],[0.2, -0.02871, 0.02409],[0.2, -0.01874, 0.03246],[0.2, -0.00651, 0.03691],[0.2, 0.00651, 0.03691],[0.2, 0.01874, 0.03246],[0.2, 0.02871, 0.02409],[0.2, -0.02871, -0.02409],[0.2, -0.03522, -0.01282],[0.2, -0.03748, 0.0],[0.2, -0.03522, 0.01282],[0.2, 0.03522, 0.01282],[0.2, 0.03748, 0.0],[0.2, 0.03522, -0.01282],[0.2, 0.02871, -0.02409],[0.2, 0.01874, -0.03246],[-0.2, -0.02871, 0.02409],[-0.2, 0.01874, -0.03246],[-0.2, 0.00651, -0.03691],[-0.2, -0.03522, 0.01282],[-0.2, -0.03748, 0.0],[-0.2, -0.03522, -0.01282],[-0.2, -0.02871, -0.02409],[-0.2, 0.02871, -0.02409],[-0.2, 0.03522, -0.01282],[-0.2, -0.01874, -0.03246],[-0.2, 0.03748, 0.0],[-0.2, 0.03522, 0.01282],[-0.2, 0.02871, 0.02409],[-0.2, 0.01874, 0.03246],[-0.2, 0.00651, 0.03691],[-0.2, -0.00651, 0.03691],[-0.2, -0.00651, -0.03691],[-0.2, -0.01874, 0.03246],[-0.15, -0.14106, -0.05134],[-0.15, -0.07505, -0.13],[-0.15, -0.02607, -0.14783],[-0.15, 0.02607, -0.14783],[-0.15, 0.07505, -0.13],[-0.15, 0.11499, -0.09649],[-0.15, 0.14106, -0.05134],[-0.15, 0.15011, 0.0],[-0.15, 0.11499, 0.09649],[-0.15, 0.07505, 0.13],[-0.15, 0.02607, 0.14783],[-0.15, -0.02607, 0.14783],[-0.15, -0.07505, 0.13],[-0.15, -0.11499, 0.09649],[-0.15, -0.14106, 0.05134],[-0.15, -0.15011, 0.0],[-0.15, -0.11499, -0.09649],[-0.15, 0.14106, 0.05134],[-0.1, 0.07505, 0.13],[-0.1, -0.11499, -0.09649],[-0.1, -0.14106, -0.05134],[-0.1, -0.15011, 0.0],[-0.1, -0.14106, 0.05134],[-0.1, -0.11499, 0.09649],[-0.1, -0.07505, 0.13],[-0.1, -0.02607, 0.14783],[-0.1, 0.02607, 0.14783],[-0.1, -0.02607, -0.14783],[-0.1, 0.11499, 0.09649],[-0.1, 0.14106, 0.05134],[-0.1, 0.15011, 0.0],[-0.1, 0.14106, -0.05134],[-0.1, 0.11499, -0.09649],[-0.1, 0.07505, -0.13],[-0.1, 0.02607, -0.14783],[-0.1, -0.07505, -0.13],[0.0, 0.0, 0.0]

Flist[8] = [36, 34, 37, 54],[34, 33, 38, 37],[33, 32, 39, 38],[32, 31, 46, 39],[31, 30, 47, 46],[30, 29, 48, 47],[29, 28, 49, 48],[28, 27, 40, 49],[27, 26, 41, 40],[26, 25, 42, 41],[25, 24, 43, 42],[24, 23, 44, 43],[23, 22, 45, 44],[22, 21, 50, 45],[21, 20, 51, 50],[20, 19, 52, 51],[19, 35, 53, 52],[35, 36, 54, 53],[54, 37, 57, 56],[38, 39, 64, 71],[39, 46, 61, 64],[47, 48, 59, 60],[40, 41, 72, 55],[41, 42, 70, 72],[42, 43, 69, 70],[45, 50, 66, 67],[50, 51, 65, 66],[51, 52, 63, 65],[52, 53, 62, 63],[53, 54, 56, 62],[60, 61, 46, 47],[58, 59, 48, 49],[55, 58, 49, 40],[68, 69, 43, 44],[67, 68, 44, 45],[71, 57, 37, 38],[89, 74, 64, 61],[73, 89, 61, 60],[88, 73, 60, 59],[87, 88, 59, 58],[86, 87, 58, 55],[85, 86, 55, 72],[84, 85, 72, 70],[83, 84, 70, 69],[82, 83, 69, 68],[81, 82, 68, 67],[90, 81, 67, 66],[80, 90, 66, 65],[79, 80, 65, 63],[78, 79, 63, 62],[77, 78, 62, 56],[76, 77, 56, 57],[75, 76, 57, 71],[74, 75, 71, 64],[75, 74, 108, 100],[76, 75, 100, 107],[77, 76, 107, 106],[78, 77, 106, 105],[79, 78, 105, 104],[80, 79, 104, 103],[90, 80, 103, 102],[81, 90, 102, 101],[82, 81, 101, 91],[83, 82, 91, 99],[84, 83, 99, 98],[85, 84, 98, 97],[86, 85, 97, 96],[87, 86, 96, 95],[88, 87, 95, 94],[73, 88, 94, 93],[89, 73, 93, 92],[74, 89, 92, 108],[108, 92, 109],[92, 93, 109],[93, 94, 109],[94, 95, 109],[95, 96, 109],[96, 97, 109],[97, 98, 109],[98, 99, 109],[99, 91, 109],[91, 101, 109],[101, 102, 109],[102, 103, 109],[103, 104, 109],[104, 105, 109],[105, 106, 109],[106, 107, 109],[107, 100, 109],[100, 108, 109],[36, 35, 1, 18],[35, 19, 2, 1],[19, 20, 3, 2],[20, 21, 4, 3],[21, 22, 5, 4],[22, 23, 6, 5],[23, 24, 7, 6],[24, 25, 8, 7],[25, 26, 9, 8],[26, 27, 10, 9],[27, 28, 11, 10],[28, 29, 12, 11],[29, 30, 13, 12],[30, 31, 14, 13],[31, 32, 15, 14],[32, 33, 16, 15],[33, 34, 17, 16],[34, 36, 18, 17],[18, 0, 17],[17, 0, 16],[16, 0, 15],[15, 0, 14],[14, 0, 13],[13, 0, 12],[12, 0, 11],[11, 0, 10],[10, 0, 9],[9, 0, 8],[8, 0, 7],[7, 0, 6],[6, 0, 5],[5, 0, 4],[4, 0, 3],[3, 0, 2],[2, 0, 1],[1, 0, 18]

## List for 7
Vlist[7] = [0.0, 0.0, 0.0],[0.15, 0.02607, -0.14783],[0.15, -0.02607, -0.14783],[0.15, -0.07505, -0.13],[0.15, -0.11499, -0.09649],[0.15, -0.14106, -0.05134],[0.15, -0.15011, 0.0],[0.15, -0.14106, 0.05134],[0.15, -0.11499, 0.09649],[0.15, -0.07505, 0.13],[0.15, -0.02607, 0.14783],[0.15, 0.02607, 0.14783],[0.15, 0.07505, 0.13],[0.15, 0.11499, 0.09649],[0.15, 0.14106, 0.05134],[0.15, 0.15011, 0.0],[0.15, 0.14106, -0.05134],[0.15, 0.11499, -0.09649],[0.15, 0.07505, -0.13],[0.15, 0.00651, -0.03691],[0.15, 0.01874, -0.03246],[0.15, -0.00651, -0.03691],[0.15, -0.01874, -0.03246],[0.15, -0.02871, 0.02409],[0.15, -0.01874, 0.03246],[0.15, -0.00651, 0.03691],[0.15, 0.00651, 0.03691],[0.15, 0.01874, 0.03246],[0.15, 0.02871, 0.02409],[0.15, 0.03522, 0.01282],[0.15, 0.03748, 0.0],[0.15, 0.03522, -0.01282],[0.15, 0.02871, -0.02409],[0.15, -0.03748, 0.0],[0.15, -0.03522, -0.01282],[0.15, -0.02871, -0.02409],[0.15, -0.03522, 0.01282],[-0.15, -0.02871, 0.02409],[-0.15, -0.01874, 0.03246],[-0.15, -0.00651, 0.03691],[-0.15, 0.00651, 0.03691],[-0.15, 0.01874, 0.03246],[-0.15, 0.02871, 0.02409],[-0.15, 0.03522, 0.01282],[-0.15, 0.03748, 0.0],[-0.15, 0.03522, -0.01282],[-0.15, 0.02871, -0.02409],[-0.15, -0.00651, -0.03691],[-0.15, 0.01874, -0.03246],[-0.15, 0.00651, -0.03691],[-0.15, -0.01874, -0.03246],[-0.15, -0.02871, -0.02409],[-0.15, -0.03522, -0.01282],[-0.15, -0.03748, 0.0],[-0.15, -0.03522, 0.01282],[-0.15, -0.02607, -0.14783],[-0.15, -0.11499, -0.09649],[-0.15, -0.14106, -0.05134],[-0.15, -0.15011, 0.0],[-0.15, -0.14106, 0.05134],[-0.15, -0.11499, 0.09649],[-0.15, -0.07505, 0.13],[-0.15, -0.02607, 0.14783],[-0.15, 0.02607, 0.14783],[-0.15, 0.07505, 0.13],[-0.15, 0.11499, 0.09649],[-0.15, 0.14106, 0.05134],[-0.15, 0.15011, 0.0],[-0.15, 0.14106, -0.05134],[-0.15, 0.11499, -0.09649],[-0.15, 0.07505, -0.13],[-0.15, 0.02607, -0.14783],[-0.15, -0.07505, -0.13],[0.0, 0.0, 0.0]

Flist[7] = [18, 0, 1],[1, 0, 2],[2, 0, 3],[3, 0, 4],[4, 0, 5],[5, 0, 6],[6, 0, 7],[7, 0, 8],[8, 0, 9],[9, 0, 10],[10, 0, 11],[11, 0, 12],[12, 0, 13],[13, 0, 14],[14, 0, 15],[15, 0, 16],[16, 0, 17],[17, 0, 18],[18, 1, 19, 20],[1, 2, 21, 19],[2, 3, 22, 21],[3, 4, 35, 22],[4, 5, 34, 35],[5, 6, 33, 34],[6, 7, 36, 33],[7, 8, 23, 36],[8, 9, 24, 23],[9, 10, 25, 24],[10, 11, 26, 25],[11, 12, 27, 26],[12, 13, 28, 27],[13, 14, 29, 28],[14, 15, 30, 29],[15, 16, 31, 30],[16, 17, 32, 31],[17, 18, 20, 32],[20, 19, 49, 48],[21, 22, 50, 47],[22, 35, 51, 50],[34, 33, 53, 52],[23, 24, 38, 37],[24, 25, 39, 38],[25, 26, 40, 39],[28, 29, 43, 42],[29, 30, 44, 43],[30, 31, 45, 44],[31, 32, 46, 45],[32, 20, 48, 46],[52, 51, 35, 34],[54, 53, 33, 36],[37, 54, 36, 23],[41, 40, 26, 27],[42, 41, 27, 28],[47, 49, 19, 21],[56, 72, 50, 51],[57, 56, 51, 52],[58, 57, 52, 53],[59, 58, 53, 54],[60, 59, 54, 37],[61, 60, 37, 38],[62, 61, 38, 39],[63, 62, 39, 40],[64, 63, 40, 41],[65, 64, 41, 42],[66, 65, 42, 43],[67, 66, 43, 44],[68, 67, 44, 45],[69, 68, 45, 46],[70, 69, 46, 48],[71, 70, 48, 49],[55, 71, 49, 47],[72, 55, 47, 50],[72, 56, 73],[56, 57, 73],[57, 58, 73],[58, 59, 73],[59, 60, 73],[60, 61, 73],[61, 62, 73],[62, 63, 73],[63, 64, 73],[64, 65, 73],[65, 66, 73],[66, 67, 73],[67, 68, 73],[68, 69, 73],[69, 70, 73],[70, 71, 73],[71, 55, 73],[55, 72, 73]

## List for 6
Vlist[6] = [0.0, 0.0, 0.0],[0.125, 0.13232, -0.1017],[0.125, -0.13232, -0.1017],[0.125, -0.13232, 0.1017],[0.125, -0.1017, 0.13232],[0.125, -0.1017, -0.13232],[0.125, 0.1017, -0.13232],[0.125, 0.1017, 0.13232],[0.125, 0.13232, 0.1017],[0.15, 0.05, 0.03232],[0.15, 0.125, 0.08964],[0.15, 0.125, -0.08964],[0.15, 0.05, -0.03232],[0.15, -0.03232, 0.05],[0.15, 0.03232, 0.05],[0.15, 0.08964, 0.125],[0.15, -0.08964, 0.125],[0.15, -0.05, -0.03232],[0.15, -0.05, 0.03232],[0.15, -0.125, 0.08964],[0.15, -0.125, -0.08964],[0.15, 0.03232, -0.05],[0.15, -0.03232, -0.05],[0.15, -0.08964, -0.125],[0.15, 0.08964, -0.125],[0.175, 0.025, -0.0375],[0.175, -0.025, -0.0375],[0.175, -0.025, 0.0375],[0.175, 0.0375, -0.025],[0.175, 0.0375, 0.025],[0.175, -0.0375, -0.025],[0.175, -0.0375, 0.025],[0.175, 0.025, 0.0375],[-0.175, 0.025, -0.0375],[-0.175, 0.0375, -0.025],[-0.175, 0.0375, 0.025],[-0.175, -0.025, 0.0375],[-0.175, -0.025, -0.0375],[-0.175, 0.025, 0.0375],[-0.175, -0.0375, -0.025],[-0.175, -0.0375, 0.025],[-0.15, 0.125, 0.08964],[-0.15, 0.08964, -0.125],[-0.15, 0.03232, -0.05],[-0.15, -0.03232, -0.05],[-0.15, -0.125, 0.08964],[-0.15, -0.125, -0.08964],[-0.15, -0.05, -0.03232],[-0.15, -0.05, 0.03232],[-0.15, 0.08964, 0.125],[-0.15, -0.08964, 0.125],[-0.15, -0.03232, 0.05],[-0.15, 0.03232, 0.05],[-0.15, 0.05, -0.03232],[-0.15, 0.05, 0.03232],[-0.15, -0.08964, -0.125],[-0.15, 0.125, -0.08964],[-0.125, 0.13232, -0.1017],[-0.125, 0.1017, -0.13232],[-0.125, -0.1017, -0.13232],[-0.125, 0.1017, 0.13232],[-0.125, -0.13232, -0.1017],[-0.125, -0.13232, 0.1017],[-0.125, -0.1017, 0.13232],[-0.125, 0.13232, 0.1017],[0.0, 0.0, 0.0]

Flist[6] = [38, 32, 27, 36],[35, 34, 28, 29],[31, 30, 39, 40],[25, 33, 37, 26],[13, 14, 15, 16],[17, 18, 19, 20],[21, 22, 23, 24],[9, 12, 11, 10],[7, 0, 4],[3, 0, 2],[5, 0, 6],[1, 0, 8],[57, 64, 65],[60, 63, 65],[62, 61, 65],[59, 58, 65],[53, 54, 41, 56],[52, 51, 50, 49],[48, 47, 46, 45],[44, 43, 42, 55],[32, 38, 35, 29],[27, 32, 14, 13],[27, 31, 40, 36],[52, 38, 36, 51],[34, 35, 54, 53],[28, 34, 33, 25],[28, 12, 9, 29],[30, 31, 18, 17],[39, 30, 26, 37],[40, 39, 47, 48],[37, 33, 43, 44],[25, 26, 22, 21],[15, 14, 9, 10],[16, 15, 7, 4],[16, 19, 18, 13],[20, 19, 3, 2],[20, 23, 22, 17],[24, 23, 5, 6],[24, 11, 12, 21],[10, 11, 1, 8],[8, 0, 7],[0, 3, 4],[2, 0, 5],[0, 1, 6],[57, 56, 41, 64],[65, 64, 60],[65, 58, 57],[63, 60, 49, 50],[63, 62, 65],[61, 62, 45, 46],[61, 59, 65],[58, 59, 55, 42],[54, 52, 49, 41],[53, 56, 42, 43],[50, 51, 48, 45],[46, 47, 44, 55],[38, 52, 54, 35],[32, 29, 9, 14],[27, 13, 18, 31],[36, 40, 48, 51],[34, 53, 43, 33],[28, 25, 21, 12],[30, 17, 22, 26],[39, 37, 44, 47],[15, 10, 8, 7],[16, 4, 3, 19],[20, 2, 5, 23],[24, 6, 1, 11],[57, 58, 42, 56],[64, 41, 49, 60],[63, 50, 45, 62],[61, 46, 55, 59]

## List for 5
Vlist[5] = [0.0, 0.0, 0.0],[0.15, -0.03, -0.03],[0.15, 0.03, -0.03],[0.15, 0.15, -0.15],[0.15, 0.03, 0.03],[0.15, -0.03, 0.03],[0.15, -0.15, 0.15],[0.15, 0.15, 0.15],[0.15, -0.15, -0.15],[-0.15, -0.03, 0.03],[-0.15, 0.03, 0.03],[-0.15, -0.03, -0.03],[-0.15, 0.15, 0.15],[-0.15, -0.15, 0.15],[-0.15, 0.15, -0.15],[-0.15, -0.15, -0.15],[-0.15, 0.03, -0.03],[0.0, 0.0, 0.0]

Flist[5] = [10, 4, 5, 9],[10, 16, 2, 4],[5, 1, 11, 9],[2, 16, 11, 1],[5, 4, 7, 6],[1, 5, 6, 8],[2, 1, 8, 3],[4, 2, 3, 7],[7, 0, 6],[6, 0, 8],[8, 0, 3],[3, 0, 7],[14, 12, 17],[12, 13, 17],[13, 15, 17],[15, 14, 17],[16, 10, 12, 14],[10, 9, 13, 12],[9, 11, 15, 13],[11, 16, 14, 15]

if __name__ == '__main__':
  pass
