#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparseui
from PyQt5 import QtWidgets

def createGUI(obj):
  '''A function to simplify creating GUIs from classes with appropriate argparse-related functions.
  
  .. todo:: Document properly with example code, etc.
  '''
  parser = obj.get_argument_parser()
  if len(sys.argv) > 1:
    obj.writeFromParsedOptions(parser.parse_args())
  else:
    app = QtWidgets.QApplication(sys.argv)
    a = argparseui.ArgparseUi(parser, use_save_load_button=True, use_scrollbars=True, window_title=type(obj).__name__, ok_button_handler=lambda x: obj.writeFromParsedOptions(x.parse_args()))
    a.show()
    app.exec_()
  return
