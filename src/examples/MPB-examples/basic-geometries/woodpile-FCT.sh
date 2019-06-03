#!/bin/bash
for c in 1.0 1.1 1.2 1.3 1.4
do
  mpb _c=${c} woodpile-FCT.ctl | tee woodpile-FCT_c-${c}.log
done
mpb woodpile-FCT.ctl | tee woodpile-FCT_c-FCC.log
