#!/bin/bash

set -eu

FLAGS_COMMON="--archive --compress"
FLAGS_WINDOWS="--no-perms --no-group --no-links --chmod=ugo=rwX"
FLAGS_EXTRA="--info=progress2 --exclude '.ssh'"
FLAGS_REMOVE="--remove-source-files"

FLAGS_MAIN="${FLAGS_COMMON} ${FLAGS_WINDOWS} ${FLAGS_EXTRA}"

ACCOUNT=$1
echo "ACCOUNT=${ACCOUNT}"
shift
# exit

SRC_MOUNTED_DIR="${HOME}/local_mount/${ACCOUNT}"
SRC_SSH_DIR="${ACCOUNT}:~"
DST_BASE="${HOME}/RDS/${ACCOUNT}"

# test -d ${SRC_MOUNTED_DIR}
# echo OK
# ssh ${ACCOUNT} "[ -d ~ ]"
# echo OK
# test -d ${DST_BASE}
# echo OK

# echo ${SRC_MOUNTED_DIR}
# echo ${SRC_SSH_DIR}
# echo ${DST_BASE}

proceed()
{
  echo "Proceed $1"
  read ans
  case ${ans} in
    y) echo "Proceeding.";;
    *) exit;;
  esac
}

rsync_action()
{
  REMOTE_SRC_DIR="${1}/"
  DST="${2}/"
#   test -d "${SRC}"
#   test -d "${DST}"
  
  SRC="${ACCOUNT}:~/${REMOTE_SRC_DIR}"
  echo "${SRC} -> ${DST}"
  
  if ! (ssh ${ACCOUNT} "[[ -d ~/${REMOTE_SRC_DIR} ]]")
  then
    echo "Source directory does not exist!"
    exit
  fi
  if [[ ! -d "${DST}" ]]
  then
    echo "Destination directory does not exist!"
    exit
  fi

#   echo OK
#   exit
  
#   if test -d "${SRC}" && test -d "${DST}"
#   then
  echo "SRC = ${SRC}"
  echo "DST = ${DST}"

  echo rsync ${FLAGS_MAIN} "${SRC}" "${DST}"
  proceed "with rsync?"
  rsync ${FLAGS_MAIN} "${SRC}" "${DST}"
  
  echo rsync ${FLAGS_MAIN} ${FLAGS_REMOVE} "${SRC}" "${DST}"
  proceed "with rsync --remove-source-files?"
  rsync ${FLAGS_MAIN} ${FLAGS_REMOVE} "${SRC}" "${DST}"
  
  proceed "remove empty source directories?"
  ssh ${ACCOUNT} "find ${REMOTE_SRC_DIR} -empty -type d -delete"
#   proceed "with removeEmptyDirectories.py?"
#   removeEmptyDirectories.py "${SRC}"
#   
#   proceed "with rmdir?"
#   rmdir "${SRC}"
#   else
#     echo "Source or destination directory does not exist!"
#     exit
#   fi
}

for REMOTE_SRC_DIR in "$@"
do
  rsync_action "${REMOTE_SRC_DIR}" "${DST_BASE}/${REMOTE_SRC_DIR}"
done
