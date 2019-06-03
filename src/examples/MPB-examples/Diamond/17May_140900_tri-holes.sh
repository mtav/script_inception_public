# submit to default que
#PBS -l walltime=360:00:00,nodes=2:ppn=8
#PBS -j oe
export RUNDIR="ANONYMIZED/ANONYMIZED/Simulations/MPB/test/" 

# Name of application --------------------------------------------------- 
export APPLICATION="/usr/local/bin/mpb"


# Any required run flags/input/output files etc. -------------------------------

export RUNFLAGS="ANONYMIZED/ANONYMIZED/Simulations/MPB/test/tri-holes.ctl > ANONYMIZED/ANONYMIZED/Simulations/MPB/test/tri-holes.ctl.out"

# Change into the working directory -------------------------------------

cd $RUNDIR

# Generate the list of nodes the code will run on -----------------------

cat $PBS_NODEFILE
export nodes=`cat $PBS_NODEFILE`
export nnodes=`cat $PBS_NODEFILE | wc -l`

export confile=inf.$PBS_JOBID.conf

for i in $nodes; do
   echo ${i} >>$confile
done

# Execute the code ------------------------------------------------------

mpirun -np $nnodes -machinefile $confile $APPLICATION $RUNFLAGS

