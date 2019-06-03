% create a theoretical dipole "energy distribution"
% cf "Introduction to electrodynamics" by David J. Griffiths, p444-451

x=linspace(-1,1,100);
y=x;
z=x;
[X,Y,Z] = meshgrid(x,y,z);
[azimuth,elevation,r] = cart2sph(X,Y,Z);
theta=elevation-pi/2;
S=((sin(theta)).^2)./r.^2;
log_S = log(S);

contourslice(X,Y,Z,log(S),[0],[0],[0]);
colormap hsv;

h5file='dipole.h5';

h5create(h5file, '/S',size(S));
h5write(h5file, '/S', S);

h5create(h5file, '/log_S',size(log_S));
h5write(h5file, '/log_S', log_S);
