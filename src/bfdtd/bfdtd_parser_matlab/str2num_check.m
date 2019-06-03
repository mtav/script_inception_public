function [x, status] = str2num_check(s)
  [x, status] = str2num(s);
  if ~status
    error('Failed to convert %s to a number.', s);
  end
end
