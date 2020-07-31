function k = DBR_bands(wn, n1, n2, d1, d2)
  % Calculates the theoretical photonic bands of a 1D DBR photonic crystal.
  % Returns the "k" (wavevector) values for given "wn" (normalized omega = a / lambda) values.
  %
  % See equation 7.2-19 in "Fundamentals of photonics", second edition by Saleh&Teich.
  %
  % See the scripts in src/examples/MPB-examples/DBR-stacks/ for an example application.

  a = d1 + d2;
  g = 2*pi./a;
  r12_squared = (n2-n1).^2 ./ (n1+n2).^2;
  t12t21 = 4*n1*n2 ./ (n1+n2).^2;
  C = (n1*d1-n2*d2)./(n1*d1+n2*d2);
  neff = n1*d1+n2*d2;
  omega_bragg = (get_c0()./neff) .* (pi./a);
  
  % cos(k*a) = 1./t12t21 * (cos(2*pi*neff*wn)-r12_squared*cos(2*pi*neff*C*wn));
  k = acos(1./t12t21 * (cos(2*pi*neff*wn)-r12_squared*cos(2*pi*neff*C*wn))) ./ a;
end
