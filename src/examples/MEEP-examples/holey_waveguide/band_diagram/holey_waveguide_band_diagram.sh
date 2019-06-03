#!/bin/bash

set -eu

# clean up
trash.py *.png *.h5 *.out *.gif *.dat

# create band diagram
tee_wrapper.py meep holey_waveguide_band_diagram.ctl
grep freqs: holey_waveguide_band_diagram.out > fre.dat
grep freqs-im: holey_waveguide_band_diagram.out > fim.dat
octave holey_waveguide_band_diagram.m

# output fields for specific omega, k points:
output_fields()
{
  kx=$1
  fcen=$2
  df=$3
  echo "=== kx=${kx} fcen=${fcen} df=${df} ==="
  tee_wrapper.py meep kx=${kx} fcen=${fcen} df=${df} holey_waveguide_band_diagram.ctl
  BASE=$(printf "holey_waveguide_band_diagram_kx-%.2f_fcen-%.4f_df-%.4f" ${kx} ${fcen} ${df})
  echo "BASE = ${BASE}"
  h5topng -RZc dkbluered -C ${BASE}-eps-000000.00.h5 ./${BASE}-hz-0*.h5
  convert ${BASE}-hz-0*.png ${BASE}-hz.gif
}

output_fields 0.40 0.1896 0.01
output_fields 0.40 0.3175 0.01
output_fields 0.10 0.4811 0.01
output_fields 0.30 0.8838 0.01
output_fields 0.25 0.2506 0.01

# for the leaky mode with small kx, we need a bigger df value (broader frequency range of gaussian excitation)
output_fields 0.10 0.4811 0.0025000
output_fields 0.10 0.4811 0.1 # this looks like the one on the wiki
output_fields 0.10 0.4811 0.001
