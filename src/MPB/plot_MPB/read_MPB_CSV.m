function mpbdata = read_MPB_CSV(datafilename, varargin)
  % argument parsing
  p = inputParser();
  p = inputParserWrapper(p, 'addRequired', 'datafilename', @ischar);
  p = inputParserWrapper(p, 'addParamValue', 'data_info', mpb_DataInfo(), @isstruct);
  p = inputParserWrapper(p, 'addParamValue', 'klabels', {}, @iscell);
  p = inputParserWrapper(p, 'addParamValue', 'GuessCsvDelimiter', true, @islogical);
  p = inputParserWrapper(p, 'parse', datafilename, varargin{:});
  
  % initialize mpbdata structure
  mpbdata = struct();
  
  %%% read in data
  % read datafile
  [ mpbdata.rawdata.header_full, mpbdata.rawdata.data_full ] = readPrnFile(p.Results.datafilename, 'GuessCsvDelimiter', p.Results.GuessCsvDelimiter);
  
  % create more convenient arrays
  mpbdata.data.k_index = mpbdata.rawdata.data_full(:, 1);
  mpbdata.data.k_reciprocal_x = mpbdata.rawdata.data_full(:, 2);
  mpbdata.data.k_reciprocal_y = mpbdata.rawdata.data_full(:, 3);
  mpbdata.data.k_reciprocal_z = mpbdata.rawdata.data_full(:, 4);
  mpbdata.data.k_mag_over_2pi = mpbdata.rawdata.data_full(:, 5);
  mpbdata.data.normalized_frequency = mpbdata.rawdata.data_full(:, 6:end);
  
  %%% postprocess k-points
  
  % 1*N matrices
  k_reciprocal_x = reshape(mpbdata.data.k_reciprocal_x, 1, []);
  k_reciprocal_y = reshape(mpbdata.data.k_reciprocal_y, 1, []);
  k_reciprocal_z = reshape(mpbdata.data.k_reciprocal_z, 1, []);
  
  % 3*N matrix
  k_reciprocal = [k_reciprocal_x; k_reciprocal_y; k_reciprocal_z];
  
  % 3*3 matrix
  M = p.Results.data_info.reciprocal_to_cartesian;
  
  % 3*N matrix
  k_cartesian = M*k_reciprocal;
  
  k_cartesian_x = k_cartesian(1, :);
  k_cartesian_y = k_cartesian(2, :);
  k_cartesian_z = k_cartesian(3, :);
  
  % convert to spherical coordinates
  [azimuth, elevation_from_equator, r, elevation_from_Z] = cart2sph_advanced(k_cartesian_x, k_cartesian_y, k_cartesian_z);
  
  %%% create fields for postprocessed k-point data
  mpbdata.data.k_cartesian_x = k_cartesian_x(:);
  mpbdata.data.k_cartesian_y = k_cartesian_y(:);
  mpbdata.data.k_cartesian_z = k_cartesian_z(:);
  
  mpbdata.data.k_r = r(:);
  mpbdata.data.k_azimuth = azimuth(:);
  mpbdata.data.k_elevation_from_equator = elevation_from_equator(:);
  mpbdata.data.k_elevation_from_Z = elevation_from_Z(:);
  
  %%% postprocess bands
  %fn = a./lambda
  %lambda = a./fn
  mpbdata.data.wavelength = p.Results.data_info.unit_cell_size ./ mpbdata.data.normalized_frequency;
  
  %%% additional info fields
  % define special info fields for convenience
  mpbdata.info.header = mpbdata.rawdata.header_full;
  mpbdata.info.datafilename = p.Results.datafilename;
  mpbdata.info.Nkpoints = size(mpbdata.data.normalized_frequency, 1);
  mpbdata.info.Nbands = size(mpbdata.data.normalized_frequency, 2);
  
  % data_info field if needed
  mpbdata.data_info = p.Results.data_info;
  
  %%% additional k-point label field
  % set up empty k-point labels
  mpbdata.data.k_label = cell(mpbdata.info.Nkpoints, 1);
  
  % add given labels
  Nlabels = length(p.Results.klabels);
  if Nlabels > 0
    klabels_k_index = linspace(1, mpbdata.info.Nkpoints, Nlabels);
    for i = 1:Nlabels
      mpbdata.data.k_label(klabels_k_index(i)) = p.Results.klabels(i);
    end
  end
  
end
