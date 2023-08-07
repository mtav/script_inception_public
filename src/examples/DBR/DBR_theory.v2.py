#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import this first, as scipy has two constants module, which can lead to conflicts...
#   scipy.optimize._highs.constants
#   scipy.constants
# TODO: convert SIP to a proper module (again)
# Use the scipy.constants module instead
# from constants import get_c0

# other imports
import warnings
import scipy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema, argrelmin, find_peaks
from tmm import coh_tmm
import math
import meep as mp
from meep import mpb
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy.io import savemat
import os

# https://blakeaw.github.io/2020-05-25-improve-matplotlib-notebook-inline-res/
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

def get_c0():
    '''
    speed of light in vacuum
    '''
    return scipy.constants.c

class DBR():
    n1 = np.sqrt(2)
    n2 = np.sqrt(13)
    t1 = n2/(n1+n2)
    t2 = n1/(n1+n2)

    @property
    def a(self): return self.getPeriod()

    def getBraggFrequency(self):
        '''
        Returns omega_{B}=(c0/navg)*(pi/a)
        where:
            navg = (n1*t1+n2*t2)/a
        '''
        return (get_c0()/self.getAverageRefractiveIndex()) * (np.pi/self.getPeriod())

    def getAverageRefractiveIndex(self):
        return (self.n1*self.t1 + self.n2*self.t2) / self.getPeriod()
        

    def getBrewsterAngles(self, degrees=False):
        '''
        Returns the Brewster angles (thetaB_1_deg, thetaB_2_deg), where:
            * thetaB_1_deg: Brewster angle if light is coming from medium n_in=n1 and the first layer is n2.
            * thetaB_2_deg: Brewster angle if light is coming from medium n_in=n2 and the first layer is n1.
        '''
        thetaB_1_rad = np.arctan(self.n2/self.n1)
        thetaB_2_rad = np.arctan(self.n1/self.n2)
        if degrees:
            thetaB_1_deg = np.rad2deg(thetaB_1_rad)
            thetaB_2_deg = np.rad2deg(thetaB_2_rad)
            return (thetaB_1_deg, thetaB_2_deg)
        else:
            return (thetaB_1_rad, thetaB_2_rad)

    def getMatrixElements(self, omega=1, beta=1, Spol=False):
        n1 = self.n1
        n2 = self.n2
        a = self.t1
        b = self.t2
        
        # convert to array (in case a list is passed)
        omega = np.array(omega)
        beta = np.array(beta)
        
        k1x = np.sqrt( (n1*omega/get_c0())**2 - beta**2 + 0j)
        k2x = np.sqrt( (n2*omega/get_c0())**2 - beta**2 + 0j)

        # ignore warnings when k1x==0 or k2x==0 (which happens when omega==beta==0 or when theta1==90deg or theta2==90deg)
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=RuntimeWarning, message="invalid value encountered in true_divide", append=True)
            warnings.filterwarnings("ignore", category=RuntimeWarning, message="divide by zero encountered in true_divide", append=True)
            warnings.filterwarnings("ignore", category=RuntimeWarning, message="invalid value encountered in cdouble_scalars", append=True)
            warnings.filterwarnings("ignore", category=RuntimeWarning, message="divide by zero encountered in cdouble_scalars", append=True)
            warnings.filterwarnings("error", append=True)
            if Spol:
                # S-polarization
                u = k2x/k1x
                v = k1x/k2x
            else:
                # P-polarization
                u = (pow(n2,2)*k1x) / (pow(n1,2)*k2x)
                v = (pow(n1,2)*k2x) / (pow(n2,2)*k1x)
        
        # ignore warnings when k1x==0 or k2x==0 (which happens when omega==beta==0 or when theta1==90deg or theta2==90deg)
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=RuntimeWarning, message="invalid value encountered in cdouble_scalars", append=True)
            warnings.filterwarnings("ignore", category=RuntimeWarning, message="invalid value encountered in multiply", append=True)
            warnings.filterwarnings("error", append=True)
            A = np.exp( 1j*k1x*a) * ( np.cos(k2x*b) + (1/2)*1j*(u + v)*np.sin(k2x*b) )
            B = np.exp(-1j*k1x*a) * ( ( 1/2)*1j*(u - v)*np.sin(k2x*b) )
            C = np.exp( 1j*k1x*a) * ( (-1/2)*1j*(u - v)*np.sin(k2x*b) )
            D = np.exp(-1j*k1x*a) * ( np.cos(k2x*b) - (1/2)*1j*(u + v)*np.sin(k2x*b) )
            
        ##### when k1x=k2x=0, A=D=1 and B=C=0
        for idx, val in np.ndenumerate(omega):
            if k1x[idx]==0 and k2x[idx]==0:
                A[idx] = 1
                B[idx] = 0
                C[idx] = 0
                D[idx] = 1
                
        return(A, B, C, D)

    def getK(self, omega=1, beta=1, Spol=False):
        # convert to array (in case a list is passed)
        omega = np.array(omega)
        beta = np.array(beta)
        (A,B,C,D) = self.getMatrixElements(omega=omega, beta=beta, Spol=Spol)
        K = (1/self.getPeriod())*np.arccos((1/2)*(A+D))
        return K

    def getPeriod(self):
        period = self.t1 + self.t2
        return period
    
    def getBandEdges(self, omega=1, beta=1, Spol=False, plot_X=None, plot_Y=None):
        
        # convert to array (in case a list is passed)
        omega = np.array(omega)
        beta = np.array(beta)
        
        # get matrix elements
        (A,B,C,D) = self.getMatrixElements(omega=omega, beta=beta, Spol=Spol)
        cosval = np.abs((1/2)*(A+D))

        ##### dataframe including only index values
        # create dataframe that will contain the band edge data
        df_idx = pd.DataFrame()

        # fill the dataframe
        for slice_idx in range(beta.shape[0]):
            
            y = cosval[slice_idx,:] # criteria values
            
            y2 = np.abs(y-1) # function for which to find zeros
            idx = argrelmin(y2) # relative minima (not zeros!)
            
            # plt.figure()
            # plt.plot(y2)
            
            # col = pd.DataFrame(data=np.array(idx), columns=[slice_idx])
            col = pd.DataFrame(data=idx[0], columns=[slice_idx])
            
            # print(col)
            # print(col.shape)
            # raise
            df_idx = pd.concat([df_idx, col], axis=1)
            
        # print(df_idx.shape)
        # raise
        # transpose dataframe
        df_idx = df_idx.T
        # name columns
        df_idx.columns = [f'band_{i}' for i in df_idx.columns]

        ##### dataframe including values
        if plot_X is None:
            plot_X = beta
        if plot_Y is None:
            plot_Y = omega
    
        # create dataframe that will contain the band edge data
        df = pd.DataFrame()

        ##### fill the dataframe
        for slice_idx, plot_X_slice in enumerate(plot_X[:,0]):
            
            x = plot_Y[slice_idx,:] # omega values
            y = cosval[slice_idx,:] # criteria values
            
            y2 = np.abs(y-1) # function for which to find zeros
            idx = argrelmin(y2) # relative minima (not zeros!)
            r1 = x[idx] # omega band edge values
    
            col = pd.DataFrame(data=r1, columns=[plot_X_slice])
            df = pd.concat([df, col], axis=1)
            
        # transpose dataframe
        df = df.T
        # name columns
        df.columns = [f'band_{i}' for i in df.columns]
        
        # print(df.shape)
        # print(df_idx.shape)
        # raise
        return df, df_idx

class plottingRange():
    '''
    A class to handle plotting parameters.
    '''

    __beta_n_1D = None
    __angle_deg_1D = None

    @property
    def lattice_constant(self): return self.__lattice_constant
    @property
    def n_in(self): return self.__n_in

    @property
    def beta_n_1D(self): return self.__beta_n_1D
    @property
    def beta_n_2D(self): return self.__beta_n_2D
    @property
    def beta_1D(self):
      if self.__beta_n_1D is not None:
        return (2*np.pi/self.__lattice_constant) * self.__beta_n_1D
      else:
        return None
    @property
    def beta_2D(self): return (2*np.pi/self.__lattice_constant) * self.__beta_n_2D
    @property
    def angle_deg_1D(self): return self.__angle_deg_1D
    @property
    def angle_deg_2D(self): return self.__angle_deg_2D
    @property
    def angle_rad_1D(self): return np.deg2rad(self.__angle_deg_1D)
    @property
    def angle_rad_2D(self): return np.deg2rad(self.__angle_deg_2D)

    @property
    def fn_1D(self): return self.__fn_1D
    @property
    def fn_2D(self): return self.__fn_2D
    @property
    def wvl_1D(self):
      with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=RuntimeWarning, message="divide by zero encountered in true_divide", append=False)
        warnings.filterwarnings("ignore", category=RuntimeWarning, message="divide by zero encountered in divide", append=False)
        return self.__lattice_constant / self.__fn_1D
    @property
    def wvl_2D(self):
      with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=RuntimeWarning, message="divide by zero encountered in true_divide", append=False)
        warnings.filterwarnings("ignore", category=RuntimeWarning, message="divide by zero encountered in divide", append=False)
        return self.__lattice_constant / self.__fn_2D
    @property
    def omega_1D(self): return (2*np.pi*get_c0()/self.__lattice_constant)*self.__fn_1D
    @property
    def omega_2D(self): return (2*np.pi*get_c0()/self.__lattice_constant)*self.__fn_2D
        
    def __init__(self,
                 wvl=None,
                 fn=None,
                 beta_normalized=None,
                 angle_deg=None,
                 n_in=1,
                 lattice_constant=1):

      # other default values
      if fn is None and wvl is None:
        wvl = np.linspace(345.038, 1034.95, 4)*1e-9
      if beta_normalized is None and angle_deg is None:
        angle_deg = np.linspace(0, 90, 3)
      
      # define normalization variables
      self.__n_in = n_in
      self.__lattice_constant = lattice_constant
      
      # set Y axis variable
      if fn is not None:
        self.__fn_1D = np.array(fn)
      else:
        with warnings.catch_warnings():
          warnings.filterwarnings("ignore", category=RuntimeWarning, message="divide by zero encountered in true_divide", append=False)
          self.__fn_1D = self.__lattice_constant / np.array(wvl)
    
      # set X axis variable
      if angle_deg is not None:
        self.__angle_deg_1D = np.array(angle_deg)
      else:
        self.__beta_n_1D = np.array(beta_normalized)
        
      self.update()

    def update(self):
      if self.__beta_n_1D is not None:
        # print('==> X = beta_n_1D')
        self.__fn_2D, self.__beta_n_2D = np.meshgrid(self.__fn_1D, self.__beta_n_1D)
        
        with warnings.catch_warnings():
          warnings.filterwarnings("ignore", category=RuntimeWarning, message="divide by zero encountered in true_divide", append=False)
          warnings.filterwarnings("ignore", category=RuntimeWarning, message="invalid value encountered in true_divide", append=False)
          warnings.filterwarnings("ignore", category=RuntimeWarning, message="invalid value encountered in arcsin", append=False)
          self.__angle_deg_2D = np.rad2deg( np.arcsin( self.__beta_n_2D / (self.__n_in * self.__fn_2D) ) )

      elif self.__angle_deg_1D is not None:
        # print('==> X = angle_deg_1D')
        self.__fn_2D, self.__angle_deg_2D = np.meshgrid(self.__fn_1D, self.__angle_deg_1D)

        with warnings.catch_warnings():
          warnings.filterwarnings("ignore", category=RuntimeWarning, message="invalid value encountered in multiply", append=False)
          warnings.filterwarnings("ignore", category=RuntimeWarning, message="invalid value encountered in sin", append=False)
          self.__beta_n_2D = self.__n_in * self.__fn_2D * np.sin( np.deg2rad(self.__angle_deg_2D) )
        
      else:
        raise

      return

    def imshow(self):
      fig, axs = plt.subplots(3, 2)
      
      axs[0,0].imshow(self.beta_n_2D)
      axs[0,0].set_title('beta_n_2D')
      axs[1,0].imshow(self.beta_2D)
      axs[1,0].set_title('beta_2D')
      axs[2,0].imshow(self.angle_deg_2D)
      axs[2,0].set_title('angle_deg_2D')
      
      axs[0,1].imshow(self.fn_2D)
      axs[0,1].set_title('fn_2D')
      axs[1,1].imshow(self.wvl_2D)
      axs[1,1].set_title('wvl_2D')
      axs[2,1].imshow(self.omega_2D)
      axs[2,1].set_title('omega_2D')

    def __str__(self):
      s=''
      s+='----- Normalization parameters:\n'
      s+=f'lattice_constant = {self.lattice_constant}\n'
      s+=f'n_in = {self.n_in}\n'
      s+='----- 1D X values:\n'
      s+=f'beta_n_1D = {self.beta_n_1D}\n'
      s+=f'beta_1D = {self.beta_1D}\n'
      s+=f'angle_deg_1D = {self.angle_deg_1D}\n'
      s+='----- 1D Y values:\n'
      s+=f'fn_1D = {self.fn_1D}\n'
      s+=f'wvl_1D = {self.wvl_1D}\n'
      s+=f'omega_1D = {self.omega_1D}\n'
      s+='----- 2D X data shapes:\n'
      s+=f'np.shape(beta_n_2D): {np.shape(self.beta_n_2D)}\n'
      s+=f'np.shape(beta_2D): {np.shape(self.beta_2D)}\n'
      s+=f'np.shape(angle_deg_2D): {np.shape(self.angle_deg_2D)}\n'
      s+='----- 2D Y data shapes:\n'
      s+=f'np.shape(fn_2D): {np.shape(self.fn_2D)}\n'
      s+=f'np.shape(wvl_2D): {np.shape(self.wvl_2D)}\n'
      s+=f'np.shape(omega_2D): {np.shape(self.omega_2D)}\n'
      s+='----- data:\n'
      s+=f'angle_deg_2D = {self.angle_deg_2D}\n'
      s+=f'beta_n_2D = {self.beta_n_2D}\n'

      return s
  
    def is_vs_angle(self):
        '''Returns True if arrays are defined based on angle, else returns False.'''
        if self.__beta_n_1D is not None:
          return False
        elif self.__angle_deg_1D is not None:
          return True
        else:
          raise
        pass

