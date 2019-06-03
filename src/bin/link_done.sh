#!/bin/bash
set -u

usage()
{
  echo "usage :"
  echo "`basename $0` 0 file1.out/.sh file2.out/.sh ... (just list finished ones)"
  echo "`basename $0` 1 file1.out/.sh file2.out/.sh ... (list unfinished running ones)"
  echo "`basename $0` 2 file1.sh file2.sh ... (list all unfinished ones)"
  echo "`basename $0` 3 DEST  file1.out/.sh file2.out/.sh ... (create links to finished ones in DEST)"
  echo "creates links to the dirs containing *.out in DEST if *.out contains \"Deallocating\", i.e. if the simulations in those dirs are finished"
  echo "`basename $0` 4 file1.out/.sh file2.out/.sh ... (submit unfinished ones)"
  echo "`basename $0` 5 file1.out/.sh file2.out/.sh ... (create links to finished ones in ~/DATA/DONE with correct directory structure)"
  echo "NOTE: Use of */*.sh is recommended instead of */*.out as out files may not exist"
  exit 0
}

if [ $# -lt 2 ]
then
  usage;
fi

operation_type=$1
shift

source script_inception_common_functions.sh

function list_finished()
{
  #~ echo "==>list_finished called"
  for f in "$@"
  do
    OUTFILE=$(getOutFile "$f")
    getDataState $f
    status=$?
    if  [ $status == 0 ]
    then
      echo $OUTFILE
    fi
  done
}

function list_unfinished_running()
{
  #~ echo "==>list_unfinished_running called"
  for f in "$@"
  do
    OUTFILE=$(getOutFile "$f")
    getDataState $f
    status=$?
    if  [ $status == 1 ]
    then
      echo $OUTFILE
    fi
  done
}

function list_unstarted()
{
  #~ echo "==>list_unstarted called"
  for f in "$@"
  do
    OUTFILE=$(getOutFile "$f")
    getDataState $f
    status=$?
    if  [ $status == 2 ]
    then
      echo $OUTFILE
    fi
  done
}

function list_all_unfinished()
{
  #~ echo "==>list_all_unfinished called"
  for f in "$@"
  do
    OUTFILE=$(getOutFile "$f")
    getDataState $f
    status=$?
    if  [ $status == 1 ] || [ $status == 2 ]
    then
      echo $OUTFILE
    fi
  done
}

function link_finished()
{
  #~ echo "==>link_finished called"
  DST=$(readlink -f $1)
  if ! [ -d $DST ]
  then
    echo "Error: $DST does not exist or is not a directory"
    exit -1
  fi
  shift
  for f in "$@"
  do
    echo "Processing $f"
    OUTFILE=$(getOutFile "$f")
    DIR=$(dirname $(readlink -f $OUTFILE))
    BASE=$(basename $DIR)
    LINKNAME="$DST/$BASE"
    if ! [ -e "$LINKNAME" ]
    then
      if grep Deallocating  "$OUTFILE"
      then
        echo "ln -s $DIR $LINKNAME"
        ln -s "$DIR" "$LINKNAME"
      else
        echo "Deallocating not found in $OUTFILE"
      fi
    else
      echo "Warning: $LINKNAME already exists"
    fi
  done
}

function qsub_unfinished()
{
  #~ echo "==>qsub_unfinished called"
  for f in "$@"
  do
    OUTFILE=$(getOutFile "$f")
    SCRIPTFILE=$(getScriptFile "$f")
    if [ -s  "$OUTFILE" ]
    then
      #~ echo "$OUTFILE exists"
      if ! grep Deallocating  "$OUTFILE" 1>/dev/null 2>&1
      then
        #~ echo "$OUTFILE exists but is unfinished"
        superqsub.sh "$f"
      fi
    else
      #~ echo "$OUTFILE does not exist"
      superqsub.sh "$f"
    fi
  done
}

if [ $operation_type = "0" ]
then
  list_finished "$@";
elif [ $operation_type = "1" ]
then
  list_unfinished_running "$@";
elif [ $operation_type = "2" ]
then
  list_all_unfinished "$@";
elif [ $operation_type = "3" ]
then
  link_finished "$@";
elif [ $operation_type = "4" ]
then
  qsub_unfinished "$@";
else
  usage;
fi
