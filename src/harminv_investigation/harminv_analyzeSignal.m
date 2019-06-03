function [f,decay,Q,amp,phase,err] = harminv_analyzeSignal(infile, timestep, start_freq, stop_freq)
  timeseries = dlmread(infile);
  
  %f = real(omega(:))/(2*pi);
  
  %f_range = max(f) - min(f);
  %f_mid = (max(f) + min(f))/2;
  
  %start_freq = f_mid - f_range
  %stop_freq = f_mid + f_range
  
  [f,decay,Q,amp,phase,err] = harminv2( timeseries, timestep, start_freq, stop_freq );
end
