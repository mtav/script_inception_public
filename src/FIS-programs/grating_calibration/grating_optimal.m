NA = [0.75, 1];
n = 1;
m = 1;

lambda_range_VIS = [0.340, 0.800];
lambda_range_IR = [0.900, 1.700];

%  lambda_intersection = (NA/n)*a_um/m;
%  target_um = ((NA1+NA2)/n)*(a_um/m)*(1/2)
target_um = mean(lambda_range_VIS);
a_um = target_um*(2*m)*n/(NA(1)+NA(2));
N = floor(1000/a_um);
fprintf('target_um=%.2f: a_um=%.2f -> %d lines per mm\n', target_um, a_um, N);

target_um = mean(lambda_range_IR);
a_um = target_um*(2*m)*n/(NA(1)+NA(2));
N = floor(1000/a_um);
fprintf('target_um=%.2f: a_um=%.2f -> %d lines per mm\n', target_um, a_um, N);

%  target_um=0.57: a_um=0.65 -> 1535 lines per mm
%  target_um=1.30: a_um=1.49 -> 673 lines per mm
