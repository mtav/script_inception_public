%%%%%
% visualization functions
function [fig, a1, a2, a3] = plotMesh(fig, a1, a2, a3, mymesh, xmin, xmax, spacing_left, spacing_max, spacing_right, ratio_used, ratio_max)
  
  if isfigure(fig)
    fig = figure(fig);
  else
    fig = figure();
  end

  thickness = diff(mymesh);
  [ratio, ratio2] = getThicknessRatios(mymesh);
  
  spacing_left_fake = spacing_left;
  spacing_right_fake = spacing_right;
  if spacing_max <= spacing_left
    spacing_left_fake = thickness(1);
  end
  if spacing_max <= spacing_right
    spacing_right_fake = thickness(end);
  end
  extended_ratio = [ thickness(1)/spacing_left_fake, ratio, spacing_right_fake/thickness(end)];
  extended_ratio2 = [ getRatio(spacing_left_fake, thickness(1)), ratio2, getRatio(thickness(end), spacing_right_fake)];

  if isaxes(a1)
    a1 = axes(a1); hold on;
  else
    a1 = subplot(1,3,1); hold on;
  end
  stairs(mymesh, [thickness, thickness(end)], 'bo-');
  axis_xmin = min(mymesh)-1;
  axis_xmax = max(mymesh)+1;
  axis_ymin = min([thickness, spacing_left, spacing_right, spacing_max])-1;
  axis_ymax = max([thickness, spacing_left, spacing_right, spacing_max])+1;
  axis([axis_xmin, axis_xmax, axis_ymin, axis_ymax]);
  xlabel('position');
  ylabel('thickness');
  vline(xmin,'r--','xmin',90);
  vline(xmax,'r--','xmax',90);
  vline(mymesh(1),'r--','x_{start}',90);
  vline(mymesh(end),'r--','x_{end}',90);
  hline(spacing_max,'r--','\delta_{max}');
  hline(spacing_left,'r--','\delta_{left}');
  hline(spacing_right,'r--','\delta_{right}');

  % plot a line showing the maximum ratio
  x = linspace(mymesh(1), mymesh(end), 100);
  plot(x, spacing_left+((ratio_max-1)/ratio_max)*x,'g--');

  % plot a line showing the used ratio
  x = linspace(mymesh(1), mymesh(end), 100);
  plot(x, spacing_left+((ratio_used-1)/ratio_used)*x,'b--');

  axis('auto'); % well, that's easier... (but does not do the +/-1)

  if isaxes(a2)
    a2 = axes(a2); hold on;
  else
    a2 = subplot(1,3,2); hold on;
  end
  plot(mymesh, extended_ratio, 'bo-');
  axis_ymin = min([ratio, ratio_max, 1/ratio_max, extended_ratio])-1;
  axis_ymax = max([ratio, ratio_max, 1/ratio_max, extended_ratio])+1;
  axis([axis_xmin, axis_xmax, axis_ymin, axis_ymax]);
  xlabel('position');
  ylabel('ratio t2/t1');
  vline(xmin,'r--','xmin',90);
  vline(xmax,'r--','xmax',90);
  vline(mymesh(1),'r--','x_{start}',90);
  vline(mymesh(end),'r--','x_{end}',90);
  hline(ratio_max, 'r--', '\alpha_{max}');
  hline(1/ratio_max, 'r--', '1/\alpha_{max}');

  axis('auto'); % well, that's easier... (but does not do the +/-1)

  if isaxes(a3)
    a3 = axes(a3); hold on;
  else
    a3 = subplot(1,3,3); hold on;
  end
  plot(mymesh, extended_ratio2, 'bo-');
  axis_ymin = min([ratio2, ratio_max, 1, extended_ratio2])-1;
  axis_ymax = max([ratio2, ratio_max, 1, extended_ratio2])+1;
  axis([axis_xmin, axis_xmax, axis_ymin, axis_ymax]);
  xlabel('position');
  ylabel('ratio max(t2,t1)/min(t2,t1)');
  vline(xmin,'r--','xmin',90);
  vline(xmax,'r--','xmax',90);
  vline(mymesh(1),'r--','x_{start}',90);
  vline(mymesh(end),'r--','x_{end}',90);
  hline(ratio_max, 'r--', '\alpha_{max}');
  hline(1, 'r--', '1');

  axis('auto'); % well, that's easier... (but does not do the +/-1 (or take into account min/max lines))

end
