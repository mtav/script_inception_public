#!/usr/bin/env python3

# source: https://nbviewer.jupyter.org/github/mitmath/18369/blob/master/notes/MPB-demo.ipynb

# if not showing plots, avoid using X server, as it can be problematic
# cf: https://stackoverflow.com/questions/4931376/generating-matplotlib-graphs-without-a-running-x-server
if True:
  import matplotlib as mpl
  mpl.use('Agg')

# do inline plots with Python's matplotlib library
#%matplotlib inline
import sys
from matplotlib import pyplot as plt
import numpy as np

# load the Meep and MPB modules in Python
import meep as mp
from meep import mpb

def extract_band(bands, eps_tuning=40):
  single_band = []
  n=0
  eps = eps_tuning*abs(np.diff(bands[51,0:2]))
  eps_min = mp.inf

  n_values = []
  D_values = []

  for idx, band in enumerate(bands):
    if n+1 <= len(band)-1:
      D=abs(band[n+1]-band[n])
      if D < eps_min:
        eps_min=D
      if D < eps:
        n+=1
        eps_min = mp.inf
    D_values.append(D)
    n_values.append(n)
    single_band.append(band[n])

  D_values=np.array(D_values)
  n_values=np.array(n_values)

  #print(n_values)
  #print(len(n_values))
  #print(D_values)
  #print(len(D_values))
  #print(kx2)
  #print(len(kx2))

  #plt.plot(kx2, single_band, "r.-")

  #plt.figure(figsize=(10,8))
  #plt.plot(kx2, D_values, "b.-")
  #plt.plot(kx2, min(D_values) + (n_values/max(n_values))*(max(D_values)-min(D_values)), "r-")
  ##plt.plot(kx2, D_values, "b.-")
  #plt.axhline(y=eps)
  ##plt.show()

  #print('eps', eps)
  #print('eps_min', eps_min)

  #plt.show()
  return single_band

def showGeom(ms2, outfile=None):
  ms2.get_epsilon().shape  # (x size, y size) = (resolution, Y*resolution)
  plt.figure(figsize=(10,8))
  plt.imshow(ms2.get_epsilon().T, cmap='binary')
  if outfile:
    outfile_final=outfile+'.unitcell.png'
    print(f'Saving as {outfile_final}')
    plt.savefig(outfile_final)
  else:
    plt.show()

  md = mpb.MPBData(x=21, resolution=32)
  plt.figure(figsize=(10,8))
  plt.imshow(md.convert(ms2.get_epsilon()).T, cmap='binary')
  if outfile:
    outfile_final=outfile+'.png'
    print(f'Saving as {outfile_final}')
    plt.savefig(outfile_final)
  else:
    plt.show()
  return

def computeBands(wx_n, wy_n, eps_hi = 12, modes='TM'):
  #### figure 3a, p125 in SJ-book
  # w=0.4a
  # h=0.4a
  # epsilon = 12
  # TM even and odd
  #eps_hi = 12
  eps_lo = 1  # the surrounding low-dielectric material
  #wx_n = 0.4
  #wx_n = mp.inf
  #wy_n = 0.4
  Y = 10      # the size of the computational cell in the y direction

  block = mp.Block(center=mp.Vector3(0, 0, 0), material=mp.Medium(epsilon=eps_hi), size=mp.Vector3(wx_n, wy_n, mp.inf))

  #cylinder = mp.Cylinder(center=(0,0), radius=0.2, material=mp.Medium(epsilon=eps_hi))
  k_points = mp.interpolate(50, [mp.Vector3(0),mp.Vector3(0.5),mp.Vector3(1)])
  #k_points = []

  ms2 = mpb.ModeSolver(
      num_bands=6,
      k_points=k_points,
      geometry=[block],
      geometry_lattice=mp.Lattice(size=(1, Y)),
      resolution=16,
      default_material=mp.Medium(epsilon=eps_lo))

  if modes=='TM':
    ms2.run_tm_yeven()  # Ez polarization, even with respect to y=0
    tmyeven_freqs2 = ms2.all_freqs
    ms2.run_tm_yodd()   # Ez polarization, odd with respect to y=0
    tmyodd_freqs2 = ms2.all_freqs
  else:
    ms2.run_te_yeven()  # Ez polarization, even with respect to y=0
    tmyeven_freqs2 = ms2.all_freqs
    ms2.run_te_yodd()   # Ez polarization, odd with respect to y=0
    tmyodd_freqs2 = ms2.all_freqs
    
  kx2 = [k.x for k in ms2.k_points]
  return (ms2, kx2, tmyeven_freqs2, tmyodd_freqs2)
  
