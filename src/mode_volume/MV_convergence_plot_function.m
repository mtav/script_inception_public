function figure_handle = MV_convergence_plot_function(header, data, x_column_name)

  x_column_idx = find(strcmpi(x_column_name, header));
  
  if isempty(x_column_idx)
    error('x_column_name = %s not found in header.', x_column_name);
  end

  figure_handle = figure();
  
  for i=1:10
    if i*i >= numel(header)
      break;
    end
  end
  
  rows=i;
  cols=i;
  
  for y_column_idx = 1:numel(header)
    subplot(rows, cols, y_column_idx);
    plot(data(:, x_column_idx), data(:, y_column_idx), 'ro');
    xlabel(header{x_column_idx}, 'interpreter', 'none');
    ylabel(header{y_column_idx}, 'interpreter', 'none');
  end
  
end
