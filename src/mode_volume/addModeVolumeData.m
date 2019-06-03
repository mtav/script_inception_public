function ret = addModeVolumeData(ret)
  idx_material = find(strcmpi('material', ret.data.header));
  idx_Exmod = find(strcmpi('Exmod', ret.data.header));
  idx_Eymod = find(strcmpi('Eymod', ret.data.header));
  idx_Ezmod = find(strcmpi('Ezmod', ret.data.header));
  
  %ret.data.material = ret.data.D(:,:,:, idx_material);
  ret.data.Emod2 = ret.data.D(:,:,:, idx_Exmod).^2 + ret.data.D(:,:,:, idx_Eymod).^2 + ret.data.D(:,:,:, idx_Ezmod).^2;
  %ret.data.EnergyDensity = ret.data.material .* ret.data.Emod2;
  ret.data.EnergyDensity = ret.data.D(:,:,:, idx_material) .* ret.data.Emod2;
end
