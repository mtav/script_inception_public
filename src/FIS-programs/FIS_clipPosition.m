function data = FIS_clipPosition(data, min_val, max_val)
  %%% function data = FIS_clipPosition(data, min_val, max_val)
  %%% Clips the data so that the position only goes from min_val to max_val.

  %%% get closest index values
  min_idx = closestInd(data.Position(1,:), min_val);
  max_idx = closestInd(data.Position(1,:), max_val);

  %%% clip data
  data.Position = data.Position(:, min_idx:max_idx);
  data.Lambda = data.Lambda(:, min_idx:max_idx);
  data.Intensity = data.Intensity(:, min_idx:max_idx);

  %%% Update angles
  if isfield(data, 'metadata') && isfield(data.metadata, 'calibration')
    centro = data.metadata.calibration.x.centre;
    factor = data.metadata.calibration.x.degrees_per_mm;
    bool_trigonometric_mode = data.metadata.calibration.x.bool_trigonometric_mode;
    data.AngleDegrees = FIS_PositionToAngle(data.Position, centro, factor, bool_trigonometric_mode);
    data.metadata.PositionToAngle = @(x) FIS_PositionToAngle(x, centro, factor, bool_trigonometric_mode);
  end
end
