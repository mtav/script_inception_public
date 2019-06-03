#!/bin/bash
#
#PBS -l walltime=12:00:00
#PBS -mabe
#PBS -joe
#

export WORKDIR=$JOBDIR
export EXE=fdtd

if [ -z ${PBS_O_WORKDIR+x} ]
then
  echo "PBS_O_WORKDIR is unset"
  export WORKDIR="$(readlink -f $(dirname "${0}"))"
else
  echo "PBS_O_WORKDIR is set"
  # on compute node, change directory to 'submission directory':
  # cd ${PBS_O_WORKDIR}
fi

cd ${WORKDIR}

echo "WORKDIR = ${WORKDIR}"
echo "pwd = $(pwd)"

$EXE sim.in > sim.out
