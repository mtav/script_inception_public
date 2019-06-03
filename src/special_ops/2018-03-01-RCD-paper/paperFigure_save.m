for idx = 1:length(fig)
  figure(fig{idx});
  outfile = sprintf('fig%02d', idx);
  saveas_fig_and_png(figure(fig{idx}), fullfile('fixedFigures', outfile));
  % saveas_fig_and_png_tight(figure(fig{idx}), fullfile('fixedFigures', outfile));
  disp(outfile);
end
