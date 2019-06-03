% getSlice() test

prnfile = 'cross-section.prn';

% prepare a .prn file
[X, Y] = meshgrid(-8:0.1:8, -8:0.2:8);
Z1 = X .* exp(-X.^2 - Y.^2);
Z2 = sin (sqrt (X.^2 + Y.^2)) ./ (sqrt (X.^2 + Y.^2));
Z3 = 3*(1-X).^2 .* exp(-X.^2 - (Y+1).^2) - 10*(X/5 - X.^3 - Y.^5).*exp(-X.^2-Y.^2) - 1/3*exp(-(X+1).^2 - Y.^2);
writePrnFile(prnfile, {'x', 'y', 'Z1', 'Z2', 'Z3'}, cat(3,Z1,Z2,Z3), X(1,:), Y(:,1));

% plot each one as a surface plot
close all;

figure(1);
surf(X,Y,Z1); xlabel('x'); ylabel('y'); zlabel('z');

figure(2);
surf(X,Y,Z2); xlabel('x'); ylabel('y'); zlabel('z');

figure(3);
surf(X,Y,Z3); xlabel('x'); ylabel('y'); zlabel('z');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% add slices using plot3 lines
figure(1);
hold on;
column_str = 'Z1';

fixed_coord_str = 'x';
fixed_coord_value = 1;
[x_data, y_data, x_label, y_label, central_fixed_value] = getSlice(prnfile, column_str, fixed_coord_str, fixed_coord_value);
plot3(fixed_coord_value*ones(size(x_data)), x_data, y_data, 'color', 'red', 'marker', 'o');

fixed_coord_str = 'y';
fixed_coord_value = 9; %0.2;
[x_data, y_data, x_label, y_label, central_fixed_value] = getSlice(prnfile, column_str, fixed_coord_str, fixed_coord_value);
plot3(x_data, fixed_coord_value*ones(size(x_data)), y_data, 'color', 'blue', 'marker', 's');

% add slices using plot3 lines
figure(2);
hold on;
column_str = 'Z2';

fixed_coord_str = 'x';
fixed_coord_value = 2;
[x_data, y_data, x_label, y_label, central_fixed_value] = getSlice(prnfile, column_str, fixed_coord_str, fixed_coord_value);
plot3(fixed_coord_value*ones(size(x_data)), x_data, y_data, 'color', 'red', 'marker', 'o');

fixed_coord_str = 'y';
fixed_coord_value = 9; %5;
[x_data, y_data, x_label, y_label, central_fixed_value] = getSlice(prnfile, column_str, fixed_coord_str, fixed_coord_value);
plot3(x_data, fixed_coord_value*ones(size(x_data)), y_data, 'color', 'blue', 'marker', 's');

% add slices using plot3 lines
figure(3);
hold on;
column_str = 'Z3';

fixed_coord_str = 'x';
fixed_coord_value = 0.3;
[x_data, y_data, x_label, y_label, central_fixed_value] = getSlice(prnfile, column_str, fixed_coord_str, fixed_coord_value);
plot3(fixed_coord_value*ones(size(x_data)), x_data, y_data, 'color', 'red', 'marker', 'o');

fixed_coord_str = 'y';
fixed_coord_value = 0.6;
[x_data, y_data, x_label, y_label, central_fixed_value] = getSlice(prnfile, column_str, fixed_coord_str, fixed_coord_value);
plot3(x_data, fixed_coord_value*ones(size(x_data)), y_data, 'color', 'blue', 'marker', 's');

%cc = hsv(size(X,2));
%for i = 1:size(X,2)
  %fixed_coord_value = X(1,i);
  %[x_data, y_data, x_label, y_label, central_fixed_value] = getSlice(prnfile, column_str, fixed_coord_str, fixed_coord_value);
  %plot3(fixed_coord_value*ones(1,size(X,1)), x_data, y_data, 'color', cc(i,:), 'marker', 'o');
%end

%cc = hsv(size(X,1));
%for i = 1:size(X,1)
  %fixed_coord_value = Y(i,1);
  %[x_data, y_data, x_label, y_label, central_fixed_value] = getSlice(prnfile, column_str, fixed_coord_str, fixed_coord_value);
  %plot3(x_data, fixed_coord_value*ones(1,size(Y,2)), y_data, 'color', cc(i,:), 'marker', 'o');
%end
