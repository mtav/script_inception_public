#!/bin/bash
set -eu

function checkIfDone() {
  FSP=${1}
  SHELLFILE=${1%.fsp}.sh

  if grep finished ${SHELLFILE}.o* &> /dev/null
  then
    return 0
  else
    return 1
  fi
}

function resubmit() {
  FSP=${1}
  SHELLFILE=${1%.fsp}.sh

  if grep finished ${SHELLFILE}.o* &> /dev/null
  then
    echo "${FSP} : DONE"
  else
    echo "${FSP} : RESUBMITTING"
    rm -fv ${SHELLFILE}.o* ${SHELLFILE}.e*
    fdtd-run-pbs.sh ${FSP}
  fi
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
    F=$((F + 1))
  fi
  N=$((N + 1))
done

echo "======================================"
echo "SUCCESS: ${S}/${N}, FAILURE: ${F}/${N}"
