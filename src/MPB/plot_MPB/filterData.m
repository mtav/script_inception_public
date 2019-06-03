function mpbdata_selection = filterData(mpbdata, varargin)
  %%%%% command options:
  p = inputParser();
  
  p = inputParserWrapper(p, 'addRequired', 'mpbdata', @ischar);
  
  % limit data ranges
  p = inputParserWrapper(p, 'addParamValue', 'k_point_indices', [], @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'bands', [], @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'azimuth_list', [], @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'tol', 1e-10, @isnumeric);
  
  % set verbosity:
  p = inputParserWrapper(p, 'addParamValue', 'verbosity', 1, @isnumeric);
  
  p = inputParserWrapper(p, 'parse', filename, varargin{:});
  
  %%%%% filter by bands
end