def plot2D(x, y, z, yhack=True):
    # z_min, z_max = -abs(z).max(), abs(z).max()
    
    if yhack:
        if np.isinf(y).any():
            x = x[:,1:]
            y = y[:,1:]
            z = z[:,1:]
    
    if np.isinf(x).any():
        raise Exception('x has infinite values.')
    if np.isinf(y).any():
        raise Exception('y has infinite values.')
    if np.isnan(x).any():
        raise Exception('x has NaN values.')
    if np.isnan(y).any():
        raise Exception('y has NaN values.')
    
    fig = plt.figure()
    # c = plt.pcolormesh(x, y, z, cmap='RdBu', vmin=z_min, vmax=z_max, shading='gouraud')
    if np.amax(z) <= 1:
        c = plt.pcolormesh(x, y, z, shading='gouraud')
    else:
        print('Warning: vmax>1! Clipping values.')
        c = plt.pcolormesh(x, y, z, shading='gouraud', vmax=1)
    fig.colorbar(c)
        
    fig.tight_layout()
    #plt.show()
    return(fig)

def test_plot2D():
    x = np.linspace(-10,10,100)
    y = np.linspace(-5,5,200)
    Y, X = np.meshgrid(y, x)
    # X, Y = np.meshgrid(x, y)
    R = np.ones(X.shape)
    R = np.exp( -( (X**2 + Y**2 ) / (2**2)) )
    
    # f1 = plt.figure()
    f1 = plot2D(X, Y, R)
    plt.title('NO TITLE')
    
    # f2 = plt.figure()
    f2 = plot2D(X, Y, R)
    
    plt.figure(f1.number)
    plt.title('My figure 1')
    plt.axhline(0)
    
    plt.figure(f2.number)
    plt.title('My figure 2')
    plt.axvline(0)
    
    plt.show()
    print(R.shape)

def plotDBR(dbr_instance = DBR()):
    
    omega_normalized = np.linspace(0, 1.4, 300)
    beta_normalized = np.linspace(0, 1, 200)
    omega = omega_normalized * (2*np.pi*get_c0()/dbr_instance.getPeriod())
    beta = beta_normalized * (2*np.pi/dbr_instance.getPeriod())
    
    Y, X = np.meshgrid(omega, beta)
    YN, XN = np.meshgrid(omega_normalized, beta_normalized)
    
    K_Spol = dbr_instance.getK(omega=Y, beta=X, Spol=True)
    plot2D(XN, YN, np.isreal(K_Spol))
    plt.xlabel("Wave vector $k_y a/(2\pi)$")
    plt.ylabel("Frequency $\omega a / (2 \pi c)$")
    plt.title("S polarization")

    K_Ppol = dbr_instance.getK(omega=Y, beta=X, Spol=False)
    plot2D(XN, YN, np.isreal(K_Ppol))
    plt.xlabel("Wave vector $k_y a/(2\pi)$")
    plt.ylabel("Frequency $\omega a / (2 \pi c)$")
    plt.title("P polarization")
    
    (thetaB_1_rad, thetaB_2_rad) = dbr_instance.getBrewsterAngles(degrees=False)
    
    slope = 1 / ( dbr_instance.n1 * np.sin( thetaB_1_rad ) )
    plt.plot(beta_normalized, slope*beta_normalized, 'r-', label=r'$slope = 1/(n_1*sin(\theta_{B1}))$')

    slope = 1
    plt.plot(beta_normalized, slope*beta_normalized, 'k--', label='$slope = 1$')

    slope = 1/dbr_instance.n1
    plt.plot(beta_normalized, slope*beta_normalized, 'g:', label='$slope = 1/n_1$')

    slope = 1/dbr_instance.n2
    plt.plot(beta_normalized, slope*beta_normalized, 'b:', label='$slope = 1/n_2$')

    plt.legend()

def plotDBR_vs_angle(dbr_instance = DBR(), n_in = DBR.n1):
    
    omega_normalized = np.linspace(0, 1.4, 300)
    angle_deg = np.linspace(0, 90, 300)

    omega_normalized, angle_deg = np.meshgrid(omega_normalized, angle_deg)

    omega = omega_normalized * (2*np.pi*get_c0()/dbr_instance.getPeriod())
        
    angle_rad = np.deg2rad(angle_deg)

    beta = (omega*n_in/get_c0()) * np.sin(angle_rad)
    beta_normalized = beta / (2*np.pi/dbr_instance.getPeriod())
    
    K_Spol = dbr_instance.getK(omega=omega, beta=beta, Spol=True)
    plot2D(angle_deg, omega_normalized, np.isreal(K_Spol))
    plt.xlabel(r"Incident angle $\theta_{in}$ (degrees)")
    plt.ylabel(r"Frequency $\omega a / (2 \pi c)$")
    plt.title(fr"S polarization, $n_{{in}} = {n_in}$")

    K_Ppol = dbr_instance.getK(omega=omega, beta=beta, Spol=False)
    plot2D(angle_deg, omega_normalized, np.isreal(K_Ppol))
    plt.xlabel(r"Incident angle $\theta_{in}$ (degrees)")
    plt.ylabel(r"Frequency $\omega a / (2 \pi c)$")
    plt.title(fr"P polarization, $n_{{in}} = {n_in}$")
    
    (thetaB_1_deg, thetaB_2_deg) = dbr_instance.getBrewsterAngles(degrees=True)
    plt.axvline(x = thetaB_1_deg, color = 'r', label = r'$\theta_{B1}$')
    plt.axvline(x = thetaB_2_deg, color = 'b', label = r'$\theta_{B2}$')

    plt.axvline(x = np.rad2deg(np.arcsin(dbr_instance.n1/dbr_instance.n2)), color = 'k', label = r'$\theta_C$')
    plt.legend()
    
def testBrewsterAngles():
    foo = DBR()
    print(f'-> Brewster angles for n1={foo.n1}, n2={foo.n2}:\n in radians: {foo.getBrewsterAngles()}\n in degrees: {foo.getBrewsterAngles(degrees=True)}')
    # air/glass interface
    foo.n1=1
    foo.n2=1.5
    print(f'-> Brewster angles for n1={foo.n1}, n2={foo.n2}:\n in radians: {foo.getBrewsterAngles()}\n in degrees: {foo.getBrewsterAngles(degrees=True)}')
    # air/water interface
    foo.n1=1
    foo.n2=1.33
    print(f'-> Brewster angles for n1={foo.n1}, n2={foo.n2}:\n in radians: {foo.getBrewsterAngles()}\n in degrees: {foo.getBrewsterAngles(degrees=True)}')

def IdxToVal(df_idx, plot_X, plot_Y):
    for col in df_idx.columns:
        print('col', col)
        omega_idx = df_idx[col]
        omega_idx = omega_idx[~np.isnan(omega_idx)]
        omega_idx = omega_idx.astype(int)
        y = plot_Y[0, idx]
        
        x_idx = np.argwhere(np.array(~np.isnan(df_idx[col])))
        x_idx = np.squeeze(x_idx)
        x = plot_X[x_idx,0]
        
    return df
    
