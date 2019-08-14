function [data, ax, mini, maxi] = FIS_plot1D()
  [filename, filepath] = uigetfile('*.txt');
  data = load(fullfile(filepath, filename));
  lambda = data(:,1);
  intensity = data(:,2);
  figure();
  plot(lambda, intensity);
end
