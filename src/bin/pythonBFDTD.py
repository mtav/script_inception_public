#!/usr/bin/env python3

# A script reading in BFDTD files into a BFDTDobject named "sim" and then dropping to an interactive python prompt for further processing.
## for use with python3 -i:
# python3 -i ./pythonBFDTD.py FILE1 FILE2 ...
## for use like usual python3 scripts:
# ./pythonBFDTD.py FILE1 FILE2 ...

import os
import sys
import code
print('argv = {}'.format(sys.argv))

# read in ~/.pystartup to have all the desired modules
pystartup = os.path.expanduser("~/.pystartup")
with open(pystartup) as f:
  code_object = compile(f.read(), pystartup, 'exec')
  exec(code_object)

# read in the BFDTD files
sim = bfdtd.readBristolFDTD(*sys.argv[1:])

# start the interactive shell
code.interact(local=locals())
