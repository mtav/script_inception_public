function data_esnap = setPermittivityInObject(data_esnap, column_1_esnap, column_2_esnap, snap_plane_position, snap_plane_orientation, new_permittivity, object)
  % unfinished function supposed to modify an epsilon snapshot by changing values inside object to new_permittivity.
  % used in calculateModeVolume()
  % TODO: finish this?
  
  error('Unfinished function');
  
  switch snap_plane_orientation
    case 'x'
      [X,Y,Z] = meshgrid(snap_plane_position, column_1_esnap, column_2_esnap);
      V = 0;
    case 'y'
      disp('y')
    case 'z'
      disp('z')
    otherwise
      error('invalid snap_plane_orientation');
  end
  
  size(X)
  
  return
  
  size(data_esnap), snap_plane, new_permittivity, object
  
  Snaps{m}.pos
  
  if strcmp(snap_plane_orientation,'x')
    % k->plane->x, j->col1->y, i->col2->z
    x = Snaps{m}.pos;
    y = column_1_esnap(column_1_index);
    z = column_2_esnap(column_2_index);
  elseif strcmp(snap_plane_orientation,'y')
    % k->plane->y, j->col1->x, i->col2->z
    x = column_1_esnap(column_1_index);
    y = Snaps{m}.pos;
    z = column_2_esnap(column_2_index);
  else
    % k->plane->z, j->col1->x, i->col2->y
    x = column_1_esnap(column_1_index);
    y = column_2_esnap(column_2_index);
    z = Snaps{m}.pos;
  end
  
end
