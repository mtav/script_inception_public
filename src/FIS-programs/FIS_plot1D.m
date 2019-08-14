function [data, ax, mini, maxi] = FIS_plot1D()
  [filename, filepath] = uigetfile('*.txt');
  data = load(fullfile(filepath, filename));
  lambda = data(:,1);
  intensity = data(:,2);
  figure();
  ax = axes();
  plot(lambda, intensity);

  mini = min(intensity(:));
  maxi = max(intensity(:));
  if maxi >= 65535
    warning('Saturated signal: maxi = %d', maxi);
  end
end
