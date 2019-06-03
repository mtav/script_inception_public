function plotSnapshotBasic(filename, column)
  [header, data, u1, u2] = readPrnFile(filename, 'includeAllColumns', true);
  U1 = data(:, :, 1);
  U2 = data(:, :, 2);
  U3 = data(:, :, column);
  
  %[U1,U2] = meshgrid(u1,u2);
  %U3 = data(:, :, column);
  
  size(U1)
  size(U2)
  size(U3)
  figure;
  subplot(1,4,1); imagesc(U1);
  subplot(1,4,2); imagesc(U2);
  subplot(1,4,3); imagesc(U3);
  
  subplot(1,4,4);
  surf(U1, U2, U3);
  view(2);
  shading flat;
  axis tight;
  axis equal;
  xlabel(header{1});
  ylabel(header{2});
end
