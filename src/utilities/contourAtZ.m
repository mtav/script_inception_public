function [ContourMatrix , handle] = contourAtZ(Zc0, Xc, Yc, Zc, varargin)
  % function [ContourMatrix , handle] = contourAtZ(Zc0, Xc, Yc, Zc, varargin)
  %
  % TODO: C_enhanced = structure of Ncontourlines, which each contain a 2*Npts matrix?
  % TODO: support same options as contour(), including absence of X,Y? + return same handle object
  % TODO: possible to plot multiple lines with one plot3 call?
  % TODO: at the moment, meshgrid format is required. We should support Xc,Yc swapping, i.e. non-meshgrid format
  %
  % Hacking:
  %    -Specifying the Z value at which to draw, should really be part of the Contour Properties...
  %    -Or maybe there is a way to plot any usual 2D stuff using specified 3D space vectors? -> would be even more powerful.
  %

  p = inputParser();
  p = inputParserWrapper(p, 'addRequired', 'Zc0', @isnumeric);
  p = inputParserWrapper(p, 'addRequired', 'Xc', @isnumeric);
  p = inputParserWrapper(p, 'addRequired', 'Yc', @isnumeric);
  p = inputParserWrapper(p, 'addRequired', 'Zc', @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'cmin', NaN, @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'cmax', NaN, @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'colormap', colormap(), @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'contourValues', NaN, @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'LineWidth', NaN, @isnumeric);
  p = inputParserWrapper(p, 'parse', Zc0, Xc, Yc, Zc, varargin{:});
  
  handle = struct();
  
  %figure;
  %subplot(1,3,1);
  %imagesc(Xc);
  %colorbar
  %getRange(Xc)
  %subplot(1,3,2);
  %imagesc(Yc);
  %colorbar
  %getRange(Yc)
  %subplot(1,3,3);
  %imagesc(Zc);
  %colorbar
  %getRange(Zc)
  %error('STOP');
  %size(Xc)
  %size(Yc)
  %size(Zc)

  % compute contour lines
  %  ContourMatrix  = contourc(xvals, yvals, Z);
  %ContourMatrix  = contourc(Xc, Yc, Zc); % only works in Octave
  
  if min(Xc(1,:)) ~= max(Xc(1,:))
    contourc_x = Xc(1,:);
    contourc_y = Yc(:,1);
    contourc_z = Zc;
  else
    %error('Please use the meshgrid format, i.e. X varies along the second dimension and Y along the first.');
    contourc_x = Xc(:,1);
    contourc_y = Yc(1,:);
    contourc_z = Zc';
  end
  
  if ( length(contourc_x) ~= size(contourc_z, 2) ) || ( length(contourc_y) ~= size(contourc_z, 1) )
    error('Lengths of X and Y must match number of cols and rows in Z, respectively.: (%d, %d) ~= (%d, %d)', length(contourc_x), length(contourc_y), size(contourc_z, 2), size(contourc_z, 1));
  end
  
  if isnan(p.Results.contourValues)
    ContourMatrix  = contourc(contourc_x, contourc_y, contourc_z);
  else
    ContourMatrix  = contourc(contourc_x, contourc_y, contourc_z, p.Results.contourValues);
  end

  % problem: doing this will also change the caxis for the surface plot... (probably should not use colors for epsilon contours anyway)
  %  caxis([zc_min, zc_max]);
  %  v = caxis();
  if isnan(p.Results.cmin)
    handle.cmin = min(contourc_z(:));
  end
  if isnan(p.Results.cmax)
    handle.cmax = max(contourc_z(:));
  end

  handle.Ncolors = size(p.Results.colormap, 1);
  
  handle.line.info_idx = [];
  handle.line.level = [];
  handle.line.length = [];
  handle.line.start_idx = [];
  handle.line.stop_idx = [];
  handle.line.color = [];
  handle.line.handle = [];

  hold on;
  
  line_idx = 1;
  line_info_idx = 1;
  while true
    line_lev = ContourMatrix (1, line_info_idx);
    line_len = ContourMatrix (2, line_info_idx);

    line_start_idx = line_info_idx+1;
    line_stop_idx  = line_info_idx+line_len;

    line_X = ContourMatrix (1, line_start_idx:line_stop_idx);
    line_Y = ContourMatrix (2, line_start_idx:line_stop_idx);
    line_Z = Zc0*ones(size(line_X));

    % determine color to use:
    color_index = fix((line_lev-handle.cmin)/(handle.cmax-handle.cmin)*handle.Ncolors) + 1;
    RGB = ind2rgb(color_index, p.Results.colormap);
    %  %Clamp values outside the range [1 m]
    %  index(index<1) = 1;
    %  index(index>m) = m;

    line_handle = plot3(line_X, line_Y, line_Z, 'Color', RGB);
    if ~isnan(p.Results.LineWidth)
      set(line_handle, 'LineWidth', p.Results.LineWidth);
    end

    % store line info
    handle.line.info_idx(end+1) = line_info_idx;
    handle.line.level(end+1) = line_lev;
    handle.line.length(end+1) = line_len;
    handle.line.start_idx(end+1) = line_start_idx;
    handle.line.stop_idx(end+1) = line_stop_idx;
    handle.line.color = cat(1, handle.line.color, RGB);
    handle.line.handle(end+1) = line_handle;

    %line_idx += 1; % Matlab does not understand +=...
    line_idx = line_idx + 1;
    line_info_idx = line_stop_idx+1;
    
    if line_info_idx > size(ContourMatrix , 2)
      break;
    end
  end

  handle.Nlines = line_idx-1;
  
  %    [ContourMatrix , handle] = contour(varargin{:});
  
end
