#!/usr/bin/env python3

from bfdtd.bfdtd_parser import *

if __name__ == '__main__':
  PROBE_MAX = 439
  TIMESNAPSHOT_MAX = 439
  FREQUENCYSNAPSHOT_MAX = 836
  EPSILONSNAPSHOT_MAX = 439
  MODEFILTEREDPROBE_MAX = 43

  p = Probe()
  t = Time_snapshot()
  f = Frequency_snapshot()
  m = ModeFilteredProbe()
  e = EpsilonSnapshot()

  sim = BFDTDobject()
  sim.flag.iterations = 1

  sim.fileList = []
  sim.probe_list = PROBE_MAX*[p]
  sim.snapshot_list = []
  sim.writeAll('Probes')

  sim.fileList = []
  sim.probe_list = []
  sim.snapshot_list = TIMESNAPSHOT_MAX*[t]
  sim.writeAll('TimeSnapshots')

  sim.fileList = []
  sim.probe_list = []
  sim.snapshot_list = FREQUENCYSNAPSHOT_MAX*[f]
  sim.writeAll('FrequencySnapshots')

  # NOTE: Bristol FDTD 2003 does not support epsilon snapshots. Use 2008 or later instead.
  sim.fileList = []
  sim.probe_list = []
  sim.snapshot_list = EPSILONSNAPSHOT_MAX*[e]
  #sim.snapshot_list = 1*[e]
  sim.writeAll('EpsilonSnapshots')

  sim.excitation_list = [ExcitationWithGaussianTemplate()]

  sim.fileList = []
  sim.probe_list = []
  sim.snapshot_list = MODEFILTEREDPROBE_MAX*[m]
  sim.writeAll('ModeFilteredProbes')
