function [data, ax, mini, maxi] = FIS_plot2D(data, drawing_function, bool_x_axis_angle)
  % Usage:
  %   [data, ax, mini, maxi] = FIS_plot2D(data, drawing_function, bool_x_axis_angle)
  %
  % If 'data' is not given, a GUI will allow the user to select it.
  %
  % Data can be loaded in advance as follows:
  %   data = FIS_getData_VIS();
  %
  % options:
  %   drawing_function:
  %     'pcolor' (default)
  %     'surf'
  %     'contour'
  %   bool_x_axis_angle:
  %     true: Use angle in degrees for the X axis. (requires the calibration field to be present, see below)
  %     false: Use position in mm for the X axis.
  
  % Angle calibration:
  %   In order to convert between position (mm) and angle (degrees), the **data** structure should contain the following values:
  %     data.metadata.calibration.x.centre: normal incidence position in mm
  %     data.metadata.calibration.x.degrees_per_mm: degrees/mm value
  %     data.metadata.calibration.x.bool_trigonometric_mode: true/false
  %
  % useful customization commands:
  %   xlim([min, max]);
  %   ylim([min, max]);
  %   zlim([min, max]);
  %   caxis([min, max]);
  %   color scale:
  %     set(gca,'ColorScale', 'linear');
  %     set(gca,'ColorScale', 'log');
  %   Y axis direction:
  %     set(gca, 'YDir','reverse');
  %     set(gca, 'YDir','normal');
  
  figure_info = struct();
  
  if ~exist('data', 'var')
    data = FIS_getData_VIS();
  end
  if ~exist('drawing_function', 'var')
    drawing_function = 'pcolor';
  end
  if ~exist('bool_x_axis_angle', 'var')
    bool_x_axis_angle = true;
  end
  if length(data.Position) > 0
      if bool_x_axis_angle && isfield(data.metadata, 'calibration')
          centro = data.metadata.calibration.x.centre;
          factor = data.metadata.calibration.x.degrees_per_mm;
          bool_trigonometric_mode = data.metadata.calibration.x.bool_trigonometric_mode;
          x_values = FIS_PositionToAngle(data.Position, centro, factor, bool_trigonometric_mode);
          x_label = 'angle (degrees)';
          data.AngleDegrees = x_values;
          data.metadata.PositionToAngle = @(x) FIS_PositionToAngle(x, centro, factor, bool_trigonometric_mode);
      else
          x_values = data.Position;
          x_label = 'position (mm)';
      end
      ax = gca();
      if strcmpi(drawing_function, 'pcolor')
        pcolor(x_values, data.Lambda, data.Intensity);
      elseif strcmpi(drawing_function, 'contour')
        contour(x_values, data.Lambda, data.Intensity);
      else
        surf(x_values, data.Lambda, data.Intensity);
      end
      xlabel(x_label);
      ylabel('lambda (nm)');
      zlabel('intensity (AU)');
      colorbar(); % The colorbar can mess up axis overlays!
      shading interp;
      axis tight;
      view(2);
      mini = min(data.Intensity(:));
      maxi = max(data.Intensity(:));
      if maxi >= 65535
          warning('Saturated signal: maxi = %d', maxi);
      end
      drawnow();
  else
      error('Something wrong');
  end
end
