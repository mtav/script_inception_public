close all;
clear all;

m = 5;
N = 101;
x = linspace(-m,m,N);
y = linspace(-m,m,N);
z = linspace(-m,m,N);
[X,Y,Z] = meshgrid(x,y,z);
R2 = X.^2 + Y.^2 + Z.^2;
E2 = exp(-R2);
E = sqrt(E2);

eps = ones(size(R2));
eps(find(abs(R2)>1)) = 10;

epsE2 = eps.*E2;

Nx=length(x)
Ny=length(y)
Nz=length(z)

xc_idx = round(Nx/2)
yc_idx = round(Ny/2)
zc_idx = round(Nz/2)

subplot(4,1,1);
plot(squeeze(X(yc_idx,:,zc_idx)), squeeze(E(yc_idx,:,zc_idx)));
title('E');
subplot(4,1,2);
plot(squeeze(X(yc_idx,:,zc_idx)), squeeze(E2(yc_idx,:,zc_idx)));
title('E^2');
subplot(4,1,3);
plot(squeeze(X(yc_idx,:,zc_idx)), squeeze(eps(yc_idx,:,zc_idx)));
title('eps');
subplot(4,1,4);
plot(squeeze(X(yc_idx,:,zc_idx)), squeeze(epsE2(yc_idx,:,zc_idx)));
title('eps*E^2');

figure;
surf(squeeze(X(:,:,zc_idx)), squeeze(Y(:,:,zc_idx)), squeeze(E(:,:,zc_idx)));
title('E');
view(2);
shading interp;
axis tight;
axis square;
colorbar;

figure;
surf(squeeze(X(:,:,zc_idx)), squeeze(Y(:,:,zc_idx)), squeeze(E2(:,:,zc_idx)));
title('E^2');
view(2);
shading interp;
axis tight;
axis square;
colorbar;

figure;
surf(squeeze(X(:,:,zc_idx)), squeeze(Y(:,:,zc_idx)), squeeze(eps(:,:,zc_idx)));
title('eps');
view(2);
shading interp;
axis tight;
axis square;
colorbar;

figure;
surf(squeeze(X(:,:,zc_idx)), squeeze(Y(:,:,zc_idx)), squeeze(epsE2(:,:,zc_idx)));
title('eps*E^2');
view(2);
shading interp;
axis tight;
axis square;
colorbar;

plotSnapshot('z51_id_01.prn', 'column',3);
plotSnapshot('zay_id_00_energy.prn','column', 3);

dx = diff(x);
dy = diff(y);
dz = diff(z);

dx = [(x(2) - x(1))/2, (x(3:end) - x(1:end-2))/2, (x(end) - x(end-1))/2];
dy = [(y(2) - y(1))/2, (y(3:end) - y(1:end-2))/2, (y(end) - y(end-1))/2];
dz = [(z(2) - z(1))/2, (z(3:end) - z(1:end-2))/2, (z(end) - z(end-1))/2];

[dX,dY,dZ] = meshgrid(dx,dy,dz);

dV = dX .* dY .* dZ;
E2V = E2 .* dV;
energy = epsE2 .* dV;

total_E2V = sum(E2V(:))
total_energy = sum(energy(:))

disp('==> conventional mode volume');
[max_val, max_idx] = max(epsE2(:))
epsAtMax = eps(max_idx)
XAtMax = X(max_idx) + m
YAtMax = Y(max_idx) + m
ZAtMax = Z(max_idx) + m
Veff0 = total_energy ./ epsE2(max_idx)

disp('==> low-index cavity mode volume');
[max_val, max_idx] = max(E2(:))
epsAtMax = eps(max_idx)
XAtMax = X(max_idx) + m
YAtMax = Y(max_idx) + m
ZAtMax = Z(max_idx) + m
Veff1 = total_energy ./ ( eps(max_idx) .* E2(max_idx) )

% reference output
%>> calculateModeVolume_test
%Nx =  200
%Ny =  200
%Nz =  200
%total_E2V =  5.5683
%total_energy =  33.928
%==> conventional mode volume
%max_val =  3.6144
%max_idx =  3698699
%epsAtMax =  10
%Veff0 =  9.3867
%==> low-index cavity mode volume
%max_val =  0.99245
%max_idx =  3979900
%epsAtMax =  1
%Veff1 =  34.186

%>> calculateModeVolume_test
%Nx =  100
%Ny =  100
%Nz =  100
%total_E2V =  5.5683
%total_energy =  35.032
%==> conventional mode volume
%max_val =  3.6418
%max_idx =  484855
%epsAtMax =  10
%Veff0 =  9.6193
%==> low-index cavity mode volume
%max_val =  0.96985
%max_idx =  494950
%epsAtMax =  1
%Veff1 =  36.121

%>> calculateModeVolume_test
%Nx =  101
%Ny =  101
%Nz =  101
%xc_idx =  51
%yc_idx =  51
%zc_idx =  51
%total_E2V =  5.5683
%total_energy =  34.810
%==> conventional mode volume
%max_val =  3.6788
%max_idx =  484552
%epsAtMax =  10
%Veff0 =  9.4624
%==> low-index cavity mode volume
%max_val =  1
%max_idx =  515151
%epsAtMax =  1
%Veff1 =  34.810

%>> calculateModeVolume_test
%Nx =  101
%Ny =  101
%Nz =  101
%xc_idx =  51
%yc_idx =  51
%zc_idx =  51
%total_E2V =  5.5683
%total_energy =  34.810
%==> conventional mode volume
%max_val =  3.6788
%max_idx =  484552
%epsAtMax =  10
%XAtMax = 0
%YAtMax =  0.80000
%ZAtMax = -0.60000
%Veff0 =  9.4624
%==> low-index cavity mode volume
%max_val =  1
%max_idx =  515151
%epsAtMax =  1
%XAtMax = 0
%YAtMax = 0
%ZAtMax = 0
%Veff1 =  34.810

%>> calculateModeVolume_test
%Nx =  101
%Ny =  101
%Nz =  101
%xc_idx =  51
%yc_idx =  51
%zc_idx =  51
%total_E2V =  5.5683
%total_energy =  34.382
%==> conventional mode volume
%max_val =  3.6788
%max_idx =  433549
%epsAtMax =  10
%XAtMax =  5
%YAtMax =  5.6000
%ZAtMax =  4.2000
%Veff0 =  9.3459
%==> low-index cavity mode volume
%max_val =  1
%max_idx =  515151
%epsAtMax =  1
%XAtMax =  5
%YAtMax =  5
%ZAtMax =  5
%Veff1 =  34.382

%>> sqrt(pi)^3
%ans =  5.5683
