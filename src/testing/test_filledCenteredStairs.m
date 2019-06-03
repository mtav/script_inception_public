close all;
clear all;

xmin = -2*pi;
xmax = 2*pi;

x = linspace(xmin, xmax, 100);
y = cos(x);

color = [1,0,0];
threshold = 0;

figure; hold on;
plot(x,y,'b-o');
hline(threshold, 'k--');
filledCenteredStairsWithThreshold(x, y, threshold, color);

ymin = min(y(:));
ymax = max(y(:));

xlim([xmin, xmax]);
ylim([ymin, ymax]);

basevalue = ymin;

xx = x;
yy = 2*( y < 0 ) - 1;

figure; hold on;
plot(x, y, 'b-o');
plot(xx,yy, 'k-s');
filledCenteredStairs(xx, yy, basevalue, color, xmin, xmax);
%filledCenteredStairs([-pi,0,pi], [0,1,0], basevalue, color, -5, 5);

figure; hold on;
plot(x, y, 'b-o');
plot(xx,yy, 'k-s');
filledCenteredStairs(xx, yy, -2, color, -4, 4);
%filledCenteredStairs([-pi,0,pi], [0,1,0], basevalue, color, -5, 5);

x = linspace(-10, 10, 10);
y = rand(10,1);
threshold = rand(1,1);
figure; hold on;
plot(x,y,'b-o');
hline(threshold, 'k--');
filledCenteredStairsWithThreshold(x, y, threshold, color);

% test with FDTD data
WORKDIR='~/TEST/MV_LowIndexCavities/low_index/';
cd(WORKDIR);
ret = BFDTD_loadVolumetricData('mesh_file', 'sim.in');
ret = calculateModeVolume2(ret);
%calculateModeVolume_plotMaxDebug(ret.MV.info_full.MaximumEmod2, ret, 'ret.MV.info_full.MaximumEmod2');

max_info = ret.MV.info_full.MaximumEmod2;

x=squeeze(ret.data.Z(max_info.y_index, max_info.x_index, :));
y1=squeeze(ret.data.EnergyDensity(max_info.y_index, max_info.x_index, :));
y2=squeeze(ret.data.D(max_info.y_index, max_info.x_index, :, 1));

figure; hold on;
subplot(3,1,1);
plot(x, y1);
subplot(3,1,2);
plot(x, y2);
subplot(3,1,3);
plot(x, y1); hold on; filledCenteredStairsWithThreshold(x, y2, 1, color);
