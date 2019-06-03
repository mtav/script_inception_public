#!/bin/bash
set -eux
DIR=$(readlink -f $1)
matlab_batcher.sh plotAll "'$DIR',NaN,{'p01id.prn','p001id.prn'},{'foo'}"
#matlab_batcher.sh plotAll "'$DIR',NaN,{'p05id.prn','p005id.prn'},{'foo'}"
#find . -name "*.png" | xargs -n1 -I{} convert {} -trim {}new
trim.sh $DIR
find $DIR -name "*.eps" | xargs rm -v
$HOME/Development/script_inception_public/special_ops/SO_delimages.py $DIR p001id.png
#$HOME/Development/script_inception_public/special_ops/SO_delimages.py $DIR p005id.png
#$HOME/Development/script_inception_public/special_ops/SO_reportGenerator.py -t $title -o $texfile p001id.png !(p001id).png
