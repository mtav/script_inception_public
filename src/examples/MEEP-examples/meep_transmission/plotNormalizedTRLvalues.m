function ret = plotNormalizedTRLvalues(reference_file, geometry_file, preprocessed_flux, x_is_wavelength, scale_factor, bool_normalize_by_reference_input)
  
  ret = struct();
  
  [ ret.frequency, ret.transmission_normalized, ret.reflection_normalized, ret.loss ] = getNormalizedTRLvalues(reference_file, geometry_file, preprocessed_flux, bool_normalize_by_reference_input);
  hold on;
  
  if x_is_wavelength
    x = scale_factor .* 1 ./ ret.frequency;
    x_label_text = 'Wavelength';
  else
    x = scale_factor .* ret.frequency;
    x_label_text = 'Frequency';
  end
  
  %plot(x, ret.transmission_normalized, 'bo');
  %plot(x, ret.reflection_normalized, 'ro');
  plot(x, ret.loss, 'k-');
  plot(x, ret.transmission_normalized, 'b-');
  plot(x, ret.reflection_normalized, 'r--');
  
  xlabel(x_label_text);
  ylabel('Transmission and Reflection (no unit)');
  legend('MEEP transmission','MEEP reflection','MEEP loss');
  %legend('transmission','reflection','MEEP loss');
  title(geometry_file, 'interpreter', 'none');

end
