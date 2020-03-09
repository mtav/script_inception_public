function plot_custom(n1, n2, d1, d2)
  % This script creates a figure similar to fig 7.2-7 in fundamentals of photonics by Saleh.

  %close all; clear all;
  
  if exist('n1','var')==0
    n1 = 1.5;
  end
  if exist('n2','var')==0
    n2 = 3.5;
  end
  if exist('d1','var')==0
    d1 = 0.5;
  end
  if exist('d2','var')==0
    d2 = 0.5;
  end
  
  a = d1+d2;
  n_average = (n1*d1+n2*d2)/a;
  omega_bragg_normalized = 1./(2*n_average); % 0.2
  angle_brewster_rad = atan(n2/n1);
  angle_brewster_deg = degrees(angle_brewster_rad);

  %cmd = ['./DBR-TE-TM.sh ', num2str(n1), ' ', num2str(n2), ' ', num2str(d1),' ',  num2str(d2)]
  cd(fileparts(which(mfilename)));
  cmd = sprintf('./DBR-TE-TM.sh %.2f %.2f %.2f %.2f', n1, n2, d1, d2);
  disp(cmd);

  system(cmd);

  % reciprocal lattice vector b1
  b1 = [1/0.25,0,0];

  %kfunc = @(x,y,z) norm(b1)*x;
  xzfunc = @(data, pos, data_info) mpb_xzfunc_custom(data, pos, data_info, norm(b1));
  %yfunc = @(y) y./omega_bragg_normalized;
  yfunc = @(data, pos, data_info) mpb_yfunc_custom(data, pos, data_info, omega_bragg_normalized);

  %myPlotter = @(f) plot_MPB(f, 'ylim',[0,2.5], 'y_axis_scale_factor', 1/omega_bragg_normalized, 'grid', true, 'new_figure', false, 'linespec', 'o', 'kfunc', kfunc);
  myPlotter = @(f) plot_MPB(f, 'ylim',[0,2.5], 'yfunc',yfunc, 'grid', true, 'new_figure', false, 'linespec', 'o', 'xzfunc', xzfunc);

  %kfunc_rev = @(x,y,z) -norm(b1)*x;
  xzfunc_rev = @(data, pos, data_info) mpb_xzfunc_custom(data, pos, data_info, -norm(b1));
  %myPlotter_rev = @(f) plot_MPB(f, 'ylim',[0,2.5], 'y_axis_scale_factor', 1/omega_bragg_normalized, 'grid', true, 'new_figure', false, 'linespec', 'o', 'kfunc', kfunc_rev);
  myPlotter_rev = @(f) plot_MPB(f, 'ylim',[0,2.5], 'yfunc', yfunc, 'grid', true, 'new_figure', false, 'linespec', 'o', 'xzfunc', xzfunc_rev);

  %kfunc1 = @(x,y,z) x;
  %myPlotter1 = @(f) plot_MPB(f, 'ylim',[0,2.5], 'y_axis_scale_factor', 1/omega_bragg_normalized, 'grid', true, 'new_figure', false, 'linespec', 'o-', 'kfunc', kfunc1, 'bands', 1:2:6);
  %myPlotter1 = @(f) plot_MPB(f, 'ylim',[0,2.5], 'yfunc', yfunc, 'grid', true, 'new_figure', false, 'linespec', 'o-', 'kfunc', kfunc1, 'bands', 1:2:6);
  %kfunc2 = @(x,y,z) -x+1;
  %myPlotter2 = @(f) plot_MPB(f, 'ylim',[0,2.5], 'y_axis_scale_factor', 1/omega_bragg_normalized, 'grid', true, 'new_figure', false, 'linespec', 'o-', 'kfunc', kfunc2, 'bands', 2:2:6);
  %myPlotter2 = @(f) plot_MPB(f, 'ylim',[0,2.5], 'yfunc', yfunc, 'grid', true, 'new_figure', false, 'linespec', 'o-', 'kfunc', kfunc2, 'bands', 2:2:6);

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

  saveas(gcf, sprintf('DBR_TE_TM_projected_bands.n1=%.2f.n2=%.2f.d1=%.2f.d1=%.2f.png', n1, n2, d1, d2));

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
end
