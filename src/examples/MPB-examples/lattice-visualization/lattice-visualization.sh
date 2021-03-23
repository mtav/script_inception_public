#!/bin/bash
# See here for a good paraview manual:
# http://www.dma.uvigo.es/files/cursos/elmer2/Sesion8/ParaViewTutorial42.pdf

set -eu

# rm -fv *.h5 *.vtk

mpb lattice-visualization.ctl
h5tovtk lattice-cartesian-epsilon.h5 lattice-non-cartesian-epsilon.h5
h5tovts.py lattice-cartesian-epsilon.h5 lattice-non-cartesian-epsilon.h5

mpb-data -o lattice-non-cartesian-epsilon.r.h5 -m3 -n50 -r ./lattice-non-cartesian-epsilon.h5
h5tovtk lattice-non-cartesian-epsilon.r.h5

#mpb-data -o lattice-non-cartesian-epsilon.e100.h5 -m3 -e 1,0,0 ./lattice-non-cartesian-epsilon.h5
#mpb-data -o lattice-non-cartesian-epsilon.e010.h5 -m3 -e 0,1,0 ./lattice-non-cartesian-epsilon.h5
#mpb-data -o lattice-non-cartesian-epsilon.e001.h5 -m3 -e 0,0,1 ./lattice-non-cartesian-epsilon.h5
#h5tovtk lattice-non-cartesian-epsilon.e*.h5

echo "SUCCESS"
