close all;
clear all;

datafilename = '~/DATA/MPB/topological_defects/spirals/spirals.csv';

klabels = {'A+x+y+z','M+x+y','X+y','M+y+z','A+x+y+z','X+z','Gamma','M+x+y','X+y','Gamma','X+z','M+y+z'};

% set up data_info structure
data_info = mpb_DataInfo_lattice_orthorhombic_simple();

% read in data
mpbdata = read_MPB_CSV(datafilename, 'data_info', data_info, 'klabels', klabels);

plot_MPB(datafilename);
plot_MPB(datafilename, 'data_info', data_info, 'klabels', klabels, 'vline_labels', klabels);

return

%% select data
%selected_k_points = 1:mpbdata.info.Nkpoints;
%selected_bands = 1:mpbdata.info.Nbands;

%% plot selected bands for selected k-points
%figure; hold all;
%for i = selected_bands
  %plot(mpbdata.data.k_index(selected_k_points), mpbdata.data.normalized_frequency(selected_k_points, i));
%end

%% k-point path/positions
%figure;
%plot3(mpbdata.data.k_cartesian_x, mpbdata.data.k_cartesian_y, mpbdata.data.k_cartesian_z);
%xlabel('x'); ylabel('y'); zlabel('z');

%figure;
%scatter3(mpbdata.data.k_cartesian_x, mpbdata.data.k_cartesian_y, mpbdata.data.k_cartesian_z);
%xlabel('x'); ylabel('y'); zlabel('z');

%figure;
%comet3(mpbdata.data.k_cartesian_x, mpbdata.data.k_cartesian_y, mpbdata.data.k_cartesian_z);
%xlabel('x'); ylabel('y'); zlabel('z');

%figure;
%[x,y,z] = sph2cart(mpbdata.data.k_azimuth, mpbdata.data.k_elevation_from_equator, mpbdata.data.k_mag_over_2pi);
%scatter3(x,y,z);
%xlabel('x'); ylabel('y'); zlabel('z');

%%% fn(k_theta, k_phi) in "spherical"
%figure;
%[x,y,z] = sph2cart(mpbdata.data.k_azimuth, mpbdata.data.k_elevation_from_equator, mpbdata.data.normalized_frequency(:,1));
%scatter3(x,y,z);
%xlabel('x'); ylabel('y'); zlabel('z');
%title('fn(k_theta, k_phi) in "spherical"', 'Interpreter', 'none');

% filter out unwanted k-points, based on a given azimuth angle
azimuth_list = [-pi/2, 0, pi/2];
tol = 1e-10;
mpbdata_selection = filterDataByAzimuth(mpbdata, azimuth_list, tol);

%plot_MPB(datafile);

val = pi/2;
field_name = 'k_azimuth';
mpbdata_selection = filterDataByAzimuth(mpbdata, val, tol);
selected_k = getKpointIndicesByValue(mpbdata, field_name, val, tol);

mini = 1;
maxi = 1.2;
selected_k2 = getKpointIndicesByRange(mpbdata, field_name, mini, maxi);

% check k-point selections
selected_k = 1:mpbdata.info.Nkpoints;
figure;
plot3(mpbdata.data.k_cartesian_x(selected_k), mpbdata.data.k_cartesian_y(selected_k), mpbdata.data.k_cartesian_z(selected_k));
xlabel('x'); ylabel('y'); zlabel('z');
title('phi=any');

selected_k = getKpointIndicesByValue(mpbdata, 'k_azimuth', -pi/2, 0);
figure;
scatter3(mpbdata.data.k_cartesian_x(selected_k), mpbdata.data.k_cartesian_y(selected_k), mpbdata.data.k_cartesian_z(selected_k));
xlabel('x'); ylabel('y'); zlabel('z');
title('phi=-pi/2');

selected_k = getKpointIndicesByValue(mpbdata, 'k_azimuth', 0, 0);
figure;
scatter3(mpbdata.data.k_cartesian_x(selected_k), mpbdata.data.k_cartesian_y(selected_k), mpbdata.data.k_cartesian_z(selected_k));
xlabel('x'); ylabel('y'); zlabel('z');
title('phi=0');

