#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from GWL.woodpile import *

from GWL.box import *

from GWL.GWL_parser import GWLobject


def createWoodpile(DSTDIR, VerticalPeriod, w_factor, box_size_X, box_size_Y, n_layers, laser_power_at_z0, K, interfaceAt, rotationAngleDegrees = 0, filename=None):

  d_value = VerticalPeriod/numpy.sqrt(2) # Distance between two adjacent logs

##  box_size = 50
  #box_size = 50

  n_logs_X = int(box_size_X/d_value) # number of logs in each layer
  print(n_logs_X)
  n_logs_Y = int(box_size_Y/d_value) # number of logs in each layer
  print(n_logs_Y)

  w = w_factor*VerticalPeriod # width of the logs
  h = 0.25*VerticalPeriod # heigth of logs (should be 1/4 for fcc to not overlap)
  print('w = '+str(w))
  print('h = '+str(h))

  #L = (n_logs-1)*d_value+w+d_value # Length of logs (should > (n_logs-1)*d_value+w)
  #n_layers = 4*4 # Number of layers of logs required

  wall_thickness = 0
  XL = 0.5*wall_thickness # Lower edge of the simulation domain in x direction.
  YL = 0.5*wall_thickness # Lower edge of the simulation domain in y direction.
  ZL = 0 # Lower edge of the simulation domain in z direction.

  XU = XL + box_size_X # Upper edge of the simulation domain in x direction.
  YU = YL + box_size_Y # Upper edge of the simulation domain in y direction.
  ZU = 4 # Upper edge of the simulation domain in z direction.

  Nlayers_Z = n_layers
  NRodsPerLayer_X = n_logs_X
  NRodsPerLayer_Y = n_logs_Y

  woodpile_Zoffset = 0.5*h
  wall_height = n_layers*h

  leg_width = 5

  BottomToTop = False

  woodpile_obj = Woodpile()
  woodpile_obj.BottomToTop = 1
  print('Nlayers_Z='+str(Nlayers_Z))
  woodpile_obj.Nlayers_Z = Nlayers_Z
  woodpile_obj.NRodsPerLayer_X = NRodsPerLayer_X
  woodpile_obj.NRodsPerLayer_Y = NRodsPerLayer_Y
  woodpile_obj.interRodDistance = d_value
  woodpile_obj.interLayerDistance = h

  # new overlap handling function
  voxel_width = 0.150 # in mum
  voxel_height = 0.300 # in mum

  (woodpile_obj.LineNumber_X, woodpile_obj.LineDistance_X) = calculateNvoxelsAndInterVoxelDistance(Length=w,Voxelsize=voxel_width,Overlap=0.5)
  (woodpile_obj.LineNumber_Y, woodpile_obj.LineDistance_Y) = calculateNvoxelsAndInterVoxelDistance(Length=w,Voxelsize=voxel_width,Overlap=0.5)
  (woodpile_obj.LineNumber_Z, woodpile_obj.LineDistance_Z) = calculateNvoxelsAndInterVoxelDistance(Length=h,Voxelsize=voxel_height,Overlap=0.99)

  woodpile_obj.LineDistance_X = 0.067
  woodpile_obj.LineDistance_Y = 0.067
  woodpile_obj.LineDistance_Z = 0.067

  # change this manually to set number of lines
  woodpile_obj.LineNumber_X = 2
  woodpile_obj.LineNumber_Y = 4
  woodpile_obj.LineNumber_Z = 4

  #woodpile_obj.LineNumber_X = 1
  #woodpile_obj.LineNumber_Y = 1
  #woodpile_obj.LineNumber_Z = 1

  woodpile_obj.initialDirection = 0

  woodpile_obj.initialLayerType_X = 0
  woodpile_obj.initialLayerType_Y = 0

  woodpile_obj.Xmin = XL
  woodpile_obj.Xmax = XU
  woodpile_obj.Ymin = YL
  woodpile_obj.Ymax = YU

#  woodpile_obj.Xoffset = 0.5*(w + woodpile_obj.interRodDistance)
#  woodpile_obj.Yoffset = 0.5*(w + woodpile_obj.interRodDistance)

  woodpile_obj.isSymmetrical = True
  woodpile_obj.adaptXYMinMax()



  if filename is None:
    subfilename = 'woodpile.a_%.3f.w_factor_%.3f.size_%.fx%.f.layer_%.f.gwl'% (VerticalPeriod,w_factor,box_size_X,box_size_Y,n_layers)
    filename = DSTDIR + os.path.sep + subfilename
  
  (GWL_obj, tmp) = woodpile_obj.getGWLandBFDTDobjects()

  GWL_obj.rotate([0,0,0], [0,0,1], rotationAngleDegrees)
  
  GWL_obj.addPowerCompensation(laser_power_at_z0, K, interfaceAt);
  GWL_obj.writeGWL(filename, writingOffset = [0,0,woodpile_Zoffset,0] )

