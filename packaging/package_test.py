#!/usr/bin/env python3
import code
import readline
import rlcompleter
from photonics import *

import photonics.bfdtd as bfdtd

print(bfdtd.Sphere)
sim = bfdtd.readBristolFDTD()
sim.runSimulation()

# change autocomplete to tab
readline.parse_and_bind("tab: complete")

code.interact(local=locals())
