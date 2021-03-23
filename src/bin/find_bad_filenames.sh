#!/bin/bash

FILELIST=$(mktemp)
FINAL="${FILELIST}.sorted.uniq"

# https://unix.stackexchange.com/questions/572592/finding-files-with-and-asterisk-in-the-file-name
find . -name "*[\*]*" >>${FILELIST}
find . -name "*:*" >>${FILELIST}
find . -name "*>*" >>${FILELIST}
find . -name "*<*" >>${FILELIST}
# find . -name "*\?*" >>${FILELIST}
find . -name '*`*' >>${FILELIST}
find . -name '*\\*' >>${FILELIST}
find . -name "*£*" >>${FILELIST}
LC_ALL=C find . -name '*[! -~]*' >>${FILELIST}
# LC_ALL=C find . -name '*[!~]*' >>${FILELIST}
LC_ALL=C find . -name '*[\!]*' >>${FILELIST}
# LC_ALL=C find . -name '*[~]*' >>${FILELIST}
# LC_ALL=C find . -name '*[-]*' >>${FILELIST}
# LC_ALL=C find . -name '*[ ]*' >>${FILELIST}
# LC_ALL=C find . -name '*[\^]*' >>${FILELIST}

sort ${FILELIST} | uniq >${FINAL}

echo "==================================="
cat ${FINAL}
echo "==================================="
echo "FILELIST = ${FILELIST} FINAL = ${FINAL}"
echo "NFILES = $(wc -l ${FINAL})"
echo "==================================="
