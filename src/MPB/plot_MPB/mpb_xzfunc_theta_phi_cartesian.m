function [x, z, x_label, z_label] = mpb_xzfunc_theta_phi_cartesian(data, pos, data_info)
  x_label = 'theta (rad)';
  z_label = 'phi (rad)';
  
  if ~exist('pos', 'var'); pos=[]; end;
  
  % first get the coordinates in the reciprocal lattice k1,k2,k3
  if isempty(pos)
    k1 = data(:, 2);
    k2 = data(:, 3);
    k3 = data(:, 4);
  else
    k1 = data(pos, 2);
    k2 = data(pos, 3);
    k3 = data(pos, 4);
  end
  
  k1 = k1(:)';
  k2 = k2(:)';
  k3 = k3(:)';
  
  k_reciprocal = [k1;k2;k3];
  
  M = data_info.reciprocal_to_cartesian;
  
  k_cartesian = M*k_reciprocal;
  
  k_cartesian_x = k_cartesian(1,:);
  k_cartesian_y = k_cartesian(2,:);
  k_cartesian_z = k_cartesian(3,:);
  
  [azimuth, elevation, r] = cart2sph(k_cartesian_x, k_cartesian_y, k_cartesian_z);
  
  theta = pi/2 - elevation;
  phi = azimuth;
  
  x = theta;
  z = phi;
end
