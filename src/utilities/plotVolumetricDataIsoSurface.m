function [patch_isosurface, patch_isocaps] = plotVolumetricDataIsoSurface(X, Y, Z, V, subvolume_limits, isovalue)
  
  % exit gracefully in case of empty data
  if any(isnan(getRange(V)))
    disp('Empty dataset.');
    return
  end
  
  if ~exist('isovalue', 'var')
    isovalue = mean(getRange(V))
  end
  
  if exist('subvolume_limits', 'var')
    [X, Y, Z, V] = subvolume_octave(X, Y, Z, V, subvolume_limits);
  end
  
  % conversion to double is required (in GNU Octave at least -> TODO: fix?)
  v = double(V);
  patch_isosurface = patch(isosurface(X, Y, Z, v, isovalue));
  isonormals(X, Y, Z, v, patch_isosurface);
  set(patch_isosurface, 'FaceColor', 'red');
  set(patch_isosurface, 'EdgeColor', 'none');
  if ~inoctave()
    % TODO: Transparency not yet supported in GNU Octave... :(
    set(patch_isosurface, 'FaceAlpha', 0.5);
  end
  
  % add isocaps
  patch_isocaps = patch(isocaps(X, Y, Z, v, isovalue), 'FaceColor', 'interp', 'EdgeColor', 'none');
  
  % TODO: GNU Octave still does not support this kind of notation...
  %patch_isosurface.FaceColor = 'red';
  %patch_isosurface.EdgeColor = 'none';
  %patch_isosurface.FaceAlpha = 0.5;
  daspect([1,1,1]);
  view(3); axis tight
  
  if ~inoctave()
    % TODO: Add GNU Octave support for camlight+lighting...
    camlight;
    set(patch_isosurface, 'FaceLighting', 'gouraud');
    set(patch_isocaps, 'FaceLighting', 'none');
  end
  
  % labels
  xlabel('x'); ylabel('y'); zlabel('z');
  
  % axis limits
  xlim(getRange(X));
  ylim(getRange(Y));
  zlim(getRange(Z));
end
