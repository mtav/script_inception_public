function DiffractionGratingPlot2(N_lines, line_width_mum, grating_period_mum, lambda_mum_slice, lambda_mum, theta_deg)
  % DiffractionGratingPlot2(N_lines, line_width_mum, grating_period_mum, lambda_mum_slice, lambda_mum, theta_deg)
  % function [reflectance, transmittance] = DiffractionGratingPlot2(lambda, N_lines, line_width_mum, grating_period_mum, incidence_angle_rad)
  % cf: http://scienceworld.wolfram.com/physics/MultipleSlitInterference.html
  % cf: https://www.classe.cornell.edu/~liepe/webpage/docs/Phys2208_lecture34.pdf
  % example usage:
  %   close all; clear all; DiffractionGratingPlot2(10,0.500,1.000, 0.400, linspace(0.1,0.5), linspace(-30,30,1000));
  
  % TODO: Add incident angle dependence
  % TODO: Add collection angle dependence (lens NA (Numerical Aperture))
  % TODO: overlay mode lines
  
  if ~exist('N_lines', 'var')
    N_lines = 6;
  end
  if ~exist('line_width_mum', 'var')
    line_width_mum = 0.100;
  end
  if ~exist('grating_period_mum', 'var')
    grating_period_mum = 2.400;
  end
  
  if ~exist('lambda_mum_slice', 'var')
    lambda_mum_slice = 0.600;
  end
  if ~exist('lambda_mum', 'var')
    lambda_mum = linspace(0.100, 0.500);
  end
  
  if ~exist('theta_deg', 'var')
    theta_deg = linspace(-31,31,1000);
  end
  
  theta_rad = deg2rad(theta_deg);
  
  %DiffractionGratingPlot(grating_period_mum, x_values, lambda_mum_range, L_mm, theta_i_deg, m_list, invert_axis, plot_vs_theta, lambda_in_nm)
  DiffractionGratingPlot(grating_period_mum, theta_deg, lambda_mum, 25, 0, 1:7, true, true, false);
  hline(lambda_mum_slice, 'r-');
  
  [I1,I2,I3] = Grating(theta_rad, lambda_mum_slice, N_lines, line_width_mum, grating_period_mum, true);
  
  figure;
  hold on;
  plot(theta_deg, I1,'g-');
  plot(theta_deg, I2,'r--');
  plot(theta_deg, I3,'k-');
  
  legend({'I1','I2','I1*I2'});
  xlim(getRange(theta_deg));
  xlabel('theta (degrees)');
  grid on;
  title(sprintf('lambda = %.3f mum', lambda_mum_slice));
  
  [meshgrid_theta_rad, meshgrid_lambda_mum] = meshgrid(theta_rad, lambda_mum);
  [I1,I2,I3] = Grating(meshgrid_theta_rad, meshgrid_lambda_mum, N_lines, line_width_mum, grating_period_mum, true);
  
  meshgrid_theta_deg = rad2deg(meshgrid_theta_rad);
  
  figure;
  surf(meshgrid_theta_deg, meshgrid_lambda_mum, I1);
  view(2);
  set(gca, 'YDir','reverse');
  shading interp;
  colorbar;
  xlabel('theta (degrees)');
  ylabel('lambda (mum)');
  title('I1 (Single Slot Diffraction)');
  
  figure;
  surf(meshgrid_theta_deg, meshgrid_lambda_mum, I2);
  view(2);
  set(gca, 'YDir','reverse');
  shading interp;
  colorbar;
  xlabel('theta (degrees)');
  ylabel('lambda (mum)');
  title('I2 (Multiple Slot Interference)');
  
  figure;
  surf(meshgrid_theta_deg, meshgrid_lambda_mum, I3);
  view(2);
  set(gca, 'YDir','reverse');
  shading interp;
  colorbar;
  xlabel('theta (degrees)');
  ylabel('lambda (mum)');
  title('I3 (Grating)');
end

function I1 = SingleSlotDiffraction(theta_rad, lambda_mum, a)
  size(theta_rad)
  size(lambda_mum)
  alpha = ((pi*a)./lambda_mum).*sin(theta_rad);
  I1 = (sin(alpha)./alpha).^2;
end

function I2 = MultipleSlotInterference(theta_rad, lambda_mum, N, d)
  % TODO: find proper normalization factor...
  k = 2*pi./lambda_mum;
  delta = k.*d.*sin(theta_rad);
  I2 = (sin((1/2)*N*delta)./sin((1/2)*delta)).^2;
end

function [I1,I2,I3] = Grating(theta_rad, lambda_mum, N_lines, line_width_mum, grating_period_mum, normalize)
  
  if ~exist('normalize', 'var')
    normalize = false;
  end
  
  N = N_lines;
  a = line_width_mum;
  d = grating_period_mum;
  I1 = SingleSlotDiffraction(theta_rad, lambda_mum, a);
  I2 = MultipleSlotInterference(theta_rad, lambda_mum, N, d);
  
  if normalize
    I1 = I1/max(I1(:));
    I2 = I2/max(I2(:));
  end
  I3 = I1.*I2;
  %I3 = I3/max(I3(:));
end
