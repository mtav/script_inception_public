% Simple script to check that the numID/alphaID conversion is consistent in both direction for all BFDTD versions.

snap_plane = 'y';
probe_ident = 'cool';
snap_time_number = 42;

version_list = {'2003', '2008', '2013'};

for version_idx = 1:length(version_list)
  BFDTD_version = version_list{version_idx};
  disp(['==> BFDTD_version = ', BFDTD_version]);

  for numID = 1:806
    [ f_filename, f_alphaID, f_pair ] = numID_to_alphaID_FrequencySnapshot(numID, 'snap_plane', snap_plane, 'probe_ident', probe_ident, 'snap_time_number', snap_time_number, 'BFDTD_version', BFDTD_version);
    [ fout_numID, fout_snap_plane, fout_snap_time_number, fout_ok ] = alphaID_to_numID(f_filename, 'probe_ident', probe_ident, 'BFDTD_version', BFDTD_version);

    %[ t_filename, t_alphaID, t_pair ] = numID_to_alphaID_TimeSnapshot(numID, snap_plane, probe_ident, snap_time_number);
    %[ tout_numID, tout_snap_plane, tout_snap_time_number, tout_ok ] = alphaID_to_numID(t_filename, 'probe_ident', probe_ident, 'BFDTD_version', BFDTD_version);
    %disp(['fout_numID: ', num2str(fout_numID), ' - f_alphaID: ', f_alphaID, ' - t_alphaID: ', t_alphaID]);

    disp(['numID: ', num2str(numID), ' - fout_numID: ', num2str(fout_numID), ' - f_alphaID: ', f_alphaID, ' - f_filename: ', f_filename]);
    if numID - fout_numID ~=0
      error(['for BFDTD_version = ', BFDTD_version]);
    end
    
  end

end

% test with default args
for numID = 1:806
  [ f_filename, f_alphaID, f_pair ] = numID_to_alphaID_FrequencySnapshot(numID);
  [ fout_numID, fout_snap_plane, fout_snap_time_number, fout_ok ] = alphaID_to_numID(f_filename);

  disp(['numID: ', num2str(numID), ' - fout_numID: ', num2str(fout_numID), ' - f_alphaID: ', f_alphaID, ' - f_filename: ', f_filename]);
  if numID - fout_numID ~=0
    error('with default args');
  end
  
end

% direct test
for numID = 1:806
  disp(['numID = ', num2str(numID)])
  if alphaID_to_numID(numID_to_alphaID_FrequencySnapshot(numID)) ~= numID
    error();
  end  
end

% direct test with versions
for version_idx = 1:length(version_list)
  BFDTD_version = version_list{version_idx};
  disp(['==> BFDTD_version = ', BFDTD_version]);
  for numID = 1:806
    disp(['numID = ', num2str(numID)])
    if alphaID_to_numID(numID_to_alphaID_FrequencySnapshot(numID, 'BFDTD_version', BFDTD_version), 'BFDTD_version', BFDTD_version) ~= numID
      error(['for BFDTD_version = ', BFDTD_version]);
    end  
  end
end
