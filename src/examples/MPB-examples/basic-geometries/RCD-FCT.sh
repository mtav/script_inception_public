#!/bin/bash
for c in 1.0 1.1 1.2 1.3 1.4
do
  mpb _c=${c} RCD-FCT.ctl | tee RCD-FCT_c-${c}.log
done
mpb RCD-FCT.ctl | tee RCD-FCT_c-FCC.log
