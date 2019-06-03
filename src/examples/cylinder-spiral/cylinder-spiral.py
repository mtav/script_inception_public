#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utilities.common import matlab_range
from numpy import sqrt, cos, sin
from GWL.GWL_parser import GWLobject
from bfdtd.bfdtd_parser import *
from numpy import array, cos, sin, tan, degrees, radians, arccos, arcsin, arctan, floor, ceil, ones, zeros, pi, linspace, log10

def addCylinder(sim, obj, voxel_step, cylinder_radius, refractive_index_cylinder):
  L = len(obj.GWL_voxels[-1]) - 1
  if L >= voxel_step and (L-1)%(voxel_step-1) == 0:
    cyl = Cylinder()
    cyl.setRefractiveIndex(refractive_index_cylinder)
    cyl.setStartEndPoints(obj.GWL_voxels[-1][-voxel_step], obj.GWL_voxels[-1][-1])
    cyl.setOuterRadius(cylinder_radius)
    sim.appendGeometryObject(cyl)

obj = GWLobject()
sim = BFDTDobject()
sim.setDefaultRefractiveIndex(2)
sim.setSizeAndResolution([10,10,10],[100,100,100])

cylinder_radius = 0.1
refractive_index_cylinder = 3

voxel_step = 3

ellipse_factor_x = 1
ellipse_factor_y = 2

XOffset=0.7
YOffset=0.7
ZOffset=0.26

FI = 0.5  # FindInterfaceAt
p0 = 25.5 # laserpower at z=0
LN = 1        # linenumber for main structure
LD = 50		#line distance

#LineDistance $LD
#LineNumber $LN
#LaserPower $p0

twopi = 6.28318531

# Helix parameters
r= 0.52*0.5 #0.52/2 #0.25				    % radius of helices
pitch=0.6 * (2 * r) * 2.5 #0.15*6*1.5			% pitch of helices
pitches= 8			# number of pitches
#a=10				# center2center distance of helices
#footprint = 10       # footprint in µm

# Loop variables: rotation angle and point coordinates
phi=0
x = 0
y = 0
z = 0
xl = 0
yl = 0
zl = 0
xr = 0
yr = 0
zr = 0

# Position of a single helix 
offsetx = 0
offsety = 0
offsetz = 0
offx = 0
offy = 0
offz = 0

offx0 = 0
offy0 = 0
offz0 = 0

phigs=0
xgs= 0
ygs= 0
zgs = 0
rgs = 0

# Parameters
ntot= 3 #1965 % 27778 # 3*250            % total number of PC air holes; a golden-angle spiral that consists of N = 1000 circles
m = 1                  # golden ratio: m=1; the Fibonacci series m (1,2,3,5,8,13,21,34,55,89,144, . . . ).

# the dominant m values are 5,8,13,21,34,55,89, which are Fibonacci numbers and represent the number of parastichies in each family.
err=0                  # error on the angle

alpha=0                # -0.208 %  0.092

#alpha=deg2rad(alpha)     % golden angle (in rad) = 2*pi/(phi+1)


