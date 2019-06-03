function data_info = mpb_DataInfo_lattice_orthorhombic_simple(varargin)
  p = inputParser();
  
  % dimensions of the orthorhombic unit-cell
  p = inputParserWrapper(p, 'addParamValue', 'a', 1, @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'b', 1, @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'c', 1.2, @isnumeric);
  
  p = inputParserWrapper(p, 'addParamValue', 'v1', [0, 0, 1], @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'v2', [0, 1, 0], @isnumeric);
  
  p = inputParserWrapper(p, 'parse', varargin{:});
  
  data_info = mpb_DataInfo('a', 1, ...
                           'a1', [p.Results.a, 0, 0], ...
                           'a2', [0, p.Results.b, 0], ...
                           'a3', [0, 0, p.Results.c], ...
                           'v1', p.Results.v1, ...
                           'v2', p.Results.v2);
end
