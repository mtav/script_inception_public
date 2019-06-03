mag = 30000
%dwell = 5000;
dwell = 30000;%1.5*12*2400
%radius_mum = 0.5*1e-3*860.9;
%radius_mum = 0.5*1e-3*1662.5;
radius_mum = 0.5*1e-3*1286.5;
Ntop = 10
Nbottom = 20
size_x_mum = 2*0.066
%size_y_mum = 0.200
size_y_mum = 0.5
rep = 2

% customconfig info:
%          holeType_left = customconfig(1);
%          holeType_center = customconfig(2);
%          holeType_right = customconfig(3);
%          left = customconfig(4);
%          center = customconfig(5);
%          right = customconfig(6);


%DSTDIR='~/FIBstreamfiles/1286.5_separatefiles'
DSTDIR='~/FIBstreamfiles/2012-05-23-b'

% Note: beamCurrent argument still unused

%beamCurrent = 4
%a = holes_test([DSTDIR,filesep,'loncar'],'loncar',mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep,customconfig);
%a = holes_test([DSTDIR,filesep,'DFBrectSpiral'],'DFBrectSpiral',mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep,customconfig);
%a = holes_test([DSTDIR,filesep,'DFBrectRaster'],'DFBrectRaster',mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep,customconfig);
%a = holes_test([DSTDIR,filesep,'DFBtriangle'],'DFBtriangle',mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep,customconfig);
%dwell = 30000;%12*2400

beamCurrent = 11
%a = holes_test([DSTDIR,filesep,'loncar'],'loncar',mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep,customconfig);
%a = holes_test([DSTDIR,filesep,'all'],'custom',mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep,[1,0,1,1,0,1]);

%a = holes_test([DSTDIR,filesep,'bottom'],'custom',mag,dwell,beamCurrent,radius_mum,0,Nbottom,size_x_mum,size_y_mum,rep,[1,0,1,1,0,1]);
%a = holes_test([DSTDIR,filesep,'top'],'custom',mag,dwell,beamCurrent,radius_mum,Ntop,0,size_x_mum,size_y_mum,rep,[1,0,1,1,0,1]);

a = holes_test([DSTDIR,filesep,'left'],'custom',mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep,[1,0,1,1,0,0]);
a = holes_test([DSTDIR,filesep,'right'],'custom',mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep,[1,0,1,0,0,1]);

%a = holes_test([DSTDIR,filesep,'bottom_left'],'custom',mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep,[1,0,1,1,0,1]);
%a = holes_test([DSTDIR,filesep,'bottom_right'],'custom',mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep,[1,0,1,1,0,1]);

%a = holes_test([DSTDIR,filesep,'top_left'],'custom',mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep,[1,0,1,1,0,1]);
%a = holes_test([DSTDIR,filesep,'top_right'],'custom',mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep,[1,0,1,1,0,1]);

%a = holes_test([DSTDIR,filesep,'single'],'custom',mag,dwell,beamCurrent,radius_mum,0,1,size_x_mum,size_y_mum,rep,[1,0,1,1,0,1]);
%a = holes_test([DSTDIR,filesep,'single_left'],'custom',mag,dwell,beamCurrent,radius_mum,0,1,size_x_mum,size_y_mum,rep,[1,0,1,1,0,0]);
%a = holes_test([DSTDIR,filesep,'single_right'],'custom',mag,dwell,beamCurrent,radius_mum,0,1,size_x_mum,size_y_mum,rep,[1,0,1,0,0,1]);

%a = holes_test([DSTDIR,filesep,'DFBrectSpiral'],'DFBrectSpiral',mag,dwell,beamCurrent,radius_mum,0,Nbottom,size_x_mum,size_y_mum,rep,customconfig);
%a = holes_test([DSTDIR,filesep,'DFBrectSpiral'],'DFBrectSpiral',mag,dwell,beamCurrent,radius_mum,Ntop,0,size_x_mum,size_y_mum,rep,customconfig);
%a = holes_test([DSTDIR,filesep,'DFBrectRaster'],'DFBrectRaster',mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep,customconfig);
%a = holes_test([DSTDIR,filesep,'DFBtriangle'],'DFBtriangle',mag,dwell,beamCurrent,radius_mum,Ntop,Nbottom,size_x_mum,size_y_mum,rep,customconfig);

close all; clear all;
mag = 30000
beamCurrent = 11
dwell = 30000;%1.5*12*2400
rep = 2

[res, HFW] = getResolution(mag)
fileBaseName = '/tmp/test'
holes_Type=0:6
N = length(holes_Type)
holes_X=linspace(-HFW/4, HFW/4, N)
holes_Y=zeros(1,N)
dx = (holes_X(2) - holes_X(1))/2
holes_Size_X = dx*ones(size(holes_Type))
holes_Size_Y = dx*ones(size(holes_Type))
separate_files=false
a = holes(fileBaseName,mag,dwell,rep,holes_X,holes_Y,holes_Size_X,holes_Size_Y,holes_Type,separate_files,beamCurrent)
readStrFile(a);
vline(2048); hline(2060);

vline(round(holes_X/res)+2048);
axis equal
%  saveas_fig_and_png(gcf, [fileBaseName, '.png']); % takes too long for some reason.... Too many points? :/

% TODO: figure out why file is incomplete (missing bottom holes) (too many points when central cylinders added?)

Ntop = 10
Nbottom = 20
radius_mum=1
size_x_mum = 2*0.066
size_y_mum = 0.5
a = holes_test(fileBaseName,'custom', mag, dwell, beamCurrent, radius_mum, Ntop, Nbottom, size_x_mum, size_y_mum, rep, [1,0,1,1,1,1]);
readStrFile(a);

vline(2048); hline(2060);
hline(  round(radius_mum/res) + 2060, 'r-')
hline( -round(radius_mum/res) + 2060, 'r-')

hline( round( (radius_mum - size_y_mum/2) /res) + 2060, 'r--')
hline( round( (-radius_mum - size_y_mum/2) /res) + 2060, 'r--')
