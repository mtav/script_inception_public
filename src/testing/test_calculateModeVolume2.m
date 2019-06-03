%close all;
%filename = 'output/output.MV_convergence.csv';
%doSave = true;
%fig = MV_convergence_analysis_function2(filename, doSave);
%STOP

close all;
clear all;

WORKDIR='~/TEST/MV_LowIndexCavities/low_index/';
%WORKDIR='MV_LowIndexCavities/low_index/';

cd(WORKDIR);

if false
  ret_old = calculateModeVolume({'sim.in'}, 'logfile_bool', true);
  test_save_structure(ret_old, 'ret_old');
end

if true
  ret = BFDTD_loadVolumetricData('mesh_file', 'sim.in');
  
  %ret = calculateModeVolume2(ret, 'geofile', 'defect.geo', 'defect_name', 'BFDTD-Block-222');
  %ret = calculateModeVolume2(ret, 'geofile', 'defect.geo', 'defect_name', 'BFDTD-Block-333');
  %ret = calculateModeVolume2(ret, 'geofile', 'defect.geo', 'defect_name', 'BFDTD-Block-444');
  %ret = calculateModeVolume2(ret, 'geofile', 'defect.geo', 'defect_name', 'BFDTD-Block-555');
  %ret = calculateModeVolume2(ret, 'geofile', 'defect.geo', 'defect_name', 'BFDTD-Cylinder-222');
  %ret = calculateModeVolume2(ret, 'geofile', 'defect.geo', 'defect_name', 'BFDTD-Cylinder-333');
  %ret = calculateModeVolume2(ret, 'geofile', 'defect.geo', 'defect_name', 'BFDTD-Cylinder-444');
  %ret = calculateModeVolume2(ret, 'geofile', 'defect.geo', 'defect_name', 'BFDTD-Cylinder-555');
  %ret = calculateModeVolume2(ret, 'geofile', 'defect.geo', 'defect_name', 'BFDTD-Sphere-222', 'log', true);
  %ret = calculateModeVolume2(ret, 'geofile', 'defect.geo', 'defect_name', 'BFDTD-Sphere-333');
  %ret = calculateModeVolume2(ret, 'geofile', 'defect.geo', 'defect_name', 'BFDTD-Sphere-444');
  %ret = calculateModeVolume2(ret, 'geofile', 'defect.geo', 'defect_name', 'BFDTD-Sphere-555');
  %ret = calculateModeVolume2(ret, 'geofile', 'defect.geo', 'defect_name', 'BFDTD-Sphere-455');
  
  verbosity = 0;
  disp('---> start');
  ret = calculateModeVolume2(ret, 'verbosity', verbosity);
  ret = calculateModeVolume2(ret, 'verbosity', verbosity, 'log', true);
  ret = calculateModeVolume2(ret, 'verbosity', verbosity, 'log', 'defect-no.log');
  ret = calculateModeVolume2(ret, 'verbosity', verbosity, 'geofile', 'defect.geo', 'defect_name', 'test_defect_low', 'log', 'defect-low.log');
  ret = calculateModeVolume2(ret, 'verbosity', verbosity, 'geofile', 'defect.geo', 'defect_name', 'test_defect_high', 'log', 'defect-high.log');
  disp('---> end');
end

if false
  test_save_structure(ret, 'ret');
  test_save_structure(ret.info, 'ret.info');
  test_save_structure(ret.MV, 'ret.MV');
end

if false
  if inoctave()
    graphics_toolkit('qt');
  end
  defect_name = 'BFDTD-Sphere-222';
  doSavePlot = false;
  ret = MV_convergence_process('sim.in', {'sim.in'}, fullfile(WORKDIR, 'output', 'output'), 'N', 10, 'doLoop', true, 'doSavePlot', doSavePlot, 'geofile', 'defect.geo', 'defect_name', defect_name, 'linear_volume', false);
end
if true
  if inoctave()
    graphics_toolkit('qt');
  end
  
  calculateModeVolume_plotMaxDebug(ret.MV.info_full.MaximumEmod2, ret, 'ret.MV.info_full.MaximumEmod2');
  calculateModeVolume_plotMaxDebug(ret.MV.info_full.MaximumEnergyDensity, ret, 'ret.MV.info_full.MaximumEnergyDensity');
  calculateModeVolume_plotMaxDebug(ret.MV.info_defect.MaximumEmod2, ret, 'ret.MV.info_defect.MaximumEmod2');
  calculateModeVolume_plotMaxDebug(ret.MV.info_defect.MaximumEnergyDensity, ret, 'ret.MV.info_defect.MaximumEnergyDensity');
