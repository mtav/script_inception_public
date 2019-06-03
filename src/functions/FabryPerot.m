function [reflectance, transmittance] = FabryPerot(lambda, n_outside, n_inside, thickness, incidence_angle_rad)
  % function [reflectance, transmittance] = FabryPerot(lambda, n_outside, n_inside, thickness, incidence_angle_rad)
  %
  % Returns the reflectance and transmittance for a thin film
  %
  % input:
  %  lambda: wavelength of the incident light beam
  %  n_outside: refractive index of the medium around the thin film
  %  n_inside: refractive index of the thin film
  %  thickness: thickness of the thin film
  %  incidence_angle_rad: incidence angle of the incident light beam in radians
  %
  % output:
  %  reflectance: reflectance of the thin film
  %  transmittance: transmittance of the thin film
  %
  % refs:
  %   https://en.wikipedia.org/wiki/Fabry%E2%80%93P%C3%A9rot_interferometer
  %   Lipson, S.G.; Lipson, H.; Tannhauser, D.S. (1995). Optical Physics (3rd ed.). London: Cambridge U.P. p. 248. ISBN 0-521-06926-2. (or 4th edition, p305)
  %   Pochi Yeh, Optical waves in layered media
  %   Mark Fox, Quantum Optics
  
  % Normal Reflection Coefficient R
  R = ((n_inside-n_outside)/(n_inside+n_outside))^2;
  % The phase difference between each succeeding reflection is given by δ
  delta = (2*pi./lambda).*(2*n_inside*thickness*cos(incidence_angle_rad));
  
  % "coefficient of finesse" F (not "finesse") ( "finesse" = Delta(lambda)/delta(lambda) ~ pi*sqrt("coefficient of finesse")/2 )
  F = (4*R)/(1-R)^2;
  transmittance = 1./(1+F*sin(delta/2).^2);
  reflectance = 1-transmittance;  
end
