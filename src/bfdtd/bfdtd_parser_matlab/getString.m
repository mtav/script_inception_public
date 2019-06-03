function ret = getString(data, idx, default_value)
  if length(data) >= idx
    str_val = strtrim(char(data{idx}));
    ret = str_val(str_val ~= '"');
  else
    ret = default_value;
  end
end
