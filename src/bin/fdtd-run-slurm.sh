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
TEMPLATE=$SCRIPTDIR/../templates/lumerical-fdtd-slurm-template.sh

#Determine number of processes to use. Default is 8 if no -n argument is
#given
PROCS=4
SCRIPTONLY=false
PRINTSCRIPTONLY=false
SPECIFYJOBNAME=false
SBATCHOPTIONS=""
TEMPLATEOPTIONS=""

print_help() {
  echo "usage :"
  echo "`basename $0` [-ps|--print-script-only] [-s|--create-script-only] [-n PROCS] [-t WALLTIME] [-j JOBNAME] [-p PARTITION] [-m MEM_IN_MB] FILE1.fsp FILE2.fsp FILE3.fsp ..."
}

POSITIONAL_ARGS=()

while [[ $# -gt 0 ]]; do
  case $1 in
    -n)
      PROCS=${2}
      shift
      shift
      ;;
    -t|--time)
      WALLTIME=${2}
      shift
      shift
      ;;
    -j|--job-name)
      JOBNAME=${2}
      shift
      shift
      ;;
    -p|--partition)
      PARTITION=${2}
      shift
      shift
      ;;
    -m|--mem)
      MEM_IN_MB=${2}
      shift
      shift
      ;;
    -s|--create-script-only)
      SCRIPTONLY=true
      shift
      ;;
    -ps|--print-script-only)
      PRINTSCRIPTONLY=true
      shift
      ;;
    -h|--help)
      print_help
      exit
      ;;
    -*|--*)
      echo "Unknown option $1"
      exit 1
      ;;
    *)
      POSITIONAL_ARGS+=("$1") # save positional arg
      shift # past argument
      ;;
  esac
done

set -- "${POSITIONAL_ARGS[@]}" # restore positional parameters

# Check if all parameters are present
# If no, exit
if [ $# -lt 1 ]
then
  print_help;
  exit 0
fi

echo "-------------------------"
echo "PROCS: ${PROCS}"
echo "SCRIPTONLY: ${SCRIPTONLY}"
echo "PRINTSCRIPTONLY: ${PRINTSCRIPTONLY}"
if [ -z ${WALLTIME+x} ]
then
  echo "WALLTIME is unset";
else
  echo "WALLTIME: ${WALLTIME}"
  SBATCHOPTIONS="${SBATCHOPTIONS} --time=${WALLTIME}"
fi
if [ -z ${JOBNAME+x} ]
then
  echo "JOBNAME is unset";
else
  echo "JOBNAME: ${JOBNAME}"
  SBATCHOPTIONS="${SBATCHOPTIONS} --job-name=${JOBNAME}"
fi
if [ -z ${PARTITION+x} ]
then
  echo "PARTITION is unset";
else
  echo "PARTITION: ${PARTITION}"
  SBATCHOPTIONS="${SBATCHOPTIONS} --partition=${PARTITION}"
fi
if [ -z ${MEM_IN_MB+x} ]
then
  echo "MEM_IN_MB is unset";
else
  echo "MEM_IN_MB: ${MEM_IN_MB}"
  TEMPLATEOPTIONS="${TEMPLATEOPTIONS} -mem ${MEM_IN_MB}"
fi
echo "TEMPLATEOPTIONS: ${TEMPLATEOPTIONS}"
echo "SBATCHOPTIONS: ${SBATCHOPTIONS}"
echo "FILES: ${@}"
echo "-------------------------"

# default return code
ret_code=0

#For each fsp file listed on the command line, generate the
#submission script and submit it with qsub
while(( $# > 0 ))
do

    #Generate the submission script by replacing the tokens in the template
    #Addional arguments  can be added to fdtd-process-template to fine tune
    #the memory and time estimates. See comments in that file for details.
    SHELLFILE=${1%.fsp}.sh
    if ${PRINTSCRIPTONLY}
    then
      # echo "${SCRIPTDIR}/fdtd-process-template-slurm.sh ${1} ${TEMPLATE} ${PROCS}"
      ${SCRIPTDIR}/fdtd-process-template-slurm.sh ${TEMPLATEOPTIONS} ${1} ${TEMPLATE} ${PROCS}
      exit
    else
      ${SCRIPTDIR}/fdtd-process-template-slurm.sh ${TEMPLATEOPTIONS} ${1} ${TEMPLATE} ${PROCS} > $SHELLFILE
    fi

    if ! ${SCRIPTONLY}
    then
      #Submit the job scrtipt using qsub
      echo "Submitting: ${SHELLFILE}"
      cd $(dirname ${SHELLFILE})
      sbatch ${SBATCHOPTIONS} $(basename ${SHELLFILE})
    fi

    if test $? -ne 0
    then
      ret_code=$((ret_code+1))
    fi

    if ! [ -z ${OLDPWD+x} ]; # only cd back to previous directory if cd was used before
    then
      cd - >/dev/null
    fi

shift
done

exit $ret_code
