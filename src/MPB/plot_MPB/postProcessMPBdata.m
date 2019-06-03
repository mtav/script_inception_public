function ret = postProcessMPBdata()
  % this function will postprocess MPB output and do coordinate conversions based on input arguments
  % The output from MPB is 4D: k1, k2, k3, a/lambda
  %%%%% command options:
  p = inputParser();
  
  % select input file
  p = inputParserWrapper(p, 'addRequired', 'filename', @ischar);
  
  % additional structure for use by the postprocessing functions (for lattice, unit cell size, etc)
  p = inputParserWrapper(p, 'addParamValue', 'data_info', mpb_DataInfo());
  
  % set verbosity:
  p = inputParserWrapper(p, 'addParamValue', 'verbosity', 1, @isnumeric);
  
  p = inputParserWrapper(p, 'parse', filename, varargin{:});
  
  % return structure
  ret.k1
  ret.k2

end