def plotBandsSingle(kx2, tmyeven_freqs2, tmyodd_freqs2, outfile=None):
  tmyeven_freqs2_band1 = extract_band(tmyeven_freqs2)
  tmyodd_freqs2_band1 = extract_band(tmyodd_freqs2, eps_tuning=10)
  plt.figure(figsize=(10,8))
  L,=plt.plot(kx2, tmyodd_freqs2_band1, "r-")
  L.set_label('TM odd band #1')
  L,=plt.plot(kx2, tmyeven_freqs2_band1, "b-")
  L.set_label('TM even band #1')
  plt.fill_between([0,0.5],[0,0.5],[1,1], zorder=3)
  plt.xlim(0,1)
  plt.ylim(0,0.5)
  plt.xlabel("Wavevector $k a / 2 \pi$")
  plt.ylabel("Frequency $\omega a / (2 \pi c)$")
  plt.legend()
  #plt.savefig('continuous_waveguide_single_bands.png')
  #plt.savefig('continuous_waveguide_bands_even.png')
  #plt.savefig('continuous_waveguide_bands_odd.png')

  if outfile:
    outfile_final=outfile+'.bands.png'
    print(f'Saving as {outfile_final}')
    plt.savefig(outfile_final)
  else:
    plt.show()
  return

def plotBandsAll(kx2, tmyeven_freqs2, tmyodd_freqs2, symmetric_fill=False, highlight_bandgap=False, outfile=None, x_limits=[0,1], show=True, lightcone=True, modes='TM'):
  plt.figure(figsize=(10,8))
  lines_odd = plt.plot(kx2, tmyodd_freqs2, "r-")
  lines_even = plt.plot(kx2, tmyeven_freqs2, "b-")
  if lightcone:
    if symmetric_fill:
      plt.fill_between([0,0.5,1],[0,0.5,0],[1,1,1], zorder=3)
    else:
      plt.fill_between([0,0.5],[0,0.5],[1,1], zorder=3)
  if highlight_bandgap:
    mini = tmyeven_freqs2[51,0]
    maxi = tmyeven_freqs2[51,1]
    plt.fill_between([0,1], [mini,mini], [maxi,maxi], zorder=2, color=(1,1,0))
  plt.xlim(*x_limits)
  plt.ylim(0,0.5)
  plt.xlabel("Wavevector $k a / 2 \pi$")
  plt.ylabel("Frequency $\omega a / (2 \pi c)$")

  plt.legend([lines_odd[0], lines_even[0]], ['{} odd bands'.format(modes), '{} even bands'.format(modes)])

  if outfile:
    outfile_final=outfile+'.bands.png'
    print(f'Saving as {outfile_final}')
    plt.savefig(outfile_final)
  else:
    if show:
      plt.show()
  return

def SJ_fig3a():
  ### SJ-book, p125, fig 3a
  wx_n = mp.inf
  wy_n = 0.4
  outfile_base = 'continuous'
  (ms2, kx2, tmyeven_freqs2, tmyodd_freqs2) = computeBands(wx_n, wy_n)
  showGeom(ms2, outfile=outfile_base)
  #plotBandsAll(kx2, tmyeven_freqs2, tmyodd_freqs2, symmetric_fill=False)
  plotBandsSingle(kx2, tmyeven_freqs2, tmyodd_freqs2, outfile=outfile_base)

def SJ_fig3b():
  ### SJ-book, p125, fig 3b
  wx_n = 0.4
  wy_n = 0.4
  outfile_base = 'SWG'
  (ms2, kx2, tmyeven_freqs2, tmyodd_freqs2) = computeBands(wx_n, wy_n)
  showGeom(ms2, outfile=outfile_base)
  plotBandsAll(kx2, tmyeven_freqs2, tmyodd_freqs2, symmetric_fill=True, highlight_bandgap=True, outfile=outfile_base)
  #plotBandsSingle(kx2, tmyeven_freqs2, tmyodd_freqs2)

