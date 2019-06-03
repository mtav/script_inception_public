figure_list = dir('*.fig')
for idx = 1:length(figure_list)
  filename = figure_list(idx).name;
  disp(filename);
  MatlabFigure_to_OctavePlot(filename);
end
