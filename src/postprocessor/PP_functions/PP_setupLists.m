function [handles, ok] = PP_setupLists(handles)
  % Sets up the handles fields containing the lists of BFDTD input/output files, used for the dropdown lists in the postprocessor GUI.
  % ok=1 : successful run of all commands
  % ok=0 : failed to categorize at least one data file (.prn/.dat/.int files)
  
  % TODO: Move this into a generic utility function, so it can be used by other stuff more easily.
  
  disp('function [handles, ok] = PP_setupLists(handles)')

  handles.data_files = {};
  handles.ProbeList = {};
  handles.TimeSnapshotList = {};
  handles.FrequencySnapshotList = {};
  handles.ExcitationTemplateList = {};
  handles.SnapshotList = {};
  handles.geolist = {};
  handles.inplist = {};

  data_files = [dir(fullfile(handles.workdir,'*.prn')); dir(fullfile(handles.workdir,'*.dat')); dir(fullfile(handles.workdir,'*.int'))];
  handles.data_files = {data_files.name};
  handles.data_files = handles.data_files';
  for idx=1:length(handles.data_files)
    unknown = 1;
    if ~isempty(regexp(handles.data_files{idx},'^p.*\.(prn|dat)$','ignorecase'))
      handles.ProbeList{end+1} = handles.data_files{idx};
      unknown = 0;
    end
    if ~isempty(regexp(handles.data_files{idx},'^[xyz]\d+.*\d\d\.(prn|dat)$','ignorecase'))
      handles.TimeSnapshotList{end+1} = handles.data_files{idx};
      unknown = 0;
    end
    if ~isempty(regexp(handles.data_files{idx},'^[xyz][a-z{|}~][a-z{]?.*\d\d\.(prn|dat)$','ignorecase'))
      handles.FrequencySnapshotList{end+1} = handles.data_files{idx};
      unknown = 0;
    end
    if ~isempty(regexp(handles.data_files{idx},'^.*\.(int|dat)$','ignorecase'))
      handles.ExcitationTemplateList{end+1} = handles.data_files{idx};
      unknown = 0;
    end
    if ~isempty(regexp(handles.data_files{idx},'^.*\.(prn|dat|int)$','ignorecase'))
      handles.SnapshotList{end+1} = handles.data_files{idx};
      unknown = 0;
    end
    if unknown & isempty(regexp(handles.data_files{idx},'^ref\.(prn|dat)$','ignorecase'))
      warning(['unknown data : ', handles.data_files{idx}])
      ok = 0;
      return
    end
  end
 
  disp([ 'length(handles.data_files)=', num2str(length(handles.data_files)) ])
  disp([ 'length(handles.ProbeList)=', num2str(length(handles.ProbeList)) ])
  disp([ 'length(handles.TimeSnapshotList)=', num2str(length(handles.TimeSnapshotList)) ])
  disp([ 'length(handles.FrequencySnapshotList)=', num2str(length(handles.FrequencySnapshotList)) ])
  disp([ 'length(handles.ExcitationTemplateList)=', num2str(length(handles.ExcitationTemplateList)) ])
  total = length(handles.ProbeList) + length(handles.TimeSnapshotList) + length(handles.FrequencySnapshotList) + length(handles.ExcitationTemplateList) + 1;
  disp(['total = ',num2str(total)])

  %prn_files = [dir(fullfile(handles.workdir,'*.prn')); dir(fullfile(handles.workdir,'*.dat'))];
  %handles.snaplist = {prn_files.name}; handles.snaplist = handles.snaplist';
  %prn_files = char(prn_files.name);
  
  geo_files = dir(fullfile(handles.workdir,'*.geo'));
  handles.geolist = {geo_files.name}; handles.geolist = handles.geolist';
  %geo_files = char(geo_files.name);
  
  inp_files = dir(fullfile(handles.workdir,'*.inp'));
  handles.inplist = {inp_files.name}; handles.inplist = handles.inplist';
  %inp_files = char(inp_files.name);

  %prn_files
  %disp(['prn_files=',prn_files(:)']);
  % if(prn_files=='')
  %     disp('no .prn files found');
  % end

  %if length(prn_files)>0
    %set(handles.popupmenu_inputsnapshot,'String',prn_files);
  %end
  %if length(geo_files)>0
    %set(handles.popupmenu_geometryfile,'String',geo_files);
  %end
  %if length(inp_files)>0
    %set(handles.popupmenu_inputfile,'String',inp_files);
  %end

  clear data_files geo_files inp_files;
  
  %handles.snaplist
  ok = 1;
end
