function ret = thesis_readPrnFiles(x_snap, y_snap, z_snap, dirtype)

  ret = struct();

  [x_header, x_data, x_u1, x_u2] = readPrnFile(x_snap, 'includeAllColumns', true);
  [y_header, y_data, y_u1, y_u2] = readPrnFile(y_snap, 'includeAllColumns', true);
  [z_header, z_data, z_u1, z_u2] = readPrnFile(z_snap, 'includeAllColumns', true);
  %[x_U1, x_U2] = meshgrid(x_u1, x_u2);
  %[y_U1, y_U2] = meshgrid(y_u1, y_u2);
  %[z_U1, z_U2] = meshgrid(z_u1, z_u2);
  
  if dirtype==3
    ret.x.header = x_header;
    %ret.x_U1 = y_U1;
    %ret.x_U2 = y_U2;
    ret.x.data = y_data;
    
    ret.y.header = y_header;
    %ret.y_U1 = x_U1;
    %ret.y_U2 = x_U2;
    ret.y.data = x_data;
    
    ret.z.header = z_header;
    %ret.z_U1 = permute(z_U2, [2,1,3]);
    %ret.z_U2 = permute(z_U1, [2,1,3]);
    swapped_data = z_data;
    swapped_data(:,:,1) = z_data(:,:,2);
    swapped_data(:,:,2) = z_data(:,:,1);
    ret.z.data = permute(swapped_data, [2,1,3]);
  else
    ret.x.header = x_header;
    %ret.x_U1 = x_U1;
    %ret.x_U2 = x_U2;
    ret.x.data = x_data;
    
    ret.y.header = y_header;
    %ret.y_U1 = y_U1;
    %ret.y_U2 = y_U2;
    ret.y.data = y_data;
    
    ret.z.header = z_header;
    %ret.z_U1 = z_U1;
    %ret.z_U2 = z_U2;
    ret.z.data = z_data;
  end
  
end
