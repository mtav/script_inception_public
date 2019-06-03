#!/bin/bash

function getOutFile()
{
    DIR=$(dirname "$(readlink -f "$1")")
    BASE=$(basename "$1" '_4ppn.sh')
    BASE=$(basename "$BASE" '_8ppn.sh')
    BASE=$(basename "$(basename "$BASE" '.out')" .sh)
    OUTFILE="$DIR/$BASE.out"
    echo "$OUTFILE"
}

function getScriptFile()
{
    DIR=$(dirname $(readlink -f "$1"))
    BASE=$(basename "$1" '_4ppn.sh')
    BASE=$(basename "$BASE" '_8ppn.sh')
    BASE=$(basename "$(basename $BASE '.out')" .sh)
    SCRIPTFILE="$DIR/$BASE.sh"
    echo "$SCRIPTFILE"
}

function getDataState()
{
    OUTFILE=$(getOutFile "$1")
    DIR=$(dirname "$(readlink -f "$OUTFILE")")
    BASE=$(basename "$DIR")
    if [ -s  "$OUTFILE" ]
    then
      if grep Deallocating  "$OUTFILE" 1>/dev/null 2>&1
      then
        #echo "$OUTFILE exists and is finished"
        #echo "$OUTFILE"
        return 0
      else
        #echo "$OUTFILE exists but is unfinished"
        #echo "$OUTFILE"
        return 1
      fi
    else
      #echo "$OUTFILE does not exist"
      #echo "$OUTFILE"
      return 2
    fi
}
