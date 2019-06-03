function fig = calculateModeVolume_plotMaxDebug(max_info, ret, title_base, varargin)
  % creates some debugging plots: 2D + 1D cross-sections for Emod2 and EnergyDensity taken at the max_info point
  %
  % Note: To reduce RAM usage, no additional intermediate values are created for normalization.
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %%%%% create parser
  p = inputParser();
  p = inputParserWrapper(p, 'addRequired', 'max_info', @isstruct);
  p = inputParserWrapper(p, 'addRequired', 'ret', @isstruct);
  p = inputParserWrapper(p, 'addRequired', 'title_base', @ischar);
  p = inputParserWrapper(p, 'addParamValue', 'save_subplots', false, @islogical);
  p = inputParserWrapper(p, 'addParamValue', 'normalized', false, @islogical);
  p = inputParserWrapper(p, 'addParamValue', 'limits', [NaN, NaN, NaN, NaN, NaN, NaN], @(x) (isnumeric(x) && numel(x)==6));
  p = inputParserWrapper(p, 'addParamValue', 'material_background', true, @islogical);
  p = inputParserWrapper(p, 'addParamValue', 'color', [1,0,0], @(x) (isnumeric(x) && numel(x)==3));
  p = inputParserWrapper(p, 'addParamValue', 'save_dir', '.', @ischar);
  
  p = inputParserWrapper(p, 'parse', max_info, ret, title_base, varargin{:});
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  
  % define line style
  line_style = 'bo-';
  
  % create new figure
  fig = figure();
  
  % set limits, using the data range by default
  limits = p.Results.limits;
  if isnan(limits(1)); limits(1) = min(ret.data.X(:)); end;
  if isnan(limits(2)); limits(2) = max(ret.data.X(:)); end;
  if isnan(limits(3)); limits(3) = min(ret.data.Y(:)); end;
  if isnan(limits(4)); limits(4) = max(ret.data.Y(:)); end;
  if isnan(limits(5)); limits(5) = min(ret.data.Z(:)); end;
  if isnan(limits(6)); limits(6) = max(ret.data.Z(:)); end;
  
  % set normalization factors
  if p.Results.normalized
    EnergyDensity_normalization = max_info.EnergyDensity;
    Emod2_normalization = max_info.Emod2;
  else
    EnergyDensity_normalization = 1;
    Emod2_normalization = 1;
  end
  
  % number of rows and columns for the subplots
  rows = 2;
  cols = 5;
  
  %%%%%%%%%%%%%%%%%%%%%%%
  %%% create Emod2 plots
  
  % define data in cross-section planes
  x_plane = ret.data.Emod2(:, max_info.x_index, :) ./ Emod2_normalization;
  y_plane = ret.data.Emod2(max_info.y_index, :, :) ./ Emod2_normalization;
  z_plane = ret.data.Emod2(:, :, max_info.z_index) ./ Emod2_normalization;
  
  % get max value in each cross-section plane
  x_plane_max = max(x_plane(:));
  y_plane_max = max(y_plane(:));
  z_plane_max = max(z_plane(:));
  
  % get overall max value in all cross-section planes
  all_planes_max = max([x_plane_max, y_plane_max, z_plane_max]);
  
  subplot_handle = {};
  
  subplot_handle{end+1} = subplot(rows, cols, 1);
  plotVolumetricData(ret.data.X, ret.data.Y, ret.data.Z, ret.data.Emod2 ./ Emod2_normalization, max_info.x, max_info.y, max_info.z);
  caxis([0, all_planes_max]);
  hold on;
  plotVolumetricData(ret.data.X, ret.data.Y, ret.data.Z, ret.data.defect_mask, [], [], [], 'isosurface');
  xlabel('x'); ylabel('y'); zlabel('z');
  title(sprintf('%s - Emod2 - 3D', title_base), 'interpreter', 'none');
  xlim(limits(1:2)); ylim(limits(3:4)); zlim(limits(5:6));
  
  subplot_handle{end+1} = subplot(rows, cols, 2);
  plotVolumetricData(ret.data.X, ret.data.Y, ret.data.Z, ret.data.Emod2 ./ Emod2_normalization, max_info.x, max_info.y, max_info.z);
  caxis([0, all_planes_max]);
  xlabel('x'); ylabel('y'); zlabel('z');
  title(sprintf('%s - Emod2 - 3D', title_base), 'interpreter', 'none');
  xlim(limits(1:2)); ylim(limits(3:4)); zlim(limits(5:6));
  
  subplot_handle{end+1} = subplot(rows, cols, 3);
  x = squeeze(ret.data.X(max_info.y_index, :, max_info.z_index));
  data = squeeze(ret.data.Emod2(max_info.y_index, :, max_info.z_index)) ./ Emod2_normalization;
  xlim(limits(1:2));
  setSafeYlim(data);
  if p.Results.material_background
    hold on;
    filledCenteredStairsWithThreshold(x, squeeze(ret.data.D(max_info.y_index, :, max_info.z_index, 1)), 1, p.Results.color);
  end
  plot(x, data, line_style);
  xlabel('x'); ylabel('Emod2');
  title(sprintf('%s - Emod2 - X', title_base), 'interpreter', 'none');
  hline(max_info.Emod2 ./ Emod2_normalization);
  vline(max_info.x);
  
  subplot_handle{end+1} = subplot(rows, cols, 4);
  y = squeeze(ret.data.Y(:, max_info.x_index, max_info.z_index));
  data = squeeze(ret.data.Emod2(:, max_info.x_index, max_info.z_index)) ./ Emod2_normalization;
  xlim(limits(3:4));
  setSafeYlim(data);
  if p.Results.material_background
    hold on;
    filledCenteredStairsWithThreshold(y, squeeze(ret.data.D(:, max_info.x_index, max_info.z_index, 1)), 1, p.Results.color);
  end
  plot(y, data, line_style);
  xlabel('y'); ylabel('Emod2');
  title(sprintf('%s - Emod2 - Y', title_base), 'interpreter', 'none');
  hline(max_info.Emod2 ./ Emod2_normalization);
  vline(max_info.y);
  
  subplot_handle{end+1} = subplot(rows, cols, 5);
  z = squeeze(ret.data.Z(max_info.y_index, max_info.x_index, :));
  data = squeeze(ret.data.Emod2(max_info.y_index, max_info.x_index, :)) ./ Emod2_normalization;
  xlim(limits(5:6));
  setSafeYlim(data);
  if p.Results.material_background
    hold on;
    filledCenteredStairsWithThreshold(z, squeeze(ret.data.D(max_info.y_index, max_info.x_index, :, 1)), 1, p.Results.color);
  end
  plot(z, data, line_style);
  xlabel('z'); ylabel('Emod2');
  title(sprintf('%s - Emod2 - Z', title_base), 'interpreter', 'none');
  hline(max_info.Emod2 ./ Emod2_normalization);
  vline(max_info.z);
  
  %%%%%%%%%%%%%%%%%%%%%%%
  %%% create EnergyDensity plots
  
  % define data in cross-section planes
  x_plane = ret.data.EnergyDensity(:, max_info.x_index, :) ./ EnergyDensity_normalization;
  y_plane = ret.data.EnergyDensity(max_info.y_index, :, :) ./ EnergyDensity_normalization;
  z_plane = ret.data.EnergyDensity(:, :, max_info.z_index) ./ EnergyDensity_normalization;
  
  % get max value in each cross-section plane
  x_plane_max = max(x_plane(:));
  y_plane_max = max(y_plane(:));
  z_plane_max = max(z_plane(:));
  
  % get overall max value in all cross-section planes
  all_planes_max = max([x_plane_max, y_plane_max, z_plane_max]);
  
  subplot_handle{end+1} = subplot(rows, cols, 6);
  plotVolumetricData(ret.data.X, ret.data.Y, ret.data.Z, ret.data.EnergyDensity ./ EnergyDensity_normalization, max_info.x, max_info.y, max_info.z);
  caxis([0, all_planes_max]);
  hold on;
  plotVolumetricData(ret.data.X, ret.data.Y, ret.data.Z, ret.data.defect_mask, [], [], [], 'isosurface');
  xlabel('x'); ylabel('y'); zlabel('z');
  title(sprintf('%s - EnergyDensity - 3D', title_base), 'interpreter', 'none');
  xlim(limits(1:2)); ylim(limits(3:4)); zlim(limits(5:6));

  subplot_handle{end+1} = subplot(rows, cols, 7);
  plotVolumetricData(ret.data.X, ret.data.Y, ret.data.Z, ret.data.EnergyDensity ./ EnergyDensity_normalization, max_info.x, max_info.y, max_info.z);
  caxis([0, all_planes_max]);
  xlabel('x'); ylabel('y'); zlabel('z');
  title(sprintf('%s - EnergyDensity - 3D', title_base), 'interpreter', 'none');
  xlim(limits(1:2)); ylim(limits(3:4)); zlim(limits(5:6));
  
  subplot_handle{end+1} = subplot(rows, cols, 8);
  x = squeeze(ret.data.X(max_info.y_index, :, max_info.z_index));
  data = squeeze(ret.data.EnergyDensity(max_info.y_index, :, max_info.z_index)) ./ EnergyDensity_normalization;
  xlim(limits(1:2));
  setSafeYlim(data);
  if p.Results.material_background
    hold on;
    filledCenteredStairsWithThreshold(x, squeeze(ret.data.D(max_info.y_index, :, max_info.z_index, 1)), 1, p.Results.color);
  end
  plot(x, data, line_style);
  xlabel('x'); ylabel('EnergyDensity');
  title(sprintf('%s - EnergyDensity - X', title_base), 'interpreter', 'none');
  hline(max_info.EnergyDensity ./ EnergyDensity_normalization);
  vline(max_info.x);
  
  subplot_handle{end+1} = subplot(rows, cols, 9);
  y = squeeze(ret.data.Y(:, max_info.x_index, max_info.z_index));
  data = squeeze(ret.data.EnergyDensity(:, max_info.x_index, max_info.z_index)) ./ EnergyDensity_normalization;
  xlim(limits(3:4));
  setSafeYlim(data);
  if p.Results.material_background
    hold on;
    filledCenteredStairsWithThreshold(y, squeeze(ret.data.D(:, max_info.x_index, max_info.z_index, 1)), 1, p.Results.color);
  end
  plot(y, data, line_style);
  xlabel('y'); ylabel('EnergyDensity');
  title(sprintf('%s - EnergyDensity - Y', title_base), 'interpreter', 'none');
  hline(max_info.EnergyDensity ./ EnergyDensity_normalization);
  vline(max_info.y);
  
  subplot_handle{end+1} = subplot(rows, cols, 10);
  z = squeeze(ret.data.Z(max_info.y_index, max_info.x_index, :));
  data = squeeze(ret.data.EnergyDensity(max_info.y_index, max_info.x_index, :)) ./ EnergyDensity_normalization;
  xlim(limits(5:6));
  setSafeYlim(data);
  if p.Results.material_background
    hold on;
    filledCenteredStairsWithThreshold(z, squeeze(ret.data.D(max_info.y_index, max_info.x_index, :, 1)), 1, p.Results.color);
  end
  plot(z, data, line_style);
  xlabel('z'); ylabel('EnergyDensity');
  title(sprintf('%s - EnergyDensity - Z', title_base), 'interpreter', 'none');
  hline(max_info.EnergyDensity ./ EnergyDensity_normalization);
  vline(max_info.z);
  
  if p.Results.save_subplots
    for subplot_handle_idx = 1:numel(subplot_handle)
      outfile = fullfile(p.Results.save_dir, sprintf('%s_%d', title_base, subplot_handle_idx));
      fprintf('Saving subplot %d as %s\n', subplot_handle_idx, outfile);
      saveSubPlot(subplot_handle{subplot_handle_idx}, outfile);
    end
  end
end

function setSafeYlim(data)
  R = getRange(data);
  if min(data(:)) == max(data(:))
    ymin = min(data(:))-1;
    ymax = max(data(:))+1;
    R_fixed = [ymin, ymax];
    warning('Data is homogeneous (range = [%f, %f] ). Using [%f, %f] as range instead.', R(1), R(2), R_fixed(1), R_fixed(2));
    R = R_fixed;
  end
  ylim(R);
end

function saveSubPlot(hax, outfile)
  hfig = figure;
  hax_new = copyobj(hax, hfig);
  set(hax_new, 'Position', get(0, 'DefaultAxesPosition'));
  %print(hfig);
  saveas_fig_and_png(hfig, outfile);
end
