close all;
clear all;

%cd('~/TEST/UniverseIsFullOfBalls/v2/Z/');

%ret = BFDTD_loadVolumetricData('mesh_file', 'sim.in');

%ret = calculateModeVolume2(ret);

cd('~/TEST/MV_LowIndexCavities/low_index');

ret = BFDTD_loadVolumetricData('mesh_file', 'sim.in');

ret = calculateModeVolume2(ret);

ret = calculateModeVolume2(ret, 'geofile', 'defect.geo', 'defect_name', 'test_defect_centre');

figure;
plotVolumetricData(ret.data.X, ret.data.Y, ret.data.Z, ret.data.D(:,:,:,1));
figure;
plotVolumetricData(ret.data.X, ret.data.Y, ret.data.Z, ret.data.EnergyDensity);
