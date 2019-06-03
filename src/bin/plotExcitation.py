#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ..todo:: plot FFT
# ..todo:: finish checking against real signals
# ..todo:: make it work on BC3
# ..todo:: could create extra probe at source location

import os
import re
import sys
import pick
import numpy
import bfdtd
import argparse
import tempfile
import subprocess
import matplotlib.pyplot as plt
import utilities.common
import utilities.prnutils

def plotProbe(filename, component=None, title=None, plot_list=None, normalize=False):
  
  if plot_list is None:
    plot_list = []
  
  (h, d) = utilities.prnutils.readProbeFile(filename)
  if component is None:
    component, index = pick.pick(h, 'Select component to plot:')
    print(component, index)
  
  y = d[component]
  if normalize:
    y = y/max(y)
  
  probe_signal, = plt.plot(d['time_mus'], y, label='probe data')
  plot_list.append(probe_signal)
  
  plt.xlabel('Time ($\mu s$)')
  plt.ylabel('{} (arbitrary units)'.format(component))
  extra_title = '{} - {}'.format(filename, component)
  if title is None:
    plt.title(extra_title)
  else:
    plt.title('{} - {}'.format(title, extra_title))
  plt.legend(handles=plot_list)
  plt.show(block=False)
  return

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('infile')
  parser.add_argument('-v', '--verbose', action="count", dest="verbosity", default=0, help='general verbosity level')
  parser.add_argument('-t', '--t-range', nargs=2, metavar=('TMIN', 'TMAX'), type=float)
  parser.add_argument('-r', '--run-simulation', action="store_true")
  parser.add_argument('-f', '--fix-simulation', action="store_true")
  parser.add_argument('-n', '--normalize', action="store_true")
  parser.add_argument('-d', '--simulation-directory', default=None)
  parser.add_argument('-p', '--probe', help='probe file to use')
  parser.add_argument('-c', '--component', help='component to plot', choices=['Ex', 'Ey', 'Ez', 'Hx', 'Hy', 'Hz'])
  parser.add_argument('--simulation-verbosity', type=int, default=0, help='simulation verbosity level')
  
  args = parser.parse_args()
  print(args)
  
  plot_list = []
  
  # read input
  sim = bfdtd.readBristolFDTD(args.infile, verbosity=args.verbosity)
  
  if args.fix_simulation:
    sim.fixSimulation()
  
  E = sim.getExcitations()[0]
  
  w = E.getTimeConstant()
  tau = E.getTimeOffset()
  f = E.getFrequency()
  A = E.getAmplitude()
  
  if args.t_range:
    t = numpy.linspace(*args.t_range, 100)
  else:
    t = numpy.array(utilities.common.matlab_range(-20*w+tau, (1/f)/100, 20*w+tau))
  
  u = A * numpy.exp( -1 * numpy.power(t-tau,2) / numpy.power(w, 2) ) * numpy.sin( 2 * numpy.pi * f * t )
  if args.normalize:
    u = u/max(u)
  
  #plt.rc('text', usetex=True)
  theoretical_signal, = plt.plot(t, u, label='theoretical signal')
  plot_list.append(theoretical_signal)
  
  plt.xlabel('Time ($\mu s$)')
  plt.ylabel('amplitude (arbitrary units)')
  title = 'fix_simulation = {}, Excited components: {}'.format(args.fix_simulation, E.getExcitedComponentNames())
  plt.title(title)
  plt.show(block=False)
  
  if args.run_simulation:
    if args.simulation_directory:
      simulation_directory = args.simulation_directory
    else:
      simulation_directory = tempfile.mkdtemp()
    print('======================================================')
    print('simulation_directory = {}'.format(simulation_directory))
    print('======================================================')
  
    sim.disableAutoFix()
    sim.disableSafetyChecks()
    
    sim.clearFileList()
    sim.clearAllSnapshots()
    sim.clearGeometry()
    
    sim.setSimulationTime(sim.getExcitationEndTimeMax())
    #sim.checkSimulation()
    
    #sim.writeAll(simulation_directory)
    #sim.writeTorqueJobDirectory(simulation_directory)
    sim.runSimulation(simdir=simulation_directory, verbosity=args.simulation_verbosity)
    print('======================================================')
    print('simulation_directory = {}'.format(simulation_directory))
    print('======================================================')
  
  if args.probe:
    plotProbe(args.probe, component=args.component, title=title, plot_list=plot_list, normalize=args.normalize)
  
  input("Press Enter to continue...")
  
  return 0

if __name__ == '__main__':
  main()
