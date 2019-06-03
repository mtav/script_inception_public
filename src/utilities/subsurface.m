function [Nx, Ny, Nv] = subsurface(X, Y, V, limits)
  % Extract subset of surface data set
  %
  % Syntax:
  %   [Nx, Ny, Nv] = subvolume(X, Y, V, limits)
  %
  % Description:
  %   [Nx, Ny, Nv] = subvolume(X, Y, V, limits) extracts a subset of the surface data set V using the specified axis-aligned limits.
  %     limits = [X_min,X_max, Y_min,Y_max] (Any NaNs in the limits indicate that the surface should not be cropped along that axis.)
  %   The arrays X and Y define the coordinates for the surface V. The subsurface is returned in Nv and the coordinates of the subsurface are given in Nx and Ny.
  %   It assumes the arrays X and Y are defined as
  %     [X, Y] = meshgrid(y0:y0+N, x0:x0+M)
  %   where [M, N] = size(V).
  
  Z = zeros(size(V));
  
  limits(5) = NaN;
  limits(6) = NaN;
  
  [Nx, Ny, Nz, Nv] = subvolume_octave(X, Y, Z, V, limits);
  
end
