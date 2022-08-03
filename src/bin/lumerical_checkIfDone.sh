#!/bin/bash
set -eu

# speed could be optimized using grep -l and grep -L (matching and non-matching)

function checkIfDone() {
  FSP=${1}
  SHELLFILE=${1%.fsp}.sh
  LUMERICAL_LOGFILE=${1%.fsp}_p0.log

  #if grep finished ${SHELLFILE}.o* &> /dev/null
  if grep "Simulation completed successfully at:" ${LUMERICAL_LOGFILE} &> /dev/null
  then
    return 0
  else
    return 1
  fi
}

function resubmit() {
  FSP=${1}
  SHELLFILE=${1%.fsp}.sh

  rm -fv ${SHELLFILE}.o* ${SHELLFILE}.e*
  fdtd-run-slurm.sh -p veryshort -n 1 -m 1024 -t 01:00:00 ${FSP}

  # if grep finished ${SHELLFILE}.o* &> /dev/null
  # then
    # echo "${FSP} : DONE"
  # else
    # echo "${FSP} : RESUBMITTING"
    # rm -fv ${SHELLFILE}.o* ${SHELLFILE}.e*
    # fdtd-run-pbs.sh ${FSP}
  # fi
}

function getFinished() {
  echo
}

S=0
F=0
N=0
for i in "${@}"
do
  # FSP=${i}
  # SHELLFILE=${i%.fsp}.sh

  # WORKDIR=$(dirname ${FSP})
  # cd ${WORKDIR}

  # if grep finished ${SHELLFILE}.o* &> /dev/null
  # then
    # echo "${FSP} : SUCCESS"
  # else
    # echo "${FSP} : FAILURE"
  # fi
  # resubmit "${i}"
  if checkIfDone "${i}"
  then
    echo "${FSP} : SUCCESS"
    S=$((S + 1))
  else
    echo "${FSP} : FAILURE"
    # resubmit "${FSP}"
    F=$((F + 1))
  fi
  N=$((N + 1))
done

echo "======================================"
echo "SUCCESS: ${S}/${N}, FAILURE: ${F}/${N}"

# return error if at least one file failed
test ${F} -eq 0
