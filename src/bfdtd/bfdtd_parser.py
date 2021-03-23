#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This is the main module for Bristol FDTD related classes and functions. It provides an easier way to work with Bristol FDTD.

Example::

  #!/usr/bin/env python3
  # -*- coding: utf-8 -*-

  # import everything from the bfdtd module into current namespace
  from bfdtd import *

  # create a BFDTDobject instance, which will store everything related to the simulation
  sim = BFDTDobject()

  # set a size and resolution
  # Note: This will create a homogeneous mesh. For a custom mesh, please refer to some of the existing scripts. The meshing system is still changing a lot.)
  sim.setSizeAndResolution([10,10,10],[100,100,100])

  # create an object
  obj = Cylinder()

  # set some of its parameters
  obj.setLocation([1,2,3])
  obj.setStartEndPoints([-1,2,-5], [1,1,1])
  obj.setOuterRadius(0.5)

  # add the object to the simulation
  sim.appendGeometryObject(obj)

  # add an excitation to the simulation
  E = Excitation()
  sim.appendExcitation(E)

  # add a probe to the simulation
  P = Probe()
  P.setPosition([4,5,6])
  sim.appendProbe(P)

  # add a snapshot to the simulation
  F = FrequencySnapshot()
  F.setFrequencies([100])
  sim.appendSnapshot(F)

  # write out only a .geo file
  sim.writeGeoFile('foo.geo')

  # write out only a .inp file
  sim.writeInpFile('foo.inp')

  # write out only a .in file
  sim.writeFileList('foo.in')

  # write out all files necessary to submit the job using qsub (i.e. the *Torque* queueing system).
  sim.writeTorqueJobDirectory('somedir')

  # You can even run the simulation directly. Files will be written as necessary.
  sim.runSimulation()

For more examples, please have a look in the **script_inception_public/examples** directory.

Developer notes:

| The BFDTD simulation box always goes from (0,0,0) to (Sx,Sy,Sz).
| The MEEP/MPB simulation box always goes from (-Sx/2,-Sy/2,-Sy/2) to (+Sx/2,+Sy/2,+Sy/2).
| This might cause problems when trying to inegrate the two.
| One possible solution: The user places the simulation box like all other objects according to his own coordinate system. The writing/export functions will automatically reposition things as needed.

IDEAS:

* instaur ".bfdtd.py" extension for geometry creating scripts, so that people use them like .ctl files for MPB/MEEP
* create MPB/MEEP like runner to run those ".bfdtd.py", while taking care of imports and other recurring things
* Use "#PBS"-like prefix/comment in ".bfdtd.py" scripts or other for special things/CLI option replacement
* create extended snapshot classes. Ex: FullBoxSnapshots -> when write is called, it will create snapshots along a specified axis over the whole simulation box.
* accept loss of information once writing to .geo/.inp files (special class info could be added later in comments eventually to allow reading back in written .geo/.inp files)

Note about plane specifications:

* BFDTD indices: 1,2,3 -> _bfdtdidx
* python indices: 0,1,2 -> _pythonidx
* upper letters indices: 'X','Y','Z' -> _upperletteridx
* lower letter indices: 'x','y','z' -> _lowerletteridx
* vectors: [1,0,0], [0,1,0], [0,0,1] -> _upperletteridx

.. todo:: different output options when writing the files, for easier CLI piping/processing. :)
.. todo:: Safety checks on PML layer thickness and object positions
.. todo:: Range check for mode filtered probes
.. todo:: Change comments based on input variables (ex: current source type, etc)
.. todo:: Add documentation/test 2D simulations
.. todo:: Merge unique objects like flag/boundaries/mesh/etc into main BFDTDobject?
.. todo:: Rename setCentro() to setPosition()? or location! (blender style)
.. todo:: Implement location/rotation/parent/modifier systems like in Blender or find similar usable system. Single rotation matrix instead of "rotation lists". Parenting can help deal with more complex rotations.
.. todo:: Check out OpenEMS and other FDTD tools. Create superclass with multiple import/export tools/functions. (again, like blender). We will need our own "super-FDTD format", which has to be extensible so it can include all FDTD tools.
.. todo:: Maybe some "writer classes"? for Ex/Ey/Ez, noGeom/withGeom, transmission, reflection, resonance run, mode volume run, etc?
.. todo:: BFDTDobject comparison operator...
.. todo:: Use property() and decorators.

