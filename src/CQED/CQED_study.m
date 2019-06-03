function ret = CQED_study(gamma, g, omega0, delta_omega, Q)
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %%% compute values
  %
  % TODO: find proper factor for spectrum!!! (but normalization by numerically integrated area is pretty good)
  
  ret = struct();

  % for conversions
  Hz_to_meV = get_hb()/(1e-3*get_eV()); % to convert angular frequencies (omega) from Hz to meV

  % grid size
  ret.N_Q = length(Q);
  ret.N_delta_omega = length(delta_omega);

  % create grids
  [ret.grid_delta_omega, ret.grid_Q] = meshgrid(delta_omega, Q);

  ret.grid_omega = omega0 + ret.grid_delta_omega;
  ret.grid_kappa = omega0 ./ ret.grid_Q;
  
  [ret.grid_S_Andreani, omega_p, omega_m] = function_S_Andreani(ret.grid_omega, omega0, ret.grid_kappa, gamma, g);

  % compute area under spectrum for each Q
  ret.area_per_Q = ones(ret.N_Q,1);
  for idx =1:ret.N_Q
    y = ret.grid_S_Andreani(idx,:);
    x = ret.grid_delta_omega(idx,:);
    ret.area_per_Q(idx) = trapz(x,y);
  end
  
  % create grid for it
  ret.grid_area = repmat(ret.area_per_Q(:), 1, ret.N_delta_omega);
  
  % normalize each by its area
  ret.grid_S_Andreani_normalized_by_area = ret.grid_S_Andreani ./ ret.grid_area;
  
%    figure; plot(ret.grid_delta_omega(1,:), ret.grid_S_Andreani_normalized_by_area(1,:));
  
  % normalize again to have overall maximum at 1
%    ret.grid_S_Andreani_normalized_by_area = ret.grid_S_Andreani_normalized_by_area ./ max(ret.grid_S_Andreani_normalized_by_area(:));

  % scale so that area under curve looks =1 using meV units
  ret.grid_S_Andreani_normalized_by_area = ret.grid_S_Andreani_normalized_by_area ./ Hz_to_meV;
  
  % get non-grid values
  ret.omega_p = omega_p(:,1);
  ret.omega_m = omega_m(:,1);
  
  ret.kappa_lim1 = 4*g+gamma; % split
  ret.kappa_lim2 = 4*g-gamma; % strong
  ret.kappa_lim3 = sqrt(8*g^2-gamma^2); % 2 peak
  
  ret.Q_lim1 = omega0/ret.kappa_lim1;
  ret.Q_lim2 = omega0/ret.kappa_lim2;
  ret.Q_lim3 = omega0/ret.kappa_lim3;

  % convenience attributes

  ret.delta_omega_p_real_meV = ( real(ret.omega_p)-omega0 )*Hz_to_meV;
  ret.delta_omega_p_imag_meV = ( -2*imag(ret.omega_p) )*Hz_to_meV;

  ret.delta_omega_n_real_meV = ( real(ret.omega_m)-omega0 )*Hz_to_meV;
  ret.delta_omega_n_imag_meV = ( -2*imag(ret.omega_m) )*Hz_to_meV;

  ret.grid_delta_omega_meV = ret.grid_delta_omega*Hz_to_meV;

  ret.gamma_meV = gamma*Hz_to_meV*ones(size(Q));
  ret.kappa_meV = (omega0 ./ Q)*Hz_to_meV;
  
end
