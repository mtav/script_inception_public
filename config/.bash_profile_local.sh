#!/bin/bash
case $(hostname) in
  bigblue*) BC=2;;
  newblue*) BC=3;;
  *) BC=0;;
esac

# show quota
if test ${BC} -eq 2
then
  showquota # BC1+2
elif test ${BC} -eq 3
then
  #panfs_quota # BC3
  pan_quota # BC3
fi

# show job stats
if test ${BC} -gt 0
then
	jobstats.sh
fi
