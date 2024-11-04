#!/bin/bash
rm -v two-moving-sources-out/*.png
meep two-moving-sources.ctl
cd two-moving-sources-out
convert *.png two-moving-sources-out.gif
