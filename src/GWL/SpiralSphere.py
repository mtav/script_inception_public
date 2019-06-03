#!/usr/bin/env python3
from numpy import pi, arcsin, sin, cos, zeros, isnan
from GWL.GWL_parser import GWLobject

#class SpiralSphereHull(GWLobject):
  #def __init__(self):
    
def test():
  r = 1
  # write one hull of radius r
  write_sequence = []
  for j in range(Nmax):
    phi_rad = phi0 + i*deltaP
    theta_rad = theta0 + i*deltaT
    x = r*sin(theta_rad)*cos(phi_rad)
    y = r*sin(theta_rad)*sin(phi_rad)
    z = r*cos(theta_rad)
    write_sequence.append([x, y, z])
  return(write_sequence)

class SpiralSphere(GWLobject):
  def __init__(self):
    GWLobject.__init__(self)
    self.radius = 1
    self.rstart = 1

    self.thickness = 3
    self.hole_radius = 2.5

    self.ZtoX_radius_ratio = 0.6

    self.deltaR = 0.2
    self.deltaP = 6

    self.phi_start = 0

    self.voxelX = 0.3
    self.overlap = 0.5

    self.deltaR_direction = -1
    self.theta_direction = 1
    
    self.TopHemisphere = True
    
  def setDiametre(self, diametre):
    self.radius = 0.5*diametre
    return
  
  def setRadius(self, radius):
    self.radius = radius
    return

  def getDiametre(self):
    return(2*self.radius)
  
  def getRadius(self):
    return(self.radius)

  def computePoints(self):
    self.clear()
    print('thickness = {}, deltaR = {}'.format(self.thickness, self.deltaR))
    Nhulls = int(self.thickness/self.deltaR)
    #Nhulls = int(self.thickness/self.deltaR) + 1 + 1 # Quick hack. This script needs a lot of improvements.
    print('Nhulls = {}'.format(Nhulls))
    if self.TopHemisphere:
      theta_start = 0 + arcsin(self.hole_radius/self.getRadius())
    else:
      theta_start = pi - arcsin(self.hole_radius/self.getRadius())
    print('theta_start = {}'.format(theta_start))
    deltaX = self.voxelX*(1-self.overlap)
    r = self.rstart
    for i in range(Nhulls):
      phi = self.phi_start
      theta = theta_start
      
      # This formula keeps the distance between "rings" constant and equal to deltaX:
      deltaT = deltaX/r/(360/self.deltaP)
      
      Nmax_float = (pi-arcsin(self.hole_radius/self.rstart))/deltaT+1
      if not isnan(Nmax_float):
        Nmax = int(Nmax_float)

        ###############
        # write one hull of radius r
        write_sequence = []
        for j in range(Nmax):
          x = r*sin(theta)*cos(phi*2*pi/360)
          y = r*sin(theta)*sin(phi*2*pi/360)
          z = r*cos(theta)
          new_z = (z+self.radius)*self.ZtoX_radius_ratio
          write_sequence.append([x, y, new_z])
          phi = phi + self.deltaP
          theta = theta + self.theta_direction*deltaT
        self.GWL_voxels.append(write_sequence)
        ###############

      r = r + self.deltaR_direction*self.deltaR
    
  def writeGWL(self, filename, writingOffset = [0,0,0,0]):
    print('SpiralSphere.writeGWL')
    self.computePoints()
    GWLobject.writeGWL(self, filename, writingOffset)
    return
  
  def getMeshData(self, position = [0,0,0]):
    self.computePoints()
    return(GWLobject.getMeshData(self, position))

def main():
  DESTDIR='/tmp/huhu/'
  outfile1 = DESTDIR + 'outfile1.python3.gwl'
  outfile2 = DESTDIR + 'outfile2.python3.gwl'
  outfile3 = DESTDIR + 'outfile3.python3.gwl'
  outfile4 = DESTDIR + 'outfile4.python3.gwl'

  lol = SpiralSphere()
  lol.writeGWL(outfile1)
  return
  lol.setDiametre(10)
  lol.thickness = 3
  lol.ZtoX_radius_ratio = 0.6
  lol.deltaR = 0.2
  lol.deltaP = 6
  lol.phi_start = 0
  lol.voxelX = 0.3
  lol.overlap = 0.5

  for IPX in [True, False]:
    if IPX:
      lol.rstart = lol.getRadius()
      lol.hole_radius = 2.5
      lol.deltaR_direction = -1
      lol.theta_direction = 1
      lol.writeGWL(outfile1)
      
      #writeIt2(r0,       int(t/deltaR),    0+arcsin(hole/r0), -1, hole,  1)
      #writeIt2(r0 - t,   int(t/deltaR+1),  pi/2,               1, 0,     1)
    else:
      #writeIt2(r0,       int(t/deltaR),    pi,                -1, 0,    -1)
      #writeIt2(r0,       int(t/deltaR),    pi/2,              -1, hole, -1)
      pass

if __name__ == "__main__":
  test()
  #main()
