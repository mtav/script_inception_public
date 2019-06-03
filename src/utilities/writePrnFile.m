function writePrnFile(filename, header_arg, data, varargin)
  % Usage:
  %  writePrnFile(filename, header, data) % probe-style save
  %  writePrnFile(filename, header, data, ux, uy) % snapshot-style save
  %
  % TODO: separate data<->data_reshaped conversion functions? (for use in console/scripts)
  % TODO: finish createEnergySnapshot tests to validate new writePrn() function
  % TODO: change defaults to auto-precision and semicolon, i.e. sane .csv format? or create writeCSVwrapper? -> because we can always read BFDTD output, but also saner .csv formats, so no need to write out shitty BFDTD formats from Matlab/Octave, except maybe for BFDTD input template generation...
  %
  % Note on naming conventions (cf https://en.wikipedia.org/wiki/Delimiter-separated_values):
  %   CSV: Comma Separated Values
  %   DSV: Delimiter Separated Values
  %   SCSV: Semi-colon Separated Values ?
  %   SPSV: Space Separated Values ?
  %   TSV: Tab Separated Values
  %
  % Note: In Matlab, one could also simply use readtable/writetable/table? (but not in Octave yet)
  
  % create parser
  p = inputParser();
  p = inputParserWrapper(p, 'addRequired', 'filename', @ischar);
  p = inputParserWrapper(p, 'addRequired', 'header_arg', @(x) ischar(x) || iscellstr(x));
  p = inputParserWrapper(p, 'addRequired', 'data', @isnumeric);
  p = inputParserWrapper(p, 'addOptional', 'ux', [], @isnumeric);
  p = inputParserWrapper(p, 'addOptional', 'uy', [], @isnumeric);
  
  p = inputParserWrapper(p, 'addParamValue', 'delimiter', '\t', @ischar);
  p = inputParserWrapper(p, 'addParamValue', 'newline', 'pc', @(x) any(validatestring(x, {'pc','unix'})));
  
  % to get exactly the same results as when using save(), use '%.16e'
  % to get BFDTD-like output, use '%.8E'
  p = inputParserWrapper(p, 'addParamValue', 'precision', '%.16e');
  
  p = inputParserWrapper(p, 'addParamValue', 'interactive', false, @islogical);
  
  p = inputParserWrapper(p, 'parse', filename, header_arg, data, varargin{:});
  
  % Transform the header into a string if necessary.
  if iscellstr(p.Results.header_arg)
    % TODO: 2017-02-28: strjoin only exists in Matlab >= 2013 + use sprintf for tab delimiter in old code, cf hack on Xu PC -> create strjoin wrapper with version check
    % TODO: 2017-02-28: Note: Matlab doc recommends using "join". -> not yet available in Octave (and in statistics package for some reason).
    header_str = strjoin(p.Results.header_arg, p.Results.delimiter);
    %header_str = '';
    %for i = 1:length(p.Results.header_arg)
      %header_str = [header_str, p.Results.header_arg{i}];
      %if i < length(p.Results.header_arg)
        %header_str = [header_str, p.Results.delimiter];
      %end
    %end
  else
    header_str = p.Results.header_arg;
  end

  % Reshape the data if necessary.
  if ~isempty(p.Results.ux) && ~isempty(p.Results.uy)
    % snapshot-style save
    NX = size(data, 2);
    NY = size(data, 1);
    Ncols = size(data, 3);
    data_reshaped = zeros(NX*NY, Ncols+2);

    Xcol = kron(p.Results.ux(:), ones(NY, 1));
    Ycol = repmat(p.Results.uy(:), NX, 1);
    data_reshaped(:, 1) = Xcol;
    data_reshaped(:, 2) = Ycol;
    for col = 1:Ncols
      data_reshaped(:, col+2) = reshape(data(:,:,col),[],1);
    end
    data = data_reshaped;
  else
    % probe-style save
    if length(size(data)) ~= 2
      error('Invalid data size for a probe-style save');
    end
  end

  choice = 'Yes';
  if p.Results.interactive && exist(filename, 'file')
    choice = questdlg([filename, ' already exists. Overwrite?'], 'Overwrite existing file?', 'Yes', 'No', 'No');
  end

  if strcmp(choice, 'Yes')
  
    %%% Write the header to file.
    file = fopen(filename,'w');
    if strcmp(p.Results.newline, 'pc')
      newline = '\r\n';
    else
      newline = '\n';
    end
    fprintf(file, ['%s', newline], header_str);
    fclose(file);

    %%% Finally write the data to file.
    
    % using save (Note: Only saves real part of numbers, while dlmwrite actually saves complex number with real+imaginary parts)
    %save([filename, '.save'], 'data', '-ascii', '-double', '-tabs', '-append');
    
    % using dlmwrite
    if isempty(p.Results.precision)
      dlmwrite(filename, data, '-append', 'newline', p.Results.newline, 'delimiter', p.Results.delimiter);
    else
      dlmwrite(filename, data, '-append', 'newline', p.Results.newline, 'delimiter', p.Results.delimiter, 'precision', p.Results.precision);
    end
  end

end
