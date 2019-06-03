function surf_triplet(params)
  % nicely arrange three surface plots, with common colorbar

  % changing figure size after creation and then changing axes does not work properly :(
  %A5	148 x 210 mm
  %w_fig_cm = 21.0;
  %h_fig_cm = 14.8;
  %fig = figure('Units', 'centimeters', 'position', [0, 0, w_fig_cm, h_fig_cm]);
  %set(params.figure_handle, 'Units', 'centimeters', 'position', [0, 0, w_fig_cm, h_fig_cm]);
  %drawnow();

  TYPE=1;

  w_fig_cm = params.w_fig_cm;
  h_fig_cm = params.h_fig_cm;

  if TYPE==0
    bx = 1/w_fig_cm;
    by = 1/h_fig_cm;

    x_colorbar = bx;
    y_colorbar = by;
    h_colorbar = by;
    w_colorbar = 1 - 2*bx;

    x_surf_canvas = bx;
    y_surf_canvas = 2*by + h_colorbar;
    w_surf_canvas = 1 - 2*bx;
    h_surf_canvas = 1 - 3*by - h_colorbar;

    w1 = (1/3)*(w_surf_canvas - bx);
    w2 = (w_surf_canvas - bx) - w1;
    w3 = w2;

    h1 = (w1*w_fig_cm)/h_fig_cm;
    h2 = 0.5*(h_surf_canvas - by);
    h3 = h_surf_canvas - by - h2;

    x1 = x_surf_canvas;
    y1 = y_surf_canvas + 0.5*h_surf_canvas - 0.5*h1;

    x2 = x_surf_canvas + w1 + bx;
    y2 = y_surf_canvas + h3 + by;

    x3 = x2;
    y3 = y_surf_canvas;
  else
    bx = 1.5/w_fig_cm;
    by = 1.5/h_fig_cm;
    
    bx_left = bx;
    bx_right = 0.5/w_fig_cm;
    
    by_bottom = by;
    by_top = 0.5/h_fig_cm;

    x_colorbar = bx;
    y_colorbar = by;
    h_colorbar = 0.5/h_fig_cm;
    w_colorbar = 1 - bx_left - bx_right;

    x_surf_canvas = bx_left;
    y_surf_canvas = by_bottom + h_colorbar + by;
    w_surf_canvas = w_colorbar;
    h_surf_canvas = 1 - by_top - by_bottom - by - h_colorbar;

    h2 = (h_surf_canvas - by)*2/3;
    h1 = h2;
    h3 = (h_surf_canvas - by) - h2;

    w1 = 0.5*(h1*h_fig_cm)/w_fig_cm;
    w2 = (w_surf_canvas - bx) - w1;
    w3 = w2;

    x1 = x_surf_canvas;
    y1 = y_surf_canvas + h3 + by;

    x2 = x_surf_canvas + w1 + bx;
    y2 = y1;

    x3 = x2;
    y3 = y_surf_canvas;
  end
  
  positionVector_colorbar = [x_colorbar, y_colorbar, w_colorbar, h_colorbar];
  positionVector1 = [x1,y1,w1,h1];
  positionVector2 = [x2,y2,w2,h2];
  positionVector3 = [x3,y3,w3,h3];
  
  set(params.plot_1.handle, 'Position', positionVector1);
  set(params.plot_2.handle, 'Position', positionVector2);
  set(params.plot_3.handle, 'Position', positionVector3);
  set(params.handle_colorbar, 'Position', positionVector_colorbar);

  [xmin, xmax, ymin, ymax] = axis_equal_advanced(params.plot_1.handle, params.plot_1.X, params.plot_1.Y, params.plot_1.anchor_data, params.plot_1.anchor_window, 'relative_data_coordinates', params.plot_1.relative_data_coordinates, 'forced_limit', params.plot_1.forced_limit);
  [xmin, xmax, ymin, ymax] = axis_equal_advanced(params.plot_2.handle, params.plot_2.X, params.plot_2.Y, params.plot_2.anchor_data, params.plot_2.anchor_window, 'relative_data_coordinates', params.plot_2.relative_data_coordinates, 'forced_limit', params.plot_2.forced_limit);
  
  % hack for third plot:
  params.plot_3.X = [xmin, xmax];
  params.plot_3.forced_limit = 'x';
  [xmin, xmax, ymin, ymax] = axis_equal_advanced(params.plot_3.handle, params.plot_3.X, params.plot_3.Y, params.plot_3.anchor_data, params.plot_3.anchor_window, 'relative_data_coordinates', params.plot_3.relative_data_coordinates, 'forced_limit', params.plot_3.forced_limit);
end
