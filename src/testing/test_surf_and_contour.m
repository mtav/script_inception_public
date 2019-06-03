close all;
clear all;

Ngridlines = 25;
[Xc, Yc] = meshgrid(linspace(-5, 5, 50), linspace(-2.5, 2.5, 100));
Xs = Xc;
Ys = Yc;
Zc = peaks(Xc,Yc);
Zs = peaks(Xs,Ys);

%[Xc, Yc, Zc] = peaks(Ngridlines);
%[Xs, Ys, Zs] = sombrero_custom(Ngridlines);

xc_vals = Xc(1,:);
yc_vals = Yc(:,1);
xc_vals = xc_vals(:);
yc_vals = yc_vals(:);

xc_min = min(Xc(:));
xc_max = max(Xc(:));
yc_min = min(Yc(:));
yc_max = max(Yc(:));
zc_min = min(Zc(:));
zc_max = max(Zc(:));

xs_min = min(Xs(:));
xs_max = max(Xs(:));
ys_min = min(Ys(:));
ys_max = max(Ys(:));
zs_min = min(Zs(:));
zs_max = max(Zs(:));

xmin = min( min(Xs(:)), min(Xc(:)) );
xmax = max( max(Xs(:)), max(Xc(:)) );

ymin = min( min(Ys(:)), min(Yc(:)) );
ymax = max( max(Ys(:)), max(Yc(:)) );

Zc0 = 1.1*max(Zs(:));

%figure;
%surf(Xs, Ys, Zs);
%view(2);
%xlim([xmin, xmax]);
%ylim([ymin, ymax]);

%figure;
%[C, h] = contour(Xc, Yc, Zc);
%view(2);
%xlim([xmin, xmax]);
%ylim([ymin, ymax]);

%figure;
%subplot(1,2,1);
%plot(Xc(1,:));
%title('Xc values');
%subplot(1,2,2);
%plot(Yc(:,1));
%title('Yc values');

%figure;
%[C, h] = contourAtZ(Zc0, Xc, Yc, Zc);
%view(2);
%xlim([xmin, xmax]);
%ylim([ymin, ymax]);

%figure;
%surf(Xs, Ys, Zs);
%[C, h] = contourAtZ(Zc0, Xc, Yc, Zc);
%view(2);
%xlim([xmin, xmax]);
%ylim([ymin, ymax]);

%figure;
%surf(Xs, Ys, Zs);
%[C, h] = contourAtZ(Zc0, Xc, Yc, Zc, 'colormap', [0,0,0]);
%view(2);
%xlim([xmin, xmax]);
%ylim([ymin, ymax]);

%figure;
%[C, h] = contourAtZ(Zc0, Xc, Yc, Zc, 'colormap', [0,0,0]);
%view(2);
%xlim([xmin, xmax]);
%ylim([ymin, ymax]);

figure;
subplot(1,2,1);
surf(Xs, Ys, Zs);
[C, h] = contourAtZ(Zc0, Xc, Yc, Zc, 'colormap', [0,0,0], 'contourValues', 3);
view(2);
shading flat;
xlim([xmin, xmax]);
ylim([ymin, ymax]);

subplot(1,2,2);
surf(Ys, Xs, Zs);
[C, h] = contourAtZ(Zc0, Yc, Xc, Zc, 'colormap', [0,0,0], 'contourValues', [4,-4], 'LineWidth', 5);
view(2);
shading flat;
xlim(getRange(Yc));
ylim(getRange(Xc));