def findBandEdgesAnalysis(dbr_instance=DBR(), Spol=True, n_in = DBR.n1, vs_angle=False):
    if vs_angle:
        ##### vs angle
        omega_normalized = np.linspace(0, 1.4, 400)
        angle_deg = np.linspace(0, 90, 300)
    
        omega_normalized, angle_deg = np.meshgrid(omega_normalized, angle_deg)
    
        omega = omega_normalized * (2*np.pi*get_c0()/dbr_instance.getPeriod())
            
        angle_rad = np.deg2rad(angle_deg)
    
        beta = (omega*n_in/get_c0()) * np.sin(angle_rad)
        beta_normalized = beta / (2*np.pi/dbr_instance.getPeriod())
    
        # plot_X = beta_normalized
        # plot_X = beta
        plot_X = beta_normalized
        plot_X_label = "Wave vector $k_y a/(2\pi)$"
        # plot_X = angle_deg
        # plot_X_label = r"Incident angle $\theta_{in}$ (degrees)"
        ##############################################################
        # plt.figure();
        # plt.imshow(omega_normalized); plt.title('omega_normalized')
        # plt.figure()
        # plt.imshow(beta_normalized); plt.title('beta_normalized')
        # plt.colorbar()
        # plt.figure()
        # plt.imshow(beta); plt.title('beta')
        # plt.colorbar()
        # plt.figure();
        # plt.imshow(angle_deg); plt.title('angle_deg')
        # return

    else:
        ##### vs ky
        omega_normalized = np.linspace(0, 1.4, 300)
        beta_normalized = np.linspace(0, 1, 200)
    
        omega_normalized, beta_normalized = np.meshgrid(omega_normalized, beta_normalized)
    
        omega = omega_normalized * (2*np.pi*get_c0()/dbr_instance.getPeriod())
        beta = beta_normalized * (2*np.pi/dbr_instance.getPeriod())
        plot_X = beta_normalized
        plot_X_label = "Wave vector $k_y a/(2\pi)$"
        
        angle_rad = np.arcsin( (beta*get_c0())/(n_in*omega) )
        angle_deg = np.rad2deg(angle_rad)
        ##############################################################

    title_base = fr"Spol={Spol}, $n_{{in}}$={n_in}"

    K_Spol = dbr_instance.getK(omega=omega, beta=beta, Spol=Spol)

    f1 = plot2D(plot_X, omega_normalized, np.isreal(K_Spol)) # plot bands for reference
    plt.xlabel(plot_X_label)
    plt.ylabel("Frequency $\omega a / (2 \pi c)$")
    plt.title(fr"{title_base}: isreal(K)")

    # f2 = plot2D(plot_X, omega_normalized, np.abs(K_Spol)) # plot bands for reference
    # plt.xlabel(plot_X_label)
    # plt.ylabel("Frequency $\omega a / (2 \pi c)$")
    # plt.title(fr"{title_base}: abs(K)")
    
    # f3 = plot2D(plot_X, omega_normalized, np.real(K_Spol)) # plot bands for reference
    # plt.xlabel(plot_X_label)
    # plt.ylabel("Frequency $\omega a / (2 \pi c)$")
    # plt.title(fr"{title_base}: real(K)")
    
    # f4 = plot2D(plot_X, omega_normalized, np.imag(K_Spol)) # plot bands for reference
    # plt.xlabel(plot_X_label)
    # plt.ylabel("Frequency $\omega a / (2 \pi c)$")
    # plt.title(fr"{title_base}: imag(K)")

    df, df_idx = dbr_instance.getBandEdges(omega=omega, beta=beta, Spol=Spol, plot_X=None, plot_Y=None)
    # df.plot()
    # df_idx.plot()
    # print(df)
    # print(df_idx)
    
    ##### plot using df_idx
    f5=plt.figure()
    fig_list = [f1,f5]
    
    # for fn in [f1,f2,f3,f4,f5]:
    for fn in fig_list:
        plt.figure(fn.number)
        for col in df_idx.columns:
            # idx = np.array(df_idx[col])
            print('col', col)
            idx = df_idx[col]
            idx = idx[~np.isnan(idx)]
            idx = idx.astype(int)
            y = omega_normalized[0, idx]
            
            x_idx = np.argwhere(np.array(~np.isnan(df_idx[col])))
            x_idx = np.squeeze(x_idx)
            x = plot_X[x_idx,0]
            
            print(x.shape, y.shape, x.shape==y.shape)
            
            # plt.plot(x, y)
            plt.scatter(x, y, marker='.', s=1, color='r')
    
    df, df_idx = dbr_instance.getBandEdges(omega=omega, beta=beta, Spol=Spol, plot_X=beta, plot_Y=None)
    df.plot()
    plt.title('df.plot: beta,None')

    # df, df_idx = dbr_instance.getBandEdges(omega=omega, beta=beta, Spol=Spol, plot_X=beta_normalized, plot_Y=None)
    # df.plot()

    df, df_idx = dbr_instance.getBandEdges(omega=omega, beta=beta, Spol=Spol, plot_X=angle_deg, plot_Y=None)
    df.plot()
    plt.title('df.plot: angle_deg,None')

    # df, df_idx = dbr_instance.getBandEdges(omega=omega, beta=beta, Spol=Spol, plot_X=None, plot_Y=omega_normalized)
    # df.plot()

    # df, df_idx = dbr_instance.getBandEdges(omega=omega, beta=beta, Spol=Spol, plot_X=angle_deg, plot_Y=omega_normalized)
    # df.plot()

    # df, df_idx = dbr_instance.getBandEdges(omega=1, beta=1, Spol=True, plot_X=None, plot_Y=None)
    # df.plot()
    # return

    (A,B,C,D) = dbr_instance.getMatrixElements(omega=omega, beta=beta, Spol=Spol)
    cosval = np.abs((1/2)*(A+D))

    df = pd.DataFrame()

    xs = []
    ys = []
    xs_list = []
    ys_list = []
    for slice_idx, plot_X_slice in enumerate(plot_X[:,0]):
        # print(plot_X_slice)
        x = omega_normalized[slice_idx,:]
        y = cosval[slice_idx,:]
        y2 = np.abs(y-1)
        idx = argrelmin(y2)
        r1 = x[idx]
        
        ys = np.append(ys, r1)
        xs = np.append(xs, np.ones_like(r1)*plot_X_slice)
        ys_list.append(r1)
        xs_list.append(np.ones_like(r1)*plot_X_slice)

        col = pd.DataFrame(data=r1, columns=[plot_X_slice])
        df = pd.concat([df, col], axis=1)
    
    df = df.T
    df.columns = [f'band_{i}' for i in df.columns]
    print('===> DATAFRAME')
    print(df)
    print('==============')
    df.plot(style='b.', legend=False, markersize=1)
    plt.title(f'{title_base}: dataframe scatter')

    # df.plot(legend=False, linewidth=1)
    # plt.title(f'{title_base}: dataframe lines')
    # df.plot.scatter(x=df.index)
    # return
    
    # L = [len(i) for i in ys_list]
    # L = np.array(L)
    # Nmax = max(L)
    # print('Nmax:', Nmax)
    # Nmin = min(L)
    # print('Nmin:', Nmin, L.argmin(), plot_X[:,0][L.argmin()])
    
    # print(xs)
    # print(ys)
    # print(xs.shape)
    # print(ys.shape)
    # plt.figure()
    # plt.scatter(xs, ys, marker='.', color='r', s=1)
    # plt.title(f'{title_base}: xs, ys')
    # for fn in fig_list:
    #     plt.figure(fn.number)
    #     plt.scatter(xs, ys, marker='.', color='r', s=1)
    #     plt.axvline(x=plot_X[:,0][L.argmin()])
    #     for i in ys_list[L.argmin()]:
    #         plt.axhline(y=i)

    print('=================================================')
    print('Advanced debugging...')
    for val in [10,40,80]:
        # val = 80
        # val = (n_in*omega/get_c0())*np.sin(np.deg2rad(val))
        # fixed_angle_beta = plot_X[:,0]
        slice_idx = np.abs(plot_X[:,0] - val).argmin()
        plt.figure()
        plt.imshow(plot_X)
        plt.title('plot_X')
        plt.axhline(slice_idx, color='r')
        plt.axvline(0, color='r')
        plot_X_slice = plot_X[:,0][slice_idx]
        # plot_X_slice = plot_X[:,-1][slice_idx]
        print(plot_X.shape)
        expected_beta = (n_in*omega[slice_idx,:]/get_c0())*np.sin(np.deg2rad(val))
        print('val:', val, 'exp_beta:', min(expected_beta), max(expected_beta), 'slice_idx:', slice_idx, 'plot_X_slice:', plot_X_slice)
        
        x = omega_normalized[slice_idx,:]
        y = cosval[slice_idx,:]
        y2 = np.abs(y-1)
        
        plt.figure()
        plt.title(f'val={val}: x,y2')
        plt.plot(x,y2)
        
        plt.figure()
        plt.title(f'val={val}: x,beta')
        plt.plot(x,beta[slice_idx,:])
    return

    # idx = argrelmin(y2)
    # r1 = x[idx]
        
    # ys = np.append(ys, r1)
    # xs = np.append(xs, np.ones_like(r1)*plot_X_slice)
    # ys_list.append(r1)
    # xs_list.append(np.ones_like(r1)*plot_X_slice)

    # col = pd.DataFrame(data=r1, columns=[plot_X_slice])
    # df = pd.concat([df, col], axis=1)

    # plt.figure(f2.number)
    # plt.scatter(xs, ys, marker='.')
    # f3 = plt.figure()
    # plt.plot(y,x) # plot cos val
    # plt.axvline(x=1, color='k', linestyle='--')

    
    # f4 = plt.figure()
    # plt.plot(y2,x) # plot abs(y-1)
    # plt.axvline(x=0, color='k', linestyle='--')
    
    # print(idx)
    # r1 = x[idx]
    # print(r1)
    # for i in r1:
    #     print(i)
    #     plt.axhline(y=i, color='r', linestyle='--')
    
    # f5 = plt.figure()
    # plt.plot(-y2,x) # plot -abs(y-1)
    # plt.axvline(x=0, color='k', linestyle='--')
    # idx, _ = find_peaks(-y2)
    # r2 = x[idx]
    # print(r2)
    # for i in r2:
    #     print(i)
    #     plt.axhline(y=i, color='b', linestyle='--')
    
    # for fn in [f1, f2, f3]:
    #     plt.figure(fn.number)
    #     for i in r2:
    #         plt.axhline(y=i, color='r', linestyle='--')
    
    return

