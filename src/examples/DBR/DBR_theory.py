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

    def getBrewsterAngles(self, degrees=False):
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
    # ##### Public attributes (fundamental)
    # wvl_1D = None
    # angle_deg_1D = None
    # beta_vacuum_1D = None
    
    # lattice_constant = None
    # n_in = None
    
    # ##### Private variables (computed when update is called).
    # ##### They are all 2D
    # __wvl = None
    # __angle_deg = None
    # __beta_vacuum = None # beta in vacuum
    
    # __wvl_n = None       # normalized wavelength
    # __f_n = None         # normalized f and omega f_n = omega_n = (a/lambda)
    # __f = None
    # __omega = None
    
    # __angle_rad = None
    # __beta = None        # beta in material
    # __beta_n = None      # normalized beta

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
    def fn_1D(self): return self.__fn_1D
    @property
    def fn_2D(self): return self.__fn_2D
    @property
    def wvl_1D(self):
      with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=RuntimeWarning, message="divide by zero encountered in true_divide", append=False)
        return self.__lattice_constant / self.__fn_1D
    @property
    def wvl_2D(self):
      with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=RuntimeWarning, message="divide by zero encountered in true_divide", append=False)
        return self.__lattice_constant / self.__fn_2D
    @property
    def omega_1D(self): return (2*np.pi*get_c0()/self.__lattice_constant)*self.__fn_1D
    @property
    def omega_2D(self): return (2*np.pi*get_c0()/self.__lattice_constant)*self.__fn_2D
    
    # @property
    # def wvl(self): return self.__wvl
    # @property
    # def angle_deg(self): return self.__angle_deg
    # @property
    # def beta_vacuum(self): return self.__beta_vacuum
    # @property
    # def f(self): return get_c0()/self.__wvl
    # @property
    # def omega(self): return 2*np.pi*get_c0()/self.__wvl
    # @property
    # def angle_rad(self): return self.__angle_rad
    # @property
    # def beta(self): return self.__beta
    # @property
    # def beta_n(self): return self.__beta_n
    
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
        print('==> X = beta_n_1D')
        self.__fn_2D, self.__beta_n_2D = np.meshgrid(self.__fn_1D, self.__beta_n_1D)
        
        with warnings.catch_warnings():
          warnings.filterwarnings("ignore", category=RuntimeWarning, message="divide by zero encountered in true_divide", append=False)
          warnings.filterwarnings("ignore", category=RuntimeWarning, message="invalid value encountered in true_divide", append=False)
          warnings.filterwarnings("ignore", category=RuntimeWarning, message="invalid value encountered in arcsin", append=False)
          self.__angle_deg_2D = np.rad2deg( np.arcsin( self.__beta_n_2D / (self.__n_in * self.__fn_2D) ) )
        
        # omega_normalized = np.linspace(0, 1.4, 300)
        # if vs_K_normal:
        #     beta_normalized = 0
        # else:
        #     beta_normalized = np.linspace(0, n_in*1.4, 200)

        # omega = omega_normalized * (2*np.pi*get_c0()/dbr_instance.getPeriod())
        # beta = beta_normalized * (2*np.pi/dbr_instance.getPeriod())

        # plot_X = beta_normalized
        # plot_X_label = "Wave vector $k_y a/(2\pi)$"

      elif self.__angle_deg_1D is not None:
        print('==> X = angle_deg_1D')
        self.__fn_2D, self.__angle_deg_2D = np.meshgrid(self.__fn_1D, self.__angle_deg_1D)

        with warnings.catch_warnings():
          warnings.filterwarnings("ignore", category=RuntimeWarning, message="invalid value encountered in multiply", append=False)
          warnings.filterwarnings("ignore", category=RuntimeWarning, message="invalid value encountered in sin", append=False)
          self.__beta_n_2D = self.__n_in * self.__fn_2D * np.sin( np.deg2rad(self.__angle_deg_2D) )
        
        # omega_normalized = np.linspace(0, 1.4, 400)
        # angle_deg = np.linspace(0, 90, 300)
        # omega_normalized, angle_deg = np.meshgrid(omega_normalized, angle_deg)

        # omega = omega_normalized * (2*np.pi*get_c0()/dbr_instance.getPeriod())
        
        # angle_rad = np.deg2rad(angle_deg)
        # beta = (omega*n_in/get_c0()) * np.sin(angle_rad)
        # beta_normalized = beta / (2*np.pi/dbr_instance.getPeriod())
    
        # plot_X = angle_deg
        # plot_X_label = r"Incident angle $\theta_{in}$ (degrees)"
      else:
        raise

        # with warnings.catch_warnings():
        #     warnings.filterwarnings("ignore", category=RuntimeWarning, message="invalid value encountered in true_divide", append=True)
        #     warnings.filterwarnings("ignore", category=RuntimeWarning, message="divide by zero encountered in true_divide", append=True)
        #     warnings.filterwarnings("ignore", category=RuntimeWarning, message="invalid value encountered in cdouble_scalars", append=True)
        #     warnings.filterwarnings("ignore", category=RuntimeWarning, message="divide by zero encountered in cdouble_scalars", append=True)
        #     warnings.filterwarnings("error", append=True)

      # self.__f = get_c0()/self.__wvl
      # self.__omega = 2*np.pi*get_c0()/self.__wvl
      # self.__wvl_n = self.__wvl / self.lattice_constant
      # self.__f_n = self.lattice_constant / self.__wvl


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
    
    # def setWavelength(self, wvl):
    #   # self.omega_normalized = self.lattice_constant / wvl
    #   self.wvl = wvl

    # def setOmegaNormalized(self, fn):
    #   self.wvl = self.lattice_constant / fn

    # def setBetaNormalized(self, beta_normalized):
    #   angle_rad = np.arcsin( beta_normalized / (self.n_in*self.omega_normalized) )
    #   self.angle_deg = np.rad2deg(angle_rad)
    
    # def getWavelength():
    #   # wvl = self.lattice_constant / self.omega_normalized
    #   return self.wvl
    
    # def getOmega(self):
    #   omega = self.omega_normalized * (2*np.pi*get_c0()/self.lattice_constant)
    #   return omega
    
    # def getAngleRad(self):
    #   angle_rad = np.deg2rad(self.angle_deg)
    #   return angle_rad
      
    # def getBeta(self):
    #   beta = (omega*self.n_in/get_c0()) * np.sin(self.getAngleRad())
    #   return beta
    
    # def getBetaNormalized(self):
    #   beta_normalized = self.getBeta() / (2*np.pi/self.lattice_constant)
    #   return beta_normalized

