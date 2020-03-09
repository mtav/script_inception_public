function [x, z, x_label, z_label] = mpb_xzfunc_custom(data, pos, data_info, s)

  x_label = 'direction';
  z_label = '';
  
  if ~exist('pos', 'var'); pos=[]; end;
  
  if isempty(pos)
    x = data(:, 2);
  else
    x = pos;
  end
  
  x = s*x;
  z = zeros(size(x));
end