def findBandEdges(dbr_instance=DBR(), Spol=False, n_in = DBR.n1, vs_angle=None, details=False, vs_K_normal=False, pr=None, vs_wavelength=False):

    title_base = fr"Spol={Spol}, $n_{{in}}$={n_in}"

    if pr is None:
        pr = getTestPlottingRanges(vs_angle, vs_K_normal, n_in, dbr_instance)
    
    omega_normalized = pr.fn_2D
    angle_deg = pr.angle_deg_2D
    omega = pr.omega_2D
    beta = pr.beta_2D
    beta_normalized = pr.beta_n_2D

    # define vs_angle based on pr
    if vs_angle is None:
        vs_angle = pr.is_vs_angle()
    
    if vs_angle and not vs_K_normal:
        ##### vs angle
        plot_X = angle_deg
        plot_X_label = r"Incident angle $\theta_{in}$ (degrees)"
    else:
        ##### vs ky
        plot_X = beta_normalized
        plot_X_label = "Wave vector $k_y a/(2\pi)$"

    if vs_wavelength:        
        plot_Y = pr.wvl_2D*1e9
        plot_Y_label = "Wavelength $\lambda_0$ (nm)"
    else:
        plot_Y = pr.fn_2D
        plot_Y_label = "Frequency $\omega a / (2 \pi c)$"
    
    ##### compute values
    K_normal = dbr_instance.getK(omega=omega, beta=beta, Spol=Spol)
    df, df_idx = dbr_instance.getBandEdges(omega=omega, beta=beta, Spol=Spol, plot_X=plot_X, plot_Y=plot_Y)

    ##### create plots
    if not vs_K_normal:
        f1 = plot2D(plot_X, plot_Y, np.isreal(K_normal)) # plot bands for reference
        plt.xlabel(plot_X_label)
        plt.ylabel(plot_Y_label)
        plt.title(fr"{title_base}: isreal(K)")
        df.plot(style='r.', legend=False, markersize=1, ax=plt.gca())
    
        if details:
            f2 = plot2D(plot_X, plot_Y, np.abs(K_normal)) # plot bands for reference
            plt.xlabel(plot_X_label)
            plt.ylabel(plot_Y_label)
            plt.title(fr"{title_base}: abs(K)")
            df.plot(style='r.', legend=False, markersize=1, ax=plt.gca())
            
            f3 = plot2D(plot_X, plot_Y, np.real(K_normal)) # plot bands for reference
            plt.xlabel(plot_X_label)
            plt.ylabel(plot_Y_label)
            plt.title(fr"{title_base}: real(K)")
            df.plot(style='r.', legend=False, markersize=1, ax=plt.gca())
            
            f4 = plot2D(plot_X, plot_Y, np.imag(K_normal)) # plot bands for reference
            plt.xlabel(plot_X_label)
            plt.ylabel(plot_Y_label)
            plt.title(fr"{title_base}: imag(K)")
            df.plot(style='r.', legend=False, markersize=1, ax=plt.gca())
        
    else:
        x = []
        y = []
        for idx,val in np.ndenumerate(K_normal):
            # print(idx, val, np.isreal(val))
            if np.isreal(val):
                x.append( np.real(val) / (2*np.pi/dbr_instance.getPeriod()) )
                y.append( plot_Y[idx] )
        plt.figure()
        plt.scatter(x, y, marker='.', s=1)
        plt.xlabel("Wave vector $k_{normal}$ $a/(2\pi)$")
        plt.ylabel(plot_Y_label)
        plt.title(title_base)
        # plt.figure()
        # plt.imshow(np.isreal(K_normal))
        # plt.colorbar()
        # plt.figure()
        # plt.imshow(np.real(K_normal))
        # plt.colorbar()
        # return
        # plot2D(K_normal, omega_normalized, np.isreal(K_normal)) # plot bands for reference
        # plt.xlabel(plot_X_label)
        # plt.ylabel("Frequency $\omega a / (2 \pi c)$")
        # plt.title(fr"{title_base}: isreal(K)")
        # df.plot(style='r.', legend=False, markersize=1, ax=plt.gca())
        
def testExtremeCases(dbr_instance=DBR()):
    print('-------------------------------')
    beta = [0, 1, dbr_instance.n1*1/get_c0(), dbr_instance.n2*1/get_c0()]
    beta = np.array([beta, beta])
    omega = np.array([[0,0,0,0],[1,1,1,1]])

    for Spol in [True, False]:
        print(f'===> Spol: {Spol}')
        (A,B,C,D) = dbr_instance.getMatrixElements(omega=omega, beta=beta, Spol=Spol)
        for idx,val in np.ndenumerate(omega):
            print(f'omega={omega[idx]}, beta={beta[idx]}:')
            M=[[A[idx],B[idx]], [C[idx],D[idx]]]
            print(M)

def testFillBands():
    x1 = np.array(range(10), dtype=float)
    x2 = x1
    y1 = x1
    y2 = x2**2
    print(x1)
    y2[8] = np.nan
    print(y2)
    plt.plot(x1,y1)
    plt.plot(x2,y2)
    plt.fill_between(x1, y1, y2)

def testPandas():
    beta = np.linspace(25,40,5)
    # IND = None
    IND = beta
    df = pd.DataFrame(index=IND)
    for i in range(len(beta)):
        print(f'---> {i}')
        N = min(len(beta), i+2)
        col = pd.DataFrame(data=i*np.array(range(N)), index=IND[:N], columns=[f'band_{i}'])
        df = pd.concat([df, col], axis=1)
    print(df)
    df.plot()

    df = pd.DataFrame(index=None)
    for i in range(len(beta)):
        print(f'---> {i}')
        # N = min(len(beta), i)
        N = i
        col = pd.DataFrame(data=i*np.array(range(N)), columns=[beta[i]])
        df = pd.concat([df, col], axis=1)
    print(df)
    df = df.T
    print(df)
    df.plot()

def testDataFrameConversion():
    omega_normalized = np.linspace(0, 1.4, 4)
    angle_deg = np.linspace(0, 90, 3)
    omega_normalized, angle_deg = np.meshgrid(omega_normalized, angle_deg)
    print('X', angle_deg)
    print('Y', omega_normalized)
    print('X', angle_deg[:,0])
    print('Y', omega_normalized[0,:])
    
    beta = omega_normalized * angle_deg
    print('beta', beta)
    
    K = np.ones_like(beta)
   #  K = np.random.randint(4,size=(,))
   # K[1,2]=np.nan
    print(K)

def getTestPlottingRanges(vs_angle=True,
                          vs_K_normal=False,
                          n_in=1,
                          dbr_instance=DBR(),
                          Nx=300,
                          Ny=400):
    
    fn = np.linspace(0, 1.4, Ny) # non-zero fn needed to plot vs lambda
    # fn = np.linspace(1e-2, 1.4, 400) # non-zero fn needed to plot vs lambda
    
    if vs_angle and not vs_K_normal:
        ##### vs angle
        pr = plottingRange(fn=fn,
                           angle_deg=np.linspace(0, 90, Nx),
                           n_in=n_in,
                           lattice_constant=dbr_instance.getPeriod())
    else:
        ##### vs ky
        if vs_K_normal:
            beta_normalized = 0
        else:
            beta_normalized = np.linspace(0, n_in*1.4, Nx)

        pr = plottingRange(fn=fn,
                           beta_normalized=beta_normalized,
                           n_in=n_in,
                           lattice_constant=dbr_instance.getPeriod())

    return pr

def reference_DBR_1(Nx=50, Ny=50):
    dbr_instance = DBR()
    pr = getTestPlottingRanges(vs_angle=True,
                               vs_K_normal=False,
                               n_in=dbr_instance.n2,
                               dbr_instance=dbr_instance,
                               Nx=Nx,
                               Ny=Ny)
    return dbr_instance, pr

def reference_DBR_2(Nx=50, Ny=50):
    dbr_instance = DBR()
    dbr_instance.t1 = 0.5
    dbr_instance.t2 = 0.5
    pr = getTestPlottingRanges(vs_angle=True,
                               vs_K_normal=False,
                               n_in=dbr_instance.n2,
                               dbr_instance=dbr_instance,
                               Nx=Nx,
                               Ny=Ny)
    return dbr_instance, pr

def reference_DBR_3(Nx=600,Ny=300):
    dbr_instance = DBR()
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
    dbr_instance.n1 = 2.05
    dbr_instance.n2 = 1.43
    dbr_instance.t1 = 246e-9 #m
    dbr_instance.t2 = 343e-9 #m
    
    pr = plottingRange(wvl=np.linspace(345.038e-9, 1034.95e-9,Ny),
                       # angle_deg = np.linspace(-45,45,Nx),
                       angle_deg = np.linspace(-90,90,Nx),
                       n_in=1,
                       lattice_constant=dbr_instance.getPeriod())

    return (dbr_instance, pr)

def reference_DBR_4(Nx=50,Ny=50):
    """
    DBR for Saleh&Teich figure 7.2-7
    """
    dbr_instance = DBR()
    dbr_instance.n1 = 3.5
    dbr_instance.n2 = 1.5
    dbr_instance.t1 = 0.5
    dbr_instance.t2 = 0.5

    omega_Bragg = dbr_instance.getBraggFrequency()
    custom_fn = np.linspace(0, 2.5, Ny)
    
    omega = custom_fn*omega_Bragg
    fn = omega / (2*np.pi*get_c0()/dbr_instance.a)
    
    pr = plottingRange(fn=fn,
                       angle_deg=np.linspace(0, 90, Nx),
                       n_in=dbr_instance.n2,
                       lattice_constant=dbr_instance.getPeriod())
    
    print(f'n1={dbr_instance.n1}, n2={dbr_instance.n2}')
    print('Brewster angles:', dbr_instance.getBrewsterAngles(degrees=True))
    print('Total internal reflection angle:', np.rad2deg( np.arcsin(dbr_instance.n2/dbr_instance.n1) ) )
    
    return dbr_instance, pr

def test_plottingRange():
  # foo = plottingRange(n_in=12, lattice_constant=34)
  # print(foo)
  # print(foo.angle_deg.shape)

  with warnings.catch_warnings():
    warnings.filterwarnings("error", append=True)

    x = np.array([0,3,4,56,np.inf])
    y = np.array([0,2,3,np.inf])
    with warnings.catch_warnings():
      warnings.filterwarnings("ignore", category=RuntimeWarning, message="divide by zero encountered in true_divide", append=False)
      fn = 34/y

    foo = plottingRange(n_in=12, lattice_constant=34, fn=fn, angle_deg=x)
    print(foo)
    foo.imshow()
    a=foo
    
    foo = plottingRange(n_in=12, lattice_constant=34, wvl=y, angle_deg=x)
    print(foo)
    foo.imshow()
    b=foo
    
    foo = plottingRange(n_in=12, lattice_constant=34, fn=fn, beta_normalized=x)
    print(foo)
    foo.imshow()
    c=foo
    
    foo = plottingRange(n_in=12, lattice_constant=34, wvl=y, beta_normalized=x)
    print(foo)
    foo.imshow()
    d=foo
    
    plt.figure()
    plt.imshow(foo.fn_2D)
    plt.colorbar()
    
    plt.show()
    
    print(a.beta_n_2D)
    print(b.beta_n_2D)
    
    print(c.angle_deg_2D)
    print(d.angle_deg_2D)
    
    print(a.is_vs_angle())
    print(b.is_vs_angle())
    print(c.is_vs_angle())
    print(d.is_vs_angle())
    
  # print(foo.angle_deg)
  # foo = plottingRange(wvl=[1,2,3], beta_normalized=[2,3,4])
  # foo = plottingRange(wvl=[1,2,3], beta_normalized=[2,3,4])
  # foo = plottingRange(wvl=[1,2,3], beta_normalized=[2,3,4])
  
  return

def test_findBandEdges_v1():
    foo = DBR()
    findBandEdges(dbr_instance=foo, vs_K_normal=True, vs_angle=False)
    findBandEdges(dbr_instance=foo, vs_K_normal=False, vs_angle=False)
    findBandEdges(dbr_instance=foo, Spol=True)
    findBandEdges(dbr_instance=foo, Spol=False)
    findBandEdges(dbr_instance=foo, Spol=False, n_in=1)
    findBandEdges(dbr_instance=foo, Spol=False, n_in=foo.n1)
    findBandEdges(dbr_instance=foo, Spol=False, n_in=foo.n2, vs_angle=False)
    findBandEdges(dbr_instance=foo, Spol=False, n_in=foo.n2, vs_angle=True)
    for Spol in [True,False]:
        for n_in in [1,foo.n1,foo.n2]:
            for vs_angle in [False,True]:
                findBandEdges(dbr_instance=foo, Spol=Spol, n_in=n_in, vs_angle=vs_angle)

