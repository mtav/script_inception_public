#!/bin/bash

# TESTING SCRIPT

set -eux

echo "===================="
make -f Makefile.linux

echo "===================="
./ID_test.py

EXE=fdtd64_withRotation

cd EpsilonSnapshots/
$EXE EpsilonSnapshots.in
cd ../FrequencySnapshots/
$EXE FrequencySnapshots.in
cd ../ModeFilteredProbes/
$EXE ModeFilteredProbes.in
cd ../Probes/
$EXE Probes.in
cd ../TimeSnapshots/
$EXE TimeSnapshots.in
cd ..

echo "===================="
grep -ci ^probe */*.inp
grep -ci ^snapshot */*.inp
grep -ci ^frequency_snapshot */*.inp

set +x
echo "===================="

ls -1 Probes/*.prn | wc -l
ls -1 TimeSnapshots/*.prn | wc -l
ls -1 EpsilonSnapshots/*.prn | wc -l
ls -1 FrequencySnapshots/*.prn | wc -l
ls -1 ModeFilteredProbes/*.prn | wc -l

set +x
echo "===================="

./FrequencySnapshot_IDs | xargs -n1 -I{} ls FrequencySnapshots/{} 1>/dev/null
./TimeSnapshot_IDs | xargs -n1 -I{} ls TimeSnapshots/{} 1>/dev/null
./TimeSnapshot_IDs | xargs -n1 -I{} ls EpsilonSnapshots/{} 1>/dev/null
./Probe_IDs | xargs -n1 -I{} ls Probes/{} 1>/dev/null
./ModeFilteredProbe_IDs | xargs -n1 -I{} ls ModeFilteredProbes/{} 1>/dev/null
echo "===================="
