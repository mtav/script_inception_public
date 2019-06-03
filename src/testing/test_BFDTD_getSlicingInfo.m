close all;
clear all;

inpfile_list = {'sim.inp', 'sim.geo'};

DIRTEST='~/TEST/snapshot_counting';
cd(DIRTEST);
[inpEntries, structured_entries] = GEO_INP_reader(inpfile_list);
slicing_info = BFDTD_getSlicingInfo(structured_entries)

snap_type_list = {'xe','ye','ze',...
                  'xf','yf','zf',...
                  'xt','yt','zt'};
snap_type_list_input = {snap_type_list{:},...
                        'x','y','z',...
                        'e','f','t',...
                        'auto'};

for idx = 1:length(snap_type_list_input)
  snap_type = snap_type_list_input{idx}
  fprintf('================> snap_type = %s\n', snap_type);
  slicing_info = BFDTD_getSlicingInfo(structured_entries, 'snap_type', snap_type)
end

DIRTEST='~/TEST/mode_volume_validation/UniverseIsFullOfBalls/';
cd(fullfile(DIRTEST, 'X'));
[inpEntries, structured_entries] = GEO_INP_reader(inpfile_list);
slicing_info = BFDTD_getSlicingInfo(structured_entries)

cd(fullfile(DIRTEST, 'Y'));
[inpEntries, structured_entries] = GEO_INP_reader(inpfile_list);
slicing_info = BFDTD_getSlicingInfo(structured_entries)

cd(fullfile(DIRTEST, 'Z'));
[inpEntries, structured_entries] = GEO_INP_reader(inpfile_list);
slicing_info = BFDTD_getSlicingInfo(structured_entries)
