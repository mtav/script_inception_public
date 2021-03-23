#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from photonics.utilities.common import *

# measurement objects

class Probe(object):
  '''
  The format of the probe object is as follows:
  
  1-3)position: Coordinates of the probe position(x,y,z)
  4)step: Samples may be taken at every time step, by setting the parameter “step” equal to 1, or after every n timesteps by setting “step” to the value “n”.
  5-13)E,H,J: Field components to be sampled: E(Ex,Ey,Ez), H(Hx,Hy,Hz), J(Jx,Jy,Jz)
  '''
  def __init__(self,
    position = [0,0,0],
    name = 'probe',
    step = 10,
    E = [1,1,1],
    H = [1,1,1],
    J = [0,0,0],
    power = 0,
    layer = 'probe',
    group = 'probe'):
        
    self.name = name
    self.layer = layer
    self.group = group
    self.position = position
    self.step = step
    self.E = E
    self.H = H
    self.J = J
    self.power = power

    self.useForMeshing = True # set to False to disable use of this object during automeshing

  def setName(self, name):
    self.name = name
    return

  def enableElectricField(self):
    self.E = [1,1,1]
  def disableElectricField(self):
    self.E = [0,0,0]

  def enableMagneticField(self):
    self.H = [1,1,1]
  def disableMagneticField(self):
    self.H = [0,0,0]

  def enableCurrentDensity(self):
    self.J = [1,1,1]
  def disableCurrentDensity(self):
    self.J = [0,0,0]

  def enablePower(self):
    self.power = 1
  def disablePower(self):
    self.power = 0

  def setStep(self, n):
    self.step = int(n)
    return self.step
  def getStep(self):
    return self.step

  # For convenience, since others like box/blocks use it.
  def getCentro(self):
    return self.getPosition()

  def getPosition(self):
    return numpy.array(self.position)

  def setPosition(self, position):
    self.position = numpy.array(position)
    return self.position

  def setLocation(self, loc):
    return self.setPosition(loc)

  def getLocation(self):
    return self.getPosition()
  
  def __str__(self):
    ret  = 'name = '+self.name+'\n'
    ret += 'position = ' + str(self.position) + '\n' +\
    'step = ' + str(self.step) + '\n' +\
    'E = ' + str(self.E) + '\n' +\
    'H = ' + str(self.H) + '\n' +\
    'J = ' + str(self.J) + '\n' +\
    'power = ' + str(self.power)
    return ret
  def read_entry(self,entry):
    if entry.name:
      self.name = entry.name
    self.position = float_array([entry.data[0],entry.data[1],entry.data[2]])
    self.step = int(entry.data[3])
    self.E = float_array([entry.data[4],entry.data[5],entry.data[6]])
    self.H = float_array([entry.data[7],entry.data[8],entry.data[9]])
    self.J = float_array([entry.data[10],entry.data[11],entry.data[12]])
    self.power = float(entry.data[13])
  def write_entry(self, FILE=sys.stdout):
    FILE.write('PROBE **name='+self.name+'\n')
    FILE.write('{\n')
    FILE.write("%E **X\n" % self.position[0])
    FILE.write("%E **Y\n" % self.position[1])
    FILE.write("%E **Z\n" % self.position[2])
    FILE.write("%d **STEP\n" % self.step)
    FILE.write("%d **EX\n" % self.E[0])
    FILE.write("%d **EY\n" % self.E[1])
    FILE.write("%d **EZ\n" % self.E[2])
    FILE.write("%d **HX\n" % self.H[0])
    FILE.write("%d **HY\n" % self.H[1])
    FILE.write("%d **HZ\n" % self.H[2])
    FILE.write("%d **JX\n" % self.J[0])
    FILE.write("%d **JY\n" % self.J[1])
    FILE.write("%d **JZ\n" % self.J[2])
    FILE.write("%d **POW\n" % self.power)
    FILE.write('}\n')
    FILE.write('\n')

  def getMeshingParameters(self,xvec,yvec,zvec,epsx,epsy,epsz):
    objx = numpy.sort([0,self.position[0]])
    objy = numpy.sort([0,self.position[1]])
    objz = numpy.sort([0,self.position[2]])
    eps = 1
    xvec = numpy.vstack([xvec,objx])
    yvec = numpy.vstack([yvec,objy])
    zvec = numpy.vstack([zvec,objz])
    epsx = numpy.vstack([epsx,eps])
    epsy = numpy.vstack([epsy,eps])
    epsz = numpy.vstack([epsz,eps])
    return xvec,yvec,zvec,epsx,epsy,epsz

if __name__ == '__main__':
	pass
