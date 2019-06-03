#!/bin/bash
set -eux

DIR=$(readlink -f $1)
PROBEINDEX=$2

PROBENAME1=$(printf "p%02did.prn" $PROBEINDEX)
PROBENAME2=$(printf "p%03did.prn" $PROBEINDEX)
PROBENAME3=$(printf "p%02did.png" $PROBEINDEX)
PROBENAME4=$(printf "p%03did.png" $PROBEINDEX)

matlab_batcher.sh plotAll "'$DIR',NaN,{'$PROBENAME1','$PROBENAME2'},{'foo'}"

#find . -name "*.png" | xargs -n1 -I{} convert {} -trim {}new

trim.sh $DIR
find $DIR -name "*.eps" | xargs rm -v

TODO: Handle cases where it is p01 or p001
if [ -f  ]
$HOME/Development/script_inception_public/special_ops/SO_delimages.py $DIR $PROBENAME3
$HOME/Development/script_inception_public/special_ops/SO_delimages.py $DIR $PROBENAME4

#$HOME/Development/script_inception_public/special_ops/SO_reportGenerator.py -t $title -o $texfile image.png !(image).png
