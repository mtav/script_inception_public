function [y, y_label] = mpb_yfunc_k_index(data, pos, data_info)
  y_label = 'k index';
  
  if ~exist('pos', 'var'); pos=[]; end;
  
  if isempty(pos)
    y = data(:, 1);
  else
    y = pos;
  end
  
end
