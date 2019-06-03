function column_data = prnGetColumnByName(header, data, column_name)
  column_idx = find(strcmpi(column_name, header));
  if isempty(column_idx)
    error('column_name = %s not found in header.', column_name);
  end
  
  column_data = data(:, column_idx);
end
