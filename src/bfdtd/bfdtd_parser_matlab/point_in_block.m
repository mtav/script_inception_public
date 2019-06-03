function mask = point_in_block(X, Y, Z, block)
  % works for single points and meshgrid like arrays
  % TODO: rotation support
  
  if not(isequal(size(X), size(Y))) || not(isequal(size(Y), size(Z))) || not(isequal(size(Z), size(X)))
    error('X,Y,Z must all have the same size.');
  end
  
  centro = 0.5*(block.upper + block.lower);
  radius = 0.5*abs(block.upper - block.lower);
  
  mask = getVolumetricMaskBox(X, Y, Z, centro, radius);
end
