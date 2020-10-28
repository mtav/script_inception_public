function [data, ax, mini, maxi] = FIS_plot2D(data)
  if ~exist('data', 'var')
    data = FIS_getData();
  end
  if length(data.Position) > 0
      figure();
      ax = axes();
      cla();
      surf(data.Position, data.Lambda, data.Intensity);
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
    %   setValue(handles, hmin, 'min', mini);
    %   setValue(handles, hmax, 'max', maxi);

      drawnow();
  else
      error('Something wrong');
  end
end
