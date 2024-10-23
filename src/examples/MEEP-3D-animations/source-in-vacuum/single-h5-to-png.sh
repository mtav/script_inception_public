#!/bin/bash
# Helper script to process 3D data from a single XYZT .h5 file.
# Adapt the filenames and time slice range as needed.
# You can check the number of time slices in your .h5 file using h5ls.
#
# See here for more details:
# https://manpages.org/h5topng
# https://github.com/NanoComp/h5utils/blob/master/doc/h5tovtk-man.md

set -eux
for i in {0..49}
do
  # convert data to VTK files for viewing with Paraview or MayaVI
  h5tovtk -t${i} -o "source-in-vacuum-fields-${i}.vtk" source-in-vacuum-fields.h5
  # convert data to images for potential future conversion to an animated .gif
  h5topng -t${i} -0 -z0 -o "source-in-vacuum-fields-${i}.png" -S3 -Z -c dkbluered source-in-vacuum-fields.h5
done

# create .gif
convert "source-in-vacuum-fields-*.png" "source-in-vacuum-fields.gif"
