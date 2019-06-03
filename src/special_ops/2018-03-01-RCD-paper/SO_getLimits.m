xrange_list = []; yrange_list = []; zrange_list = [];

figure(1);
xrange_list(end+1, :) = xlim(); yrange_list(end+1, :) = ylim(); zrange_list(end+1, :) = zlim();
figure(2);
xrange_list(end+1, :) = xlim(); yrange_list(end+1, :) = ylim(); zrange_list(end+1, :) = zlim();
figure(3);
xrange_list(end+1, :) = xlim(); yrange_list(end+1, :) = ylim(); zrange_list(end+1, :) = zlim();

figure(4);
xrange_list(end+1, :) = xlim();
figure(5);
yrange_list(end+1, :) = xlim();
figure(6);
zrange_list(end+1, :) = xlim();

xrange_list
yrange_list
zrange_list

xrange_min = max(xrange_list(:,1));
xrange_max = min(xrange_list(:,2));

yrange_min = max(yrange_list(:,1));
yrange_max = min(yrange_list(:,2));

zrange_min = max(zrange_list(:,1));
zrange_max = min(zrange_list(:,2));

xc = mean([xrange_min, xrange_max])
yc = mean([yrange_min, yrange_max])
zc = mean([zrange_min, zrange_max])
