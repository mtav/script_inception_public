function [x_ret, y_ret, z_ret, params, energy_min_real, energy_max_real] = thesis_plotPillarSnapshots_function(fx, ex, fy, ey, fz, ez, excitation_location, freq, dirtype, Y2_size, test_mode, column_to_plot, colorbar_label, figure_basename, log_norm_abs)
  
  % defaults
  x_ret = NaN;
  y_ret = NaN;
  z_ret = NaN;
  params = NaN;
  
  % close any existing figures
  if ~test_mode
    close all;
  end
  
  excitation_location
  sprintf('%s %s %s %s %s %s', fx, ex, fy, ey, fz, ez)
  x_energy = [fx, '_energy.prn']
  y_energy = [fy, '_energy.prn']
  z_energy = [fz, '_energy.prn']
  x_epsilon = [ex, '.prn']
  y_epsilon = [ey, '.prn']
  z_epsilon = [ez, '.prn']
  freq
  dirtype

  %% new system
  %ret_energy = thesis_readPrnFiles(x_energy, y_energy, z_energy, dirtype);
  %ret_epsilon = thesis_readPrnFiles(x_epsilon, y_epsilon, z_epsilon, dirtype);

  %% create single snapshots
  %% X
  %[fig, w_fig_cm, h_fig_cm] = thesis_figure(1);
  %thesis_surfWithContour(ret_energy.x, ret_epsilon.x, column_to_plot, colorbar_label);
  %% Y
  %[fig, w_fig_cm, h_fig_cm] = thesis_figure(1);
  %thesis_surfWithContour(ret_energy.y, ret_epsilon.y, column_to_plot, colorbar_label);
  %% Z
  %[fig, w_fig_cm, h_fig_cm] = thesis_figure(1);
  %thesis_surfWithContour(ret_energy.z, ret_epsilon.z, column_to_plot, colorbar_label);
  
  %return
  
  [x_header, x_data, x_u1, x_u2] = readPrnFile(x_energy, 'includeAllColumns', true);
  [y_header, y_data, y_u1, y_u2] = readPrnFile(y_energy, 'includeAllColumns', true);
  [z_header, z_data, z_u1, z_u2] = readPrnFile(z_energy, 'includeAllColumns', true);
  [x_U1, x_U2] = meshgrid(x_u1, x_u2);
  [y_U1, y_U2] = meshgrid(y_u1, y_u2);
  [z_U1, z_U2] = meshgrid(z_u1, z_u2);
  
  x_data = x_data(:,:,column_to_plot);
  y_data = y_data(:,:,column_to_plot);
  z_data = z_data(:,:,column_to_plot);
  data = [x_data(:); y_data(:); z_data(:)];
  
  if log_norm_abs
    data = abs(data);
    data = data ./ max(abs(data(:)));
    data = log10(data);
  end
  energy_min_real = min(data(:))
  energy_max_real = max(data(:))

  energy_min = energy_min_real;
  energy_max = energy_max_real;

  % special caxis hack...
  if log_norm_abs
    if column_to_plot==5
      % Emod2
      energy_min = -10;
      energy_max = 0;
    elseif column_to_plot==3
      % energy
      energy_min = -11;
      energy_max = 0;
    else
      error('should not happen');
    end
    %if dirtype == 1
      %disp('pass');
    %elseif dirtype == 2
      %energy_min = -10;
      %energy_max = 0;
    %else
      %energy_min = -10;
      %energy_max = 0;
    %end
  end

  [fig, w_fig_cm, h_fig_cm] = thesis_figure(1);

  common_options_special = {'column', column_to_plot, ...
    'createFigure', false, ...
    'drawTitle', false, ...
    'modulus', log_norm_abs, ...
    'normalized', log_norm_abs, ...
    'log10', log_norm_abs, ...
    'saveas', false, ...
    'drawColorBar', true ...
    'colorbarPosition', 'SouthOutside', ...
    };

  % additional non-zoomed longitudinal plot
  if dirtype == 1
    ret_special = plotSnapshot('filename', y_energy, 'contourFile', y_epsilon, 'swap_axes', true, common_options_special{:});
  elseif dirtype == 2
    ret_special = plotSnapshot('filename', y_energy, 'contourFile', y_epsilon, 'swap_axes', true, common_options_special{:});
  else
    ret_special = plotSnapshot('filename', x_energy, 'contourFile', x_epsilon, 'swap_axes', true, common_options_special{:});
  end
  caxis([energy_min, energy_max]);
  xlabel('x (\mum)');
  ylabel('z (\mum)');

  xlabel(ret_special.handle_colorbar, colorbar_label);
  if ~test_mode
    saveas_fig_and_png(fig, [figure_basename, '_single']);
  end
  STOP
  
  %return
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  
  bool_save_x = false;
  bool_save_y = false;
  bool_save_z = false;
  %bool_save_x = 'energy_x';
  %bool_save_y = 'energy_y';
  %bool_save_z = 'energy_z';
  
  drawColorBar = false;
  drawTitle = false;
  createFigure = false;

  common_options = {'column', column_to_plot, ...
    'createFigure', createFigure, ...
    'drawTitle', drawTitle, ...
    'modulus', log_norm_abs, ...
    'normalized', log_norm_abs, ...
    'log10', log_norm_abs};
  
  [fig, w_fig_cm, h_fig_cm] = thesis_figure(2);
  
  %xc = 0.4;
  %yc = 0.5;
  %b = 0.01;
  %positionVector1 = [b, b, xc-1.5*b, 1-2*b];
  %positionVector2 = [xc+0.5*b, yc+0.5*b, (1-xc)-1.5*b, (1-yc)-1.5*b];
  %positionVector3 = [xc+0.5*b, b, (1-xc)-1.5*b, yc-1.5*b];
  
  V=2;
  H=3;
  subplot(V,H,[1,1+H]);
  %  subplot('Position',positionVector1)
  if dirtype == 1
    x_ret = plotSnapshot('filename', x_energy, 'contourFile', x_epsilon, 'saveas', bool_save_x, 'drawColorBar', true, 'colorbarPosition', 'SouthOutside', 'swap_axes', true, common_options{:});
  elseif dirtype == 2
    x_ret = plotSnapshot('filename', x_energy, 'contourFile', x_epsilon, 'saveas', bool_save_x, 'drawColorBar', true, 'colorbarPosition', 'SouthOutside', 'swap_axes', true, common_options{:});
  else
    x_ret = plotSnapshot('filename', y_energy, 'contourFile', y_epsilon, 'saveas', bool_save_y, 'drawColorBar', true, 'colorbarPosition', 'SouthOutside', 'swap_axes', true, common_options{:});
  end
  %  title('(a)') %, 'Position', [0.5,-1], 'Units', 'normalized');
  caxis([energy_min, energy_max]);
  
  xlabel(x_ret.handle_colorbar, colorbar_label);
  
  subplot(V,H,[2,H]);
  %  subplot('Position',positionVector2)
  if dirtype == 1
    y_ret = plotSnapshot('filename', y_energy, 'contourFile', y_epsilon, 'saveas', bool_save_y, 'drawColorBar', drawColorBar, 'swap_axes', true, common_options{:});
  elseif dirtype == 2
    y_ret = plotSnapshot('filename', y_energy, 'contourFile', y_epsilon, 'saveas', bool_save_y, 'drawColorBar', drawColorBar, 'swap_axes', true, common_options{:});
  else
    y_ret = plotSnapshot('filename', x_energy, 'contourFile', x_epsilon, 'saveas', bool_save_x, 'drawColorBar', drawColorBar, 'swap_axes', true, common_options{:});
  end
  %  title('(b)') %, 'Position', [0.5,-1], 'Units', 'normalized');
  caxis([energy_min, energy_max]);
  
  subplot(V,H,[2,H]+H);
  %  subplot('Position',positionVector3)
  if dirtype == 1
    z_ret = plotSnapshot('filename', z_energy, 'contourFile', z_epsilon, 'saveas', bool_save_z, 'drawColorBar', drawColorBar, common_options{:});
  elseif dirtype == 2
    z_ret = plotSnapshot('filename', z_energy, 'contourFile', z_epsilon, 'saveas', bool_save_z, 'drawColorBar', drawColorBar, common_options{:});
  else
    z_ret = plotSnapshot('filename', z_energy, 'contourFile', z_epsilon, 'saveas', bool_save_z, 'drawColorBar', drawColorBar, 'swap_axes', true, common_options{:});
  end
  %  title('(c)') %, 'Position', [0.5,-1], 'Units', 'normalized');
  caxis([energy_min, energy_max]);
  
  params = struct();
  
  params.figure_handle = fig;
  params.w_fig_cm = w_fig_cm;
  params.h_fig_cm = h_fig_cm;
  
  params.handle_colorbar = x_ret.handle_colorbar;

  params.plot_1.handle = x_ret.handle_axis;
  if dirtype == 1
    params.plot_1.X = x_ret.handles.data_reshaped.XData;
    %params.plot_1.Y = x_ret.handles.data_reshaped.YData;
    params.plot_1.anchor_data = [excitation_location(2), excitation_location(3)];
  elseif dirtype == 2
    params.plot_1.X = [x_ret.handles.data_reshaped.XData(1,1), excitation_location(2)];
    %params.plot_1.Y = x_ret.handles.data_reshaped.YData;
    params.plot_1.anchor_data = [excitation_location(2), excitation_location(3)];
    %params.plot_1.X = [0,1.4];
    %x1max = ceil(size(x_ret.handles.data_reshaped.XData, 2)/2);
    %params.plot_1.X = x_ret.handles.data_reshaped.XData(:, 1:x1max);
    %params.plot_1.X = x_ret.handles.data_reshaped.XData;
    %close all;
    %imagesc(params.plot_1.X);
    %STOP
  else
    params.plot_1.X = x_ret.handles.data_reshaped.XData;
    %params.plot_1.Y = x_ret.handles.data_reshaped.YData;
    params.plot_1.anchor_data = [excitation_location(1), excitation_location(3)];
  end
  params.plot_1.Y = [params.plot_1.anchor_data(2)-Y2_size/2, params.plot_1.anchor_data(2)+Y2_size/2];
  params.plot_1.anchor_window = [0.5, 0];
  params.plot_1.relative_data_coordinates = false;
  params.plot_1.forced_limit = 'y';
  
  %getRange(params.plot_1.Y)
  %getRange(params.plot_1.X)

  params.plot_2.handle = y_ret.handle_axis;
  params.plot_2.X = y_ret.handles.data_reshaped.YData;
  if dirtype == 1
    params.plot_2.anchor_data = [excitation_location(1), excitation_location(3)];
    %params.plot_2.Y = y_ret.handles.data_reshaped.XData;
  elseif dirtype == 2
    params.plot_2.anchor_data = [excitation_location(1), excitation_location(3)];
    %params.plot_2.Y = y_ret.handles.data_reshaped.XData;
  else
    params.plot_2.anchor_data = [excitation_location(2), excitation_location(3)];
    %params.plot_2.Y = y_ret.handles.data_reshaped.XData;
  end
  params.plot_2.Y = params.plot_1.Y;
  params.plot_2.anchor_window = [0, 0];
  params.plot_2.relative_data_coordinates = false;
  params.plot_2.forced_limit = 'y';

  params.plot_3.handle = z_ret.handle_axis;
  params.plot_3.X = z_ret.handles.data_reshaped.XData;
  if dirtype == 1
    params.plot_3.Y = z_ret.handles.data_reshaped.YData;
    params.plot_3.anchor_data = [excitation_location(1), excitation_location(2)];
  elseif dirtype == 2
    params.plot_3.Y = [z_ret.handles.data_reshaped.YData(1,1), excitation_location(2)];
    params.plot_3.anchor_data = [excitation_location(1), excitation_location(2)];
  else
    params.plot_3.Y = z_ret.handles.data_reshaped.YData;
    params.plot_3.anchor_data = [excitation_location(2), excitation_location(1)];
  end
  params.plot_3.anchor_window = [0, 0.5];
  params.plot_3.relative_data_coordinates = false;
  params.plot_3.forced_limit = 'x';

  surf_triplet(params);
  
  if ~test_mode
    saveas_fig_and_png(fig, figure_basename);
  end

  % relabel axes
  xlabel(params.plot_1.handle, 'y (\mum)');
  ylabel(params.plot_1.handle, 'z (\mum)');
  
  xlabel(params.plot_2.handle, 'x (\mum)');
  ylabel(params.plot_2.handle, 'z (\mum)');
  
  xlabel(params.plot_3.handle, 'x (\mum)');
  ylabel(params.plot_3.handle, 'y (\mum)');

end
