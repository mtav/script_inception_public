function [header, delimiter] = readHeader(filename, varargin)

  % create parser
  p = inputParser();
  p = inputParserWrapper(p, 'addRequired', 'filename', @ischar);
  p = inputParserWrapper(p, 'addOptional', 'delimiter', '', @ischar);
  p = inputParserWrapper(p, 'addOptional', 'GuessCsvDelimiter', true, @islogical);
  p = inputParserWrapper(p, 'addParamValue', 'stripHeader', true, @islogical);
  p = inputParserWrapper(p, 'parse', filename, varargin{:});

  % guess delimiter if not specified
  delimiter = p.Results.delimiter;
  if length(delimiter) == 0 && p.Results.GuessCsvDelimiter
    [delimiter, first_line] = GuessCsvDelimiter(p.Results.filename);
  else
    % read first line. This is actually extremely fast, even for large files. :)
    [fid, message] = fopen(p.Results.filename, 'r');
    if fid == -1
      error(message);
    end
    first_line = fgets(fid);
    fclose(fid);
  end

  
  % the simple variant from postprocessor/PP_functions/PP_load_data.m. TODO: Why not use it?
  % columns = strread(handles.header,'%s');

  % split into words separated by space characters
  % \s: Any white-space character; equivalent to [ \f\n\r\t\v]
  % \S: Any non-whitespace character; equivalent to [^ \f\n\r\t\v]
  % words = regexp(first_line,'\s*(?<word>\S+)\s*','tokens');

  % Because strsplit is not as smart as dlmwrite, does not work the same way.
  if length(delimiter) == 0
    words = strsplit_custom(strtrim(first_line));
  else
    words = strsplit_custom(strtrim(first_line), delimiter);
  end

  for m = 1:length(words)
    S = char(words{m});
    if p.Results.stripHeader
      if strcmp(S(1), '#')
        S = S(2:end);
      end
    end
    header{m} = strtrim(S);
  end

end
