#!/bin/bash
# run an MPB simulation and plot the results to test if everything is setup correctly.

set -eu

TESTDIR=$(mktemp -d)
cd ${TESTDIR}

OUTFILE="test.out"

mpb_wrapper.py --workdir='.' --outfile=${OUTFILE} k-interp=5 resolution=10 num-bands=3 ${HOME}/Development/script_inception_public/src/examples/MPB-examples/RCD/RCD.ctl
MPB_parser.py ${OUTFILE} plot --y-range-auto --x-range-auto

echo "SUCCESS"
