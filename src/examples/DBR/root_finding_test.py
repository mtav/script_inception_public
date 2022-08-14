#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 14:45:32 2022

@author: Mike Taverne
Based on answer from: https://stackoverflow.com/questions/13054758/python-finding-multiple-roots-of-nonlinear-equation
"""

import math
import numpy as np
import matplotlib.pyplot as plt

def rootsearch(f,a,b,dx):
    '''
    Search for roots of f on interval [a,b], starting on interval [a,a+dx], then [a+dx,a+2*dx], etc.
    Returns (None, None) if nothing found over the whole interval.
    '''
    x1 = a; f1 = f(a)
    x2 = a + dx; f2 = f(x2)
    while f1*f2 > 0.0:
        if x1 >= b:
            return None,None
        x1 = x2; f1 = f2
        x2 = x1 + dx; f2 = f(x2)
    return x1,x2

def bisect(f,x1,x2,switch=0,epsilon=1.0e-9):
    f1 = f(x1)
    if f1 == 0.0:
        return x1
    f2 = f(x2)
    if f2 == 0.0:
        return x2
    if f1*f2 > 0.0:
        print('Root is not bracketed')
        return None
    n = int(math.ceil(math.log(abs(x2 - x1)/epsilon)/math.log(2.0)))
    for i in range(n):
        x3 = 0.5*(x1 + x2); f3 = f(x3)
        if (switch == 1) and (abs(f3) >abs(f1)) and (abs(f3) > abs(f2)):
            return None
        if f3 == 0.0:
            return x3
        if f2*f3 < 0.0:
            x1 = x3
            f1 = f3
        else:
            x2 =x3
            f2 = f3
    return (x1 + x2)/2.0

def roots(f, a, b, eps=1e-6):
    r = []
    print ('The roots on the interval [%f, %f] are:' % (a,b))
    while 1:
        x1,x2 = rootsearch(f,a,b,eps)
        if x1 != None:
            a = x2
            root = bisect(f,x1,x2,1)
            if root != None:
                r.append(root)                
                print (round(root,-int(math.log(eps, 10))))
        else:
            print ('\nDone')
            break
    return r

def main():
    f=lambda x:x*np.cos(x-4)
    a=-3
    b=3
    r = roots(f, a, b)
    # plot(x, f(x))
    x = np.linspace(a,b)
    print(x)
    
    plt.plot(x, f(x))
    plt.axhline(y=0, color='k')
    
    for i in r:
        plt.axvline(x=i, color='r', linestyle='--')
        
    from scipy.optimize import fsolve
    def func(x):
        return [x[0] * np.cos(x[1]) - 4,
                x[1] * x[0] - x[1] - 5]

    root = fsolve(func, [1, 1])
    print(root)
    
    root = fsolve(f, 0)
    print(root)

    # from sympy import symbols
    # from sympy.plotting import plot
    # x=symbols('x')
    # plot(x*x)
    

if __name__ == "__main__":
    main()
