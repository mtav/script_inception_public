% This script creates a figure similar to fig 7.2-7 in fundamentals of photonics by Saleh.

close all; clear all;

system('./DBR-TE-TM.sh');

omega_bragg_normalized = 0.2;
n1 = 1.5;
n2 = 3.5;
d1 = 0.5;
d2 = 0.5;
a = d1+d2;
n_average = (n1*d1+n2*d2)/a;
angle_brewster_rad = atan(n2/n1);
angle_brewster_deg = degrees(angle_brewster_rad);

% reciprocal lattice vector b1
b1 = [1/0.25,0,0];

kfunc = @(x,y,z) norm(b1)*x;
myPlotter = @(f) plot_MPB(f, 'ylim',[0,2.5], 'y_axis_scale_factor', 1/omega_bragg_normalized, 'grid', true, 'new_figure', false, 'linespec', 'o', 'kfunc', kfunc);

kfunc_rev = @(x,y,z) -norm(b1)*x;
myPlotter_rev = @(f) plot_MPB(f, 'ylim',[0,2.5], 'y_axis_scale_factor', 1/omega_bragg_normalized, 'grid', true, 'new_figure', false, 'linespec', 'o', 'kfunc', kfunc_rev);

kfunc1 = @(x,y,z) x;
myPlotter1 = @(f) plot_MPB(f, 'ylim',[0,2.5], 'y_axis_scale_factor', 1/omega_bragg_normalized, 'grid', true, 'new_figure', false, 'linespec', 'o-', 'kfunc', kfunc1, 'bands', 1:2:6);
kfunc2 = @(x,y,z) -x+1;
myPlotter2 = @(f) plot_MPB(f, 'ylim',[0,2.5], 'y_axis_scale_factor', 1/omega_bragg_normalized, 'grid', true, 'new_figure', false, 'linespec', 'o-', 'kfunc', kfunc2, 'bands', 2:2:6);

figure();
subplot(1, 2, 1);
ret_te = myPlotter_rev('DBR-TE-TM.te?=true.csv');
xlabel('kx');
ylabel('\omega/\omega_{Bragg}');
title('TM polarization (run-te in MPB)');
%  ret_te = myPlotter1('DBR-TE-TM.te?=true.csv');
%  ret_te = myPlotter2('DBR-TE-TM.te?=true.csv');
subplot(1, 2, 2);
ret_tm = myPlotter('DBR-TE-TM.te?=false.csv');
xlabel('kx');
ylabel('\omega/\omega_{Bragg}');
title('TE polarization (run-tm in MPB)');
%  ret_tm = myPlotter1('DBR-TE-TM.te?=false.csv');
%  ret_tm = myPlotter2('DBR-TE-TM.te?=false.csv');

for angle_deg = [20,40,60,90]
  subplot(1, 2, 1);
  kxn = linspace(-1, 0);
  y = omega_fixed_angle(radians(angle_deg), kxn, n1, n_average);
  plot(kxn, y, 'b-');

  subplot(1, 2, 2);
  kxn = linspace(0, 1);
  y = omega_fixed_angle(radians(angle_deg), kxn, n1, n_average);
  plot(kxn, y, 'b-');
end

subplot(1, 2, 1);
kxn = linspace(-1, 0);
y = omega_fixed_angle(angle_brewster_rad, kxn, n1, n_average);
plot(kxn, y, 'r-');

saveas(gcf, 'DBR_TE_TM_projected_bands.png');

%  figure();
%  subplot(1, 5, 1);
%  myPlotter('DBR-TE-TM.kx=0.csv');
%  subplot(1, 5, 2);
%  myPlotter('DBR-TE-TM.kx=0.125.csv');
%  subplot(1, 5, 3);
%  myPlotter('DBR-TE-TM.kx=0.25.csv');
%  subplot(1, 5, 4);
%  myPlotter('DBR-TE-TM.kx=0.375.csv');
%  subplot(1, 5, 5);
%  myPlotter('DBR-TE-TM.kx=0.5.csv');
