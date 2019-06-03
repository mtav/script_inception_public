#!/bin/bash

set -eux

meep no-bend?=true bend-flux.ctl | tee bend0.out
meep bend-flux.ctl | tee bend.out
meep sx=32 sy=64 no-bend?=true bend-flux.ctl | tee bend0-big.out
meep sx=32 sy=64 bend-flux.ctl | tee bend-big.out

grep flux2: bend.out > bend.dat
grep flux2: bend0.out > bend0.dat
grep flux2: bend-big.out > bend-big.dat
grep flux2: bend0-big.out > bend0-big.dat

/usr/bin/octave-3.2.3 ./meep_tutorial.m
matlab_batcher.sh meep_tutorial
