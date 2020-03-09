#!/bin/bash

n1=${1:-1.5}
n2=${2:-3.5}
d1=${3:-0.5}
d2=${4:-0.5}

# mpb_wrapper.py -m -a te?=true n1=${n1} n2=${n2} d1=${d1} d2=${d2} DBR-TE-TM.ctl
# mpb_wrapper.py -m -a te?=false n1=${n1} n2=${n2} d1=${d1} d2=${d2} DBR-TE-TM.ctl

mpb_wrapper.py -m --suffix="te?=true" te?=true n1=${n1} n2=${n2} d1=${d1} d2=${d2} DBR-TE-TM.ctl
mpb_wrapper.py -m --suffix="te?=false" te?=false n1=${n1} n2=${n2} d1=${d1} d2=${d2} DBR-TE-TM.ctl

# mpb_wrapper.py -m -a te?=true DBR-TE-TM.ctl
# mpb_wrapper.py -m -a te?=false DBR-TE-TM.ctl
