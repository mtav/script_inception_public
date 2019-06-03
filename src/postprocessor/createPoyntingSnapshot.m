function [new_header, new_data, outfile, total] = createPoyntingSnapshot(fsnap, varargin)
  % function [new_header, new_data, outfile, total] = createPoyntingSnapshot(fsnap, varargin)
  %
  % Converts a frequency snapshot into a snapshot containing the poynting vector components and modulus.
  % Poynting vector unit: W/m^2
  %
  % Example usage:
  %   [new_header, new_data, outfile, total] = createPoyntingSnapshot('xd_id_00.prn'); % do not create any files
  %   [new_header, new_data, outfile, total] = createPoyntingSnapshot('xd_id_00.prn', 'out.prn'); % save output snapshot to 'out.prn'
  %   [new_header, new_data, outfile, total] = createPoyntingSnapshot('xd_id_00.prn', true); % save output snapshot using default output filename (ex: 'xd_id_00_poynting.prn')

  %%%%%%%%
  % create parser
  p = inputParser();
  p = inputParserWrapper(p, 'addRequired', 'fsnap', @ischar);
  p = inputParserWrapper(p, 'addOptional', 'save', false, @(x) islogical(x) || ischar(x));
  
  % parse arguments
  p = inputParserWrapper(p, 'parse', fsnap, varargin{:});
  %%%%%%%%
  
  % check that the files exist
  if ~exist(fsnap, 'file')
    error('createPoyntingSnapshot:FileNotFound', ['File not found: ', fsnap]);
  end
  
  % read in data
  [header_fsnap, data_fsnap, column_1_fsnap, column_2_fsnap] = readPrnFile(fsnap);

  %% Assign data columns to field values
  % TODO: Do string searches to get proper fields, dictionary-style lookup. -> Should be done in readPrnFile or similar and return directly usable structure...
  Ex.re = data_fsnap(:,:,4-2); Ex.im = data_fsnap(:,:,5-2);
  Ey.re = data_fsnap(:,:,7-2); Ey.im = data_fsnap(:,:,8-2);
  Ez.re = data_fsnap(:,:,10-2); Ez.im = data_fsnap(:,:,11-2);
  Hx.re = data_fsnap(:,:,13-2); Hx.im = data_fsnap(:,:,14-2);
  Hy.re = data_fsnap(:,:,16-2); Hy.im = data_fsnap(:,:,17-2);
  Hz.re = data_fsnap(:,:,19-2); Hz.im = data_fsnap(:,:,20-2);

  % calculate new data
  Sx = poynting(Ey,Hy,Ez,Hz);
  Sy = poynting(Ez,Hz,Ex,Hx);
  Sz = poynting(Ex,Hx,Ey,Hy);
  Smod = sqrt(Sx.^2 + Sy.^2 + Sz.^2);
  
  % build new header
  new_header = {header_fsnap{1}, header_fsnap{2}, 'Sx', 'Sy', 'Sz', 'Smod'};
  % build new data
  new_data = cat(3, Sx, Sy, Sz, Smod);
  
  % TODO: integrate over plane, should have general function which can integrate any of the field components... -> h5/vtk 3D storage for easier processing/visualization...
  column_1_fsnap_cellsize = [(column_1_fsnap(2) - column_1_fsnap(1))/2; (column_1_fsnap(3:end) - column_1_fsnap(1:end-2))/2; (column_1_fsnap(end) - column_1_fsnap(end-1))/2];
  column_2_fsnap_cellsize = [(column_2_fsnap(2) - column_2_fsnap(1))/2; (column_2_fsnap(3:end) - column_2_fsnap(1:end-2))/2; (column_2_fsnap(end) - column_2_fsnap(end-1))/2];

  % data_fsnap has dimensions [size(col2), size(col1)] and vi,vj are column vectors, hence the following area matrix for the integration:
  areaM = column_2_fsnap_cellsize * column_1_fsnap_cellsize';
  
  total.Sx = sum(sum(Sx.*areaM));
  total.Sy = sum(sum(Sy.*areaM));
  total.Sz = sum(sum(Sz.*areaM));
  total.Smod = sum(sum(Smod.*areaM));

  % write poynting snapshot to outfile
  outfile = '';
  if ( islogical(p.Results.save) && p.Results.save == true )
    outfile = fullfile( dirname(fsnap), [basename(fsnap, '.prn'), '_poynting.prn']);
  elseif ischar(p.Results.save) && ~isempty(p.Results.save)
    outfile = p.Results.save;
  end
  if ~isempty(outfile)
    disp(['Saving poynting snapshot as ', basename(outfile)]);
    writePrnFile(outfile, new_header, new_data, column_1_fsnap, column_2_fsnap);
  end
  
end
