#!/bin/bash
########## SLURM SBATCH OPTIONS
#SBATCH --partition=cpu                    # replace with one of options - veryshort (6 hours limit), cpu (10 days limit), test (1 hour limit), hmem (when v.high RAM is needed)
#SBATCH --mem=<total_memory>M              # Specify the real memory required per node. Default units are megabytes. Different units can be specified using the suffix [K|M|G|T].
#SBATCH --cpus-per-task=<n>                # adjust to number of cores per node
#SBATCH --output=%x.%j.out                 # custom output filename for convenience. %x: job name, %j: job id

########## output SLURM infos:
echo "---> SLURM infos:"
env | grep SLURM

########## Load the FDTD module:
echo "---> Loading modules:"
module load apps/lumerical/2021-R2

########## Define variables:
MPIEXEC=mpiexec
MY_PROG=fdtd-engine-mpich2nem
NUM_PROCS=${SLURM_CPUS_PER_TASK}
INPUT=<filename>

########## cd to the directory the sbatch command was executed in:
cd "${SLURM_SUBMIT_DIR}"

########## output debugging infos:
echo "---> debugging infos:"
echo "Working directory: $(pwd)"
echo "MPIEXEC: $(which ${MPIEXEC})"
echo "MY_PROG: $(which ${MY_PROG})"
echo "NUM_PROCS: ${NUM_PROCS}"
echo "INPUT: ${INPUT}"

########## reset test file
# echo "---> Resetting test file..."
# cp --verbose ${INPUT}.nodata ${INPUT}

########## run executable
echo "---> Running program..."
echo "Starting run at: $(date)"
echo "Running on ${NUM_PROCS} processors."
${MPIEXEC} -n ${NUM_PROCS} ${MY_PROG} ${INPUT}
echo "Job finished at: $(date)"
