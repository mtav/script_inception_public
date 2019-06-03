% plots MV results for different integration radiuses
function MV_vs_integration_radius(rmin, rmax, N)
  
  radius_list = linspace(rmin, rmax, N);
  
  TotalEnergy_list_calculated = zeros(size(radius_list));
  mode_volume_mum3_list_calculated = zeros(size(radius_list));
  Vn1_list_calculated = zeros(size(radius_list));
  eps_list_calculated = zeros(size(radius_list));
  Emax_list_calculated = zeros(size(radius_list));
  x_list_calculated = zeros(size(radius_list));
  y_list_calculated = zeros(size(radius_list));
  z_list_calculated = zeros(size(radius_list));
  
  for idx = 1:length(radius_list)
  
    ret = calculateModeVolume({'RCD111.inp', '../../epsilon/RCD111.inp'}, 'integration_sphere', [6.216506E+00, 6.216506E+00, 6.216506E+00, radius_list(idx)], 'numID_list', 1:95, 'justCheck', false, 'eps_folder', '../../epsilon/', 'snap_plane', 'x', 'refractive_index_defect', 1);
    
    TotalEnergy_list_calculated(idx) = ret.TotalEnergy;
    mode_volume_mum3_list_calculated(idx) = ret.mode_volume_mum3;
    Vn1_list_calculated(idx) = ret.normalized_mode_volume_1;
    eps_list_calculated(idx) = ret.MaximumEnergyDensity.epsilon;
    
    Emax_list_calculated(idx) = ret.MaximumEnergyDensity.value;
    x_list_calculated(idx) = ret.MaximumEnergyDensity.x;
    y_list_calculated(idx) = ret.MaximumEnergyDensity.y;
    z_list_calculated(idx) = ret.MaximumEnergyDensity.z;

  end

  figure;
  subplot(2,2,1);
  hold on;
  plot(radius_list, mode_volume_mum3_list_calculated, 'ro');
  ylabel('mode_volume_mum3', 'interpreter', 'None');
  xlabel('integration radius');

  subplot(2,2,2);
  hold on;
  plot(radius_list, TotalEnergy_list_calculated, 'ro');
  ylabel('TotalEnergy', 'interpreter', 'None');
  xlabel('integration radius');

  subplot(2,2,3);
  hold on;
  plot(radius_list, Vn1_list_calculated, 'ro');
  ylabel('Vn1', 'interpreter', 'None');
  xlabel('integration radius');

  subplot(2,2,4);
  hold on;
  plot(radius_list, eps_list_calculated, 'ro');
  ylabel('epsilon', 'interpreter', 'None');
  xlabel('integration radius');

  saveas_fig_and_png(gcf, 'MVstudy-part1');

  figure;
  subplot(2,2,1);
  hold on;
  plot(radius_list, Emax_list_calculated, 'ro');
  ylabel('Emax_list_calculated', 'interpreter', 'None');
  xlabel('integration radius');

  subplot(2,2,2);
  hold on;
  plot(radius_list, x_list_calculated, 'ro');
  ylabel('x_list_calculated', 'interpreter', 'None');
  xlabel('integration radius');

  subplot(2,2,3);
  hold on;
  plot(radius_list, y_list_calculated, 'ro');
  ylabel('y_list_calculated', 'interpreter', 'None');
  xlabel('integration radius');

  subplot(2,2,4);
  hold on;
  plot(radius_list, z_list_calculated, 'ro');
  ylabel('z_list_calculated', 'interpreter', 'None');
  xlabel('integration radius');
  
  saveas_fig_and_png(gcf, 'MVstudy-part2');

end
