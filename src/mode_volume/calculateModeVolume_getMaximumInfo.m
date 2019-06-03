function max_info = calculateModeVolume_getMaximumInfo(data_to_search_for_max, X, Y, Z, epsilon, Emod2, dV)
  
  max_info = struct();
  
  % find maximum
  [max_info.value, max_info.linear_index] = max(data_to_search_for_max(:));
  
  % get maximum location
  max_info.x = X(max_info.linear_index);
  max_info.y = Y(max_info.linear_index);
  max_info.z = Z(max_info.linear_index);
  [max_info.y_index, max_info.x_index, max_info.z_index] = ind2sub(size(X), max_info.linear_index);
  
  % other values at maximum: from datasets
  max_info.epsilon = epsilon(max_info.linear_index);
  max_info.Emod2 = Emod2(max_info.linear_index);
  max_info.dV = dV(max_info.linear_index);
  
  % other values at maximum: computed
  max_info.EnergyDensity = max_info.epsilon .* max_info.Emod2;
  max_info.Energy = max_info.EnergyDensity .* max_info.dV;
  max_info.refractive_index = sqrt(max_info.epsilon);
  
end
