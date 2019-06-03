#!/bin/bash

for eps1 in 13 12 1
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
