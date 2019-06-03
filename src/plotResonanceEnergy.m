function plotResonanceEnergy()
  % arguments
  nGaAs=3.521;%no unit
  nAlGaAs=2.973;%no unit
  n0 = 1; % air refractive index
  Lcav = 253; % (nm)

  %n_cavity = nGaAs;
  %n_mirror = nAlGaAs;
  n_cavity = 2.4;
  n_mirror = 1;
  n_outside = n0;

  radius_mum = [0:0.1:5];
  figure;
  
  L_vector = 0:4;
  M_vector = 1:4;
  %L_vector = [0,2];
  %M_vector = [1];
  v_cutoff_mat = zeros(length(L_vector),length(M_vector));
  
  for L_idx = 1:length(L_vector)
    for M_idx = 1:length(M_vector)
      L = L_vector(L_idx);
      M = M_vector(M_idx);
      
      [ E_meV, lambda_nm, real_neff, radius_vector_mum, E_vector_meV, lambda_vector_nm, real_neff_vector, u, v, b, v_cutoff ] = resonanceEnergy(n_cavity, n_mirror, n_outside, Lcav, radius_mum, L, M);
      v_cutoff_mat(L_idx,M_idx) = v_cutoff;
      
      subplot(3,2,1);
      grid on; hold on;
      plot(radius_vector_mum,E_vector_meV,'r-','LineWidth',1);
      plot(radius_mum,E_meV,'bo','LineWidth',1);
      xlabel('radius (\mum)');
      ylabel('dE (meV)');
    
      subplot(3,2,2);
      grid on; hold on;
      plot(radius_vector_mum,lambda_vector_nm,'r-','LineWidth',1);
      plot(radius_mum,lambda_nm,'bo','LineWidth',1);
      xlabel('radius (\mum)');
      ylabel('\lambda (nm)');
      
      subplot(3,2,3);
      grid on; hold on;
      plot(v,b,'r-','LineWidth',1);
      xlabel('v (no unit)');
      ylabel('b (no unit)');
      axis([ 0 12 0 1 ]);

      subplot(3,2,4);
      grid on; hold on;
      plot(v,real_neff_vector,'r-','LineWidth',1);
      xlabel('v (no unit)');
      ylabel('n_{eff} = \beta/k = n_{mirror} + b*(n_{cavity}-n_{mirror}) (no unit)');
      axis([ 0 6.5 n_mirror n_cavity ]);

      subplot(3,2,5);
      grid on; hold on;
      plot(radius_vector_mum,real_neff_vector,'r-','LineWidth',1);
      plot(radius_mum,real_neff,'bo','LineWidth',1);
      xlabel('radius (mum)');
      ylabel('n_{eff} = \beta/k = n_{mirror} + b*(n_{cavity}-n_{mirror}) (no unit)');

    end
  end

  v_cutoff_mat

end
