function [delimiter, line_1, line_2, N_1, N_2] = GuessCsvDelimiter(filename, varargin)
  % TODO: test on arbitrary number of lines?

  % create parser
  p = inputParser();
  p = inputParserWrapper(p, 'addRequired', 'filename', @ischar);
  p = inputParserWrapper(p, 'parse', filename, varargin{:});

  % read first two lines
  [fid, message] = fopen(p.Results.filename, 'r');
  if fid == -1
    error(message);
  end
  line_1 = fgets(fid);
  line_2 = fgets(fid);
  fclose(fid);

  delimiter_list = {',', ';', '\t', ' '};

  % return empty delimiter by default
  delimiter = '';
  Nmax = 0;
  
  for i = 1:length(delimiter_list)
    N_1(i) = length(strfind(line_1, delimiter_list{i}));
    N_2(i) = length(strfind(line_2, delimiter_list{i}));
    if N_1(i) == N_2(i) && N_1(i) > Nmax
      Nmax = N_1(i);
      delimiter = delimiter_list{i};
    end
  end

end
