#!/usr/bin/env python3

from bfdtd.bfdtd_parser import *
from numpy import *
from utilities.common import *

def main():

    # arguments to adapt for each simulation
    basename = 'PhotonicCrystallineDiamond'
    infile = 'PhotonicCrystallineDiamond.in'
    destdir = 'mode_volume'
    executable = 'fdtd64_2013'
    walltime = 360
    first = 12800
    repetition = 32000
    starting_sample = 12800
    frequency_vector = [154052000] # should be list of frequencies from the peaks

    # read in simulation
    sim = readBristolFDTD(infile)
    print('sim.getTimeStep() = ',sim.getTimeStep())
    E = sim.excitation_list[0]
    print('E.getFrequencyRange() =', E.getFrequencyRange())
    print('E.getFrequency() =', E.getFrequency())
    T = 1/E.getFrequency();
    print('1/E.getFrequency() =', 1/E.getFrequency())
    print(T/sim.getTimeStep())
    (fmin, fmax) = E.getFrequencyRange()
    print((1/fmin)/sim.getTimeStep())
    print((1/fmax)/sim.getTimeStep())
    print(get_c0()/fmin)
    print(get_c0()/fmax)

    excitation_centre = E.getCentro()
    print(excitation_centre)

    # clear any previous snapshots
    sim.clearAllSnapshots()

    # Add snapshpots along Z axis to calculate the mode volume
    pos_list = sim.mesh.getZmesh()
    pos_mid_idx, pos_mid_value = findNearestInSortedArray(pos_list, excitation_centre[2], 0)
    reduced_range = pos_list[ pos_mid_idx-25:pos_mid_idx+25+1]

    for pos in reduced_range:
        eps = sim.addEpsilonSnapshot('Z',pos)
        F = sim.addFrequencySnapshot('Z',pos)
        F.name = 'ModeVolume.freq'
        F.first = first
        F.repetition = repetition
        F.starting_sample = starting_sample
        F.frequency_vector = frequency_vector

    # Add full X,Y central snapshots for reference
    for i in [0,1]:
        letter = ['X','Y','Z'][i]
        eps = sim.addEpsilonSnapshot(letter, excitation_centre[i])
        f = sim.addFrequencySnapshot(letter, excitation_centre[i])
        f.name = 'central.'+letter+'.fsnap'
        f.first = first
        f.repetition = repetition
        f.starting_sample = starting_sample
        f.frequency_vector = frequency_vector


    sim.fileList = []
    sim.writeAll(destdir, basename)
    sim.writeShellScript(destdir + os.path.sep + basename + '.sh', basename, executable, '$JOBDIR', WALLTIME = walltime)

    pass

if __name__ == '__main__':
    main()
