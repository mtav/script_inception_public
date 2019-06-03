#!/bin/bash
# request resources:
#PBS -l nodes=1:ppn=1
#PBS -l walltime=01:00:00
#PBS -q testq

# on compute node, change directory to 'submission directory':
cd $PBS_O_WORKDIR
# record some potentially useful details about the job:
echo Running on host `hostname`
echo Time is `date`
echo Directory is `pwd`
echo PBS job ID is $PBS_JOBID
echo This jobs runs on the following machines:
echo `cat $PBS_NODEFILE | uniq`

which guile
which meep-mpi
ldd /cm/shared/apps/Meep-1.2/bin/meep-mpi
module list

echo "=== env ==="
env
echo "==========="

env > ./env.qsub.log

# count the number of processors available:
numprocs=`wc $PBS_NODEFILE | awk '{print $1}'`
# launch the program using mpiexec:
mpiexec -np $numprocs meep-mpi ./minimal-meep.ctl