.. todo:: Add function to easily change basename
.. todo:: Add check for negative values in mesh.
.. todo:: refactor class names with "_", get rid of unused lists or use them
.. todo:: Add check for more than 99/100 snapshots (number only go from 0/1 to 99)
.. todo:: create ref document about .prn files numbering, bfdtd output files, etc

.. todo:: Certain objects (like Flag) are unique anyway. Integrate them directly into BFDTDobject?
'''

import math
import os
import tempfile
import sys
import re

from numpy.linalg import norm
from numpy import array, rad2deg, cross, dot, sqrt, ceil

from photonics.utilities.common import *
import photonics.utilities.brisFDTD_ID_info
from photonics.meshing.meshing import subGridMultiLayer

from photonics.constants.physcon import get_c0, get_e, get_eV, get_epsilon0, get_mu0, get_h, get_h_eVs, get_hb, get_me

from .BFDTDobject import BFDTDobject
from .bristolFDTD_generator_functions import *
from .excitation import *
from .meshobject import MeshObject, MeshingParameters
from .snapshot import TimeSnapshot, ModeFilteredProbe, EpsilonSnapshot, FrequencySnapshot, EpsilonBox, EpsilonBoxFull, SnapshotBoxSurface

#==== CLASSES START ====#

class FDTDdataObject():
  Nx = 1
  Ny = 1
  Nz = 1
  data_epsilon = None
  data_time_snapshots = None
  data_frequency_snapshots = None
  
  def __init__(self):
    return

  def setData(self, x, y, z, field, value):
    print('{} {} {} {} {}', x, y, z, field, value)
    return

#==== CLASSES END ====#

def readBristolFDTD(*filename, **kwargs):
  '''
  Reads one or more .in (=>.inp+.geo), .geo or .inp files and returns a BFDTDobject built from them.
  
  Usage::
  
    sim = readBristolFDTD('foo.geo')
    sim = readBristolFDTD('foo.inp')
    sim = readBristolFDTD('foo.in')
    sim = readBristolFDTD('foo1.geo','foo2.geo','foo3.inp','foo4.in',...)
    L = ['foo1.geo','foo2.geo','foo3.inp','foo4.in']
    sim = readBristolFDTD(*L)
    readBristolFDTD('sim1.in', 'sim2.in', verbosity=9001)
    
  Available keyword arguments:
    verbosity : integer
  '''

  # ugly hack for python2 compatibility (based on http://stackoverflow.com/questions/15301999/python-2-x-default-arguments-with-args-and-kwargs )
  verbosity = 1
  if kwargs.__contains__('verbosity'):
    verbosity = kwargs['verbosity']

  structured_entries = BFDTDobject()
  structured_entries.verbosity = verbosity
  structured_entries.readBristolFDTD(*filename)
  return structured_entries

def truncateGeoList(geo_list, xmin, xmax, ymin, ymax, zmin, zmax):
  new_geo_list = []
  for obj in geo_list:
    if xmin <= obj.location[0] <= xmax and ymin <= obj.location[1] <= ymax and zmin <= obj.location[2] <= zmax:
      new_geo_list.append(obj)
  return new_geo_list

def testWriting():
    '''
    function to test the various functions, might not create working input files, but should create the correct format
    can be used as a template to create new geometries
    '''
    # initialize object
    obj = BFDTDobject()
    # mesh
    obj.mesh.setXmeshDelta([1,2,3])
    obj.mesh.setYmeshDelta([1,2,3])
    obj.mesh.setZmeshDelta([1,2,3])
    # flag
    obj.flag.iterations = 1048000
    # boundary
    obj.boundaries.Xpos_bc = 10
    obj.boundaries.Ypos_bc = 1
    obj.boundaries.Zpos_bc = 10
    obj.boundaries.Xneg_bc = 10
    obj.boundaries.Yneg_bc = 10
    obj.boundaries.Zneg_bc = 10
    obj.boundaries.Xpos_param = [ 8, 2, 1e-3 ]
    obj.boundaries.Ypos_param = [ 1, 1, 0 ]
    obj.boundaries.Zpos_param = [ 8, 2, 1e-3 ]
    obj.boundaries.Xneg_param = [ 8, 2, 1e-3 ]
    obj.boundaries.Yneg_param = [ 8, 2, 1e-3 ]
    obj.boundaries.Zneg_param = [ 8, 2, 1e-3 ]
    # box
    obj.box.lower = [0,0,0]
    obj.box.upper = [10,20,30]

    # write object to example_dir/example.***
    obj.writeAll(tempfile.gettempdir()+os.sep+'example_dir','example')
    
    # more code, unchanged
    with open(tempfile.gettempdir()+os.sep+'tmp.txt', 'w') as FILE:
      delta_X_vector = [11.25,21.25,31.25]
      delta_Y_vector = [12.25,22.25,32.25]
      delta_Z_vector = [13.25,23.25,33.25]
      COMMENT = 'example comment'
      
      #GEOmesh(FILE, COMMENT, delta_X_vector, delta_Y_vector, delta_Z_vector)
      #GEOflag(FILE, COMMENT, 70, 12.34, 24, 42, 1000, 0.755025, '_id_')
      #GEOboundary(FILE, COMMENT, 1.2, [3.4,3.4,3.4],\
                                  #5.6, [7.8,7.8,6.2],\
                                  #9.10, [11.12,1,2],\
                                  #13.14, [15.16,3,4],\
                                  #17.18, [19.20,5,6],\
                                  #21.22, [23.24,7.8,5.4])
      #GEObox(FILE, COMMENT, [1.2,3.4,5.6], [9.8,7.6,5.4])
      excitation_obj = Excitation(COMMENT, 77, [1,2,3], [4,5,6], [7,8,9], [77,88,99], 69, 12.36, 45.54, 78.87, 456, 1, 22, 333, 4444)
      excitation_obj.write_entry(FILE)
      GEOcommand('tmp.bat', 'BASENAME')
      GEOin('tmp.in', ['file','list'])
      GEOshellscript('tmp.sh', 'BASENAME', '/usr/bin/superexe', '/work/todo', 999)

def testCylinderRotation():
  obj = BFDTDobject()
  obj.box.setExtension([0,0,0],[10,10,10])

  A = array([1,2,3])
  B = array([6,5,4])
  u = B-A
  H = norm(B-A)
  C = 0.5*(A+B)

  cyl = Cylinder()
  cyl.setRefractiveIndex(1.52)
  cyl.setInnerRadius(0)
  cyl.setOuterRadius(0.5)

  # method 1
  cyl.setLocation(C)
  cyl.setHeight(H)
  cyl.setAxis(u)

  # method 2
  cyl.setStartEndPoints(A, B)

  #cyl.computeRotationObjects()

  obj.appendGeometryObject(cyl)
  obj.writeGeoFile(tempfile.gettempdir()+os.sep+'cylinder_rotation.geo')
  obj.autoMeshGeometry(1)
  obj.writeAll(tempfile.gettempdir(),'cylinder_rotation')
  return

def testParallelpiped():
  sim=BFDTDobject()
  sim.setVerbosity(2)
  
  u = array([5,6,7])
    
  a = Block()
  a.setLocation(1*u)
  sim.appendGeometryObject(a)

  a = Sphere()
  a.setLocation(2*u)
  sim.appendGeometryObject(a)

  a = Distorted()
  a.setLocation(3*u)
  sim.appendGeometryObject(a)

  a = Cylinder()
  a.setLocation(4*u)
  sim.appendGeometryObject(a)

  a = Parallelepiped()
  a.setLocation(5*u)
  sim.appendGeometryObject(a)

  a = Parallelepiped()
  a.setLocation([5,4,-3])
  a.setDirectionsAndSize([1,1,0],[1,-1,0],[1,2,3],[0.10, 0.20, 0.50])
  sim.appendGeometryObject(a)

  #a = Distorted()
  #a.setLocation(3*u)
  #sim.appendGeometryObject(a)

  a = Distorted()
  a.setLocation([6*u])
  v_list = []
  for i,v in enumerate(a.getVerticesRelative()):
    v_list.append(v/(i+1))
  print(v_list)
  #raise()
  a.setVerticesRelative(v_list)
  #a.setVerticesRelative([ [1/(i+1),1/(i+1),1/(i+1)] for i in range(8)])
  a.setOrigin([12,34,56])
  sim.appendGeometryObject(a)

  sim.writeGeoFile(tempfile.gettempdir()+os.sep+'parallelepiped.geo')
  
if __name__ == "__main__":
  testWriting()
  testCylinderRotation()
  testParallelpiped()
