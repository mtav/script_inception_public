Overview of FIB related code:
=============================

./multiRing.m:function filename_cellarray = multiRing(folder,mag,prefix,direction,interRingDistancePxl)
./holeSpiralErman_single_ring.m:function holeSpiralErman_single_ring(folder,rep,mag,r_inner,r_outer)
./multiLine.m:function filename_cellarray = multiLine(folder,mag,prefix,direction,interRingDistancePxl)
./multiRingPrototype.m:function multiRingPrototype(folder,rep,mag,prefix,direction,interRingDistancePxl)
./annularProfiler.m:function annularProfiler(folder,rep,mag,r_inner_mum,r_outer_mum,prefix,direction,profile_type,profile,interRingDistancePxl)
./yagiStream.m:function filename_cellarray = yagiStream(folder,prefix)
./surfMask.m:function surfMask(x,y,dwell,beamStep)
./holeCocentricErman_single_dome.m:function holeCocentricErman_single_dome(folder,rep,mag,r_inner,r_outer,minDwell)

./DFBstructures/holes_test.m:function filename_cellarray_all = holes_test(fileBaseName,type,mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep,customconfig)
./DFBstructures/holes.m:function filename_cellarray = holes(fileBaseName,mag,dwell,rep,holes_X,holes_Y,holes_Size_X,holes_Size_Y,holes_Type,separate_files,beamCurrent)

./spiral_holes/ShiftMask.m:function [M]=ShiftMask(res,shiftX,shiftY,newDwell,newRep,pathName,fileName,writeFile)

./FIB_commons/triangleHoleLeft.m:function [dwell_vector,X,Y] = triangleHoleLeft(beamCurrent,res,dwell,x_center,y_center,x_size,y_size)
./FIB_commons/triangleHoleRight.m:function [dwell_vector,X,Y] = triangleHoleRight(beamCurrent,res,dwell,x_center,y_center,x_size,y_size)
./FIB_commons/ZigZagHoleRectangular.m:function [dwell_vector,X,Y] = ZigZagHoleRectangular(beamCurrent,res,dwell,x_center,y_center,x_size,y_size)
./FIB_commons/triangleHoleUp.m:function [dwell_vector,X,Y] = triangleHoleUp(beamCurrent,res,dwell,x_center,y_center,x_size,y_size)
./FIB_commons/triangleHoleDown.m:function [dwell_vector,X,Y] = triangleHoleDown(beamCurrent,res,dwell,x_center,y_center,x_size,y_size)
./FIB_commons/spiralHoleCircular.m:function [dwell_vector,X,Y] = spiralHoleCircular(beamCurrent,res,dwell,x_center,y_center,x_size,y_size)
./FIB_commons/spiralHoleRectangular.m:function [dwell_vector,X,Y] = spiralHoleRectangular(beamCurrent,res,dwell,x_center,y_center,x_size,y_size)

./FIB_utilities/getResolution.m:function [res, HFW] = getResolution(mag)
./FIB_utilities/readStrFile.m:function [x,y,dwell,rep,numPoints] = readStrFile(filename_cellarray, magnitude)

Non-function scripts:
=====================
./holeSpiralErman.m
./DFBstructures/holes_test_wrapper.m
./spiral_holes/holeSpiralErman.m
./grating_v1.m

