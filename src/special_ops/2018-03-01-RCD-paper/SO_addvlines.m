%vline_color = [175, 171, 171]/255;
vline_color = [0, 0, 0];

figure(1); xlim([xrange_min, xrange_max]); ylim([yrange_min, yrange_max]); zlim([zrange_min, zrange_max]);
plot3_xline(xc, 'Color', vline_color);
delete(findall(gcf,'Type','light')); camlight('headlight');
figure(3); xlim([xrange_min, xrange_max]); ylim([yrange_min, yrange_max]); zlim([zrange_min, zrange_max]);
plot3_yline(yc, 'Color', vline_color);
delete(findall(gcf,'Type','light')); camlight('headlight');
figure(2); xlim([xrange_min, xrange_max]); ylim([yrange_min, yrange_max]); zlim([zrange_min, zrange_max]);
plot3_zline(zc, 'Color', vline_color);
delete(findall(gcf,'Type','light')); camlight('headlight');

figure(4); xlim([xrange_min, xrange_max]);
plot3_xline(xc, 'Color', vline_color);
figure(5); xlim([yrange_min, yrange_max]);
plot3_xline(yc, 'Color', vline_color);
figure(6); xlim([zrange_min, zrange_max]);
plot3_xline(zc, 'Color', vline_color);
