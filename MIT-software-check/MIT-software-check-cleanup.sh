#!/bin/bash
set -eu

SCRIPTDIR=$(dirname "$0")
echo "SCRIPTDIR=${SCRIPTDIR}"
cd ${SCRIPTDIR}/MIT-software-check

rm -v *.h5 *.png *.gif
