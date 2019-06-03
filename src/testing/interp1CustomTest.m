close all;
clear all;

index_list = rand(1,20)*5;
a = 1:length(index_list(:));
TABLE = [index_list(:), a'];

x = TABLE(:,1);
y = TABLE(:,2);

data_esnap = (5+2)*rand(50,100)-1;
data_esnap_mod = interp1Custom(x, y, data_esnap, 'nearest', 'extrap');
%data_esnap_mod = interp1Custom(x, y, data_esnap, 'nearest');

[xs, p] = sort (x);
ys = y(p,:);

plot(xs, ys, 'r-', data_esnap(:), data_esnap_mod(:), 'b*');
vline(0.5*(xs(2:end)+xs(1:end-1)), 'r-');

ys(1)
ys(end)

if any(isnan(data_esnap_mod))
  error('NaNs found');
else
  disp('all OK');
end
