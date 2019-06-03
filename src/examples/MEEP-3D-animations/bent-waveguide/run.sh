#!/bin/bash
rm -v *.h5 *.png *.vtk ./y-slices/*.png ./z-slices/*.png

meep bent-waveguide.ctl

h5topng -o x-eps.png -0x0 bent-waveguide-eps-000000.00.h5
h5topng -o y-eps.png -0x0 bent-waveguide-eps-000000.00.h5
h5topng -o z-eps.png -0x0 bent-waveguide-eps-000000.00.h5

h5topng -o x-denergy.png -0x0 -c dkbluered bent-waveguide-denergy-000100.00.h5
h5topng -o y-denergy.png -0y0 -c dkbluered bent-waveguide-denergy-000100.00.h5
h5topng -o z-denergy.png -0z0 -c dkbluered bent-waveguide-denergy-000100.00.h5

h5topng -0y0 -R -Zc dkbluered bent-waveguide-ez-*.h5
h5topng -0y0 -R -c dkbluered bent-waveguide-denergy-*.h5
mkdir -p y-slices
mv bent-waveguide-ez-*.png bent-waveguide-denergy-*.png ./y-slices

h5topng -0z0 -R -Zc dkbluered bent-waveguide-ez-*.h5
h5topng -0z0 -R -c dkbluered bent-waveguide-denergy-*.h5
mkdir -p z-slices
mv bent-waveguide-ez-*.png bent-waveguide-denergy-*.png ./z-slices

h5tovtk bent-waveguide-eps-000000.00.h5 bent-waveguide-ez-*.h5 bent-waveguide-denergy-*.h5
rename 's/(\d\d\d\d\d\d)\.(\d\d)/$1$2/' bent-waveguide-ez-*.vtk
rename 's/(\d\d\d\d\d\d)\.(\d\d)/$1$2/' bent-waveguide-denergy-*.vtk

# after saving animation to .png in paraview:
# convert bent-animation.*.png bent-animation.gif
# https://www.scivision.co/convert-png-to-avi-ffmpeg/
# fails:
# ffmpeg -framerate 5 -pattern_type glob -i 'bent-animation.*.png' -c:v ffv1 out.avi
# works:
# ffmpeg -f image2 -i bent-animation.%4d.png video.mpg

# #!/bin/bash
# # h5topng -0z0 -t 0:332 -R -Zc dkbluered bent-waveguide-ez-all.h5
# 
# rm -v *.h5 *.png *.vtk ./y-slices/*.png ./z-slices/*.png
# 
# meep bent-waveguide.ctl
# 
# h5topng -o x-eps.png -0x0 bent-waveguide-eps-000000.00.h5
# h5topng -o y-eps.png -0y0 bent-waveguide-eps-000000.00.h5
# h5topng -o z-eps.png -0z0 bent-waveguide-eps-000000.00.h5
# 
# h5topng -o x-ez.png -0x0 -c dkbluered bent-waveguide-ez-000100.00.h5
# h5topng -o y-ez.png -0y0 -c dkbluered bent-waveguide-ez-000100.00.h5
# h5topng -o z-ez.png -0z0 -c dkbluered bent-waveguide-ez-000100.00.h5
# 
# h5topng -o x-denergy.png -0x0 -c dkbluered bent-waveguide-denergy-000100.00.h5
# h5topng -o y-denergy.png -0y0 -c dkbluered bent-waveguide-denergy-000100.00.h5
# h5topng -o z-denergy.png -0z0 -c dkbluered bent-waveguide-denergy-000100.00.h5
# 
