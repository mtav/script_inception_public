#!/bin/bash
# bfdtd_tool.py \1/sim.in -d $DSTDIR/\1 -b "sim" --modevolume --wavelength_mum 123

set -eu

# nlog_1.52.nout_1.00.a_0.54.w_0.20/Ez/sim.in
# nlog_2.10.nout_1.00.a_0.46.w_0.20/Ez/sim.in
# nlog_2.40.nout_1.00.a_0.43.w_0.20/Ez/sim.in
# nlog_3.30.nout_1.00.a_0.34.w_0.20/Ez/sim.in
# nlog_3.50.nout_1.00.a_0.33.w_0.20/Ez/sim.in
# 
# nlog_3.30.nout_1.52.a_0.28.w_0.20/Ez/sim.in
# 
# nlog_1.52.nout_1.00.a_0.54.w_0.31/Ez/sim.in
# nlog_2.10.nout_1.00.a_0.46.w_0.27/Ez/sim.in
# nlog_2.40.nout_1.00.a_0.43.w_0.26/Ez/sim.in
# nlog_3.30.nout_1.00.a_0.34.w_0.21/Ez/sim.in
# nlog_3.50.nout_1.00.a_0.33.w_0.21/Ez/sim.in
# 
# nlog_3.30.nout_1.52.a_0.28.w_0.27/Ez/sim.in

# SUBMISSION ON BC1 ON 2012-08-28
# superqsub.sh ./nlog_3.50.nout_1.00.a_0.33.w_0.21/Ez/sim.sh ./nlog_3.30.nout_1.52.a_0.28.w_0.27/Ez/sim.sh ./nlog_3.30.nout_1.00.a_0.34.w_0.21/Ez/sim.sh ./nlog_2.40.nout_1.00.a_0.43.w_0.26/Ez/sim.sh ./nlog_2.10.nout_1.00.a_0.46.w_0.27/Ez/sim.sh ./nlog_1.52.nout_1.00.a_0.54.w_0.31/Ez/sim.sh ./nlog_3.50.nout_1.00.a_0.33.w_0.20/Ez/sim.sh ./nlog_3.30.nout_1.00.a_0.34.w_0.20/Ez/sim.sh ./nlog_2.40.nout_1.00.a_0.43.w_0.20/Ez/sim.sh ./nlog_2.10.nout_1.00.a_0.46.w_0.20/Ez/sim.sh ./nlog_1.52.nout_1.00.a_0.54.w_0.20/Ez/sim.sh


#SRCDIR="/space/ANONYMIZED/home_rama/DATA/woodpile_2012-08-28"
#DSTDIR="/space/ANONYMIZED/home_rama/TEST/2012-08-28-woodpile-modevolume"
SRCDIR=$1
DSTDIR=$2

# quick test
bfdtd_tool.py $SRCDIR/nlog_3.30.nout_1.52.a_0.28.w_0.27/Ez/sim.in -d $DSTDIR/quicktest/nlog_3.30.nout_1.52.a_0.28.w_0.27/Ez/ -b "sim" --modevolume --wavelength_mum 0.6643 --first 3200 --repetition 3200 --iterations 10000

# w_factor = 0.2
bfdtd_tool.py $SRCDIR/nlog_1.52.nout_1.00.a_0.54.w_0.20/Ez/sim.in -d $DSTDIR/nlog_1.52.nout_1.00.a_0.54.w_0.20/Ez/ -b "sim" --modevolume --wavelength_mum 0.6785
bfdtd_tool.py $SRCDIR/nlog_2.10.nout_1.00.a_0.46.w_0.20/Ez/sim.in -d $DSTDIR/nlog_2.10.nout_1.00.a_0.46.w_0.20/Ez/ -b "sim" --modevolume --wavelength_mum 0.6666
bfdtd_tool.py $SRCDIR/nlog_2.40.nout_1.00.a_0.43.w_0.20/Ez/sim.in -d $DSTDIR/nlog_2.40.nout_1.00.a_0.43.w_0.20/Ez/ -b "sim" --modevolume --wavelength_mum 0.6252
bfdtd_tool.py $SRCDIR/nlog_3.30.nout_1.00.a_0.34.w_0.20/Ez/sim.in -d $DSTDIR/nlog_3.30.nout_1.00.a_0.34.w_0.20/Ez/ -b "sim" --modevolume --wavelength_mum 0.637 0.660
bfdtd_tool.py $SRCDIR/nlog_3.50.nout_1.00.a_0.33.w_0.20/Ez/sim.in -d $DSTDIR/nlog_3.50.nout_1.00.a_0.33.w_0.20/Ez/ -b "sim" --modevolume --wavelength_mum 0.640 0.6583

# optimized w_factor
bfdtd_tool.py $SRCDIR/nlog_1.52.nout_1.00.a_0.54.w_0.31/Ez/sim.in -d $DSTDIR/nlog_1.52.nout_1.00.a_0.54.w_0.31/Ez/ -b "sim" --modevolume --wavelength_mum 0.670
bfdtd_tool.py $SRCDIR/nlog_2.10.nout_1.00.a_0.46.w_0.27/Ez/sim.in -d $DSTDIR/nlog_2.10.nout_1.00.a_0.46.w_0.27/Ez/ -b "sim" --modevolume --wavelength_mum 0.7137
bfdtd_tool.py $SRCDIR/nlog_2.40.nout_1.00.a_0.43.w_0.26/Ez/sim.in -d $DSTDIR/nlog_2.40.nout_1.00.a_0.43.w_0.26/Ez/ -b "sim" --modevolume --wavelength_mum 0.7215
bfdtd_tool.py $SRCDIR/nlog_3.30.nout_1.00.a_0.34.w_0.21/Ez/sim.in -d $DSTDIR/nlog_3.30.nout_1.00.a_0.34.w_0.21/Ez/ -b "sim" --modevolume --wavelength_mum 0.6376
bfdtd_tool.py $SRCDIR/nlog_3.50.nout_1.00.a_0.33.w_0.21/Ez/sim.in -d $DSTDIR/nlog_3.50.nout_1.00.a_0.33.w_0.21/Ez/ -b "sim" --modevolume --wavelength_mum 0.6436
bfdtd_tool.py $SRCDIR/nlog_3.30.nout_1.52.a_0.28.w_0.27/Ez/sim.in -d $DSTDIR/nlog_3.30.nout_1.52.a_0.28.w_0.27/Ez/ -b "sim" --modevolume --wavelength_mum 0.6643
