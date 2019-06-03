function [snap_header, snap_data_fixed, idx_range] = BFDTD_processSlice(snapshot, xmesh, ymesh, zmesh)

  if ~exist(snapshot.snap_filename, 'file')
    error('File not found: %s', snapshot.snap_filename);
  end
  [snap_header, snap_data, snap_u, snap_v] = readPrnFile(snapshot.snap_filename, 'includeAllColumns', true);

  % snapshot direction specific handling
  switch snapshot.plane_letter
    case 'x'
      % u,v = y,z
      [ind_x, val, abs_err] = closestInd(xmesh, snapshot.plane_position);
      [idx_range.ymin, val, abs_err] = closestInd(ymesh, min(snap_u(:)));
      [idx_range.ymax, val, abs_err] = closestInd(ymesh, max(snap_u(:)));
      [idx_range.zmin, val, abs_err] = closestInd(zmesh, min(snap_v(:)));
      [idx_range.zmax, val, abs_err] = closestInd(zmesh, max(snap_v(:)));

      idx_range.xmin = ind_x;
      idx_range.xmax = ind_x;
      
      %snap_data_fixed = snap_data;
      snap_data_fixed = permute(snap_data, [2,1,3]);
      
    case 'y'
      % u,v = x,z
      [ind_y, val, abs_err] = closestInd(ymesh, snapshot.plane_position);
      [idx_range.xmin, val, abs_err] = closestInd(xmesh, min(snap_u(:)));
      [idx_range.xmax, val, abs_err] = closestInd(xmesh, max(snap_u(:)));
      [idx_range.zmin, val, abs_err] = closestInd(zmesh, min(snap_v(:)));
      [idx_range.zmax, val, abs_err] = closestInd(zmesh, max(snap_v(:)));

      idx_range.ymin = ind_y;
      idx_range.ymax = ind_y;
      
      %snap_data_fixed = snap_data;
      snap_data_fixed = permute(snap_data, [2,1,3]);
      
    case 'z'
      % u,v = x,y
      [ind_z, val, abs_err] = closestInd(zmesh, snapshot.plane_position);
      [idx_range.xmin, val, abs_err] = closestInd(xmesh, min(snap_u(:)));
      [idx_range.xmax, val, abs_err] = closestInd(xmesh, max(snap_u(:)));
      [idx_range.ymin, val, abs_err] = closestInd(ymesh, min(snap_v(:)));
      [idx_range.ymax, val, abs_err] = closestInd(ymesh, max(snap_v(:)));

      idx_range.zmin = ind_z;
      idx_range.zmax = ind_z;
      
      snap_data_fixed = snap_data;
      % snap_data_fixed = permute(snap_data, [2,1,3]);
      
    otherwise
      error('Invalid direction: snapshot.plane_letter = %s', snapshot.plane_letter);
  end
end
