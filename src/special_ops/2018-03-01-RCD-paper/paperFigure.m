% TODO: Linked ranges...
% TODO: Put into array...
% TODO: Add labels...

set(0,'DefaultFigureWindowStyle','docked');

xlim_list = {};
ylim_list = {};
zlim_list = {};

xrange_list = [];
yrange_list = [];
zrange_list = [];

fig = {};

% 3D plots
fig{01} = open('./FIGs-4ANONYMIZED/Data/09102017/RCD111-size=10x10x10-n_defect=3.30.n_crystal=1.00.n_backfill=3.30-defectPos=2.0-sphere/0.100a/Emod2/Emode2_defect_mask_z.fixColor.fig');
xlim_list{end+1} = xlim(); ylim_list{end+1} = ylim(); zlim_list{end+1} = zlim();
xrange_list(end+1,:) = xlim(); yrange_list(end+1,:) = ylim(); zrange_list(end+1,:) = zlim();
fig{02} = open('./FIGs-4ANONYMIZED/Data/09102017/RCD111-size=10x10x10-n_defect=3.30.n_crystal=1.00.n_backfill=3.30-defectPos=2.0-sphere/0.100a/Emod2/Emode2_defect_mask_x.fixColor.fig');
xlim_list{end+1} = xlim(); ylim_list{end+1} = ylim(); zlim_list{end+1} = zlim();
xrange_list(end+1,:) = xlim(); yrange_list(end+1,:) = ylim(); zrange_list(end+1,:) = zlim();
fig{03} = open('./FIGs-4ANONYMIZED/Data/09102017/RCD111-size=10x10x10-n_defect=3.30.n_crystal=1.00.n_backfill=3.30-defectPos=2.0-sphere/0.100a/Emod2/Emode2_defect_mask_y.fixColor.fig');
xlim_list{end+1} = xlim(); ylim_list{end+1} = ylim(); zlim_list{end+1} = zlim();
xrange_list(end+1,:) = xlim(); yrange_list(end+1,:) = ylim(); zrange_list(end+1,:) = zlim();
view([0,1,0]);
set(gca,'Zdir','reverse');
set(gca,'Xdir','reverse');
set(gca,'XAxisLocation','top');
camroll(90);

% 2D plots
fig{04} = open('./FIGs-4ANONYMIZED/Data/09102017/RCD111-size=10x10x10-n_defect=3.30.n_crystal=1.00.n_backfill=3.30-defectPos=2.0-sphere/0.100a/Emod2/ret.MV.info_limit.MaximumEmod2_3.fixColor.fig');
xlim_list{end+1} = xlim(); ylim_list{end+1} = ylim(); zlim_list{end+1} = zlim();
xrange_list(end+1,:) = xlim();
fig{05} = open('./FIGs-4ANONYMIZED/Data/09102017/RCD111-size=10x10x10-n_defect=3.30.n_crystal=1.00.n_backfill=3.30-defectPos=2.0-sphere/0.100a/Emod2/ret.MV.info_limit.MaximumEmod2_4.fixColor.fig');
xlim_list{end+1} = xlim(); ylim_list{end+1} = ylim(); zlim_list{end+1} = zlim();
yrange_list(end+1,:) = xlim();
fig{06} = open('./FIGs-4ANONYMIZED/Data/09102017/RCD111-size=10x10x10-n_defect=3.30.n_crystal=1.00.n_backfill=3.30-defectPos=2.0-sphere/0.100a/Emod2/ret.MV.info_limit.MaximumEmod2_5.fixColor.fig');
xlim_list{end+1} = xlim(); ylim_list{end+1} = ylim(); zlim_list{end+1} = zlim();
zrange_list(end+1,:) = xlim();

% 3D plots
fig{07} = open('./FIGs-4ANONYMIZED/Data/16052016/rerun_single_sphere/0.100a/Fig/Emod2/Emode2_defect_mask_z.fixColor.fig');
xlim_list{end+1} = xlim(); ylim_list{end+1} = ylim(); zlim_list{end+1} = zlim();
xrange_list(end+1,:) = xlim(); yrange_list(end+1,:) = ylim(); zrange_list(end+1,:) = zlim();
fig{08} = open('./FIGs-4ANONYMIZED/Data/16052016/rerun_single_sphere/0.100a/Fig/Emod2/Emode2_defect_mask_x.fixColor.fig');
xlim_list{end+1} = xlim(); ylim_list{end+1} = ylim(); zlim_list{end+1} = zlim();
xrange_list(end+1,:) = xlim(); yrange_list(end+1,:) = ylim(); zrange_list(end+1,:) = zlim();
fig{09} = open('./FIGs-4ANONYMIZED/Data/16052016/rerun_single_sphere/0.100a/Fig/Emod2/Emode2_defect_mask_y.fixColor.fig');
xlim_list{end+1} = xlim(); ylim_list{end+1} = ylim(); zlim_list{end+1} = zlim();
xrange_list(end+1,:) = xlim(); yrange_list(end+1,:) = ylim(); zrange_list(end+1,:) = zlim();
view([0,1,0]);
set(gca,'Zdir','reverse');
set(gca,'Xdir','reverse');
set(gca,'XAxisLocation','top');
camroll(90);

