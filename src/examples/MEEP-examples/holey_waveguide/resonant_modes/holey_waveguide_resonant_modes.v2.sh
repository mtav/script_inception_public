#!/bin/bash

set -eu

# clean up
# trash.py *.png *.gif *.out *.h5

# mpirun meep-mpi compute-mode?=true holey_waveguide_resonant_modes.ctl
meep compute-mode?=true holey_waveguide_resonant_modes.ctl | tee holey_waveguide_resonant_modes.out

BASE="./holey_waveguide_resonant_modes_sy-6.000_fcen-0.250_df-0.200_N-03_compute-mode-true"
h5topng -RZc dkbluered -C ${BASE}-eps-000000.00.h5 ./${BASE}-hz-0*.h5
convert ${BASE}-hz-0*.png ${BASE}-hz.gif

for (( N = 2 ; N <= 16 ; N++ ))
do
  NSTR=$(printf "%02d" ${N})
  echo "=== N = ${NSTR} ==="
  tee_wrapper.py -s "N=${NSTR}" meep N=$N compute-mode?=true holey_waveguide_resonant_modes.ctl
done

tee_wrapper.py -s "higher-order-mode" meep sy=12 fcen=0.328227374843021 df=0.01 N=16 compute-mode?=true holey_waveguide_resonant_modes.ctl
BASE="./holey_waveguide_resonant_modes_sy-12.000_fcen-0.328_df-0.010_N-16_compute-mode-true"
h5topng -RZc dkbluered -C ${BASE}-eps-000000.00.h5 ./${BASE}-hz-0*.h5
convert ${BASE}-hz-0*.png ${BASE}-hz.gif

for i in holey_waveguide_resonant_modes.N=??.out
do
  grep harminv $i > ${i%.out}.csv
done
