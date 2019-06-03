close all;
clear all;

Nlist = 2:16;
frequency_list = [];
Q_list = [];

for N = Nlist
  infile = sprintf('holey_waveguide_resonant_modes.N=%02d.csv', N);
  fprintf('infile = %s\n', infile);
%    data = dlmread(infile, ',', 1, 1);
  [header, data] = readPrnFile(infile, NaN, NaN, ',');
  frequency = data(:, 2);
  Q = data(:, 4);
  [linear_indices, values, abs_err, sub_indices, minerr] = closestInd(frequency, 0.23)
  frequency_list(end+1) = frequency(linear_indices(1));
  Q_list(end+1) = Q(linear_indices(1));
end

semilogy(Nlist, Q_list, 'bo-');
xlabel('N (# layers)');
ylabel('Q');

saveas(gcf, 'holey_waveguide_resonant_modes_Qfactors.png');
