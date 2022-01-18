function data = FIS_clipWavelength(data, min_val, max_val)
  %%% function data = FIS_clipWavelength(data, min_val, max_val)
  %%% Clips the data so that the wavelength only goes from min_val to max_val.

  %%% get closest index values
  min_idx = closestInd(data.Lambda(:,1), min_val);
  max_idx = closestInd(data.Lambda(:,1), max_val);

  %%% clip data
  data.Position = data.Position(min_idx:max_idx, :);
  data.Lambda = data.Lambda(min_idx:max_idx, :);
  data.Intensity = data.Intensity(min_idx:max_idx, :);
end
