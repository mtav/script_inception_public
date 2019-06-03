function info = calculateModeVolume_getFundamentalInfo(X, Y, Z, epsilon, Emod2, dV)
  % input: epsilon, Emod2, dV datasets
  % output:
  %   -TotalEnergy
  %   -TotalVolume_AvailableData
  %   -TotalVolume_Mesh
  %   -MaximumEmod2
  %   -MaximumEnergyDensity
  %
  % with Maximum* containing the following info:
  %   --value
  %   --linear_index
  %   --x, y, z
  %   --x_index, y_index, z_index
  %   --epsilon
  %   --refractive_index
  %   --Emod2
  %   --EnergyDensity
  %
  % TODO: add energy fraction info
  
  ret = struct();
  
  EnergyDensity = epsilon .* Emod2;
  Energy = EnergyDensity .* dV;
  
  % integrate over whole volume
  nonzeros_idx = find(epsilon.*Emod2);
  info.TotalVolume_AvailableData = sum(dV(nonzeros_idx));
  info.TotalVolume_Mesh = sum(dV(:));
  info.TotalEnergy = sum(Energy(:));
  
  % get maxima info
  info.MaximumEmod2 = calculateModeVolume_getMaximumInfo(Emod2, X, Y, Z, epsilon, Emod2, dV);
  info.MaximumEnergyDensity = calculateModeVolume_getMaximumInfo(EnergyDensity, X, Y, Z, epsilon, Emod2, dV);
  
end
