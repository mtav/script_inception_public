function mask = point_in_sphere(X, Y, Z, sphere)
  % works for single points and meshgrid like arrays
  % TODO: rotation support
  
  if not(isequal(size(X), size(Y))) || not(isequal(size(Y), size(Z))) || not(isequal(size(Z), size(X)))
    error('X,Y,Z must all have the same size.');
  end
  
  dX = X - sphere.center(1);
  dY = Y - sphere.center(2);
  dZ = Z - sphere.center(3);
  dist2 = dX.^2 + dY.^2 + dZ.^2;
  
  mask = ( dist2 <= sphere.outer_radius.^2 );
  
end
