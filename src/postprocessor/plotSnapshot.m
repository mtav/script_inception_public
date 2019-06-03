function ret = plotSnapshot(varargin)
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % Function to display results from frequency snapshots and poynting vector calculations from University of Bristol FDTD software
  %
  % WARNING: SPAGHETTI CODE!!! Way too complex and convoluted to be properly usable!
  %
  % Written by Ian Buss 2006
  % Modified quite a bit by Mike T.
  % To be pythonified, Qt-ified or at least de-Matlabified. :p
  %
  % TODO: Re-assess utility of readtextfile.m, inputparms.m, geometryparms.m
  %
  % For Poynting vector plots in the same format use snap_poy_int.m
  % TODO: Locate snap_poy_int.m (Poynting vector snapshot?)
  % TODO: Add axis scaling (useful for thin structures)
  % TODO: When showing geometry, only show "current layer", i.e. slice through geometry instead of whole geometry projection...
  % TODO: Use transparent overlay of epsilon snapshot (use alphamap function maybe?) instead of geometry lines.
  % TODO: Option to pass the title or some base properties of it...? User can easily rename manually anyway...
  % TODO: needs serious cleaning up like plotProbe and plotMPB... -> need to always split data reading, processing, plotting, plotting options, saving, etc...
  % TODO: more importantly need proper GUI, to make all this almost obsolete...
  % TODO: warning: the 'clearvars' function is not yet implemented in Octave
  % TODO: specify columns by name?
  %
  % Arguments:
  % column = column ID, 1 being the first column of the snaphot .prn file, i.e. the xy/yz/zx columns are included
  %
  % Default values:
  %   zlimits = [NaN, NaN]
  %
  % required attributes of handles:
  % ===============================
  % handles.AllHeaders
  % handles.colour
  % handles.data
  % handles.dataSize
  % handles.interpolate
  % handles.plane
  % handles.plotSnapshotType
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %%%%% create parser
  p = inputParser();
  
  p = inputParserWrapper(p, 'addParamValue', 'filename', '', @ischar);
  p = inputParserWrapper(p, 'addParamValue', 'column', -1, @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'zlimits', [NaN, NaN], @(x) isnumeric(x) && length(x)==2);
  p = inputParserWrapper(p, 'addParamValue', 'handles', struct(), @isstruct);
  p = inputParserWrapper(p, 'addParamValue', 'swap_axes', false, @islogical);
  p = inputParserWrapper(p, 'addParamValue', 'view', 2, @isnumeric); % directly passed to view() command, i.e. can be [azimuth, elevation] or simply 2,3 for 2D, 3D view
  p = inputParserWrapper(p, 'addParamValue', 'createFigure', true, @islogical);
  p = inputParserWrapper(p, 'addParamValue', 'hide_figures', false, @islogical);
  p = inputParserWrapper(p, 'addParamValue', 'drawTitle', true, @islogical);
  p = inputParserWrapper(p, 'addParamValue', 'drawColorBar', true, @islogical);
  p = inputParserWrapper(p, 'addParamValue', 'colorbarPosition', 'EastOutside', @ischar);
  p = inputParserWrapper(p, 'addParamValue', 'saveas', false, @(x) islogical(x) || ischar(x)); % save file (true for automatic naming, else specify filename)
  p = inputParserWrapper(p, 'addParamValue', 'contourFile', '', @ischar);
  p = inputParserWrapper(p, 'addParamValue', 'contourColumn', 3, @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'contourValues', NaN, @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'LineWidth', 1, @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'LineColor', 'yellow', @(x) isnumeric(x) || ischar(x));
  p = inputParserWrapper(p, 'addParamValue', 'modulus', false, @islogical);
  p = inputParserWrapper(p, 'addParamValue', 'normalized', false, @islogical);
  p = inputParserWrapper(p, 'addParamValue', 'log10', false, @islogical);
  p = inputParserWrapper(p, 'addParamValue', 'symmetricRange', false, @islogical);
  p = inputParserWrapper(p, 'addParamValue', 'updateCaxis', true, @islogical); % update caxis range
  
  p = inputParserWrapper(p, 'addParamValue', 'drawGeometry', false, @islogical);
  p = inputParserWrapper(p, 'addParamValue', 'geofile', '', @ischar);
  p = inputParserWrapper(p, 'addParamValue', 'inpfile', '', @ischar);
  
  p = inputParserWrapper(p, 'addParamValue', 'pre_2008_BFDTD_version', false, @islogical);
  
  %p = inputParserWrapper(p, 'addParamValue', 'surface', true, @islogical); % plot as surface or contour?
  MainPlotType_list_input = {'surface', 'contour', 'contourAtZ'};
  p = inputParserWrapper(p, 'addParamValue', 'MainPlotType', 'surface', @(x) any(validatestring(x, MainPlotType_list_input))); % plot as surface or contour?
  p = inputParserWrapper(p, 'addParamValue', 'MainContourZposition', 0, @isnumeric); % Z position of the contour from the main file
  
  p = inputParserWrapper(p, 'parse', varargin{:});

  MainPlotType = validatestring(p.Results.MainPlotType, MainPlotType_list_input);
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  snapshot_filename = p.Results.filename;
  if ~ischar(snapshot_filename) || isempty(snapshot_filename)
    [FNAME, FPATH, FLTIDX] = uigetfile('*.prn', 'Select a snapshot file');
    if ~ischar(FNAME) || isempty(FNAME)
      disp('No file selected. Exiting');
      return
    else
      snapshot_filename = fullfile(FPATH, FNAME);
    end
  end

  % simple hack to quickly fix PP again :)
  if ~isempty(fieldnames(p.Results.handles))
    handles = p.Results.handles;
  end
  
  if exist('handles','var')==0 || isfield(handles,'colour')==0; handles.colour = 1; end
  if exist('handles','var')==0 || isfield(handles,'interpolate')==0; handles.interpolate = true; end
  %if exist('handles','var')==0 || isfield(handles,'useAdaptedMaxIfIsNaN')==0; handles.useAdaptedMaxIfIsNaN = true; end
  if exist('handles','var')==0 || isfield(handles,'LimitToBox')==0; handles.LimitToBox = true; end
  
  if exist('handles','var')==0 || isfield(handles, 'cropData_Xmin')==0; handles.cropData_Xmin = NaN; end
  if exist('handles','var')==0 || isfield(handles, 'cropData_Xmax')==0; handles.cropData_Xmax = NaN; end
  if exist('handles','var')==0 || isfield(handles, 'cropData_Ymin')==0; handles.cropData_Ymin = NaN; end
  if exist('handles','var')==0 || isfield(handles, 'cropData_Ymax')==0; handles.cropData_Ymax = NaN; end
  if exist('handles','var')==0 || isfield(handles, 'cropData_Zmin')==0; handles.cropData_Zmin = NaN; end
  if exist('handles','var')==0 || isfield(handles, 'cropData_Zmax')==0; handles.cropData_Zmax = NaN; end
  
  if exist('handles','var')==0 || isfield(handles, 'grid')==0; handles.grid = true; end
  
  if exist('handles','var')==0 || ...
     isfield(handles,'header')==0 || ...
     isfield(handles,'data')==0 || ...
     isfield(handles,'dataSize')==0 || ...
     isfield(handles,'plane')==0 || ...
     isfield(handles,'AllHeaders')==0
    
    [handles.header, handles.data] = readPrnFile(snapshot_filename);
    handles.dataSize = size(handles.data);
    columns = handles.header(:);
    if strcmp(columns(1),'y') && strcmp(columns(2),'z')
      handles.plane = 1;
    elseif strcmp(columns(1),'x') && strcmp(columns(2),'z')
      handles.plane = 2;
    elseif strcmp(columns(1),'#y') && strcmp(columns(2),'z')
      handles.plane = 1;
    elseif strcmp(columns(1),'#x') && strcmp(columns(2),'z')
      handles.plane = 2;
    else
      handles.plane = 3;
    end
    handles.AllHeaders = columns; % all headers
    
  end

  selected_column = p.Results.column;
  
  if ~isfinite(selected_column) || selected_column < 1 || selected_column > length(handles.AllHeaders)
    [selected_column, ok] = listdlg('PromptString', 'Choose what you want to plot:\n', 'SelectionMode', 'single', 'ListString', handles.AllHeaders);
    if ~ok
      disp('No valid column selected. Exiting.');
      return
    end
  end

  fprintf('selected_column = %d -> %s\n' ,selected_column, handles.AllHeaders{selected_column});
  
  % frequency snapshot specific
  if exist('handles','var') == 0 || isfield(handles, 'plotSnapshotType') == 0
    [handles.plotSnapshotType, type_name] = getDataType(snapshot_filename);
  end

  % read BFDTD input files (to load the geometry data and specify frequency information)
  geofile_loaded = false;
  inpfile_loaded = false;
  % TODO: Do this in a nicer way? Arbitrary amount of .inp/.geo/.in files accepted?
  % Only load the geometry, if the user requested it. Else, only load the .inp file, if possible.
  if p.Results.drawGeometry
    if exist(p.Results.geofile, 'file') && exist(p.Results.inpfile, 'file')
      [entries, FDTDobj] = GEO_INP_reader({p.Results.geofile, p.Results.inpfile});
      geofile_loaded = true;
      inpfile_loaded = true;
    elseif exist(p.Results.geofile, 'file')
      [entries, FDTDobj] = GEO_INP_reader({p.Results.geofile});
      geofile_loaded = true;
    elseif exist(p.Results.inpfile, 'file')
      [entries, FDTDobj] = GEO_INP_reader({p.Results.inpfile});
      inpfile_loaded = true;
    end
  else
    if exist(p.Results.inpfile, 'file')
      [entries, FDTDobj] = GEO_INP_reader({p.Results.inpfile});
      inpfile_loaded = true;
    end
  end
  
  if p.Results.drawGeometry && ~geofile_loaded
    uiwait(warndlg('You need to specify a .geo file in order to show the geometry. Geometry drawing will be disabled.', 'No .geo file specified.'));
  end
  
  %% Determine size of snapshot
  ii = 1; ValPrev = handles.data(ii,1); grid_j = 1;
  while ii<handles.dataSize(1)
    if handles.data(ii,1) ~= ValPrev
      ValPrev = handles.data(ii,1);
      grid_j = grid_j+1;
    end
    ii = ii+1;
  end
  grid_i = handles.dataSize(1)/grid_j;
  
  %% Create meshgrids for snapshot
  % Doing some manual reshaping here... Why not use readPrnFile with data reshaping?!!!!
  % TODO: use readPrnFile data reshaping...
  % TODO: Replace i,j,k with more explicit variable names... (and less likely to be used elsewhere...)
  for pp = 1:grid_j
    for qq = 1:grid_i
      i(pp,qq) = handles.data(qq,2);
    end
  end
  
  for pp = 1:grid_j
    for qq = 1:grid_i
      j(pp,qq) = handles.data((qq+((pp-1)*grid_i)),1);
    end
  end
  
  %% Load column of choice to data
  rawdata = handles.data(:, selected_column);
  rawdata_name = char(handles.AllHeaders(selected_column));
  data = rawdata;
  data_name = rawdata_name;

  %% postprocess data
  if p.Results.modulus
    data = abs(data);
    data_name = sprintf('|%s|', data_name);
  end
  if p.Results.normalized
    data = data ./ max(abs(data(:)));
    data_name = sprintf('%s/max(|%s|)', data_name, rawdata_name);
  end
  if p.Results.log10
    data = log10(data);
    data_name = sprintf('log10(%s)', data_name);
  end

  if ~isreal(data)
    uiwait(warndlg('data contains non-real elements. Make sure you enable modulus when using logarithmic plotting.','non-real data'));
    return;
  end

  %% check for empty data
  disp(['DATA INFO: min(rawdata) = ',num2str(min(rawdata))]);
  disp(['DATA INFO: max(rawdata) = ',num2str(max(rawdata))]);
  if min(rawdata)==0 && max(rawdata)==0
    uiwait(warndlg('empty data: min(data)=max(data)=0','empty data'));
    return;
  end
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %% set minval/maxval
  minval = p.Results.zlimits(1);
  maxval = p.Results.zlimits(2);

  disp(['DATA INFO: min(data(:)) = ',num2str(min(data(:)))]);
  disp(['DATA INFO: max(data(:)) = ',num2str(max(data(:)))]);
  disp(['DATA INFO: mean(data(:)) = ',num2str(mean(data(:)))]);
  if isnan(minval)
    minval = min(data(:));
  end
  if isnan(maxval)
    maxval = max(data(:));
    % TODO: Old weird system which makes no sense. Just leaving for future reference...
    %if handles.useAdaptedMaxIfIsNaN
      %maxval = 8./9.*max(data(:))+1./9.*mean(data(:)); % this gives a pretty good color bar usually...
    %else
      %maxval = max(data(:));
    %end
  end

  disp(['PLOT INFO: minval = ',num2str(minval)]);
  disp(['PLOT INFO: maxval = ',num2str(maxval)]);
    
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  
  %% Create plot data meshgrid
  % Doing some manual reshaping here... Why not use readPrnFile with data reshaping?!!!!
  % TODO: use readPrnFile data reshaping...
  count = 1;
  for ii = 1:grid_j
    kk = grid_i*count;
    for jj = 1:grid_i
      k(ii,jj) = data(jj+(kk-grid_i));
    end
    count = count+1;
  end
  
  % debug info
  %disp('size(k)');
  %size(k);
  %disp('size(data)');
  %size(data);
  
  %% Create figure and plot data
  if p.Results.createFigure
    if p.Results.hide_figures
      fig = figure('visible','off');
    else
      fig = figure('visible','on');
    end
  end
  
  grey = 0; % used for automatic naming of save file
  if (handles.colour)
    main_colormap = colormap(jet(256));
    grey = 0;
  else
    main_colormap = colormap(gray(256));
    grey = 1;
  end
  
  % Why is Z handled differently? TODO: Use better standards... + Maybe allow option...
  if handles.plane == 1
    handles.data_reshaped.XData = i;
    handles.data_reshaped.YData = j;
    handles.data_reshaped.ZData = k;
  elseif handles.plane == 2
    handles.data_reshaped.XData = i;
    handles.data_reshaped.YData = j;
    handles.data_reshaped.ZData = k;
  else
    handles.data_reshaped.XData = j;
    handles.data_reshaped.YData = i;
    handles.data_reshaped.ZData = k;
  end
  
  switch MainPlotType
    case 'contour'
      if ~p.Results.swap_axes
        handle_contour = contour(handles.data_reshaped.XData, handles.data_reshaped.YData, handles.data_reshaped.ZData);
      else
        %error('swap_axes not yet fully implemented (need to deal with labels and axis dimensions, .geo files, etc...)');
        handle_contour = contour(handles.data_reshaped.YData, handles.data_reshaped.XData, handles.data_reshaped.ZData);
      end
    case 'contourAtZ'
      if ~p.Results.swap_axes
        [handle_contour_ContourMatrix , handle_contour] = contourAtZ(p.Results.MainContourZposition, handles.data_reshaped.XData, handles.data_reshaped.YData, handles.data_reshaped.ZData, 'colormap', main_colormap, 'contourValues', p.Results.contourValues, 'LineWidth', p.Results.LineWidth);
      else
        [handle_contour_ContourMatrix , handle_contour] = contourAtZ(p.Results.MainContourZposition, handles.data_reshaped.YData, handles.data_reshaped.XData, handles.data_reshaped.ZData, 'colormap', main_colormap, 'contourValues', p.Results.contourValues, 'LineWidth', p.Results.LineWidth);
      end
    otherwise
      % surface plot
      % pcolor(XData, YData, ZData) % pcolor is the equivalent of imagesc for coloring by vertices instead of cells (array values considered as vertex values, not cell values)
      % TODO: How does surf() color things?
      if ~p.Results.swap_axes
        handle_surf = surf(handles.data_reshaped.XData, handles.data_reshaped.YData, handles.data_reshaped.ZData);
      else
        %error('swap_axes not yet fully implemented (need to deal with labels and axis dimensions, .geo files, etc...)');
        handle_surf = surf(handles.data_reshaped.YData, handles.data_reshaped.XData, handles.data_reshaped.ZData);
      end
  end
  
  %colave = max(fin1(:, selected_column));
  colfig = handles.AllHeaders{selected_column};

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % set caxis range
  
  if p.Results.updateCaxis
    
    % default
    caxis_range = caxis();
    
    % set range if possible
    if all(isfinite([minval, maxval]))
      % reorder min/max values...
      if maxval < minval
        minval_orig = minval;
        minval = maxval;
        maxval = minval_orig;
      end
      caxis_range = [minval, maxval];
    end
    
    % symmetric range
    if p.Results.symmetricRange
      L = max(abs(caxis_range));
      caxis_range = [-L, L];
    end
    
    % finally use range
    if all(isfinite(caxis_range)) && (caxis_range(1) < caxis_range(2))
      caxis(caxis_range);
    end
  end
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  
  %axis equal;
  AspectRatio = get(gca,'DataAspectRatio');
  AspectRatio(1) = AspectRatio(2);
  set(gca,'DataAspectRatio',AspectRatio);

  if handles.interpolate
    shading interp;
  else
    shading flat;
  end
  
  % to avoid white patches on the image
  if(not(inoctave))
    lighting phong;
  end
  
  % TODO: handle NaNs
  switch handles.plane
    case 1
      xlabel_text = 'z';
      ylabel_text = 'y';
      if p.Results.drawGeometry && geofile_loaded && handles.LimitToBox
        axis_limits = [FDTDobj.box.lower(3), FDTDobj.box.upper(3), FDTDobj.box.lower(2), FDTDobj.box.upper(2)];%, zmin,zmax,cmin,cmax];
      else
        axis_limits = [ i(1,1),i(1,size(i,2)) , j(1,1),j(size(j,1),1)];%, zmin,zmax,cmin,cmax ];
      end
    case 2
      xlabel_text = 'z';
      ylabel_text = 'x';
      if p.Results.drawGeometry && geofile_loaded && handles.LimitToBox
        axis_limits = [FDTDobj.box.lower(3), FDTDobj.box.upper(3), FDTDobj.box.lower(1), FDTDobj.box.upper(1)];%, zmin,zmax,cmin,cmax];
      else
        axis_limits = [ i(1,1),i(1,size(i,2)) , j(1,1),j(size(j,1),1)];%, zmin,zmax,cmin,cmax ];
      end
    case 3
      xlabel_text = 'x';
      ylabel_text = 'y';
      if p.Results.drawGeometry && geofile_loaded && handles.LimitToBox
        axis_limits = [FDTDobj.box.lower(1), FDTDobj.box.upper(1), FDTDobj.box.lower(2), FDTDobj.box.upper(2)];%, zmin,zmax,cmin,cmax];
      else
        axis_limits = [ j(1,1),j(size(j,1),1), i(1,1),i(1,size(i,2))];%, zmin,zmax,cmin,cmax];
      end
  end
  if ( axis_limits(1)<axis_limits(2) && axis_limits(3)<axis_limits(4) )
    if ~p.Results.swap_axes
      xlabel(xlabel_text);
      ylabel(ylabel_text);
      axis(axis_limits);
    else
      xlabel(ylabel_text);
      ylabel(xlabel_text);
      axis(axis_limits([3,4,1,2]));
    end
  end

  % for octave, but might make things easier for matlab too
  if p.Results.drawColorBar
    handle_colorbar = colorbar(p.Results.colorbarPosition);
    colorbarLabel(handle_colorbar, data_name);
  end

  % old code from unknown origin and for unknown use  
  %snapshot_filename
  %titlesnap = strread(snapshot_filename,'%s','delimiter','\\');
  %snapfile_full = char(titlesnap(length(titlesnap)));
  
  % much easier and apparently working solution...
  snapfile_full = snapshot_filename;
  disp(['snapfile_full = ',snapfile_full]);

  [ snapfile_full_folder, snapfile_full_basename, snapfile_full_ext ] = fileparts(snapfile_full);
  [ snapfile_full_folder_folder, snapfile_full_folder_basename ] = fileparts(snapfile_full_folder);
  
  title_base = [ snapfile_full_folder_basename, filesep, snapfile_full_basename, snapfile_full_ext ];
  disp(['title_base = ',title_base]);

  %%% Get object related information
  % TODO: Add support for time snapshots. Note: Requires time snapshot support in alphaID_to_numID... :(
  
  %if exist('FDTDobj','var')==1 && inpfile_loaded
  %else
    %uiwait(warndlg('No .inp file specified. You need to specify a .inp file in order to determine the properties of the snapshot. Property determination will be disabled.', 'Could not determine snapshot properties.'));
  %end
  
  %exist('FDTDobj','var')==1
  %else
    %message = ['Could not determine snapshot properties from the provided .inp file. Requested snapshot number (',num2str(Nsnap),') exceeds number of snapshots in .inp file (',num2str(length(FDTDobj.frequency_snapshots)),').'];
    %if inpfile_loaded
      %uiwait(warndlg(message, 'Could not determine snapshot properties.'));
    %else
    %end
  %end
  
  %if handles.plotSnapshotType == 2 % time snapshot
    %if exist('FDTDobj','var')==1
      %Nsnap = alphaID_to_numID([snapfile_full_basename, snapfile_full_ext], 'probe_ident', FDTDobj.flag.id, 'pre_2008_BFDTD_version', p.Results.pre_2008_BFDTD_version);
      %disp(['Nsnap = ',num2str(Nsnap)]);
      %disp(['length(FDTDobj.frequency_snapshots) = ',num2str(length(FDTDobj.frequency_snapshots))]);
      %if Nsnap <= length(FDTDobj.frequency_snapshots)
        %freq_snap_MHz = FDTDobj.frequency_snapshots(Nsnap).frequency;
        %lambda_snap_mum = get_c0()/freq_snap_MHz;
        %lambda_snap_nm = lambda_snap_mum*1e3;
        %pos_mum = FDTDobj.frequency_snapshots(Nsnap).P1(handles.plane);
      %else
      %end
    %end

  if handles.plotSnapshotType == 3 || handles.plotSnapshotType == 6 % frequency snapshot or energy snapshot
    if exist('FDTDobj','var')==1
      Nsnap = alphaID_to_numID([snapfile_full_basename, snapfile_full_ext], 'probe_ident', FDTDobj.flag.id, 'pre_2008_BFDTD_version', p.Results.pre_2008_BFDTD_version);
      disp(['Nsnap = ',num2str(Nsnap)]);
      disp(['length(FDTDobj.frequency_snapshots) = ',num2str(length(FDTDobj.frequency_snapshots))]);
      if Nsnap <= length(FDTDobj.frequency_snapshots)
        freq_snap_MHz = FDTDobj.frequency_snapshots(Nsnap).frequency;
        lambda_snap_mum = get_c0()/freq_snap_MHz;
        lambda_snap_nm = lambda_snap_mum*1e3;
        pos_mum = FDTDobj.frequency_snapshots(Nsnap).P1(handles.plane);
      else
        message = ['Could not determine snapshot frequency and position from the provided .inp file. Requested snapshot number (',num2str(Nsnap),') exceeds number of snapshots in .inp file (',num2str(length(FDTDobj.frequency_snapshots)),').'];
        if inpfile_loaded
          uiwait(warndlg(message, 'Could not determine snapshot properties.'));
        else
          uiwait(warndlg('No .inp file specified. You need to specify a .inp file in order to determine the frequency and position of the snapshot. Frequency and position determination will be disabled.', 'Could not determine snapshot properties.'));
        end
      end
    end
  
  end

  %%% Create and show title
  if p.Results.drawTitle
    if handles.plotSnapshotType == 1 % probe
      error('ERROR: Trying to plot probe with snapshot plotter');
      return;
    %elseif handles.plotSnapshotType == 2 % time snapshot
      %if exist('FDTDobj', 'var') == 1
        %if Nsnap <= length(FDTDobj.time_snapshots)
          %handle_title = title([title_base, ': ', data_name, ' at ',  num2str(lambda_snap_nm), ' nm, '], 'FontWeight', 'bold', 'Interpreter', 'none');
        %else
          %handle_title = title([title_base, ': ', data_name, ' at ',  '???', ' nm, '], 'FontWeight', 'bold', 'Interpreter', 'none');
        %end
      %else
        %handle_title = title([title_base, ': ', data_name], 'FontWeight', 'bold', 'Interpreter', 'none');
      %end
    elseif handles.plotSnapshotType == 3 || handles.plotSnapshotType == 6 % frequency or energy snapshot
      if exist('FDTDobj', 'var') == 1
        if Nsnap <= length(FDTDobj.frequency_snapshots)
          handle_title = title([title_base, ': ', data_name, ' at ',  num2str(lambda_snap_nm), ' nm, ', num2str(freq_snap_MHz),' MHz'],'FontWeight','bold','Interpreter','none');
        else
          handle_title = title([title_base, ': ', data_name, ' at ',  '???', ' nm, ', '???',' MHz'],'FontWeight','bold','Interpreter','none');
        end
      else
        handle_title = title([title_base, ': ', data_name], 'FontWeight', 'bold', 'Interpreter', 'none');
      end
    %elseif handles.plotSnapshotType == 4 % excitation template
      %handle_title = title([title_base, ': ', data_name], 'FontWeight', 'bold', 'Interpreter', 'none');
    %elseif handles.plotSnapshotType == 5 % any snapshot, but assuming energy snapshot for now, as that is the most common use case.
      %% TODO: Add a nice title for energy snapshots...
      %handle_title = title([strrep(title_base,'_','\_'), ': ', '\epsilon{}\cdot{}(E_{x}^2+E_{y}^2+E_{z}^2)'], 'FontWeight', 'bold', 'Interpreter','tex');
    %elseif handles.plotSnapshotType == 6 % energy snapshot
      %% TODO: Add a nice title for energy snapshots...
      %handle_title = title([strrep(title_base,'_','\_'), ': ', '\epsilon{}\cdot{}(E_{x}^2+E_{y}^2+E_{z}^2)'], 'FontWeight', 'bold', 'Interpreter','tex');
    else
      %warning(['Unknown data type: handles.plotSnapshotType = ', num2str(handles.plotSnapshotType)]);
      %handle_title = title(snapshot_filename,'Interpreter','none');
      handle_title = title([title_base, ': ', data_name], 'FontWeight', 'bold', 'Interpreter', 'none');
      %return;
    end
  end
  clear titlesnap;
  hold on;
  
  %% Plot Geometry Entities
  if p.Results.drawGeometry && geofile_loaded
    disp('DRAWING GEOMETRY')
    t = 0:0.1:((2*pi)+0.1);
    circle_i = cos(t);
    circle_j = sin(t);
    plotting_height_rectangle = max(data)*ones(1,5);
    plotting_height_circle = max(data)*ones(1,length(t));
    switch handles.plane
      case 1 % Z,Y
        for ii=1:length(FDTDobj.block_list)
          lower = FDTDobj.block_list(ii).lower;
          upper = FDTDobj.block_list(ii).upper;
          plot3([lower(3) lower(3) upper(3) upper(3) lower(3)],...
            [lower(2) upper(2) upper(2) lower(2) lower(2)], plotting_height_rectangle, 'Color', p.Results.LineColor, 'LineWidth', p.Results.LineWidth);
        end
        for ii=1:length(FDTDobj.cylinder_list)
          center = FDTDobj.cylinder_list(ii).center;
          inner_radius = FDTDobj.cylinder_list(ii).inner_radius;
          outer_radius = FDTDobj.cylinder_list(ii).outer_radius;
          height = FDTDobj.cylinder_list(ii).height;
          if inner_radius == 0
            I = [(center(3)-outer_radius) ...
                (center(3)+outer_radius) ...
                (center(3)+outer_radius) ...
                (center(3)-outer_radius) ...
                (center(3)-outer_radius)];
            J = [(center(2)-(height/2)) ...
                (center(2)-(height/2)) ...
                (center(2)+(height/2)) ...
                (center(2)+(height/2)) ...
                (center(2)-(height/2))];
            plot3(I,J,plotting_height_rectangle, 'Color', p.Results.LineColor,'LineWidth', p.Results.LineWidth);
          else
            I = [(center(3)-outer_radius) ...
                (center(3)-inner_radius) ...
                (center(3)-inner_radius) ...
                (center(3)-outer_radius) ...
                (center(3)-outer_radius)];
            J = [(center(2)-(height/2)) ...
                (center(2)-(height/2)) ...
                (center(2)+(height/2)) ...
                (center(2)+(height/2)) ...
                (center(2)-(height/2))];
            plot3(I,J,plotting_height_rectangle, 'Color', p.Results.LineColor,'LineWidth', p.Results.LineWidth);
            I = [(center(3)+outer_radius) ...
                (center(3)+inner_radius) ...
                (center(3)+inner_radius) ...
                (center(3)+outer_radius) ...
                (center(3)+outer_radius)];
            J = [(center(2)-(height/2)) ...
                (center(2)-(height/2)) ...
                (center(2)+(height/2)) ...
                (center(2)+(height/2)) ...
                (center(2)-(height/2))];
            plot3(I,J,plotting_height_rectangle, 'Color', p.Results.LineColor,'LineWidth', p.Results.LineWidth);
          end
          clear I J;
          if ~inoctave()
            clearvars I J;
          end
        end
        for ii=1:length(FDTDobj.sphere_list)
          center = FDTDobj.sphere_list(ii).center;
          outer_radius = FDTDobj.sphere_list(ii).outer_radius;
          inner_radius = FDTDobj.sphere_list(ii).inner_radius;
          I = (outer_radius*circle_i)+center(3);
          J = (outer_radius*circle_j)+center(2);
          plot3(I, J, plotting_height_circle, 'Color', p.Results.LineColor,'LineWidth', p.Results.LineWidth); clear I J; if ~inoctave(); clearvars I J; end;
          I = (inner_radius*circle_i)+center(3);
          J = (inner_radius*circle_j)+center(2);
          plot3(I, J, plotting_height_circle, 'Color', p.Results.LineColor,'LineWidth', p.Results.LineWidth); clear I J; if ~inoctave(); clearvars I J; end;
        end
        for ii=1:length(FDTDobj.excitations)
          lower = FDTDobj.excitations(ii).P1;
          upper = FDTDobj.excitations(ii).P2;
          plot3([lower(3) lower(3) upper(3) upper(3) lower(3)],...
            [lower(2) upper(2) upper(2) lower(2) lower(2)], plotting_height_rectangle,'r','LineWidth', p.Results.LineWidth);
        end
      case 2 % Z,X
        for ii=1:length(FDTDobj.block_list)
          lower = FDTDobj.block_list(ii).lower;
          upper = FDTDobj.block_list(ii).upper;
          plot3([lower(3) lower(3) upper(3) upper(3) lower(3)],...
            [lower(1) upper(1) upper(1) lower(1) lower(1)], plotting_height_rectangle, 'Color', p.Results.LineColor,'LineWidth', p.Results.LineWidth);
        end
        for ii=1:length(FDTDobj.cylinder_list)
          center = FDTDobj.cylinder_list(ii).center;
          inner_radius = FDTDobj.cylinder_list(ii).inner_radius;
          outer_radius = FDTDobj.cylinder_list(ii).outer_radius;
          height = FDTDobj.cylinder_list(ii).height;
          I = (outer_radius*circle_i)+center(3);
          J = (outer_radius*circle_j)+center(1);
          plot3(I, J, plotting_height_circle, 'Color', p.Results.LineColor,'LineWidth', p.Results.LineWidth); clear I J; if ~inoctave(); clearvars I J; end;
          I = (inner_radius*circle_i)+center(3);
          J = (inner_radius*circle_j)+center(1);
          plot3(I, J, plotting_height_circle, 'Color', p.Results.LineColor,'LineWidth', p.Results.LineWidth); clear I J; if ~inoctave(); clearvars I J; end;
        end
        for ii=1:length(FDTDobj.sphere_list)
          center = FDTDobj.sphere_list(ii).center;
          outer_radius = FDTDobj.sphere_list(ii).outer_radius;
          inner_radius = FDTDobj.sphere_list(ii).inner_radius;
          I = (outer_radius*circle_i)+center(3);
          J = (outer_radius*circle_j)+center(1);
          plot3(I, J, plotting_height_circle, 'Color', p.Results.LineColor,'LineWidth', p.Results.LineWidth); clear I J; if ~inoctave(); clearvars I J; end;
          I = (inner_radius*circle_i)+center(3);
          J = (inner_radius*circle_j)+center(1);
          plot3(I, J, plotting_height_circle, 'Color', p.Results.LineColor,'LineWidth', p.Results.LineWidth); clear I J; if ~inoctave(); clearvars I J; end;
        end
        for ii=1:length(FDTDobj.excitations)
          lower = FDTDobj.excitations(ii).P1;
          upper = FDTDobj.excitations(ii).P2;
          plot3([lower(3) lower(3) upper(3) upper(3) lower(3)],...
            [lower(1) upper(1) upper(1) lower(1) lower(1)], plotting_height_rectangle,'r','LineWidth', p.Results.LineWidth);
        end
      case 3 % X,Y
        for ii=1:length(FDTDobj.block_list)
          lower = FDTDobj.block_list(ii).lower;
          upper = FDTDobj.block_list(ii).upper;
          plot3([lower(1), lower(1), upper(1), upper(1), lower(1)],...
            [lower(2), upper(2), upper(2), lower(2), lower(2)], plotting_height_rectangle, 'Color', p.Results.LineColor,'LineWidth', p.Results.LineWidth);
        end
        for ii=1:length(FDTDobj.cylinder_list)
          center = FDTDobj.cylinder_list(ii).center;
          inner_radius = FDTDobj.cylinder_list(ii).inner_radius;
          outer_radius = FDTDobj.cylinder_list(ii).outer_radius;
          height = FDTDobj.cylinder_list(ii).height;
          if inner_radius == 0
            I = [(center(1)-outer_radius) ...
                (center(1)+outer_radius) ...
                (center(1)+outer_radius) ...
                (center(1)-outer_radius) ...
                (center(1)-outer_radius)];
            J = [(center(2)-(height/2)) ...
                (center(2)-(height/2)) ...
                (center(2)+(height/2)) ...
                (center(2)+(height/2)) ...
                (center(2)-(height/2))];
            plot3(I,J,plotting_height_rectangle, 'Color', p.Results.LineColor,'LineWidth', p.Results.LineWidth);
          else
            I = [(center(1)-outer_radius) ...
                (center(1)-inner_radius) ...
                (center(1)-inner_radius) ...
                (center(1)-outer_radius) ...
                (center(1)-outer_radius)];
            J = [(center(2)-(height/2)) ...
                (center(2)-(height/2)) ...
                (center(2)+(height/2)) ...
                (center(2)+(height/2)) ...
                (center(2)-(height/2))];
            plot3(I,J,plotting_height_rectangle, 'Color', p.Results.LineColor,'LineWidth', p.Results.LineWidth);
            I = [(center(1)+outer_radius) ...
                (center(1)+inner_radius) ...
                (center(1)+inner_radius) ...
                (center(1)+outer_radius) ...
                (center(1)+outer_radius)];
            J = [(center(2)-(height/2)) ...
                (center(2)-(height/2)) ...
                (center(2)+(height/2)) ...
                (center(2)+(height/2)) ...
                (center(2)-(height/2))];
            plot3(I,J,plotting_height_rectangle, 'Color', p.Results.LineColor,'LineWidth', p.Results.LineWidth);
          end
          clear I J;
          if ~inoctave(); clearvars I J; end;
        end
        for ii=1:length(FDTDobj.sphere_list)
          center = FDTDobj.sphere_list(ii).center;
          outer_radius = FDTDobj.sphere_list(ii).outer_radius;
          inner_radius = FDTDobj.sphere_list(ii).inner_radius;
          I = (outer_radius*circle_i)+center(1);
          J = (outer_radius*circle_j)+center(2);
          plot3(I, J, plotting_height_circle, 'Color', p.Results.LineColor,'LineWidth', p.Results.LineWidth); clear I J; if ~inoctave(); clearvars I J; end;
          I = (inner_radius*circle_i)+center(1);
          J = (inner_radius*circle_j)+center(2);
          plot3(I, J, plotting_height_circle, 'Color', p.Results.LineColor,'LineWidth', p.Results.LineWidth); clear I J; if ~inoctave(); clearvars I J; end;
        end
        for ii=1:length(FDTDobj.excitations)
          lower = FDTDobj.excitations(ii).P1;
          upper = FDTDobj.excitations(ii).P2;
          plot3([lower(1), lower(1), upper(1), upper(1), lower(1)],...
            [lower(2), upper(2), upper(2), lower(2), lower(2)], plotting_height_rectangle,'r','LineWidth', p.Results.LineWidth);
        end
    end
  end
  
  if handles.grid
    grid on;
  else
    grid off;
  end
  
  % set view
  view(p.Results.view);
  
  % Add contour lines from contourFile if specified:
  if p.Results.contourFile
    [handles.contour.header, handles.contour.data, handles.contour.u1, handles.contour.u2] = readPrnFile(p.Results.contourFile, 'includeAllColumns', true);
    % If u1 and u2 are requested:
    %   u1 = list of unique values in column 1 and of size N1
    %   u2 = list of unique values in column 2 and of size N2
    %   data = 3D matrix of size (N2, N1, N_data_columns) of col(3:) vs ( col(1), col(2) )
    
    if handles.plane == 2 % Y-plane
      % WARNING: We permute the meaning of u1, u2 here!!! (maybe rename vars?)
      [U1, U2] = meshgrid(handles.contour.u2, handles.contour.u1);
      handles.contour.ZData = permute(handles.contour.data, [2,1,3]);
    else % X- or Z-plane
      [U1, U2] = meshgrid(handles.contour.u1, handles.contour.u2);
      handles.contour.ZData = handles.contour.data;
    end
    
    if handles.plane == 1 % X-plane
      handles.contour.XData = U2;
      handles.contour.YData = U1;
    else % Y- or Z-plane
      handles.contour.XData = U1;
      handles.contour.YData = U2;
    end
    
    %disp('handles.plane')
    %handles.plane
    %disp('ZData')
    %size(XData)
    %size(YData)
    %size(ZData)
    %disp('handles.contour: u1, u2, columns, data')
    %size(handles.contour.u1)
    %size(handles.contour.u2)
    %size(handles.contour.header)-2
    %size(handles.contour.XData)
    %size(handles.contour.YData)
    %size(handles.contour.ZData)
    %handles.contour.XData(1,:)
    %handles.contour.YData(:,1)
    
    Zc0 = 1.1*max(handles.data_reshaped.ZData(:));
    
    %contour(handles.contour.XData, handles.contour.YData, handles.contour.ZData(:, :, p.Results.contourColumn));
    if ~p.Results.swap_axes
      [handles.contour.ContourMatrix , handles.contour.handle] = contourAtZ(Zc0, handles.contour.XData, handles.contour.YData, handles.contour.ZData(:, :, p.Results.contourColumn), 'colormap', [0,0,0], 'contourValues', p.Results.contourValues, 'LineWidth', p.Results.LineWidth);
    else
      [handles.contour.ContourMatrix , handles.contour.handle] = contourAtZ(Zc0, handles.contour.YData, handles.contour.XData, handles.contour.ZData(:, :, p.Results.contourColumn), 'colormap', [0,0,0], 'contourValues', p.Results.contourValues, 'LineWidth', p.Results.LineWidth);
    end
    
  end

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %%%%% save figure
  if islogical(p.Results.saveas) && p.Results.saveas
    %% autosave (TODO: merge both saving methods...)
    dim = length(snapshot_filename);
    figout = [snapshot_filename(1:(dim-4)), '_', colfig, '_', num2str(minval), '-', num2str(maxval)];
    if grey == 1
      figout = [figout, '_grey'];
    end
    figout = strrep(figout,'*','x'); % to avoid * in filenames
    disp(['Saving figure as ', figout]);
    %print(fig,'-dpng','-r300',figout);
    print(fig,'-dpng',[figout,'.png']);
    saveas(fig, [figout,'.fig'])
  elseif ischar(p.Results.saveas) && ~isempty(p.Results.saveas)
    %% normal saving ( with format string! :D )
    % substitution variable preparation
    [ folder, basename, ext ] = fileparts(snapshot_filename);
    % substitution
    imageSaveNameFinal = p.Results.saveas;
    imageSaveNameFinal = strrep(imageSaveNameFinal, '%DATE', datestr(now,'yyyymmdd_HHMMSS'));
    imageSaveNameFinal = strrep(imageSaveNameFinal, '%BASENAME', basename);
    imageSaveNameFinal = strrep(imageSaveNameFinal, '%FIELD', num2str(colfig));
    imageSaveNameFinal = strrep(imageSaveNameFinal, '%MIN', num2str(minval));
    imageSaveNameFinal = strrep(imageSaveNameFinal, '%MAX', num2str(maxval));
    % additional stuff for frequency snapshots
    if handles.plotSnapshotType == 3 % frequency snapshot
      if exist('FDTDobj','var')==1
        imageSaveNameFinal = strrep(imageSaveNameFinal, '%NSNAP', num2str(Nsnap));
        imageSaveNameFinal = strrep(imageSaveNameFinal, '%FREQ_SNAP_MHZ', num2str(freq_snap_MHz));
        imageSaveNameFinal = strrep(imageSaveNameFinal, '%LAMBDA_SNAP_MUM', num2str(lambda_snap_mum));
        imageSaveNameFinal = strrep(imageSaveNameFinal, '%LAMBDA_SNAP_NM', num2str(lambda_snap_nm));
        imageSaveNameFinal = strrep(imageSaveNameFinal, '%POS_MUM', num2str(pos_mum));
      end
    end
    % saving
    disp(['Saving figure as ', imageSaveNameFinal]);
    saveas(fig, imageSaveNameFinal,'fig');
    print(fig, '-dpng', '-r300', imageSaveNameFinal);
    %print(fig,'-depsc','-r1500',imageSaveNameFinal);
    
    % DO NOT CALL THIS IN INTERACTIVE MODE (otherwise the figure never shows up)
    delete(fig); %clear(fig);
  end
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  
  clear i;
  clear j;
  clear k;
  clear FDTDobj;
  if ~inoctave(); clearvars i j k FDTDobj; end;
  %clear;
  
  % TODO: Implement close(figure) or close all to prevent RAM filling when running in automated mode (hidden figures remain in memory and exiting the function does not close them)
  
  % Added to prevent RAM filling. But prevents returning values.
  %clear all;
  %clearvars -global;

  if  nargout
    ret.handles = handles;
    ret.handle_axis = gca;
    ret.handle_figure = gcf;
    if exist('handle_contour','var')
      ret.handle_contour = handle_contour;
    end
    if exist('handle_surf','var')
      ret.handle_surf = handle_surf;
    end
    if exist('handle_colorbar','var')
      ret.handle_colorbar = handle_colorbar;
    end
    if exist('handle_title','var')
      ret.handle_title = handle_title;
    end
  end

end
