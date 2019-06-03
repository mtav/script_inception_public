function mask = getVolumetricMaskBox(X, Y, Z, centro, radius)
  if numel(radius)==1
    rx = radius;
    ry = radius;
    rz = radius;
  elseif numel(radius)==3
    rx = radius(1);
    ry = radius(2);
    rz = radius(3);
  else
    error('radius should be of length 1 or 3');
  end
  
  rmin = min([rx,ry,rz]);
  if isnan(rmin) || rmin==0
    mask = zeros(size(X));
    return
  end
  
  % and(dx<=1, dy<=1, dz<=1) -> (3 ineqs + 3 eqs)*N ops = 6*N
  % max(max(dx,dy),dz) <= 1 -> (2*ineqs + 1 ineq)*N ops = 3*N
  mask = ( max( max( abs((X - centro(1))./rx), abs((Y - centro(2))./ry) ), abs((Z - centro(3))./rz) ) <= 1 );
  
end
