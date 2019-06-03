#!/bin/bash

FILELIST=$(mktemp)
FINAL="${FILELIST}.sorted.uniq"

find . -name "*:*" >>${FILELIST}
find . -name "*>*" >>${FILELIST}
find . -name "*<*" >>${FILELIST}
find . -name "*\?*" >>${FILELIST}
find . -name '*`*' >>${FILELIST}
find . -name '*\\*' >>${FILELIST}
find . -name "*£*" >>${FILELIST}
LC_ALL=C find . -name '*[! -~]*' >>${FILELIST}

sort ${FILELIST} | uniq >${FINAL}

echo "==================================="
cat ${FINAL}
echo "==================================="
echo "FILELIST = ${FILELIST} FINAL = ${FINAL}"
echo "NFILES = $(wc -l ${FINAL})"
echo "==================================="
