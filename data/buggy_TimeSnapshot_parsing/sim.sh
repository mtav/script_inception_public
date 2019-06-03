#!/bin/bash
#
#PBS -l walltime=12:00:00
#PBS -mabe
#PBS -joe
#


export WORKDIR=$JOBDIR
export EXE=fdtd

cd $WORKDIR

$EXE sim.in > sim.out
