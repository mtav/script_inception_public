#!/bin/bash

set -eux

export PYTHONPATH=${HOME}/opt/lib/python2.7/site-packages/

# function submit_job()
# {
#   N_LOG=$1
#   N_OUTER=$2
#   echo $N_LOG $N_OUTER
#   BASE="maximize_woodpile_bandgap.nlog_$N_LOG.nouter_$N_OUTER"
#   qsub -N "$BASE.sh" -o "$BASE.log" -joe -v JOBDIR=$(readlink -f .),N_LOG=$N_LOG,N_OUTER=$N_OUTER ./maximize_woodpile_bandgap.sh
# }
# 
# Nlist="1 1.52 2.1 2.4 3.3 3.5"
# for nlog in $Nlist
# do
#     submit_job $nlog $nouter
# done
# 
# epsilon

# epsilon=4.1
# n_inside=
# n_outside=

# epsilon_inside=3.00
# epsilon_outside=12.50

# epsilon_inside=12.50
# epsilon_outside=3.00

epsilon_inside=1.52
epsilon_outside=1.00

outfile_basename="tapsterite_epsilon_inside-${epsilon_inside}_epsilon_outside-${epsilon_outside}"

# ./quick_tapsterite.sh ~/Development/tapsterite/MPBruns/tapsteriteForMPB.stl
stlfile="$1"
#stlfile="tapsteriteForMPB.stl"

./h5_vtk_stl_converters.py ${stlfile} ${epsilon_inside} ${epsilon_outside} "${outfile_basename}"

outfile="${outfile_basename}.out"
h5file="${outfile_basename}.h5"

cp -v ${h5file} "foo.h5"

mpb diamond.ctl | tee ${outfile}

mpb-data -x3 -y3 -z3 -r epsilon.h5
h5tovtk -d data-new epsilon.h5
# paraview epsilon.vtk
postprocess_mpb.sh ${outfile}
