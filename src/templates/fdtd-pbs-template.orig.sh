#PBS -S /bin/bash
#PBS -l mem=<total_memory>mb
#PBS -l walltime=<hours>:<minutes>:<seconds>
#PBS -l procs=<n>
#PBS -l software=FDTD
#PBS -l qos=parallel

cd $PBS_O_WORKDIR
module load lumerical
NUM_PROCS=`/bin/awk 'END {print NR}' $PBS_NODEFILE`
echo "Starting run at: `date`"
echo "Running on $NUM_PROCS processors."
MY_PROG="/opt/lumerical/v212/bin/fdtd-engine-mpich2nem"
INPUT="<filename>"
/opt/lumerical/v212/mpich2/nemesis/bin/mpiexec.hydra -n $NUM_PROCS $MY_PROG -t 1 ./${INPUT}
echo "Job finished at: `date`"
exit
