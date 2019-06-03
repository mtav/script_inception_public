function mask = getVolumetricMaskSphere(X, Y, Z, centro, radius)
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
  mask = ( ((X - centro(1))./rx).^2 + ((Y - centro(2))./ry).^2 + ((Z - centro(3))./rz).^2 <= 1 );
end
