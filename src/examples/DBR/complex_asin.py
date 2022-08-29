# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 10:16:48 2022

@author: Mike Taverne
Test of arcsin for values outside [-1,1] range.

definitions:
    numpy:
        https://numpy.org/doc/stable/reference/generated/numpy.arcsin.html
    matlab:
        https://www.mathworks.com/help/matlab/ref/asin.html
"""
import numpy as np
import matplotlib.pyplot as plt

def matlab_arcsin(z):
    f = -1j*np.log(1j*z + np.power((1-z**2), 1/2));
    return(f)

P=5 # points in between integers
N=2 # zmax
Npts = 1 + 2*N*(P+1) # number of points
z = np.linspace(-N, N, Npts);

plt.plot(z, np.arcsin(z), 'k-', label=r'arcsin(z)');

plt.plot(z, np.real(np.arcsin(z+0j)), 'ro', label=r'real(numpy.arcsin(z+0j))', markerfacecolor='none');
plt.plot(z, np.imag(np.arcsin(z+0j)), 'bx', label=r'imag(numpy.arcsin(z+0j))', markerfacecolor='none');

plt.plot(z, np.real(matlab_arcsin(z+0j)), 'r+', label=r'real(matlab_arcsin(z+0j))', markerfacecolor='none');
plt.plot(z, np.imag(matlab_arcsin(z+0j)), 'bs', label=r'imag(matlab_arcsin(z+0j))', markerfacecolor='none');

plt.xlabel(r'z');
plt.ylabel(r'$\theta$ (radians)');
plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0.);
