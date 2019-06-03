function [ filename, alphaID, pair ] = numID_to_alphaID_TimeSnapshot(numID, snap_plane, probe_ident, snap_time_number)
  % function [ filename, alphaID, pair ] = numID_to_alphaID_TimeSnapshot(numID, snap_plane, probe_ident, snap_time_number)
  %
  % IMPORTANT: These functions are only valid for BFDTD 2003 past "az" (2*26). Since BFDTD 2008 up to BFDTD 2013, "ba" comes after "az" instead of "a{".
  % TODO: Update code and please, stop using FDTD 2003!!!
  %
  %  Converts numeric IDs to alpha IDs used by Bristol FDTD 2003
  %
  %  return values:
  %  filename, alphaID, pair
  %
  %  examples:
  %  99 -> 99
  %  100 -> :0
  
  % convert to char in case we get cells
  snap_plane = char(snap_plane);
  probe_ident = char(probe_ident);
  
  % "constants" % TODO: find a way to share them between python, matlab/octave and other codes (config files?) Or compute them, or just leave it as is...
  TIMESNAPSHOT_MAX = 439;
  
  % default values
  if exist('snap_plane','var')==0
    snap_plane = 'x';
  end
  
  if exist('probe_ident','var')==0
    probe_ident = '_id_';
  end
  
  if exist('snap_time_number','var')==0
    snap_time_number = 0;
  end
  
  % safety checks
  if ( numID < 1 ) || ( numID > TIMESNAPSHOT_MAX )
    error(['ERROR: numID must be between 1 and ',num2str(TIMESNAPSHOT_MAX),' or else you will suffer death by monkeys!!!']);
  end
  
  if ( snap_time_number < 0 ) || ( snap_time_number > 99 )
    error('ERROR: snap_time_number must be between 0 and 99 or else you will suffer death by monkeys!!!');
  end
  
  % actual conversion
  ilo = mod(snap_time_number, 10);
  ihi = floor(snap_time_number / 10);
  
  if (numID < 10)
    alphaID = char(numID + double('0'));
  else
    alphaID = [char(floor(numID/10) + double('0')), char(mod(numID,10) + double('0'))];
  end
  
  filename = [snap_plane, alphaID, probe_ident, char(ihi + double('0')), char(ilo + double('0')), '.prn'];
  filename = char(filename);
  pair = [num2str(numID), ':', alphaID];    
end
