#!/bin/bash

set -eu

echo "=== MPB run ==="
for ((eps1=1;eps1<=13;eps1++));
do
  BASENAME="DBR-stack_${eps1}-13"
  mpb eps1=${eps1} eps2=13 DBR-stack.ctl | tee ${BASENAME}.out
  postprocess_mpb.sh ${BASENAME}.out
done
echo "-----> MPB run complete"

echo "=== h5tovtk run ==="
for ((eps1=1;eps1<=13;eps1++));
do
  BASENAME="DBR-stack_${eps1}-13"
  echo ${BASENAME}
  for N in 1 2
  do
    echo "N=${N}"
    h5tovtk -d data ${BASENAME}-epsilon.h5
    h5tovtk -d z.r ${BASENAME}-e.k23.b0${N}.tm.h5
    h5tovtk -d z.r ${BASENAME}-d.k23.b0${N}.tm.h5
    h5tovtk -d z.r ${BASENAME}-h.k23.b0${N}.tm.h5
    h5tovtk -d data ${BASENAME}-dpwr.k23.b0${N}.tm.h5
    h5tovtk -d data ${BASENAME}-hpwr.k23.b0${N}.tm.h5
  done
done
echo "-----> h5tovtk run complete"

# 
# h5tovtk -d z.r ${BASENAME}-e.k23.b02.tm.h5
# h5tovtk -d z.r ${BASENAME}-d.k23.b02.tm.h5
# h5tovtk -d z.r ${BASENAME}-h.k23.b02.tm.h5
# h5tovtk -d data ${BASENAME}-dpwr.k23.b02.tm.h5
# h5tovtk -d data ${BASENAME}-hpwr.k23.b02.tm.h5
# 
#   cmd='h5tovtk -d z.r ',BASENAME,'-e.k23.b01.tm.h5'];
#   system(cmd);
# 
# h5tovtk -d z.r DBR-stack-e.k23.b02.tm.h5
#   
#   DBR-stack_1-13-d.k23.b03.tm.h5
#   DBR-stack_1-13-dpwr.k23.b02.tm.h5
#   DBR-stack_1-13-hpwr.k23.b03.tm.h5
#   DBR-stack_1-13-h.k23.b02.tm.h5
