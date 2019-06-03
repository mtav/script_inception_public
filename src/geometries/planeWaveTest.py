#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import tempfile
import bfdtd
from bfdtd.bfdtd_parser import *

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('DSTDIR', default=tempfile.gettempdir(), nargs='?')
  args = parser.parse_args()  
  print(args.DSTDIR)

  # DSTDIR + BASENAME
  BASENAME = 'planeWaveTest'
  if not os.path.isdir(args.DSTDIR):
    os.mkdir(args.DSTDIR)

  # define a wavelength for calculations
  Lambda = 0.1

  # BFDTDobject
  sim = BFDTDobject()
  sim.boundaries.setBoundaryConditionsToPML()
  sim.box.upper=[2,1,1]

  # probes
  sim.appendProbe(bfdtd.Probe([0,0.5,0.5]))
  sim.appendProbe(bfdtd.Probe([0.25,0.5,0.5]))
  sim.appendProbe(bfdtd.Probe([0.5,0.5,0.5]))
  sim.appendProbe(bfdtd.Probe([0.75,0.5,0.5]))
  sim.appendProbe(bfdtd.Probe([1,0.5,0.5]))
  sim.appendProbe(bfdtd.Probe([1.25,0.5,0.5]))
  sim.appendProbe(bfdtd.Probe([1.5,0.5,0.5]))
  sim.appendProbe(bfdtd.Probe([1.75,0.5,0.5]))
  sim.appendProbe(bfdtd.Probe([2,0.5,0.5]))

  # excitation
  e = ExcitationWithUniformTemplate()
  e.plane_direction = [1,0,0]
  e.excitation_direction = ['Eyre', 'Hzre']
  e.centre = sim.box.getCentro()
  e.setLambda(Lambda)
  sim.appendExcitation(e)

  # write
  sim.autoMeshGeometry(Lambda/4.)
  sim.writeAll(os.path.join(args.DSTDIR, BASENAME))
  sim.writeShellScript(os.path.join(args.DSTDIR, BASENAME+'.sh'), EXE='fdtd64_2003', WORKDIR='$JOBDIR', WALLTIME=12)

if __name__ == "__main__":
  main()
