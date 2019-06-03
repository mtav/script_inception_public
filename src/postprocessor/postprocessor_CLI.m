function postprocessor_CLI()
  disp('function postprocessor_CLI()')
  handles = struct;
  handles.isLoaded = 0;
  handles.workdir = pwd();
  handles.snaplist = {};
  handles.geolist = {};
  handles.inplist = {};

  % browse
  [handles, dirChosen] = PP_browse(handles);
  if ~dirChosen
    return
  end

  handles.Type = 2;
  handles.ProbeID = 1;
  handles.TimeSnapshotID = 1;
  handles.FrequencySnapshotID = 1;
  handles.ExcitationTemplateID = 1;
  handles.SnapshotID = 1;
  handles.geometryfile = 1;
  handles.inputfile = 1;
  
  [handles, ok] = PP_setupLists(handles);
  
  % load data
  [ handles ] = PP_load_data(handles);
  if ~handles.isLoaded
    return
  end
  
  handles.col = 3;
  handles.minplotvalue = NaN;
  handles.maxplotvalue = NaN;

  handles.interpolate = 0;
  handles.autosave= 0;
  handles.geometry= 1;
  handles.modulus = 0;

  handles.colour = 1;
  handles.surface = 1;

  % generate plot
  [ handles, ok ] = PP_generate_plot(handles);
end
