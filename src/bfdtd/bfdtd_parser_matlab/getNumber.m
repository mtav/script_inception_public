function ret = getNumber(data, idx, default_value)
  if length(data) >= idx
    ret = str2num_check(data{idx});
  else
    if ~exist('default_value', 'var')
      error('getNumber: data{%d} not available and no default value specified.', idx);
    end
    ret = default_value;
  end
end
