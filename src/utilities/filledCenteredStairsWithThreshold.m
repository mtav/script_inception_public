function filledCenteredStairsWithThreshold(x, y, threshold, color)
  x = x(:);
  y = y(:);
  
  y_limits = get(gca, 'YLim');
  ymin = y_limits(1);
  ymax = y_limits(2);
  
  xmin = min(x);
  xmax = max(x);
  
  yy = (ymax-ymin)*(y > threshold) + ymin;
  
  filledCenteredStairs(x, yy, ymin, color, xmin, xmax);
  
end
