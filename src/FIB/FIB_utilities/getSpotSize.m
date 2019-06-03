function spotSize_mum = getSpotSize(beamCurrent)
  % function spotSize_mum = getSpotSize(beamCurrent)
  
  % size of circles in nm as a function of the beamcurrent
  spotSizes_nm = [1 8;
  4 12;
  11 15;
  70 25;
  150 35;
  350 55;
  1000 80;
  2700 120;
  6600 270;
  11500 500;
  ];
  beamCurrent_idx = find(spotSizes_nm==beamCurrent); % this is dangerous. Might find a spotsize value instead of beamcurrent value... TODO: Fix.
  if isempty(beamCurrent_idx)
    error( [ 'Invalid beamCurrent. Valid values are: ', num2str(reshape(spotSizes_nm(:,1),1,[])) ] )
  else
    % size of a circle in mum
    spotSize_mum = spotSizes_nm(beamCurrent_idx,2)*1e-3;
  end
end
