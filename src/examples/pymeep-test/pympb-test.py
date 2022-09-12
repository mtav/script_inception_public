#!/usr/bin/env python3
import math
import meep as mp
from meep import mpb

num_bands = 8

k_points = [mp.Vector3(),          # Gamma
            mp.Vector3(0.5),       # X
            mp.Vector3(0.5, 0.5),  # M
            mp.Vector3()]          # Gamma

k_points = mp.interpolate(4, k_points)

geometry = [mp.Cylinder(0.2, material=mp.Medium(epsilon=12))]

geometry_lattice = mp.Lattice(size=mp.Vector3(1, 1))

resolution = 32

ms = mpb.ModeSolver(num_bands=num_bands,
                    k_points=k_points,
                    geometry=geometry,
                    geometry_lattice=geometry_lattice,
                    resolution=resolution)

#import sys
#sys.exit(0)

#print_heading("Square lattice of rods: TE bands")
ms.run_te()

# quick plotting
import matplotlib.pyplot as plt
plt.plot(ms.all_freqs)
plt.xlabel('k index')
plt.ylabel('$a/\lambda$')
plt.show()

# output testing
ms.run_tm(mpb.output_efield_z)
ms.run_te(mpb.output_at_kpoint(mp.Vector3(0.5), mpb.output_hfield_z, mpb.output_dpwr))
