function y = omega_fixed_angle(angle_rad, kxn, n1, n_average)
  y = 2*n_average/n1 * sqrt( 1 + (1/tan(angle_rad))^2 ) * abs(kxn);
end
