function [Nx, Ny, Nz, Nv] = subvolume_octave(X, Y, Z, V, limits)
  % custom implementation of missing Matlab function
  %
  % Extract subset of volume data set
  %
  % Syntax:
  %   [Nx,Ny,Nz,Nv] = subvolume(X,Y,Z,V,limits)
  %
  % Description:
  %   [Nx,Ny,Nz,Nv] = subvolume(X,Y,Z,V,limits) extracts a subset of the volume data set V using the specified axis-aligned limits.
  %     limits = [X_min,X_max, Y_min,Y_max, Z_min,Z_max] (Any NaNs in the limits indicate that the volume should not be cropped along that axis.)
  %   The arrays X, Y, and Z define the coordinates for the volume V. The subvolume is returned in NV and the coordinates of the subvolume are given in NX, NY, and NZ.
  %   It assumes the arrays X, Y, and Z are defined as
  %     [X, Y, Z] = meshgrid(y0:y0+N, x0:x0+M, z0:z0+P)
  %   where [M, N, P] = size(V).
  
  if ~inoctave()
    [Nx, Ny, Nz, Nv] = subvolume(X, Y, Z, V, limits);
    return;
  else
    
    X_min = limits(1);
    X_max = limits(2);
    
    Y_min = limits(3);
    Y_max = limits(4);
    
    Z_min = limits(5);
    Z_max = limits(6);
    
    X_list = reshape(X(1,:,1),1,[]);
    Y_list = reshape(Y(:,1,1),1,[]);
    Z_list = reshape(Z(1,1,:),1,[]);
    
    if isnan(X_min)
      X_min_index = 1;
    else
      X_min_index = find( abs(X_list-X_min)==min(abs(X_list-X_min)), 1, 'first');
    end
    
    if isnan(X_max)
      X_max_index = length(X_list);
    else
      X_max_index = find( abs(X_list-X_max)==min(abs(X_list-X_max)), 1, 'last');
    end
    
    if isnan(Y_min)
      Y_min_index = 1;
    else
      Y_min_index = find( abs(Y_list-Y_min)==min(abs(Y_list-Y_min)), 1, 'first');
    end
    
    if isnan(Y_max)
      Y_max_index = length(Y_list);
    else
      Y_max_index = find( abs(Y_list-Y_max)==min(abs(Y_list-Y_max)), 1, 'last');
    end
    
    if isnan(Z_min)
      Z_min_index = 1;
    else
      Z_min_index = find( abs(Z_list-Z_min)==min(abs(Z_list-Z_min)), 1, 'first');
    end
    
    if isnan(Z_max)
      Z_max_index = length(Z_list);
    else
      Z_max_index = find( abs(Z_list-Z_max)==min(abs(Z_list-Z_max)), 1, 'last');
    end
    
    Nx = X(Y_min_index:Y_max_index, X_min_index:X_max_index, Z_min_index:Z_max_index);
    Ny = Y(Y_min_index:Y_max_index, X_min_index:X_max_index, Z_min_index:Z_max_index);
    Nz = Z(Y_min_index:Y_max_index, X_min_index:X_max_index, Z_min_index:Z_max_index);
    Nv = V(Y_min_index:Y_max_index, X_min_index:X_max_index, Z_min_index:Z_max_index);
    
  end
  
end
