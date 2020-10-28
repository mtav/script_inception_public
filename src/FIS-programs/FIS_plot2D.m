function [data, ax, mini, maxi] = FIS_plot2D(data, drawing_function)
  % Usage:
  %   [data, ax, mini, maxi] = FIS_plot2D(data, drawing_function)
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
  
  if ~exist('data', 'var')
    data = FIS_getData_VIS();
  end
  if ~exist('drawing_function', 'var')
    drawing_function = 'pcolor';
  end
  if length(data.Position) > 0
      ax = gca();
      if strcmpi(drawing_function, 'pcolor')
        pcolor(data.Position, data.Lambda, data.Intensity);
      elseif strcmpi(drawing_function, 'contour')
        contour(data.Position, data.Lambda, data.Intensity);
      else
        surf(data.Position, data.Lambda, data.Intensity);
      end
      xlabel('position (mm)');
      ylabel('lambda (nm)');
      zlabel('intensity (AU)');
      colorbar();
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
