function [data, ax, mini, maxi] = FIS_plot2D()
  data = FIS_getData();
  if length(data.Position) > 0
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
    %   setValue(handles, hmin, 'min', mini);
    %   setValue(handles, hmax, 'max', maxi);

      drawnow();
  else
      error('Something wrong');
  end
end