selected_k = getKpointIndicesByValue(mpbdata, 'k_azimuth', pi/2, 0);
figure;
scatter3(mpbdata.data.k_cartesian_x(selected_k), mpbdata.data.k_cartesian_y(selected_k), mpbdata.data.k_cartesian_z(selected_k));
xlabel('x'); ylabel('y'); zlabel('z');
title('phi=pi/2');

selected_k = getKpointIndicesByValue(mpbdata, 'k_azimuth', pi/4, 0);
figure;
scatter3(mpbdata.data.k_cartesian_x(selected_k), mpbdata.data.k_cartesian_y(selected_k), mpbdata.data.k_cartesian_z(selected_k));
xlabel('x'); ylabel('y'); zlabel('z');
title('phi=pi/4');

selected_k = getKpointIndicesByValue(mpbdata, 'k_azimuth', 3*pi/8, 0.1);
figure;
scatter3(mpbdata.data.k_cartesian_x(selected_k), mpbdata.data.k_cartesian_y(selected_k), mpbdata.data.k_cartesian_z(selected_k));
xlabel('x'); ylabel('y'); zlabel('z');
title('phi=3*pi/8, tol=0.1');

selected_k = getKpointIndicesByRange(mpbdata, 'k_azimuth', pi/4, pi/2);
figure;
scatter3(mpbdata.data.k_cartesian_x(selected_k), mpbdata.data.k_cartesian_y(selected_k), mpbdata.data.k_cartesian_z(selected_k));
xlabel('x'); ylabel('y'); zlabel('z');
title('phi = pi/4 to pi/2, strict=true');

selected_k = getKpointIndicesByRange(mpbdata, 'k_azimuth', pi/4, pi/2, false);
figure;
scatter3(mpbdata.data.k_cartesian_x(selected_k), mpbdata.data.k_cartesian_y(selected_k), mpbdata.data.k_cartesian_z(selected_k));
xlabel('x'); ylabel('y'); zlabel('z');
title('phi = pi/4 to pi/2, strict=false');

% plot k-points for phi = [-pi/2, 0, pi/2];
selected_k = getKpointIndicesByValue(mpbdata, 'k_azimuth', [-pi/2, 0, pi/2]);
figure;
scatter3(mpbdata.data.k_cartesian_x(selected_k), mpbdata.data.k_cartesian_y(selected_k), mpbdata.data.k_cartesian_z(selected_k));
xlabel('x'); ylabel('y'); zlabel('z');
title('phi = [-pi/2, 0, pi/2]');

% plot fn(theta) for phi = [-pi/2,0,pi/2];
selected_k = getKpointIndicesByValue(mpbdata, 'k_azimuth', [-pi/2, 0, pi/2]);
figure;
x = degrees(mpbdata.data.k_elevation_from_Z(selected_k));
y = mpbdata.data.normalized_frequency(selected_k, :);
hold all;
for n = 1:size(y,2)
  plot(x, y(:, n), 'o');
end
xlabel('\theta (degrees)'); ylabel('a/\lambda');
title('fn(theta) for phi = [-pi/2, 0, pi/2]');

%% plot fn(theta) for phi = [-pi/2,0,pi/2];
[xs, I] = sort(x);
hold all;
for n = 1:size(y,2)
  plot(xs, y(I, n), 'r-');
end

% without for loops:
figure; hold all;
xlabel('\theta (degrees)'); ylabel('a/\lambda');
title('fn(theta) for phi = [-pi/2, 0, pi/2] (no for loops)');
plot(x, y, 'o');
[xs, I] = sort(x);
plot(xs, y(I, :), 'r-');

% fn(theta, phi) in cylindrical coords (z=fn, r=theta, polar angle=phi)
figure;
z     = mpbdata.data.normalized_frequency;
theta = repmat( mpbdata.data.k_azimuth(:),            1, size(z, 2));
rho   = repmat( mpbdata.data.k_elevation_from_Z(:),   1, size(z, 2));
[x,y,z] = pol2cart(theta, rho, z);
scatter3(x,y,z);
title('fn(theta, phi) in cylindrical coords (z=fn, r=theta, polar angle=phi)');
xlabel('x'); ylabel('y'); zlabel('a/lambda');

