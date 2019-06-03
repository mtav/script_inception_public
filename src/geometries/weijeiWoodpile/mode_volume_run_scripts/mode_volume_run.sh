#!/bin/bash
# bfdtd_tool.py \1/sim.in -d ~/TEST/2012-08-24-woodpile-modevolume/\1 -b "sim" --modevolume --wavelength_mum 123

# w_factor = 0.2

bfdtd_tool.py 2012-08-22/3.3_1.52/Ez/sim.in -d ~/TEST/2012-08-24-woodpile-modevolume/testfolder/3.3_1.52/Ez -b "sim" --modevolume --wavelength_mum 0.6643 --first 3200 --repetition 3200 --iterations 10000

# bfdtd_tool.py 2012-08-14/1.52/Ex/sim.in -d ~/TEST/2012-08-24-woodpile-modevolume/w_0.2/1.52/Ex -b "sim" --modevolume --wavelength_mum 123
# bfdtd_tool.py 2012-08-14/1.52/Ey/sim.in -d ~/TEST/2012-08-24-woodpile-modevolume/w_0.2/1.52/Ey -b "sim" --modevolume --wavelength_mum 123
bfdtd_tool.py 2012-08-14/1.52/Ez/sim.in -d ~/TEST/2012-08-24-woodpile-modevolume/w_0.2/1.52/Ez -b "sim" --modevolume --wavelength_mum 0.6785

# bfdtd_tool.py 2012-08-14/2.1/Ex/sim.in -d ~/TEST/2012-08-24-woodpile-modevolume/w_0.2/2.1/Ex -b "sim" --modevolume --wavelength_mum 123
# bfdtd_tool.py 2012-08-14/2.1/Ey/sim.in -d ~/TEST/2012-08-24-woodpile-modevolume/w_0.2/2.1/Ey -b "sim" --modevolume --wavelength_mum 123
bfdtd_tool.py 2012-08-14/2.1/Ez/sim.in -d ~/TEST/2012-08-24-woodpile-modevolume/w_0.2/2.1/Ez -b "sim" --modevolume --wavelength_mum 0.6666

# bfdtd_tool.py 2012-08-14/2.4/Ex/sim.in -d ~/TEST/2012-08-24-woodpile-modevolume/w_0.2/2.4/Ex -b "sim" --modevolume --wavelength_mum 123
# bfdtd_tool.py 2012-08-14/2.4/Ey/sim.in -d ~/TEST/2012-08-24-woodpile-modevolume/w_0.2/2.4/Ey -b "sim" --modevolume --wavelength_mum 123
bfdtd_tool.py 2012-08-14/2.4/Ez/sim.in -d ~/TEST/2012-08-24-woodpile-modevolume/w_0.2/2.4/Ez -b "sim" --modevolume --wavelength_mum 0.6252

# bfdtd_tool.py 2012-08-14/3.3/Ex/sim.in -d ~/TEST/2012-08-24-woodpile-modevolume/w_0.2/3.3/Ex -b "sim" --modevolume --wavelength_mum 123
# bfdtd_tool.py 2012-08-14/3.3/Ey/sim.in -d ~/TEST/2012-08-24-woodpile-modevolume/w_0.2/3.3/Ey -b "sim" --modevolume --wavelength_mum 123
bfdtd_tool.py 2012-08-14/3.3/Ez/sim.in -d ~/TEST/2012-08-24-woodpile-modevolume/w_0.2/3.3/Ez -b "sim" --modevolume --wavelength_mum 0.637 0.660

# bfdtd_tool.py 2012-08-14/3.5/Ex/sim.in -d ~/TEST/2012-08-24-woodpile-modevolume/w_0.2/3.5/Ex -b "sim" --modevolume --wavelength_mum 123
# bfdtd_tool.py 2012-08-14/3.5/Ey/sim.in -d ~/TEST/2012-08-24-woodpile-modevolume/w_0.2/3.5/Ey -b "sim" --modevolume --wavelength_mum 123
bfdtd_tool.py 2012-08-14/3.5/Ez/sim.in -d ~/TEST/2012-08-24-woodpile-modevolume/w_0.2/3.5/Ez -b "sim" --modevolume --wavelength_mum 0.640 0.6583

# optimized w_factor

