function ret = plot_MPB(datafilename, varargin)
  % function ret = plot_MPB(datafilename, varargin)
  %
  % Script to plot photonic bandgap diagrams from MPB output.
  % It should be replaced by a better tool in the future (directly using the .ctl and then plotting the output, or reading in any kind of MPB output), but if you want to quickly have a look at the bands, it works well enough.
  %
  % Parameters:
  % ===========
  % datafilename: The name of the data file (in CSV format).
  %
  % If plot_MPB fails to read the data file, you can try directly importing it via the Matlab import tool and manually plotting it.
  %
  % If you are still having problems, open your .dat file in a text editor to look for any unusual content.
  %
  % TODO: make sure old-style .dat files are still supported...
  % TODO: integrate MPB output postprocessing step
  % TODO: should read MPB .ctl file to plot vertical direction lines with labels
  % TODO: plots with two y axes (cf old code)
  % TODO: plot as function of angle -> requires lattice vectors + at least two vectors for oriented angles
  % TODO: Find matlab equivalent of is_function_handle()
  % TODO: create useful xzfunc/yfunc functions
  % TODO: move this and related functions into own folder
  % TODO: 3D isosurface plotting, k-index as Y-value? path animation, etc
  % TODO: python/C++/Qt version, i.e. for future Matlab-free GUI?
  % TODO: call via mpb_wrapper.py somehow, unless python-plotting implemented first?
  % TODO: allow passing arrays (pos+label) to hline/vline or create wrappers for convenience? (including wrapper to support k-interp easily)
  % TODO: split off data processing part from plotting, to make later implementation of density of states, isoenergysurfaces, k-point paths, etc easier.

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %%%%% command options:
  p = inputParser();
  
  % select input file
  p = inputParserWrapper(p, 'addRequired', 'datafilename', @ischar);
  
  %%% hline/vline options. While a 3D plot can be created, these are simply meant to be used in 2D and are therefore in the XY plane.
  % add vlines
  p = inputParserWrapper(p, 'addParamValue', 'vline_labels', {}, @iscell);
  p = inputParserWrapper(p, 'addParamValue', 'vline_positions', [], @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'vline_process_coordinates', false, @islogical);
  
  % add hlines
  p = inputParserWrapper(p, 'addParamValue', 'hline_labels', {}, @iscell);
  p = inputParserWrapper(p, 'addParamValue', 'hline_positions', [], @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'hline_process_coordinates', true, @islogical);
  
  % limit data ranges
  p = inputParserWrapper(p, 'addParamValue', 'k_point_indices', [], @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'bands', [], @isnumeric);

  % set axis limits
  p = inputParserWrapper(p, 'addParamValue', 'xlim', [NaN, NaN], @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'ylim', [NaN, NaN], @isnumeric);
  
  % These can all be done easily manually, but are useful for re-using the generated "custom_function":
  p = inputParserWrapper(p, 'addParamValue', 'title', true, @(x) (islogical(x) || ischar(x)) );
  p = inputParserWrapper(p, 'addParamValue', 'grid', false, @islogical);
  
  % automatically mark gaps?
  p = inputParserWrapper(p, 'addParamValue', 'gap_marking', true, @islogical);
  
  % save file (true for automatic naming, else specify filename)
  p = inputParserWrapper(p, 'addParamValue', 'saveas', false, @(x) islogical(x) || ischar(x));
  
  % create new figure or not? (useful for use of subplots, etc)
  p = inputParserWrapper(p, 'addParamValue', 'new_figure', true, @islogical);

  % specify linespec options for plotting
  p = inputParserWrapper(p, 'addParamValue', 'linespec', '', @ischar);
  
  %%% Two custom functions a user can pass to postprocess the coordinates.
  %%% Both must support one array input argument D and a position argument "pos"
  %%% and return output arrays with the same number of rows as "D" (or "pos" if "pos" is passed), as well as labels.
  %%% cf the default functions for examples.
  %%% They will simply be passed the data array (after restrictions, but including k point and frequency data).
  %%% For hline and vlines, single scalar values will be passed additionally as the "pos" argument.
  p = inputParserWrapper(p, 'addParamValue', 'xzfunc', @mpb_xzfunc_default);
  p = inputParserWrapper(p, 'addParamValue', 'yfunc', @mpb_yfunc_default);
  
  % additional structure for use by the postprocessing functions (for lattice, unit cell size, etc)
  p = inputParserWrapper(p, 'addParamValue', 'data_info', mpb_DataInfo());
  p = inputParserWrapper(p, 'addParamValue', 'klabels', {}, @iscell);
  
  % to support old .dat file format...
  p = inputParserWrapper(p, 'addParamValue', 'GuessCsvDelimiter', true, @islogical);
  
  % set verbosity:
  p = inputParserWrapper(p, 'addParamValue', 'verbosity', 1, @isnumeric);
  
  p = inputParserWrapper(p, 'parse', datafilename, varargin{:});
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % TODO: re-enable later, once happy with plotting system
  %% define a custom function, so it can be re-used easily for other filenames (useful together with filefun() for example)
  %ret.custom_function = @(x) plot_MPB(x, ...
                                      %'bands', p.Results.bands, ...
                                      %'vline_labels', p.Results.vline_labels, ...
                                      %'vline_positions', p.Results.vline_positions, ...
                                      %'vline_process_coordinates', p.Results.vline_process_coordinates, ...
                                      %'hline_labels', p.Results.hline_labels, ...
                                      %'hline_positions', p.Results.hline_positions, ...
                                      %'hline_process_coordinates', p.Results.hline_process_coordinates, ...
                                      %'k_point_indices', p.Results.k_point_indices, ...
                                      %'gap_edges', p.Results.gap_edges, ...
                                      %'xlim', p.Results.xlim, ...
                                      %'ylim', p.Results.ylim, ...
                                      %'title', p.Results.title, ...
                                      %'invert_y_values', p.Results.invert_y_values, ...
                                      %'y_axis_scale_factor', p.Results.y_axis_scale_factor, ...
                                      %'disable_gap_marking', p.Results.disable_gap_marking, ...
                                      %'saveas', p.Results.saveas, ...
                                      %'new_figure', p.Results.new_figure, ...
                                      %'grid', p.Results.grid, ...
                                      %'angle_reference_vector', p.Results.angle_reference_vector, ...
                                      %'angle_normal_vector', p.Results.angle_normal_vector, ...
                                      %'linespec', p.Results.linespec, ...
                                      %'lattice', p.Results.lattice, ...
                                      %'xzfunc', p.Results.xzfunc, ...
                                      %'verbosity', p.Results.verbosity);

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %%%%% data input
  ret.mpbdata = read_MPB_CSV(datafilename, 'data_info', p.Results.data_info, 'klabels', p.Results.klabels, 'GuessCsvDelimiter', p.Results.GuessCsvDelimiter);
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %%%%% gap calculations
  ret.gapdata = mpb_getGaps(ret.mpbdata);
  
  % quick hack to make things work again
  ret.data = ret.mpbdata.rawdata.data_full;
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %%%%% extract x,y,z values and labels based on data
  [ret.x, ret.z, x_label, z_label] = p.Results.xzfunc(ret.data, [], p.Results.data_info);
  [ret.y, y_label] = p.Results.yfunc(ret.data, [], p.Results.data_info);
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %%%%% plotting

  % create figure if needed
  if p.Results.new_figure
    ret.figure_handle = figure;
  else
    ret.figure_handle = gcf();
  end
  hold all;
  
  % plot data
  for i = 1:size(ret.y, 2)
    if p.Results.linespec
      plot3(ret.x, ret.y(:, i), ret.z, p.Results.linespec);
    else
      plot3(ret.x, ret.y(:, i), ret.z);
    end
  end

  % 2D view
  view(2);

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %%%%% apply common plotting options
  
  xlabel(x_label);
  ylabel(y_label);
  zlabel(z_label);
  
  if ischar(p.Results.title)
    title(p.Results.title, 'Interpreter', 'none');
  elseif p.Results.title
    title(datafilename, 'Interpreter', 'none');
  end
  
  % grid on/off
  if p.Results.grid
    grid on;
  else
    grid off;
  end
  
  % restrict to given limits (should be done before adding hline/vline annotations, because they adapt to current xlim/ylim)
  if ~any(isnan(p.Results.xlim))
    xlim(p.Results.xlim);
  end
  if ~any(isnan(p.Results.ylim))
    ylim(p.Results.ylim);
  end
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %%%%% add annotations
  
  x_lim = xlim();
  y_lim = ylim();
  
  % For convenience, define vline_positions if they are not defined, but vline_labels are.
  % Note: done based on data_full!
  if isempty(p.Results.vline_positions) && ~isempty(p.Results.vline_labels)
    vline_positions = linspace(1, size(ret.mpbdata.rawdata.data_full, 1), length(p.Results.vline_labels) );
  else
    vline_positions = p.Results.vline_positions;
  end
  
  % add vertical lines
  for i = 1:length(vline_positions)
    pos = vline_positions(i);
    if p.Results.vline_process_coordinates
      pos = p.Results.xzfunc(ret.data, pos, p.Results.data_info);
    end
    if i <= length(p.Results.vline_labels)
      label = p.Results.vline_labels(i);
    else
      label = '';
    end
    if x_lim(1) <= pos && pos <= x_lim(2)
      vline(pos, 'r', label, 270, false);
    end
  end
  
  % add horizontal lines
  for i = 1:length(p.Results.hline_positions)
    pos = p.Results.hline_positions(i);
    if p.Results.hline_process_coordinates
      pos = p.Results.yfunc(ret.data, pos, p.Results.data_info);
    end
    if i <= length(p.Results.hline_labels)
      label = p.Results.hline_labels(i);
    else
      label = '';
    end
    if y_lim(1) <= pos && pos <= y_lim(2)
      hline(pos, 'r', label);
    end
  end
  
  % gap marking
  if p.Results.gap_marking
    for idx = 1:length(ret.gapdata.fullgaps.bottom_band_idx)
      hline(p.Results.yfunc(ret.data, ret.gapdata.fullgaps.top(idx), p.Results.data_info));
      hline(p.Results.yfunc(ret.data, ret.gapdata.fullgaps.bottom(idx), p.Results.data_info));
      gap_text = sprintf('%.2f%% at a/\\lambda = %.3f', 100*ret.gapdata.fullgaps.size_relative(idx), ret.gapdata.fullgaps.midgap(idx));
      gap_text_x = mean(xlim);
      gap_text_y = p.Results.yfunc(ret.data, ret.gapdata.fullgaps.midgap(idx), p.Results.data_info);
      text(gap_text_x, gap_text_y, gap_text, 'HorizontalAlignment', 'center');
      fprintf('Full gap between bands %d and %d: %s\n', ret.gapdata.fullgaps.bottom_band_idx(idx), ret.gapdata.fullgaps.bottom_band_idx(idx)+1, gap_text);
    end
  end
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %%%%% save figure
  ret.save_filename = '';
  if islogical(p.Results.saveas) && p.Results.saveas
    [filename_DIR, filename_NAME, filename_EXT] = fileparts(datafilename);
    ret.save_filename = fullfile(filename_DIR, [filename_NAME, '.png']);
  elseif ischar(p.Results.saveas) && ~isempty(p.Results.saveas)
    ret.save_filename = p.Results.saveas;
  end

  if ~isempty(ret.save_filename)
    if p.Results.verbosity >=1
      fprintf('Saving plot as %s\n', ret.save_filename);
    end
    saveas(gcf, ret.save_filename);
  end
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% old deprecated code dump
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  % for full bandgaps
  %top = min(min(data(:,firstband+2:N))); % bands i>=3 
  %bot = max(max(data(:,firstband:firstband+1))); % bands 1+2
  %mid = 0.5*(top+bot);
  %top_line = hline(top,'r',num2str(top));
  %mid_line = hline(mid,'g',num2str(mid));
  %bot_line = hline(bot,'b',num2str(bot));
  
  %disp(['top = ',num2str(top)]);
  %disp(['mid = ',num2str(mid)]);
  %disp(['bot = ',num2str(bot)]);

  % mid-gaps

  %i = 2
  %aa = data(1+(i-1)*10,find(strcmp(header,'band_5')));
  %b = data(1+(i-1)*10,find(strcmp(header,'band_6')));
  %delta = abs(b-aa);
  %hline(aa,'r',num2str(aa));
  %hline(b,'r',num2str(b));
  %text(1,0.5*(aa+b),num2str(delta));

  %i = 3 % L direction
  %aa = data(1+(i-1)*10,find(strcmp(header,'band_2')))
  %b = data(1+(i-1)*10,find(strcmp(header,'band_3')))
  %delta = abs(b-aa);
  %hline(aa,'r',num2str(aa));
  %hline(b,'r',num2str(b));
  %text(1,0.5*(aa+b),num2str(delta));
  %gap = abs(b-aa)
  %midgap = 0.5*(aa+b)
  %gapsize = gap/midgap
  %hline(midgap,'r',num2str(midgap));

  %i = 7;
  %maxi = data(1+(i-1)*10,find(strcmp(header,'band_3')))
  %i = 7;
  %mini = data(1+(i-1)*10,find(strcmp(header,'band_2')))
  %delta = abs(maxi-mini);
  %%hline(aa,'r',num2str(aa));
  %%hline(b,'r',num2str(b));
  %%text(1,0.5*(aa+b),num2str(delta));
  %%gap = abs(maxi-mini);
  %midgap = 0.5*(mini+maxi)
  %%gapsize = gap/midgap;
  
  %hline(mini,'r',num2str(mini));
  %hline(midgap,'g',num2str(midgap));
  %hline(maxi,'b',num2str(maxi));
  
  %a_value = midgap*lambda0;
  %lambda_mini = a_value/mini;
  %lambda_midgap = a_value/midgap;
  %lambda_maxi = a_value/maxi;
  
  %disp(['midgap = ',num2str(midgap)]);
  %disp(['lambda0 = ',num2str(lambda0)]);
  %disp(['a_value = ',num2str(a_value)]);
  %disp(['lambda_mini = ',num2str(lambda_mini)]);
  %disp(['lambda_midgap = ',num2str(lambda_midgap)]);
  %disp(['lambda_maxi = ',num2str(lambda_maxi)]);
  
  %midgap1=0.645561870915862
  %hline(midgap1,'r',num2str(midgap1));
  %midgap2=0.673605092161939
  %hline(midgap2,'r',num2str(midgap2));
  %midgap3=0.5*(midgap1+midgap2)

  %if exist('spacepoints','var')
    %for i=1:length(spacepoints)
      %vline(data(1+(i-1)*(interpol+1),1),'r',spacepoints{i}, 270, false);
    %end
  %end
  
  %%% to plot band edges and calculate gap position and size
  % mini = rawdata(11,6);
  % maxi = rawdata(11,8);
  % hline(mini, 'g', num2str(mini));
  % hline(maxi, 'g', num2str(maxi));
  % midgap = (mini+maxi)/2
  % gap = (maxi-mini)/midgap

  %p = inputParserWrapper(p, 'addParamValue', 'invert_y_values', false, @islogical);
  %p = inputParserWrapper(p, 'addParamValue', 'y_axis_scale_factor', 1, @isnumeric);
  %p = inputParserWrapper(p, 'addParamValue', 'angle_reference_vector', [NaN, NaN, NaN], @isnumeric);
  %p = inputParserWrapper(p, 'addParamValue', 'angle_normal_vector', [NaN, NaN, NaN], @isnumeric);
  %p = inputParserWrapper(p, 'addParamValue', 'lattice', [[1,0,0], [0,1,0], [0,0,1]], @(x) isnumeric(x) || ischar(x));
  %p = inputParserWrapper(p, 'addParamValue', 'gap_edges', [NaN, NaN], @isnumeric);
  % add vertical lines
  %for i = 1:length(p.Results.vline_positions)
    %if p.Results.vline_process_coordinates
      %%k_point = 
      %pos = getKpointAngle(k_point, p.Results.angle_reference_vector, p.Results.angle_normal_vector, p.Results.lattice);
    %else
      %pos = p.Results.vline_positions(i);
    %end
    %if i <= length(p.Results.vline_labels)
      %label = p.Results.vline_labels(i);
    %else
      %label = '';
    %end
    %vline(pos, 'r', label, 270, false);
  %end
  %%% Both must support array input arguments and return output arrays of the same size.
  % A function taking as input (k_index, k1, k2, k3, kmag_over_2pi) and returning two values to use as x and z coordinates.
  % Note that for postprocessing vline positions, it simply calls xzfunc(pos,pos,pos,pos,pos).
  % define x coordinates
  %if is_function_handle(p.Results.xzfunc)
    %ret.x = p.Results.xzfunc(ret.k1, ret.k2, ret.k3);
  %elseif ~any(isnan(p.Results.angle_reference_vector))
    %% redefine indices as angles if a reference vector is given
    %error('angle conversion not yet implemented');
  %else
    %ret.x = ret.k_index;
  %end
  % A function taking as input a normalized frequency (a/lambda) and returning a point to use as y-coordinate.
  %p = inputParserWrapper(p, 'addParamValue', 'xlabel', 'direction', @ischar);
  %p = inputParserWrapper(p, 'addParamValue', 'ylabel', 'a/\lambda', @ischar);
  %p = inputParserWrapper(p, 'addParamValue', 'zlabel', '', @ischar);
