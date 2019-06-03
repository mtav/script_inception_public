function [snap_time_number_max, snap_time_number_list] = getLastSnapTimeNumber(workdir, prefix, varargin)
  % function snap_time_number_max = getLastSnapTimeNumber(workdir, prefix, varargin)
  %
  % Arguments:
  %  Required:
  %   workdir: string
  %   prefix: string
  %  Parameter-value pairs:
  %   'pre_2008_BFDTD_version': true (version<2008) or false (version>=2008) (important if more than 52 snapshots are used!). The default is 'false'.
  %   'probe_ident': Default='_id_'
  % 
  % TODO: part_1/part_2 searcher, multidir, etc, recursive search, etc
  % TODO: return corresponding file, etc

  %%%%%%%%
  % create parser
  p = inputParser();
  p = inputParserWrapper(p, 'addRequired', 'workdir', @isdir);
  p = inputParserWrapper(p, 'addRequired', 'prefix', @ischar);
  p = inputParserWrapper(p, 'addParamValue', 'probe_ident', '_id_', @ischar);
  p = inputParserWrapper(p, 'addParamValue', 'pre_2008_BFDTD_version', false, @islogical);

  % parse arguments
  p = inputParserWrapper(p, 'parse', workdir, prefix, varargin{:});
  %%%%%%%%

  snap_time_number_max = -Inf;
  snap_time_number_list = [];
  
  files = dir([workdir, filesep, prefix, '*.prn']);
  for file = files'
  
    if ~isempty(regexp(file.name,'^[xyz][a-z{|}~][a-z{]?.*\d\d\.(prn|dat)$','ignorecase'))

      alphaID = file.name;
      [ numID, snap_plane, snap_time_number ] = alphaID_to_numID(alphaID, 'probe_ident', p.Results.probe_ident, 'pre_2008_BFDTD_version', p.Results.pre_2008_BFDTD_version);
      snap_time_number_list(end+1) = snap_time_number;
      if snap_time_number > snap_time_number_max
        snap_time_number_max = snap_time_number;
      end

    end

  end

  snap_time_number_list =  sort(snap_time_number_list);

end
