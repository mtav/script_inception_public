function grating_calibration_plot(a_um, lambda_range, angle_range_deg, NA_list)

  if exist('a_um','var')==0
    a_um = 1000/600;
  end

  if exist('lambda_range','var')==0
    lambda_range = [0.899, 1.714];
  end
  if exist('angle_range_deg','var')==0
    angle_range_deg = [-50, 50];
  end
  if exist('NA_list','var')==0
    NA_list = [0.75, 1];
  end

  %  clear all;
  %  close all;
  n = 1;
%    a_um = 1
%    a_um = 1000/600
  %a_um = 1000/300
  %a_um = 1000/1800
  %a_um = 1.6
  %a_um = 1000/830

%    lambda_range_VIS = [0.340, 0.800];
%    lambda_range_IR = [0.900, 1.700];
  
  lambda_um = linspace(lambda_range(1), lambda_range(2));
%    size(lambda_um)
  %  Xposition = FIS_PositionToAngle(theta_deg, 6, 1.88*10, false);

  LineSpec_list = {'r-', 'b-'};
  
  for idx = 1:length(NA_list)
  
      LineSpec = LineSpec_list{idx};
      NA = NA_list(idx);
      fprintf('NA=%.2f:\n', NA);
      
      for m = [1,2,3]
%            m
          lambda_intersection = (NA/n)*a_um/m;
          fprintf('m=%d: lambda_intersection=%.2f um\n', m, lambda_intersection);
          theta_deg = grating_calibration_line(m, NA, n, lambda_um, a_um);
          size(theta_deg);
          plot(theta_deg, lambda_um, LineSpec);
          hold on;
          plot(-theta_deg, lambda_um, LineSpec);
          hline(lambda_intersection);
      end
  end

  xlim(angle_range_deg);
  ylim(lambda_range);
  set(gca, 'YDir','reverse');
  title(sprintf('a=%.2f um -> %d lines per mm', a_um, floor(1000/a_um)));
  xlabel('Angle (degrees)');
  ylabel('Wavelength (um)');
end
