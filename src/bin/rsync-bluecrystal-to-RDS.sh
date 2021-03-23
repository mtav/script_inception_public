#!/bin/bash

# default options
INTERACTIVE=1
REMOVESRCDIR=0
DSDIFFCHECK=1

# usage
print_usage() {
  printf -- "Usage:\n"
  printf -- "  $(basename ${0}) ACCOUNT DIR\n"
  printf -- "  $(basename ${0}) -a ACCOUNT DIR\n"
  printf -- "  $(basename ${0}) -r ACCOUNT DIR\n"
  printf -- "  $(basename ${0}) -s ACCOUNT DIR\n"
  printf -- "  $(basename ${0}) -a -r ACCOUNT DIR\n"
  printf -- "Arguments:\n"
  printf -- "  ACCOUNT: user@host\n"
  printf -- "  DIR: directory to rsync (relative path to host home directory)\n"
  printf -- "  -a: automatic mode (no command confirmation prompts)\n"
  printf -- "  -r: remove source directory after successful rsync\n"
  printf -- "  -s: skip ds-diff.sh check\n"
}

TEMP=$(getopt -o 'ars' -n 'rsync-bluecrystal-to-RDS.sh' -- "$@")

if [ $? -ne 0 ]; then
  print_usage >&2
  exit 1
fi

# Note the quotes around "$TEMP": they are essential!
eval set -- "$TEMP"
unset TEMP

while true; do
  case "$1" in
    '-a')
      INTERACTIVE=0
      shift
      continue
    ;;
    '-r')
      REMOVESRCDIR=1
      shift
      continue
    ;;
    '-s')
      DSDIFFCHECK=0
      shift
      continue
    ;;
    '--')
      shift
      break
    ;;
    *)
      echo 'Internal error!' >&2
      exit 1
    ;;
  esac
done

echo "=== options ==="
echo "INTERACTIVE=${INTERACTIVE}"
echo "REMOVESRCDIR=${REMOVESRCDIR}"
echo "DSDIFFCHECK=${DSDIFFCHECK}"
echo "==============="

# enable exit on error or unbound
set -eu

myprompt()
{
  if [[ ${INTERACTIVE} -eq 1 ]]
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

if [[ ${DSDIFFCHECK} -eq 1 ]]
then
  echo "ds-diff.sh ${HOME}/local_mount/${ACCOUNT}/${DIR}/ ${DSTDIR}"
  myprompt
  ds-diff.sh ${HOME}/local_mount/${ACCOUNT}/${DIR}/ ${DSTDIR}
fi

echo "======================================================================================"
echo "If everything was successful, you may now run this command to remove the source files:"
echo "rsync ${FLAGS} --remove-source-files ${SSH_SRCDIR} ${DSTDIR}"
if [[ ${REMOVESRCDIR} -eq 1 ]]
then
  myprompt
  rsync ${FLAGS} --remove-source-files ${SSH_SRCDIR} ${DSTDIR}
fi