%function plot_MPB(datafilename, interpol, titolo, spacepoints)
  % function plot_MPB(datafilename, interpol, titolo, spacepoints)
  % interpol: (optional) The number of interpolation points (i.e. the number passed to the CTL interpolate function). Example: (set! k-points (interpolate 4 k-points)) -> interpol=4
  % titolo: (optional) The title of your plot.
  % spacepoints: (optional) The labels of your main k points. Example: {'Gamma','M','K','Gamma'}
  % Example procedure:
  % ==================
  % Run MPB and create a .out file:
  %   $ mpb mysim.ctl > mysim.out
  % Postprocess the file to create a mysim.out.dat file:
  %   $ postprocess_mpb.sh mysim.out
  % Plot using plot_MPB in Matlab:
  %   >>> plot_MPB('mysim.out.dat', 4, 'My amazing title', {'Gamma','M','K','Gamma'});
  %
  % Note: The postprocess_mpb.sh was created to be able to use the column titles more easily, but if you cannot use it, just use grep instead:
  %   $ grep freq mysim.out > mysim.out.dat
%function mpb_label_kpoints(label_list, k_interp)
  %% interpol: (optional) The number of interpolation points (i.e. the number passed to the CTL interpolate function). Example: (set! k-points (interpolate 4 k-points)) -> interpol=4
  %% titolo: (optional) The title of your plot.
  %% : (optional) The labels of your main k points. Example: {'Gamma','M','K','Gamma'}
%vline_labels
%vline_positions
%end