def plot2D(x,y,z):
    # z_min, z_max = -abs(z).max(), abs(z).max()
    
    fig = plt.figure()
    # c = plt.pcolormesh(x, y, z, cmap='RdBu', vmin=z_min, vmax=z_max, shading='gouraud')
    c = plt.pcolormesh(x, y, z, shading='gouraud')
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

def findBandEdges(dbr_instance=DBR(), Spol=False, n_in = DBR.n1, vs_angle=False, details=False, vs_K_normal=False):

    title_base = fr"Spol={Spol}, $n_{{in}}$={n_in}"

    if vs_angle and not vs_K_normal:
        ##### vs angle
        omega_normalized = np.linspace(0, 1.4, 400)
        angle_deg = np.linspace(0, 90, 300)
        
        pr = plottingRange(fn=omega_normalized, angle_deg=angle_deg, n_in=n_in)
        omega_normalized = pr.fn_2D
        angle_deg = pr.angle_deg_2D
        omega = pr.omega_2D
        beta = pr.beta_2D
        beta_normalized = pr.beta_n_2D
        
        # omega_normalized, angle_deg = np.meshgrid(omega_normalized, angle_deg)

        # omega = omega_normalized * (2*np.pi*get_c0()/dbr_instance.getPeriod())
        
        # angle_rad = np.deg2rad(angle_deg)
        # beta = (omega*n_in/get_c0()) * np.sin(angle_rad)
        # beta_normalized = beta / (2*np.pi/dbr_instance.getPeriod())
    
        plot_X = angle_deg
        plot_X_label = r"Incident angle $\theta_{in}$ (degrees)"
    else:
        ##### vs ky
        omega_normalized = np.linspace(0, 1.4, 300)
        if vs_K_normal:
            beta_normalized = 0
        else:
            beta_normalized = np.linspace(0, n_in*1.4, 200)

        pr = plottingRange(fn=omega_normalized, beta_normalized=beta_normalized, n_in=n_in)
        omega_normalized = pr.fn_2D
        angle_deg = pr.angle_deg_2D
        omega = pr.omega_2D
        beta = pr.beta_2D
        beta_normalized = pr.beta_n_2D

        # omega_normalized, beta_normalized = np.meshgrid(omega_normalized, beta_normalized)

        # omega = omega_normalized * (2*np.pi*get_c0()/dbr_instance.getPeriod())
        # beta = beta_normalized * (2*np.pi/dbr_instance.getPeriod())

        plot_X = beta_normalized
        plot_X_label = "Wave vector $k_y a/(2\pi)$"
        
    ##### compute values
    K_normal = dbr_instance.getK(omega=omega, beta=beta, Spol=Spol)
    df, df_idx = dbr_instance.getBandEdges(omega=omega, beta=beta, Spol=Spol, plot_X=plot_X, plot_Y=omega_normalized)

    ##### create plots
    if not vs_K_normal:
        f1 = plot2D(plot_X, omega_normalized, np.isreal(K_normal)) # plot bands for reference
        plt.xlabel(plot_X_label)
        plt.ylabel("Frequency $\omega a / (2 \pi c)$")
        plt.title(fr"{title_base}: isreal(K)")
        df.plot(style='r.', legend=False, markersize=1, ax=plt.gca())
    
        if details:
            f2 = plot2D(plot_X, omega_normalized, np.abs(K_normal)) # plot bands for reference
            plt.xlabel(plot_X_label)
            plt.ylabel("Frequency $\omega a / (2 \pi c)$")
            plt.title(fr"{title_base}: abs(K)")
            df.plot(style='r.', legend=False, markersize=1, ax=plt.gca())
            
            f3 = plot2D(plot_X, omega_normalized, np.real(K_normal)) # plot bands for reference
            plt.xlabel(plot_X_label)
            plt.ylabel("Frequency $\omega a / (2 \pi c)$")
            plt.title(fr"{title_base}: real(K)")
            df.plot(style='r.', legend=False, markersize=1, ax=plt.gca())
            
            f4 = plot2D(plot_X, omega_normalized, np.imag(K_normal)) # plot bands for reference
            plt.xlabel(plot_X_label)
            plt.ylabel("Frequency $\omega a / (2 \pi c)$")
            plt.title(fr"{title_base}: imag(K)")
            df.plot(style='r.', legend=False, markersize=1, ax=plt.gca())
        
    else:
        x = []
        y = []
        for idx,val in np.ndenumerate(K_normal):
            # print(idx, val, np.isreal(val))
            if np.isreal(val):
                x.append( np.real(val) / (2*np.pi/dbr_instance.getPeriod()) )
                y.append( omega_normalized[idx] )
        plt.figure()
        plt.scatter(x, y, marker='.', s=1)
        plt.xlabel("Wave vector $k_{normal}$ $a/(2\pi)$")
        plt.ylabel("Frequency $\omega a / (2 \pi c)$")
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

