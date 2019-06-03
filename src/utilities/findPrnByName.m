function PrnFileNameList = findPrnByName(inputFileList,name,snap_time_number)

  if exist('snap_time_number','var')==0; snap_time_number = 0; end

  PrnFileNameList = {};
  [entries,FDTDobj] = GEO_INP_reader(inputFileList);
  for numID = 1:length(FDTDobj.probe_list)
    if strcmp(name, FDTDobj.probe_list(numID).name)
      snap_plane = 'p';
      probe_ident = FDTDobj.flag.id;
      [ filename, alphaID, pair ] = numID_to_alphaID(numID, snap_plane, probe_ident);
      num = sprintf('%03d',numID);
      filename = strcat({snap_plane}, num, {probe_ident}, '.prn');
      filename = char(filename);
      PrnFileNameList{end+1} = filename;
    end
  end
  for numID = 1:length(FDTDobj.frequency_snapshots)
    if strcmp(name, FDTDobj.frequency_snapshots(numID).name)
      snap_plane_list = {'x','y','z'};
      snap_plane = snap_plane_list{FDTDobj.frequency_snapshots(numID).plane};
      probe_ident = FDTDobj.flag.id;
      [ filename, alphaID, pair ] = numID_to_alphaID(numID, snap_plane, probe_ident, snap_time_number);
      %num = sprintf('%03d',numID);
      %filename = strcat({snap_plane}, num, {probe_ident}, '.prn');
      %filename = char(filename);
      PrnFileNameList{end+1} = filename;
    end
  end

end
