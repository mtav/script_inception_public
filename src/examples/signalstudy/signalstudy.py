#!/usr/bin/env python3

import bfdtd
##from bfdtd.bfdtd_parser import BFDTDobject, Excitation, Probe
#import subprocess
#import os
from numpy import array, linspace, ceil
#from bfdtd.snapshot import TimeSnapshotBoxFull

#from pylab import plot, show, title, xlabel, ylabel, subplot, xlim, ylim

def test0():
  # create files
  sim = bfdtd.BFDTDobject()
  S = 3
  N = 30
  sim.setSizeAndResolution([S,S,S],[N,N,N])
  c = sim.getCentro()

  #sim.setBoundaryConditionsToPML()

  E = sim.appendExcitation(bfdtd.Excitation())
  #E.setExtension(c-array([0.25,0,0]),c+array([0.25,0,0]))
  E.setExtension(c,c)
  E.setEx()

  dt = sim.getTimeStep()
  T = 10*dt

  #E.setTimeOffset(100*T)
  #E.setFrequency(10/T)
  #E.setTimeConstant(20*T)
  #E.setFrequency(10/E.getTimeConstant())
  f0 = 1/T
  Q = 100
  df = f0/Q
  #E.setFrequency(f0)
  #E.setFrequencyRange(f0-df, f0+df)
  print(E.setFrequencyRange(5e8, 5.5e8))

  E.setTimeOffset(20*E.getTimeConstant())
  E.setAmplitude(1)

  p = sim.appendProbe(bfdtd.Probe())
  p.setPosition(c)
  p.setStep(1)

  print(T)
  print(1/T)
  print(100*T)
  sim.setTimeStep((1/E.getFrequency())/100)
  #sim.setSimulationTime(1e-7)
  sim.setSimulationTime(E.getTimeOffset()+20*E.getTimeConstant())


  print(sim.getIterations())
  print(E.getFrequencyRange())
  print('A={}; tau={}; w={}; f={}; fmin={}; fmax={};'.format(E.getAmplitude(), E.getTimeOffset(), E.getTimeConstant(), E.getFrequency(), *E.getFrequencyRange()))

  # run simulation
  sim.setExecutable('fdtd64_2013')
  sim.runSimulation('.')

  # plot result

  # then in Matlab:
  #t=-2*w+tau:(1/f)/10:2*w+tau;
  #plot(t,A*exp(-(t-tau).^2/w^2).*exp(i*2*pi*f*t),'r');
  #hold on;
  #data=dlmread('p01_id_.prn','',1,0); plot(1e-12*data(:,1),data(:,2),'b');

  #t = -20*w+tau:(1/f)/100:20*w+tau;
  #u = A*exp(-(t-tau).^2/w^2).*sin(2*pi*f*t);
  #[calcFFT_output, lambda_vec_mum, freq_vec_Mhz] = calcFFT(u, t(2)-t(1));
  #Y = calcFFT_output.*conj(calcFFT_output);
  #plot(t,u)
  #plot(freq_vec_Mhz,Y);
  #axis([f-1/w,f+1/w,min(Y),max(Y)])
  #vline(fmin)
  #vline(fmax)

  # to plot the FFT:
  # t=-20*w+tau:(1/f)/100:20*w+tau; u=A*exp(-(t-tau).^2/w^2).*sin(2*pi*f*t); [calcFFT_output, lambda_vec_mum, freq_vec_Mhz] = calcFFT(u, t(2)-t(1)); Y=calcFFT_output.*conj(calcFFT_output); plot(freq_vec_Mhz,Y); axis([f-1/w,f+1/w,min(Y),max(Y)])

  # A=10.0; tau=2.7e-08; w=4e-09; f=2500000000.0;
  # t=-200*w+tau:(1/f)/100:200*w+tau; u=A*exp(-(t-tau).^2/w^2).*sin(2*pi*f*t); [calcFFT_output, lambda_vec_mum, freq_vec_Mhz] = calcFFT(u, t(2)-t(1)); Y=calcFFT_output.*conj(calcFFT_output); plot(freq_vec_Mhz,Y); axis([f-1/w,f+1/w,min(Y),max(Y)])
  # hold on; plot(freq_vec_Mhz, max(Y)*(exp(-pi^2*w^2*(freq_vec_Mhz-f).^2)).^2,'go');

def test1():
  # effect of dipole length
  sim = bfdtd.BFDTDobject()

  S = 3
  N = 30
  sim.setSizeAndResolution([S,S,S],[N,N,N])
  c = sim.getCentro()

  E = sim.appendExcitation(bfdtd.Excitation())
  E.setEx()
  E.setLocation(c)

  dt = sim.getTimeStep()
  T = 10*dt
  f0 = 1/T
  Q = 100
  df = f0/Q

  #E.setTimeOffset(100*T)
  #E.setFrequency(10/T)
  #E.setTimeConstant(20*T)
  #E.setFrequency(10/E.getTimeConstant())
  #E.setFrequency(f0)
  #E.setFrequencyRange(f0-df, f0+df)
  print(E.setFrequencyRange(5e8, 5.5e8))

  E.setTimeOffset(20*E.getTimeConstant())
  E.setAmplitude(1)

  p = sim.appendProbe(bfdtd.Probe())
  p.setLocation(c)
  p.setStep(1)

  print(T)
  print(1/T)
  print(100*T)
  sim.setTimeStep((1/E.getFrequency())/100)
  #sim.setSimulationTime(1e-7)
  sim.setSimulationTime(E.getTimeOffset()+20*E.getTimeConstant())
  #sim.setIterations(1)

  for L in linspace(0,1,10):
    outdir = 'LX_{:.3f}'.format(L)
    print('outdir =', outdir)
    E.setSize([L,0,0])
    sim.runSimulation(outdir)

    outdir = 'LY_{:.3f}'.format(L)
    print('outdir =', outdir)
    E.setSize([0,L,0])
    sim.runSimulation(outdir)

    outdir = 'LZ_{:.3f}'.format(L)
    print('outdir =', outdir)
    E.setSize([0,0,L])
    sim.runSimulation(outdir)

  return

def test2():
  sim = bfdtd.BFDTDobject()
  S = 1
  N = 30
  sim.setSizeAndResolution([S,S,S],[N,N,N])

  c = sim.getCentro()

  E = sim.appendExcitation(bfdtd.Excitation())
  E.setEx()
  E.setLocation(c)
  E.setSize([0,0,0])

  dt_max = sim.getTimeStepMax()
  T_max = 10*dt_max
  f_min = 1/T_max
  Q = 100
  #df = f0_min/Q
  f_max = ((Q+1/2)/(Q-1/2))*f_min

  print(E.setFrequencyRange(f_min, f_max))

  E.setTimeOffset(1*E.getTimeConstant())
  E.setAmplitude(1)

  p = sim.appendProbe(bfdtd.Probe())
  p.setLocation(c)
  p.setStep(1)

  sim.setTimeStep((1/E.getFrequency())/100)
  #sim.setSimulationTime(E.getTimeOffset()+10*E.getTimeConstant())
  
  sim.setIterations( ceil( E.getTimeOffset()/sim.getTimeStep() ) + 99)
  
  Tbox = sim.appendSnapshot(bfdtd.TimeSnapshotBoxFull())
  Tbox.setFirst(sim.getIterations()-99)
  Tbox.setRepetition(1)

  print(E.getTimeOffset()/sim.getTimeStep())
  print(sim.getIterations())

  sim.runSimulation('/tmp/dipole-test2', verbosity=2)
  return

if __name__ == '__main__':
  test2()
