'''
This module contains BFDTD related code. However, it might be extended to more general FDTD utilities later, so it can be used with other FDTD software.

.. todo:: Once design is cleaner and more stable, get rid of import * statements? (According to docs, using * is not recommended (should specify all or use the __init.py__ files), but for the moment, this is a simple working solution while things change a lot.)

'''

from .BFDTDobject import *
from .bfdtd_parser import *
from .snapshot import *
from .probe import *
from .GeometryObjects import *
from .meshobject import increaseResolution3D
