#!/bin/bash

# example usage:
# ../transmission.sh . dim=3

set -eux

cd $1
echo "=== $(pwd) ==="

shift

CTL="transmission.ctl"
REF="reference_file"
GEO="geometry_file"

meep $@ is-reference?=true ${CTL}  | tee ${REF}.out
meep $@ is-reference?=false ${CTL} | tee ${GEO}.out
grep flux1: ${GEO}.out > ${GEO}.dat
grep flux1: ${REF}.out > ${REF}.dat

# meep sx=32 sy=64 is-reference?=true $CTL | tee bend0-big.out
# meep sx=32 sy=64 $CTL | tee bend-big.out
# grep flux1: bend-big.out > bend-big.dat
# grep flux1: bend0-big.out > bend0-big.dat

# /usr/bin/octave-3.2.3 ./transmission.m
# matlab_batcher.sh transmission

# unix% h5topng -t 0:329 -R -Zc dkbluered -a yarg -A eps-000000.00.h5 ez.h5
#    -x ix, -y iy, -z iz, -t it
#               This tells h5topng to use a particular slice of a multi-dimensional dataset.  e.g.  -x causes a yz plane (of a 3d dataset) to be used, at an x index of ix (where the indices run from zero to one less than the maximum index in that direction).   Here,
#               x/y/z  correspond to the first/second/third dimensions of the HDF5 dataset. The -t option specifies a slice in the last dimension, whichever that might be.  See also the -0 option to shift the origin of the x/y/z slice coordinates to the dataset cen‐
#               ter.
# 
#               Instead of specifying a single index as an argument to these options, you can also specify a range of indices in a Matlab-like notation: start:step:end or start:end (step defaults to 1).  This loops over that slice index, from start to end  in  steps
#               of step, producing a sequence of output PNG files (with the slice index appended to the filename, before the ".png").
#      -R     When multiple files are specified, set the bottom and top of the color maps according to the minimum and maximum over all the data.  This is useful to process many files using a consistent color scale, since otherwise the scale is set for  each  file
#               individually.
# 
#        -Z     Center the color scale on the value zero in the data.
#      -c colormap
#               Use a color map colormap rather than the default gray color map (a grayscale ramp from white to black).  colormap is normally the name of one of the color maps provided with h5topng (in the /usr/share/h5utils/colormaps directory), or can  instead  be
#               the name of a color-map file.
# 
#               Three useful included color maps are hot (black-red-yellow-white, useful for intensity data), bluered (blue-white-red, useful for signed data), and hsv (a multi-color "rainbow").  If you use the bluered color map for signed data, you may also want to
#               use the -Z option so that the center of the color scale (white) corresponds to zero.
# 
#               A color-map file is a sequence of whitespace-separated R G B A quadruples, where each value is in the range 0.0 to 1.0 and indicates the fraction of red/green/blue/alpha.  (An alpha of 0 is transparent and of 1 is opaque; this is only used for the -a
#               option, below.)  The colors in the color map are linearly interpolated as necessary to provide a continuous color ramp.
#     -A file, -a colormap:opacity
#               Translucently overlay the data from the first dataset in the file HDF5 file, which should have the same dimensions as the input dataset, on all of the output images, using the colormap colormap with opacity (from 0 for completely transparent to 1 for
#               completely  opaque)  opacity  multiplied by the opacity (alpha) values in the colormap.  (If the overlay dataset does not have the same dimensions as the output data, it is peridically "tiled" over the output.)  You can use the syntax file:dataset to
#               specify a particular dataset within the file.
# 
#               Some predefined colormaps that work particularly well for this feature are yellow (transparent white to opaque yellow) gray (transparent white to opaque black), yarg (transparent black to opaque white), green (transparent white to opaque green),  and
#               bluered (opaque blue to transparent white to opaque red).  You can prepend "-" to the colormap name to reverse the colormap order.  (See also -c, above.)  The default for -a is yellow:0.3 (yellow colormap multiplied by 30% opacity).
