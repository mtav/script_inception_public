#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from numpy import array
from bfdtd.bfdtd_parser import BFDTDobject, Excitation, Probe, Block
from bfdtd.snapshot import EpsilonBox, ModeVolumeBox, ModeVolumeBoxFull

def main():

  ### basic setup of the simulation

  sim = BFDTDobject()
  sim.setExecutable('fdtd64_2014')
  sim.setIterations(1)

  S = [1,2,3]
  N = 3*array([10,20,30])
  sim.setSizeAndResolution(S, N)

  xblock = Block()
  xblock.setName('xblock')
  location = [0.750, 1.000, 1.500]
  dimensions = [0.500, 0.200, 0.200]
  xblock.setLocation(location)
  xblock.setSize(dimensions)
  xblock.setRelativePermittivity(2)

  yblock = Block()
  yblock.setName('yblock')
  location = [0.500, 1.500, 1.500]
  dimensions = [0.200, 1.000, 0.200]
  yblock.setLocation(location)
  yblock.setSize(dimensions)
  yblock.setRelativePermittivity(3)

  zblock = Block()
  zblock.setName('zblock')
  location = [0.500, 1.000, 2.250]
  dimensions = [0.200, 0.200, 1.500]
  zblock.setLocation(location)
  zblock.setSize(dimensions)
  zblock.setRelativePermittivity(4)
  
  sim.appendGeometryObject([xblock, yblock, zblock])

  c = sim.getCentro()
  e = sim.appendExcitation(Excitation())
  e.setExtension(c,c)
  e.setEx()

  ### various snapshot tests

  # A pythonic way to switch between just outputting the files and running them.
  #myfunc = sim.runSimulation
  myfunc = sim.writeAll
  
  # full MV box
  MV = ModeVolumeBoxFull()
  sim.setSnapshots([MV])

  MV.setPlaneOrientationX()
  sim.setFileBaseName('MV-full-X')
  myfunc(sim.getFileBaseName())

  MV.setPlaneOrientationY()
  sim.setFileBaseName('MV-full-Y')
  myfunc(sim.getFileBaseName())

  MV.setPlaneOrientationZ()
  sim.setFileBaseName('MV-full-Z')
  myfunc(sim.getFileBaseName())
  
  # MV box from lower to centre
  MV = ModeVolumeBox()
  MV.setExtension(sim.getLower(), sim.getCentro())
  sim.setSnapshots([MV])

  MV.setPlaneOrientationX()
  sim.setFileBaseName('MV-lower-to-centre-X')
  myfunc(sim.getFileBaseName())

  MV.setPlaneOrientationY()
  sim.setFileBaseName('MV-lower-to-centre-Y')
  myfunc(sim.getFileBaseName())

  MV.setPlaneOrientationZ()
  sim.setFileBaseName('MV-lower-to-centre-Z')
  myfunc(sim.getFileBaseName())

  # MV box from centre to upper
  MV = ModeVolumeBox()
  MV.setExtension(sim.getCentro(), sim.getUpper())
  sim.setSnapshots([MV])

  MV.setPlaneOrientationX()
  sim.setFileBaseName('MV-centre-to-upper-X')
  myfunc(sim.getFileBaseName())

  MV.setPlaneOrientationY()
  sim.setFileBaseName('MV-centre-to-upper-Y')
  myfunc(sim.getFileBaseName())

  MV.setPlaneOrientationZ()
  sim.setFileBaseName('MV-centre-to-upper-Z')
  myfunc(sim.getFileBaseName())
  
  # other
  sim.clearAllSnapshots()
  eps = sim.addEpsilonBox()

  eps.setPlaneOrientationX()
  sim.setFileBaseName('slice_x')
  #sim.writeAll(sim.getFileBaseName())
  myfunc(sim.getFileBaseName())

  eps.setPlaneOrientationY()
  sim.setFileBaseName('slice_y')
  myfunc(sim.getFileBaseName())
  #sim.writeAll(sim.getFileBaseName())
  #myfunc('.')

  eps.setPlaneOrientationZ()
  sim.setFileBaseName('slice_z')
  myfunc(sim.getFileBaseName())
  #sim.writeAll(sim.getFileBaseName())
  #myfunc('.')

  # smaller MV box:
  epsbox = EpsilonBox()
  epsbox.setPlaneOrientationY()
  epsbox.setCentro(c)
  epsbox.setSize(0.5*sim.getSize())
  sim.setSnapshots([epsbox])

  epsbox.setPlaneOrientationX()
  sim.setFileBaseName('mini-box-centered-X')
  myfunc(sim.getFileBaseName())

  epsbox.setPlaneOrientationY()
  sim.setFileBaseName('mini-box-centered-Y')
  myfunc(sim.getFileBaseName())

  epsbox.setPlaneOrientationZ()
  sim.setFileBaseName('mini-box-centered-Z')
  myfunc(sim.getFileBaseName())

  epsbox.setCentro(epsbox.getCentro()+array([1/4,0,0]))

  epsbox.setPlaneOrientationX()
  sim.setFileBaseName('mini-box-offset-X')
  #sim.writeAll(sim.getFileBaseName())
  myfunc(sim.getFileBaseName())

  epsbox.setPlaneOrientationY()
  sim.setFileBaseName('mini-box-offset-Y')
  #sim.writeAll(sim.getFileBaseName())
  myfunc(sim.getFileBaseName())

  epsbox.setPlaneOrientationZ()
  sim.setFileBaseName('mini-box-offset-Z')
  #sim.writeAll(sim.getFileBaseName())
  myfunc(sim.getFileBaseName())

  epsbox.setPlaneOrientationX()

  epsbox.setExtension(sim.getCentro(), sim.getExtension()[1])
  sim.setFileBaseName('mini-box-centre-to-upper-X')
  myfunc(sim.getFileBaseName())

  epsbox.setExtension(sim.getExtension()[0], sim.getCentro())
  sim.setFileBaseName('mini-box-lower-to-centre-X')
  myfunc(sim.getFileBaseName())

  epsbox.setPlaneOrientationY()

  epsbox.setExtension(sim.getCentro(), sim.getExtension()[1])
  sim.setFileBaseName('mini-box-centre-to-upper-Y')
  myfunc(sim.getFileBaseName())

  epsbox.setExtension(sim.getExtension()[0], sim.getCentro())
  sim.setFileBaseName('mini-box-lower-to-centre-Y')
  myfunc(sim.getFileBaseName())

  epsbox.setPlaneOrientationZ()

  epsbox.setExtension(sim.getCentro(), sim.getExtension()[1])
  sim.setFileBaseName('mini-box-centre-to-upper-Z')
  myfunc(sim.getFileBaseName())

  epsbox.setExtension(sim.getExtension()[0], sim.getCentro())
  sim.setFileBaseName('mini-box-lower-to-centre-Z')
  myfunc(sim.getFileBaseName())
  
  #myfunc('.')
  
  #sim.clearAllSnapshots()
  #eps_full = sim.appendSnapshot(EpsilonSnapshot())
  #eps_partial = sim.appendSnapshot(EpsilonSnapshot())
  #sim.setFileBaseName('full_vs_partial')
  #myfunc(sim.getFileBaseName())
      	
  return 0

if __name__ == '__main__':
	main()

