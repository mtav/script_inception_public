#!/bin/bash
rm -v *.vtk *.h5
meep source-in-vacuum.ctl
h5tovtk source-in-vacuum-ez-*.h5
rename 's/(\d\d\d\d\d\d)\.(\d\d)/$1$2/' source-in-vacuum-ez-*.vtk
