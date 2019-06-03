#!/bin/bash

# Extracts flux info from MEEP .out files and stores it in .dat files.
set -eu

for IN in "$@"
do
  grep flux1: "${IN}" > "${IN%.out}.dat"
done
