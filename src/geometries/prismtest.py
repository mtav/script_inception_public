#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import numpy
import argparse
import tempfile
import bfdtd
from bfdtd.bfdtd_parser import *
from utilities.common import *
from bfdtd.triangular_prism import TriangularPrism
from bfdtd.SpecialTriangularPrism import SpecialTriangularPrism
from bfdtd.excitationTemplate import *
from bfdtd.excitation_utilities import *

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('DSTDIR', default=tempfile.gettempdir(), nargs='?')
  args = parser.parse_args()  
  print(args.DSTDIR)
  
  pillar = BFDTDobject()

  ## define geometry
  offset = array([1,2,3])
  prism = SpecialTriangularPrism()
  prism.lower = offset+array([ 0,0,0 ])
  prism.upper = offset+array([ 5,1,2 ])
  prism.orientation = [2,0,1]
  prism.permittivity = pow(2.4,2)
  prism.conductivity = 0
  prism.NvoxelsX = 30
  prism.NvoxelsY = 30
  prism.NvoxelsZ = 30
  pillar.geometry_object_list.append(prism)

  # define excitation
  P_centre = prism.getGeoCentre()
  template_radius = prism.getInscribedSquarePlaneRadius(P_centre)
  print('template_radius = ',template_radius)
  #template_radius = 0.0307

  #(A1_global,B1_global,C1_global,A2_global,B2_global,C2_global) = prism.getGlobalEnvelopPoints()
  envelop = prism.getGlobalEnvelopPoints()

  # define probes
  probe = bfdtd.Probe(position = P_centre)
  pillar.probe_list.append(probe)
  for i in envelop:
    print(i)
    probe = bfdtd.Probe(position = i)
    pillar.probe_list.append(probe)

  # excitations  
  excitation, template = ExcitationWrapper(Ysym=False, centre=P_centre, size=template_radius, plane_direction='x', type='1D', excitation_direction=[0,0,1], frequency=123)
  pillar.appendExcitation(excitation)
  pillar.excitation_template_list.append(template)
  
  excitation, template = ExcitationWrapper(Ysym=False, centre=P_centre, size=template_radius, plane_direction='x', type='1D', excitation_direction=[0,1,0], frequency=123)
  pillar.appendExcitation(excitation)
  pillar.excitation_template_list.append(template)
  
  excitation, template = ExcitationWrapper(Ysym=False, centre=P_centre, size=template_radius, plane_direction='x', type='2D', excitation_direction=[0,0,1], frequency=123)
  pillar.appendExcitation(excitation)
  pillar.excitation_template_list.append(template)
    
  # write
  #DSTDIR = os.getenv('TESTDIR')
  BASENAME = 'prismtest'
  pillar.writeAll(os.path.join(args.DSTDIR, BASENAME), BASENAME)

if __name__ == "__main__":
  main()
