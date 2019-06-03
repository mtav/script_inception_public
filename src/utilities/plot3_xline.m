function line_handle = plot3_xline(xlist, varargin)
  % function plot3_xline(zlist, varargin)
  % vararagin goes to a plot3() call

  ishold_orig = ishold();
  
  if ~ishold_orig
    hold on;
  end
  % TODO: Ideally, we should use the data range?
  x_range = get(gca,'XLim');
  y_range = get(gca,'YLim');
  z_range = get(gca,'ZLim');
  
  xlist = xlist(:)';
  
  for x = xlist
    xx = x*ones(1,5);
    yy = [y_range(1), y_range(2), y_range(2), y_range(1), y_range(1)];
    zz = [z_range(1), z_range(1), z_range(2), z_range(2), z_range(1)];
    line_handle = plot3(xx, yy, zz, varargin{:});
  end
  
  if ~ishold_orig
    hold off;
  end
  
end
