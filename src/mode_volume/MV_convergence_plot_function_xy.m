function [x_data, y_data] = MV_convergence_plot_function_xy(header, data, x_column_name, y_column_name, varargin)
  
  x_column_idx = find(strcmpi(x_column_name, header));
  if isempty(x_column_idx)
    error('x_column_name = %s not found in header.', x_column_name);
  end
  
  y_column_idx = find(strcmpi(y_column_name, header));
  if isempty(y_column_idx)
    error('y_column_name = %s not found in header.', y_column_name);
  end
  
  x_data = data(:, x_column_idx);
  y_data = data(:, y_column_idx);
  
  plot(x_data, y_data, varargin{:});
  
  xlabel(header{x_column_idx}, 'interpreter', 'none');
  ylabel(header{y_column_idx}, 'interpreter', 'none');
  
end
