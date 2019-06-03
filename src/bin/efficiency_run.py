#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utilities.bfdtd_utilities import efficiency_run

def main(argv=None):
  '''
  Copy src to dst while removing the geometry
  '''
  src = sys.argv[1]
  dst = sys.argv[2]
  efficiency_run(src, dst)

if __name__ == "__main__":
  sys.exit(main())
