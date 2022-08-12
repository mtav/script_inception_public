#!/usr/bin/env python3

# source: https://nbviewer.jupyter.org/github/mitmath/18369/blob/master/notes/MPB-demo.ipynb

# do inline plots with Python's matplotlib library
#%matplotlib inline
from matplotlib import pyplot as plt
import numpy as np

# load the Meep and MPB modules in Python
import meep as mp
from meep import mpb

# First, we will define some parameters describing our structure.  
# Defining them symbolically here makes it easier to change them.

eps_hi = 12  # the waveguide dielectric constant
eps_lo = 1  # the surrounding low-dielectric material
h = 1       # the thickness of the waveguide (arbitrary units)
Y = 10      # the size of the computational cell in the y direction

# Here we define the size of the computational cell.  Since it is 2d,
# it has no-size in the z direction.  Because it is a waveguide in the
# x direction, then the eigenproblem at a given k has no-size in the
# x direction as well.
geometry_lattice = mp.Lattice(size=(0, Y))

# the default-material is what fills space where we haven't placed objects
default_material = mp.Medium(epsilon=eps_lo)

# a list of geometric objects to create structures in our computation:
# (in this case, we only have one object, a block to make the waveguide)
geometry = [mp.Block(center=(0,0), # center of computational cell
                     size=(mp.inf, h, mp.inf),
                     material=mp.Medium(epsilon=eps_hi))]

# MPB discretizes space with a given resolution.   Here, we set
# a resolution of 32 pixels per unit distance.  Thus, with Y=10
# our comptuational cell will be 320 pixels wide.  In general,
# you should make the resolution fine enough so that the pixels
# are much smaller than the wavelength of the light.
#   -- to get high accuracy results, in practice you 
#      double the resolution until your answer stops changing
#      to your desired tolerance
resolution = 32

# Generally, we want omega(k) for a range of k values.  MPB
# can automatically interpolate a set of k values between any
# given bounds.  Here, we will interpolate 10 k's between 0 and 2.
#
# in MPB, the k vectors are in the basis of the primitive 
# reciprocal lattice vectors.   Here, for a 1d cell with zero
# width in the x direction, the units of kx are just units of 2pi/a
# where a is our distance units.

kmin = 0
kmax = 2
k_interp = 10
k_points = mp.interpolate(k_interp, [mp.Vector3(kmin), mp.Vector3(kmax)])

print(k_points)

num_bands = 10

ms = mpb.ModeSolver(num_bands=num_bands,
                    k_points=k_points,
                    geometry=geometry,
                    geometry_lattice=geometry_lattice,
                    resolution=resolution,
                    default_material=default_material)

ms.run_tm_yeven()

tmyeven_freqs = ms.all_freqs
print(tmyeven_freqs)

print(tmyeven_freqs[:,0]) # omega(k) for band 1 (= column 0 in Python)

ms.run_tm_yodd()
tmyodd_freqs = ms.all_freqs

kx = [k.x for k in ms.k_points]
kx

plt.figure(figsize=(10,7))
plt.plot(kx, tmyeven_freqs, "ro-")
plt.plot(kx, tmyodd_freqs, "bs-")
plt.plot(kx, kx, "k-", linewidth=2)
plt.plot(kx, kx / np.sqrt(eps_hi), "k--", linewidth=2)
plt.fill([0,2,0],[0,2,2], facecolor=(0.9,0.9,0.9), zorder=3)
plt.xlabel("$k_x a / 2\pi$")
plt.ylabel("$\omega a / 2\pi c = fa/c = a/\lambda$")
plt.ylim(0,2)
plt.show()

eps = ms.get_epsilon()

y = np.linspace(-Y/2,Y/2,eps.size)
plt.figure(figsize=(10,3))
plt.plot(y, eps)
plt.xlabel("$y$")
plt.ylabel("$\epsilon$")
plt.ylim(0,13)
plt.show()

ms.k_points = [mp.Vector3(1)]
ms.run_tm(mpb.fix_efield_phase)

ms.get_efield(1) # gets E field for band 1 at the last k point (kx=1)

ms.get_efield(1).shape  # 4d array (y,x,z,3 components)

