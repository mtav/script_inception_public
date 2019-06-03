function [S_Carmichael_general, lambda_p, lambda_m, S_Carmichael_weak, S_Carmichael_strong, T_Carmichael_strong, S_factor] = function_S_Carmichael(omega, omega0, kappa, gamma, g)
  % Emission spectrum expression from Carmichael1989
  %
  % WARNING: kappa is defined differently by Carmichael and by Andreani apparently!!!
  % kappa_Carmichael = -kappa_Andreani/2 ???

  lambda_p = -1/2*(kappa+gamma/2) + sqrt( (kappa-gamma/2).^2 - g.^2 );
  lambda_m = -1/2*(kappa+gamma/2) - sqrt( (kappa-gamma/2).^2 - g.^2 );
  
  % frequency independent factor
  S_factor = (1/2 * ((kappa.*(kappa+gamma/2)+g.^2) ./ ( (kappa+gamma/2).*( kappa.*gamma/2 + g.^2 ) )) .* abs(lambda_p-lambda_m).^2).^(-1);
  
  % Spontaneous emission spectrum expression from Carmichael1989 in the general case
  S_Carmichael_general = S_factor .* abs( (lambda_p + kappa) ./ (lambda_p - i*(omega - omega0)) - (lambda_m + kappa) ./ (lambda_m - i*(omega - omega0)) ).^2;

  % Spontaneous emission spectrum expression from Carmichael1989, for kappa>>g>>gamma/2
  S_Carmichael_weak = (gamma + 2*g.^2 ./ kappa) ./ ( 1/4*(gamma + 2*g.^2./kappa).^2 + (omega-omega0).^2 );

  % Spontaneous emission spectrum expression from Carmichael1989, for g>>kappa, g>>gamma/2
  S_Carmichael_strong = ( (1/2*(kappa+gamma/2)) ./ ( (1/4*(kappa+gamma/2).^2) + (omega-omega0-g).^2 ) ) + ( (1/2*(kappa+gamma/2)) ./ ( (1/4*(kappa+gamma/2).^2) + (omega-omega0+g).^2 ) );

  % Fluorescent emission spectrum expression from Carmichael1989, for g>>kappa, g>>gamma/2
  T_Carmichael_strong = ( (1/4*(kappa+gamma/2).^3) ./ ( (1/4*(kappa+gamma/2).^2) + (omega-omega0-g).^2 ).^2 ) + ( (1/4*(kappa+gamma/2).^3) ./ ( (1/4*(kappa+gamma/2).^2) + (omega-omega0+g).^2 ).^2 );
end
