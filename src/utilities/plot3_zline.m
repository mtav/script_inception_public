function line_handle = plot3_zline(zlist, varargin)
  % function plot3_zline(zlist, varargin)
  % vararagin goes to a plot3() call
  
  ishold_orig = ishold();
  
  if ~ishold_orig
    hold on;
  end
  % TODO: Ideally, we should use the data range?
  x_range = get(gca,'XLim');
  y_range = get(gca,'YLim');
  z_range = get(gca,'ZLim');
  
  zlist = zlist(:)';
  
  for z = zlist
    xx = [x_range(1), x_range(1), x_range(2), x_range(2), x_range(1)];
    yy = [y_range(1), y_range(2), y_range(2), y_range(1), y_range(1)];
    zz = z*ones(1,5);
    line_handle = plot3(xx, yy, zz, varargin{:});
  end
  
  if ~ishold_orig
    hold off;
  end
  
end
