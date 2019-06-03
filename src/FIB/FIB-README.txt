From:
FIB_manuals/FIB-etching-rate.pdf
FIB_manuals/UGAdv.pdf
======================================

Stream Files:
-------------
A stream file, created as an ASCII text or binary file that addresses
the patterning DAC directly, produces custom pattern files.
Because a 12-bit DAC is used, the patterning field of view is
divided into 4096 steps. The range in X is 0–4095, but in Y is
approximately 280–3816. Y values outside of this range will be off
the image area and may not scan correctly.

...

When you open a stream file, approximately 2000 of the points
display onscreen to give an indication of the pattern to be scanned.
The displayed mill time is calculated from the loop time (pixels x
dwell per pixel) and the total number of loops.

Magnification presets:
======================
cf: FIB_manuals/Mag.pdf

20
50
100
200
500
1000
2000
5000
10000
20000
50000
100000
