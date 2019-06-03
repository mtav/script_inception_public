#!/bin/bash
set -eu

meep sphere-cone.ctl;
h5tovtk -o epsilon.vtk ./sphere-cone-eps-000000.00.h5
unset LD_LIBRARY_PATH PYTHONPATH PYTHONSTARTUP
mayavi2 -d epsilon.vtk -m IsoSurface &> /dev/null
