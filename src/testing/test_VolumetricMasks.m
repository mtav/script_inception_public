close all;
clear all;

x=linspace(-10,10);
y=linspace(-10,10);
z=linspace(-10,10);

[X,Y,Z]=meshgrid(x,y,z);

Xc = mean(getRange(X));
Yc = mean(getRange(Y));
Zc = mean(getRange(Z));

% spheres
centro = [0,0,0];
mask = getVolumetricMaskSphere(X, Y, Z, centro, 5);
figure;
subplot(1,2,1);
plotVolumetricData(X, Y, Z, mask, centro(1), centro(2), centro(3), 'slice');
subplot(1,2,2);
plotVolumetricData(X, Y, Z, mask, centro(1), centro(2), centro(3), 'isosurface');

centro = [5,-5,-10];
mask = getVolumetricMaskSphere(X, Y, Z, centro, 2);
figure;
subplot(1,2,1);
plotVolumetricData(X, Y, Z, mask, centro(1), centro(2), centro(3), 'slice');
subplot(1,2,2);
plotVolumetricData(X, Y, Z, mask, centro(1), centro(2), centro(3), 'isosurface');

centro = [0,0,0];
mask = getVolumetricMaskSphere(X, Y, Z, centro, [5,10,2]);
figure;
subplot(1,2,1);
plotVolumetricData(X, Y, Z, mask, centro(1), centro(2), centro(3), 'slice');
subplot(1,2,2);
plotVolumetricData(X, Y, Z, mask, centro(1), centro(2), centro(3), 'isosurface');

centro = [5,-5,-10];
mask = getVolumetricMaskSphere(X, Y, Z, centro, [7,6,1]);
figure;
subplot(1,2,1);
plotVolumetricData(X, Y, Z, mask, centro(1), centro(2), centro(3), 'slice');
subplot(1,2,2);
plotVolumetricData(X, Y, Z, mask, centro(1), centro(2), centro(3), 'isosurface');

% boxes
centro = [0,0,0];
mask = getVolumetricMaskBox(X, Y, Z, centro, 5);
figure;
subplot(1,2,1);
plotVolumetricData(X, Y, Z, mask, centro(1), centro(2), centro(3), 'slice');
subplot(1,2,2);
plotVolumetricData(X, Y, Z, mask, centro(1), centro(2), centro(3), 'isosurface');

centro = [5,-5,-10];
mask = getVolumetricMaskBox(X, Y, Z, centro, 2);
figure;
subplot(1,2,1);
plotVolumetricData(X, Y, Z, mask, centro(1), centro(2), centro(3), 'slice');
subplot(1,2,2);
plotVolumetricData(X, Y, Z, mask, centro(1), centro(2), centro(3), 'isosurface');

centro = [0,0,0];
mask = getVolumetricMaskBox(X, Y, Z, centro, [5,10,2]);
figure;
subplot(1,2,1);
plotVolumetricData(X, Y, Z, mask, centro(1), centro(2), centro(3), 'slice');
subplot(1,2,2);
plotVolumetricData(X, Y, Z, mask, centro(1), centro(2), centro(3), 'isosurface');

centro = [5,-5,-10];
mask = getVolumetricMaskBox(X, Y, Z, centro, [7,6,1]);
figure;
subplot(1,2,1);
plotVolumetricData(X, Y, Z, mask, centro(1), centro(2), centro(3), 'slice');
subplot(1,2,2);
plotVolumetricData(X, Y, Z, mask, centro(1), centro(2), centro(3), 'isosurface');
