#!/bin/bash
cd $JOBDIR
# pwd >tmp1.txt
# ls >tmp2.txt
# pwd >&2
mpb *.ctl > data.out
