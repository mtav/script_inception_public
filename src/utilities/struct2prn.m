function [header, data] = struct2prn(max_info, prefix)
  % Converts a structure into a {header, data} pair suitable for .prn/.csv file writing, i.e.:
  %   header = {'field1', 'field2', ...}
  %   data = [value1, value2, ...]
  %
  % note: only structures and scalar numeric/logical fields are considered
  
  if ~exist('prefix', 'var')
    prefix = '';
  end
  
  header = {};
  data = [];
  F = fieldnames(max_info);
  for idx = 1:numel(F)
    VAL = getfield (max_info, F{idx});
    
    if isstruct(VAL)
      [h, d] = struct2prn(VAL, sprintf('%s%s.', prefix, F{idx}));
      header = [header, h];
      data = [data, d];
    elseif ( isnumeric(VAL) || islogical(VAL) ) && isscalar(VAL)
      header{end+1} = sprintf('%s%s', prefix, F{idx});
      data(end+1) = VAL;
    else
      warning('Skipping %s of class %s.', sprintf('%s%s', prefix, F{idx}), class(VAL));
    end
  end
  
end
