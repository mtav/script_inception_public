function [ numID, snap_plane, snap_time_number, ok ] = alphaID_to_numID(alphaID, varargin)
  % function [ numID, snap_plane, snap_time_number, ok ] = alphaID_to_numID(alphaID, varargin)
  %
  % Converts alpha IDs used by Bristol FDTD to numeric IDs.
  % Note that it is currently only designed for frequency snapshots.
  % IMPORTANT: Since BFDTD 2008 up to BFDTD 2013, "ba" comes after "az" instead of "a{". Please stop using the old BFDTD 2003.
  %
  % Usage:
  %  [ numID, snap_plane, snap_time_number, ok ] = alphaID_to_numID(alphaID)
  %  [ numID, snap_plane, snap_time_number, ok ] = alphaID_to_numID(alphaID, 'pre_2008_BFDTD_version', true)
  %  [ numID, snap_plane, snap_time_number, ok ] = alphaID_to_numID(alphaID, 'probe_ident', 'a')
  %
  % Arguments:
  %  Required:
  %   alphaID: filename or "alphaID" ('az', 'zc', etc)
  %  Parameter-value pairs:
  %   'pre_2008_BFDTD_version': true (version<2008) or false (version>=2008) (important if more than 52 snapshots are used!). The default is 'false'.
  %   'probe_ident': Default='_id_'
  %
  % Examples:
  % z -> 26
  % a{ -> 26+27 (BFDTD 2003 only, invalid for BFDTD 2008/2013)
  % MAXIMUM NUMBER OF SNAPSHOTS: 32767 (=(2^8)*(2^8)/2 -1)
  % MAXIMUM NUMBER OF SNAPSHOTS BEFORE RETURN to aa: 6938 = 26+256*27
  % MAXIMUM NUMBER OF SNAPSHOTS BEFORE DUPLICATE IDs: 4508 = 26+(6-(ord('a')-1)+256)*27+1 (6=character before non-printable bell character)
  % MAXIMUM NUMBER OF SNAPSHOTS BEFORE ENTERING DANGER AREA (non-printable characters): 836 = 26+(126-(ord('a')-1))*27
  %
  % 1-26 : a-z
  % 27: {
  % 28: |
  % 29: }
  % 30: ~
  %
  % TODO: Make it work for time snapshots as well. Currently only works for frequency snapshots.
  % TODO: fix this error: alphaID_to_numID('x{a_id_00.prn') -> ans =  703 (should be invalid for newer BFDTD versions)
  
  %%%%%%%%
  % Valid value lists, yes, because after validating once, we need to validate again to make sure we actually get valid values...

  % create parser
  p = inputParser();
  p = inputParserWrapper(p, 'addRequired', 'alphaID', @ischar);
  p = inputParserWrapper(p, 'addParamValue', 'probe_ident', '_id_', @ischar);
  p = inputParserWrapper(p, 'addParamValue', 'pre_2008_BFDTD_version', false, @islogical);
  
  % parse arguments
  p = inputParserWrapper(p, 'parse', alphaID, varargin{:});

  %%%%%%%%
  
  % default return values in case of errors
  numID = -1;
  snap_plane = '';
  snap_time_number = -1;
  ok = false;
    
  % take the basename, just in case it's a full filepath
  alphaID = basename(p.Results.alphaID);
  
  % step 1: extract just alphaID
  if p.Results.pre_2008_BFDTD_version
    alphaID_pattern = '([a-z\{\|\}~][a-z\{]|[a-z])';
  else
    alphaID_pattern = '([a-z\{\|\}~][a-z]|[a-z])';
  end
  
  if length(alphaID)==1 || length(alphaID)==2
    if inoctave()
      [tokens, match] =  regexp(alphaID, alphaID_pattern, 'tokens', 'match');
    else
      [tokens, match] =  regexp(alphaID, alphaID_pattern, 'tokens', 'match', 'warnings');
    end
    if length(match)==1 && strcmp(match, alphaID) % we also need to check that it's a complete match
      just_alphaID = alphaID;
    else
      error(['Match error. Invalid alphaID:', ' alphaID=', alphaID, ' probe_ident=', p.Results.probe_ident]);
    end
  elseif length(alphaID) > 2
    if inoctave()
      [tokens, match] =  regexp(alphaID, ['([xyz])', alphaID_pattern, p.Results.probe_ident, '(..)\.prn'], 'tokens', 'match');
    else
      [tokens, match] =  regexp(alphaID, ['([xyz])', alphaID_pattern, p.Results.probe_ident, '(..)\.prn'], 'tokens', 'match', 'warnings');
    end
    if length(match) == 1
      snap_plane = char(tokens{:}(1));
      just_alphaID = tokens{:}{2};
      snap_time_number = str2num(tokens{:}{3});
    else
      error(['Match error. Invalid alphaID:', ' alphaID=', alphaID, ' probe_ident=', p.Results.probe_ident]);
    end
  else
    error('Me thinks you made a little mistake in your alphaID...');
  end

  % step 2: convert alphaID to numID
  if length(just_alphaID)==1
    numID = double(just_alphaID(1)) - double('a') + 1;
  else
    if p.Results.pre_2008_BFDTD_version
      numID = 27*(double(just_alphaID(1)) - double('a') + 1) + (double(just_alphaID(2)) - double('a'));
    else
      numID = 26 * (double(just_alphaID(1)) - double('a') + 1) + (double(just_alphaID(2)) - double('a') + 1);
    end
  end
    
  ok = true;

end
