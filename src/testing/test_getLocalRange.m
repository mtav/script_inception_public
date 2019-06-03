close all;
clear all;

x = linspace(-2, 2, 100);
y = linspace(-3, 3, 50);
[X, Y] = meshgrid(x, y);
Z = peaks(X,Y);

xmin=-1
xmax=1
ymin=-3
ymax=-1

subplot(3, 1, 1);
surf(X, Y, Z);
%axis equal;
view(2);
shading flat;
c1 = colorbar();
xlim([xmin,xmax]);
ylim([ymin,ymax]);

I2 = find(xmin<=X & X<=xmax & ymin<=Y & Y<=ymax);
%IX = find(-1<=X & X<=1);
%IY = find(-3<=Y & Y<=-1);

[I,J] = ind2sub(size(Z), I2);

X2=X(I,J);
Y2=Y(I,J);
Z2=Z(I,J);

subplot(3, 1, 2);
surf(X2,Y2,Z2);
%axis equal;
view(2);
shading flat;
c2 = colorbar();
xlim([xmin,xmax]);
ylim([ymin,ymax]);

%subplot(3, 1, 3);
%surf(X(I2), Y(I2), Z(I2));
%axis equal;
%view(2);
%shading flat;
%c3 = colorbar();

figure();
imagesc(Z2);
