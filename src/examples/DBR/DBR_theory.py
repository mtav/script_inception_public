#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from constants.physcon import get_c0
import matplotlib.pyplot as plt
import warnings

class DBR():
    n1 = np.sqrt(2)
    n2 = np.sqrt(13)
    t1 = n2/(n1+n2)
    t2 = n1/(n1+n2)

    def getMatrixElements_Spol(self, omega=1,beta=1):
        n1 = self.n1
        n2 = self.n2
        a = self.t1
        b = self.t2
        
        # convert to array (in case a list is passed)
        omega = np.array(omega)
        beta = np.array(beta)
        
        k1x = np.sqrt( (n1*omega/get_c0())**2 - beta**2 + 0j)
        k2x = np.sqrt( (n2*omega/get_c0())**2 - beta**2 + 0j)
        
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=RuntimeWarning, message="invalid value encountered in true_divide")
            u = k2x/k1x
            v = k1x/k2x
        
        A = np.exp( 1j*k1x*a) * ( np.cos(k2x*b) + (1/2)*1j*(u + v)*np.sin(k2x*b) )
        B = np.exp(-1j*k1x*a) * ( ( 1/2)*1j*(u - v)*np.sin(k2x*b) )
        C = np.exp( 1j*k1x*a) * ( (-1/2)*1j*(u - v)*np.sin(k2x*b) )
        D = np.exp(-1j*k1x*a) * ( np.cos(k2x*b) - (1/2)*1j*(u + v)*np.sin(k2x*b) )
        return(A, B, C, D)

    def getMatrixElements_Ppol(self, omega=1,beta=1):
        n1 = self.n1
        n2 = self.n2
        a = self.t1
        b = self.t2
        
        # convert to array (in case a list is passed)
        omega = np.array(omega)
        beta = np.array(beta)
        
        k1x = np.sqrt( (n1*omega/get_c0())**2 - beta**2 + 0j)
        k2x = np.sqrt( (n2*omega/get_c0())**2 - beta**2 + 0j)
        
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=RuntimeWarning, message="invalid value encountered in true_divide")
            u = (pow(n2,2)*k1x) / (pow(n1,2)*k2x)
            v = (pow(n1,2)*k2x) / (pow(n2,2)*k1x)
        
        A = np.exp( 1j*k1x*a) * ( np.cos(k2x*b) + (1/2)*1j*(u + v)*np.sin(k2x*b) )
        B = np.exp(-1j*k1x*a) * ( ( 1/2)*1j*(u - v)*np.sin(k2x*b) )
        C = np.exp( 1j*k1x*a) * ( (-1/2)*1j*(u - v)*np.sin(k2x*b) )
        D = np.exp(-1j*k1x*a) * ( np.cos(k2x*b) - (1/2)*1j*(u + v)*np.sin(k2x*b) )
        return(A, B, C, D)

    def getK_Spol(self, omega=1,beta=1):
        # convert to array (in case a list is passed)
        omega = np.array(omega)
        beta = np.array(beta)
        (A,B,C,D) = self.getMatrixElements_Spol(omega=omega, beta=beta)
        K = (1/self.getPeriod())*np.arccos((1/2)*(A+D))
        return K

    def getK_Ppol(self, omega=1,beta=1):
        # convert to array (in case a list is passed)
        omega = np.array(omega)
        beta = np.array(beta)
        (A,B,C,D) = self.getMatrixElements_Ppol(omega=omega, beta=beta)
        K = (1/self.getPeriod())*np.arccos((1/2)*(A+D))
        return K

    def getPeriod(self):
        period = self.t1 + self.t2
        return period

def plot2D(x,y,z):
    # z_min, z_max = -abs(z).max(), abs(z).max()
    
    fig = plt.figure()
    # c = plt.pcolormesh(x, y, z, cmap='RdBu', vmin=z_min, vmax=z_max, shading='gouraud')
    c = plt.pcolormesh(x, y, z, shading='gouraud')
    fig.colorbar(c)
        
    fig.tight_layout()
    #plt.show()

def test_plot2D():
    x = np.linspace(-10,10,100)
    y = np.linspace(-5,5,200)
    Y, X = np.meshgrid(y, x)
    # X, Y = np.meshgrid(x, y)
    R = np.ones(X.shape)
    R = np.exp( -( (X**2 + Y**2 ) / (2**2)) )
    plot2D(X, Y, R)
    plt.show()
    print(R.shape)

def plotDBR():
    foo = DBR()
    omega_normalized = np.linspace(0, 1.4, 300)
    beta_normalized = np.linspace(0, 1, 200)
    omega = omega_normalized * (2*np.pi*get_c0()/foo.getPeriod())
    beta = beta_normalized * (2*np.pi/foo.getPeriod())
    
    Y, X = np.meshgrid(omega, beta)
    YN, XN = np.meshgrid(omega_normalized, beta_normalized)
    
    K_Spol = foo.getK_Spol(omega=Y, beta=X)
    plot2D(XN, YN, np.isreal(K_Spol))
    plt.xlabel("Wave vector $k_y a/(2\pi)$")
    plt.ylabel("Frequency $\omega a / (2 \pi c)$")
    plt.title("S polarization")

    K_Ppol = foo.getK_Ppol(omega=Y, beta=X)
    plot2D(XN, YN, np.isreal(K_Ppol))
    plt.xlabel("Wave vector $k_y a/(2\pi)$")
    plt.ylabel("Frequency $\omega a / (2 \pi c)$")
    plt.title("P polarization")
    
    slope = 1 / ( foo.n1 * np.sin( np.arctan(foo.n2/foo.n1) ) )
    plt.plot(beta_normalized, slope*beta_normalized, 'r-')

    slope = 1
    plt.plot(beta_normalized, slope*beta_normalized, 'k--')

    slope = 1/foo.n1
    plt.plot(beta_normalized, slope*beta_normalized, 'g:')

    slope = 1/foo.n2
    plt.plot(beta_normalized, slope*beta_normalized, 'b:')
        
def main():
    # test_plot2D()
    plotDBR()

if __name__ == "__main__":
    main()
