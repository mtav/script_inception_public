function fig = MV_convergence_analysis_function(filename, doSave)

  [datafile_header, datafile_data] = readPrnFile(filename);

  idx_TotalMeshVolume = find(strcmpi('TotalMeshVolume', datafile_header));

  idx_MaxE2.epsilon = find(strcmpi('MaxE2.epsilon', datafile_header));
  idx_MaxE2.value = find(strcmpi('MaxE2.value', datafile_header));
  idx_MaxE2_nlocal.Veff = find(strcmpi('MaxE2_nlocal.Veff', datafile_header));

  idx_MaxEnergy.epsilon = find(strcmpi('MaxEnergy.epsilon', datafile_header));
  idx_MaxEnergy.value = find(strcmpi('MaxEnergy.value', datafile_header));
  idx_MaxEnergy_nlocal.Veff = find(strcmpi('MaxEnergy_nlocal.Veff', datafile_header));

  fig = figure;

  rows = 3;
  cols = 2;

  subplot(rows, cols, 1); hold on;
  plot(datafile_data(:, idx_TotalMeshVolume), datafile_data(:, idx_MaxE2.epsilon), 'b+');
  xlabel('Integration volume [\mum^3]');
  ylabel('\epsilon_{r} at max [no unit]');
  title('based on |E|^{2}_{max}');

  subplot(rows, cols, 3); hold on;
  plot(datafile_data(:, idx_TotalMeshVolume), datafile_data(:, idx_MaxE2.value), 'b+');
  xlabel('Integration volume [\mum^3]');
  ylabel('|E|^{2}_{max} [(V/m)^2]');

  subplot(rows, cols, 5); hold on;
  plot(datafile_data(:, idx_TotalMeshVolume), datafile_data(:, idx_MaxE2_nlocal.Veff), 'b+');
  xlabel('Integration volume [\mum^3]');
  ylabel('Veff [\mum^3]');

  subplot(rows, cols, 2); hold on;
  plot(datafile_data(:, idx_TotalMeshVolume), datafile_data(:, idx_MaxEnergy.epsilon), 'b+');
  xlabel('Integration volume [\mum^3]');
  ylabel('\epsilon_{r} at max [no unit]');
  title('based on (\epsilon|E|^{2})_{max}');

  subplot(rows, cols, 4); hold on;
  plot(datafile_data(:, idx_TotalMeshVolume), datafile_data(:, idx_MaxEnergy.value), 'b+');
  xlabel('Integration volume [\mum^3]');
  ylabel('(\epsilon|E|^{2})_{max} [(V/m)^2]');

  subplot(rows, cols, 6); hold on;
  plot(datafile_data(:, idx_TotalMeshVolume), datafile_data(:, idx_MaxEnergy_nlocal.Veff), 'b+');
  xlabel('Integration volume [\mum^3]');
  ylabel('Veff [\mum^3]');

  if doSave
    saveas_fig_and_png(fig, filename, 'saveMethod', 'gnuplot', 'FontSize', 8);
  end
 
end
