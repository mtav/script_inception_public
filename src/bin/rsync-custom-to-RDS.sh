#!/bin/bash
set -eu

DIR=$1

SRC=${HOME}/ANONYMIZED@BC2/DATA
DST=${HOME}/RDS/ANONYMIZED@BC2/DATA

FLAGS="--archive --compress --no-perms --no-group --no-links --chmod=ugo=rwX --info=progress2 --exclude '.ssh' --update"

rsync ${FLAGS} ${SRC}/${DIR} ${DST}/
ds-diff.sh ${SRC}/${DIR}/ ${DST}/${DIR}/
rsync ${FLAGS} --remove-source-files  ${SRC}/${DIR} ${DST}/
removeEmptyDirectories.py ${SRC}/${DIR}/
