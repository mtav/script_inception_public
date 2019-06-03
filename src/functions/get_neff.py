#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import sqrt

def get_neff(n_cavity,n_mirror):
  '''calculates the average refractive index'''
  return sqrt(2*pow(n_cavity,4)/(3*pow(n_cavity,2)-pow(n_mirror,2)))

if __name__ == '__main__':
  pass