def reference_DBR():
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
    
    wvl_min_nm = 345.038
    wvl_max_nm = 1034.95
    pr = plottingRange(wvl=np.linspace(wvl_min_nm, wvl_max_nm),
                       angle_deg = np.linspace(0,45,100),
                       n_in=1,
                       lattice_constant=dbr_instance.getPeriod())

    return (dbr_instance, pr)

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
    
    foo = plottingRange(n_in=12, lattice_constant=34, wvl=y, angle_deg=x)
    print(foo)
    foo.imshow()
    
    foo = plottingRange(n_in=12, lattice_constant=34, fn=fn, beta_normalized=x)
    print(foo)
    foo.imshow()
    a=foo
    
    foo = plottingRange(n_in=12, lattice_constant=34, wvl=y, beta_normalized=x)
    print(foo)
    foo.imshow()
    b=foo
    
    plt.figure()
    plt.imshow(foo.fn_2D)
    plt.colorbar()
    
    plt.show()
    
    print(a.angle_deg_2D)
    print(b.angle_deg_2D)
    
  # print(foo.angle_deg)
  # foo = plottingRange(wvl=[1,2,3], beta_normalized=[2,3,4])
  # foo = plottingRange(wvl=[1,2,3], beta_normalized=[2,3,4])
  # foo = plottingRange(wvl=[1,2,3], beta_normalized=[2,3,4])
  
  return

def main():
    # test_plottingRange()
    # return
    # testFillBands()
    # test_plot2D()
    # testPandas()
    # testDataFrameConversion()
    # return
    
    foo = DBR()
    pr = plottingRange()
    
    # foo, pr = reference_DBR()
    # foo.t1 = 0.5
    # foo.t2 = 0.5
    
    # plotDBR(dbr_instance=foo)
    # plotDBR_vs_angle(dbr_instance=foo, n_in=1)
    # plotDBR_vs_angle(dbr_instance=foo, n_in=foo.n1)
    # plotDBR_vs_angle(dbr_instance=foo, n_in=foo.n2)

    # testExtremeCases(dbr_instance=foo)
    for Spol in [True, False]:
        findBandEdges(dbr_instance=foo, vs_K_normal=True, vs_angle=False, n_in=foo.n1, Spol=Spol)
        findBandEdges(dbr_instance=foo, vs_K_normal=False, vs_angle=False, n_in=foo.n1, Spol=Spol)
        findBandEdges(dbr_instance=foo, vs_K_normal=False, vs_angle=True, n_in=foo.n1, Spol=Spol)
    # findBandEdges(dbr_instance=foo, vs_K_normal=True, vs_angle=False)
    # findBandEdges(dbr_instance=foo, vs_K_normal=False, vs_angle=False)
    # findBandEdges(dbr_instance=foo, Spol=True)
    # findBandEdges(dbr_instance=foo, Spol=False)
    # findBandEdges(dbr_instance=foo, Spol=False, n_in=1)
    # findBandEdges(dbr_instance=foo, Spol=False, n_in=foo.n1)
    # findBandEdges(dbr_instance=foo, Spol=False, n_in=foo.n2, vs_angle=False)
    # findBandEdges(dbr_instance=foo, Spol=False, n_in=foo.n2, vs_angle=True)
    # for Spol in [True,False]:
    #     for n_in in [1,foo.n1,foo.n2]:
    #         for vs_angle in [False,True]:
    #             findBandEdges(dbr_instance=foo, Spol=Spol, n_in=n_in, vs_angle=vs_angle)
    # plotOmegaVsKz()
    plt.show()

if __name__ == "__main__":
    main()
