function data = FIS_addCalibrationNonTrigonometric(data, centre, degrees_per_mm)
  % function data = FIS_addCalibrationNonTrigonometric(data, centre, degrees_per_mm)
  % Basic function to fill in the metadata information used for conversion to angles.
  data.metadata.calibration.x.centre = centre; % normal incidence position in mm
  data.metadata.calibration.x.degrees_per_mm = degrees_per_mm; % degrees/mm value
  data.metadata.calibration.x.bool_trigonometric_mode = false; % true/false
end
