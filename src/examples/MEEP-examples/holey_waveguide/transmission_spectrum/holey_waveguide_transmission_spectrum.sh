#!/bin/bash

set -eu

NMIN=${1:-0}
NMAX=${2:-16}

# clean up
# trash.py *.png *.gif *.out *.h5

CTLFILEBASE=holey_waveguide_transmission_spectrum
CTLFILE=${CTLFILEBASE}.ctl

# for (( N = 0 ; N <=  1 ; N++ ))
# for (( N = 2 ; N <= 16 ; N++ ))
for (( N = ${NMIN} ; N <= ${NMAX} ; N++ ))
do
  NSTR=$(printf "%02d" ${N})
  echo "=== N = ${NSTR} ==="
  tee_wrapper.py -s "N=${NSTR}" meep N=$N ${CTLFILE}
  grep flux1: "${CTLFILEBASE}.N=${NSTR}.out" > "${CTLFILEBASE}.N=${NSTR}.dat"
#   meep_wrapper.py --grep-flux --h5topng --automatic-suffix --automatic-filename-prefix N=$N ${CTLFILE}
done
