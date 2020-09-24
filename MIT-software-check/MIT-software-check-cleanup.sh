#!/bin/bash
set -eu

SCRIPTDIR=$(dirname "$0")
echo "SCRIPTDIR=${SCRIPTDIR}"
cd ${SCRIPTDIR}/MIT-software-check

echo "=== WARNING: USE AT YOUR OWN RISK! ==="
echo "Optional: clean up first (y/n)?"
echo "This will run 'rm --verbose *.h5 *.png *.gif' in $(pwd)."
echo "i.e. it will delete all *.h5 *.png *.gif in this directory permanently."
echo "Press 'y' then 'enter' to clean up before the test."
echo "Otherwise, just press enter."
read ans
case $ans in
  y) rm --verbose *.h5 *.png *.gif;;
esac
