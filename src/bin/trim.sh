#!/bin/bash

# for auto-cropping/trimming images
#
# cf also:
# http://askubuntu.com/questions/351767/how-to-crop-borders-white-spaces-from-image
# find . -name "*.png" | xargs mogrify -trim 
#
# TODO: Get rid of the ghostscript stuff if possible. Simple "convert OLD -trim NEW" for multiple files should be enough.
# TODO: Use input arguments, CLI options, etc (python?)

set -eux

trimit()
{
  OLDFULL=$1
  localdir=$(dirname $OLDFULL)
  cd $localdir
  OLD=$(basename $OLDFULL)
  NEW=$(basename $OLD .eps).png
  gs -r300 -dEPSCrop -dTextAlphaBits=4 -sDEVICE=png16m -sOutputFile=$NEW -dBATCH -dNOPAUSE $OLD
  convert $NEW -trim $NEW
  cd -
}

#trimit $1
#find . -name "*.eps" | xargs -n1 -I{} trimit() {}

DIR=$(readlink -f $1)

find $DIR -name "*.eps"  | while read FILENAME;
do
  trimit $FILENAME
done

# convert image1.png \( image2.png  image3.png -append \) -gravity center +append out.png
#ls -d */resonance/*/ | xargs -n1 -I{} ~/Development/script_inception_public/special_ops/SO_delimages.py {}
