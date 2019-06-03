#!/bin/bash

./RCD-bandgap-plots.sh 2.40 1.00 0.01 0.23
./RCD-bandgap-plots.sh 1.00 2.40 0.15 0.32

./RCD-bandgap-plots.sh 2.00 1.00 0.01 0.23
./RCD-bandgap-plots.sh 1.00 2.00 0.15 0.32

./RCD-bandgap-plots.sh 1.90 1.00 0.01 0.23
./RCD-bandgap-plots.sh 1.00 1.90 0.15 0.32

# grep fill output-nrod_2.40.nbg_1.00/*.out
# grep fill output-nrod_1.00.nbg_2.40/*.out

# ./RCD-bandgap-plots-postprocess.py output-nrod_?.??.nbg_?.??/*.out
./RCD-bandgap-plots-postprocess.py output-nrod_1.00.nbg_1.90/*.out > output-nrod_1.00.nbg_1.90.csv
./RCD-bandgap-plots-postprocess.py output-nrod_1.00.nbg_2.00/*.out > output-nrod_1.00.nbg_2.00.csv
./RCD-bandgap-plots-postprocess.py output-nrod_1.00.nbg_2.40/*.out > output-nrod_1.00.nbg_2.40.csv
./RCD-bandgap-plots-postprocess.py output-nrod_1.90.nbg_1.00/*.out > output-nrod_1.90.nbg_1.00.csv
./RCD-bandgap-plots-postprocess.py output-nrod_2.00.nbg_1.00/*.out > output-nrod_2.00.nbg_1.00.csv
./RCD-bandgap-plots-postprocess.py output-nrod_2.40.nbg_1.00/*.out > output-nrod_2.40.nbg_1.00.csv

./RCD-bandgap-plots-postprocess.py output-nrod_1.00.nbg_1.90/*.out > output-nrod_1.00.nbg_1.90.v2.csv
./RCD-bandgap-plots-postprocess.py output-nrod_1.00.nbg_2.00/*.out > output-nrod_1.00.nbg_2.00.v2.csv
./RCD-bandgap-plots-postprocess.py output-nrod_1.00.nbg_2.40/*.out > output-nrod_1.00.nbg_2.40.v2.csv
./RCD-bandgap-plots-postprocess.py output-nrod_1.90.nbg_1.00/*.out > output-nrod_1.90.nbg_1.00.v2.csv
./RCD-bandgap-plots-postprocess.py output-nrod_2.00.nbg_1.00/*.out > output-nrod_2.00.nbg_1.00.v2.csv
./RCD-bandgap-plots-postprocess.py output-nrod_2.40.nbg_1.00/*.out > output-nrod_2.40.nbg_1.00.v2.csv

../RCD-bandgap-plots-postprocess.py output-nrod_1.00.nbg_1.90/*.out > output-nrod_1.00.nbg_1.90.v4.csv
../RCD-bandgap-plots-postprocess.py output-nrod_1.00.nbg_2.00/*.out > output-nrod_1.00.nbg_2.00.v4.csv
../RCD-bandgap-plots-postprocess.py output-nrod_1.00.nbg_2.40/*.out > output-nrod_1.00.nbg_2.40.v4.csv
../RCD-bandgap-plots-postprocess.py output-nrod_1.90.nbg_1.00/*.out > output-nrod_1.90.nbg_1.00.v4.csv
../RCD-bandgap-plots-postprocess.py output-nrod_2.00.nbg_1.00/*.out > output-nrod_2.00.nbg_1.00.v4.csv
../RCD-bandgap-plots-postprocess.py output-nrod_2.40.nbg_1.00/*.out > output-nrod_2.40.nbg_1.00.v4.csv

# test FF values
nrod=1.00
nbg=2.40
rn=0.25
rn_string=$(printf "%.2f" ${rn})
# FLAGS="--output_epsilon_only"
FLAGS=""
DSTDIR="output-nrod_${nrod}.nbg_${nbg}"
mkdir --parents ${DSTDIR}
mpb_wrapper.py ${FLAGS} --outfile "${DSTDIR}/nrod_${nrod}.nbg_${nbg}.rn_${rn_string}.out" r=${rn} inside-index=${nrod} outside-index=${nbg} RCD-bandgap-plots.ctl
time_plus mpb_wrapper.py ${FLAGS} --outfile "${DSTDIR}/nrod_${nrod}.nbg_${nbg}.rn_${rn_string}.out" r=${rn} inside-index=${nrod} outside-index=${nbg} resolution=100 RCD-bandgap-plots.ctl
