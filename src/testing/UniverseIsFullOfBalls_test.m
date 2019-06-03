% Script to validate integration volume restriction, based on the UniverseIsFullOfBalls sampling function.

function UniverseIsFullOfBalls_test(centre, energy_inside, energy_outside)

  radius_max = 1;
  
  radius_list = linspace(0, 1.5, 16);
  %radius_list = [0.5,1,1.5];
  %radius_list = [0.1, 0.2, 0.3];
  
  TotalEnergy_list_calculated = zeros(size(radius_list));
  mode_volume_mum3_list_calculated = zeros(size(radius_list));

  TotalEnergy_list_theory = zeros(size(radius_list));
  mode_volume_mum3_list_theory = zeros(size(radius_list));
  
  %TotalEnergy_list_theory = (4/3)*pi*(radius_list.^3)*energy_inside;
  %mode_volume_mum3_list_theory = (4/3)*pi*(radius_list.^3);

  for idx = 1:length(radius_list)
  
    ret = calculateModeVolume({'sim.inp'}, 'integration_sphere', [centre, radius_list(idx)]);
    TotalEnergy_list_calculated(idx) = ret.TotalEnergy;
    mode_volume_mum3_list_calculated(idx) = ret.mode_volume_mum3;
    
    if radius_list(idx) <= radius_max
      TotalEnergy_list_theory(idx) = (4/3)*pi*(radius_list(idx).^3)*energy_inside;
      mode_volume_mum3_list_theory(idx) = TotalEnergy_list_theory(idx) / energy_inside;
    else
      TotalEnergy_list_theory(idx) = (4/3)*pi*(radius_list(idx).^3)*energy_outside + (4/3)*pi*(radius_max.^3)*(energy_inside-energy_outside);
      mode_volume_mum3_list_theory(idx) = TotalEnergy_list_theory(idx) / max([energy_inside, energy_outside]);
    end
    
  end

  
  prefix = sprintf('centre = [%.1f %.1f %.1f], energy_inside = %.1f, energy_outside = %.1f', centre, energy_inside, energy_outside);

  subplot(2,1,1);
  hold on;
  plot(radius_list, mode_volume_mum3_list_calculated, 'ro');
  plot(radius_list, mode_volume_mum3_list_theory, 'b-');
  title([prefix, ' - mode_volume_mum3'], 'interpreter', 'None');
  legend('calculated', 'theory', 'Location', 'northwest');

  subplot(2,1,2);
  hold on;
  plot(radius_list, TotalEnergy_list_calculated, 'ro');
  plot(radius_list, TotalEnergy_list_theory, 'b-');
  title([prefix, ' - TotalEnergy'], 'interpreter', 'None');
  legend('calculated', 'theory', 'Location', 'northwest');

end
