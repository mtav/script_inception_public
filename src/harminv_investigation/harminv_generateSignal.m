function harminv_generateSignal(outfile, Npoints, timestep, freq, decay)
%function [freq_list, decay_list] = harminv_generateSignal(outfile, Npoints, timestep, omega)
  freq_str = ''
  %freq_list = [];
  %decay_list = [];
  %for idx = 1:length(omega)
  for idx = 1:length(freq)
    if idx > 1
      freq_str = [freq_str, ' '];
    end
    %freq = real(omega(idx))./(2*pi);
    %decay = -imag(omega(idx));
    freq_str = [freq_str, sprintf("%f+%fi", freq(idx), decay(idx))];
    %freq_list = [freq_list, freq];
    %decay_list = [decay_list, decay];
  end
  cmd = sprintf('sines -r -n%d -t%E %s > %s', Npoints, timestep, freq_str, outfile)
  system(cmd);
  
  %freq_list
  %min(freq_list)
  %max(freq_list)
  %omega = 2*pi*freq - I*decay;
  %u = exp(-I*timestep*omega);
  %phi = arg(u);
  
end
