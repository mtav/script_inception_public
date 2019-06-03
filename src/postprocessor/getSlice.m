function [x_data, y_data, x_label, y_label, used_fixed_coord_value] = getSlice(prnfile, column_str, fixed_coord_str, fixed_coord_value)
  % function [x_data, y_data, x_label, y_label, used_fixed_coord_value] = getSlice(prnfile, column_str, fixed_coord_str, fixed_coord_value)
  % cf getSliceTest for a usage example.

  % create parser
  p = inputParser;
  p = inputParserWrapper(p, 'addRequired', 'prnfile', @(x) ischar(x) && exist(x,'file'));
  p = inputParserWrapper(p, 'addRequired', 'column_str', @ischar);
  p = inputParserWrapper(p, 'addRequired', 'fixed_coord_str', @ischar);
  p = inputParserWrapper(p, 'addRequired', 'fixed_coord_value', @isnumeric);

  % parse arguments
  p = inputParserWrapper(p, 'parse', prnfile, column_str, fixed_coord_str, fixed_coord_value);

  % default return values
  x_data = [];
  y_data = [];
  x_label = '';
  y_label = '';
  used_fixed_coord_value = 0;
  
  % load file and validate column strings
  [ header, data, u1, u2 ] = readPrnFile(p.Results.prnfile);
  column_str = validatestring(p.Results.column_str, header);
  fixed_coord_str = validatestring(p.Results.fixed_coord_str, header);

  % get and validate column indices
  column_idx = find(strcmp(header, column_str));
  if isempty(column_idx)
    disp([column_str, ' not found. Valid values are:']);
    for i = 1:length(header)
      disp(header{i});
    end
    return;
  end
  if column_idx - 2 < 1
    error('Invalid column. The 2 first columns cannot be chosen.')
  end

  fixed_coord_idx = find(strcmp(header, fixed_coord_str));
  if isempty(fixed_coord_idx)
    disp([fixed_coord_str, ' not found. Valid values are:']);
    for i = 1:length(header)
      disp(header{i});
    end
    return;
  end

  % get return values
  if fixed_coord_idx == 1
    [central_fixed_idx, used_fixed_coord_value, central_fixed_abs_err] = closestInd(u1, p.Results.fixed_coord_value);
    x_data = u2;
    y_data = data( :, central_fixed_idx, column_idx-2 );
    x_label = char(header(2));
    y_label = char(header(column_idx));
  else if fixed_coord_idx == 2
    [central_fixed_idx, used_fixed_coord_value, central_fixed_abs_err] = closestInd(u2, p.Results.fixed_coord_value);
    x_data = u1;
    y_data = data( central_fixed_idx, :, column_idx-2 );
    x_label = char(header(1));
    y_label = char(header(column_idx));
  else
    error(['invalid value for fixed_coord_idx: ', num2str(fixed_coord_idx)]);
  end
  
  x_data = x_data(:);
  y_data = y_data(:);

end
