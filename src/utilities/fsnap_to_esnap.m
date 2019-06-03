function [esnap, esnap_basename] = fsnap_to_esnap(fsnap, varargin)
  % function esnap = fsnap_to_esnap(fsnap, varargin)
  %
  % Gives the filename of the epsilon snapshot corresponding to a given frequency snapshot. (Assuming that your simulations have one epsilon snapshot for each frequency snapshot, with the same position/size parameters.)
  %
  % Return values:
  %  esnap: full path to the epsilon snapshot (ex: '/a/b/c/x26_id_01.prn')
  %  esnap_basename: basename of the epsilon snapshot (ex: 'x26_id_01.prn')
  %
  % Usage:
  %  [esnap, esnap_basename] = fsnap_to_esnap('xhh_id_52.prn')
  %  [esnap, esnap_basename] = fsnap_to_esnap('xhh_LOL_52.prn', 'probe_ident', '_LOL_')
  %  [esnap, esnap_basename] = fsnap_to_esnap('xhh_id_52.prn', 'pre_2008_BFDTD_version', false)
  %  [esnap, esnap_basename] = fsnap_to_esnap('xhh_id_52.prn', 'epsilon_dir','../../epsilon')
  %  [esnap, esnap_basename] = fsnap_to_esnap('xhh_LOL_52.prn', 'probe_ident', '_LOL_' ,'pre_2008_BFDTD_version', false,'epsilon_dir','../../epsilon')
  %
  % Arguments:
  %   Required:
  %     fsnap: path to frequency snapshot
  %  Parameter-value pairs:
  %    'pre_2008_BFDTD_version': Default=false
  %    'probe_ident': Default='_id_'.
  %    'epsilon_dir': Directory containing the epsilon snapshot. If it is an empty string, the epsilon snapshots will be searched for in the directory containing fsnap. Default=''.

  %%%%%%%%
  %%% arg processing
  % create parser
  p = inputParser();
  p = inputParserWrapper(p, 'addRequired', 'fsnap', @ischar);
  p = inputParserWrapper(p, 'addParamValue', 'pre_2008_BFDTD_version', false, @islogical);
  p = inputParserWrapper(p, 'addParamValue', 'probe_ident', '_id_', @ischar);
  p = inputParserWrapper(p, 'addParamValue', 'epsilon_dir', '', @ischar);
  
  % parse arguments
  p = inputParserWrapper(p, 'parse', fsnap, varargin{:});
  %%%%%%%%
  
  %%% actual function body
  [ numID, snap_plane, snap_time_number, ok ] = alphaID_to_numID(p.Results.fsnap, 'probe_ident', p.Results.probe_ident, 'pre_2008_BFDTD_version', p.Results.pre_2008_BFDTD_version);
  if ~ok
    error('Could not determine epsilon snapshot corresponding to given frequency snapshot. Please specify it manually.');
  end
  [ esnap_basename, alphaID, pair ] = numID_to_alphaID_TimeSnapshot(numID, snap_plane, p.Results.probe_ident, 1);
  
  if isempty(p.Results.epsilon_dir)
    esnap = fullfile( dirname(fsnap), esnap_basename );
  else
    esnap = fullfile( p.Results.epsilon_dir, esnap_basename );
  end
end
