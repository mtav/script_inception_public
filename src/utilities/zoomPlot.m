function [xzoom, yzoom, index_min, index_max] = zoomPlot(x, y, xmin, xmax)
  % function [xzoom, yzoom, index_min, index_max] = zoomPlot(x, y, xmin, xmax)
  %   Returns a subset xzoom, yzoom of x,y so that:
  %     x(index_min) is closest to xmin
  %     x(index_max) is closest to xmax
  %   For 1D plots only!
  index_1 = find(abs(x-xmin)==min(abs(x-xmin)));
  index_2 = find(abs(x-xmax)==min(abs(x-xmax)));
  
  edge_indices = [index_1(:); index_2(:)];
  
  index_min = min(edge_indices(:));
  index_max = max(edge_indices(:));
  
  xzoom = x(index_min:index_max);
  yzoom = y(index_min:index_max);
end
