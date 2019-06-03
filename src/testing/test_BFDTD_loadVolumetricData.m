close all;
clear all;

inpfile_list = {'sim.inp', 'sim.geo'};

% TODO: auto-detect snap plane in old calcMV script...

%TESTDATA=fullfile(getuserdir(), 'TEST','MV_LowIndexCavities','low_index'); snap_plane='z';
%TESTDATA='~/TEST/MV_LowIndexCavities/low_index/'; snap_plane='z';
TESTDATA='/tmp/UniverseIsFullOfBalls/X'; snap_plane='x';
%TESTDATA='/tmp/UniverseIsFullOfBalls/Y'; snap_plane='y';
%TESTDATA='/tmp/UniverseIsFullOfBalls/Z'; snap_plane='z';

%TESTDATA='~/TEST/UniverseIsFullOfBalls/v2/X'; snap_plane='x';
%TESTDATA='~/TEST/UniverseIsFullOfBalls/v2/Y'; snap_plane='y';
%TESTDATA='~/TEST/UniverseIsFullOfBalls/v2/Z'; snap_plane='z';

cd(TESTDATA);

ret_orig = calculateModeVolume(inpfile_list, 'snap_plane', snap_plane);

%[inpEntries, structured_entries] = GEO_INP_reader(inpfile_list);

%slicing_info = BFDTD_getSlicingInfo(structured_entries)
%slicing_info = BFDTD_getSlicingInfo(structured_entries, 'SnapshotType', p.Results.SnapshotType)

columns = {'x', 'y', 'z', 'material', 'Exmod', 'Eymod', 'Ezmod', 'Hxmod', 'Hymod', 'Hzmod'};
ret_new = BFDTD_loadVolumetricData('mesh_file', inpfile_list{1}, 'inpfile_list', inpfile_list, 'columns', columns);
ret_new = calculateModeVolume2(ret_new);

Xc = mean(getRange(ret_new.data.X));
Yc = mean(getRange(ret_new.data.Y));
Zc = mean(getRange(ret_new.data.Z));

figure;
for idx=1:numel(ret_new.data.header)
  subplot(2,5,idx);
  plotVolumetricData(ret_new.data.X, ret_new.data.Y, ret_new.data.Z, squeeze(ret_new.data.D(:,:,:,idx)), [Xc],[Yc],[Zc]);
  title(ret_new.data.header{idx});
end

figure;
subplot(1,3,1);
plotVolumetricData(ret_new.data.X, ret_new.data.Y, ret_new.data.Z, ret_new.data.D(:,:,:,1), [Xc],[Yc],[Zc]);
title('material');
subplot(1,3,2);
plotVolumetricData(ret_new.data.X, ret_new.data.Y, ret_new.data.Z, ret_new.data.Emod2, [Xc],[Yc],[Zc]);
title('Emod^2');
subplot(1,3,3);
plotVolumetricData(ret_new.data.X, ret_new.data.Y, ret_new.data.Z, ret_new.data.EnergyDensity, [Xc],[Yc],[Zc]);
title('energy density');

% comparison:
dMV = 100*(ret_new.MV.MV_MaximumEnergyDensity_nlocal.mode_volume_mum3 - ret_orig.MV_MaximumEnergyDensity_nlocal.mode_volume_mum3)/ret_orig.MV_MaximumEnergyDensity_nlocal.mode_volume_mum3
dTotalEnergy = 100*(ret_new.MV.MV_MaximumEnergyDensity_nlocal.TotalEnergy - ret_orig.TotalEnergy)/ret_orig.TotalEnergy
dMaxEnergyDensity = 100*(ret_new.MV.MV_MaximumEnergyDensity_nlocal.MaximumEnergyDensity - ret_orig.MaximumEnergyDensity.value)/ret_orig.MaximumEnergyDensity.value
dVolume = 100*(ret_new.MV.info_full.TotalVolume_AvailableData - ret_orig.TotalVolume)/ret_orig.TotalVolume

MV_orig = ret_orig.MV_MaximumEnergyDensity_nlocal.mode_volume_mum3
MV_new = ret_new.MV.MV_MaximumEnergyDensity_nlocal.mode_volume_mum3

disp('SUCCESS');

%% slice filling tests:
%Ny=2;
%Nx=3;
%Nz=4;
%Nd=5;

%% x
%x = zeros([Ny, Nx, Nz, Nd]);
%x(:,1,:,1) = reshape(1:(Ny*Nz), Ny, Nz);
%%x(:,1,:,1) = reshape(1:(Ny*Nz), Nz, Ny); % fails

%% y
%y = zeros([Ny,Nx,Nz,Nd]);
%y(1,:,:,1) = reshape(1:(Nx*Nz), Nx, Nz);
%%y(1,:,:,1) = reshape(1:(Nx*Nz), Nz, Nx); % fails

%% z
%z = zeros([Ny,Nx,Nz,Nd]);
%z(:,:,1,1) = reshape(1:(Ny*Nx), Ny, Nx);
%%z(:,:,1,1) = reshape(1:(Ny*Nx), Nx, Ny); % fails

%vi = [(column_1_esnap(2) - column_1_esnap(1))/2; (column_1_esnap(3:end) - column_1_esnap(1:end-2))/2; (column_1_esnap(end) - column_1_esnap(end-1))/2];
%vj = [(column_2_esnap(2) - column_2_esnap(1))/2; (column_2_esnap(3:end) - column_2_esnap(1:end-2))/2; (column_2_esnap(end) - column_2_esnap(end-1))/2];
