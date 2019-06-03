function [y, y_label] = mpb_yfunc_default(data, pos, data_info)
  y_label = 'a/\lambda';
  
  if ~exist('pos', 'var'); pos=[]; end;
  
  if isempty(pos)
    y = data(:, 6:end);
  else
    y = pos;
  end
end
