function DiffractionGratingPlot(grating_period_mum, x_values, lambda_mum_range, L_mm, theta_i_deg, m_list, invert_axis, plot_vs_theta, lambda_in_nm)
  % measurement-like transmittance plot for a diffraction grating:
  % TODO
  
  % basic mode lines
  % d*(sin(theta_m_rad)-sin(theta_i_rad))=m*lambda
  % lambda = d*(sin(theta_m_rad)-sin(theta_i_rad)) / m
  
  % principal maxima when sin(theta)=n*lambda_mum/grating_period_mum
  % theta=asin(n*lambda_mum/grating_period_mum)
  % cf formulas in ~/Desktop/proposals/DLW/publications2/Phys2208_lecture34.pdf -> adapt for different incidence angles
  
  %close all;
  %clear all;
  %theta=linspace(-pi/4, pi/4);
  %theta=linspace(-pi/2, pi/2);
  if ~exist('lambda_mum_range','var')
    %lambda_mum_range = [0.4, 0.8]
    lambda_mum_range = [0.200,1.700]
    %lambda_mum_range=[0.2, 0.8];
    %lambda_mum_range=[0.8,2];
    %lambda_mum_range=[0,2];
  end
  if ~exist('grating_period_mum','var')
    %grating_period_mum = 1.5
    grating_period_mum = 1
  end
  if ~exist('L_mm','var')
    L_mm = 25
  end
  if ~exist('theta_i_deg','var')
    theta_i_deg = 90
  end
  if ~exist('m_list','var')
    m_list = 1:3
  end
  if ~exist('invert_axis','var')
    invert_axis = true
  end
  if ~exist('plot_vs_theta','var')
    plot_vs_theta = true
  end
  if ~exist('lambda_in_nm','var')
    lambda_in_nm = true
  end
  
  if invert_axis
    set(gca, 'YDir','reverse');
  else
    set(gca, 'YDir','normal');
  end
  if ~exist('x_values','var')
    if plot_vs_theta
      theta_m_deg = linspace(0, 60);
      x_mm = L_mm*tan(deg2rad(theta_m_deg));
    else
      x_mm = linspace(-6,6);
      %theta_m_deg = rad2deg(atan(x_mm/L_mm));
      theta_m_deg = rad2deg(atan2(x_mm, L_mm));
    end
  else
    if plot_vs_theta
      theta_m_deg = x_values;
      x_mm = L_mm*tan(deg2rad(theta_m_deg));
    else
      x_mm = x_values;
      %theta_m_deg = rad2deg(atan(x_mm/L_mm));
      theta_m_deg = rad2deg(atan2(x_mm, L_mm));
    end
  end
  
  hold on;
  for m = m_list
    for dir = [1,-1]
      lambda_mum = abs(grating_period_mum*(sin(deg2rad(dir*theta_m_deg))-sin(deg2rad(theta_i_deg)))/m);
      if lambda_in_nm
        Y = 1000*lambda_mum;
      else
        Y = lambda_mum;
      end
      if plot_vs_theta
        plot(theta_m_deg, Y);
      else
        plot(x_mm, Y);
      end
    end
  end

  if lambda_in_nm
    ylim(1000*getRange(lambda_mum_range));
  else
    ylim(getRange(lambda_mum_range));
  end
  ylabel('lambda (mum)');
  
  if plot_vs_theta
    xlabel('theta (degrees)');
    xlim(getRange(theta_m_deg));
  else
    xlabel('x (mm)');
    xlim(getRange(x_mm));
  end
  grid on;
  
  title(sprintf('grating period (mum) = %.2f, L (mm) = %.2f', grating_period_mum, L_mm));
end
