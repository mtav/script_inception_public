function fig = MV_convergence_analysis_function2(filename, doSave, row_selection)
  
  if ~exist('doSave', 'var')
    doSave = false;
  end
  if inoctave() && doSave
    graphics_toolkit('gnuplot');
  end
  
  [datafile_header, datafile_data] = readPrnFile(filename);
  if exist('row_selection', 'var')
    datafile_data = datafile_data(row_selection, :); % skip first row, since it is all zeros normally
    %datafile_data = datafile_data(2:end,:); % skip first row, since it is all zeros normally
  end
  
  if inoctave()
    fig = createFigureIki();
  else
    fig = figure();
  end
  
  subplot_function(datafile_header, datafile_data, 1, 'based on |E|^{2}_{max} - max anywhere', 'info_selection.MaximumEmod2', 'MV_MaximumEmod2_nlocal');
  subplot_function(datafile_header, datafile_data, 2, 'based on (\epsilon|E|^{2})_{max} - max anywhere', 'info_selection.MaximumEnergyDensity', 'MV_MaximumEnergyDensity_nlocal');
  
  subplot_function(datafile_header, datafile_data, 3, 'based on |E|^{2}_{max} - max in defect', 'info_selection_and_defect.MaximumEmod2', 'MV_MaximumEmod2_nlocal_defect');
  subplot_function(datafile_header, datafile_data, 4, 'based on (\epsilon|E|^{2})_{max} - max in defect', 'info_selection_and_defect.MaximumEnergyDensity', 'MV_MaximumEnergyDensity_nlocal_defect');
  
  if doSave
    saveas_fig_and_png(fig, filename, 'saveMethod', 'default', 'FontSize', 5);
  end
  
end

function subplot_function(datafile_header, datafile_data, row_idx, titolo, max_info, MV_info)
  rows = 4;
  cols = 6;
  
  x_labelname = 'Integration volume [\mum^3]';
  x_fieldname = 'info_selection.TotalVolume_Mesh';
  label_options = {'interpreter', 'tex'};
  
  subplot(rows, cols, (row_idx-1)*cols + 1); hold on;
  MV_convergence_plot_function_xy(datafile_header, datafile_data, x_fieldname, [max_info, '.epsilon'], 'b+');
  xlabel(x_labelname, label_options{:});
  ylabel('\epsilon_{r}', label_options{:});
  title(titolo);
  
  subplot(rows, cols, (row_idx-1)*cols + 2); hold on;
  MV_convergence_plot_function_xy(datafile_header, datafile_data, x_fieldname, [max_info, '.Emod2'], 'b+');
  xlabel(x_labelname, label_options{:});
  ylabel('|E|^{2}', label_options{:});
  
  subplot(rows, cols, (row_idx-1)*cols + 3); hold on;
  MV_convergence_plot_function_xy(datafile_header, datafile_data, x_fieldname, [MV_info, '.TotalEnergy'], 'b+');
  xlabel(x_labelname, label_options{:});
  ylabel('Total energy', label_options{:});
  
  subplot(rows, cols, (row_idx-1)*cols + 4); hold on;
  MV_convergence_plot_function_xy(datafile_header, datafile_data, x_fieldname, [MV_info, '.MaximumEnergyDensity'], 'b+');
  xlabel(x_labelname, label_options{:});
  ylabel('(\epsilon|E|^{2})_{max}', label_options{:});
  
  subplot(rows, cols, (row_idx-1)*cols + 5); hold on;
  MV_convergence_plot_function_xy(datafile_header, datafile_data, x_fieldname, [MV_info, '.mode_volume_mum3'], 'b+');
  xlabel(x_labelname, label_options{:});
  ylabel('V_{eff} [\mum^{3}]', label_options{:});
  
  subplot(rows, cols, (row_idx-1)*cols + 6); hold on;
  MV_convergence_plot_function_xy(datafile_header, datafile_data, x_fieldname, [MV_info, '.normalized_mode_volume_1'], 'b+');
  xlabel(x_labelname, label_options{:});
  ylabel('V_{eff}/(\lambda/n)^{3}', label_options{:});
  
end
