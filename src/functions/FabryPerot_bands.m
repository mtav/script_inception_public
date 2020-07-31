function Lambda = FabryPerot_bands(n_inside, thickness, incidence_angle_rad, Mode)
  % function Lambda = FabryPerot_bands(n_inside, thickness, incidence_angle_rad, Mode)
  %
  % Returns the reflectance (half-integer modes) and transmittance (integer modes) bands for a thin film.
  %
  % input:
  %  n_inside: refractive index of the thin film
  %  thickness: thickness of the thin film
  %  incidence_angle_rad: incidence angle of the incident light beam in radians
  %  Mode: mode; use half-integers for reflectance and integers for transmittance
  %
  % output:
  %  Lambda: wavelength of the incident light beam
  %
  % refs:
  %   https://en.wikipedia.org/wiki/Fabry%E2%80%93P%C3%A9rot_interferometer
  %   Lipson, S.G.; Lipson, H.; Tannhauser, D.S. (1995). Optical Physics (3rd ed.). London: Cambridge U.P. p. 248. ISBN 0-521-06926-2. (or 4th edition, p305)
  %   Pochi Yeh, Optical waves in layered media
  %   Mark Fox, Quantum Optics
  
  Lambda = 2*n_inside*thickness*cos(incidence_angle_rad) ./ Mode;
end
