#!/bin/bash
#Examples files for testing geotoctl.py converter script.

# exit on error
set -e

#Example usage:

# generate test.geo and test.geo.ctl
./RCD111_CTL_generator.py

# convert files with converting BFDTD coordinates to MEEP coordinates (default)
geotoctl.py test.geo

# convert files without converting BFDTD coordinates to MEEP coordinates
geotoctl.py RCD111_1x1x1.geo RCD111_3x3x3.geo --no-offset

# use example.ctl to quickly generate an epsilon.h5 and .vtk file for visualization with paraview
meep geoctlfile=\"test.geo.ctl\" example.ctl
h5tovtk ./example-eps-000000.00.h5
paraview ./example-eps-000000.00.vtk

meep geoctlfile=\"RCD111_1x1x1.geo.ctl\" example.ctl
h5tovtk ./example-eps-000000.00.h5
paraview ./example-eps-000000.00.vtk

meep geoctlfile=\"RCD111_3x3x3.geo.ctl\" example.ctl
h5tovtk ./example-eps-000000.00.h5
paraview ./example-eps-000000.00.vtk
