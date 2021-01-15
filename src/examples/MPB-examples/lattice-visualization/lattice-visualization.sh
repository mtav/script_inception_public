#!/bin/bash
# See here for a good paraview manual:
# http://www.dma.uvigo.es/files/cursos/elmer2/Sesion8/ParaViewTutorial42.pdf

set -eu

mpb lattice-visualization.ctl
h5tovtk lattice-cartesian-epsilon.h5 lattice-non-cartesian-epsilon.h5
h5tovts.py lattice-cartesian-epsilon.h5 lattice-non-cartesian-epsilon.h5
echo "SUCCESS"