def test_findBandEdges_v2():
    foo = DBR()
    pr = plottingRange()
    
    pr00 = getTestPlottingRanges(vs_angle=False, vs_K_normal=False, n_in=foo.n1, dbr_instance=foo)
    pr01 = getTestPlottingRanges(vs_angle=False, vs_K_normal=True, n_in=foo.n1, dbr_instance=foo)
    pr10 = getTestPlottingRanges(vs_angle=True, vs_K_normal=False, n_in=foo.n1, dbr_instance=foo)
    pr11 = getTestPlottingRanges(vs_angle=True, vs_K_normal=True, n_in=foo.n1, dbr_instance=foo)

    # pr = pr00
    # pr = pr10
    # print(pr.is_vs_angle())
    # return
    
    # foo.t1 = 0.5
    # foo.t2 = 0.5
    
    # plotDBR(dbr_instance=foo)
    # plotDBR_vs_angle(dbr_instance=foo, n_in=1)
    # plotDBR_vs_angle(dbr_instance=foo, n_in=foo.n1)
    # plotDBR_vs_angle(dbr_instance=foo, n_in=foo.n2)

    # testExtremeCases(dbr_instance=foo)
    # for pr in [pr00,pr01,pr10,pr11]:
    # for Spol in [True, False]:
    #     findBandEdges(dbr_instance=foo, vs_angle=False, vs_K_normal=True, n_in=foo.n1, Spol=Spol, pr=pr01)
    #     findBandEdges(dbr_instance=foo, vs_angle=False, vs_K_normal=False, n_in=foo.n1, Spol=Spol, pr=pr00)
    #     findBandEdges(dbr_instance=foo, vs_angle=True, vs_K_normal=False, n_in=foo.n1, Spol=Spol, pr=pr10)

    # for pr in [pr00,pr01,pr10,pr11]:
    for vs_wavelength in [False]:
        for pr in [pr00,pr10]:
            for Spol in [True, False]:
                # findBandEdges(dbr_instance=foo, vs_K_normal=True, n_in=foo.n1, Spol=Spol, pr=pr)
                findBandEdges(dbr_instance=foo, vs_K_normal=False, n_in=foo.n1, Spol=Spol, pr=pr, vs_wavelength=vs_wavelength)
                    # findBandEdges(dbr_instance=foo, vs_angle=True, vs_K_normal=False, n_in=foo.n1, Spol=Spol, pr=pr10)

def test_reference_DBR_3():
    foo, pr = reference_DBR_3()
    for Spol in [True, False]:
        findBandEdges(dbr_instance=foo, vs_K_normal=False, n_in=1, Spol=Spol, pr=pr, vs_wavelength=True)
        findBandEdges(dbr_instance=foo, vs_K_normal=False, n_in=1, Spol=Spol, pr=pr, vs_wavelength=False)

def test_reference_DBR_4(mode):
    '''
    For *mode*, see: *plotMPB_2D*.
    '''
    # mode = 'k_transverse'
    # mode = 'vs_angle'

    dbr, pr = reference_DBR_4(100, 100)
    # Nperiods = 15
    Nperiods = 30
    # plotTMM(dbr, pr, plot_wvl=False, plot_theory=False)
    scale_factor = (2*np.pi*get_c0()/dbr.a)/dbr.getBraggFrequency()

    # get the bandstructure points
    Xs,Ys,Xp,Yp = plotMPB_2D(dbr, pr, mode, Ny=2)

    fig_list = []
    for Spol in [True, False]:
        if Spol:
            pol = 's'
        else:
            pol = 'p'
        ret = getTMM_for_DBR(dbr, pr, Spol=Spol, Nperiods=Nperiods)

        fig = plot2D(pr.angle_deg_2D, pr.fn_2D*scale_factor, ret['T'])
        plt.xlabel("Angle (degrees)")
        plt.ylabel('$\omega/\omega_{Bragg}$')
        plt.title(f'pol={pol}, Nperiods={Nperiods}+0.5')
        fig.tight_layout()
        fig_list.append(fig)
        print('Xs, Ys data shape:', Xs.shape)
        
        if Spol:
          plt.plot(Xs, Ys, '.')
        else:
          plt.plot(Xp, Yp, '.')
        plt.ylim(0,2.5)

    fig_Spol = fig_list[0]
    fig_Ppol = fig_list[1]
    return fig_Spol, fig_Ppol

def testTMM(Nx=100,Ny=100):
    print('=== reference_DBR_1 ===')
    dbr_instance, pr = reference_DBR_1(Nx,Ny)
    # plt.figure()
    # plt.imshow(pr.beta_n_2D)
    # plt.figure()
    # plt.imshow(pr.angle_deg_2D)
    plotTMM(dbr_instance, pr)
    
    print('=== reference_DBR_2 ===')
    dbr_instance, pr = reference_DBR_2(Nx,Ny)
    plotTMM(dbr_instance, pr)
    
    print('=== reference_DBR_3 ===')
    dbr_instance, pr = reference_DBR_3(Nx,Ny)
    plotTMM(dbr_instance, pr)

def getTMM_for_DBR(dbr_instance, pr, Spol=False, Nperiods = 15):
    '''
    Return transmission/reflection values for a DBR computed using TMM.

    Parameters
    ----------
    dbr_instance : DBR instance
    pr : plottingRange instance
    Spol : Boolean, optional
        DESCRIPTION. S-Polarization if True, P-polarization if False. The default is False.
    Nperiods : Integer, optional
        DESCRIPTION. Number of DBR periods. The default is 15.

    Returns
    -------
    ret : TYPE
        DESCRIPTION.

    '''
    if Spol:
        pol = 's'
    else:
        pol = 'p'

    d_list = [np.inf] + Nperiods*[dbr_instance.t1, dbr_instance.t2] + [dbr_instance.t1] + [np.inf]
    n_list = [pr.n_in] + Nperiods*[dbr_instance.n1, dbr_instance.n2] + [dbr_instance.n1] + [pr.n_in]

    ret = coh_tmm_for_arrays(pol, n_list, d_list, pr.angle_rad_2D, pr.wvl_2D)
    return ret

def plotTMM(dbr_instance, pr, plot_wvl=True, plot_theory=True, Nperiods = 15):
    for Spol in [True, False]:
    
        # pr = plottingRange(wvl=np.linspace(345.038e-9, 1034.95e-9,3),
        #                    angle_deg = np.linspace(-45,45,6),
        #                    n_in=1,
        #                    lattice_constant=dbr_instance.getPeriod())
    
        # print(pr.angle_deg_2D.shape)
        # print(pr.wvl_2D.shape)
        # print(pr.angle_deg_1D)
        # print(pr.wvl_1D)
        # plt.figure()
        # plt.imshow(pr.angle_deg_2D)
        # plt.figure()
        # plt.imshow(pr.wvl_2D)

        # Spol = True
        if Spol:
            pol = 's'
        else:
            pol = 'p'

        ret = getTMM_for_DBR(dbr_instance, pr, Spol=Spol, Nperiods=Nperiods)
    
        # for k,v in ret.items():
        #     # print(k,v)
        #     if k!='pol' and k!='n_list' and k!='d_list':
        #         plt.figure()
        #         plt.imshow(np.real(v))
        #         plt.title(k)
    
        # special handling for nan/inf values
        if plot_wvl:
            fig1 = plot2D(pr.angle_deg_2D, pr.wvl_2D*1e9, ret['T'], yhack=True)
            plt.xlabel("Angle (degrees)")
            plt.ylabel("$\lambda (nm)$")
            plt.title(f'pol={pol}, Nperiods={Nperiods}+0.5')
            fig1.tight_layout()
    
        fig2 = plot2D(pr.angle_deg_2D, pr.fn_2D, ret['T'])
        plt.xlabel("Angle (degrees)")
        plt.ylabel("$a/\lambda$")
        plt.title(f'pol={pol}, Nperiods={Nperiods}+0.5')
        fig2.tight_layout()
    
        # findBandEdges(dbr_instance=dbr_instance, vs_K_normal=False, n_in=1, Spol=Spol, pr=pr, vs_wavelength=True)
        # findBandEdges(dbr_instance=dbr_instance, vs_K_normal=False, n_in=1, Spol=Spol, pr=pr, vs_wavelength=False)

        if plot_theory:
            if plot_wvl:
                df1, df1_idx = dbr_instance.getBandEdges(omega=pr.omega_2D, beta=pr.beta_2D, Spol=Spol,
                                                       plot_X=pr.angle_deg_2D, plot_Y=pr.wvl_2D*1e9)
        
            df2, df2_idx = dbr_instance.getBandEdges(omega=pr.omega_2D, beta=pr.beta_2D, Spol=Spol,
                                                   plot_X=pr.angle_deg_2D, plot_Y=pr.fn_2D)
        
            if plot_wvl:
                plt.figure(fig1)
                df1.plot(style='r.', legend=False, markersize=3, ax=plt.gca())
            plt.figure(fig2)
            df2.plot(style='r.', legend=False, markersize=3, ax=plt.gca())
        
            # pass
            # s = coh_tmm(pol, n_list, d_list, pr.angle_rad_2D[3,2], pr.wvl_2D[3,2])
            # for k,v in s.items():
            #     # print(k,v)
            #     if k!='pol':
            #         # print('--> shape:', k, v.shape)
            #         if v.shape == ():
            #             print(k)

def testParallelPython():
    pass

def coh_tmm_for_arrays(pol, n_list, d_list, th_0, lam_vac):
    '''
    Wrapper around tmm.coh_tmm() to support numpy arrays.
    th_0 and lam_vac must be of the same size/shape
    Note: Unlike coh_tmm, it does not return vw_list, kz_list, th_list.
    TODO: Parallelize the for loop.
    '''
    r = np.ones_like(lam_vac, dtype=np.complex_)*np.nan
    t = np.ones_like(lam_vac, dtype=np.complex_)*np.nan
    R = np.ones_like(lam_vac)*np.nan
    T = np.ones_like(lam_vac)*np.nan
    power_entering = np.ones_like(lam_vac)*np.nan
    
    for idx, val in np.ndenumerate(lam_vac):
        # print('idx', idx)
        scalar_dict = coh_tmm(pol, n_list, d_list, th_0[idx], lam_vac[idx])
        r[idx] = scalar_dict['r']
        t[idx] = scalar_dict['t']
        R[idx] = scalar_dict['R']
        T[idx] = scalar_dict['T']
        power_entering[idx] = scalar_dict['power_entering']
        
    return {'r': r,
            't': t,
            'R': R,
            'T': T,
            'power_entering': power_entering,
            'pol': pol,
            'n_list': n_list,
            'd_list': d_list,
            'th_0': th_0,
            'lam_vac':lam_vac}
    
def testNanxyArrays():
    x = [1,2,3]
    y = [4,5,6,7]
    x,y=np.meshgrid(x,y)
    z = x+y
    plt.pcolormesh(x,y,z)

