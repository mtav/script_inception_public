function [azimuth, elevation_from_equator, r, elevation_from_Z] = cart2sph_advanced(x, y, z)
  % This function is is equivalent to cart2sph from Matlab/Octave, but returns two elevations:
  % - elevation_from_equator
  % - elevation_from_Z
  %
  % Note: It was created to avoid the issue of (x,y,z)=(0,0,0) giving (elevation from Z) = pi/2 - (elevation from equator) = pi/2 - 0 = pi/2.
  %
  azimuth = atan2(y, x);
  r = sqrt(x.^2 + y.^2 + z.^2);
  
  % Matlab/Octave style elevation from the "equator".
  elevation_from_equator = atan2(z, sqrt(x.^2 + y.^2));
  
  % Elevation from the "Z axis".
  elevation_from_Z = atan2(sqrt(x.^2 + y.^2), z);
  
end
