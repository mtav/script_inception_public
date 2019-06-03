close all;
clear all;

x = linspace(-2*pi,2*pi,500);

f1 = figure;
y1 = sin(x);
hCurve1 = plot(x,y1,'r');
xlabel('x'); ylabel('sin(x)');
xlim([0,2*pi]);
ylim([0,1]);

f2 = figure;
y2 = cos(x);
hCurve2 = plot(x,y2,'r');
xlabel('x'); ylabel('cos(x)');
xlim([-2*pi,0]);
ylim([-1,0]);

combineFigures({f1, f2}, 2, 2);

return

figure;
hSub1 = subplot(2,1,1);
hSub2 = subplot(2,1,2);

%copyobj(hCurve1,hSub1);
%copyobj(hCurve2,hSub2);

hFigIAxes1 = findobj('Parent',f1,'Type','axes');
hFigIAxes2 = findobj('Parent',f2,'Type','axes');

if ~isempty(hFigIAxes1)
  hAxes = hFigIAxes1(1);  % assume just the one axes
  copyobj(get(hAxes,'Children'),hSub1);
end

if ~isempty(hFigIAxes2)
  hAxes = hFigIAxes2(1);  % assume just the one axes
  copyobj(get(hAxes,'Children'),hSub2);
end