def SWG_fig4():
  ### SWG-paper, fig4
  # operating wavelength
  Lambda = 1.651 #um
  # silicon refractive index at lambda=1.651um
  #n_hi = 3.4674
  n_hi = 1.44
  eps_hi = n_hi**2  # the waveguide dielectric constant
  # waveguide width in um
  w = 0.800
  # unit cell size
  a = 0.430

  wx_n = 0.5
  wy_n = w/a
  #outfile_base = 'fig4'
  outfile_base = None
  (ms2, kx2, tmyeven_freqs2, tmyodd_freqs2) = computeBands(wx_n, wy_n, modes='TE')
  #showGeom(ms2, outfile=outfile_base)
  plotBandsAll(kx2, tmyeven_freqs2, tmyodd_freqs2, symmetric_fill=True, highlight_bandgap=False, outfile=outfile_base, x_limits=[0,0.5], show=False, lightcone=False, modes='TE')
  #plotBandsSingle(kx2, tmyeven_freqs2, tmyodd_freqs2)
  #plt.xlim(0.32,0.5)
  #plt.ylim(0.2,0.37)

  x=(0.4+0.45)/2
  y=a/Lambda
  plt.plot(x,y, marker='*', color=(0.5,0,0))

  plt.axhline(y=0.35, color='k', linestyle='--')
  plt.axhline(y=0.3, color='k', linestyle='--')
  plt.axhline(y=0.25, color='k', linestyle='--')
  plt.axhline(y=0.2, color='k', linestyle='--')
  n=1.44
  plt.fill_between([0,0.5,1],[0/n,0.5/n,0/n],[1,1,1], zorder=4, color=(0,0,1))
  n=1
  plt.fill_between([0,0.5,1],[0/n,0.5/n,0/n],[1,1,1], zorder=5, color=(0,0,0.5))
  # plt.show()
  plt.savefig('SWG_fig4_bands.png')

#SJ_fig3a()
#SJ_fig3b()
SWG_fig4()
sys.exit()

#### figure 3a, p125 in SJ-book
# w=0.4a
# h=0.4a
# epsilon = 12
# TM even and odd
eps_hi = 12
eps_lo = 1  # the surrounding low-dielectric material
wx_n = 0.4
wy_n = 0.4
Y = 10      # the size of the computational cell in the y direction

block = mp.Block(center=mp.Vector3(0, 0, 0), material=mp.Medium(epsilon=eps_hi), size=mp.Vector3(wx_n, wy_n, mp.inf))

#cylinder = mp.Cylinder(center=(0,0), radius=0.2, material=mp.Medium(epsilon=eps_hi))
k_points = mp.interpolate(50, [mp.Vector3(0),mp.Vector3(0.5),mp.Vector3(1)])
#k_points = []

ms2 = mpb.ModeSolver(
    num_bands=6,
    k_points=k_points,
    geometry=[block],
    geometry_lattice=mp.Lattice(size=(1, Y)),
    resolution=16,
    default_material=mp.Medium(epsilon=eps_lo))

ms2.run_tm_yeven()  # Ez polarization, even with respect to y=0
tmyeven_freqs2 = ms2.all_freqs
ms2.run_tm_yodd()   # Ez polarization, odd with respect to y=0
tmyodd_freqs2 = ms2.all_freqs
kx2 = [k.x for k in ms2.k_points]

#ms2.get_epsilon().shape  # (x size, y size) = (resolution, Y*resolution)
#plt.imshow(ms2.get_epsilon().T, cmap='binary')
#plt.show()

#md = mpb.MPBData(x=21, resolution=32)
#plt.imshow(md.convert(ms2.get_epsilon()).T, cmap='binary')
#plt.show()

plt.figure(figsize=(10,8))
plt.plot(kx2, tmyodd_freqs2, "r.-")
plt.plot(kx2, tmyeven_freqs2, "b.-")
plt.ylim(0,0.5)
plt.xlabel("$k_x$ in units of $2\pi/a$")
plt.show()