#%%% Spiral (Polar coordinates)
r0 = r #*(960/1050.36827)*(960/975.232439)*(960/965.367371);        % RADIUS 1 of PC air holes
c1 = 0 # air-fill fraction fraction
c = 0
n_start = 1   # n = 1,2, . . . is an integer
th = 0

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for n in matlab_range(n_start, 1, ntot):

  phigs = (1 + sqrt(5)) / (2 * m)  # The value of φ is approached by the ratio of two consecutive numbers in the Fibonacci
   # series m (1,2,3,5,8,13,21,34,55,89,144, . . . ); m= 1: 1.6180339... is the golden number
  alpha = 137.508 # 137.3 % 137.6 %  (360 / ($phigs*$phigs)) + $err %360 - (360 / $phigs) + $err % golden angle (in d¡); golden angle = 137.508 deg	;‘nearly golden spirals’ : 137.3 (i.e. alpha1-spiral) and 137.6 (i.e. alpha2-spiral or bata4-spiral)
  alpha = alpha*3.14159265359/180  # if function deg2rad not available...
  c1 = 1.5957446808510638297872340425532*1 #7*r0*1  # air-fill fraction fraction
  c=(c1*r0)                       # a constant scaling factor
  rgs=c*sqrt(n)		           # the radius or distance from the center
  th = n * alpha                # angle(golden angle:alpha= 137.508 deg)- the divergence angle, which is an irrational number
  xgs = rgs * cos(th) 		       # conversion polaire -> cartŽsien
  ygs = rgs * sin(th)
  #%	set $zgs = 2 * $rgs %* $th 	

  offx = xgs + offsetx
  offy = ygs + offsety
  offz = zgs + offsety


  # Outer loops: helix placement via $offx and $offy
  # Note: the "step $variable" part of for-loops is optional and if absent, the step size defaults to 1.0.
  #for $offx = $offsetx to $footprint step $a
  #for $offx = $offsetx to $footprint step $a

  #	for $offy = $offsety to $footprint step $a
  #	for $offy = $offsety to $footprint step $a

  offx0 = offx - 1 * ellipse_factor_x*r * cos(phi) # 1.75 * $xgs + $offsetx
  offy0 = offy - 1 * ellipse_factor_y*r * sin(phi) # 1.75 * $ygs + $offsety
  offz0 = offz  

  print((offx0, offy0, offz0))
  obj.addVoxel([offx0, offy0, offz0])
  addCylinder(sim, obj, voxel_step, cylinder_radius, refractive_index_cylinder)
  #	Write

  # Inner loop: helix generation
  
  pitches*24
  
  first_line = True
  
  for phi in matlab_range(0, twopi/24, pitches*twopi):

    #			LineDistance $LD
    #            LineNumber $LN

    # Mathematical expressions can contain the basic arithmetic operators +, -, *, /,
    # parenthesis to indicate precedence, and the special functions listed in the manual
    xl = offx + ellipse_factor_x*r * cos(phi)
    yl = offy + ellipse_factor_y*r * sin(phi)
    zl = (pitch / twopi) * phi

    # Emit computed coordinates
    # Note: coordinates can be literal numbers or variable identifiers only but not mathematical expressions.

    #print((xl, yl, zl))
    obj.addVoxel([xl, yl, zl])
    if first_line:
      cyl = Cylinder()
      cyl.setRefractiveIndex(refractive_index_cylinder)
      cyl.setStartEndPoints(obj.GWL_voxels[-1][-2], obj.GWL_voxels[-1][-1])
      cyl.setOuterRadius(cylinder_radius)
      sim.appendGeometryObject(cyl)
      first_line = False
    else:
      addCylinder(sim, obj, voxel_step, cylinder_radius, refractive_index_cylinder)
    
    # Terminate inner for-loop
    #end # phi

  # Terminate polyline
  print('Write')
  obj.startNewVoxelSequence()

  #%	set $offx0 = $offx + 1 * $r * cos($phi) % 1.75 * $xgs + $offsetx
  #%	set $offy0 = $offy + 1 * $r * sin($phi) % 1.75 * $ygs + $offsety
  #%	set $offz0 = $offz  
  #%	
  #%	$offx0 $offy0 $offz0
  #%	%	Write
  #%		for $phi = 0 to $pitches * $twopi step $twopi / 24
  #%			
  #%%			LineDistance $LD
  #%%            LineNumber $LN
  #%		
  #%			% Mathematical expressions can contain the basic arithmetic operators +, -, *, /,
  #%			% parenthesis to indicate precedence, and the special functions listed in the manual	
  #%			set $xr = $offx - $r * cos($phi)
  #%			set $yr = $offy - $r * sin($phi)
  #%			set $zr = ($pitch / $twopi) * $phi
  #%			
  #%			% Emit computed coordinates
  #%			% Note: coordinates can be literal numbers or variable identifiers only but not mathematical expressions.
  #%
  #%			$xr $yr $zr
  #%		% Terminate inner for-loop
  #%		end %phi
  #%
  #%		% Terminate polyline
  #%		Write

  #%	end %offy
  #%end %offx
  #% Done

obj.writeGWL('foo.gwl')
#sim.writeGeoFile('foo.geo')
#sim.writeInpFile('foo.inp')
sim.writeTorqueJobDirectory('.')
print(obj.getLimits())
