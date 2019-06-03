function [S_Andreani, omega_p, omega_m] = function_S_Andreani(omega, omega0, kappa, gamma, g)
  % Emission spectrum expression from Andreani1999
  %
  % WARNING: kappa is defined differently by Carmichael and by Andreani apparently!!!
  % kappa_Carmichael = -kappa_Andreani/2 ???

  omega_p = omega0 - (i/4)*(kappa+gamma) + sqrt(g.^2-((kappa-gamma)/4).^2);
  omega_m = omega0 - (i/4)*(kappa+gamma) - sqrt(g.^2-((kappa-gamma)/4).^2);
  
  S_Andreani = abs(((omega_p-omega0+i*kappa/2)./(omega-omega_p))-((omega_m-omega0+i*kappa/2)./(omega-omega_m))).^2;
  
%    [S_Carmichael_general, lambda_p, lambda_m, S_Carmichael_weak, S_Carmichael_strong, T_Carmichael_strong, S_factor] = function_S_Carmichael(omega, omega0, kappa/2, gamma, g);
%    
%    S_Andreani = S_factor.*S_Andreani;
  
  % TODO: try normalizing by area under curve (with trapz)
end
