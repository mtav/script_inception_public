#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import numpy
import argparse
import tempfile
import subprocess
import textwrap
from utilities.common import matlab_range

#testq              --      --    01:00:00   --    0   0 --   E R
#veryshort          --      --    12:00:00   --  435 431 --   E R
#short              --      --    120:00:0   --  376 539 --   E R
#medium             --      --    240:00:0   --  243  52 --   E R
#long               --      --    360:00:0   --  135  13 --   E R

ressource_dictionary = {32: [1, 12],
                        64: [1, 120],
                        128: [2, 240],
                        256: [10, 360],
                        }

class coatedWoodpile():
  
  resolution = 32
  thickness_mum = 0.010
  coating_index = 3.1
  walltime = 120
  ppn = 2
  
  a_mum = 1
  rod_width_mum = 0.240
  rod_height_mum = 0.580
  #a=c=1
  
  dstdir = None
  basename = 'BCC-coated-woodpiles'
  
  _coated_rods = True
  
  @property
  def coated_rods(self):
    if self._coated_rods:
      return 'true'
    else:
      return 'false'
  
  @coated_rods.setter
  def coated_rods(self, value):
      self._coated_rods = value
  
  def generate(self):
    if self.dstdir:
      dstdir = self.dstdir
    else:
      dstdir = tempfile.gettempdir()
      
    print('dstdir = {}'.format(dstdir))
    
    [self.ppn, self.walltime] = ressource_dictionary[self.resolution]
    
    self.generateShellScript(dstdir)
    self.generateMPBscript(dstdir)
  
  def generateShellScript(self, dstdir):
    outfilename = os.path.join(dstdir, self.basename + '.mpirun.sh')
    with open(outfilename, 'w') as outfile:
      outfile.write(textwrap.dedent('''\
      #!/bin/bash
      # request resources:
      #PBS -l nodes=1:ppn={self.ppn}
      #PBS -l walltime={self.walltime}:00:00
      
      cd $PBS_O_WORKDIR
      time mpb ./{self.basename}.ctl > ./{self.basename}.out
      '''.format(self=self) ))
    pass
  
  def generateMPBscript(self, dstdir):
    outfilename = os.path.join(dstdir, self.basename + '.ctl')
    with open(outfilename, 'w') as outfile:
      outfile.write(textwrap.dedent(r'''      (define-param a {self.a_mum}); microns
      ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
      ;;;;; FCT-woodpile geometry with optional coated rods
      ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
      ;;;;; geometry parameters
      ;;;;; all dimensions normalized by the VerticalPeriod, i.e. height of 4 layers
      ;(define-param rod_width  (/ 0.225 a)) ; width of the logs
      ;(define-param rod_height (/ 0.400 a)) ; height of logs (should be 1/4 for fcc to not overlap)
      (define-param rod_width (/ {self.rod_width_mum:.3f} a )) ; width of the logs
      (define-param rod_height (/ {self.rod_height_mum:.3f} a) ) ; height of logs (should be 1/4 for fcc to not overlap)
      (define-param _interRodDistance (sqrt 0.5)) ; distance between rods in one layer (horizontal period)
      
      (define-param elliptical-rod-shape? true); if true, use elliptical rods, else blocks
      
      (define-param coated-rods? {self.coated_rods}); if true, add coating
      (define-param coating-thickness (/ {self.thickness_mum:.3f} a))
      
      (define-param backfill-index 1.00 )
      (define-param rod-index      1.52 )
      (define-param coating-index  {self.coating_index:.2f} )
      
      (define-param _lattice_mode 2) ; 0=FCT, 1=FCC, 2=BCC (FCC and BCC will override any interRodDistance setting)
      ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
      ;;;;; simulation parameters
      (set-param! verbose? true)
      (set-param! num-bands 16)
      (define-param k-interp 9)
      (define-param output_epsilon_only? false) ; if true, exit after outputting epsilon
      ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
      ;;;;; load woodpile function (includes lattice setup)
      (load-from-path "MPB_woodpile_FCT.ctl")
      ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
      ;;;;; non-user-defined parameters
      (define interLayerDistance 0.25) ; distance between layers (usually VerticalPeriod/4)
      (define overlap (- 1 (/ interLayerDistance rod_height)) )
      (define VerticalPeriod (* 4 interLayerDistance))
      (define rod_coated_height (+ rod_height (* 2 coating-thickness)))
      (define rod_coated_width  (+ rod_width  (* 2 coating-thickness)))
      
      ;;; set up k-point list
      ;; (set! k-points (interpolate k-interp FCC_standard_kpoints))
      ;; (set_kpoints FCC_standard_kpoints)
      ;; (define kpoint_list RotAround_-x+y_quarter)
      ;; (define kpoint_list (list X+z U+z+x+y L+x+y+z K+x+y))
      ;; (define kpoint_list (list U+z+x+y L+x+y+z K+x+y)) ;; Sun 23 Feb 18:15:45 GMT 2020
      (define kpoint_list (list U+z+x+y L+x+y+z))
      
      (set_kpoints kpoint_list)
      (print_kpoints_labels_matlab_style kpoint_list)
      
      ;; (exit)
      
      ;;; set up materials
      (set! default-material (make dielectric (index backfill-index) ) )
      (define rod-material (make dielectric (index rod-index)))
      (define coating-material (make dielectric (index coating-index)))
      ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
      ;;;;; print summary of essential parameters
      (print "_lattice_mode = " _lattice_mode "\n")
      (print "_a = " _a "\n")
      (print "_b = " _b "\n")
      (print "_c = " _c "\n")
      
      (print "backfill-index = " backfill-index "\n")
      (print "rod-index = " rod-index "\n")
      
      (print "rod_width = " rod_width "\n")
      (print "rod_height = " rod_height "\n")
      (print "_interRodDistance = " _interRodDistance "\n")
      (print "interLayerDistance = " interLayerDistance "\n")
      (print "VerticalPeriod = " VerticalPeriod "\n")
      
      (print "rod aspect ratio rod_height/rod_width = " (/ rod_height rod_width) "\n")
      (print "overlap = " overlap "\n")
      
      (print "elliptical-rod-shape? = " elliptical-rod-shape? "\n")
      (print "coated-rods? = " coated-rods? "\n")
      (print "coating-index = " coating-index "\n")
      (print "coating-thickness = " coating-thickness "\n")
      ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
      ;;;;; set up geometry
      (set! geometry
        (append
          (if coated-rods?
            (MPB_woodpile_FCT elliptical-rod-shape? coating-material rod_coated_width rod_coated_height)
            (list)
          )
          (MPB_woodpile_FCT elliptical-rod-shape? rod-material rod_width rod_height)
        )
      )
      ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
      ;;;;; create a custom prefix for output files
      
      (use-modules (ice-9 format)) ; for formatting support on BC3
      
      (set-param! filename-prefix
        (string-append
          "woodpile-FCT"
          "_w-" (format #f "~,3f" rod_width)
          "_h-" (format #f "~,3f" rod_height)
          "_i-" (format #f "~,3f" _interRodDistance)
          "_t-" (format #f "~,3f" coating-thickness)
          "_nb-" (format #f "~,2f" backfill-index)
          "_nr-" (format #f "~,2f" rod-index)
          "_nc-" (format #f "~,2f" coating-index)
          "_l-" (format #f "~d" _lattice_mode)
          "_e-" (if elliptical-rod-shape? "true" "false")
          "_c-" (if coated-rods? "true" "false")
          "_"
          )
      )
      
      (print "filename-prefix = " filename-prefix "\n")
      ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
      ;;;;; run simulation
      (set! resolution {self.resolution})
      
      ; reset
      (init-params NO-PARITY true); for MPB -> it looks like this leads to init output and is done again when run is called. -> leads to output processing issues.
      
      ;;; output epsilon.h5 file only
      (if output_epsilon_only?
        (begin
          ;; (init-fields) ; for MEEP
          (output-epsilon)
          (exit)
        )
      )
      
      ;;; calculate bands
      (run)
      '''.format(self=self) ))
    
    pass

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('DSTDIR', default=tempfile.gettempdir(), nargs='?')
  parser.add_argument('-v', '--verbose', action="count", dest="verbosity", default=0, help='verbosity level')
  args = parser.parse_args()
  # print(args)
  
  if not os.path.isdir(args.DSTDIR):
    os.mkdir(args.DSTDIR)
  
  #128 -> ~4GB -> PPN = 1 or 2
  #256 -> ~33GB RAM -> PPN = 9
  for resolution in [32, 64, 128, 256]:
  
    # generate a non-coated reference
    sim = coatedWoodpile()
    sim.coated_rods = False
    sim.resolution = resolution
    sim.dstdir = os.path.join(args.DSTDIR, 'resolution={:d}'.format(resolution), 'non-coated')
    os.makedirs(sim.dstdir, exist_ok=True)
    sim.generate()
    
    #thickness_list = numpy.linspace(0.001, 0.005, 5)
    # thickness_list = numpy.append(numpy.linspace(0.006, 0.009, 4), numpy.linspace(0.010,0.150,15))
    # thickness_list = [0.001, 0.002, 0.003, 0.004, 0.006, 0.015]

    # coating_index_list = numpy.arange(2.0, 3.1+0.1, 0.1)
    # thickness_list = numpy.arange(10, 30+5, 5)
    # cf https://stackoverflow.com/questions/37571622/matlab-range-in-python
    # Note: Does not work properly for float or float64!!!

    # # SUCCESS
    # eps = numpy.finfo(numpy.float32).eps
    # coating_index_list = numpy.arange(2.0, 3.1+eps, 0.1)
    # thickness_list = numpy.arange(10, 30+eps, 5)
    # print(coating_index_list)
    # print(thickness_list)
    # print(len(coating_index_list))
    # print(len(thickness_list))
    # print(len(coating_index_list) * len(thickness_list))

    # # FAIL
    # eps = numpy.finfo(numpy.float64).eps
    # coating_index_list = numpy.arange(2.0, 3.1+eps, 0.1)
    # thickness_list = numpy.arange(10, 30+eps, 5)
    # print(coating_index_list)
    # print(thickness_list)
    # print(len(coating_index_list))
    # print(len(thickness_list))
    # print(len(coating_index_list) * len(thickness_list))

    # # FAIL
    # coating_index_list = matlab_range(2.0, 0.1, 3.1)
    # thickness_list = matlab_range(10, 5, 30)
    # print(coating_index_list)
    # print(thickness_list)
    # print(len(coating_index_list))
    # print(len(thickness_list))
    # print(len(coating_index_list) * len(thickness_list))

    # SUCCESS
    coating_index_list = numpy.linspace(2.0, 3.1, 12)
    thickness_list = numpy.linspace(0.010, 0.030, 5)    
    # print(coating_index_list)
    # print(thickness_list)
    # print(len(coating_index_list))
    # print(len(thickness_list))
    # print(len(coating_index_list) * len(thickness_list))
    # print('Total simulations: ', (len(coating_index_list) * len(thickness_list) * 4) + 4)

    # coating_index_list = [3.1]
    for coating_index in coating_index_list:
      for thickness_mum in thickness_list:
        sim = coatedWoodpile()
        sim.coated_rods = True
        sim.resolution = resolution
        sim.thickness_mum = thickness_mum
        sim.coating_index = coating_index
        sim.dstdir = os.path.join(args.DSTDIR, 'resolution={:d}'.format(resolution), 'coating_index={:.2f}'.format(coating_index), 'thickness_mum={:.3f}'.format(thickness_mum))
        os.makedirs(sim.dstdir, exist_ok=True)
        sim.generate()

  return 0

if __name__ == '__main__':
  main()

  #resolution = 123
  #thickness = 45
  #refractive_index = 123
  #generate(resolution, thickness, refractive_index)
  #main()