plt.figure(figsize=(10,8))
ez1 = ms.get_efield(1)[:,0,0,2] # the z component of band 1
ez2 = ms.get_efield(2)[:,0,0,2] # the z component of band 2
ez3 = ms.get_efield(3)[:,0,0,2] # the z component of band 3
# ez4 = ms.get_efield(4)[:,0,0,2] # the z component of band 3
plt.plot(y, np.real(ez1), "b-")
plt.plot(y, np.real(ez2), "r:")
plt.plot(y, np.real(ez3), "k--")
# plt.plot(y, np.real(ez4), "g-")
plt.legend(["band 1", "band 2", "band 3"])
plt.show()

print(np.dot(ez3, (eps * ez1)) / (np.linalg.norm(ez1) * np.linalg.norm(ez3)))

ms2 = mpb.ModeSolver(
    num_bands=5,
    k_points=mp.interpolate(200, [mp.Vector3(0),mp.Vector3(2)]),
    geometry=[mp.Cylinder(center=(0,0), radius=0.2, material=mp.Medium(epsilon=eps_hi))],
    geometry_lattice=mp.Lattice(size=(1, Y)),
    resolution=16,
    default_material=mp.Medium(epsilon=eps_lo))

ms2.run_tm_yeven()  # Ez polarization, even with respect to y=0
tmyeven_freqs2 = ms2.all_freqs
ms2.run_tm_yodd()   # Ez polarization, odd with respect to y=0
tmyodd_freqs2 = ms2.all_freqs
kx2 = [k.x for k in ms2.k_points]

ms2.get_epsilon().shape  # (x size, y size) = (resolution, Y*resolution)

plt.imshow(ms2.get_epsilon().T, cmap='binary')

plt.show()

md = mpb.MPBData(x=21, resolution=32)
plt.imshow(md.convert(ms2.get_epsilon()).T, cmap='binary')
plt.show()

plt.figure(figsize=(10,8))
plt.plot(kx2, tmyeven_freqs2, "r-")
plt.plot(kx2, tmyodd_freqs2, "b--")
plt.plot(kx2, kx2, "k-", linewidth=2)
plt.fill_between([0,0.5,1,1.5,2.0],[0,0.5,0,0.5,0],[1,1,1,1,1], zorder=3)
plt.ylim(0,0.6)
plt.xlabel("$k_x$ in units of $2\pi/a$")
plt.show()

ms2.k_points = [mp.Vector3(0.4)]
ms2.run_tm_yeven(mpb.fix_efield_phase)

ez1 = ms2.get_efield(1)[:,:,0,2] # Ez(x,y) of 1st band
plt.imshow(np.imag(ez1).T, cmap="viridis")
plt.show()

ez = np.imag(md.convert(ms2.get_efield(1)[:,:,0,2]))
maxabs = np.max(abs(ez))
plt.figure(figsize=(14,7))
plt.imshow(ez.T, cmap='RdBu', vmin=-maxabs, vmax=+maxabs)
plt.colorbar()
plt.title("$E_z$ of band 1 at $k_x = 0.4 \\times 2\pi/a$")
plt.show()

ez = np.real(md.convert(ms2.get_efield(2)[:,:,0,2]))
maxabs = np.max(abs(ez))
plt.figure(figsize=(14,7))
plt.imshow(ez.T, cmap='RdBu', vmin=-maxabs, vmax=+maxabs)
plt.colorbar()
plt.title("non-guided mode (above light line) at $k_x = 0.4 \\times 2\pi/a$")
plt.show()

ms2.k_points = [mp.Vector3(0.5)]
ms2.run_tm_yeven(mpb.fix_efield_phase)

ez = np.imag(md.convert(ms2.get_efield(1)[:,:,0,2]))

plt.figure(figsize=(14,14))

plt.subplot(2,1,1)
eps = md.convert(ms2.get_epsilon())
maxabs = np.max(abs(ez))
plt.imshow(ez.T, cmap='RdBu', vmin=-maxabs, vmax=+maxabs)
plt.contour(eps.T)
plt.colorbar()
plt.title("$E_z$ of first band at $k_x = \pi / a = 0.5 2\pi/a$")

plt.subplot(2,1,2)
ez = np.real(md.convert(ms2.get_efield(2)[:,:,0,2]))
maxabs = np.max(abs(ez))
plt.imshow(ez.T, cmap='RdBu', vmin=-maxabs, vmax=+maxabs)
plt.contour(eps.T)
plt.colorbar()
plt.title("$E_z$ of second band at $k_x = \pi / a = 0.5 2\pi/a$")

plt.show()

print('SUCCESS')
