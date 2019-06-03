#!/usr/bin/env python

# TODO: Finish or remove. Non-working code.

import re
import os
import sys

if __name__ == '__main__':
  pass

  # TODO: Unported bash code follows...
  # store arguments in variables
  #DIR = os.path.abspath(sys.argv[1])
  #if not os.path.isdir(DIR):
    #sys.exit(-1)

  #PROBEINDEX = sys.argv[2]

  ## create probe names
  #PROBENAME1=$(printf "p%02did.prn" $PROBEINDEX)
  #PROBENAME2=$(printf "p%03did.prn" $PROBEINDEX)
  #PROBENAME3=$(printf "p%02did.png" $PROBEINDEX)
  #PROBENAME4=$(printf "p%03did.png" $PROBEINDEX)

  ## run matlab plotAll
  #matlab_batcher.sh plotAll "'$DIR',NaN,{'$PROBENAME1','$PROBENAME2'},{'foo'}"

  ##find . -name "*.png" | xargs -n1 -I{} convert {} -trim {}new

  ## trim the pictures
  #trim.sh $DIR
  #============
  ##!/bin/bash

  #set -eux

  #trimit()
  #{
    #OLDFULL=$1
    #localdir=$(dirname $OLDFULL)
    #cd $localdir
    #OLD=$(basename $OLDFULL)
    #NEW=$(basename $OLD .eps).png
    #gs -r300 -dEPSCrop -dTextAlphaBits=4 -sDEVICE=png16m -sOutputFile=$NEW -dBATCH -dNOPAUSE $OLD
    #convert $NEW -trim $NEW
    #cd -
  #}

  ##trimit $1
  ##find . -name "*.eps" | xargs -n1 -I{} trimit() {}

  #DIR=$(readlink -f $1)

  #find $DIR -name "*.eps"  | while read FILENAME;
  #do
    #trimit $FILENAME
  #done

  ## convert image1.png \( image2.png  image3.png -append \) -gravity center +append out.png
  ##ls -d */resonance/*/ | xargs -n1 -I{} ~/Development/script_inception_public/special_ops/SO_delimages.py {}
  #============

  ## remove .eps pictures
  #find $DIR -name "*.eps" | xargs rm -v

  ## merge pictures and create report
  ##TODO: Handle cases where it is p01 or p001
  #if [ -f  ]
  #$HOME/Development/script_inception_public/special_ops/SO_delimages.py $DIR $PROBENAME3
  #$HOME/Development/script_inception_public/special_ops/SO_delimages.py $DIR $PROBENAME4

  ##$HOME/Development/script_inception_public/special_ops/SO_reportGenerator.py -t $title -o $texfile image.png !(image).png
