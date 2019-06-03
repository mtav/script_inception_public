#!/bin/bash

set -u

ORIGDIR=$(pwd)

LOGFILE="$ORIGDIR/testrun.log"

echo >"$LOGFILE"

for f in "$@"
do
	echo "=== Testing $f ==="
	#readlink -f "$f"
	FILE=$(readlink -f "$f")
	#echo $FILE
	DIR=$(dirname $FILE)
	cd $DIR
	(fdtd "$FILE" | grep ERR &) ; sleep 1; killall fdtd
	RESULT=$?
	if [ $RESULT -ne 0 ]
	then
		echo "$f" >>"$LOGFILE"
	fi
	cd $ORIGDIR
done
