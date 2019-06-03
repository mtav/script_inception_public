% file to load oscillator properties for use with calculateCouplingStrengthTable()

% nos: refractive index of the oscillator, dimensionless
% lambda (nm): wavelength of the oscillator, in nm
% gamma/(2*pi) (GHz): radial frequency (=2pi/(spontaneous emission lifetime)), in GHz
% deg (C*m): Dipole moment of the oscillator, in Coul*m
% feg (no unit): oscillator strength, dimensionless (will be calculated using get_feg() if missing)

oscillator_properties_quantumdot_nofeg = struct()
oscillator_properties_quantumdot_nofeg.nos = 3.55
oscillator_properties_quantumdot_nofeg.lambda_nm = 940
oscillator_properties_quantumdot_nofeg.gamma_over_2pi_GHz = [1]
oscillator_properties_quantumdot_nofeg.deg_Cm = 9.11E-029

oscillator_properties_quantumdot_fixedfeg = struct()
oscillator_properties_quantumdot_fixedfeg.nos = 3.55
oscillator_properties_quantumdot_fixedfeg.lambda_nm = 940
oscillator_properties_quantumdot_fixedfeg.gamma_over_2pi_GHz = [1]
oscillator_properties_quantumdot_fixedfeg.deg_Cm = 9.11E-029
oscillator_properties_quantumdot_fixedfeg.feg = 10

oscillator_properties_NVcentre_nofeg = struct()
oscillator_properties_NVcentre_nofeg.nos = 2.4
oscillator_properties_NVcentre_nofeg.lambda_nm = 637
oscillator_properties_NVcentre_nofeg.gamma_over_2pi_GHz = [8.33E-002, 3.30E-003]
oscillator_properties_NVcentre_nofeg.deg_Cm = 3.57E-030
