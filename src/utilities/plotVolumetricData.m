function plotVolumetricData(X, Y, Z, V, SX, SY, SZ, plot_type)
  
  %%%%%%%%%%%%%%%%%%%
  % TODO: necessary?
  %% argument parsing
  %p = inputParser();
  %p = inputParserWrapper(p, 'addRequired', 'X', @isnumeric);
  %p = inputParserWrapper(p, 'addRequired', 'Y', @isnumeric);
  %p = inputParserWrapper(p, 'addRequired', 'Z', @isnumeric);
  %p = inputParserWrapper(p, 'addRequired', 'V', @isnumeric);
  %p = inputParserWrapper(p, 'addParamValue', 'SX', 'X', @(x) any(validatestring(x, snap_plane_list)));
  %p = inputParserWrapper(p, 'addParamValue', 'probe_ident', '_id_', @ischar);
  %p = inputParserWrapper(p, 'addParamValue', 'snap_time_number', 0, @(x) isnumeric(x) && 0<=x && x<=99);
  %p = inputParserWrapper(p, 'addParamValue', 'pre_2008_BFDTD_version', false, @islogical);
  %p = inputParserWrapper(p, 'parse', numID, varargin{:});
  %%%%%%%%%%%%%%%%%%%
  
  if ~exist('SX', 'var')
    SX = mean(getRange(X));
  end
  if ~exist('SY', 'var')
    SY = mean(getRange(Y));
  end
  if ~exist('SZ', 'var')
    SZ = mean(getRange(Z));
  end
  if ~exist('plot_type', 'var')
    plot_type = 'slice';
  end
  
  % exit gracefully in case of empty data
  if any(isnan(getRange(V)))
    disp('Empty dataset.');
    return
  end
  
  % conversion to double is required (in GNU Octave at least -> TODO: fix?)
  switch plot_type
    case 'isosurface'
      if min(V(:)) ~= max(V(:))
        v = double(V);
        isovalue = mean(getRange(V));
        if inoctave()
          isosurface(X, Y, Z, v, isovalue);
        else
          p = patch(isosurface(X, Y, Z, v, isovalue));
          isonormals(X, Y, Z, v, p);
          p.FaceColor = 'red';
          p.EdgeColor = 'none';
          p.FaceAlpha = 0.5;
          daspect([1,1,1])
          view(3); axis tight
          camlight;
          set(p, 'FaceLighting', 'gouraud');
        end
      else
        warning('plotVolumetricData: isosurface: data is homogeneous.');
        fprintf('size(V) = %s\n', num2str(size(V)));
        fprintf('getRange(V) = %s\n', num2str(getRange(V)));
        fprintf('mean(getRange(V)) = %f\n', mean(getRange(V)));
      end
    case 'contourslice'
      contourslice(X, Y, Z, double(V), SX, SY, SZ);
      shading flat;
      colormap jet;
      colorbar;
    otherwise
      slice(X, Y, Z, double(V), SX, SY, SZ);
      shading flat;
      colormap jet;
      colorbar;
  end
  
  % labels
  xlabel('x'); ylabel('y'); zlabel('z');
  
  % axis limits
  xlim(getRange(X));
  ylim(getRange(Y));
  zlim(getRange(Z));
end
