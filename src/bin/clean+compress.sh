#!/bin/bash
# helper script to remove empty files and compress large text files in order to reduce size of backed up data
# Note: Using gzip in the find command might be faster, but having a progress bar is nice too...

set -eu

function datefull()
{
  date +%Y%m%d_%H%M%S
}

# Check if all parameters are present
# If no, exit
if [ $# -ne 1 ]
then
        echo "usage :"
        echo "`basename $0` source_directory"
        exit 0
fi

source_directory=${1}
STAMP=$(datefull)

echo "=== source_directory=${source_directory} ==="
# source_directory=$(readlink -f ${source_directory})
# echo "--> source_directory=${source_directory}"
echo "Proceed? (y/n)"
read ans
if [[ $ans != "y" ]]
then
  echo "Exiting."
  exit
fi

FILELIST=${source_directory}/${STAMP}.tocompress.log
LOGFILE=${source_directory}/${STAMP}.clean+compress.log

echo "=== remove empty files and directories ===" >>${LOGFILE} 2>&1
find ${source_directory} -empty -print -delete >>${LOGFILE} 2>&1

echo "=== find files to compress ===" >>${LOGFILE} 2>&1
# find ${source_directory} -type f -name "*.prn" | tee ${FILELIST}
find ${source_directory} -type f -size +100c -and \( -name "*.prn" -or -name "*.geo" -or -name "*.inp" -or -name "*.out" -or -name "*.dat" -or -name "*.txt" -or -name "*.str" -or -name "*.gwl" \) | tee ${FILELIST}

echo "=== find empty files ===" >>${LOGFILE} 2>&1
find ${source_directory} -type f -empty | tee ${source_directory}/${STAMP}.empty.files.log

echo "=== find empty directories ==="
find ${source_directory} -type d -empty | tee ${source_directory}/${STAMP}.empty.directories.log

echo "=== run gzip check ==="
gzip.py --exe=pigz --force --check --logfile="${FILELIST}.gzip" --from-file ${FILELIST}

echo "LOGFILE = ${LOGFILE}"
