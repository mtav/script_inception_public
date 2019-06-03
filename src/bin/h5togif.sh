#!/bin/bash

set -eu

# Check if all parameters are present
# If no, exit
if [ $# -ne 1 ] && [ $# -ne 2 ]
then
        echo "usage :"
        echo "`basename $0` FIELD_FILE.h5 EPS_FILE.h5"
        exit 0
fi

# EPS_FILE=$(readlink --canonicalize ${1})
# FIELD_FILE=$(readlink --canonicalize ${2})
# FIELD_BASE_PATTERN=${2%.h5}
# GIF_FILE=$(readlink --canonicalize ${3})

FIELD_FILE=${1}
FIELD_BASE_PATTERN=${FIELD_FILE%.h5}
EPS_FILE=${2:-}
GIF_FILE=${FIELD_BASE_PATTERN}.gif

# get number of time slices
N=$(h5ls ${FIELD_FILE} | awk '{print $5}' | awk -F'/' '{print $1}')
N=$((${N} - 1))

# echo "-t 0:${N}"

# TMP=$(mktemp -d )
# echo "TMP=${TMP}"
# cd ${TMP}

# pwd
if test -z "${EPS_FILE}"
then
  echo "no epsilon contour added"
  h5topng -t 0:${N} -R -Zc dkbluered ${FIELD_FILE}
else
  echo "epsilon contour added"
  h5topng -t 0:${N} -R -Zc dkbluered -a yarg -A ${EPS_FILE} ${FIELD_FILE}
fi

# h5topng -t 0:${N} -R -Zc dkbluered -a gray -A ${EPS_FILE} ${FIELD_FILE}
# h5topng -t 0:${N} -R -Zc dkbluered ${FIELD_FILE}
# pwd
# echo "===="
# ls
# echo "===="
# ls "${FIELD_BASE_PATTERN}*.png"
# echo "===="
# ls
# exit

# x="${FIELD_BASE_PATTERN}*.png"
# convert -delay 0.1 "${FIELD_BASE_PATTERN}*.png" ${GIF_FILE}
convert "${FIELD_BASE_PATTERN}*.png" ${GIF_FILE}

# pwd
# ls -- "${FIELD_BASE_PATTERN}"*.png
rm -- "${FIELD_BASE_PATTERN}"*.png

# cd -
# echo "TMP=${TMP}"

# -Z     Center the color scale on the value zero in the data.
# -R     When multiple files are specified, set the bottom and top of the color maps according to the minimum and maximum over all the data.  This is useful to process many files using a consistent color scale, since otherwise the scale is set for  each  file
#               individually.
# -c colormap
#               Use a color map colormap rather than the default gray color map (a grayscale ramp from white to black).  colormap is normally the name of one of the color maps provided with h5topng (in the /usr/share/h5utils/colormaps directory), or can  instead  be
#               the name of a color-map file.
# 
#               Three useful included color maps are hot (black-red-yellow-white, useful for intensity data), bluered (blue-white-red, useful for signed data), and hsv (a multi-color "rainbow").  If you use the bluered color map for signed data, you may also want to
#               use the -Z option so that the center of the color scale (white) corresponds to zero.
# 
#               A color-map file is a sequence of whitespace-separated R G B A quadruples, where each value is in the range 0.0 to 1.0 and indicates the fraction of red/green/blue/alpha.  (An alpha of 0 is transparent and of 1 is opaque; this is only used for the -a
#               option, below.)  The colors in the color map are linearly interpolated as necessary to provide a continuous color ramp.
# -C file, -b val
#               Superimpose  contour outlines from the first dataset in the file HDF5 file on all of the output images.  (If the contour dataset does not have the same dimensions as the output data, it is peridically "tiled" over the output.)  You can use the syntax
#               file:dataset to specify a particular dataset within the file.  The contour outlines are around a value of val (defaults to middle of value range in file).
# 
