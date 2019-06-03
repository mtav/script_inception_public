#!/bin/bash
#
#PBS -l walltime=1:00:00
#PBS -mabe
#PBS -joe
#


export WORKDIR=$JOBDIR
export EXE=fdtd

cd $WORKDIR

$EXE minimal-bfdtd.in > minimal-bfdtd.out
