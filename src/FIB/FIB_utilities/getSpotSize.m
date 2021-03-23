function beamDiameter_mum = getSpotSize(beamCurrent_pA)
  % Returns the diameter of the beam (also known as spot size) at the sample surface in mum as a function of the beamcurrent in pA.
  %
  % Usage:
  %   beamDiameter_mum = getSpotSize(beamCurrent_pA)
  %
  
  FIB_infos_struct = FIB_infos();

  % FIB_infos_struct.beamInfos
  % beamCurrent_pA
  
  % prepare array of the right size
  beamDiameter_mum = NaN*ones(size(beamCurrent_pA));
  
  % fill array with corresponding beam diameter values
  for array_pos = 1:numel(beamCurrent_pA)
    beamCurrent_pA_current = beamCurrent_pA(array_pos);
    
    beamCurrent_idx = find(beamCurrent_pA_current == FIB_infos_struct.beamInfos.beamCurrent_pA);
    if isempty(beamCurrent_idx)
      % error_message = 'Invalid beamCurrent. Valid values are: ';
      % for i = FIB_infos_struct.beamInfos.beamCurrent_pA
        % error_message = [ error_message, sprintf('\n  %d', i) ];
      % end
      % error('getSpotSize:invalidBeamCurrent', error_message);
      warning(['Invalid beamCurrent: ', num2str(beamCurrent_pA_current)]);
    else
      beamDiameter_mum(array_pos) = FIB_infos_struct.beamInfos.beamDiameter_mum(beamCurrent_idx);
    end
  end
  
end
