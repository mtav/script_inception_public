function [x, z, x_label, z_label] = mpb_xzfunc_default(data, pos, data_info)
  x_label = 'direction';
  z_label = '';
  
  if ~exist('pos', 'var'); pos=[]; end;
  
  if isempty(pos)
    x = data(:, 1);
  else
    x = pos;
  end
  z = zeros(size(x));
end
