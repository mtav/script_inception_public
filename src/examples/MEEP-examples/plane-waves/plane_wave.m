k = [1,1];
k=(2*pi/1)*k/norm(k);
kx = dot(k,[1,0]);
ky = dot(k,[0,1]);

[X,Y] = meshgrid(linspace(-2,2), linspace(-2,2));
Z = cos(kx.*X+ky.*Y);
surf(X,Y,Z, 'EdgeColor','none');
view(2);
