function ellipse_handles = plot3_ellipsoid(centro3, radius3, sides_str, varargin)
  % function ellipse_handles = plot3_ellipsoid(centro3, radius3, sides_str, varargin)
  % Projects a 3D ellipsoid onto the 6 sides of a 3D axes box by drawing corresponding ellipses using plot3() calls.
  % "sides_str" specifies which sides to draw on. It should be a string of the form 'x', 'y', 'xz', 'xyz', etc.
  % vararagin goes to the plot3() calls.
  %
  % example:
  %   centro3=rand(1,3); radius3=rand(1,3);
  %   figure;
  %   [x, y, z] = sphere();
  %   surf(centro3(1)+radius3(1)*x, centro3(2)+radius3(2)*y, centro3(3)+radius3(3)*z); daspect([1,1,1]);
  %   ellipse_handles = plot3_ellipsoid(centro3, radius3, 'x', 'r-');
  %   ellipse_handles = plot3_ellipsoid(centro3, radius3, 'y', 'g-');
  %   ellipse_handles = plot3_ellipsoid(centro3, radius3, 'z', 'b-');
  
  ishold_orig = ishold();
  
  if ~ishold_orig
    hold on;
  end
  % TODO: Ideally, we should use the data range?
  x_range = get(gca,'XLim');
  y_range = get(gca,'YLim');
  z_range = get(gca,'ZLim');
  
  theta = linspace(0, 2*pi);
  
  ellipse_handles = {};
  
  if contains(sides_str,'x')
    % X-/X+ side ellipses
    for idx = 1:2
      xx = x_range(idx)*ones(size(theta));
      yy = centro3(2) + radius3(2)*cos(theta);
      zz = centro3(3) + radius3(3)*sin(theta);
      ellipse_handles{end+1} = plot3(xx, yy, zz, varargin{:});
    end
  end
  
  if contains(sides_str,'y')
    % Y-/Y+ side ellipses
    for idx = 1:2
      yy = y_range(idx)*ones(size(theta));
      zz = centro3(3) + radius3(3)*cos(theta);
      xx = centro3(1) + radius3(1)*sin(theta);
      ellipse_handles{end+1} = plot3(xx, yy, zz, varargin{:});
    end
  end
  
  if contains(sides_str,'z')
    % Z-/Z+ side ellipses
    for idx = 1:2
      zz = z_range(idx)*ones(size(theta));
      xx = centro3(1) + radius3(1)*cos(theta);
      yy = centro3(2) + radius3(2)*sin(theta);
      ellipse_handles{end+1} = plot3(xx, yy, zz, varargin{:});
    end
  end
  
  if ~ishold_orig
    hold off;
  end
  
end
