#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bfdtd.bfdtd_parser import *

if __name__ == '__main__':

  toto=BFDTDobject()
  #toto.read_input_file('cylinder.bottomN_20.topN_10.geo')
  toto.read_input_file('sample.geo')

  b=toto.block_list[0]
  print 'dummy = ', 'fjhjs'
  print 'b.name = ', b.name

  b=toto.block_list[1]
  print 'b.name = ', b.name

  print 'len(toto.cylinder_list) = ', len(toto.cylinder_list)

  for cyl in toto.cylinder_list:
    print 'cyl.name = ', cyl.name