sys.exit()

tmyeven_freqs2_band1 = extract_band(tmyeven_freqs2)
tmyodd_freqs2_band1 = extract_band(tmyodd_freqs2, eps_tuning=10)

plt.figure(figsize=(10,8))
L,=plt.plot(kx2, tmyodd_freqs2_band1, "r-")
L.set_label('TM odd band #1')
L,=plt.plot(kx2, tmyeven_freqs2_band1, "b-")
L.set_label('TM even band #1')
plt.fill_between([0,0.5],[0,0.5],[1,1], zorder=3)
plt.xlim(0,1)
plt.ylim(0,0.5)
plt.xlabel("Wavevector $k a / 2 \pi$")
plt.ylabel("Frequency $\omega a / (2 \pi c)$")
plt.legend()
#plt.savefig('continuous_waveguide_single_bands.png')
#plt.savefig('continuous_waveguide_bands_even.png')
#plt.savefig('continuous_waveguide_bands_odd.png')

plt.show()
sys.exit()

plt.figure(figsize=(10,8))
#plt.plot(kx2, tmyodd_freqs2, "b.-")
#plt.plot(kx2, tmyodd_freqs2_band1, "r.-")
plt.plot(kx2, tmyeven_freqs2, "b.-")
#L.set_label('even band #1')
plt.plot(kx2, tmyeven_freqs2_band1, "r.-")
#L.set_label('even band #1')
plt.ylim(0,0.5)
plt.xlabel("$k_x$ in units of $2\pi/a$")
plt.legend()
#plt.savefig('continuous_waveguide_bands_even.png')
#plt.savefig('continuous_waveguide_bands_odd.png')

plt.show()

plt.figure(figsize=(10,8))
plt.plot(kx2, tmyodd_freqs2, "b.-")
plt.plot(kx2, tmyodd_freqs2_band1, "r.-")
#plt.plot(kx2, tmyeven_freqs2_band1, "b-")
plt.ylim(0,0.5)
plt.xlabel("$k_x$ in units of $2\pi/a$")
#plt.savefig('continuous_waveguide_bands_even.png')
#plt.savefig('continuous_waveguide_bands_odd.png')

plt.show()

raise
    #print(idx, bands)
#print(len(kx2))
#print(len(y))
#raise

plt.figure(figsize=(10,8))
plt.plot(kx2, tmyeven_freqs2, "b-")
plt.plot(kx2, tmyodd_freqs2, "r--")
plt.plot(kx2, kx2, "k-", linewidth=2) # light cone in air
#plt.fill_between([0,0.5,1,1.5,2.0],[0,0.5,0,0.5,0],[1,1,1,1,1], zorder=3)
plt.fill_between([0,0.5],[0,0.5],[1,1], zorder=3)
plt.ylim(0,0.5)
plt.xlabel("$k_x$ in units of $2\pi/a$")
#plt.show()
plt.savefig('continuous_waveguide_bands.png')

raise

n_hi = 3.4674
eps_hi = n_hi**2  # the waveguide dielectric constant
eps_lo = 1  # the surrounding low-dielectric material
#h = 1       # the thickness of the waveguide (arbitrary units)
Y = 10      # the size of the computational cell in the y direction

## Here we define the size of the computational cell.  Since it is 2d,
## it has no-size in the z direction.  Because it is a waveguide in the
## x direction, then the eigenproblem at a given k has no-size in the
## x direction as well.
#geometry_lattice = mp.Lattice(size=(0, Y))

## the default-material is what fills space where we haven't placed objects
#default_material = mp.Medium(epsilon=eps_lo)

## a list of geometric objects to create structures in our computation:
## (in this case, we only have one object, a block to make the waveguide)
#geometry = [mp.Block(center=(0,0), # center of computational cell
                     #size=(mp.inf, h, mp.inf),
                     #material=mp.Medium(epsilon=eps_hi))]

