function ret = bfdtdLoadData(bfdtd_file_list, varargin)
  % reads in BFDTD data and returns it as 3D meshgrid data
  
  % deprecated and now implemented in BFDTD_loadVolumetricData

  % parse args
  p = inputParser();
  p = inputParserWrapper(p, 'addRequired', 'bfdtd_file_list', @iscellstr);
  p = inputParserWrapper(p, 'parse', bfdtd_file_list, varargin{:});
  
  % read input files
  
  % initialize meshgrid data based on bfdtd mesh (mesh_data)
  
  % read snapshot files
  
  % initialize meshgrid data based on snapshot files (snapshot_data)
  
  % fill mesh_data based on snapshot_data
  
end
