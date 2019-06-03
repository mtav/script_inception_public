#!/bin/bash

set -eux

#mpb-data -o $1.h5 -m1 -r -n32 $1 && h5tovtk -d data-new epsilon.h5

function h5tovtk_enhanced()
{
  infile=$1; shift;
  outfilebase=$1; shift;
  dataset=$1; shift;
  xperiods=$1; shift;
  yperiods=$1; shift;
  zperiods=$1; shift;
  rectangular=$1; shift;
  resolution=$1

  if $rectangular
  then
    outfile=$outfilebase.x$xperiods.y$yperiods.z$zperiods.r1.n$resolution.h5
    mpb-data -r -x $xperiods -y $yperiods -z $zperiods -n $resolution -d $dataset -o $outfile $infile
  else
    outfile=$outfilebase.x$xperiods.y$yperiods.z$zperiods.r0.n$resolution.h5
    mpb-data    -x $xperiods -y $yperiods -z $zperiods -n $resolution -d $dataset -o $outfile $infile
  fi
  h5tovtk $outfile
}

for infile in "$@"
do
  echo "processing $infile"
  outdir=${infile%.h5}
  base=$(basename $outdir)
  mkdir -p $outdir

  resolution=32
  dataset=data

  h5tovtk_enhanced $infile $outdir/$base $dataset 1 1 1 false $resolution
  h5tovtk_enhanced $infile $outdir/$base $dataset 1 1 1 true  $resolution
  h5tovtk_enhanced $infile $outdir/$base $dataset 5 5 5 false $resolution
  h5tovtk_enhanced $infile $outdir/$base $dataset 5 5 5 true  $resolution

done

# echo ${ko%.h5}
# 
#   mpb-data -x1 -y1 -z1 -r -n32 -d data -o epsilon1.x1.y2.z3.r1.n32.h5:koko epsilon1.h5
# 
#   mpb-data -m5 -r -n32 $i
#   h5tovtk -d data-new $i
# 
# mpb-data -x1 -y2 -z3 -r -n32 -d data -o epsilon1.x1.y2.z3.r1.n32.h5:koko epsilon1.h5

# NOTE: Have a look at h5copy and other h5 tools to create maybe just 1 or 2 files instead of so many. ;)
