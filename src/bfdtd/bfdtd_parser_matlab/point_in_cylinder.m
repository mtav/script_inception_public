function mask = point_in_cylinder(X, Y, Z, cylinder)
  % works for single points and meshgrid like arrays
  % TODO: rotation support
  
  if not(isequal(size(X), size(Y))) || not(isequal(size(Y), size(Z))) || not(isequal(size(Z), size(X)))
    error('X,Y,Z must all have the same size.');
  end
  
  dX = abs(X - cylinder.center(1));
  dY = abs(Y - cylinder.center(2));
  dZ = abs(Z - cylinder.center(3));
  
  % cylinder in Y direction (BFDTD default)
  % r2 = dX.^2 + dZ.^2;
  % mask = (dY <= cylinder.height/2) & (r2 <= cylinder.outer_radius.^2 ) & (r2 >= cylinder.inner_radius.^2 );

  % cylinder in Z direction
  r2 = dX.^2 + dY.^2;
  mask = (dZ <= cylinder.height/2) & (r2 <= cylinder.outer_radius.^2 ) & (r2 >= cylinder.inner_radius.^2 );
  
end