## MPB discretizes space with a given resolution.   Here, we set
## a resolution of 32 pixels per unit distance.  Thus, with Y=10
## our comptuational cell will be 320 pixels wide.  In general,
## you should make the resolution fine enough so that the pixels
## are much smaller than the wavelength of the light.
##   -- to get high accuracy results, in practice you 
##      double the resolution until your answer stops changing
##      to your desired tolerance
#resolution = 32

## Generally, we want omega(k) for a range of k values.  MPB
## can automatically interpolate a set of k values between any
## given bounds.  Here, we will interpolate 10 k's between 0 and 2.
##
## in MPB, the k vectors are in the basis of the primitive 
## reciprocal lattice vectors.   Here, for a 1d cell with zero
## width in the x direction, the units of kx are just units of 2pi/a
## where a is our distance units.

#kmin = 0
#kmax = 2
#k_interp = 10
#k_points = mp.interpolate(k_interp, [mp.Vector3(kmin), mp.Vector3(kmax)])

#print(k_points)

#num_bands = 10

#ms = mpb.ModeSolver(num_bands=num_bands,
                    #k_points=k_points,
                    #geometry=geometry,
                    #geometry_lattice=geometry_lattice,
                    #resolution=resolution,
                    #default_material=default_material)

#ms.run_tm_yeven()

#tmyeven_freqs = ms.all_freqs
#print(tmyeven_freqs)

#print(tmyeven_freqs[:,0]) # omega(k) for band 1 (= column 0 in Python)

#ms.run_tm_yodd()
#tmyodd_freqs = ms.all_freqs

#kx = [k.x for k in ms.k_points]
#kx

#plt.figure(figsize=(10,7))
#plt.plot(kx, tmyeven_freqs, "ro-")
#plt.plot(kx, tmyodd_freqs, "bs-")
#plt.plot(kx, kx, "k-", linewidth=2)
#plt.plot(kx, kx / np.sqrt(eps_hi), "k--", linewidth=2)
#plt.fill([0,2,0],[0,2,2], facecolor=(0.9,0.9,0.9), zorder=3)
#plt.xlabel("$k_x a / 2\pi$")
#plt.ylabel("$\omega a / 2\pi c = fa/c = a/\lambda$")
#plt.ylim(0,2)
#plt.show()

#eps = ms.get_epsilon()

#y = np.linspace(-Y/2,Y/2,eps.size)
#plt.figure(figsize=(10,3))
#plt.plot(y, eps)
#plt.xlabel("$y$")
#plt.ylabel("$\epsilon$")
#plt.ylim(0,13)
#plt.show()

#ms.k_points = [mp.Vector3(1)]
#ms.run_tm(mpb.fix_efield_phase)

#ms.get_efield(1) # gets E field for band 1 at the last k point (kx=1)

#ms.get_efield(1).shape  # 4d array (y,x,z,3 components)

#plt.figure(figsize=(10,8))
#ez1 = ms.get_efield(1)[:,0,0,2] # the z component of band 1
#ez2 = ms.get_efield(2)[:,0,0,2] # the z component of band 2
#ez3 = ms.get_efield(3)[:,0,0,2] # the z component of band 3
## ez4 = ms.get_efield(4)[:,0,0,2] # the z component of band 3
#plt.plot(y, np.real(ez1), "b-")
#plt.plot(y, np.real(ez2), "r:")
#plt.plot(y, np.real(ez3), "k--")
## plt.plot(y, np.real(ez4), "g-")
#plt.legend(["band 1", "band 2", "band 3"])
#plt.show()

#print(np.dot(ez3, (eps * ez1)) / (np.linalg.norm(ez1) * np.linalg.norm(ez3)))

# waveguide width in um
w = 0.800

# unit cell size
a = 0.430

block = mp.Block(center=mp.Vector3(0, 0, 0), material=mp.Medium(epsilon=eps_hi), size=mp.Vector3(0.5, w/a, 1))
cylinder = mp.Cylinder(center=(0,0), radius=0.2, material=mp.Medium(epsilon=eps_hi))
k_points = mp.interpolate(200, [mp.Vector3(0),mp.Vector3(2)])
#k_points = []

ms2 = mpb.ModeSolver(
    num_bands=5,
    k_points=k_points,
    geometry=[block],    
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
