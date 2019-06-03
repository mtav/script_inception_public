function ret = BFDTD_getSlicingInfo(structured_entries, varargin)
  % function ret = BFDTD_getSlicingInfo(structured_entries, varargin)
  %
  % -returns snapshot counts by type
  % -returns direction with most snapshots of requested type
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % default
  ret = struct();
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % input parsing
  snap_type_list = {'xe','ye','ze',...
                    'xf','yf','zf',...
                    'xt','yt','zt'};
  snap_type_list_input = {snap_type_list{:},...
                          'x','y','z',...
                          'e','f','t',...
                          'auto'};
  
  % create parser
  p = inputParser();
  p = inputParserWrapper(p, 'addRequired', 'structured_entries', @isstruct);
  p = inputParserWrapper(p, 'addParamValue', 'snap_type', 'auto', @(x) any(validatestring(x, snap_type_list_input)));
  p = inputParserWrapper(p, 'addParamValue', 'pre_2008_BFDTD_version', false, @islogical);
  p = inputParserWrapper(p, 'addParamValue', 'fsnap_folder', '.', @ischar);
  p = inputParserWrapper(p, 'addParamValue', 'numID_list', [], @isnumeric);
  p = inputParserWrapper(p, 'parse', structured_entries, varargin{:});
  
  % define snap_type_requested
  snap_type_requested = validatestring(p.Results.snap_type, snap_type_list_input);
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % count snapshots
  ret.all.Nxe = numel(structured_entries.epsilon_snapshots_X);
  ret.all.Nye = numel(structured_entries.epsilon_snapshots_Y);
  ret.all.Nze = numel(structured_entries.epsilon_snapshots_Z);
  ret.all.Nxf = numel(structured_entries.frequency_snapshots_X);
  ret.all.Nyf = numel(structured_entries.frequency_snapshots_Y);
  ret.all.Nzf = numel(structured_entries.frequency_snapshots_Z);
  ret.all.Nxt = numel(structured_entries.time_snapshots_X);
  ret.all.Nyt = numel(structured_entries.time_snapshots_Y);
  ret.all.Nzt = numel(structured_entries.time_snapshots_Z);
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % prepare lists
  Nsnaps_list = [ret.all.Nxe,... % 1
                 ret.all.Nye,... % 2
                 ret.all.Nze,... % 3
                 ret.all.Nxf,... % 4
                 ret.all.Nyf,... % 5
                 ret.all.Nzf,... % 6
                 ret.all.Nxt,... % 7
                 ret.all.Nyt,... % 8
                 ret.all.Nzt]; % 9

  slicing_direction_index_list = [1,2,3,...
                                  1,2,3,...
                                  1,2,3];

  snap_plane_list = {'x','y','z',...
                     'x','y','z',...
                     'x','y','z'};
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  
  % define selection
  switch snap_type_requested
    case snap_type_list
      selection = find(strcmpi(snap_type_requested, snap_type_list), 1);
    case 'x'
      selection = [1,4,7];
    case 'y'
      selection = [2,5,8];
    case 'z'
      selection = [3,6,9];
    case 'e'
      selection = [1,2,3];
    case 'f'
      selection = [4,5,6];
    case 't'
      selection = [7,8,9];
    case 'auto'
      selection = 1:9;
    otherwise
      error('Unsupported snap_type_requested = %s', snap_type_requested);
  end
  
  % restrict lists to selection
  snap_type_list_selection = snap_type_list(selection);
  snap_plane_list_selection = snap_plane_list(selection);
  Nsnaps_list_selection = Nsnaps_list(selection);
  slicing_direction_index_list_selection = slicing_direction_index_list(selection);
  
  % find max
  [Nsnaps, idx] = max(Nsnaps_list_selection);
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % fill return structure
  ret.snap_type = snap_type_list_selection{idx};
  ret.snap_plane = snap_plane_list_selection{idx};
  ret.Nsnaps = Nsnaps_list_selection(idx);
  ret.slicing_direction_index = slicing_direction_index_list_selection(idx);
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % TODO: get snapshot extension... (avoid duplication in 3D loader...)
  
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % get latest snap_time_number_fsnap
  ret.snap_time_number_fsnap = NaN;
  frequency_list = [];
  
  numID_list = p.Results.numID_list;
  if isempty(numID_list)
    numID_list = 1:numel(structured_entries.frequency_snapshots);
  end
  
  % loop through all frequency snapshots
  for numID = numID_list
    snapshot = structured_entries.frequency_snapshots(numID);
    frequency_list(end+1) = snapshot.frequency;
    
    [ fsnap_filename, fsnap_alphaID, fsnap_pair ] = numID_to_alphaID_FrequencySnapshot(numID, 'snap_plane', snapshot.plane_letter, 'probe_ident', structured_entries.flag.id, 'snap_time_number', 0, 'pre_2008_BFDTD_version', p.Results.pre_2008_BFDTD_version);
    prefix = [snapshot.plane_letter, fsnap_alphaID, structured_entries.flag.id];
    ret.snap_time_number_fsnap = getLastSnapTimeNumber(p.Results.fsnap_folder, prefix, 'probe_ident', structured_entries.flag.id, 'pre_2008_BFDTD_version', p.Results.pre_2008_BFDTD_version);
    if ret.snap_time_number_fsnap < 0
      error(['Failed to automatically determine snap_time_number_fsnap, most likely due to missing .prn files in fsnap_folder = "', p.Results.fsnap_folder, '"']);
    end
  end
  
end
