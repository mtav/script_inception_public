%This example shows how to create two x axes with different scales (units)
%This technique can be adapted to create two y axes
clear all;
close all;
%x values in radians
x = [0:0.1:6.3];
%y values values
y=sin(x);
%x values in degrees
x2=rad2deg(x);
%means each new graph destroys the previous(overlay mode off)
hold off;
plot(x, y);
xlabel('bottom');
%attach the current axes (gca) to handle "axes1"
axes1=gca;
%ensure x axis at bottom
%see "get(axes1)" for additional properties
%see "set(axes1)" for properties which can be altered
set(axes1, 'XAxisLocation',  'bottom');
%overlay mode on 
hold on;
%add additional axes
axes;
plot(x2, y);
xlabel('top');
axes2=gca;
%ensure x axis at top
set(axes2, 'XAxisLocation',  'top' );
%make different intervals
set(axes2, 'XTick', [x2(1):75:x2(length(x2))] );
%overlay off
hold off;
