function [ structured_entries, entries ] = readFileList(infile, structured_entries, entries, varargin);
  
  %%%%%%%%%%%%%
  % parse args
  p = inputParser();
  p = inputParserWrapper(p, 'addRequired', 'infile', @ischar);
  p = inputParserWrapper(p, 'addRequired', 'structured_entries', @isstruct);
  p = inputParserWrapper(p, 'addRequired', 'entries', @iscell);
  p = inputParserWrapper(p, 'addParamValue', 'loadGeometry', true, @islogical);
  p = inputParserWrapper(p, 'parse', infile, structured_entries, entries, varargin{:});
  %%%%%%%%%%%%%
  
  ORIGDIR = pwd();
  %fprintf('%s: pwd  = %s\n', basename(mfilename('fullpath')), pwd());
  
  [fileID, errmsg] = fopen(infile);
  if fileID < 0
    pwd
    error('%s : %s', errmsg, infile);
  end
  file_list = textscan(fileID, '%s', 'Delimiter', '\n');
  file_list = file_list{:};
  fclose(fileID);
  
  % TODO: get rid of cd() calls...
  % Note: cd() should be avoided in code, but Matlab's fullfile is not smart enough to handle absolute paths like python's os.path.join()
  cd(dirname(infile));
  %fprintf('%s: pwd  = %s\n', basename(mfilename('fullpath')), pwd());
  
  for file_list_idx = 1:numel(file_list)
    input_file = file_list{file_list_idx};
    % fprintf('  readFileList: processing: %s\n', input_file);
    [ entries, structured_entries ] = single_GEO_INP_reader(input_file, entries, structured_entries, 'loadGeometry', p.Results.loadGeometry);
  end
  
  cd(ORIGDIR);
  
end
