#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# add power compensation

import sys
from GWL.GWL_parser import GWLobject

#import tempfile
# tempfile.gettempdir()

def main():
  if len(sys.argv)>4:
    INFILE = sys.argv[1]
    OUTFILE = sys.argv[2]
    LP0 = float(sys.argv[3])
    K = float(sys.argv[4])
  else:
    print('Usage: '+sys.argv[0]+' INFILE OUTFILE LP0 K', file=sys.stderr)
    sys.exit(-1)
  
  obj = GWLobject()
  obj.readGWL(INFILE)
  obj.addPowerCompensation(LP0, K)
  obj.writeGWL(OUTFILE)

if __name__ == "__main__":
  main()
