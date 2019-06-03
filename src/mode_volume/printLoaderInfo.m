function ret = printLoaderInfo(global_info_struct, varargin)
  
  % create parser
  p = inputParser();
  p = inputParserWrapper(p, 'addRequired', 's', @isstruct);
  p = inputParserWrapper(p, 'addOptional', 'prefix', '', @ischar);
  p = inputParserWrapper(p, 'parse', global_info_struct, varargin{:});
  
  ret = '';
  ret = [ret, name, ' = ', value_string];
  
  ret = [ret, 'snap_time_number_fsnap:\n'];
  ret = [ret, 'time_snapshots:\n'];
  ret = [ret, 'frequency_snapshots:\n'];
  ret = [ret, 'frequency_set:\n'];
  ret = [ret, 'defect_properties:\n'];
  
  fprintf(fid, 'snap_time_number_fsnap:\n');
  
  snap_time_number_fsnap: 1x1 scalar
  time_snapshots: 1x1 scalar struct
  frequency_snapshots: 1x1 scalar struct
  frequency_set: 1x1 scalar
  defect_properties: 1x1 scalar struct
  
end
