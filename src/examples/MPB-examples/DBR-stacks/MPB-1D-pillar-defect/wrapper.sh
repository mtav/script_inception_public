#!/bin/bash

set -eu

INDEX=$(printf "%.2f" $1)

BASENAME="DBR_defect_ncav_${INDEX}"

OUTFILE_BANDS="${BASENAME}_bands.out"
OUTFILE_DEFECT_MODE="${BASENAME}_defect_mode.out"

mpb defect-mode?=false cavity_index=${INDEX} DBR_defect.ctl | tee ${OUTFILE_BANDS}
mpb defect-mode?=true cavity_index=${INDEX} DBR_defect.ctl | tee ${OUTFILE_DEFECT_MODE}

postprocess_mpb.sh ${OUTFILE_BANDS} ${OUTFILE_DEFECT_MODE}

for N in 1 2 3
do
  echo "N=${N}"
  h5tovtk -d data ${BASENAME}-epsilon.h5
  h5tovtk -d z.r ${BASENAME}-e.k01.b0${N}.tm.h5
  h5tovtk -d z.r ${BASENAME}-d.k01.b0${N}.tm.h5
  h5tovtk -d z.r ${BASENAME}-h.k01.b0${N}.tm.h5
  h5tovtk -d data ${BASENAME}-dpwr.k01.b0${N}.tm.h5
  h5tovtk -d data ${BASENAME}-hpwr.k01.b0${N}.tm.h5
done
