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

    def getBrewsterAngles(self, degrees=False):
        thetaB_1_rad = np.arctan(self.n2/self.n1)
        thetaB_2_rad = np.arctan(self.n1/self.n2)
        if degrees:
            thetaB_1_deg = np.rad2deg(thetaB_1_rad)
            thetaB_2_deg = np.rad2deg(thetaB_2_rad)
            return (thetaB_1_deg, thetaB_2_deg)
        else:
            return (thetaB_1_rad, thetaB_2_rad)

    def getMatrixElements(self, omega=1, beta=1, Spol=True):
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
        return(A, B, C, D)

    def getK(self, omega=1, beta=1, Spol=True):
        # convert to array (in case a list is passed)
        omega = np.array(omega)
        beta = np.array(beta)
        (A,B,C,D) = self.getMatrixElements(omega=omega, beta=beta, Spol=Spol)
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
    
    K_Spol = foo.getK(omega=Y, beta=X, Spol=True)
    plot2D(XN, YN, np.isreal(K_Spol))
    plt.xlabel("Wave vector $k_y a/(2\pi)$")
    plt.ylabel("Frequency $\omega a / (2 \pi c)$")
    plt.title("S polarization")

    K_Ppol = foo.getK(omega=Y, beta=X, Spol=False)
    plot2D(XN, YN, np.isreal(K_Ppol))
    plt.xlabel("Wave vector $k_y a/(2\pi)$")
    plt.ylabel("Frequency $\omega a / (2 \pi c)$")
    plt.title("P polarization")
    
    (thetaB_1_rad, thetaB_2_rad) = foo.getBrewsterAngles(degrees=False)
    
    slope = 1 / ( foo.n1 * np.sin( thetaB_1_rad ) )
    plt.plot(beta_normalized, slope*beta_normalized, 'r-', label=r'$slope = 1/(n_1*sin(\theta_{B1}))$')

    slope = 1
    plt.plot(beta_normalized, slope*beta_normalized, 'k--', label='$slope = 1$')

    slope = 1/foo.n1
    plt.plot(beta_normalized, slope*beta_normalized, 'g:', label='$slope = 1/n_1$')

    slope = 1/foo.n2
    plt.plot(beta_normalized, slope*beta_normalized, 'b:', label='$slope = 1/n_2$')

    plt.legend()

def plotDBR_vs_angle(n_in = DBR.n1):
    
    foo = DBR()
    
    omega_normalized = np.linspace(0, 1.4, 300)
    angle_deg = np.linspace(0, 90, 300)

    omega_normalized, angle_deg = np.meshgrid(omega_normalized, angle_deg)

    omega = omega_normalized * (2*np.pi*get_c0()/foo.getPeriod())
        
    angle_rad = np.deg2rad(angle_deg)

    beta = (omega*n_in/get_c0()) * np.sin(angle_rad)
    beta_normalized = beta / (2*np.pi/foo.getPeriod())
    
    K_Spol = foo.getK(omega=omega, beta=beta, Spol=True)
    plot2D(angle_deg, omega_normalized, np.isreal(K_Spol))
    plt.xlabel(r"Incident angle $\theta_{in}$ (degrees)")
    plt.ylabel(r"Frequency $\omega a / (2 \pi c)$")
    plt.title(fr"S polarization, $n_{{in}} = {n_in}$")

    K_Ppol = foo.getK(omega=omega, beta=beta, Spol=False)
    plot2D(angle_deg, omega_normalized, np.isreal(K_Ppol))
    plt.xlabel(r"Incident angle $\theta_{in}$ (degrees)")
    plt.ylabel(r"Frequency $\omega a / (2 \pi c)$")
    plt.title(fr"P polarization, $n_{{in}} = {n_in}$")
    
    (thetaB_1_deg, thetaB_2_deg) = foo.getBrewsterAngles(degrees=True)
    plt.axvline(x = thetaB_1_deg, color = 'r', label = r'$\theta_{B1}$')
    plt.axvline(x = thetaB_2_deg, color = 'b', label = r'$\theta_{B2}$')

    plt.axvline(x = np.rad2deg(np.arcsin(foo.n1/foo.n2)), color = 'k', label = r'$\theta_C$')
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
    
def main():
    plotDBR()
    plotDBR_vs_angle(n_in=1)
    plotDBR_vs_angle(n_in=DBR.n1)
    plotDBR_vs_angle(n_in=DBR.n2)
    plt.show()

if __name__ == "__main__":
    main()
