%  snap_time_number = 14
refractive_index_defect = 2.4
is_half_sim = false
numID_list = []
justCheck = false

the_list = {}

% for Jianwen's code
for snap_time_number = 0:6
  bibi = sprintf('%02d',snap_time_number);
  createEnergySnapshot('x52_id_01.prn', ['xaz_id_',bibi,'.prn'], ['energy_xaz_id_',bibi,'.prn'])
  createEnergySnapshot('y53_id_01.prn', ['yba_id_',bibi,'.prn'], ['energy_yba_id_',bibi,'.prn'])
  createEnergySnapshot('z25_id_01.prn', ['zy_id_',bibi,'.prn'], ['energy_zy_id_',bibi,'.prn'])
  createEnergySnapshot('z26_id_01.prn', ['zz_id_',bibi,'.prn'], ['energy_zz_id_',bibi,'.prn'])
  %[mode_volume_mum3, Foptn, Lambda_mum] = calculateModeVolume('.', '.', {'PhotonicCrystallineDiamond.inp'}, 'z', snap_time_number, refractive_index_defect, is_half_sim, numID_list, justCheck);
  %the_list{end+1} = [mode_volume_mum3, Foptn, Lambda_mum];
end

%% for old woodpile sims from paper
%for snap_time_number = 0:13
  %bibi = sprintf('%02d',snap_time_number);
  %createEnergySnapshot('x52_id_01.prn', ['xaz_id_',bibi,'.prn'], ['energy_xaz_id_',bibi,'.prn'])
  %createEnergySnapshot('y53_id_01.prn', ['yba_id_',bibi,'.prn'], ['energy_yba_id_',bibi,'.prn'])
  %createEnergySnapshot('z31_id_01.prn', ['zy_id_',bibi,'.prn'], ['energy_zy_id_',bibi,'.prn'])
  %%[mode_volume_mum3, Foptn, Lambda_mum] = calculateModeVolume('.', '.', {'PhotonicCrystallineDiamond.inp'}, 'z', snap_time_number, refractive_index_defect, is_half_sim, numID_list, justCheck);
  %%the_list{end+1} = [mode_volume_mum3, Foptn, Lambda_mum];
%end
