close all;
clear all;

x = linspace(-15,15);
y = linspace(-10,0);
z = linspace(0,5);
[X1,Y1] = meshgrid(x,y);
[X2,Y2] = meshgrid(y,z);
[X3,Y3] = meshgrid(x,z);

Z1 = peaks(X1,Y1);
Z2 = peaks(X2,Y2);
Z3 = peaks(X3,Y3);

%A5	148 x 210 mm
w_fig_cm = 21.0;
h_fig_cm = 14.8;
fig = figure('Units', 'centimeters', 'position', [0, 0, w_fig_cm, h_fig_cm]);
%set(params.figure_handle, 'Units', 'centimeters', 'position', [0, 0, w_fig_cm, h_fig_cm]);
%drawnow();

%subplot('Position', positionVector1);
subplot(1,3,1);
surf(X1,Y1,Z1);
handle1 = gca();
xlabel('x'); ylabel('y');
view(2); shading flat;

subplot(1,3,2);
%subplot('Position', positionVector2);
surf(X2,Y2,Z2);
handle2 = gca();
xlabel('y'); ylabel('z');
view(2); shading flat;

subplot(1,3,3);
%subplot('Position', positionVector3);
surf(X3,Y3,Z3);
handle3 = gca();
xlabel('x'); ylabel('z');
view(2); shading flat;

handle_colorbar = colorbar('southoutside');
xlabel(handle_colorbar, 'value');
Zall = [Z1(:);Z2(:);Z3(:)];
caxis(handle1, getRange(Zall));
caxis(handle2, getRange(Zall));
caxis(handle3, getRange(Zall));

params = struct();

params.figure_handle = fig;
params.w_fig_cm = w_fig_cm;
params.h_fig_cm = h_fig_cm;

params.handle_colorbar = handle_colorbar;

params.plot_1.handle = handle1;
params.plot_1.X = [-5,5];
params.plot_1.Y = [-5,0];
params.plot_1.anchor_data = [0, 0]; %[mean(getRange(X1)), mean(getRange(Y1))];
params.plot_1.anchor_window = [0, 0.5];
params.plot_1.relative_data_coordinates = false;
params.plot_1.forced_limit = 'auto';

params.plot_2.handle = handle2;
params.plot_2.X = X2;
params.plot_2.Y = Y2;
params.plot_2.anchor_data = [0, 0];
params.plot_2.anchor_window = [0, 0];
params.plot_2.relative_data_coordinates = false;
params.plot_2.forced_limit = 'x';

params.plot_3.handle = handle3;
params.plot_3.X = X3;
params.plot_3.Y = Y3;
params.plot_3.anchor_data = [0, 0];
params.plot_3.anchor_window = [0, 0];
params.plot_3.relative_data_coordinates = false;
params.plot_3.forced_limit = 'x';

surf_triplet(params);