def showGeometry(ms, init_params=True, periods=1, resolution=32):
    if init_params:
        ms.init_params(p=mp.NO_PARITY, reset_fields=True)
        eps = ms.get_epsilon()
        md = mpb.MPBData(rectify=True, periods=periods, resolution=resolution)
        converted_eps = md.convert(eps)
    # if is1D:
    #     # show geometry 1D
    #     scaley=10
    
    #     # # alternative trick to use imshow on a 1D array
    #     # bob = np.atleast_2d(converted_eps)
        
    #     # simple trick to expand the 1D data along the Y axis
    #     converted_eps,b = np.meshgrid(converted_eps, range(scaley))
        
    # else:
    #     pass
    
    # alternative trick to use imshow on a 1D array
    if len(converted_eps.shape)<=1:
        plt.imshow(np.atleast_2d(converted_eps))#, interpolation='spline36', cmap='binary')
    else:
        plt.imshow(np.atleast_2d(converted_eps).T)#, interpolation='spline36', cmap='binary')
        
    ax = plt.gca()
    ax.set_aspect('auto')

    # plt.ylim([-10,10])
    plt.colorbar()
    # plt.axis('square')
    # plt.axis('off')
    plt.show()

def plotMPB_1D(dbr, pr):

    num_bands = 8
    resolution = 32
    geometry = MPB_getGeometry(dbr)
    
    geometry_lattice_1D = mp.Lattice(size=mp.Vector3(1, 0, 0))

    k_points = [
        mp.Vector3(-0.5),          # M
        mp.Vector3(),               # Gamma
        mp.Vector3(0.5),          # M
    ]
    k_points = mp.interpolate(10, k_points)

    ms_1D = mpb.ModeSolver(
        geometry = geometry,
        geometry_lattice = geometry_lattice_1D,
        k_points = k_points,
        resolution = resolution,
        num_bands = num_bands
    )
    
    plt.title('1D')
    showGeometry(ms_1D)
    plt.title('1D')
    showGeometry(ms_1D, periods=3)

    ms_1D.run_tm()
    # ms.run_tm(mpb.output_at_kpoint(mp.Vector3(-1./3, 1./3), mpb.fix_efield_phase,
    #           mpb.output_efield_z))
    tm_freqs = ms_1D.all_freqs
    tm_gaps = ms_1D.gap_list
    
    ms_1D.run_te()
    te_freqs = ms_1D.all_freqs
    te_gaps = ms_1D.gap_list
    
    x = [k[0] for k in ms_1D.k_points]

    scale_factor = (2*np.pi*get_c0()/dbr.a)/dbr.getBraggFrequency()
    plt.title('1D')
    plt.plot(x, te_freqs*scale_factor )
    plt.ylim([0,2.5])
    plt.xlabel('$k_N^x$')
    plt.ylabel('$\omega/\omega_{Bragg}$')
    # Plot gaps
    ax=plt.gca()
    for gap in te_gaps:
        if gap[0] > 1:
            ax.fill_between(x, gap[1]*scale_factor, gap[2]*scale_factor, color='blue', alpha=0.2)
    
    return

def plotMPB_2D(dbr, pr, mode,
               do_visualize_k_points=True,
               do_plotAngles=True,
               do_PlotOmegaVsAngle=True,
               Nx = 100,
               Ny = 10,
               theta_min_deg=0,
               theta_max_deg=90):
    '''
    The k-point path used will be defined by *mode*.
    *mode* can be one of the following:
        mode = 'fixed_angle' -> computes omega values for a fixed angle theta_deg (=0 by default, i.e. normal incidence, ky=0)
        mode = 'k_transverse' -> k-points will raster-scan over kx in [0,0.5] and ky in [0,0.5], with lines along fixed ky values.
        mode = 'vs_angle' -> k-points will follow fixed angle lines, for angles going from 0 to 90 degrees.
    
    plot resolution settings:
        Ny: Number of interpolated points along kx or along one given angle.
        Nx: Number of interpolated points along ky or between angles.
        theta_min_deg: min angle in degrees when using vs_angle mode
        theta_max_deg: max angle in degrees when using vs_angle mode
    
    do_visualize_k_points: enable or disable k-point visualization.
    do_plotAngles: enable or disable angle plot.
    do_PlotOmegaVsAngle: enable or disable omega/omega_Bragg vs angle plot.

    Returns Xs,Ys,Xp,Yp:
        Xs: Angles in degrees, S polarization
        Ys: omega/omega_Bragg, P polarization
        Xp: Angles in degrees, S polarization
        Yp: omega/omega_Bragg, P polarization

    '''

    # # plot resolution settings
    # Nx = 100
    # Ny = 10
    
    num_bands = 3
    resolution = 32
    geometry = MPB_getGeometry(dbr)
    n_in = pr.n_in

    # theta_max_deg = 70
    theta_deg = 0
    
    a1 = 1
    # a2 = 0.25 # a1 / np.tan(theta_max_rad)
    a2 = 0.10 # a1 / np.tan(theta_max_rad)
    
    b1 = 2*np.pi/a1 # 2pi
    b2 = 2*np.pi/a2
    
    g = b1

    geometry_lattice_2D = mp.Lattice(size=mp.Vector3(1, 1, 0),
                                     basis_size=mp.Vector3(a1, a2, 1))
      
    kmax_x_n, kmax_y_n = getBZedge_k_point(theta_deg, geometry_lattice_2D)
    theta_deg_list = [theta_deg]
    
    if mode == 'fixed_angle':
        k_points = [
            mp.Vector3(0,0),               # Gamma
            mp.Vector3(kmax_x_n,kmax_y_n), # M
        ]
        k_points = mp.interpolate(Ny, k_points)
    elif mode == 'vs_angle':
        k_points_all = []
        theta_deg_list = np.linspace(theta_min_deg, theta_max_deg, Nx)
        for theta_deg in theta_deg_list:
            kmax_x_n, kmax_y_n = getBZedge_k_point(theta_deg, geometry_lattice_2D)
            k_points = [
                mp.Vector3(0, 0),               # Gamma
                # 1e-3*mp.Vector3(kmax_x_n, kmax_y_n), # M
                # 0.5*mp.Vector3(kmax_x_n, kmax_y_n), # M
                mp.Vector3(kmax_x_n, kmax_y_n), # M
            ]
            k_points = mp.interpolate(Ny, k_points)
            k_points_all.extend(k_points)
        k_points = k_points_all
    elif mode == 'k_transverse':
        ky_max = 0.5
        k_points_all = []
        for kx in mp.interpolate(Ny, [0,0.5]):
        # for kx in [0,0.5]:
            k_points = [
                mp.Vector3(kx, 0, 0),    # Gamma
                mp.Vector3(kx, ky_max, 0) # M
            ]
            k_points = mp.interpolate(Nx, k_points)
            k_points_all.extend(k_points)
        k_points = k_points_all
    else:
        raise Exception('Unknown mode.')
        
    ms_2D = mpb.ModeSolver(
        geometry = geometry,
        geometry_lattice = geometry_lattice_2D,
        k_points = k_points,
        resolution = resolution,
        num_bands = num_bands
    )

    x = [k[1]*b2/g for k in ms_2D.k_points]
    xlabel = '$k_y/g$'
    ms_2D.k_points
    print(ms_2D.k_points)
    print()
    kx = np.ones(len(ms_2D.k_points))*np.nan
    ky = np.ones(len(ms_2D.k_points))*np.nan
    angle = np.ones(len(ms_2D.k_points))*np.nan
    print(kx)
    for idx, k in enumerate(ms_2D.k_points):
      kx[idx] = k[0]*b1
      ky[idx] = k[1]*b2
    angle_rad = np.arctan(ky/kx)
    angle_deg = np.rad2deg(angle_rad)
    
    print('============')
    print('angle range (radians):', np.nanmin(angle_rad), np.nanmax(angle_rad))
    print('angle range (degrees):', np.nanmin(angle_deg), np.nanmax(angle_deg))
    print('============')

    ms_2D.run_tm()
    tm_freqs = ms_2D.all_freqs
    tm_gaps = ms_2D.gap_list
    
    ms_2D.run_te()
    te_freqs = ms_2D.all_freqs
    te_gaps = ms_2D.gap_list
    
    # MPB returns omega/(2*pi*c0/a), but we want omega/omega_Bragg
    scale_factor = (2*np.pi*get_c0()/dbr.a)/dbr.getBraggFrequency()

    if do_plotAngles:
        plt.figure()
        plt.title('2D-TM (S)')
        plt.plot(x, tm_freqs*scale_factor, '.')
        plt.xlim([0,1])
        plt.ylim([0,2.5])
        plt.grid()
        plt.xlabel(xlabel)
        plt.ylabel('$\omega/\omega_{Bragg}$')
        
        # Plots straight lines corresponding to angles in an omega/omega_Bragg vs ky/g plot.
        plotAngles(dbr, g, n_in)
        
        # Plot gaps
        ax = plt.gca()
        for gap in tm_gaps:
            if gap[0] > 1:
                ax.fill_between(x, gap[1]*scale_factor, gap[2]*scale_factor, color='blue', alpha=0.2)
        
        plt.figure()
        plt.title('2D-TE (P)')
        plt.plot(x, te_freqs*scale_factor, '.')
        plt.xlim([0,1])
        plt.ylim([0,2.5])
        plt.grid()
        plt.xlabel(xlabel)
        plt.ylabel('$\omega/\omega_{Bragg}$')
    
        # Plots straight lines corresponding to angles in an omega/omega_Bragg vs ky/g plot.
        plotAngles(dbr, g, n_in)
    
        # Plot gaps
        ax = plt.gca()
        for gap in te_gaps:
            if gap[0] > 1:
                ax.fill_between(x, gap[1]*scale_factor, gap[2]*scale_factor, color='red', alpha=0.2)

    #############
    # get Xs, Ys
    fn_custom_array = tm_freqs*scale_factor
    print(angle_deg.shape)
    print(fn_custom_array.shape)
    Nkpoints = fn_custom_array.shape[0]
    Nbands = fn_custom_array.shape[1]
    print(Nkpoints, Nbands)
    angle_deg_new = np.ones_like(fn_custom_array)*np.nan
    print(angle_deg_new.shape)
    for ky_idx, ky_val in enumerate(ky):
      for band_idx in range(Nbands):
        fn_custom = fn_custom_array[ky_idx, band_idx]
        omega = fn_custom * dbr.getBraggFrequency()
        theta_rad = np.arcsin(ky_val*get_c0()/(n_in*omega))
        theta_deg = np.rad2deg(theta_rad)
        angle_deg_new[ky_idx, band_idx] = theta_deg
      
    Xs = angle_deg_new
    Ys = fn_custom_array
    #############
    
    #############
    # get Xp, Yp
    fn_custom_array = te_freqs*scale_factor
    print(angle_deg.shape)
    print(fn_custom_array.shape)
    Nkpoints = fn_custom_array.shape[0]
    Nbands = fn_custom_array.shape[1]
    print(Nkpoints, Nbands)
    angle_deg_new = np.ones_like(fn_custom_array)*np.nan
    print(angle_deg_new.shape)
    for ky_idx, ky_val in enumerate(ky):
      for band_idx in range(Nbands):
        fn_custom = fn_custom_array[ky_idx, band_idx]
        omega = fn_custom * dbr.getBraggFrequency()
        theta_rad = np.arcsin(ky_val*get_c0()/(n_in*omega))
        theta_deg = np.rad2deg(theta_rad)
        angle_deg_new[ky_idx, band_idx] = theta_deg
      
    Xp = angle_deg_new
    Yp = fn_custom_array
    #############
    
    if do_PlotOmegaVsAngle:
        # Plot omega/omega_Bragg vs angle
        plt.figure()
        plt.title('2D-TM (S) - angles based in omega+ky')
        plt.plot(Xs, Ys, '.')
        # plt.xlim([0,1])
        plt.ylim([0,2.5])
        plt.grid()
        plt.xlabel('angle (degrees)')
        plt.ylabel('$\omega/\omega_{Bragg}$')
        # Plot gaps
        ax = plt.gca()
        for gap in te_gaps:
            if gap[0] > 1:
                ax.fill_between(x, gap[1]*scale_factor, gap[2]*scale_factor, color='red', alpha=0.2)
                
        plt.figure()
        plt.title('2D-TE (P) - angles based in omega+ky')
        plt.plot(Xp, Yp, '.')
        # plt.xlim([0,1])
        plt.ylim([0,2.5])
        plt.grid()
        plt.xlabel('angle (degrees)')
        plt.ylabel('$\omega/\omega_{Bragg}$')
        # Plot gaps
        ax = plt.gca()
        for gap in te_gaps:
            if gap[0] > 1:
                ax.fill_between(x, gap[1]*scale_factor, gap[2]*scale_factor, color='red', alpha=0.2)

    print('a1:', a1)
    print('a2:', a2)
    print('b1:', b1)
    print('b2:', b2)
    print('kmax_x_n', kmax_x_n)
    print('kmax_y_n', kmax_y_n)
    print('g/b2', g/b2)
    print('1/b2', 1/b2)
    print('n_in', n_in)
    
    if do_visualize_k_points:
        visualize_k_points(k_points, geometry_lattice_2D, theta_deg_list)
    
    return Xs,Ys,Xp,Yp

