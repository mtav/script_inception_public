function [xmin, xmax, ymin, ymax] = axis_equal_advanced(axes_handle, XData, YData, anchor_data, anchor_window, varargin)
  % function axis_equal_advanced(axes_handle, XData, YData, anchor_data, anchor_window, varargin)
  %
  % anchor_data: anchor position in "data coordinates", i.e. (0,0) for centre of data
  % anchor_window: anchor position in "window coordinates", i.e. (0,0) for centre of window
  %
  % ParamValue options:
  %   relative_data_coordinates : true/false to consider "anchor_data" as being in relative or absolute data coordinates
  %
  % Note that XData, YData do not have to be the actual X,Y data. You can just pass any desired range you want to be used, similar to how you would use xlim, ylim.
  % example: XData = [xmin, xmax], YData = [ymin, ymax]
  
  p = inputParser();
  p = inputParserWrapper(p, 'addRequired', 'axes_handle');
  p = inputParserWrapper(p, 'addRequired', 'XData', @isnumeric);
  p = inputParserWrapper(p, 'addRequired', 'YData', @isnumeric);
  p = inputParserWrapper(p, 'addRequired', 'anchor_reldata', @isnumeric);
  p = inputParserWrapper(p, 'addRequired', 'anchor_window', @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'relative_data_coordinates', false, @islogical);
  p = inputParserWrapper(p, 'addParamValue', 'forced_limit', 'auto', @(x) any(validatestring(x, {'auto','x','y'})));
  p = inputParserWrapper(p, 'parse', axes_handle, XData, YData, anchor_data, anchor_window, varargin{:});
  
  fig = ancestor(p.Results.axes_handle,'figure','toplevel');
  figure_position = get(fig, 'Position');
  figure_width = figure_position(3);
  figure_height = figure_position(4);
  
  axes_position = get(p.Results.axes_handle, 'Position');
  axes_width = axes_position(3)*figure_width;
  axes_height = axes_position(4)*figure_height;
  
  x_data_range = getRange(p.Results.XData);
  data_width = x_data_range(2) - x_data_range(1);
  
  y_data_range = getRange(p.Results.YData);
  data_height = y_data_range(2) - y_data_range(1);
  
  alpha = axes_height/axes_width;
  beta = data_height/data_width;
  
  if strcmp(p.Results.forced_limit, 'x')
    data_width_new = data_width;
    data_height_new = alpha*data_width_new;
  elseif strcmp(p.Results.forced_limit, 'y')
    data_height_new = data_height;
    data_width_new = data_height_new/alpha;
  else
    if alpha < beta
      %disp('alpha < beta => reducing Y limits');
      data_width_new = data_width;
      data_height_new = alpha*data_width_new;
    else
      %disp('alpha < beta => reducing X limits');
      data_height_new = data_height;
      data_width_new = data_height_new/alpha;
    end
  end
  
  % coordinate conversions
  anchor_data = anchor_data(:);
  anchor_window = anchor_window(:);
  
  M_reldata_to_absdata = diag([data_width, data_height]);
  M_win_to_absdata = diag([data_width_new, data_height_new]);
  L_window = [-0.5; -0.5];
  U_window = [0.5; 0.5];
  
  origin_absdata = [mean(x_data_range); mean(y_data_range)];
  
  if p.Results.relative_data_coordinates
    anchor_reldata = anchor_data;
    anchor_absdata = origin_absdata + M_reldata_to_absdata * anchor_reldata;
  else
    anchor_absdata = anchor_data;
  end
  
  L_absdata = anchor_absdata + M_win_to_absdata*(-anchor_window + L_window);
  U_absdata = anchor_absdata + M_win_to_absdata*(-anchor_window + U_window);
  
  xmin = L_absdata(1);
  ymin = L_absdata(2);
  
  xmax = U_absdata(1);
  ymax = U_absdata(2);
  %xc = centro(1);
  %yc = centro(2);
  %xmin = xc_abs - 0.5*data_width_new;
  %xmax = xc_abs + 0.5*data_width_new;

  %ymin = yc_abs - 0.5*data_height_new;
  %ymax = yc_abs + 0.5*data_height_new;
  
  % We cannot use xlim/ylim, because the current axes object might be different
  set(p.Results.axes_handle, 'XLim', [xmin, xmax]);
  set(p.Results.axes_handle, 'YLim', [ymin, ymax]);
  
end
