function calculateCouplingStrengthTable(n, lambda_nm, Quc, Veff_mum3, oscillator_properties_list)
  % function calculateCouplingStrengthTable(n, lambda_nm, Quc, Veff_mum3, oscillator_properties, oscillator_feg)
  % calculates values for a table like the one in the JQE paper (Ho et al. - 2011 - FDTD Simulation of Inverse 3-D Face-Centered Cubic Photonic Crystal Cavities)
  % n: refractive index of the cavity, dimensionless
  % lambda_nm: resonance wavelength of the cavity, in nm
  % Quc: quality factor of the cavity, dimensionless
  % Veff_mum3: mode volume of the cavity, in mum^3
  % oscillator_properties_list: list of structures ({struct(),struct(),...}) containing the necessary oscillator properties. cf oscillator_properties.m
  
  %print part 1 of table
  disp(['=================================================================']);
  disp(['n = ', num2str(n,'%E ')]);
  disp(['lambda(nm) = ', num2str(lambda_nm,'%E ')]);
  disp(['Quc(no unit) = ', num2str(Quc,'%E ')]);
  disp(['V(mum^3) = ', num2str(V_mum3,'%E ')]);
  disp(['Veff/(lambda/(2*n))^3 = ', num2str(V_normalized,'%E ')]);
  disp(['Fp = ', num2str(Fp,'%E ')]);
  disp(['(kuc)/(2*pi)(GHz) = ', num2str(kuc_over_2pi_GHz,'%E ')]);
  disp(['=================================================================']);
  %for each QD/NV property set given:
  for i = 1:length(oscillator_properties_list)
    oscillator_properties = oscillator_properties_list(i)
    %if feg not given:
    if isfield(oscillator_properties,'feg')==0
      %calculate feg
      oscillator_properties.feg = get_feg(oscillator_properties.lambda_nm, oscillator_properties.deg_Cm)
    end
    %print part 2 of table (with gamma and tau for each gamma in property set)
    disp(['lambda(nm) = ', num2str(lambda_nm,'%E ')]);
    disp(['V(mum^3) = ', num2str(V_mum3,'%E ')]);
    disp(['Veff/(lambda/(2*n))^3 = ', num2str(V_normalized,'%E ')]);
    disp(['(kuc)/(2*pi)(GHz) = ', num2str((kuc_GHz)/(2*pi),'%E ')]);
    for j in 1:length(oscillator_properties.gamma_over_2pi_GHz)
      disp(['g/(2*pi)(GHz) = ', num2str(1/tau_ns,'%E ')]);
      disp(['tau(ns) = ', num2str(tau_ns,'%E ')]);
    end
    disp(['mu_ZPL(Coul*m) = ', num2str(mu_ZPL_SI,'%E ')]);
    disp(['mu_ZPL(Debye) = ', num2str(mu_ZPL_Debye,'%E ')]);
    disp(['E1ph(N/coul=V/m) = ', num2str(E1ph_SI,'%E ')]);
    disp(['feg(no unit) = ', num2str(feg,'%E ')]);
    disp(['(g_R)/(2*pi)(GHz) = ', num2str(gR_over2pi_GHz,'%E ')]);
  end
end
