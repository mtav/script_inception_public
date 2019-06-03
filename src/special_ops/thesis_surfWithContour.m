function thesis_surfWithContour(struct_surf, struct_contour, column_to_plot, colorbar_label)
  hold all;
  surf(struct_surf.data(:,:,1), struct_surf.data(:,:,2), struct_surf.data(:,:,column_to_plot));
  xlabel(struct_surf.header{1});
  ylabel(struct_surf.header{2});
  view(2);
  shading flat;
  Rx = getRange(struct_surf.data(:,:,1));
  Ry = getRange(struct_surf.data(:,:,2));
  xlim(Rx);
  ylim(Ry);
  %axis equal;
  AspectRatio = get(gca,'DataAspectRatio');
  AspectRatio(1) = AspectRatio(2);
  set(gca,'DataAspectRatio',AspectRatio);
  Rdata = getRange(struct_surf.data(:,:,column_to_plot));
  Zc0 = 1.1*Rdata(2);
  [contour_ContourMatrix , contour_handle] = contourAtZ(Zc0, struct_contour.data(:,:,1), struct_contour.data(:,:,2), struct_contour.data(:,:,3), 'colormap', [0,0,0], 'contourValues', NaN, 'LineWidth', 1);
  handle_colorbar = colorbar('Location', 'SouthOutside');
  xlabel(handle_colorbar, colorbar_label);

end
