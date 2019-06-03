#!/bin/bash
set -eux

function qdel_all()
{
  qstat | grep $USER | awk -F. '{print $1}' | xargs -n1 qdel
}

echo "delete all your jobs? (y/n)"
read ans
case $ans in
  y|Y|yes) qdel_all;;
  *) echo "Not doing anything";;
esac
