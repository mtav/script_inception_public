function [y, y_label] = mpb_yfunc_custom(data, pos, data_info, omega_bragg_normalized)

  y_label = 'a/\lambda';
  
  if ~exist('pos', 'var'); pos=[]; end;
  
  if isempty(pos)
    y = data(:, 6:end);
  else
    y = pos;
  end
  
  y = y ./ omega_bragg_normalized;
end
