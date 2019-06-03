cd('BristolFDTD/Woodpile/Woodpile_CubeDefect/CubeDefect_P1/high_index/ndefect_3.30.nlog_3.30.nout_1.00.a_0.34.w_0.21/defectType_0.Size_1.500.1.500.0.500/split-run');

file_list = {'./mesh-230x230x213/epsilon/part_0/woodpile.part_0.in',...
'./mesh-230x230x213/epsilon/part_1/woodpile.part_1.in',...
'./mesh-230x230x213/epsilon/part_2/woodpile.part_2.in',...
'./mesh-230x230x213/freq-456347499.31324595-start-5984-first-92384-repetition-86400/part_0/woodpile.part_0.in',...
'./mesh-230x230x213/freq-456347499.31324595-start-5984-first-92384-repetition-86400/part_1/woodpile.part_1.in',...
'./mesh-230x230x213/freq-456347499.31324595-start-5984-first-92384-repetition-86400/part_2/woodpile.part_2.in'}

% load data
ret = BFDTD_loadVolumetricData('mesh_file', file_list{1}, 'inpfile_list', file_list);

% compute additional data like Emod2 and EnergyDensity
ret = addModeVolumeData(ret);

% plot what you want
plotVolumetricData(ret.data.X, ret.data.Y, ret.data.Z, ret.data.EnergyDensity);
plotVolumetricData(ret.data.X, ret.data.Y, ret.data.Z, ret.data.EnergyDensity, 2.4);
plotVolumetricData(ret.data.X, ret.data.Y, ret.data.Z, ret.data.EnergyDensity, 2.4, 3, 5);
plotVolumetricData(ret.data.X, ret.data.Y, ret.data.Z, ret.data.EnergyDensity, 2, [], []);

% color axis scaling
caxis([0,1e8]);

% mode volume calculation
ret = calculateModeVolume2(ret);

% with defect:
ret = calculateModeVolume2(ret, 'geofile', './woodpile.geo');

% print mode volume info
printStructure(ret.MV.MV_MaximumEnergyDensity_nlocal)
printStructure(ret.MV.MV_MaximumEnergyDensity_nlocal_defect)
printStructure(ret.MV.MV_MaximumEmod2_nlocal)
printStructure(ret.MV.MV_MaximumEmod2_nlocal_defect)
