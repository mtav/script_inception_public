#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Examples of plots and calculations using the tmm package.
Created on Fri May 20 16:15:08 2022
@author: Mike Taverne
"""

from __future__ import division, print_function, absolute_import

from tmm import (coh_tmm, unpolarized_RT, ellips,
                       position_resolved, find_in_structure_with_inf)

import numpy as np
from numpy import pi, linspace, inf, array
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

try:
    import colorpy.illuminants
    import colorpy.colormodels
    from . import color
    colors_were_imported = True
except ImportError:
    # without colorpy, you can't run sample5(), but everything else is fine.
    colors_were_imported = False


# "5 * degree" is 5 degrees expressed in radians
# "1.2 / degree" is 1.2 radians expressed in degrees
degree = pi/180

def quarterwavestack():
    """
    Here's a thin non-absorbing layer, on top of a thick absorbing layer, with
    air on both sides. Plotting reflected intensity versus wavenumber, at two
    different incident angles.
    """
    # list of layer thicknesses in nm
#    lam = 637 # nm
    n1 = 1.57
    n2 = 1.00
#    t1 = lam/(4*n1)
#    t2 = lam/(4*n2)
#    a = t1 + t2
#    t1n = t1/a
#    t2n = t2/a
    a = 3000
    t1 = 1100
    t2 = a - t1
    
    d_list = [inf] + 10*[t1, t2] + [inf]
    n_list = [1] + 10*[n1, n2] + [1]
    # list of refractive indices
    # n_list = [1, 2.2, 3.3+0.3j, 1]
    # list of wavenumbers to plot in nm^-1
    ks = linspace(1./1500, 1./400, num=400)
    #lam_list = linspace(10, 2000, num=40000)
    #ks = 1./lam_list
    
    # initialize lists of y-values to plot
    Rnorm = []
    R45 = []
    x = linspace(0,45,100)
    y = 1/ks # wavelength in nm
    Y, X = np.meshgrid(y, x)
    R = np.ones(X.shape)
    for idx, theta_deg in enumerate(x):
        data1D = []
        for k in ks:
            data1D.append(coh_tmm('s', n_list, d_list, theta_deg*degree, 1/k)['R'])
        R[idx]=data1D
    kcm = ks * 1e7 #ks in cm^-1 rather than nm^-1

    # wavelength in nm
    plot2D(X,Y,R)
    plt.xlabel("Angle (degrees)")
    plt.ylabel("\lambda (nm)")
    # normalized frequency
    plot2D(X, a/Y, R)
    plt.xlabel("Angle (degrees)")
    plt.ylabel("a/\lambda")
    return

def reference_DBR():
    wvl_min_nm = 345.038
    wvl_max_nm = 1034.95
  
    """
    Layer 1) Ta2O5, 246nm, n=2.05
    Layer 2) SiO2, 343nm, n=1.43
    Layer 3) Ta2O5, 246nm, n=2.05
    ...
    Layer 28) SiO2, 343nm, n=1.43
    Layer 29) Ta2O5, 246nm, n=2.05
    Layer 30) SiO2, 343nm, n=1.43
    Layer 31) Ta2O5, 246nm, n=2.05
    """
    # list of layer thicknesses in nm
#    lam = 637 # nm
    n1 = 2.05
    n2 = 1.43
#    t1 = lam/(4*n1)
#    t2 = lam/(4*n2)
#    a = t1 + t2
#    t1n = t1/a
#    t2n = t2/a
    t1 = 246 #nm
    t2 = 343 #nm
    a = t1 + t2
    
    d_list = [inf] + 15*[t1, t2] + [t1] + [inf]
    n_list = [1] + 15*[n1, n2] + [n1] + [1]
  
    # list of refractive indices
    # n_list = [1, 2.2, 3.3+0.3j, 1]
    # list of wavenumbers to plot in nm^-1
    ks = linspace(1./wvl_max_nm, 1./wvl_min_nm, num=400)
    #lam_list = linspace(10, 2000, num=40000)
    #ks = 1./lam_list
    
    # initialize lists of y-values to plot
    Rnorm = []
    R45 = []
    x = linspace(-45,45,201)
    y = 1/ks # wavelength in nm
    Y, X = np.meshgrid(y, x)
    R = np.ones(X.shape)
    for idx, theta_deg in enumerate(x):
        data1D = []
        for k in ks:
            data1D.append(coh_tmm('p', n_list, d_list, theta_deg*degree, 1/k)['R'])
        R[idx]=data1D
    kcm = ks * 1e7 #ks in cm^-1 rather than nm^-1

    # wavelength in nm
    plot2D(X,Y,R)
    plt.xlabel("Angle (degrees)")
    plt.ylabel("$\lambda (nm)$")
    plt.show()
  
    # normalized frequency
    plot2D(X, a/Y, R)
    plt.xlabel("Angle (degrees)")
    plt.ylabel("$a/\lambda$")
    plt.show()
    return

def plot2D(x,y,z):
    z_min, z_max = -abs(z).max(), abs(z).max()
    
    fig = plt.figure()
    c = plt.pcolormesh(x, y, z, cmap='RdBu', vmin=z_min, vmax=z_max, shading='gouraud')
    fig.colorbar(c)
        
    fig.tight_layout()
    #plt.show()

# quarterwavestack()
reference_DBR()
