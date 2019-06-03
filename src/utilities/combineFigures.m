function fig_main = combineFigures(figure_cell_array, Nrows, Ncols)
  % TODO: copy view/camroll orientation, xyz labels, xyz limits, etc
  if length(figure_cell_array) > Nrows*Ncols
    error('Grid too small for number of figures');
  end
  fig_main = figure();
  for idx = 1:length(figure_cell_array)
    h = subplot(Nrows, Ncols, idx);
    source_axes_list = findobj('Parent', figure_cell_array{idx}, 'Type', 'axes');
    if ~isempty(source_axes_list)
      source_axes = source_axes_list(1);  % assume just the one axes
      copyobj(get(source_axes, 'Children'), h);
      % copyaxes(get(source_axes, 'Children'), h);
    end
  end
end
