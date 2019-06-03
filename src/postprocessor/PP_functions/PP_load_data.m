function [ handles ] = PP_load_data(handles)
  disp('function [ handles ] = PP_load_data(handles)')
  % --- Executes on button press in pushbutton_load_data.
  % hObject    handle to pushbutton_load_data (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)

  % If this value remains 0 on return, nothing will be plotted.
  handles.isLoaded = 0;

  % Add .geo and .inp files to the handles object if possible.
  val = handles.geometryfile;
  if (1<=val) & (val<=length(handles.geolist))
    geofile = handles.geolist{val};
    handles.geofile = [handles.workdir, filesep, geofile];
  end

  val = handles.inputfile;
  if (1<=val) & (val<=length(handles.inplist))
    inpfile = handles.inplist{val};
    handles.inpfile = [handles.workdir, filesep, inpfile];
  end

  %%% type handling
  
  % handles.plotSnapshotType will be used by plotSnapshot(), while handles.Type is for use by the postprocessor GUI.
  % TODO: This is probably redundant, but until a better system is decided on, this hack will do the job.
  handles.plotSnapshotType = handles.Type;
  
  if handles.Type == 1
    val = handles.ProbeID;
    if (val<1) | (length(handles.ProbeList)<val)
      errordlg('Nothing to load.','Nothing to load.');
      return;
    end
    name = handles.ProbeList{val};
    handles.ProbeFile = [handles.workdir, filesep, name];
    handles.snapfile = handles.ProbeFile;
  elseif handles.Type == 2
    val = handles.TimeSnapshotID;
    if (val<1) | (length(handles.TimeSnapshotList)<val)
      errordlg('Nothing to load.','Nothing to load.');
      return;
    end
    name = handles.TimeSnapshotList{val};
    handles.TimeSnapshotFile = [handles.workdir, filesep, name];
    handles.snapfile = handles.TimeSnapshotFile;
  elseif handles.Type == 3
    val = handles.FrequencySnapshotID;
    if (val<1) | (length(handles.FrequencySnapshotList)<val)
      errordlg('Nothing to load.','Nothing to load.');
      return;
    end
    name = handles.FrequencySnapshotList{val};
    handles.FrequencySnapshotFile = [handles.workdir, filesep, name];
    handles.snapfile = handles.FrequencySnapshotFile;
  elseif handles.Type == 4
    val = handles.ExcitationTemplateID;
    if (val<1) | (length(handles.ExcitationTemplateList)<val)
      errordlg('Nothing to load.','Nothing to load.');
      return;
    end
    name = handles.ExcitationTemplateList{val};
    handles.ExcitationTemplateFile = [handles.workdir, filesep, name];
    handles.snapfile = handles.ExcitationTemplateFile;
  elseif handles.Type == 5 % any kind of snapshot.
    val = handles.SnapshotID;
    if (val<1) | (length(handles.SnapshotList)<val)
      errordlg('Nothing to load.','Nothing to load.');
      return;
    end
    name = handles.SnapshotList{val};
    handles.SnapshotFile = [handles.workdir, filesep, name];
    handles.snapfile = handles.SnapshotFile;    
  elseif handles.Type == 6
    val = handles.FrequencySnapshotID;
    if (val<1) | (length(handles.FrequencySnapshotList)<val)
      errordlg('Nothing to load.','Nothing to load.');
      return;
    end
    name = handles.FrequencySnapshotList{val};
    handles.FrequencySnapshotFile = [handles.workdir, filesep, name];
    handles.snapfile = handles.FrequencySnapshotFile;
  else
    errordlg('Unknown data type.', 'Unknown data type.');
    return;
  end

  %%% load snapshot data
  if handles.Type == 6 % if we want to plot an energy snapshot

    % TODO: Implement auto-epsilon-choice option and use the one from the popup list if given.
    % TODO: Option to only plot corresponding epsilon snapshot, to compare with the energy snapshot.
    % TODO: Energy snapshot title should provide names of both snapshots used.
    % TODO: And maybe they should be plotted next to each other, or with alpha overlay...
    % TODO: Actually, maybe each ".prn" type/popup should have its own "path-specification"? (ex: probe-path (resonance runs), epsilon-snapshot-path (epsilon run), frequency-snapshot-path (MV runs)), or search paths like PATH? recursive search with relative paths in the dropdown list? data files in a filesystem-like tree?

    % determine the probe identifier
    if isfield(handles, 'inpfile')
      [entries, FDTDobj] = GEO_INP_reader({handles.inpfile});
      probe_ident = FDTDobj.flag.id;
    else
      probe_ident = '_id_';
    end
    % load data
    try
      if handles.epsilon_only
        % NOTE: Disabling this for the moment, since when using the energy snapshot type, but plotting a material snapshot, we still get the position information in the title.
        % handles.plotSnapshotType = 2; % plot the snapshot as a TimeSnapshot
        [esnap, esnap_basename] = fsnap_to_esnap(handles.snapfile, 'probe_ident', probe_ident, 'pre_2008_BFDTD_version', handles.pre_2008_BFDTD_version, 'epsilon_dir', handles.epsilon_dir);
        [handles.header, handles.data] = readPrnFile(esnap);
      else
        [handles.header, handles.data, esnap, outfile] = createEnergySnapshot(handles.snapfile, '', handles.SaveEnergySnapshot, 'probe_ident', probe_ident, 'epsilon0_factor', handles.epsilon0_factor, 'pre_2008_BFDTD_version', handles.pre_2008_BFDTD_version, 'epsilon_dir', handles.epsilon_dir);
      end

    catch err
      uiwait(errordlg(err.message, err.identifier));
      return;
    end
    
  else
    % load data
    [handles.header, handles.data] = readPrnFile(handles.snapfile);
  end
  
  %%% determine orientation of snapshot
  % TODO: Use the maximums calculated here
  handles.dataSize = size(handles.data);
  columns = handles.header(:);
  if strcmp(columns(1),'y') && strcmp(columns(2),'z')
    handles.plane = 1;
    handles.maxy = handles.data(handles.dataSize(1),1);
    handles.maxz = handles.data(handles.dataSize(1),2);
  elseif strcmp(columns(1),'x') && strcmp(columns(2),'z')
    handles.plane = 2;
    handles.maxx = handles.data(handles.dataSize(1),1);
    handles.maxz = handles.data(handles.dataSize(1),2);
  elseif strcmp(columns(1),'#y') && strcmp(columns(2),'z')
    handles.plane = 1;
    handles.maxy = handles.data(handles.dataSize(1),1);
    handles.maxz = handles.data(handles.dataSize(1),2);
  elseif strcmp(columns(1),'#x') && strcmp(columns(2),'z')
    handles.plane = 2;
    handles.maxx = handles.data(handles.dataSize(1),1);
    handles.maxz = handles.data(handles.dataSize(1),2);
  else
    if size(handles.data, 2) >= 2
      handles.plane = 3;
      handles.maxx = handles.data(handles.dataSize(1),1);
      handles.maxy = handles.data(handles.dataSize(1),2);
    else
      errordlg(['Invalid snapshot file. Size of data seems to be: ', num2str(size(handles.data))], 'Invalid snapshot file.');
      return;
    end
  end
  
  handles.AllHeaders = columns; % all headers

  % allowing all columns to be plotted
  handles.HeadersForPopupList = char(columns(1:length(columns)));

  % if you want to exclude time/position columns...
  %if handles.Type == 1 % probe: first column is time
    %handles.HeadersForPopupList = char(columns(2:length(columns))); % all headers except the one/two first ones
  %else % assuming snapshots in all other cases, where first two columns give the position
    %handles.HeadersForPopupList = char(columns(3:length(columns))); % all headers except the one/two first ones
  %end
  
  handles.isLoaded = 1;
end