end

if false
  [h,d]=readPrnFile('output/output.MV_convergence.csv');
  figure; hold on;
  MV_convergence_plot_function_xy(h,d,'integration_box.idx', 'integration_box.alpha_radius', 'b+');
  MV_convergence_plot_function_xy(h,d,'integration_box.idx', 'integration_box.alpha_volume', 'ro');
  legend({'\alpha_{radius}', '\alpha_{volume}'});
end

if false
  fid = fopen('/tmp/test.log', 'w');
  fprintf(fid, '%s\n', printStructure(ret));
  fclose(fid);
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% TODO:
% -finish print() function for MV-calcs to display and log results
% -energy fraction calc
% -make MV_convergence_process work again
% -add number of pts option to MV_convergence_process
% -make things easy to use with GUI/wrapper
% -test on high-res sims
% -switch from linear volume to linear radius? (because first points are more interesting)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%figure;
%rows=4;
%cols=4;
%ret.MV.info_full.MaximumEmod2
%ret.MV.info_full.MaximumEnergyDensity
%ret.MV.info_defect.MaximumEmod2
%ret.MV.info_defect.MaximumEnergyDensity

%subplot(rows, cols, 1);
%title('Emod2-info_full');
%plotVolumetricData(ret.data.X, ret.data.Y, ret.data.Z, ret.data.EnergyDensity);
%view(2);

%figure;
%idx_mid = floor(size(ret.data.X)/2);
%plot(ret.data.X(idx_mid(1),:,idx_mid(3)), ret.data.EnergyDensity(idx_mid(1),:,idx_mid(3)));
%vline(1.5:0.5:5.5);

%figure;
%idx_mid = ceil(size(ret.data.X)/2);
%plot(ret.data.X(idx_mid(1),:,idx_mid(3)), ret.data.EnergyDensity(idx_mid(1),:,idx_mid(3)));
%vline(1.5:0.5:5.5);

%figure;
%plotVolumetricData(ret.data.X, ret.data.Y, ret.data.Z, ret.data.defect_mask, [], [], [], 'isosurface');
%view(2);

%m = ret.MV.info_defect.MaximumEmod2;
%figure;
%subplot(1,2,1);
%plotVolumetricData(ret.data.X, ret.data.Y, ret.data.Z, ret.data.Emod2, m.x, m.y, m.z);
%xlabel('x');ylabel('y');zlabel('z'); title('Emod2');
%caxis([0, m.Emod2]);
%view(2);
%hold on;
%plotVolumetricData(ret.data.X, ret.data.Y, ret.data.Z, ret.data.defect_mask, [], [], [], 'isosurface');
%xlabel('x');ylabel('y');zlabel('z');

%subplot(1,2,2);
%plotVolumetricData(ret.data.X, ret.data.Y, ret.data.Z, ret.data.EnergyDensity, m.x, m.y, m.z);
%xlabel('x');ylabel('y');zlabel('z'); title('EnergyDensity');
%caxis([0, m.EnergyDensity]);
%view(2);
%hold on;
%plotVolumetricData(ret.data.X, ret.data.Y, ret.data.Z, ret.data.defect_mask, [], [], [], 'isosurface');

%m = ret.MV.info_defect.MaximumEnergyDensity;
%figure;
%subplot(1,2,1);
%plotVolumetricData(ret.data.X, ret.data.Y, ret.data.Z, ret.data.Emod2, m.x, m.y, m.z);
%xlabel('x');ylabel('y');zlabel('z'); title('Emod2');
%caxis([0, m.Emod2]);
%view(2);
%hold on;
%plotVolumetricData(ret.data.X, ret.data.Y, ret.data.Z, ret.data.defect_mask, [], [], [], 'isosurface');
%xlabel('x');ylabel('y');zlabel('z');

%subplot(1,2,2);
%plotVolumetricData(ret.data.X, ret.data.Y, ret.data.Z, ret.data.EnergyDensity, m.x, m.y, m.z);
%xlabel('x');ylabel('y');zlabel('z'); title('EnergyDensity');
%caxis([0, m.EnergyDensity]);
%view(2);
%hold on;
%plotVolumetricData(ret.data.X, ret.data.Y, ret.data.Z, ret.data.defect_mask, [], [], [], 'isosurface');

%clear all;
%a=struct();
%a.x=@(x) max([1,2,3,x]);
%save('a.struct', 'a')
%b=a;
%b.x=NaN;
%save('b.struct', 'b')
