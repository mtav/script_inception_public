#!/bin/bash

set -u

# NOTE: This hacked up script is really useful! Need to implement a non-hacky version!

# disable processing, only show what would be done
ECHO=echo

# enable processing
#ECHO=''

# TODO: Get offset number from part 1 .inp file?

BFDTD_justList()
{
  #echo "================"
  ls -ld $1
  #ls -l --color $1
}

BFDTD_checkForEpsilon()
{
  #echo "================"
  if ls -ld --color $1/*epsilon* &>/dev/null
  then
    echo "epsilon found"
    if ls $1/*epsilon*/*.prn &>/dev/null
    then
      #echo
      echo "epsilon has data"
    else
      echo "epsilon has no data"
      ls -d $1/*epsilon*
    fi
  else
    #echo
    echo "no epsilon found"
  fi
}

BFDTD_findFiles()
{
  GEO="$1/Ex.probe-run/woodpile.geo"
  echo "================"
  ls "$GEO"
  echo "------"
  findFile.sh "$GEO"
}

BFDTD_process()
{
  PART1_DIR=$(readlink -f $1/part_1)
  PART2_DIR=$(readlink -f $1/part_2)
  EPSILON_DIR=$(readlink -f $(dirname $1)/epsilon)
  
  echo "=========================="
  echo "PART1_DIR = $PART1_DIR"
  echo "PART2_DIR = $PART2_DIR"
  echo "EPSILON_DIR = $EPSILON_DIR"
  
  ls -1 $PART1_DIR/*00.prn | wc -l
  ls -1 $PART2_DIR/*00.prn | wc -l
  
  ORIGDIR=$(pwd)
  cd $PART1_DIR
  
  # create .inp file containing all snapshots
  bfdtd_tool.py -i $PART1_DIR/woodpile.inp -i $PART2_DIR/woodpile.inp --writeInpFile=$PART1_DIR/AllSnapshots.inp
  
  # link to epsilon files
  find $EPSILON_DIR/*.prn | xargs -n1 -I{} ln -s {} $PART1_DIR/
  
  # link to part 2 files with offset
  fix_filenames.py -v --action=symlink --output-directory=$PART1_DIR/ --directory ../part_2/ --offset 26 --output-format=dummy
  
  #$ECHO touch dummy
  
  cd $ORIGDIR
}

BFDTD_verify()
{
  PART1_DIR=$(readlink -f $1/part_1)
  PART2_DIR=$(readlink -f $1/part_2)
  EPSILON_DIR=$(readlink -f $(dirname $1)/epsilon)
  
  echo "=========================="
  echo "PART1_DIR = $PART1_DIR"
  echo "PART2_DIR = $PART2_DIR"
  echo "EPSILON_DIR = $EPSILON_DIR"

#   ls $EPSILON_DIR
  echo "=part 1="
  ls -1 $PART1_DIR/*00.prn | wc -l
  echo "=part 2="
  ls -1 $PART2_DIR/*00.prn | wc -l
  #ls $PART1_DIR/[xyz][0-9]*01.prn | wc -l
  echo "=epsilon="
  ls $EPSILON_DIR/[xyz][0-9]*01.prn | wc -l
  ls $PART1_DIR/AllSnapshots.inp
}

BFDTD_getLastSnapTimeNumber()
{
  PART1_DIR=$(readlink -f $1/part_1)
  PART2_DIR=$(readlink -f $1/part_2)
  #EPSILON_DIR=$(readlink -f $(dirname $1)/epsilon)
  
  echo "=========================="
  echo "PART1_DIR = $PART1_DIR"
  echo "PART2_DIR = $PART2_DIR"
  #echo "EPSILON_DIR = $EPSILON_DIR"

  ORIGDIR=$(pwd)

  cd $PART1_DIR
  ls -1rt za_id_*.prn | tail -n1
  cd $PART2_DIR
  ls -1rt za_id_*.prn | tail -n1

  cd $ORIGDIR
}

BFDTD_processCentralSnapshots()
{
  FSNAP_DIR=$(readlink -f $1)
  EPSILON_DIR=$(readlink -f $(dirname $1)/epsilon)
  
  echo "=========================="
  echo "FSNAP_DIR = $FSNAP_DIR"
  echo "EPSILON_DIR = $EPSILON_DIR"
  
  ln -s $EPSILON_DIR/x52_id_01.prn $FSNAP_DIR
  ln -s $EPSILON_DIR/y53_id_01.prn $FSNAP_DIR
  ln -s $EPSILON_DIR/z31_id_01.prn $FSNAP_DIR
}

BFDTD_getSnapShotInfo()
{
  PART1_DIR=$(readlink -f $1/part_1)

  echo "=========================="
  echo "PART1_DIR = $PART1_DIR"

  grep -i first $PART1_DIR/AllSnapshots.inp | uniq
  grep -i repetition $PART1_DIR/AllSnapshots.inp | uniq
  grep -i starting $PART1_DIR/AllSnapshots.inp | uniq
  grep -i "\*\*FREQUENCY" $PART1_DIR/AllSnapshots.inp | uniq
}

BFDTD_mainProcess()
{
  #justList $1
  #verify $1
  getLastSnapTimeNumber $1
  #getSnapShotInfo $1
  #process $1
  #checkForEpsilon $1
  #findFiles $1
}

# If the script is not sourced, but run directly, use the first argument as processing function and process all the following arguments with it.
# Source detection method from http://stackoverflow.com/questions/2683279/how-to-detect-if-a-script-is-being-sourced/23009039#23009039
if [ "$0" = "$BASH_SOURCE" ]
then
  if [ $# -lt 1 ]
  then
          echo "usage:"
          echo "$(basename $0) FUNC DIR1 [DIR2 [...]]"
          echo "Available functions:"
          echo " BFDTD_checkForEpsilon"
          echo " BFDTD_getLastSnapTimeNumber"
          echo " BFDTD_justList"
          echo " BFDTD_process"
          echo " BFDTD_verify"
          echo " BFDTD_findFiles"
          echo " BFDTD_getSnapShotInfo"
          echo " BFDTD_mainProcess"
          echo " BFDTD_processCentralSnapshots"
          echo "This script can also be source to access the functions."
          exit 0
  fi

  FUNC=$1
  shift

  for dir in "$@"
  do
    echo "--->Processing ${dir}"
    ${FUNC} ${dir}
  done
fi
