#!/usr/bin/env python3
import math
import meep as mp
from meep import mpb
import numpy as np

num_bands = 2

k_points = [mp.Vector3(-0.5), # Brillouin zone edge
            mp.Vector3(0),    # Gamma
            mp.Vector3(0.5)]  # Brillouin zone edge

k_points = mp.interpolate(10, k_points)

n1 = np.sqrt(1)
n2 = np.sqrt(13)
t1 = 0.5
t2 = 0.5
a = t1+t1

block1 = mp.Block(center=mp.Vector3(-a/2+t1/2),
          size=mp.Vector3(t1, mp.inf, mp.inf),
          material=mp.Medium(index=n1))

block2 = mp.Block(center=mp.Vector3(t1/2),
          size=mp.Vector3(t2, mp.inf, mp.inf),
          material=mp.Medium(index=n2))

geometry = [block1, block2]

geometry_lattice = mp.Lattice(size=mp.Vector3(1)) # 1D lattice

resolution = 32

ms = mpb.ModeSolver(num_bands=num_bands,
                    k_points=k_points,
                    geometry=geometry,
                    geometry_lattice=geometry_lattice,
                    resolution=resolution)


# TE bands
ms.run_te()

# quick plotting
import matplotlib.pyplot as plt
kx = [k[0] for k in ms.k_points]
plt.plot(kx, ms.all_freqs)
plt.xlabel('k index')
plt.ylabel('$a/\lambda$')
plt.xlim([-0.5,0.5])
plt.ylim([0,0.30])
plt.show()
