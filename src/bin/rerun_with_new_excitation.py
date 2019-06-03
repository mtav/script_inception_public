#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utilities.bfdtd_utilities import rerun_with_new_excitation

def main(argv=None):
  '''
  creates a new sim DST from SRC, only changing the excitation wavelength and time constant
  example run:
  rerun_with_new_excitation.py qedc3_2_05.in /tmp/new 637 42
  '''
  src = sys.argv[1]
  dst = sys.argv[2]
  excitation_wavelength_nm = float(sys.argv[3])
  excitation_time_constant = float(sys.argv[4])
  rerun_with_new_excitation(src, dst, excitation_wavelength_nm, excitation_time_constant)

if __name__ == "__main__":
  sys.exit(main())
