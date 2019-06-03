function [snap_time_number_fsnap_max_overall, snap_time_number_fsnap_info] = getLastSnapTimeNumberOverall(inpfile_list, varargin)
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %%%%% create parser
  p = inputParser();
  p = inputParserWrapper(p, 'addRequired', 'inpfile_list', @iscellstr);
  p = inputParserWrapper(p, 'addParamValue', 'pre_2008_BFDTD_version', false, @islogical);
  p = inputParserWrapper(p, 'parse', inpfile_list, varargin{:});
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  
  snap_time_number_fsnap_max_overall = NaN; % largest snap_time_number_fsnap common to all frequency snapshots
  snap_time_number_fsnap_info = struct(); % detailed info structure
  snap_time_number_fsnap_info.inpfile_list = {};
  snap_time_number_fsnap_info.snap_time_number_common = [];
  
  origdir = pwd();
  
  first_inp_with_fsnaps = true;
  snap_time_number_fsnap_info.total_frequency_snapshots = 0;
  
  % loop through .inp files
  for inpfile_idx = 1:numel(inpfile_list)
    
    inpfile = inpfile_list{inpfile_idx};
    %fprintf('Processing file %d/%d: inpfile = %s\n', inpfile_idx, numel(inpfile_list), inpfile);
    
    % ugly directory handling (and fullfile is not smart in concatenating with absolute paths...)
    cd(origdir);
    cd(dirname(inpfile));
    fsnap_folder = pwd();
    %[inpEntries, structured_entries] = GEO_INP_reader({basename(inpfile)});
    [ structured_entries, inpEntries ] = readBristolFDTD({basename(inpfile)});
    
    inpfile_info = struct();
    inpfile_info.name = inpfile;
    inpfile_info.fsnap_list = {};
    inpfile_info.snap_time_number_common = [];
    
    snap_time_number_fsnap_info.total_frequency_snapshots = snap_time_number_fsnap_info.total_frequency_snapshots + numel(structured_entries.frequency_snapshots);
    
    % loop through all frequency snapshots
    for numID = 1:numel(structured_entries.frequency_snapshots)
      
      fsnap_info = struct();
      
      snapshot = structured_entries.frequency_snapshots(numID);
      
      [ fsnap_filename, fsnap_alphaID, fsnap_pair ] = numID_to_alphaID_FrequencySnapshot(numID, 'snap_plane', snapshot.plane_letter, 'probe_ident', structured_entries.flag.id, 'snap_time_number', 0, 'pre_2008_BFDTD_version', p.Results.pre_2008_BFDTD_version);
      prefix = [snapshot.plane_letter, fsnap_alphaID, structured_entries.flag.id];
      [snap_time_number_max, snap_time_number_list] = getLastSnapTimeNumber(fsnap_folder, prefix, 'probe_ident', structured_entries.flag.id, 'pre_2008_BFDTD_version', p.Results.pre_2008_BFDTD_version);
      if isempty(snap_time_number_list)
        fprintf('numID = %d\n', numID);
        error('getLastSnapTimeNumberOverall: Failed to find .prn files:\n pwd=%s,\n fsnap_folder=%s,\n prefix=%s,\n flag.id=%s,\n pre_2008_BFDTD_version=%d\n', pwd(), fsnap_folder, prefix, structured_entries.flag.id, p.Results.pre_2008_BFDTD_version);
      end
      
      fsnap_info.prefix = prefix;
      fsnap_info.snap_time_number_list = snap_time_number_list;
      inpfile_info.fsnap_list{numID} = fsnap_info;
      
      if numID == 1
        inpfile_info.snap_time_number_common = snap_time_number_list;
      else
        inpfile_info.snap_time_number_common = intersect(inpfile_info.snap_time_number_common, snap_time_number_list);
      end
      
    end
    
    snap_time_number_fsnap_info.inpfile_list{inpfile_idx} = inpfile_info;
  
    % only do intersections for .inp files containing frequency snapshots
    if numel(structured_entries.frequency_snapshots) > 0
      if first_inp_with_fsnaps
        snap_time_number_fsnap_info.snap_time_number_common = inpfile_info.snap_time_number_common;
        first_inp_with_fsnaps = false;
      else
        snap_time_number_fsnap_info.snap_time_number_common = intersect(snap_time_number_fsnap_info.snap_time_number_common, inpfile_info.snap_time_number_common);
      end
    end
  
    snap_time_number_fsnap_max_overall = max(snap_time_number_fsnap_info.snap_time_number_common(:));
  
  end
  
  %return
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %% get latest snap_time_number_fsnap
  %ret.snap_time_number_fsnap = NaN;
  %frequency_list = [];
  
  %numID_list = p.Results.numID_list;
  %if isempty(numID_list)
    %numID_list = 1:numel(structured_entries.frequency_snapshots);
  %end
  
  %% loop through all frequency snapshots
  %for numID = numID_list
    %snapshot = structured_entries.frequency_snapshots(numID);
    %frequency_list(end+1) = snapshot.frequency;
    
    %[ fsnap_filename, fsnap_alphaID, fsnap_pair ] = numID_to_alphaID_FrequencySnapshot(numID, 'snap_plane', snapshot.plane_letter, 'probe_ident', structured_entries.flag.id, 'snap_time_number', 0, 'pre_2008_BFDTD_version', p.Results.pre_2008_BFDTD_version);
    %prefix = [snapshot.plane_letter, fsnap_alphaID, structured_entries.flag.id];
    %ret.snap_time_number_fsnap = getLastSnapTimeNumber(p.Results.fsnap_folder, prefix, 'probe_ident', structured_entries.flag.id, 'pre_2008_BFDTD_version', p.Results.pre_2008_BFDTD_version);
    %if ret.snap_time_number_fsnap < 0
      %error(['Failed to automatically determine snap_time_number_fsnap, most likely due to missing .prn files in fsnap_folder = "', p.Results.fsnap_folder, '"']);
    %end
  %end
  
    %slicingInfo = BFDTD_getSlicingInfo(structured_entries, 'pre_2008_BFDTD_version', p.Results.pre_2008_BFDTD_version, 'fsnap_folder', dirname(inpfile))
    
    %if ~isnan(slicingInfo.snap_time_number_fsnap)
    %end
    %if slicingInfo.snap_time_number_fsnap > 1
    %end
  
  %% additional automatic info extraction (TODO: move into external function that can be shared with old calcMV script and reused by other tools)
  %ret.info.fsnap_folder = p.Results.fsnap_folder;
  %if isempty(ret.info.fsnap_folder)
    %ret.info.fsnap_folder = dirname(mesh_file);
  %end
  
  %% if snap_time_number_fsnap has not been specified, we try to use the biggest working one.
  %snap_time_number_fsnap = p.Results.snap_time_number_fsnap;
  %if isnan(snap_time_number_fsnap)
    %[ fsnap_filename, fsnap_alphaID, fsnap_pair ] = numID_to_alphaID_FrequencySnapshot(numID_fsnap, 'snap_plane', p.Results.snap_plane, 'probe_ident', probe_ident, 'snap_time_number', 0, 'pre_2008_BFDTD_version', p.Results.pre_2008_BFDTD_version);
    %prefix = [p.Results.snap_plane, fsnap_alphaID, probe_ident];
    %snap_time_number_fsnap = getLastSnapTimeNumber(ret.info.fsnap_folder, prefix, 'probe_ident', probe_ident, 'pre_2008_BFDTD_version', p.Results.pre_2008_BFDTD_version);
    %if snap_time_number_fsnap < 0
      %error(['Failed to automatically determine snap_time_number_fsnap, most likely due to missing .prn files in fsnap_folder = "', ret.info.fsnap_folder, '"']);
    %end
  %end
  
  %ret.info.slicingInfo = BFDTD_getSlicingInfo();
  
  %p = inputParserWrapper(p, 'addRequired', 'structured_entries', @isstruct);
  %p = inputParserWrapper(p, 'addParamValue', 'snap_type', 'auto', @(x) any(validatestring(x, snap_type_list_input)));
  %p = inputParserWrapper(p, 'addParamValue', 'pre_2008_BFDTD_version', false, @islogical);
  %p = inputParserWrapper(p, 'addParamValue', 'fsnap_folder', '.', @ischar);
  %p = inputParserWrapper(p, 'addParamValue', 'numID_list', [], @isnumeric);
  
end
