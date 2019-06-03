function ret = createMVstruct(TotalEnergy, MaximumEnergyDensity, wavelength_mum, refractive_index_defect)

  if ~exist('TotalEnergy', 'var'); TotalEnergy = NaN; end;
  if ~exist('MaximumEnergyDensity', 'var'); MaximumEnergyDensity = NaN; end;
  if ~exist('wavelength_mum', 'var'); wavelength_mum = NaN; end;
  if ~exist('refractive_index_defect', 'var'); refractive_index_defect = NaN; end;
  
  ret = struct();
  
  ret.TotalEnergy = TotalEnergy;
  ret.MaximumEnergyDensity = MaximumEnergyDensity;
  
  if MaximumEnergyDensity ~= 0
    ret.mode_volume_mum3 = TotalEnergy ./ MaximumEnergyDensity;
  else
    ret.mode_volume_mum3 = NaN;
  end
  
  ret.wavelength_mum = wavelength_mum;
  ret.refractive_index_defect = refractive_index_defect;
  
  ret.mode_length_mum = ret.mode_volume_mum3^(1/3);
  
  if ret.refractive_index_defect ~= 0
    ret.normalization_length_1_mum = ret.wavelength_mum / ret.refractive_index_defect;
    ret.normalization_length_2_mum = ret.wavelength_mum / (2*ret.refractive_index_defect);
  else
    ret.normalization_length_1_mum = NaN;
    ret.normalization_length_2_mum = NaN;
  end
  
  ret.normalization_volume_1_mum3 = ret.normalization_length_1_mum^3;
  
  ret.normalized_mode_volume_1 = ret.mode_volume_mum3 / ret.normalization_volume_1_mum3;
  
  ret.normalized_mode_length_1 = ret.normalized_mode_volume_1^(1/3);
  
  
  ret.normalization_volume_2_mum3 = ret.normalization_length_2_mum^3;
  
  ret.normalized_mode_volume_2 = ret.mode_volume_mum3 / ret.normalization_volume_2_mum3;
  
  ret.normalized_mode_length_2 = ret.normalized_mode_volume_2^(1/3);
end
