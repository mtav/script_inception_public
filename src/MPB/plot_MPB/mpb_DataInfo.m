function data_info = mpb_DataInfo(varargin)
  p = inputParser();
  
  p = inputParserWrapper(p, 'addParamValue', 'a', 1, @isnumeric);
  
  p = inputParserWrapper(p, 'addParamValue', 'a1', [1,0,0], @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'a2', [0,1,0], @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'a3', [0,0,1], @isnumeric);
  
  p = inputParserWrapper(p, 'addParamValue', 'v1', [0, 0, 1], @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'v2', [0, 1, 0], @isnumeric);
  
  p = inputParserWrapper(p, 'parse', varargin{:});
  
  data_info = struct();
  
  data_info.unit_cell_size = p.Results.a;
  
  % defined in cartesian
  data_info.lattice.a1 = p.Results.a1;
  data_info.lattice.a2 = p.Results.a2;
  data_info.lattice.a3 = p.Results.a3;
  
  % defined in cartesian
  data_info.reciprocal_lattice.b1 = cross(p.Results.a2, p.Results.a3) / dot(p.Results.a1, cross(p.Results.a2, p.Results.a3));
  data_info.reciprocal_lattice.b2 = cross(p.Results.a3, p.Results.a1) / dot(p.Results.a1, cross(p.Results.a2, p.Results.a3));
  data_info.reciprocal_lattice.b3 = cross(p.Results.a1, p.Results.a2) / dot(p.Results.a1, cross(p.Results.a2, p.Results.a3));
  
  % We define a reference basis for angle calculation.
  % v1 and v2 define an incidence plane, with v1 becoming the "Z vector" from which to define the polar angle
  data_info.angle_reference_basis.u = cross(p.Results.v2, p.Results.v1);
  data_info.angle_reference_basis.v = cross(p.Results.v1, data_info.angle_reference_basis.u);
  data_info.angle_reference_basis.w = p.Results.v1;
  
  % create conversion matrices
  data_info.lattice_to_cartesian = [data_info.lattice.a1(:), data_info.lattice.a2(:), data_info.lattice.a3(:)];
  data_info.reciprocal_to_cartesian = [data_info.reciprocal_lattice.b1(:), data_info.reciprocal_lattice.b2(:), data_info.reciprocal_lattice.b3(:)];
  
  data_info.cartesian_to_lattice = data_info.lattice_to_cartesian^-1;
  data_info.cartesian_to_reciprocal = data_info.reciprocal_to_cartesian^-1;
  
  data_info.reciprocal_to_lattice = data_info.cartesian_to_lattice * data_info.reciprocal_to_cartesian;
  data_info.lattice_to_reciprocal = data_info.reciprocal_to_lattice^-1;
  
end
