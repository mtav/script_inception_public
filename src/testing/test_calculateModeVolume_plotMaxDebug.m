ret = BFDTD_loadVolumetricData();
ret = calculateModeVolume2(ret);
max_info=ret.MV.info_full.MaximumEnergyDensity;
fig = calculateModeVolume_plotMaxDebug(max_info, ret, 'title_base');
