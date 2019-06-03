function [ frequency, transmission_normalized, reflection_normalized, loss, reference_file_raw_data, geometry_file_raw_data ] = getNormalizedTRLvalues(reference_file, geometry_file, preprocessed_flux, bool_normalize_by_reference_input)
  
  reference_file_raw_data = dlmread(reference_file,',',0,1);
  reference_frequency        = reference_file_raw_data(:, 1);
  reference_transmitted_flux = reference_file_raw_data(:, 2);
  reference_reflected_flux   = reference_file_raw_data(:, 3);
  
  geometry_file_raw_data  = dlmread(geometry_file,',',0,1);
  geometry_frequency        = geometry_file_raw_data(:, 1);
  geometry_transmitted_flux = geometry_file_raw_data(:, 2);
  geometry_reflected_flux   = geometry_file_raw_data(:, 3);
  
  frequency = geometry_frequency;
  
  if bool_normalize_by_reference_input
    total = reference_reflected_flux;
  else
    total = reference_transmitted_flux;
  end
  
  % incident_flux = reference_file_raw_data(:, 2);
  % incident_flux = reference_file_raw_data(:, 3);
  % total = transmitted_flux - reflected_flux;
  % reflection_normalized = -reflected_flux./total;
  
  transmission_normalized = geometry_transmitted_flux./total;
  
  if preprocessed_flux % if load-minus-flux/save-flux is used:
    reflection_normalized = -geometry_reflected_flux./total;
  else
    reflection_normalized = -(geometry_reflected_flux - reference_reflected_flux)./total;
  end
  
  loss = 1 - transmission_normalized - reflection_normalized;
  
end
