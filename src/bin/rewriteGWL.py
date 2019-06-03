#!/usr/bin/env python3

import sys
from GWL.GWL_parser import GWLobject

obj = GWLobject()
obj.readGWL(sys.argv[1])
obj.writeGWL(sys.argv[2])
