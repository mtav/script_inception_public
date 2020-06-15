#!/bin/bash
OUTFILE=/tmp/RCD.out
mpb_wrapper.py --workdir=/tmp --outfile=${OUTFILE} num-bands=5 ~/Development/script_inception_public/src/examples/MPB-examples/RCD/RCD.ctl
MPB_parser.py ${OUTFILE} plot --y-lambda
