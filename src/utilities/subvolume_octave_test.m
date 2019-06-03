function subvolume_octave_test(xmin, xmax, ymin, ymax, zmin, zmax)
  close all;
  %clear all;

  [X, Y, Z] = meshgrid(-2:.2:2,-2:.25:2,-2:.16:2);
  V = X.*exp(-X.^2-Y.^2-Z.^2);
  xslice = [-1.2,.8,2];
  yslice = 2; 
  zslice = [-2,0];

  figure;

  subplot(2,2,1);
  slice(X, Y, Z, V, xslice, yslice, zslice);
  colormap hsv;
  xlabel('x'); ylabel('y'); zlabel('z');

  subplot(2,2,2);
  xslice_mid = ( min(X(:)) + max(X(:)) )/2;
  yslice_mid = ( min(Y(:)) + max(Y(:)) )/2;
  zslice_mid = ( min(Z(:)) + max(Z(:)) )/2;
  slice(X, Y, Z, V, xslice_mid, yslice_mid, zslice_mid);
  colormap hsv;
  xlabel('x'); ylabel('y'); zlabel('z');

  %xmin = 0;
  %xmax = 1;
  %ymin = -1;
  %ymax = 0.5;
  %zmin = -0.6;
  %zmax = 1.2;
  limits =  [xmin, xmax, ymin, ymax, zmin, zmax];
  [Nx,Ny,Nz,Nv] = subvolume_octave(X, Y, Z, V, limits);

  subplot(2,2,3);
  slice(Nx, Ny, Nz, Nv, xslice, yslice, zslice);
  colormap hsv;
  xlabel('x'); ylabel('y'); zlabel('z');

  subplot(2,2,4);
  xslice_mid = ( min(Nx(:)) + max(Nx(:)) )/2;
  yslice_mid = ( min(Ny(:)) + max(Ny(:)) )/2;
  zslice_mid = ( min(Nz(:)) + max(Nz(:)) )/2;
  slice(Nx, Ny, Nz, Nv, xslice_mid, yslice_mid, zslice_mid);
  colormap hsv;
  xlabel('x'); ylabel('y'); zlabel('z');
end
