#!/bin/bash
set -euo pipefail

./RCD-bandgap-plots.sh 2.40 1.00 0.01 0.23 0.01 16 3
./RCD-bandgap-plots.sh 1.00 2.40 0.15 0.32 0.01 16 3

./RCD-bandgap-plots-postprocess.py output-nrod_2.40.nbg_1.00/*.out > output-nrod_2.40.nbg_1.00.csv
./RCD-bandgap-plots-postprocess.py output-nrod_1.00.nbg_2.40/*.out > output-nrod_1.00.nbg_2.40.csv

./RCD-bandgap-plots-plot-all-in-one.py output-nrod_2.40.nbg_1.00.csv output-nrod_1.00.nbg_2.40.csv
./RCD-bandgap-plots-plot.py output-nrod_2.40.nbg_1.00.csv output-nrod_1.00.nbg_2.40.csv