% 2D plots
fig{10} = open('./FIGs-4ANONYMIZED/Data/16052016/rerun_single_sphere/0.100a/Fig/Emod2/ret.MV.info_limit.MaximumEmod2_3.fixColor.fig');
xlim_list{end+1} = xlim(); ylim_list{end+1} = ylim(); zlim_list{end+1} = zlim();
xrange_list(end+1,:) = xlim();
fig{11} = open('./FIGs-4ANONYMIZED/Data/16052016/rerun_single_sphere/0.100a/Fig/Emod2/ret.MV.info_limit.MaximumEmod2_4.fixColor.fig');
xlim_list{end+1} = xlim(); ylim_list{end+1} = ylim(); zlim_list{end+1} = zlim();
yrange_list(end+1,:) = xlim();
fig{12} = open('./FIGs-4ANONYMIZED/Data/16052016/rerun_single_sphere/0.100a/Fig/Emod2/ret.MV.info_limit.MaximumEmod2_5.fixColor.fig');
xlim_list{end+1} = xlim(); ylim_list{end+1} = ylim(); zlim_list{end+1} = zlim();
zrange_list(end+1,:) = xlim();

%  figure(1); xrange_list(end+1,:) = xlim()
%  figure(4); diff(xlim)
%  figure(7); diff(xlim)
%  figure(10); diff(xlim)
%  figure(3); xlim();
%  figure(9); xlim();
%  
%  figure(2); diff(xlim)
%  figure(5); diff(xlim)
%  figure(8); diff(xlim)
%  figure(11); diff(xlim)
%  
%  figure(3); diff(xlim)
%  figure(6); diff(xlim)
%  figure(9); diff(xlim)
%  figure(12); diff(xlim)

%xrange_min = Inf;
%xrange_max = -Inf;

%for idx=1:length(xrange_list)
  %[a,b] = xrange_list{idx}
%end

xrange_min = max(xrange_list(:,1));
xrange_max = min(xrange_list(:,2));

yrange_min = max(yrange_list(:,1));
yrange_max = min(yrange_list(:,2));

zrange_min = max(zrange_list(:,1));
zrange_max = min(zrange_list(:,2));

xc = mean([xrange_min, xrange_max])
yc = mean([yrange_min, yrange_max])
zc = mean([zrange_min, zrange_max])

%vline_color = [175, 171, 171]/255;
vline_color = [0, 0, 0];

figure(fig{01}); xlim([xrange_min, xrange_max]); ylim([yrange_min, yrange_max]); zlim([zrange_min, zrange_max]);
plot3_xline(xc, 'Color', vline_color);
delete(findall(gcf,'Type','light')); camlight('headlight');
figure(fig{02}); xlim([xrange_min, xrange_max]); ylim([yrange_min, yrange_max]); zlim([zrange_min, zrange_max]);
plot3_yline(yc, 'Color', vline_color);
delete(findall(gcf,'Type','light')); camlight('headlight');
figure(fig{03}); xlim([xrange_min, xrange_max]); ylim([yrange_min, yrange_max]); zlim([zrange_min, zrange_max]);
plot3_zline(zc, 'Color', vline_color);
delete(findall(gcf,'Type','light')); camlight('headlight');

figure(fig{04}); xlim([xrange_min, xrange_max]);
plot3_xline(xc, 'Color', vline_color);
figure(fig{05}); xlim([yrange_min, yrange_max]);
plot3_xline(yc, 'Color', vline_color);
figure(fig{06}); xlim([zrange_min, zrange_max]);
plot3_xline(zc, 'Color', vline_color);

figure(fig{07}); xlim([xrange_min, xrange_max]); ylim([yrange_min, yrange_max]); zlim([zrange_min, zrange_max]);
plot3_xline(xc, 'Color', vline_color);
delete(findall(gcf,'Type','light')); camlight('headlight');
figure(fig{08}); xlim([xrange_min, xrange_max]); ylim([yrange_min, yrange_max]); zlim([zrange_min, zrange_max]);
plot3_yline(yc, 'Color', vline_color);
delete(findall(gcf,'Type','light')); camlight('headlight');
figure(fig{09}); xlim([xrange_min, xrange_max]); ylim([yrange_min, yrange_max]); zlim([zrange_min, zrange_max]);
plot3_zline(zc, 'Color', vline_color);
delete(findall(gcf,'Type','light')); camlight('headlight');

figure(fig{10}); xlim([xrange_min, xrange_max]);
plot3_xline(xc, 'Color', vline_color);
figure(fig{11}); xlim([yrange_min, yrange_max]);
plot3_xline(yc, 'Color', vline_color);
figure(fig{12}); xlim([zrange_min, zrange_max]);
plot3_xline(zc, 'Color', vline_color);

%view(); camroll(-90);

% paperFigure_save();

% fig_main = combineFigures(fig, 4, 3);

% paperFigure_postprocessing();
