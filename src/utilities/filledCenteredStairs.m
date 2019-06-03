function filledCenteredStairs(x, y, basevalue, color, xmin, xmax)
  x = x(:);
  y = y(:);
  
  xpos = [];
  ypos = [];
  for idx = 1:length(x)
    if idx == 1
      xpos(end+1) = xmin;
    else
      xpos(end+1) = (x(idx-1) + x(idx))/2;
    end
    if idx == length(x)
      xpos(end+1) = xmax;
    else
      xpos(end+1) = (x(idx+1) + x(idx))/2;
    end
    ypos(end+1) = y(idx);
    ypos(end+1) = y(idx);
  end
  
  area(xpos, ypos, basevalue, 'FaceColor', color, 'LineStyle', 'none');
end
