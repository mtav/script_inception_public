#!/bin/bash
set -eu

function list_queued()
{
  qstat | grep $USER | grep ' Q '
}

function qdel_queued()
{
  list_queued | awk -F. '{print $1}' | xargs -n1 qdel
}

echo "delete all queued jobs (not running ones)? (y/n)"
read ans
case $ans in
  y|Y|yes) qdel_queued;;
  *) echo "Not doing anything. But would normally delete the following jobs:"; list_queued;;
esac
