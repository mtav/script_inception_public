%https://stackoverflow.com/questions/12072412/setting-transparancy-of-surface-plot-on-octave
close all;

p = peaks(40);
f1 = figure(10);clf
s1 = surface(p)
view(3)
xlabel('x');ylabel('y');
hold on;plot3([0 40],[40 0],[-10 10],'k')
set(s1,'edgecolor','none')
set(s1,'facealpha',0.2)
