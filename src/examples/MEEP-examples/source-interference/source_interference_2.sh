#!/bin/bash
# simple debugging code to exit the script on the first error, as well as outputting each command being run
set -eux

# cleanup
rm -fv source_interference_2-out/*.png source_interference_2-out/*.h5
# source_interference_2-out/*.gif

# run the .ctl file and store its text output
meep scale=${1} source_interference_2.ctl | tee source_interference_2.out

# convert the epsilon data to an image
# h5topng -S3 source_interference_2-eps-000000.00.h5

# convert the Ez field data to an image
#h5topng -S3 -Zc dkbluered -a yarg -A source_interference_2-eps-000000.00.h5 source_interference_2-ez-000200.00.h5

cd source_interference_2-out
# convert -delay 10 *.png source_interference_2.gif

# convert all .h5 files to images
h5topng -t 0:99 -R -Zc dkbluered -a yarg ez.h5

# create an animated .gif
# delay sets the timestep between frames in hundredths of a second, i.e. 10 here means a 0.1s timestep.
convert -delay 10 ez.t*.png source_interference_2-ez.gif

#echo SUCCESS

# output SUCCESS if everything worked well
echo SUCCESS
