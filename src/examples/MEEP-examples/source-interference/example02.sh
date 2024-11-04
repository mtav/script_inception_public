#!/bin/bash
# simple debugging code to exit the script on the first error, as well as outputting each command being run
set -eux

# run the .ctl file and store its text output
meep example02.ctl | tee example02.out

# convert the epsilon data to an image
# h5topng -S3 example02-eps-000000.00.h5

# convert the Ez field data to an image
#h5topng -S3 -Zc dkbluered -a yarg -A example02-eps-000000.00.h5 example02-ez-000200.00.h5

# convert all .h5 files to images
h5topng -t 0:99 -R -Zc dkbluered -a yarg example02-ez.h5

# create an animated .gif
# delay sets the timestep between frames in hundredths of a second, i.e. 10 here means a 0.1s timestep.
convert -delay 10 example02-ez.t*.png example02-ez.gif

#echo SUCCESS

# output SUCCESS if everything worked well
echo SUCCESS
