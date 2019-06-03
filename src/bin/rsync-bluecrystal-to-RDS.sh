#!/bin/bash

set -eu

INTERACTIVE=1

myprompt()
{
  if [[ $INTERACTIVE -eq 1 ]]
  then
    read -n1 -r -p "Press any key to continue..." key
  fi
}

ACCOUNT=$1
DIR=${2:-}

echo "ACCOUNT = ${ACCOUNT}"
echo "DIR = ${DIR}"

if test -z ${DIR}
then
  DSTDIR="${HOME}/RDS/${ACCOUNT}/"
  SSH_SRCDIR="${ACCOUNT}:~/"
  MOUNTED_SRCDIR="${HOME}/local_mount/${ACCOUNT}/"
else
  DSTDIR="${HOME}/RDS/${ACCOUNT}/${DIR}/"
  SSH_SRCDIR="${ACCOUNT}:~/${DIR}/"
  MOUNTED_SRCDIR="${HOME}/local_mount/${ACCOUNT}/${DIR}/"
fi
echo "DSTDIR = ${DSTDIR}"
echo "SSH_SRCDIR = ${SSH_SRCDIR}"
echo "MOUNTED_SRCDIR = ${MOUNTED_SRCDIR}"

myprompt

if ! ssh ${ACCOUNT} echo
then
  echo "ERROR: ssh ${ACCOUNT} failed"
  exit 1
fi

if ! ssh ${ACCOUNT} test -d ${DIR}
then
  echo "ERROR: ${DIR} not found on ${ACCOUNT}"
  exit 1
fi

FLAGS="--archive --compress --no-perms --no-group --no-links --chmod=ugo=rwX --info=progress2 --exclude '.ssh'"

echo "mkdir --parents ${DSTDIR}"
myprompt
mkdir --parents ${DSTDIR}

echo "rsync ${FLAGS} ${SSH_SRCDIR} ${DSTDIR}"
myprompt
rsync ${FLAGS} ${SSH_SRCDIR} ${DSTDIR}

echo "ds-diff.sh ${HOME}/local_mount/${ACCOUNT}/${DIR}/ ${DSTDIR}"
myprompt
ds-diff.sh ${HOME}/local_mount/${ACCOUNT}/${DIR}/ ${DSTDIR}

echo "======================================================================================"
echo "If everything was successful, you may now run this command to remove the source files:"
echo "rsync ${FLAGS} --remove-source-files ${SSH_SRCDIR} ${DSTDIR}"
# myprompt
# rsync ${FLAGS} --remove-source-files ${SSH_SRCDIR} ${DSTDIR}
