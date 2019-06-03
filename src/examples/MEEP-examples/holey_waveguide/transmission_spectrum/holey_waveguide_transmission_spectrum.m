function holey_waveguide_transmission_spectrum(N_range, doSave, x_is_wavelength, scale_factor, save_base)
  
  if ~exist('N_range', 'var')
    N_range = 0:16;
  end
  if ~exist('doSave', 'var')
    doSave = false;
  end
  if ~exist('x_is_wavelength', 'var')
    x_is_wavelength = false;
  end
  if ~exist('scale_factor', 'var')
    scale_factor = 1;
  end
  
  close all;
  
  reference_file = sprintf('holey_waveguide_transmission_spectrum.N=%02d.dat', 0);
  reference_file_raw_data = dlmread(reference_file,',',0,1);
  
  for N = N_range
    geometry_base = sprintf('holey_waveguide_transmission_spectrum.N=%02d', N);
    geometry_file  = [geometry_base, '.dat'];
    
    %    system(['grep flux1: holey_waveguide_transmission_spectrum.0.out > ', reference_file]);
    %    system(['grep flux1: holey_waveguide_transmission_spectrum.out > '  , geometry_file ]);
    
    geometry_file_raw_data = dlmread(geometry_file,',',0,1);
    
    fig = figure();
    freq = geometry_file_raw_data(:,1);
    transmission = geometry_file_raw_data(:,2) ./ reference_file_raw_data(:,2);
    
    if x_is_wavelength
      x = scale_factor .* 1 ./ freq;
      x_label_text = 'Wavelength';
    else
      x = scale_factor .* freq;
      x_label_text = 'Frequency';
    end
    
    plot( x, transmission, 'b.-');
    grid on;
    axis([min(x(:)), max(x(:)), 0, max(transmission(:))]);
    xlabel(x_label_text);
    ylabel('transmission');
    title(geometry_file, 'interpreter', 'none');
    
    if doSave
      if ~exist('save_base', 'var')
        save_base = geometry_base;
      end
      saveas (fig, [save_base, '.png']);
    end
    
  end
end