def plotMPB_2D_vs_angle(dbr, pr, theta_deg):
    TE=False
    TM=True
    showgeom=False
    
    num_bands = 6
    resolution = 32
    geometry = MPB_getGeometry(dbr)

    # theta_deg = 20
    theta_rad = np.deg2rad(theta_deg)
    
    a1 = 1
    a2 = 0.25
    
    b1 = 2*np.pi/a1 # 2pi
    b2 = 2*np.pi/a2
    
    g = b1 # 2pi (normalization factor for wavevectors)
    
    geometry_lattice_2D = mp.Lattice(size=mp.Vector3(1, 1, 0),
                                     basis_size=mp.Vector3(a1, a2, 1))

    
    theta_critical_rad = np.arctan(b2/b1)
    if theta_rad <= theta_critical_rad:
        kmax_x = g*b1/2 # pi
        kmax = kmax_x / np.cos(theta_rad)
        kmax_y = kmax*np.sin(theta_rad)
    else:
        kmax_y = g*b2/2
        kmax = kmax_y / np.sin(theta_rad)
        kmax_x = kmax*np.cos(theta_rad)
    
    kmax_x_n = kmax_x / (g*b1)
    kmax_y_n = kmax_y / (g*b2)
    
    # k_points_all = []
    # for kx in mp.interpolate(10, [0,0.5]):
    # for kx in [0,0.5]:
    k_points = [
        mp.Vector3(0, 0, 0),    # Gamma
        mp.Vector3(kmax_x_n, kmax_y_n, 0) # M
    ]
    k_points = mp.interpolate(10, k_points)
    # k_points_all.extend(k_points)
    # k_points = k_points_all
    
    ms_2D = mpb.ModeSolver(
        geometry = geometry,
        geometry_lattice = geometry_lattice_2D,
        k_points = k_points,
        resolution = resolution,
        num_bands = num_bands
    )

    if showgeom:
        plt.figure()
        plt.title('2D')
        showGeometry(ms_2D)

    x = range(len(ms_2D.k_points))
    xlabel = '$k_{index}$'
    scale_factor = (2*np.pi*get_c0()/dbr.a)/dbr.getBraggFrequency()
    
    if TE:
        # TE
        ms_2D.run_te()
        te_freqs = ms_2D.all_freqs
        te_gaps = ms_2D.gap_list
        
        plt.figure()
        plt.title(f'$2D-TE, theta={theta_deg}\degree$')
        plt.plot(x, te_freqs*scale_factor, '.')
        plt.ylim([0,2.5])
        plt.xlabel(xlabel)
        plt.ylabel('$\omega/\omega_{Bragg}$')
        # Plot gaps
        ax = plt.gca()
        for gap in te_gaps:
            if gap[0] > 1:
                ax.fill_between(x, gap[1]*scale_factor, gap[2]*scale_factor, color='red', alpha=0.2)    

    if TM:
        # TM
        ms_2D.run_tm()
        tm_freqs = ms_2D.all_freqs
        tm_gaps = ms_2D.gap_list
        
        plt.figure()
        plt.title(f'$2D-TM, theta={theta_deg}\degree$')
        plt.plot(x, tm_freqs*scale_factor, '.')
        plt.ylim([0,2.5])
        plt.xlabel(xlabel)
        plt.ylabel('$\omega/\omega_{Bragg}$')
        # Plot gaps
        ax = plt.gca()
        for gap in tm_gaps:
            if gap[0] > 1:
                ax.fill_between(x, gap[1]*scale_factor, gap[2]*scale_factor, color='blue', alpha=0.2)

    print('kmax:', kmax)
    print('a1:', a1)
    print('a2:', a2)
    print('b1:', b1)
    print('b2:', b2)
    print('kmax_x_n', kmax_x_n)
    print('kmax_y_n', kmax_y_n)
    visualize_k_points(k_points, geometry_lattice_2D, [theta_deg])
    plt.title(f'k-points, $theta={theta_deg}\degree$')

def plotOmegaVsAngle(kx, ky, omega_over_omegaBragg, title_str):
    plt.figure()
    plt.title(title_str)
    plt.plot(angle_deg, te_freqs*scale_factor, '.')
    Xp = angle_deg
    Yp = te_freqs*scale_factor
    # plt.xlim([0,1])
    plt.ylim([0,2.5])
    plt.grid()
    plt.xlabel('angle (degrees)')
    plt.ylabel('$\omega/\omega_{Bragg}$')
    # Plot gaps
    ax = plt.gca()
    for gap in te_gaps:
        if gap[0] > 1:
            ax.fill_between(x, gap[1]*scale_factor, gap[2]*scale_factor, color='red', alpha=0.2)

def plotAngles(dbr, g, n_in):
    '''
    Plots straight lines corresponding to angles in an omega/omega_Bragg vs ky/g plot.
    
        black dashed lines: 0,20,40,60,90 degrees
        black solid lines: Brewster angles for n1->n2 and n2->n1 interfaces.
        red dotted lines: Light cones for n1 and n2.

    Parameters
    ----------
    dbr : DBR instance
    g : 2pi/a
    n_in : refractive index on input side.

    Returns
    -------
    None.

    '''
    # plot angles
    for theta_deg in [0,20,40,60,90]:
      ky_over_g = np.linspace(0,1)
      y = getAngleSlope(dbr, ky_over_g, g, n_in, theta_deg)
      plt.plot(ky_over_g, y, 'k--')
      
    # plot Brewster angles
    (thetaB_1_deg, thetaB_2_deg) = dbr.getBrewsterAngles(degrees=True)
    print("thetaB_1_deg, thetaB_2_deg: ", thetaB_1_deg, thetaB_2_deg)
    for theta_deg in [thetaB_1_deg, thetaB_2_deg]:
      ky_over_g = np.linspace(0,1)
      y = getAngleSlope(dbr, ky_over_g, g, n_in, theta_deg)
      plt.plot(ky_over_g, y, 'k-')

    # plot light cones
    for n in [dbr.n1, dbr.n2]:
      ky_over_g = np.linspace(0,1)
      y = getLightCone(dbr, ky_over_g, g, n)
      plt.plot(ky_over_g, y, 'r:')

def getAngleSlope(dbr, ky_over_g, g, n_in, theta_deg):
  '''
  Returns the values *omega/omega_Bragg* for the given *ky/g* values representing light travelling in a medium of refractive index *n_in*.
  '''
  theta_rad = np.deg2rad(theta_deg)
  ky = ky_over_g * g
  omega = ky * ( (get_c0()/n_in)/np.sin(theta_rad) )
  y = omega/dbr.getBraggFrequency()
  return y

def getLightCone(dbr, ky_over_g, g, n_in):
  ky = ky_over_g * g
  omega = ky * (get_c0()/n_in)
  y = omega/dbr.getBraggFrequency()
  return y

def visualize_k_points(k_points, lat, theta_deg_list=[]):
    '''
    Plots the k_points (scatter plot), the Brillouin zone (solid red line) and optionally lines corresponding to the angles in *theta_deg_list*.
    '''
    b1 = mp.reciprocal_to_cartesian(mp.Vector3(1,0,0), lat)
    b2 = mp.reciprocal_to_cartesian(mp.Vector3(0,1,0), lat)
    b3 = mp.reciprocal_to_cartesian(mp.Vector3(0,0,1), lat)
    
    print('Reciprocal lattice vectors in cartesian coordinates:')
    print('b1/(2*pi):', b1)
    print('b2/(2*pi):', b2)
    print('b3/(2*pi):', b3)

    k_cart = [mp.reciprocal_to_cartesian(kn, lat) for kn in k_points]
        
    # print('k_points', k_points)
    # print('k_cart', k_cart)
    # raise
    
    # x = [kn[0] for kn in k_points]
    # y = [kn[1] for kn in k_points]
    x = [k[0] for k in k_cart]
    y = [k[1] for k in k_cart]
    plt.figure()
    plt.title('k points')
    plt.xlabel('$k_x/(2pi/a)$')
    plt.ylabel('$k_y/(2pi/a)$')
    plt.scatter(x,y)
    ax = plt.gca()
    ax.add_patch(Rectangle((-b1.norm()/2, -b2.norm()/2), b1.norm(), b2.norm(), facecolor='none', edgecolor='r'))
    
    for theta_deg in theta_deg_list:
        # theta_deg = 20
        theta_rad = np.deg2rad(theta_deg)
        L = (b1.norm()/2)/np.cos(theta_rad)
        x = L*np.cos(theta_rad)
        y = L*np.sin(theta_rad)
        if y > b2.norm()/2:
            L = (b2.norm()/2)/np.sin(theta_rad)
            x = L*np.cos(theta_rad)
            y = L*np.sin(theta_rad)
            
        plt.plot([0, x], [0, y], 'k--')
        # print('x:', x)
        # print('y:', y)
        # for k in ms.k_points:
    
    plt.grid()
    return

