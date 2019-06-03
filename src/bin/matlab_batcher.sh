#!/bin/bash
# source : http://stackoverflow.com/questions/2001183/how-to-call-matlab-functions-from-linux-command-line

set -x

TMP=$(mktemp)
matlab_exec=matlab
X="${1}(${2})"
echo ${X} > $TMP
cat $TMP
#${matlab_exec} -nojvm -nodisplay -nosplash < $TMP
${matlab_exec} -nodesktop -nodisplay -nosplash < $TMP
rm $TMP