##def createWoodpileGroup(DSTDIR):
##    wa_list = []
##
##    ##nlog_1-nouter_1.52/band.out.dat
##    #a=0.9759; w=0.2*a
##    #wa_list.append((w,a))
##
##    ##nlog_1-nouter_2.1/band.out.dat
##    #a=0.7342; w=0.2*a
##    #wa_list.append((w,a))
##
##    ##nlog_1-nouter_2.4/band.out.dat
##    #a=0.65035; w=0.2*a
##    #wa_list.append((w,a))
##
##    ##nlog_2.1-nouter_1.52/band.out.dat
##    #a=0.78831; w=0.2*a
##    #wa_list.append((w,a))
##
##    ##nlog_2.4-nouter_1.52/band.out.dat
##    #a=0.73662; w=0.2*a
##    #wa_list.append((w,a))
##
##    ##nlog_1.52-nouter_2.1/band.out.dat
##    #a=0.69664; w=0.2*a
##    #wa_list.append((w,a))
##
##    ##nlog_1.52-nouter_2.4/band.out.dat
##    #a=0.6213; w=0.2*a
##    #wa_list.append((w,a))
##
##    #nlog_1.52-nouter_1/band.out.dat
##    a=1.1421; w_factor=0.2
##    wa_list.append((w_factor,a))
##
##    #nlog_2.1-nouter_1/band.out.dat
##    a=0.95138; w_factor=1/numpy.sqrt(2)-0.2
##    wa_list.append((w_factor,a))
##
##    #nlog_2.4-nouter_1/band.out.dat
##    a=0.87318; w_factor=1/numpy.sqrt(2)-0.2
##    wa_list.append((w_factor,a))
##
##    for (w_factor,a) in wa_list:
##      createWoodpile(DSTDIR,a,w_factor)

def main():
  if len(sys.argv)>1:
    DSTDIR = sys.argv[1]
  else:
    DSTDIR = os.getcwd()

  #createWoodpileGroup(DSTDIR)
  #print( 'Output in ' + os.getcwd())

  VerticalPeriod = 1.277;
  w_factor = 0.31;
  box_size_X = 50;
  box_size_Y = box_size_X;
  n_layers = 10*2;

  K=0.015;
  interfaceAt=1;
  #for laser_power_at_z0 in [25,26,27,28]:
    #for rotatedBy90degrees in [True, False]:
      #createWoodpile(DSTDIR, VerticalPeriod, w_factor, box_size_X, box_size_Y, n_layers, laser_power_at_z0, K, interfaceAt, rotatedBy90degrees=rotatedBy90degrees, filename='K{:.3f}_woodpile.a_{:.3f}.w_factor_{:.3f}.size_{}.layer_{}_P{}.rotated_{}.gwl'.format(K, VerticalPeriod, w_factor, box_size_X, n_layers, laser_power_at_z0, rotatedBy90degrees));

  #rotatedBy90degrees=True
  #for laser_power_at_z0 in [25,26,27,28]:
    #createWoodpile(DSTDIR, VerticalPeriod, w_factor, box_size_X, box_size_Y, n_layers, laser_power_at_z0, K, interfaceAt, rotatedBy90degrees=rotatedBy90degrees, filename='K{:.3f}_woodpile.a_{:.3f}.w_factor_{:.3f}.size_{}.layer_{}_P{}.rotated_{}.4lines.gwl'.format(K, VerticalPeriod, w_factor, box_size_X, n_layers, laser_power_at_z0, rotatedBy90degrees));

  #rotatedBy90degrees=True
  #laser_power_at_z0=25
  #filename='test.gwl'
  #createWoodpile(DSTDIR, VerticalPeriod, w_factor, box_size_X, box_size_Y, n_layers, laser_power_at_z0, K, interfaceAt, rotatedBy90degrees=rotatedBy90degrees, filename=filename);

  #for n_layers in [8,10,12,16]:
    #for laser_power_at_z0 in [25,26,27,28]:
  for n_layers in [16]:
    for laser_power_at_z0 in [27]:
      for alpha in numpy.linspace(0,45,10):
        filename='K{:.3f}_woodpile.a_{:.3f}.w_factor_{:.3f}.size_{}.layer_{}_P{}.alpha_{}.4line.gwl'.format(K, VerticalPeriod, w_factor, box_size_X, n_layers, laser_power_at_z0, alpha)
        createWoodpile(DSTDIR, VerticalPeriod, w_factor, box_size_X, box_size_Y, n_layers, laser_power_at_z0, K, interfaceAt, rotationAngleDegrees=alpha, filename=filename);

##  leg_box_size=20
##  leg_height=4*VerticalPeriod+1
##
##  legfilename = 'legs.size_%.f.height_%.3f.gwl'% (leg_box_size,leg_height)
##  createLegs(DSTDIR,NAME=legfilename,box_size=leg_box_size,leg_height=leg_height,hole_width=2,wall_thickness=1,overshoot=2.5,writingOffset=[0,0,0,0])


if __name__ == "__main__":
  main()
