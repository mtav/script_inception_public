#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Examples of plots and calculations using the tmm package.
"""

from __future__ import division, print_function, absolute_import

from tmm import (coh_tmm, unpolarized_RT, ellips,
                       position_resolved, find_in_structure_with_inf)

from numpy import pi, linspace, inf, array
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

from meshing.meshing import linspaces

try:
    import colorpy.illuminants
    import colorpy.colormodels
    from tmm import color
    colors_were_imported = True
except ImportError:
    # without colorpy, you can't run sample5(), but everything else is fine.
    colors_were_imported = False

import os
import re
import sys
import numpy
import argparse
import tempfile
import subprocess

# "5 * degree" is 5 degrees expressed in radians
# "1.2 / degree" is 1.2 radians expressed in degrees
degree = pi/180

def DBRinfo(n1, n2):
  midgap = (n1+n2)/(4*n1*n2)
  gapsize = ( (4/pi) * numpy.arcsin(abs( (n1-n2)/(n1+n2) )) )*midgap
  botgap = midgap - gapsize/2
  topgap = midgap + gapsize/2
  
  info =  dict()
  info['botgap'] = botgap
  info['midgap'] = midgap
  info['topgap'] = topgap
  
  return(info)

def FabryPerot(lam_vac, n_outside, n_inside, thickness, incidence_angle_rad):
  # function [reflectance, transmittance] = FabryPerot(lambda, n_outside, n_inside, thickness, incidence_angle_rad)
  #
  # Returns the reflectance and transmittance for a thin film
  #
  # input:
  #  lambda: wavelength of the incident light beam
  #  n_outside: refractive index of the medium around the thin film
  #  n_inside: refractive index of the thin film
  #  thickness: thickness of the thin film
  #  incidence_angle_rad: incidence angle of the incident light beam in radians
  #
  # output:
  #  reflectance: reflectance of the thin film
  #  transmittance: transmittance of the thin film
  #
  # refs:
  #   https://en.wikipedia.org/wiki/Fabry%E2%80%93P%C3%A9rot_interferometer
  #   Lipson, S.G.; Lipson, H.; Tannhauser, D.S. (1995). Optical Physics (3rd ed.). London: Cambridge U.P. p. 248. ISBN 0-521-06926-2. (or 4th edition, p305)
  #   Pochi Yeh, Optical waves in layered media
  #   Mark Fox, Quantum Optics
  
  # Normal Reflection Coefficient R
  R = ((n_inside-n_outside)/(n_inside+n_outside))**2
  # The phase difference between each succeeding reflection is given by δ
  delta = (2*pi/lam_vac)*(2*n_inside*thickness*numpy.cos(incidence_angle_rad))
  
  # "coefficient of finesse" F (not "finesse") ( "finesse" = Delta(lambda)/delta(lambda) ~ pi*sqrt("coefficient of finesse")/2 )
  F = (4*R)/(1-R)**2
  transmittance = 1/(1+F*(numpy.sin(delta/2)**2))
  reflectance = 1 - transmittance
  return (reflectance, transmittance)

def FabryPerotTest():
  lam_vac = linspace(0.75, 1.7, 100);
  n_outside = 1;
  n_inside = 3;
  thickness = 1;
  incidence_angle = 0;
  reflectance, transmittance = FabryPerot(lam_vac, n_outside, n_inside, thickness, incidence_angle)
  
  # list of layer thicknesses in nm
  d_list = [inf, thickness, inf]
  # list of refractive indices
  n_list = [n_outside, n_inside, n_outside]
  
  Rnorm = []
  Tnorm = []
  for lam_vac_current in lam_vac:
    result = coh_tmm('s', n_list, d_list, 0, lam_vac_current)
    Rnorm.append(result['R'])
    Tnorm.append(result['T'])
  
  plt.figure()
  plt.plot(lam_vac, reflectance, 'red')
  plt.plot(lam_vac, transmittance, 'blue')
  plt.plot(lam_vac, Rnorm, 'ro')
  plt.plot(lam_vac, Tnorm, 'bo')
  plt.xlabel('$\lambda$ (nm)')
  plt.ylabel('reflectance, transmittance')
  plt.title('reflectance (red), transmittance (blue) of unpolarized light at 0$^\circ$ incidence')
  plt.show()

def test_DBR_felipe(args):
  # .. todo:: find way to visualize DBR, maybe TMM module has something for that or use PIL module or similar
  # .. todo:: difference between DBR ending with high or low index layer?
  
  # 
  
  n_low = 2.94
  n_high = 3.55
  n_cav = n_high
  wavelength_0_nm = 910
  
  t_low = wavelength_0_nm/(4*n_low)
  t_high = wavelength_0_nm/(4*n_high)
  t_cav = 4*wavelength_0_nm/(4*n_high)
  
  # TMM for 33/24 DBR with lambda cavity leads to Q = 3.1335e+05
  
  #lam_range = 0.01
  #N_top = 24
  ##N_bottom = 16 # 33
  #N_bottom = 33 #int(round(N_top*33/24))
  
  lam_range = args.lam_range
  N_top = args.N_top
  N_bottom = args.N_bottom
  
  # list of layer thicknesses in nm
  # list of refractive indices
  
  d_list = [inf]
  n_list = [args.n_inf_top]
  
  for i in range(N_top):
    d_list.extend([t_high, t_low])
    n_list.extend([n_high, n_low])
  
  #if args.no_cavity:
    #d_list.extend([t_high])
    #n_list.extend([n_high])
  #else:
    #d_list.extend([t_cav])
    #n_list.extend([n_cav])
  
  #for i in range(N_bottom):
    #d_list.extend([t_low, t_high])
    #n_list.extend([n_low, n_high])
  
  d_list.extend([inf])
  n_list.extend([args.n_inf_bottom])
  
  print(d_list)
  print(n_list)
  print(len(d_list))
  print(len(n_list))
  
  lam_vac = linspace(wavelength_0_nm-lam_range, wavelength_0_nm+lam_range, args.Npoints)
  
  Rnorm = []
  Tnorm = []
  for lam_vac_current in lam_vac:
    result = coh_tmm('s', n_list, d_list, 0, lam_vac_current)
    Rnorm.append(result['R'])
    Tnorm.append(result['T'])
  
  info = DBRinfo(n_low, n_high)
  print(info)
  a = t_high + t_low
  lam_bot = a/info['topgap']
  lam_mid = a/info['midgap']
  lam_top = a/info['botgap']
  print([lam_bot, lam_mid, lam_top])
  
  Tnorm = numpy.array(Tnorm)
  if args.normalize:
    Tnorm = Tnorm / max(Tnorm)
  
  plt.figure()
  if args.plot_reflection:
    plt.plot(lam_vac, Rnorm, 'r')
  plt.plot(lam_vac, Tnorm, 'b')
  
  #plt.axvline(lam_bot, linestyle='--', color='g')
  plt.axvline(lam_mid, linestyle='--', color='g')
  #plt.axvline(lam_top, linestyle='--', color='g')
  
  plt.xlabel('$\lambda$ (nm)')
  plt.ylabel('reflectance, transmittance')
  plt.title('reflectance (red), transmittance (blue) of unpolarized light at 0$^\circ$ incidence')
  plt.show()
  
  if args.csvfile:
    csvfile = args.csvfile
  else:
    csvfile = 'DBR_Nbot-{}_Ntop-{}_N-{}_r-{}_norm-{}_cav-{}.csv'.format(args.N_bottom, args.N_top, args.Npoints, args.lam_range, args.normalize, not args.no_cavity)
  #numpy.savetxt('test_TMM.csv', numpy.transpose([lam_vac,Tnorm]), delimiter=';', header='lam_vac;Tnorm')
  numpy.savetxt(csvfile, numpy.transpose([lam_vac,Tnorm,Rnorm]), delimiter=';', header='lam_vac;Tnorm;Rnorm')
  
  return

def test_DBR(args):
  # .. todo:: find way to visualize DBR, maybe TMM module has something for that or use PIL module or similar
  
  n_low = 2.94
  n_high = 3.55
  n_cav = n_high
  wavelength_0_nm = 910
  
  t_low = wavelength_0_nm/(4*n_low)
  t_high = wavelength_0_nm/(4*n_high)
  t_cav = 4*wavelength_0_nm/(4*n_high)
  
  # TMM for 33/24 DBR with lambda cavity leads to Q = 3.1335e+05
  
  #lam_range = 0.01
  #N_top = 24
  ##N_bottom = 16 # 33
  #N_bottom = 33 #int(round(N_top*33/24))
  
  #lam_range = args.lam_range
  N_top = args.N_top
  N_bottom = args.N_bottom
  
  # list of layer thicknesses in nm
  # list of refractive indices
  
  d_list = [inf]
  n_list = [1]
  
  for i in range(N_top):
    d_list.extend([t_high, t_low])
    n_list.extend([n_high, n_low])
  
  if args.no_cavity:
    d_list.extend([t_high])
    n_list.extend([n_high])
  else:
    d_list.extend([t_cav])
    n_list.extend([n_cav])
  
  for i in range(N_bottom):
    d_list.extend([t_low, t_high])
    n_list.extend([n_low, n_high])
  
  d_list.extend([inf])
  n_list.extend([1])
  
  print(d_list)
  print(n_list)
  print(len(d_list))
  print(len(n_list))
  
  # lambda range to use
  main_points = [wavelength_0_nm]
  for r in args.lam_range:
    main_points.append(wavelength_0_nm - r)
    main_points.append(wavelength_0_nm + r)
  main_points.sort()
  print('main_points = {}'.format(main_points))
  lam_vac = linspaces(main_points, (len(main_points)-1)*[args.Npoints])
  #print('lam_vac = {}'.format(lam_vac))
  #raise
  #if lam_range <= 0.01:
    #lam_vac = linspace(wavelength_0_nm-lam_range, wavelength_0_nm+lam_range, args.Npoints)
  #else:
    #lam_vac = linspaces(wavelength_0_nm-lam_range, wavelength_0_nm-0.01, wavelength_0_nm+lam_range, args.Npoints,wavelength_0_nm+lam_range, args.Npoints)
  
  Rnorm = []
  Tnorm = []
  for lam_vac_current in lam_vac:
    result = coh_tmm('s', n_list, d_list, 0, lam_vac_current)
    Rnorm.append(result['R'])
    Tnorm.append(result['T'])
  
  info = DBRinfo(n_low, n_high)
  print(info)
  a = t_high + t_low
  lam_bot = a/info['topgap']
  lam_mid = a/info['midgap']
  lam_top = a/info['botgap']
  print([lam_bot, lam_mid, lam_top])
  
  Tnorm = numpy.array(Tnorm)
  if args.normalize:
    Tnorm = Tnorm / max(Tnorm)
  
  plt.figure()
  if args.plot_reflection:
    plt.plot(lam_vac, Rnorm, 'r')
  plt.plot(lam_vac, Tnorm, 'b')
  
  #plt.axvline(lam_bot, linestyle='--', color='g')
  plt.axvline(lam_mid, linestyle='--', color='g')
  #plt.axvline(lam_top, linestyle='--', color='g')
  
  plt.xlabel('$\lambda$ (nm)')
  plt.ylabel('reflectance, transmittance')
  plt.title('reflectance (red), transmittance (blue) of unpolarized light at 0$^\circ$ incidence')
  plt.show()
  
  if args.csvfile:
    csvfile = args.csvfile
  else:
    csvfile = 'DBR_Nbot-{}_Ntop-{}_N-{}_r-{}_norm-{}_cav-{}.csv'.format(args.N_bottom, args.N_top, args.Npoints, args.lam_range, args.normalize, not args.no_cavity)
  #numpy.savetxt('test_TMM.csv', numpy.transpose([lam_vac,Tnorm]), delimiter=';', header='lam_vac;Tnorm')
  numpy.savetxt(csvfile, numpy.transpose([lam_vac,Tnorm,Rnorm]), delimiter=';', header='lam_vac;Tnorm;Rnorm')
  
  return

def test_sample1():
  """
  Here's a thin non-absorbing layer, on top of a thick absorbing layer, with
  air on both sides. Plotting reflected intensity versus wavenumber, at two
  different incident angles.
  """
  
  # list of layer thicknesses in nm
  d_list = [inf,100,300,inf]
  # list of refractive indices
  n_list = [1,2.2,3.3+0.3j,1]
  # list of wavenumbers to plot in nm^-1
  ks=linspace(0.0001,.01,num=400)
  # initialize lists of y-values to plot
  Rnorm=[]
  R45=[]
  
  # coh_tmm(pol, n_list, d_list, th_0, lam_vac)

  for k in ks:
  # For normal incidence, s and p polarizations are identical.
  # I arbitrarily decided to use 's'.
    Rnorm.append(coh_tmm('s',n_list, d_list, 0, 1/k)['R'])
    R45.append(unpolarized_RT(n_list, d_list, 45*degree, 1/k)['R'])
  kcm = ks * 1e7 #ks in cm^-1 rather than nm^-1
  plt.figure()
  plt.plot(kcm,Rnorm,'blue',kcm,R45,'purple')
  plt.xlabel('k (cm$^{-1}$)')
  plt.ylabel('Fraction reflected')
  plt.title('Reflection of unpolarized light at 0$^\circ$ incidence (blue), '
              '45$^\circ$ (purple)')
  plt.show()
  
  return 0

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--N_top', default=24, type=int)
  parser.add_argument('--N_bottom', default=33, type=int)
  parser.add_argument('--lam_range', default=[0.01], type=float, nargs='+')
  parser.add_argument('--Npoints', default=1000, type=int)
  parser.add_argument('--csvfile', default=None, type=str)
  parser.add_argument('--normalize', action='store_true')
  parser.add_argument('--no-cavity', action='store_true')
  parser.add_argument('--n-inf-top', default=1, type=float)
  parser.add_argument('--n-inf-bottom', default=1, type=float)
  parser.add_argument('--plot-reflection', action='store_true')
  parser.add_argument('-v', '--verbose', action="count", dest="verbosity", default=0, help='verbosity level')
  args = parser.parse_args()
  print(args)
  test_DBR(args)
  return

if __name__ == '__main__':
  #test_DBR()
  #DBRinfo(1, 2)
  main()
