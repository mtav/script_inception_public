#!/bin/bash
set -eu

# Check if all parameters are present
# If no, exit
if [ $# -ne 1 ]
then
  echo "usage :"
  echo "`basename $0` DIR"
  echo "will submit all *.sh files in DIR"
  exit 0
fi

DIR=$1
find $DIR -name "*.sh" -execdir superqsub.sh {} \;
