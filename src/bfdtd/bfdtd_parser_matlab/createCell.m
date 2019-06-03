function C = createCell(cell_array_size, fill_value)
  C = cell(cell_array_size);
  C(:) = {fill_value};
end
