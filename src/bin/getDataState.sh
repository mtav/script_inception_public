#!/bin/bash

#set -eux

source script_inception_common_functions.sh

for f in "$@"
do
  OUTFILE=$(getOutFile "$f")
  getDataState $f
  status=$?
  echo "$OUTFILE : $status"
done
