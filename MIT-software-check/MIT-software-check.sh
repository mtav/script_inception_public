#!/bin/bash
set -eu

N=0

function proceed()
{
	# echo "--- press enter ---"
	# read
	N=$((N+1))
}

SCRIPTDIR=$(dirname "$0")
echo "SCRIPTDIR=${SCRIPTDIR}"
cd ${SCRIPTDIR}/MIT-software-check

echo "=== checking mpb version ==="
mpb --version
proceed

echo "=== checking meep version ==="
meep --version
proceed
 
echo "=== checking h5ls version ==="
h5ls --version
proceed

echo "=== checking harminv version ==="
harminv -V
proceed

echo "=== checking h5topng version ==="
h5topng -V
proceed

echo "=== checking convert version ==="
convert-imagemagick.exe --version
proceed

echo "=== testing mpb ==="
mpb test-mpb.ctl
proceed

echo "=== testing meep 1/4 ==="
meep bend.ctl
proceed

echo "=== testing meep 2/4 ==="
meep meep-harminv-test-2.ctl
proceed

echo "=== testing meep 3/4 ==="
meep compute-mode?=false meep-harminv-test.ctl
proceed

echo "=== testing meep 4/4 ==="
meep compute-mode?=true meep-harminv-test.ctl
proceed

echo "=== testing h5ls ==="
h5ls bend-ez.h5
proceed

echo "=== testing h5topng ==="
h5topng -t 0:329 -R -Zc dkbluered -a yarg -A bend-eps-000000.00.h5 bend-ez.h5
proceed

echo "=== testing convert ==="
convert-imagemagick.exe bend-ez.t*.png bend-ez.gif
proceed

echo "All $N tests successful! :)"