# bfdtd_tool.py 2012-08-22/1.52/Ex/sim.in -d ~/TEST/2012-08-24-woodpile-modevolume/w_optimized/1.52/Ex -b "sim" --modevolume --wavelength_mum 123
# bfdtd_tool.py 2012-08-22/1.52/Ey/sim.in -d ~/TEST/2012-08-24-woodpile-modevolume/w_optimized/1.52/Ey -b "sim" --modevolume --wavelength_mum 123
bfdtd_tool.py 2012-08-22/1.52/Ez/sim.in -d ~/TEST/2012-08-24-woodpile-modevolume/w_optimized/1.52/Ez -b "sim" --modevolume --wavelength_mum 0.670

# bfdtd_tool.py 2012-08-22/2.1/Ex/sim.in -d ~/TEST/2012-08-24-woodpile-modevolume/w_optimized/2.1/Ex -b "sim" --modevolume --wavelength_mum 123
# bfdtd_tool.py 2012-08-22/2.1/Ey/sim.in -d ~/TEST/2012-08-24-woodpile-modevolume/w_optimized/2.1/Ey -b "sim" --modevolume --wavelength_mum 123
bfdtd_tool.py 2012-08-22/2.1/Ez/sim.in -d ~/TEST/2012-08-24-woodpile-modevolume/w_optimized/2.1/Ez -b "sim" --modevolume --wavelength_mum 0.7137

# bfdtd_tool.py 2012-08-22/2.4/Ex/sim.in -d ~/TEST/2012-08-24-woodpile-modevolume/w_optimized/2.4/Ex -b "sim" --modevolume --wavelength_mum 123
# bfdtd_tool.py 2012-08-22/2.4/Ey/sim.in -d ~/TEST/2012-08-24-woodpile-modevolume/w_optimized/2.4/Ey -b "sim" --modevolume --wavelength_mum 123
bfdtd_tool.py 2012-08-22/2.4/Ez/sim.in -d ~/TEST/2012-08-24-woodpile-modevolume/w_optimized/2.4/Ez -b "sim" --modevolume --wavelength_mum 0.7215

# bfdtd_tool.py 2012-08-22/3.3/Ex/sim.in -d ~/TEST/2012-08-24-woodpile-modevolume/w_optimized/3.3/Ex -b "sim" --modevolume --wavelength_mum 123
# bfdtd_tool.py 2012-08-22/3.3/Ey/sim.in -d ~/TEST/2012-08-24-woodpile-modevolume/w_optimized/3.3/Ey -b "sim" --modevolume --wavelength_mum 123
bfdtd_tool.py 2012-08-22/3.3/Ez/sim.in -d ~/TEST/2012-08-24-woodpile-modevolume/w_optimized/3.3/Ez -b "sim" --modevolume --wavelength_mum 0.6376

# bfdtd_tool.py 2012-08-22/3.5/Ex/sim.in -d ~/TEST/2012-08-24-woodpile-modevolume/w_optimized/3.5/Ex -b "sim" --modevolume --wavelength_mum 123
# bfdtd_tool.py 2012-08-22/3.5/Ey/sim.in -d ~/TEST/2012-08-24-woodpile-modevolume/w_optimized/3.5/Ey -b "sim" --modevolume --wavelength_mum 123
bfdtd_tool.py 2012-08-22/3.5/Ez/sim.in -d ~/TEST/2012-08-24-woodpile-modevolume/w_optimized/3.5/Ez -b "sim" --modevolume --wavelength_mum 0.6436

# bfdtd_tool.py 2012-08-22/3.3_1.52/Ex/sim.in -d ~/TEST/2012-08-24-woodpile-modevolume/w_optimized/3.3_1.52/Ex -b "sim" --modevolume --wavelength_mum 123
# bfdtd_tool.py 2012-08-22/3.3_1.52/Ey/sim.in -d ~/TEST/2012-08-24-woodpile-modevolume/w_optimized/3.3_1.52/Ey -b "sim" --modevolume --wavelength_mum 123
bfdtd_tool.py 2012-08-22/3.3_1.52/Ez/sim.in -d ~/TEST/2012-08-24-woodpile-modevolume/w_optimized/3.3_1.52/Ez -b "sim" --modevolume --wavelength_mum 0.6643
