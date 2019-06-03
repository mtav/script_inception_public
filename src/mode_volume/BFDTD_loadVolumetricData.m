function ret = BFDTD_loadVolumetricData(varargin)
  % function to convert snapshot data into a 4D matrix (x, y, z, data_column)
  %
  % TODO: ability to load multiple ones in one go to avoid using too much RAM!
  % TODO: use sparse matrices
  % TODO: allow subvolume selection if mesh too big (via absolute/relative coords/indices)
  % TODO: mode/frequency selection if frequency snapshots were taken at varying frequencies... -> requires very flexible snapshot selection, easier solution would be to simply split .inp files... (but careful with BFDTD filenaming and snapshot indexing...) -> again BFDTD needs improvements upstream!!!
  % TODO: compute energy density directly if requested as field instead of storing Emod values to reduce RAM usage
  % TODO: store all in single dataset or separate datasets? named tables?:
  % --separate datasets: easier access -> range restriction could be done via a function
  % --single datasets: easier range restriction -> access can be simplified with getter functions, field additions/removal a bit difficult
  
  % default
  ret = struct();
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %snap_type_list = {'xe','ye','ze',...
                    %'xf','yf','zf',...
                    %'xt','yt','zt'};
  %snap_type_list_input = {snap_type_list{:},...
                          %'x','y','z',...
                          %'e','f','t',...
                          %'auto'};
  %%%%% create parser
  p = inputParser();
  p = inputParserWrapper(p, 'addParamValue', 'mesh_file', '', @ischar);
  p = inputParserWrapper(p, 'addParamValue', 'inpfile_list', {}, @iscellstr);
  p = inputParserWrapper(p, 'addParamValue', 'fsnap_folder', '', @ischar);
  %p = inputParserWrapper(p, 'addParamValue', 'eps_folder', '.', @ischar);
  %p = inputParserWrapper(p, 'addParamValue', 'snap_type', 'auto', @(x) any(validatestring(x, snap_type_list_input)));
  p = inputParserWrapper(p, 'addParamValue', 'snap_time_number_tsnap', 1, @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'snap_time_number_fsnap', NaN, @isnumeric); % if not given, it will be automatically determined
  %p = inputParserWrapper(p, 'addParamValue', 'numID_list', [], @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'numID_list', [], @(x) isnumeric(x) || iscell(x));
  p = inputParserWrapper(p, 'addParamValue', 'columns', {'material', 'Exmod', 'Eymod', 'Ezmod'}, @iscell);
  p = inputParserWrapper(p, 'addParamValue', 'justCheck', false, @islogical);
  p = inputParserWrapper(p, 'addParamValue', 'pre_2008_BFDTD_version', false, @islogical);
  p = inputParserWrapper(p, 'addParamValue', 'DataSizeMax', 200e6, @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'probe_ident', '', @ischar); % normally read from .inp file, but this can be used if flag is missing, or to override flag settings
  p = inputParserWrapper(p, 'addParamValue', 'loadGeometry', true, @islogical);
  p = inputParserWrapper(p, 'addParamValue', 'verbosity', 1, @isnumeric);
  
  p = inputParserWrapper(p, 'parse', varargin{:});
  
  % define snap_type_requested
  %snap_type_requested = validatestring(p.Results.snap_type, snap_type_list_input);
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % ask for files if not specified
  
  mesh_file = p.Results.mesh_file;
  if ~ischar(mesh_file) || isempty(mesh_file)
    [FNAME, FPATH, FLTIDX] = uigetfile('*.inp', 'Select a .inp file for the mesh');
    if ~ischar(FNAME) || isempty(FNAME)
      error('No file selected. Exiting');
      return
    else
      mesh_file = fullfile(FPATH, FNAME);
    end
  end
  
  inpfile_list = p.Results.inpfile_list;
  if isempty(inpfile_list)
    if inoctave()
      inpfile_list = {mesh_file};
    else
      rdir_output = rdir(fullfile('*', 'part_*', '*.inp'));
      inpfile_list = uipickfiles('FilterSpec', '*.inp', 'Prompt', 'Select .inp files containing the epsilon and frequency snapshots.', 'Append', rdir_output);
      if ~iscell(inpfile_list)
        error('No files selected for epsilon and frequency snapshots.');
      end
    end
  end
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % store original dir to deal with relative pathnames
  original_directory = pwd();
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % prepare data storage based on mesh_file
  
  fprintf('Loading mesh from %s\n', mesh_file);

  % read BFDTD input files
  %pwd
  %mesh_file
  %[mesh_file_inpEntries, mesh_file_structured_entries] = GEO_INP_reader({mesh_file});
  [mesh_file_structured_entries, mesh_file_inpEntries] = readBristolFDTD({mesh_file}, 'loadGeometry', p.Results.loadGeometry);
  
  % convert meshDeltas to a real position mesh
  xmesh = [0; cumsum(mesh_file_structured_entries.xmesh(:))];
  ymesh = [0; cumsum(mesh_file_structured_entries.ymesh(:))];
  zmesh = [0; cumsum(mesh_file_structured_entries.zmesh(:))];
  
  % compute data size
  % TODO: predict required memory (cf whos()+memory() output, in Octave: numel()*8 bytes)
  Nx = numel(xmesh);
  Ny = numel(ymesh);
  Nz = numel(zmesh);
  Nd = length(p.Results.columns);
  Npts = Nx*Ny*Nz;
  data_size = Npts * (Nd + 3 + 1);
  fprintf('Npts = %e\n', Npts);
  fprintf('data_size = %e\n', data_size);
  if data_size > p.Results.DataSizeMax
    error('Data size too big: data_size = %e*%e = %e > %e (increase DataSizeMax if needed)', Npts, Nd, data_size, p.Results.DataSizeMax);
  end

  % initialize data storage
  [ret.data.X, ret.data.Y, ret.data.Z] = meshgrid(xmesh, ymesh, zmesh);
  ret.data.dV = BFDTD_getCellVolumes(xmesh, ymesh, zmesh);
  %ret.data.D = NaN * ones([size(ret.data.X), Nd]);
  %ret.data.D = NaN([size(ret.data.X), Nd]); % this would be nice to know where no data was available
  ret.data.D = zeros([size(ret.data.X), Nd]); % this makes integration easier
  ret.data.header = p.Results.columns;
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % automatic snap_time_number_fsnap choice
  ret.info.snap_time_number_fsnap = p.Results.snap_time_number_fsnap;
  if isempty(ret.info.snap_time_number_fsnap) || isnan(ret.info.snap_time_number_fsnap)
    [ret.info.snap_time_number_fsnap, snap_time_number_fsnap_info] = getLastSnapTimeNumberOverall(inpfile_list, 'pre_2008_BFDTD_version', p.Results.pre_2008_BFDTD_version);
    fprintf('total_frequency_snapshots = %d\n', snap_time_number_fsnap_info.total_frequency_snapshots);
    if snap_time_number_fsnap_info.total_frequency_snapshots > 0
      if isempty(ret.info.snap_time_number_fsnap) || isnan(ret.info.snap_time_number_fsnap)
        error('Could not find a common snap_time_number for frequency snapshots.');
      end
    end
  end
  
  fprintf('Using snap_time_number_fsnap = %d\n', ret.info.snap_time_number_fsnap);
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  
  % set up some variables
  frequency_list = [];
  
  ret.info.time_snapshots.xmin = Inf;
  ret.info.time_snapshots.ymin = Inf;
  ret.info.time_snapshots.zmin = Inf;
  ret.info.time_snapshots.xmax = -Inf;
  ret.info.time_snapshots.ymax = -Inf;
  ret.info.time_snapshots.zmax = -Inf;
  
  ret.info.frequency_snapshots.xmin = Inf;
  ret.info.frequency_snapshots.ymin = Inf;
  ret.info.frequency_snapshots.zmin = Inf;
  ret.info.frequency_snapshots.xmax = -Inf;
  ret.info.frequency_snapshots.ymax = -Inf;
  ret.info.frequency_snapshots.zmax = -Inf;
  
  % numID_list hack to support separate lists per .inp files
  if iscell(p.Results.numID_list)
    numID_list_per_inp = p.Results.numID_list;
  else
    numID_list_per_inp = {p.Results.numID_list};
  end
  
  % loop through .inp files
  for inpfile_idx = 1:numel(inpfile_list)
    inpfile = inpfile_list{inpfile_idx};
    fprintf('Processing file %d/%d: inpfile = %s\n', inpfile_idx, numel(inpfile_list), inpfile);
    
    cd(original_directory);
    cd(dirname(inpfile));
    %[inpEntries, structured_entries] = GEO_INP_reader({basename(inpfile)});
    [structured_entries, inpEntries] = readBristolFDTD({basename(inpfile)}, 'loadGeometry', p.Results.loadGeometry);
    
    % allow manual flag ID override if flag entry is missing (or if desired)
    probe_ident = structured_entries.flag.id;
    if ~isempty(p.Results.probe_ident) > 0
      probe_ident = p.Results.probe_ident;
    end
    
    % define numID_list_current
    numID_list_current = numID_list_per_inp{ mod(inpfile_idx - 1, numel(numID_list_per_inp)) + 1 };
    
    % loop through all time snapshots
    fprintf('Loading time snapshots...\n');
    numID_list_tsnap = 1:numel(structured_entries.time_snapshots);
    if ~isempty(numID_list_current)
      numID_list_tsnap = intersect(numID_list_tsnap, numID_list_current);
    end
    waitbar_handle = waitbarSmart( 0, sprintf('%d/%d', 0, numel(structured_entries.time_snapshots)));
    for numID = numID_list_tsnap
      
      % fprintf('%d/%d%s', numID, numel(structured_entries.time_snapshots), sprintf('\r'));
      waitbarSmart( numID ./ numel(structured_entries.time_snapshots), waitbar_handle, sprintf('File %d/%d: Loading time snapshots: %d/%d', inpfile_idx, numel(inpfile_list), numID, numel(structured_entries.time_snapshots)));
      
      % get snapshot parameters
      snapshot = structured_entries.time_snapshots(numID);
      
      % update snapshot range info
      ret.info.time_snapshots.xmin = min([ret.info.time_snapshots.xmin, snapshot.P1(1), snapshot.P2(1)]);
      ret.info.time_snapshots.ymin = min([ret.info.time_snapshots.ymin, snapshot.P1(2), snapshot.P2(2)]);
      ret.info.time_snapshots.zmin = min([ret.info.time_snapshots.zmin, snapshot.P1(3), snapshot.P2(3)]);
      ret.info.time_snapshots.xmax = max([ret.info.time_snapshots.xmax, snapshot.P1(1), snapshot.P2(1)]);
      ret.info.time_snapshots.ymax = max([ret.info.time_snapshots.ymax, snapshot.P1(2), snapshot.P2(2)]);
      ret.info.time_snapshots.zmax = max([ret.info.time_snapshots.zmax, snapshot.P1(3), snapshot.P2(3)]);
      
      % get filename
      [ snapshot.snap_filename, alphaID, pair ] = numID_to_alphaID_TimeSnapshot(numID, snapshot.plane_letter, probe_ident, p.Results.snap_time_number_tsnap);
      
      %if ~exist(snapshot.snap_filename, 'file')
      if ~existFileOutsideLoadPath(snapshot.snap_filename)
        delete(waitbar_handle);
        error('File not found: %s', snapshot.snap_filename);
      end
      
      % exit if justCheck=true
      if p.Results.justCheck
        continue
      end
      
      % load+process data
      [snap_header, snap_data_fixed, idx_range] = BFDTD_processSlice(snapshot, xmesh, ymesh, zmesh);
      
      % load planar slices of data into volumetric data object
      for column_idx_in_request = 1:numel(p.Results.columns)
        column_name = p.Results.columns{column_idx_in_request};
        column_idx_in_header = find(strcmpi(column_name, snap_header), 1);
        if ~isempty(column_idx_in_header)
          ret.data.D(idx_range.ymin:idx_range.ymax, idx_range.xmin:idx_range.xmax, idx_range.zmin:idx_range.zmax, column_idx_in_request) = snap_data_fixed(:, :, column_idx_in_header);
        end
      end
    
    end
    % fprintf('\n');
    delete(waitbar_handle);
    
    % loop through all frequency snapshots
    fprintf('Loading frequency snapshots...\n');
    numID_list_fsnap = 1:numel(structured_entries.frequency_snapshots);
    if ~isempty(numID_list_current)
      numID_list_fsnap = intersect(numID_list_fsnap, numID_list_current);
    end
    waitbar_handle = waitbarSmart( 0, sprintf('%d/%d', 0, numel(structured_entries.frequency_snapshots)));
    for numID = numID_list_fsnap
      
      % fprintf('%d/%d%s', numID, numel(structured_entries.frequency_snapshots), sprintf('\r'));
      waitbarSmart( numID ./ numel(structured_entries.frequency_snapshots), waitbar_handle, sprintf('File %d/%d: Loading frequency snapshots: %d/%d', inpfile_idx, numel(inpfile_list), numID, numel(structured_entries.frequency_snapshots)));
      
      % get snapshot parameters
      snapshot = structured_entries.frequency_snapshots(numID);
      frequency_list(end+1) = snapshot.frequency;
      
      % update snapshot range info
      ret.info.frequency_snapshots.xmin = min([ret.info.frequency_snapshots.xmin, snapshot.P1(1), snapshot.P2(1)]);
      ret.info.frequency_snapshots.ymin = min([ret.info.frequency_snapshots.ymin, snapshot.P1(2), snapshot.P2(2)]);
      ret.info.frequency_snapshots.zmin = min([ret.info.frequency_snapshots.zmin, snapshot.P1(3), snapshot.P2(3)]);
      ret.info.frequency_snapshots.xmax = max([ret.info.frequency_snapshots.xmax, snapshot.P1(1), snapshot.P2(1)]);
      ret.info.frequency_snapshots.ymax = max([ret.info.frequency_snapshots.ymax, snapshot.P1(2), snapshot.P2(2)]);
      ret.info.frequency_snapshots.zmax = max([ret.info.frequency_snapshots.zmax, snapshot.P1(3), snapshot.P2(3)]);
      
      % get filename
      [ snapshot.snap_filename, alphaID, pair ] = numID_to_alphaID_FrequencySnapshot(numID, 'snap_plane', snapshot.plane_letter, 'probe_ident', probe_ident, 'snap_time_number', ret.info.snap_time_number_fsnap, 'pre_2008_BFDTD_version', p.Results.pre_2008_BFDTD_version);
      
      if ~exist(snapshot.snap_filename, 'file')
        delete(waitbar_handle);
        error('File not found: %s', snapshot.snap_filename);
      end
      
      % exit if justCheck=true
      if p.Results.justCheck
        continue
      end
      
      % load+process data
      [snap_header, snap_data_fixed, idx_range] = BFDTD_processSlice(snapshot, xmesh, ymesh, zmesh);
      
      % load planar slices of data into volumetric data object
      for column_idx_in_request = 1:numel(p.Results.columns)
        column_name = p.Results.columns{column_idx_in_request};
        column_idx_in_header = find(strcmpi(column_name, snap_header), 1);
        if ~isempty(column_idx_in_header)
          ret.data.D(idx_range.ymin:idx_range.ymax, idx_range.xmin:idx_range.xmax, idx_range.zmin:idx_range.zmax, column_idx_in_request) = snap_data_fixed(:, :, column_idx_in_header);
        end
      end
    
    end
    % fprintf('\n');
    delete(waitbar_handle);
  
  end
  
  ret.info.frequency_set = unique(frequency_list);
  
  ret.info.time_snapshots.Lx = abs(ret.info.time_snapshots.xmax - ret.info.time_snapshots.xmin);
  ret.info.time_snapshots.Ly = abs(ret.info.time_snapshots.ymax - ret.info.time_snapshots.ymin);
  ret.info.time_snapshots.Lz = abs(ret.info.time_snapshots.zmax - ret.info.time_snapshots.zmin);
  ret.info.time_snapshots.volume = ret.info.time_snapshots.Lx*ret.info.time_snapshots.Ly*ret.info.time_snapshots.Lz;

  ret.info.frequency_snapshots.Lx = abs(ret.info.frequency_snapshots.xmax - ret.info.frequency_snapshots.xmin);
  ret.info.frequency_snapshots.Ly = abs(ret.info.frequency_snapshots.ymax - ret.info.frequency_snapshots.ymin);
  ret.info.frequency_snapshots.Lz = abs(ret.info.frequency_snapshots.zmax - ret.info.frequency_snapshots.zmin);
  ret.info.frequency_snapshots.volume = ret.info.frequency_snapshots.Lx*ret.info.frequency_snapshots.Ly*ret.info.frequency_snapshots.Lz;
  
  cd(original_directory);
  
end
