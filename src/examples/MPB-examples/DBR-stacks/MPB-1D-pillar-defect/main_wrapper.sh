#!/bin/bash
set -eu

# generate all VTK files required for the .pvsm state file
bash wrapper.sh 3.00
bash wrapper.sh 3.50
bash wrapper.sh 4.00
