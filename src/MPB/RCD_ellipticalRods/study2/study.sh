#!/bin/bash

CTLFILE="ellipctical_RCD.ctl"

singleRun()
{
  w=$1
  h=$2
  inside_index=$3
  outside_index=$4
  
  PREFIX="w-${w}_h-${h}_inside-index-${inside_index}_outside-index-${outside_index}"
  
#   mpb w=${w} h=${h} inside-index=${inside_index} outside-index=${outside_index} filename-prefix=\"${PREFIX}-\" ${CTLFILE} &> ${PREFIX}.out
#   mpb mesh-size=1 w=${w} h=${h} inside-index=${inside_index} outside-index=${outside_index} filename-prefix=\"${PREFIX}-\" ${CTLFILE} &> ${PREFIX}.out
  mpb-split 4 w=${w} h=${h} inside-index=${inside_index} outside-index=${outside_index} filename-prefix=\"${PREFIX}-\" ${CTLFILE} &> ${PREFIX}.out
}

# singleRun 0.240 0.240 1.00 2.40

singleRun 0.480 0.480 1.00 2.40
singleRun 0.200 0.200 1.52 1.00
singleRun 0.200 0.600 1.52 1.00
singleRun 0.300 0.600 1.52 1.00
singleRun 0.400 0.600 1.52 1.00

### times:
# resolution=32
# mesh-size=1
# └─(^_^)(10)(13:05)─> time ./study.sh && checkcmd 
# 
# real    45m22.168s
# user    167m38.541s
# sys     0m24.973s
# SUCCESS
