function plotxxy()
  close all;

  x1 = 1:10;
  x2 = 1./x1;
  y = x1.^2;

  figure;

  hl1 = line(x1, y, 'Color', 'k');

  ax(1) = gca;

  %set(ax(1),'Position',[0.12 0.12 0.75 0.70])
  set(ax(1),'XColor','k','YColor','k');

  ax(2) = axes('Position',get(ax(1),'Position'),...
     'XAxisLocation','top',...
     'YAxisLocation','right',...
     'Color','none',...
     'XColor','b','YColor','k','HitTest','off');

  set(ax,'box','off');

  hl2 = line(x2,y,'Color','b','Parent',ax(2));

  %label the two x-axes
  set(get(ax(1),'xlabel'),'string','x1')
  set(get(ax(2),'xlabel'),'string','x2')
  set(get(ax(1),'ylabel'),'string','y')

  set(ax(1),'XLim',[min(x1) max(x1)]);
  set(ax(2),'XLim',[min(x2) max(x2)]);

  set(ax(2),'XDir','reverse');

  xlimits = get(ax(1),'XLim');
  ylimits = get(ax(1),'YLim');

  set(ax(2),'XLim', sort(1./xlimits));
  set(ax(2),'YLim', ylimits);
  
  pan_handle = pan(gcf);

  %set(pan_handle,'ActionPreCallback',@myprecallback);
  set(pan_handle,'ActionPostCallback',{@mypostcallback,ax});
end

%function myprecallback(obj,evd)
  %%disp('A pan is about to occur.');
%end

function mypostcallback(obj,evd, ax)
  %newLim = get(evd.Axes,'XLim');
  %msgbox(sprintf('The new X-Limits are [%.2f %.2f].',newLim));

  xlimits = get(ax(1),'XLim');
  ylimits = get(ax(1),'YLim');

  set(ax(2),'XLim', sort(1./xlimits));
  set(ax(2),'YLim', ylimits);
end
