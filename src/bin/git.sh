#!/bin/bash
set -eu

# loading matlab changes the curl library to one not supporting https, which prevents the use of git

if module list 2>&1 | grep matlab >/dev/null
then
  MATLAB_MODULE=$(module list 2>&1 | grep matlab | awk '{print $2}')
#   echo "MATLAB_MODULE = ${MATLAB_MODULE}"
  module unload ${MATLAB_MODULE}
fi
git "$@"
