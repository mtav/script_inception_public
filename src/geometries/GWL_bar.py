#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy
import argparse
import tempfile
from GWL.GWL_parser import *

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('DSTDIR', default=tempfile.gettempdir(), nargs='?')
  args = parser.parse_args()  
  print(args.DSTDIR)
  
  GWL_obj = GWLobject()
  P1 = [0,0,0]
  P2 = [1,0,0]
  LineNumber_Horizontal = 5
  LineDistance_Horizontal = 1
  LineNumber_Vertical = 10
  LineDistance_Vertical = 0.5
  BottomToTop = True

  GWL_obj.addXblock(P1, P2, LineNumber_Horizontal, LineDistance_Horizontal, LineNumber_Vertical, LineDistance_Vertical, BottomToTop)

  (Pmin, Pmax) = GWL_obj.getLimits()
  GWL_obj.writeGWL(os.path.join(args.DSTDIR, 'GWL_bar.gwl'), writingOffset = [0,0,-Pmin[2],0] )

if __name__ == "__main__":
  main()
