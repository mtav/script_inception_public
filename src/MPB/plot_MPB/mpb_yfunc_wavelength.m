function [y, y_label] = mpb_yfunc_wavelength(data, pos, data_info)
  y_label = '\lambda';
  
  if ~exist('pos', 'var'); pos=[]; end;
  
  if isempty(pos)
    y = data_info.unit_cell_size * 1./data(:, 6:end);
  else
    y = data_info.unit_cell_size * 1./pos;
  end
end
