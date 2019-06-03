#!/bin/bash
set -u

lattice_basis_size=1

for scaling_factor in "$@"
do
  for lattice_size in 1 3 5
  do
#     OUTFILE="MPB-scaling-test_scale-${scaling_factor}.out"
    OUTFILE="MPB-scaling-test_lattice_basis_size-${lattice_basis_size}_lattice_size-${lattice_size}_scale-${scaling_factor}.out"
    mpb scaling_factor=${scaling_factor} lattice_size=${lattice_size} MPB-scaling-test.ctl | tee ${OUTFILE}
    postprocess_mpb.sh ${OUTFILE}
  done
done
