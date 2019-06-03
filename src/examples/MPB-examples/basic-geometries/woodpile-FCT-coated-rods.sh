#!/bin/bash

set -eu

MPB_FLAGS="output_epsilon_only?=true"

# mpb_wrapper.py -s "JOSA-B" ${MPB_FLAGS} coated-rods?=false rod_height=0.25 rod_width=0.2145 rod-index=3.3 elliptical-rod-shape?=false _lattice_mode=1 woodpile-FCT-coated-rods.ctl
# mpb_wrapper.py -s "coated-rods?=true" ${MPB_FLAGS} coated-rods?=true woodpile-FCT-coated-rods.ctl
# mpb_wrapper.py -s "coated-rods?=false" ${MPB_FLAGS} coated-rods?=false woodpile-FCT-coated-rods.ctl

mpb_wrapper.py -a ${MPB_FLAGS} coated-rods?=false woodpile-FCT-coated-rods.ctl

# for Matlab/Octave:
# filebase="woodpile-FCT-coated-rods.JOSA-B";
# plot_MPB([filebase, '.csv']);
# hline(0.4853);
# hline(0.5689);
# saveas(gcf, [filebase, '.png']);
# filebase="woodpile-FCT-coated-rods.coated-rods?=true";
# plot_MPB([filebase, '.csv']); saveas(gcf, [filebase, '.png']);
# filebase="woodpile-FCT-coated-rods.coated-rods?=false";
# plot_MPB([filebase, '.csv']); saveas(gcf, [filebase, '.png']);
