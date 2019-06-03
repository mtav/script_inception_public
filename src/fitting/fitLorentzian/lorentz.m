function [y] = lorentz(v, x)
  % Usage:
  %   [y] = lorentz(v, x)
  %
  % v = [x0, y0, A, FWHM]
  % (x0,y0) = offset
  % maximum = 2*A/(pi*w)
  % FWHM = w = Full Width at Half Maximum
  % Quality factor:
  % Q = x0/FWHM = x0/w
  x0 = v(1);
  y0 = v(2);
  A = v(3);
  w = v(4);
  y = y0+(2*A/pi).*(w./(4*(x-x0).^2+w.^2));
end
