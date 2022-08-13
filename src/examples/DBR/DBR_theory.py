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
            
        ##### when k1x=k2x=0, A=D=1 and B=C=0
        for idx, val in np.ndenumerate(omega):
            if k1x[idx]==0 and k2x[idx]==0:
                A[idx] = 1
                B[idx] = 0
                C[idx] = 0
                D[idx] = 1
                
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
    
    # def getBandEdges(self, omega_min=1, omega_max=, beta=1, Spol=True):
    #     return xs,

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

def findBandEdges(dbr_instance=DBR(), Spol=True):
    omega_normalized = np.linspace(0, 1.4, 300)
    beta_normalized = np.linspace(0, 1, 200)

    omega_normalized, beta_normalized = np.meshgrid(omega_normalized, beta_normalized)

    omega = omega_normalized * (2*np.pi*get_c0()/dbr_instance.getPeriod())
    beta = beta_normalized * (2*np.pi/dbr_instance.getPeriod())

    K_Spol = dbr_instance.getK(omega=omega, beta=beta, Spol=Spol)

    f1 = plot2D(beta_normalized, omega_normalized, np.isreal(K_Spol)) # plot bands for reference
    plt.xlabel("Wave vector $k_y a/(2\pi)$")
    plt.ylabel("Frequency $\omega a / (2 \pi c)$")
    plt.title(f"Spol={Spol}")
    # plt.axvline(x=beta_normalized_slice, color='r')

    f2 = plot2D(beta_normalized, omega_normalized, np.abs(K_Spol)) # plot bands for reference
    plt.xlabel("Wave vector $k_y a/(2\pi)$")
    plt.ylabel("Frequency $\omega a / (2 \pi c)$")
    plt.title(f"Spol={Spol}: abs(K)")
    
    f3 = plot2D(beta_normalized, omega_normalized, np.real(K_Spol)) # plot bands for reference
    plt.xlabel("Wave vector $k_y a/(2\pi)$")
    plt.ylabel("Frequency $\omega a / (2 \pi c)$")
    plt.title(f"Spol={Spol}: real(K)")
    
    f4 = plot2D(beta_normalized, omega_normalized, np.imag(K_Spol)) # plot bands for reference
    plt.xlabel("Wave vector $k_y a/(2\pi)$")
    plt.ylabel("Frequency $\omega a / (2 \pi c)$")
    plt.title(f"Spol={Spol}: imag(K)")

    (A,B,C,D) = dbr_instance.getMatrixElements(omega=omega, beta=beta, Spol=Spol)
    cosval = np.abs((1/2)*(A+D))

    # f2 = plot2D(beta_normalized, omega_normalized, np.isclose(cosval,1, atol=6e-2)) # plot values close to 1
    # plt.axvline(x=beta_normalized_slice, color='r')

    df = pd.DataFrame()

    xs = []
    ys = []
    xs_list = []
    ys_list = []
    for beta_normalized_slice_idx, beta_normalized_slice in enumerate(beta_normalized[:,0]):
        # beta_normalized_slice = 0.6
        # beta_normalized_slice_idx = np.abs(beta_normalized[:,0] - beta_normalized_slice).argmin()
            
        x = omega_normalized[beta_normalized_slice_idx,:]
        y = cosval[beta_normalized_slice_idx,:]
        y2 = np.abs(y-1)
        idx = argrelmin(y2)
        r1 = x[idx]
        
        ys = np.append(ys, r1)
        xs = np.append(xs, np.ones_like(r1)*beta_normalized_slice)
        ys_list.append(r1)
        xs_list.append(np.ones_like(r1)*beta_normalized_slice)

        col = pd.DataFrame(data=r1, columns=[beta_normalized_slice])
        df = pd.concat([df, col], axis=1)

        # print(y.shape)
        # print(y)
    
    df = df.T
    df.columns = [f'band_{i}' for i in df.columns]
    print('===> DATAFRAME')
    print(df)
    print('==============')
    df.plot(style='b.', legend=False, markersize=1)
    plt.title('dataframe scatter')

    df.plot(legend=False, linewidth=1)
    plt.title('dataframe lines')
    # df.plot.scatter(x=df.index)
    # return
    
    L = [len(i) for i in ys_list]
    L = np.array(L)
    Nmax = max(L)
    print('Nmax:', Nmax)
    Nmin = min(L)
    print('Nmin:', Nmin, L.argmin(), beta_normalized[:,0][L.argmin()])
    
    x_ordered = beta_normalized[:,0]
    y_ordered = np.ones((len(x_ordered), Nmax))*np.nan
    # for i in range(len(x_ordered)):
    #     y_ordered[i,:] = ys_list[i]
        
    print('---------')
    print(y_ordered)
    print('---------')
    print(y_ordered.shape)
    print('---------')
    
    print(xs)
    print(ys)
    print(xs.shape)
    print(ys.shape)
    plt.figure()
    plt.scatter(xs, ys, marker='.', color='r', s=1)
    plt.title('xs, ys')
    for fn in [f1,f2,f3,f4]:
        plt.figure(fn.number)
        plt.scatter(xs, ys, marker='.', color='r', s=1)
        plt.axvline(x=beta_normalized[:,0][L.argmin()])
        for i in ys_list[L.argmin()]:
            plt.axhline(y=i)
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

def main():
    # testFillBands()
    # test_plot2D()
    # testPandas()
    # return
    
    foo = DBR()
    foo.t1 = 0.5
    foo.t2 = 0.5
    
    # plotDBR(dbr_instance=foo)
    # plotDBR_vs_angle(dbr_instance=foo, n_in=1)
    # plotDBR_vs_angle(dbr_instance=foo, n_in=foo.n1)
    # plotDBR_vs_angle(dbr_instance=foo, n_in=foo.n2)

    # testExtremeCases(dbr_instance=foo)
    findBandEdges(dbr_instance=foo, Spol=True)
    # findBandEdges(dbr_instance=foo, Spol=False)
    
    plt.show()

if __name__ == "__main__":
    main()
