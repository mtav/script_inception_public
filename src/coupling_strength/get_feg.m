function feg = get_feg(lambda_nm, deg_Cm)
  % function feg = get_feg(lambda_nm, deg_Cm)
  % returns the oscillator strength "feg" (dimensionless)
  % lambda_nm : oscillator wavelength in nm
  % deg_Cm : Dipole moment of the oscillator in Coul*m, usually named "mu" or "deg"
  
  feg = (2*get_me()*(2*pi*get_c0()/(lambda_nm*1e-9))*deg_Cm^2)/(get_e()^2*get_hb());

end
