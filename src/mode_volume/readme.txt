MV calculations:
================
Old style calculation looping over snapshots:
	ret = calculateModeVolume(inpfile_list, varargin)
New style calculation, where all data is loaded first and then processed:
	ret = BFDTD_loadVolumetricData(varargin)
	ret = calculateModeVolume2(ret, varargin)

1D+3D plots of data:
=====================
	fig = calculateModeVolume_plotMaxDebug(max_info, ret, title_base, varargin)

Example:
========
>> cd DATA/16052016/n_3.6/0.100ax1_0.100ax6_2_0.300ax6_n_def_1.00/0.100ax1_0.100ax6_n_def_1.00/Ez/resonance-run/mesh-268x250x298

>> file_list = {'./epsilon/part_0/sim.part_0.inp',...
'./epsilon/part_1/sim.part_1.inp',...
'./epsilon/part_2/sim.part_2.inp',...
'./epsilon/part_3/sim.part_3.inp',...
'./epsilon/part_4/sim.part_4.inp',...
'./freq-171544600.0-start-2627-first-89027-repetition-86400/part_0/sim.part_0.inp',...
'./freq-171544600.0-start-2627-first-89027-repetition-86400/part_1/sim.part_1.inp',...
'./freq-171544600.0-start-2627-first-89027-repetition-86400/part_2/sim.part_2.inp',...
'./freq-171544600.0-start-2627-first-89027-repetition-86400/part_3/sim.part_3.inp',...
'./freq-171544600.0-start-2627-first-89027-repetition-86400/part_4/sim.part_4.inp'};

>> ret = BFDTD_loadVolumetricData('inpfile_list', file_list, 'mesh_file', 'sim.mesh.inp');

>> ret = calculateModeVolume2(ret);

>> max_info=ret.MV.info_full.MaximumEnergyDensity;

>> fig = calculateModeVolume_plotMaxDebug(max_info, ret, 'title_base');
