function [header_bands, data_bands, header_defects, data_defects] = plotStuff(cavity_index)
  bandfile = sprintf('DBR_defect_ncav_%.2f_bands.out.dat', cavity_index)
  modefile= sprintf('DBR_defect_ncav_%.2f_defect_mode.out.dat', cavity_index)
  [header_bands, data_bands] = plot_MPB(bandfile);
  hold on;
  [header_defects, data_defects]=readPrnFile(modefile);
  for idx = 6:size(data_defects, 2)
    mode_number = idx-5;
    y = data_defects(1, idx);
    hline(y);
    text(25+mode_number*0.5, y, num2str(mode_number));
  end
  saveas(gcf, sprintf('DBR_defect_ncav_%.2f.png', cavity_index));
end