%i0 = find(and(theta==0, rho==0));
%i1 = find(and(theta==0, rho~=0));
%[r0,c0] = ind2sub(size(z), i0);
%[r1,c1] = ind2sub(size(z), i1);

kx = repmat( mpbdata.data.k_cartesian_x(:), 1, size(z, 2));
ky = repmat( mpbdata.data.k_cartesian_y(:), 1, size(z, 2));
kz = repmat( mpbdata.data.k_cartesian_z(:), 1, size(z, 2));

figure;
hold all;
scatter3(mpbdata.data.k_cartesian_x, mpbdata.data.k_cartesian_y, mpbdata.data.k_cartesian_z); % all
xlabel('x'); ylabel('y'); zlabel('z');
title('all k-points');

figure;
hold all;
plot3(mpbdata.data.k_cartesian_x, mpbdata.data.k_cartesian_y, mpbdata.data.k_cartesian_z); % all
i = find(and(theta==0, rho==0));
scatter3(kx(i), ky(i), kz(i));
xlabel('x'); ylabel('y'); zlabel('z');
title('theta==0, rho==0');

figure;
hold all;
plot3(mpbdata.data.k_cartesian_x, mpbdata.data.k_cartesian_y, mpbdata.data.k_cartesian_z); % all
i = find(and(theta==0, rho~=0));
scatter3(kx(i), ky(i), kz(i));
xlabel('x'); ylabel('y'); zlabel('z');
title('theta==0, rho~=0');

figure;
hold all;
plot3(mpbdata.data.k_cartesian_x, mpbdata.data.k_cartesian_y, mpbdata.data.k_cartesian_z); % all
i = find(rho==0);
scatter3(kx(i), ky(i), kz(i));
xlabel('x'); ylabel('y'); zlabel('z');
title('rho==0');

% do the usual fn(k_index) plot
figure;
hold all;
plot(mpbdata.data.k_index, mpbdata.data.normalized_frequency);
% add labels
for i = 1:length(mpbdata.data.k_index)
  S = char(mpbdata.data.k_label(i));
  if ~isempty(S)
    vline(mpbdata.data.k_index(i), 'r-', S, 270, false);
  end
end

% comparing fn(kx,ky) in cartesian and fn(kphi,ktheta) in cylindrical
z         = mpbdata.data.normalized_frequency;
cyl_theta = repmat( mpbdata.data.k_azimuth(:),          1, size(z, 2));
cyl_rho1  = repmat( mpbdata.data.k_elevation_from_Z(:), 1, size(z, 2));
kx        = repmat( mpbdata.data.k_cartesian_x(:),      1, size(z, 2));
ky        = repmat( mpbdata.data.k_cartesian_y(:),      1, size(z, 2));
kz        = repmat( mpbdata.data.k_cartesian_z(:),      1, size(z, 2));
cyl_rho2  = sqrt(kx.^2 + ky.^2);

figure;
scatter3(kx, ky, z); % all
title('fn(kx,ky)');
xlabel('kx'); ylabel('ky'); zlabel('a/lambda');
view(3);
axis('tight');

figure;
[xx,yy,zz] = pol2cart(cyl_theta, cyl_rho1, z);
scatter3(xx,yy,zz);
title('fn(theta, phi) in cylindrical coords (z=fn, r=theta, polar angle=phi)');
xlabel('x'); ylabel('y'); zlabel('a/lambda');
view(3);
axis('tight');

figure;
[xx,yy,zz] = pol2cart(cyl_theta, cyl_rho2, z);
scatter3(xx,yy,zz);
title('fn(theta, phi) in cylindrical coords (z=fn, r=sqrt(kx^2+ky^2), polar angle=phi)');
xlabel('x'); ylabel('y'); zlabel('a/lambda');
view(3);
axis('tight');

figure;
xx = repmat( mpbdata.data.k_elevation_from_Z(:), 1, size(z, 2));
yy = repmat( mpbdata.data.k_azimuth(:),          1, size(z, 2));
zz = z;
scatter3(xx,yy,zz);
title('fn(theta, phi) in cartesian coords (x=elevation from Z, y=azimuth, z=fn)');
xlabel('theta (rad)'); ylabel('azimuth (rad)'); zlabel('a/lambda');
view(3);
axis('tight');

disp('THE END');
