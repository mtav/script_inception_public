#!/bin/bash
# This script is used to replace tags in a template script file with actual
# values for an FDTD Solutions project file. The script is called with the following
# arguments:
#
# fdtd-process-template.sh [options] <fsp file> <temaplate file> <#processes>
#
# Valid options are:
#
# -r <rate>            The simulation rate in MNodes/s used in time estimates.
#                      If no option is given the default is 4MNodes/s/process
#                      which is very conservative
#
# -tm <min_time>       The minimum time in seconds that the simulation can take. If no option
#                      is given the default is 600 seconds.
#
# -ms <memory_safety>  A multiplicative factor to apply to the memory estimate in %.
#                      If no option is given the default value is 110
#
# -mm <memory_min>     The minimum memory that a process can use. If no option 
#                      is given the default is 1024MB.
#
# -tmm <memory_min>    The minimum total memory that a job can use. If no option 
#                      is given the default is 1024MB.
#
# The script will replace the following tokens in the template file with specified values
#
# Token                Value
# <total_memory>       The total memory required by all processes
# <processor_memory>   The memory required for each simuilation process
# <hours>              The total hours required for the simulation
# <minutes>            The total minutes required for the simulation
# <seconds>            The total seconds required for the simulation
# <n>                  The number of processes to use
# <dir_fsp>            The path of the fsp project file
# <filename>           The name of the fsp project file, without a leding path
#
############################################################################################

#Rate default
RATE=4

#Minimum time default
TIME_MIN=600

#Memory safety default
MEMORY_SAFETY=110

#Minimum memory default
PROC_MEMORY_MIN=1024
TOTAL_MEMORY_MIN=1024

#Process command line options
while [ $# -gt 3 ] ; do
    case $1 in
        -r) RATE=$2
         ;;
        -tm) TIME_MIN=$2
         ;;
        -ms) MEMORY_SAFETY=$2
         ;;
        -mm) PROC_MEMORY_MIN=$2
         ;;
        -tmm) TOTAL_MEMORY_MIN=$2
         ;;
    esac
    shift
    shift
done

#Number of processes
PROCS=$3
# echo $PROCS
# echo $RATE
# echo $TIME_MIN
# echo $MEMORY_SAFETY
# echo $PROC_MEMORY_MIN
# echo $TOTAL_MEMORY_MIN

#Path of fsp file
DIRFSP=`dirname $1`

#fsp file name without path
FILENAME=`basename $1`

#Run FDTD to get stats from project file
#SCRIPTDIR='/cm/shared/apps/Lumerical-FDTD-2020a-r2/bin/'
#$SCRIPTDIR/fdtd-engine-mpich2nem -mr $1 > $1.tmp
module load apps/lumerical/2021-R2

# create memory requirement file
fdtd-engine-mpich2nem -mr $1 > $1.tmp

#Estimated memory
ESTMEM=`grep memory $1.tmp | sed 's/^.*=//'`

#Total memory required
TOTALMEM=$(( ESTMEM * MEMORY_SAFETY / 100 ))

#Memory required perprocess
PROCMEM=$((TOTALMEM / PROCS))
# echo "=====> PROC_MEMORY_MIN: $PROC_MEMORY_MIN"
# echo "=====> TOTAL_MEMORY_MIN: $TOTAL_MEMORY_MIN"
if test "$PROCMEM" -lt "$PROC_MEMORY_MIN"; then
    PROCMEM=$PROC_MEMORY_MIN
fi
if test "$TOTALMEM" -lt "$TOTAL_MEMORY_MIN"; then
    TOTALMEM=$TOTAL_MEMORY_MIN
fi
# echo "=====> PROCMEM: $PROCMEM"
# echo "=====> TOTALMEM: $TOTALMEM"

#Gridpoints
GRIDPTS=`grep gridpoints $1.tmp | sed 's/^.*=//'`

#Timesteps
TIMESTEPS=`grep time_steps $1.tmp | sed 's/^.*=//'`

#Estimated time
TIME=$(( GRIDPTS * TIMESTEPS / PROCS / RATE / 1000000 ))
if [ "$TIME" -lt "$TIME_MIN" ]; then
    TIME=$TIME_MIN
fi

HOUR=$((TIME / 3600))
MINSEC=$((TIME - HOUR * 3600))
MIN=$((MINSEC / 60))
SEC=$((MINSEC - MIN * 60))


#The replacements
sed -e "s#<total_memory>#$TOTALMEM#g" \
    -e "s#<processor_memory>#$PROCMEM#g" \
    -e "s#<hours>#$HOUR#g" \
    -e "s#<minutes>#$MIN#g" \
    -e "s#<seconds>#$SEC#g" \
    -e "s#<n>#$PROCS#g" \
    -e "s#<dir_fsp>#$DIRFSP#g" \
    -e "s#<filename>#$FILENAME#g" \
    $2
