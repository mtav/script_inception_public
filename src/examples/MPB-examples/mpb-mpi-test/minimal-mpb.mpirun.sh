#!/bin/bash
# request resources:
#PBS -l nodes=1:ppn=2
#PBS -l walltime=01:00:00
#PBS -q veryshort

module load apps/mpb-1.5-mpi

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
which mpb-mpi
which mpirun
ldd $(which mpb-mpi)
module list

echo "=== env ==="
env
echo "==========="

env > ./env.qsub.log

echo "MPIRUN_RANK = ${MPIRUN_RANK}"

# create a machine file for subsequent use with mpirun:
cat $PBS_NODEFILE > machine.file.$PBS_JOBID
# count the available processors:
numprocs=`wc $PBS_NODEFILE | awk '{print $1}'`
# launch the program using mpirun:
mpirun -np $numprocs -machinefile machine.file.$PBS_JOBID mpb-mpi ./minimal-mpb.ctl
h5tovtk minimal-mpb-epsilon.h5
h5topng -0 -x0 minimal-mpb-epsilon.h5
