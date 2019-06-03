#!/bin/bash
set -eu

# for c in 1.0 1.1 1.2 1.3 1.4
# do
#   mpb _c=${c} woodpile-FCT.ctl | tee woodpile-FCT_c-${c}.log
# done
# mpb woodpile-FCT.ctl | tee woodpile-FCT_c-FCC.log
# seq 0 0.1 2.5
# seq FIRST STEP LAST
# for ((i=1;i<5;i+=1)); do echo "0.${i}" ; done

# mkdir output
# printf "%.2f\n" 56

# nrod=2.40
# nbg=1.00

nrod=${1:-2.40}
nbg=${2:-1.00}
rstart=${3:-0}
rstop=${4:-0.32}

nrod=$(printf "%.2f" ${nrod})
nbg=$(printf "%.2f" ${nbg})

DSTDIR="output-nrod_${nrod}.nbg_${nbg}"

echo "===> nrod=${nrod}"
echo "===> nbg=${nbg}"
echo "===> rstart=${rstart}"
echo "===> rstop=${rstop}"
echo "===> DSTDIR=${DSTDIR}"
# exit

mkdir --parents ${DSTDIR}

# FLAGS="--output_epsilon_only"
FLAGS=""

# for rn in $(seq 0.24 0.01 0.26)
# for rn in $(seq 0.15 0.01 0.32)
# for rn in $(seq 0.00 0.01 0.32)
for rn in $(seq ${rstart} 0.01 ${rstop})
do
  rn_string=$(printf "%.2f" ${rn})
  echo "---> rn=${rn_string} nrod=${nrod} nbg=${nbg}"
  mpb_wrapper.py ${FLAGS} --outfile "${DSTDIR}/nrod_${nrod}.nbg_${nbg}.rn_${rn_string}.out" r=${rn} inside-index=${nrod} outside-index=${nbg} resolution=100 RCD-bandgap-plots.ctl
  rm -v "${DSTDIR}/nrod_${nrod}.nbg_${nbg}.rn_${rn_string}_epsilon.h5"
done
