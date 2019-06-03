function [ filename, alphaID, pair ] = numID_to_alphaID_FrequencySnapshot(numID, varargin)
  % function [ filename, alphaID, pair ] = numID_to_alphaID_FrequencySnapshot(numID, varargin)
  %
  % Converts numeric IDs to alpha IDs used by Bristol FDTD.
  % IMPORTANT: Since BFDTD 2008 up to BFDTD 2013, "ba" comes after "az" instead of "a{". Please stop using the old BFDTD 2003.
  %
  % Usage:
  %  [ filename, alphaID, pair ] = numID_to_alphaID_FrequencySnapshot(numID)
  %  [ filename, alphaID, pair ] = numID_to_alphaID_FrequencySnapshot(numID, 'pre_2008_BFDTD_version', true)
  %  [ filename, alphaID, pair ] = numID_to_alphaID_FrequencySnapshot(numID, 'probe_ident', 'a')
  %  [ filename, alphaID, pair ] = numID_to_alphaID_FrequencySnapshot(numID, 'snap_plane', 'z')
  %  [ filename, alphaID, pair ] = numID_to_alphaID_FrequencySnapshot(numID, 'snap_time_number', 42)
  %  [ filename, alphaID, pair ] = numID_to_alphaID_FrequencySnapshot(numID, 'snap_time_number', 42, 'pre_2008_BFDTD_version', true, 'snap_plane', 'z', 'probe_ident', 'a')
  %
  % Arguments:
  %  Required:
  %   numID: numeric ID of the snapshot
  %  Parameter-value pairs:
  %   'pre_2008_BFDTD_version': true (version<2008) or false (version>=2008) (important if more than 52 snapshots are used!). The default is 'false'.
  %   'probe_ident': Default='_id_'
  %   'snap_plane': snapshot plane ('x','y' or 'z'). Default='x'
  %   'snap_time_number': "snap_time_number". Default=0
  %
  % examples:
  % 26 -> z
  % 26+26 -> az
  % 26+27 -> a{ for BFDTD 2003
  % 26+27 -> ba for BFDTD 2008 and 2013
  %
  % BFDTD 2003: a-z, aa-a{, ba-b{, ...
  % BFDTD 2008-2013: a-z, aa-az, ba-bz, ...
  %
  % MAXIMUM NUMBER OF SNAPSHOTS: 32767 (=(2^8)*(2^8)/2 -1)
  % MAXIMUM NUMBER OF SNAPSHOTS BEFORE RETURN to aa: 6938 = 26+256*27
  % MAXIMUM NUMBER OF SNAPSHOTS BEFORE DUPLICATE IDs: 4508 = 26+(6-(ord('a')-1)+256)*27+1 (6=character before non-printable bell character)
  % MAXIMUM NUMBER OF SNAPSHOTS BEFORE ENTERING DANGER AREA (non-printable characters): 836 = 26 + (ord('~')-ord('a')+1)*27 (BFDTD 2003)
  % MAXIMUM NUMBER OF SNAPSHOTS BEFORE ENTERING DANGER AREA (non-printable characters): 806 = 26 + (ord('~')-ord('a')+1)*26 (BFDTD 2008/2013)
  %
  % 126 = ord('~') = double('~')
  %
  % 1-26 : a-z
  % 27: {
  % 28: |
  % 29: }
  % 30: ~
  %
  % numID must be between 1 and 806 or else you will suffer death by monkeys!!!
  % snap_time_number must be between 0 and 99 or else you will suffer death by monkeys!!!

  %%%%%%%%
  %%% inputParser, the Matlab class supposed to make argparsing easier. Admire its complexity here! python argparse >> Matlab inputParser

  % Valid value lists, yes, because after validating once, we need to validate again to make sure we actually get valid values...
  snap_plane_list = {'x','y','z'};
  
  % create parser
  p = inputParser();
  p = inputParserWrapper(p, 'addRequired', 'numID', @(x) isnumeric(x) && 1<=x && x<=806);
  p = inputParserWrapper(p, 'addParamValue', 'snap_plane', 'x', @(x) any(validatestring(x, snap_plane_list)));
  p = inputParserWrapper(p, 'addParamValue', 'probe_ident', '_id_', @ischar);
  p = inputParserWrapper(p, 'addParamValue', 'snap_time_number', 0, @(x) isnumeric(x) && 0<=x && x<=99);
  p = inputParserWrapper(p, 'addParamValue', 'pre_2008_BFDTD_version', false, @islogical);
  
  
  % parse arguments
  p = inputParserWrapper(p, 'parse', numID, varargin{:});

  % second validatestring calls...
  snap_plane = validatestring(p.Results.snap_plane, snap_plane_list);
  %%%%%%%%

  % TODO: why use this inline function instead of simply floor(a/b) as used for ihi?
  function ret = div(A,B)
    ret = idivide(int32(A),int32(B));
  end

  %p.Results.snap_time_number = mod(p.Results.snap_time_number,100);
  ilo = mod(p.Results.snap_time_number, 10);
  ihi = floor(p.Results.snap_time_number/10);

  if p.Results.pre_2008_BFDTD_version
    % BristolFDTD 2003
    if numID < 27
      alphaID = char(numID + double('a')-1);
    else
      alphaID = strcat(char(div(numID, 27) + double('a') - 1), char(mod(numID, 27) + double('a')));
    end
  else
    % BristolFDTD 2008 and later versions (starts being different from older versions for numID >= 53)
    if numID < 27
      alphaID = char(numID + double('a')-1);
    else
      alphaID = strcat(char(div(numID-1, 26) + double('a') - 1), char(mod(numID-1, 26) + double('a')));
    end
  end

  filename = strcat({snap_plane}, alphaID, {p.Results.probe_ident}, char(ihi + double('0')), char(ilo + double('0')), '.prn');
  pair = [num2str(numID),':',alphaID];
  
  filename = char(filename);
end
