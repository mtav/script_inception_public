#!/bin/bash
rm -v *.h5 *.png *.vtk ./y-slices/*.png ./z-slices/*.png

meep straight-waveguide.ctl

h5topng -o x-eps.png -0x0 straight-waveguide-eps-000000.00.h5
h5topng -o y-eps.png -0x0 straight-waveguide-eps-000000.00.h5
h5topng -o z-eps.png -0x0 straight-waveguide-eps-000000.00.h5

h5topng -o x-denergy.png -0x0 -c dkbluered straight-waveguide-denergy-000100.00.h5
h5topng -o y-denergy.png -0y0 -c dkbluered straight-waveguide-denergy-000100.00.h5
h5topng -o z-denergy.png -0z0 -c dkbluered straight-waveguide-denergy-000100.00.h5

h5topng -0y0 -R -Zc dkbluered straight-waveguide-ez-*.h5
h5topng -0y0 -R -c dkbluered straight-waveguide-denergy-*.h5
mkdir -p y-slices
mv straight-waveguide-ez-*.png ./y-slices

h5topng -0z0 -R -Zc dkbluered straight-waveguide-ez-*.h5
h5topng -0z0 -R -c dkbluered straight-waveguide-denergy-*.h5
mkdir -p z-slices
mv straight-waveguide-ez-*.png ./z-slices


h5tovtk straight-waveguide-eps-000000.00.h5 straight-waveguide-ez-*.h5 straight-waveguide-denergy-*.h5
rename 's/(\d\d\d\d\d\d)\.(\d\d)/$1$2/' straight-waveguide-ez-*.vtk
rename 's/(\d\d\d\d\d\d)\.(\d\d)/$1$2/' straight-waveguide-denergy-*.vtk

# after saving animation to .png in paraview:
# convert straight-animation.*.png straight-animation.avi
# https://www.scivision.co/convert-png-to-avi-ffmpeg/
# fails:
# ffmpeg -framerate 5 -pattern_type glob -i 'straight-animation.*.png' -c:v ffv1 out.avi
# works:
# ffmpeg -f image2 -i straight-animation.%4d.png video.mpg
