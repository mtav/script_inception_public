function line_handle = plot3_yline(ylist, varargin)
  % function plot3_yline(zlist, varargin)
  % vararagin goes to a plot3() call

  ishold_orig = ishold();
  
  if ~ishold_orig
    hold on;
  end
  % TODO: Ideally, we should use the data range?
  x_range = get(gca,'XLim');
  y_range = get(gca,'YLim');
  z_range = get(gca,'ZLim');
  
  ylist = ylist(:)';
  
  for y = ylist
    xx = [x_range(1), x_range(2), x_range(2), x_range(1), x_range(1)];
    yy = y*ones(1,5);
    zz = [z_range(1), z_range(1), z_range(2), z_range(2), z_range(1)];
    line_handle = plot3(xx, yy, zz, varargin{:});
  end
  
  if ~ishold_orig
    hold off;
  end
  
end
