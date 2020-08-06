#!/bin/bash
#PBS -S /bin/bash
#PBS -l walltime=<hours>:<minutes>:<seconds>
#PBS -l nodes=1:ppn=8

# Load the FDTD module:
module load apps/lumerical-fdtd-2020a-r2

# cd to the directory the qsub command was executed in
cd $PBS_O_WORKDIR

NUM_PROCS=`/bin/awk 'END {print NR}' $PBS_NODEFILE`
echo "Starting run at: `date`"
echo "Running on $NUM_PROCS processors."
MY_PROG="/cm/shared/apps/Lumerical-FDTD-2020a-r2/bin/fdtd-engine-mpich2nem"
INPUT="<filename>"

/cm/shared/apps/Lumerical-FDTD-2020a-r2/mpich2/nemesis/bin/mpiexec -n $NUM_PROCS $MY_PROG ./${INPUT}

echo "Job finished at: `date`"
exit
