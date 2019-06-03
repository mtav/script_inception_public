function subsurface_test(xmin, xmax, ymin, ymax)
  close all;
  %clear all;

  [X,Y,Z] = peaks(25);

  figure;

  subplot(1, 2, 1);
  surf(X, Y, Z);

  [Nx, Ny, Nz] = subsurface(X, Y, Z, [xmin, xmax, ymin, ymax]);

  subplot(1, 2, 2);
  surf(Nx, Ny, Nz);
end
