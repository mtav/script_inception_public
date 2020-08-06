#!/bin/bash
# This script will create a PBS style job submission script for
# FDTD Solutions project files using the template provided
# in templates/fdtd-pbs-template.sh. The scripts are then submitted
# with qsub commands. Certain tags in the template file are replaced
# with project specific values that are extrated from the project file.
#
# The calling convention for this script is:
#
# fdtd-run-pbs.sh [-n <procs>] fsp1 [fsp2 ... [fspN]]
#
# The arguments are as follows:
#
# -n        The number of processes to use for the job(s).
#           If no argument is given a default value of 8 is used
#
# fsp*      An FDTD Solutions project file. One is required, but
#           multiple can be specified on one command line
#
# Users may wish to customize this script and the template file to suit their
# cluster setup. If this is done it is recommended to make a local copy of both
# scripts rather than editing them directly. This will prevent lost work during
#  upgrades
#
##########################################################################

#Locate the directory of this script so we can find
#utility scripts and templates relative to this path
SCRIPTDIR=`dirname $(readlink -f $(which --skip-alias $0))`

#The location of the template file to use when submitting jobs
#The line below can be changed to use your own template file
TEMPLATE=$SCRIPTDIR/../templates/fdtd-pbs-template.sh

#Determine number of processes to use. Default is 8 if no -n argument is
#given
PROCS=8
if [ "$1" = "-n" ]; then
    PROCS=$2
    shift
    shift
fi

#For each fsp file listed on the command line, generate the
#submission script and submit it with qsub
while(( $# > 0 ))
do

    #Generate the submission script by replacing the tokens in the template
    #Addional arguments  can be added to fdtd-process-template to fine tune
    #the memory and time estimates. See comments in that file for details.
    SHELLFILE=${1%.fsp}.sh
    $SCRIPTDIR/fdtd-process-template.sh $1 $TEMPLATE $PROCS > $SHELLFILE

    #Submit the job scrtipt using qsub
    echo Submitting: $SHELLFILE
    cd $(dirname $SHELLFILE)
    qsub $(basename $SHELLFILE)
    cd -

shift
done
