function wn = DBR_bands_getOmega(k, n1, n2, d1, d2, band_index)
  % Calculates the theoretical photonic bands of a 1D DBR photonic crystal.
  % Returns the "wn" (normalized omega = a / lambda) values values for given "k" (wavevector) values.
  %
  % See equation 7.2-19 in "Fundamentals of photonics", second edition by Saleh&Teich.
  %
  % See the scripts in src/examples/MPB-examples/DBR-stacks/ for an example application.

  if any(isnan([n1,n2,d1,d2]))
    error('Invalid NaN parameter: n1=%.2f, n2=%.2f, d1=%.2f, d2=%.2f', n1, n2, d1, d2);
  end

  a = d1 + d2;
  
  if n1 ~= n2
      g = 2*pi./a;
      r12_squared = (n2-n1).^2 ./ (n1+n2).^2;
      t12t21 = 4*n1*n2 ./ (n1+n2).^2;
      C = (n1*d1-n2*d2)./(n1*d1+n2*d2);
      neff = n1*d1+n2*d2;
      omega_bragg = (get_c0()./neff) .* (pi./a);

      midgap_approximate = a ./ ( 2*(n1 .* d1 + n2 .* d2) );

      % cos(k*a) == 1./t12t21 * (cos(2*pi*neff*wn)-r12_squared*cos(2*pi*neff*C*wn));
      % k = acos(1./t12t21 * (cos(2*pi*neff*wn)-r12_squared*cos(2*pi*neff*C*wn))) ./ a;
      syms WN;
      for idx = 1:length(k)
        solution = vpasolve(cos(k(idx)*a) == 1./t12t21 * (cos(2*pi*neff*WN)-r12_squared*cos(2*pi*neff*C*WN)), [(band_index -1)*midgap_approximate, band_index*midgap_approximate]);
        if ~isempty(solution)
            wn_sym(idx) = solution;
        else
            error('No solution found in range.');
        end
      end
      wn = double(wn_sym);
  else
      wn = (k./n1) ./ (2*pi./a);
  end
  
end
