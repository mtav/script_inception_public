function saveAsPGF(outfilename, X, Y, Z)
  % Script to save meshgrid data to a .csv file, which can be directly used by PGFplots with default options
  % X,Y,Z should be so that surf(X,Y,Z) gives the desired surface plot.
  
  % open file
  out = fopen(outfilename,'wt');

  N = length(Z(:))
  
  Nx = length(X(1,:))
  Ny = length(Y(:,1))
  
  xmin = min(X(:))
  xmax = max(X(:))
  
  ymin = min(Y(:))
  ymax = max(Y(:))
  
  zmin = min(Z(:))
  zmax = max(Z(:))

  fprintf(out,'# ordering = colwise , number points = %d x %d = %d ,\n', Nx, Ny, N);
  fprintf(out,'# domain = [%f, %f] x [%f, %f] x [%f, %f]\n', xmin, xmax, ymin, ymax, zmin, zmax);
  fprintf(out,'x\ty\tz\n');

  for idx_x = 1:Nx
    for idx_y = 1:Ny
      x = X(1, idx_x);
      y = Y(idx_y, 1);
      z = Z(idx_y, idx_x);
      fprintf(out,'%f\t%f\t%f\n', x, y, z);
    end
    fprintf(out,'\n');
  end

  % close file
  fclose(out);

  %dlmwrite ('/tmp/test2.dat', X, 'newline', '\n', 'delimiter', '\t', 'append', 'on');
end
