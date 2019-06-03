function [xzoom, yzoom]=zoomPlot(x, y, xmin, xmax)
  index_1 = find(abs(x-xmin)==min(abs(x-xmin)));
  index_2 = find(abs(x-xmax)==min(abs(x-xmax)));
  index_min = min(index_1,index_2);
  index_max = max(index_1,index_2);
  xzoom = x(index_min:index_max);
  yzoom = y(index_min:index_max);
end
