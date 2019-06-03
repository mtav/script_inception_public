#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import tempfile
import argparse
from PyQt5 import QtWidgets
import argparseui

from GWL.tube import Tube
from GWL.GWL_parser import GWLobject

def createTube(argparseuiinstance):
  options = argparseuiinstance.parse_args()
  print ("Options: ", options)

  ## create object instance
  obj = Tube()
  
  ## set object attributes
  
  # tube attributes
  obj.centro = [options.centro_X, options.centro_Y, options.centro_Z]
  obj.inner_radius = options.inner_radius
  obj.outer_radius = options.outer_radius
  obj.height = options.height
  obj.method = options.method
  obj.PointDistance_r = options.PointDistance_r
  obj.PointDistance_theta = options.PointDistance_theta
  obj.PointDistance_z = options.PointDistance_z
  obj.downwardWriting = options.downwardWriting
  obj.zigzag = options.zigzag
  obj.rotateSpirals = options.rotateSpirals
  obj.add_flat_ends = options.add_flat_ends
  obj.closed_loop = options.closed_loop

  # GWLobject attributes
  obj.set_lower_to_origin = options.set_lower_to_origin
  obj.write_power = options.write_power
  obj.PC_laser_power_at_z0 = options.PC_laser_power_at_z0
  obj.PC_slope = options.PC_slope
  obj.PC_interfaceAt = options.PC_interfaceAt
  obj.PC_bool_InverseWriting = options.PC_bool_InverseWriting
  obj.PC_float_height = options.PC_float_height
  obj.PC_bool_LaserPowerCommand = options.PC_bool_LaserPowerCommand

  ## write object
  # TODO: Limits should be calculated while computing the points to avoid looping through them again.
  obj.computePoints()
  obj.updateLimits()
  obj.writeGWLWithPowerCompensation(options.outfile)

  return

def get_argument_parser():
  parser = argparse.ArgumentParser(description = 'Create GWL tube objects.')
  
  parser.add_argument('-o','--outfile', action="store", default=tempfile.gettempdir()+os.sep+'tube.gwl', help='output filename')
  
  parser.add_argument("--set-lower-to-origin", help='offset structure so that its "lower corner" is moved to the (0,0,0) coordinates. This will make all coordinates positive.', action="store_true")

  parser.add_argument("--write-power", help="Write power values using the power compensation (PC) parameters.", action="store_true")
  
  parser.add_argument("--PC_laser_power_at_z0", help="PC: laser power at z0", type=float, default=100)
  parser.add_argument("--PC_slope", help="PC: power compensation slope", type=float, default=0)
  parser.add_argument("--PC_interfaceAt", help="PC: interface position", type=float, default=0)
  parser.add_argument("--PC_bool_InverseWriting", help="PC: To write a file designed for use with the InvertZAxis command", action="store_true", default=False)
  parser.add_argument("--PC_float_height", help='PC: "substrate height", in practice just a value added to the interfaceAt value', type=float, default=0)
  parser.add_argument("--PC_bool_LaserPowerCommand", help="PC: Use the LaserPower command instead of a 4th coordinate for power.", action="store_true", default=False)

  parser.add_argument("--centro_X", help="Centre X position", type=float, default=0)
  parser.add_argument("--centro_Y", help="Centre Y position", type=float, default=0)
  parser.add_argument("--centro_Z", help="Centre Z position", type=float, default=0)
  
  parser.add_argument("--inner-radius", help="inner radius", type=float, default=1)
  parser.add_argument("--outer-radius", help="outer radius", type=float, default=2)

  parser.add_argument("--height", help="height", type=float, default=2)

  parser.add_argument("--PointDistance_r", help="PointDistance_r", type=float, default=0.2)
  parser.add_argument("--PointDistance_theta", help="PointDistance_theta", type=float, default=0.2)
  parser.add_argument("--PointDistance_z", help="PointDistance_z", type=float, default=0.2)

  parser.add_argument("--method", help="writing method", type=str, choices=['spiral', 'vertical lines', 'horizontal disks'],  default='spiral')

  parser.add_argument("--downwardWriting", help="downwardWriting", action="store_true")
  parser.add_argument("--zigzag", help="zigzag", action="store_true")
  parser.add_argument("--rotateSpirals", help="rotateSpirals", action="store_true")
  parser.add_argument("--add_flat_ends", help="add_flat_ends", action="store_true")
  parser.add_argument("--closed_loop", help="closed_loop", action="store_true")
    
  return parser

def main():
  parser = get_argument_parser()

  app = QtWidgets.QApplication(sys.argv)
  a = argparseui.ArgparseUi(parser, use_save_load_button=True, ok_button_handler=createTube)
  a.show()
  app.exec_()
  if a.result() != 1:
    # Do what you like with the arguments...
    print ("Cancel pressed")
    sys.exit(-1)
  return 0

if __name__ == '__main__':
	main()
