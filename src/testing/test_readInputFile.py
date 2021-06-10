#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bfdtd.bfdtd_parser import *

if __name__ == '__main__':

  foo = BFDTDobject()
  foo.readInputFile('sample.geo')

  b = foo.block_list[0]
  print('b.name = ', b.name)

  b = foo.block_list[1]
  print('b.name = ', b.name)

  print('len(foo.cylinder_list) = ', len(foo.cylinder_list))

  for cyl in foo.cylinder_list:
    print('cyl.name = ', cyl.name)
