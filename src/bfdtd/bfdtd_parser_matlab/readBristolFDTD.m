function [ structured_entries, entries ] = readBristolFDTD(bfdtd_file_list, varargin)
  % function [ structured_entries, entries ] = readBristolFDTD(bfdtd_file_list, varargin)
  %
  % readBristolFDTD() can take a single filename or a cell array of filenames.
  % WARNING: It returns [ structured_entries, entries ] unlike GEO_INP_reader()!
  %
  % [ structured_entries, entries ] = readBristolFDTD(bfdtd_file_list, varargin)
  % replaces the old:
  % [ entries, structured_entries ] = GEO_INP_reader(file_list)
  %
  % It can take a single filename or a cell array of filenames.
  % Any mix of .in, .inp or .geo files is allowed.
  
  %%%%%%%%%%%%%
  % parse args
  p = inputParser();
  p = inputParserWrapper(p, 'addRequired', 'bfdtd_file_list', @(x) iscellstr(x) || ischar(x));
  p = inputParserWrapper(p, 'addParamValue', 'loadGeometry', true, @islogical);
  p = inputParserWrapper(p, 'parse', bfdtd_file_list, varargin{:});
  %%%%%%%%%%%%%
  
  if ischar(p.Results.bfdtd_file_list)
    bfdtd_file_list = {p.Results.bfdtd_file_list};
  else
    bfdtd_file_list = p.Results.bfdtd_file_list;
  end
  
  entries = {};
  structured_entries = FDTDstructure();
  
  for bfdtd_file_list_idx = 1:length(bfdtd_file_list)
    
    filename = bfdtd_file_list{bfdtd_file_list_idx};
    % fprintf('readBristolFDTD: processing: %s\n', filename);
    
    [DIR, NAME, EXT] = fileparts (filename);
    
    if strcmpi(EXT, '.in')
      [ structured_entries, entries ] = readFileList(filename, structured_entries, entries, 'loadGeometry', p.Results.loadGeometry);
    else
      [ entries, structured_entries ] = single_GEO_INP_reader(filename, entries, structured_entries, 'loadGeometry', p.Results.loadGeometry);
    end
    
  end
  
end
