#!/bin/bash
#set -eux

# clean up eventual output from previous runs
rm -v *.vtk *.h5

# run script
meep source-in-vacuum.ctl

# create VTK files
h5tovtk source-in-vacuum-ez-*.h5

# This should rename files, but may not work depending on your installation.
rename 's/(\d\d\d\d\d\d)\.(\d\d)/$1$2/' source-in-vacuum-ez-*.vtk

echo SUCCESS
