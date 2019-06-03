#!/bin/bash

for a_over_w in 2.5 3 3.5 4 4.5 5
do
  /usr/bin/meep a_over_w=${a_over_w} LDOS-tutorial.ctl | tee LDOS-tutorial-${a_over_w}.out
done

# post-processing:
# grep ldos *.out > LDOS-tutorial.csv
# LDOS-tutorial-([.0-9]+)\.out:ldos0:, ([.0-9]+)\nLDOS-tutorial-([.0-9]+)\.out:ldos1:, ([.0-9]+), ([.0-9]+)
# \1, \4, \2, \5