def getBZedge_k_point(theta_deg, lat):
  '''
  Given a lattice size a1,a2 and an angle theta, return the MPB k-point coordinates of the edge point.
  '''
  b1 = mp.reciprocal_to_cartesian(mp.Vector3(1,0,0), lat)
  b2 = mp.reciprocal_to_cartesian(mp.Vector3(0,1,0), lat)
  b3 = mp.reciprocal_to_cartesian(mp.Vector3(0,0,1), lat)

  # print('Reciprocal lattice vectors in cartesian coordinates:')
  # print('b1/(2*pi):', b1)
  # print('b2/(2*pi):', b2)
  # print('b3/(2*pi):', b3)
  
  # work out the cartesian coordinates
  theta_rad = np.deg2rad(theta_deg)
  L = (b1.norm()/2)/np.cos(theta_rad)
  x = L*np.cos(theta_rad)
  y = L*np.sin(theta_rad)
  if y > b2.norm()/2:
      L = (b2.norm()/2)/np.sin(theta_rad)
      x = L*np.cos(theta_rad)
      y = L*np.sin(theta_rad)
  
  # convert to the reciprocal lattice
  kedge_reciprocal = mp.cartesian_to_reciprocal( mp.Vector3(x, y, 0), lat )
  kx_mpb = kedge_reciprocal[0]
  ky_mpb = kedge_reciprocal[1]
  return kx_mpb, ky_mpb

def plotMPB_hack(dbr, pr):
    
    n1=1.5
    n2=3.5
    
    d1=0.5
    d2=0.5
    
    resolution=64
    num_bands=6
    
    a =d1+d2
    c1 = (d1/2) - (a/2)
    c2 = (a/2) - (d2/2)

    d1n = d1/a
    d2n = d2/a

    c1n = c1/a
    c2n = c2/a

    n_average = ((n1*d1) + (n2*d2))/a
    omega_bragg_normalized = 1 / (2*n_average)
    brewster_angle = np.arctan(n2/n1)

    # a1 = 0.25
    a1 = 0.25
    a2 = 1
    g = 2*np.pi/a2
    b1 = 2*np.pi/a1
    b2 = 2*np.pi/a2
    
    geometry_lattice_2D = mp.Lattice(size=mp.Vector3(1, 1, 0),
                                     basis_size=mp.Vector3(a1, a2, 1))


    block1 = mp.Block(center=mp.Vector3(0, c1n),
             size=mp.Vector3(mp.inf, d1n, mp.inf),
             material=mp.Medium(index=n1))

    block2 = mp.Block(center=mp.Vector3(0, c2n),
             size=mp.Vector3(mp.inf, d2n, mp.inf),
             material=mp.Medium(index=n2))
    
    geometry = [block1, block2]


    k_points_all = []
    # for ky in mp.interpolate(10, [0,0.5]):
    for ky in [0,0.5]:
        k_points = [
            mp.Vector3(0, ky, 0),    # Gamma
            mp.Vector3(g/b1, ky, 0) # M
        ]
        k_points = mp.interpolate(10, k_points)
        k_points_all.extend(k_points)
    
    ms_2D = mpb.ModeSolver(
        geometry = geometry,
        geometry_lattice = geometry_lattice_2D,
        k_points = k_points_all,
        resolution = resolution,
        num_bands = num_bands
    )

    plt.figure()
    plt.title('2D')
    showGeometry(ms_2D)
    # plt.title('2D')
    # showGeometry(ms_2D, periods=5)

    ms_2D.run_tm()
    # ms.run_tm(mpb.output_at_kpoint(mp.Vector3(-1./3, 1./3), mpb.fix_efield_phase,
    #           mpb.output_efield_z))
    tm_freqs = ms_2D.all_freqs
    tm_gaps = ms_2D.gap_list
    
    ms_2D.run_te()
    te_freqs = ms_2D.all_freqs
    te_gaps = ms_2D.gap_list
    
    x = [k[0]*b1/g for k in ms_2D.k_points]
    xlabel = '$k_x/g$'

    scale_factor = (2*np.pi*get_c0()/dbr.a)/dbr.getBraggFrequency()
    
    plt.figure()
    plt.title('2D-TM')
    plt.plot(x, tm_freqs*scale_factor, '.')
    plt.ylim([0,2.5])
    plt.xlabel(xlabel)
    plt.ylabel('$\omega/\omega_{Bragg}$')
    # Plot gaps
    ax = plt.gca()
    for gap in tm_gaps:
        if gap[0] > 1:
            ax.fill_between(x, gap[1]*scale_factor, gap[2]*scale_factor, color='blue', alpha=0.2)
    
    plt.figure()
    plt.title('2D-TE')
    plt.plot(x, te_freqs*scale_factor, '.')
    plt.ylim([0,2.5])
    plt.xlabel(xlabel)
    plt.ylabel('$\omega/\omega_{Bragg}$')
    # Plot gaps
    ax = plt.gca()
    for gap in te_gaps:
        if gap[0] > 1:
            ax.fill_between(x, gap[1]*scale_factor, gap[2]*scale_factor, color='red', alpha=0.2)

def MPB_getGeometry(dbr):
    '''
    Creates a DBR geometry for MEEP/MPB along X, i.e. layers in the YZ plane with X being the transverse/normal direction.
    '''
    block1 = mp.Block(center=mp.Vector3(-dbr.a/2+dbr.t1/2),
             size=mp.Vector3(dbr.t1, mp.inf, mp.inf),
             material=mp.Medium(index=dbr.n1))

    block2 = mp.Block(center=mp.Vector3(dbr.t1/2),
             size=mp.Vector3(dbr.t2, mp.inf, mp.inf),
             material=mp.Medium(index=dbr.n2))
    
    geometry = [block1, block2]
    return geometry

def plotMPB():
    
    # dbr = DBR()
    # dbr.n1 = 1.5
    # dbr.n2 = 3.5
    # dbr.t1 = 0.5
    # dbr.t2 = 1-dbr.t1
    
    dbr, pr = reference_DBR_4(Nx=50,Ny=50)
    
    (thetaB_1_deg, thetaB_2_deg) = dbr.getBrewsterAngles(degrees=True)
    print("thetaB_1_deg, thetaB_2_deg: ", thetaB_1_deg, thetaB_2_deg)
    
    pr = plottingRange(beta_normalized=np.linspace(-0.5,0.5),
                       fn=np.linspace(0,0.30),
                       lattice_constant=dbr.a)
    
    
    # print('==pr==========')
    # print(pr)
    # print('==pr2==========')
    # print(pr2)
    # print('============')
    # return
    
    # plotMPB_1D(dbr, pr)
    plotMPB_2D(dbr, pr)
    # plotMPB_hack(dbr, pr)
    # for i in np.linspace(0,89,10):
    #     plotMPB_2D_vs_angle(dbr, pr, i)
    # plotMPB_2D_vs_angle(dbr, pr, 20)
    # plotMPB_2D_vs_angle(dbr, pr, 30)
    # plotMPB_2D_vs_angle(dbr, pr, 66.8)
    
    return
    
    fig, ax = plt.subplots()
    x = range(len(tm_freqs))
    # Plot bands
    # Scatter plot for multiple y values, see https://stackoverflow.com/a/34280815/2261298
    for xz, tmz, tez in zip(x, tm_freqs, te_freqs):
        ax.scatter([xz]*len(tmz), tmz, color='blue')
        ax.scatter([xz]*len(tez), tez, color='red', facecolors='none')
    ax.plot(tm_freqs, color='blue')
    ax.plot(te_freqs, color='red')
    ax.set_ylim([0, 1])
    ax.set_xlim([x[0], x[-1]])
    
    # Plot gaps
    for gap in tm_gaps:
        if gap[0] > 1:
            ax.fill_between(x, gap[1], gap[2], color='blue', alpha=0.2)
    
    for gap in te_gaps:
        if gap[0] > 1:
            ax.fill_between(x, gap[1], gap[2], color='red', alpha=0.2)
    
    
    # Plot labels
    ax.text(12, 0.04, 'TM bands', color='blue', size=15)
    ax.text(13.05, 0.235, 'TE bands', color='red', size=15)
    
    points_in_between = (len(tm_freqs) - 4) / 3
    tick_locs = [i*points_in_between+i for i in range(4)]
    tick_labs = ['Γ', 'X', 'M', 'Γ']
    ax.set_xticks(tick_locs)
    ax.set_xticklabels(tick_labs, size=16)
    ax.set_ylabel('frequency (c/a)', size=16)
    ax.grid(True)
    
    plt.show()

def MPB_basis_size_test():
  L1 = mp.Lattice(size=mp.Vector3(1, 1, 0))
  L2 = mp.Lattice(size=mp.Vector3(1, 1, 0), basis_size=mp.Vector3(1, 1, 1))
  L3 = mp.Lattice(size=mp.Vector3(1, 1, 0),
                  basis_size=mp.Vector3(np.sqrt(2), np.sqrt(2), np.sqrt(2)),
                  basis1=mp.Vector3(0,1,1),
                  basis2=mp.Vector3(1,0,1),
                  basis3=mp.Vector3(1,1,0))
  
  L4 = mp.Lattice(size=mp.Vector3(1, 1, 0), basis_size=mp.Vector3(1, 0.25, 1))
  
  L=L4
  
  # geometry_lattice_2D = mp.Lattice(size=mp.Vector3(1, 1, 0),
  #                                  basis_size=mp.Vector3(a1, a2))
                                # basis1=mp.Vector3(math.sqrt(3)/2, 0.5),
                                # basis2=mp.Vector3(math.sqrt(3)/2, -0.5))
  
  # geometry_lattice = mp.Lattice(size=mp.Vector3(1, 1),
  #                               basis1=mp.Vector3(math.sqrt(3)/2, 0.5),
  #                               basis2=mp.Vector3(math.sqrt(3)/2, -0.5))

  ms_2D = mpb.ModeSolver(
      geometry = [],
      geometry_lattice = L,
      k_points = [],
      resolution = 32,
      num_bands = 2
  )
  ms_2D.run()
  
  # print(ms_2D.get_lattice())
  # L2 = ms_2D.get_lattice()
  print(mp.reciprocal_to_cartesian(mp.Vector3(1,0,0), L))
  print(mp.reciprocal_to_cartesian(mp.Vector3(0,1,0), L))
  print(mp.reciprocal_to_cartesian(mp.Vector3(0,0,1), L))
  
def testPlot():
  x = np.array([1,2,3,4,5])
  y=np.array([[1,1,1],
              [2,4,8],
              [3,9,27],
              [4,16,30],
              [5,25,50]])
  plt.plot(x, y)
  print(x.shape)
  print(y.shape)
  
def main():
    '''
    Plot TMM bands.
    Plot MPB bands on top. (TODO: As continous lines instead of a scatter plot.)
    Plot theory bands.
    Reference DBR: 4
    '''
    # test_plottingRange()
    # testFillBands()
    # test_plot2D()
    # testPandas()
    # testDataFrameConversion()
    # test_findBandEdges_v1()
    # test_findBandEdges_v2()
    # test_reference_DBR_3()

    # mode = 'fixed_angle'
    # mode = 'k_transverse'
    # mode = 'vs_angle'
    # test_reference_DBR_4('fixed_angle')
    test_reference_DBR_4('k_transverse')
    # test_reference_DBR_4('vs_angle')

    # testPlot()
    # testTMM()
    # testParallelPython()
    # testNanxyArrays()
    # plotMPB()
    # MPB_basis_size_test()

    # dbr, pr = reference_DBR_4()
    # print(pr)
    # print(min(pr.wvl_1D), max(pr.wvl_1D))
    # print(min(pr.fn_1D), max(pr.fn_1D))

    plt.show()
    print('SUCCESS')

if __name__ == "__main__":
    main()
