function coupling_strength_5(Q, Veff_mum3, lambda_0_nm, lambda_os_nm, n_def, n_os, tau_ns)

  Veff = Veff_mum3*(1e-6)^3;
  lambda_0 = lambda_0_nm*1e-9;
  lambda_os = lambda_os_nm*1e-9;
  tau = tau_ns*1e-9;

  gamma = 1/tau;
  kappa = 2*pi*get_c0()/(lambda_os*Q);
  kappa_0 = 2*pi*get_c0()/(lambda_0*Q);
  Vn = Veff/(lambda_0/n_def)^3;
  Veff_rescaled = Vn*(lambda_os/n_def)^3;
  g = sqrt( ((3*Q)/(4*pi^2*Veff_rescaled)) * (lambda_os^3/(n_def^2*n_os)) * ((kappa*gamma)/4) );
  
  kappa_0_frequency_GHz = (kappa_0/(2*pi))/1e9
  gamma_frequency_GHz = (gamma/(2*pi))/1e9
  kappa_frequency_GHz = (kappa/(2*pi))/1e9
  g_frequency_GHz = (g/(2*pi))/1e9
  
  tau_kappa_0_ns = (1/kappa_0)/1e-9
  tau_gamma_ns = (1/gamma)/1e-9
  tau_kappa_ns = (1/kappa)/1e-9
  tau_g_ns = (1/g)/1e-9

  disp('---');

end
