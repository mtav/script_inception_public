close all;
clear all;

MAINDIR=fullfile(getuserdir(), 'DATA/thesis_pillar_energy_snapshots');

SUBDIRS={'block_holes-non_tapered',
  'block_holes-tapered',
  'cylinder_holes-non_tapered',
  'cylinder_holes-tapered',
  'grated-non_tapered',
  'grated-tapered',
  'layered_circular-non_tapered',
  'layered_circular-tapered'};

SUBDIRS_TYPE = [1,
  1,
  1,
  1,
  1,
  1,
  2,
  3];

size_factor = 3;
SUBDIRS_Y2_SIZE = [size_factor*0.34,
  size_factor*0.34,
  size_factor*0.34,
  size_factor*0.34,
  size_factor*0.34,
  size_factor*0.34,
  size_factor*0.60,
  size_factor*0.65];

%FILES={'x_frequency.prn',
  %'x_epsilon.prn',
  %'x_energy.prn',
  %'y_frequency.prn',
  %'y_epsilon.prn',
  %'y_energy.prn',
  %'z_frequency.prn',
  %'z_epsilon.prn',
  %'z_energy.prn'};
  
snap_info_file = 'snapshot_overview.txt'
excitation_info_file = 'excitation_location.txt'
FILES = {snap_info_file, excitation_info_file};

createEnergySnapshot_mode = false;
plot_epsilon = true;
plot_E2 = true;
plot_energy = true;

test_mode = true;
if test_mode
  subdir_idx_list = 1:1;
else
  subdir_idx_list = 1:length(SUBDIRS);
end

for subdir_idx = subdir_idx_list

  % change dir
  cd(fullfile(MAINDIR, SUBDIRS{subdir_idx}));
  pwd
  
  % check file existence
  for file_idx = 1:length(FILES)
    if ~exist(FILES{file_idx}, 'file')
      pwd
      FILES{file_idx}
      error('FILE NOT FOUND');
    end
  end
  
  % read excitation info
  fid = fopen(excitation_info_file);
  if fid < 0
    pwd
    error('Failed to open file: %s', excitation_info_file)
  end
  excitation_location = textscan(fid, '%f %f %f');
  fclose(fid);
  excitation_location = [excitation_location{1}, excitation_location{2}, excitation_location{3}];
  
  % read snapshot info
  fid = fopen(snap_info_file);
  if fid < 0
    pwd
    error('Failed to open file: %s', snap_info_file)
  end
  snap_info = textscan(fid, '%s %s %s %s %s %s %f');
  fclose(fid);
  snap_fx = snap_info{1,1};
  snap_ex = snap_info{1,2};
  snap_fy = snap_info{1,3};
  snap_ey = snap_info{1,4};
  snap_fz = snap_info{1,5};
  snap_ez = snap_info{1,6};
  snap_freq = snap_info{1,7};
  
  %%% actually do stuff
  
  % process different modes
  Nfreqs = size(snap_freq, 1)
  if test_mode
    freq_idx_list = 1:1;
  else
    freq_idx_list = 1:Nfreqs;
  end
  for freq_idx = freq_idx_list;
    
    if createEnergySnapshot_mode
      thesis_createEnergySnapshots_function(snap_fx{freq_idx}, snap_ex{freq_idx}, snap_fy{freq_idx}, snap_ey{freq_idx}, snap_fz{freq_idx}, snap_ez{freq_idx});
    end
    
    if plot_energy
      column_to_plot = 3;
      
      colorbar_label = '\epsilon_r|E|^2';
      figure_basename = sprintf('energy_snapshots_freq-%f', snap_freq(freq_idx))
      log_norm_abs = false;
      [x_ret, y_ret, z_ret, params] = thesis_plotPillarSnapshots_function(snap_fx{freq_idx}, snap_ex{freq_idx}, snap_fy{freq_idx}, snap_ey{freq_idx}, snap_fz{freq_idx}, snap_ez{freq_idx}, excitation_location, snap_freq(freq_idx), SUBDIRS_TYPE(subdir_idx), SUBDIRS_Y2_SIZE(subdir_idx), test_mode, column_to_plot, colorbar_label, figure_basename, log_norm_abs);
      
      colorbar_label = 'log_{10}(\epsilon_r|E|^2/(\epsilon_{r}|E|)^2_{max})';
      figure_basename = sprintf('log_energy_snapshots_freq-%f', snap_freq(freq_idx))
      log_norm_abs = true;
      [x_ret, y_ret, z_ret, params, log_energy_min(subdir_idx), log_energy_max(subdir_idx)] = thesis_plotPillarSnapshots_function(snap_fx{freq_idx}, snap_ex{freq_idx}, snap_fy{freq_idx}, snap_ey{freq_idx}, snap_fz{freq_idx}, snap_ez{freq_idx}, excitation_location, snap_freq(freq_idx), SUBDIRS_TYPE(subdir_idx), SUBDIRS_Y2_SIZE(subdir_idx), test_mode, column_to_plot, colorbar_label, figure_basename, log_norm_abs);
    end
    
    if plot_E2
      column_to_plot = 5;
      
      colorbar_label = '|E|^2';
      figure_basename = sprintf('Emod2_snapshots_freq-%f', snap_freq(freq_idx))
      log_norm_abs = false;
      [x_ret, y_ret, z_ret, params] = thesis_plotPillarSnapshots_function(snap_fx{freq_idx}, snap_ex{freq_idx}, snap_fy{freq_idx}, snap_ey{freq_idx}, snap_fz{freq_idx}, snap_ez{freq_idx}, excitation_location, snap_freq(freq_idx), SUBDIRS_TYPE(subdir_idx), SUBDIRS_Y2_SIZE(subdir_idx), test_mode, column_to_plot, colorbar_label, figure_basename, log_norm_abs);
      
      colorbar_label = 'log_{10}(|E|^2/|E|^2_{max})';
      figure_basename = sprintf('log_Emod2_snapshots_freq-%f', snap_freq(freq_idx))
      log_norm_abs = true;
      [x_ret, y_ret, z_ret, params, log_Emod2_min(subdir_idx), log_Emod2_max(subdir_idx)] = thesis_plotPillarSnapshots_function(snap_fx{freq_idx}, snap_ex{freq_idx}, snap_fy{freq_idx}, snap_ey{freq_idx}, snap_fz{freq_idx}, snap_ez{freq_idx}, excitation_location, snap_freq(freq_idx), SUBDIRS_TYPE(subdir_idx), SUBDIRS_Y2_SIZE(subdir_idx), test_mode, column_to_plot, colorbar_label, figure_basename, log_norm_abs);
    end
    
  end

  if plot_epsilon
    % create epsilon snapshot pictures
    column_to_plot = 4;
    colorbar_label = '\epsilon_r';
    figure_basename = sprintf('epsilon_snapshots')
    freq_idx = 1;
    log_norm_abs = false;
    [x_ret, y_ret, z_ret, params] = thesis_plotPillarSnapshots_function(snap_fx{freq_idx}, snap_ex{freq_idx}, snap_fy{freq_idx}, snap_ey{freq_idx}, snap_fz{freq_idx}, snap_ez{freq_idx}, excitation_location, snap_freq(freq_idx), SUBDIRS_TYPE(subdir_idx), SUBDIRS_Y2_SIZE(subdir_idx), test_mode, column_to_plot, colorbar_label, figure_basename, log_norm_abs);
  end

end

%  cd(fullfile(MAINDIR, SUBDIR))
%  
%  x_energy = 'xa_id_01_energy.prn';
%  x_epsilon = 'x1_id_01.prn';
%  
%  y_energy = 'yb_id_01_energy.prn';
%  y_epsilon = 'y2_id_01.prn';
%  
%  z_energy = 'zc_id_01_energy.prn';
%  z_epsilon = 'z3_id_01.prn';

%  thesis_plotPillarSnapshots_function(x_energy, x_epsilon, y_energy, y_epsilon, z_energy, z_epsilon);

%SUBDIR1='DATA/taper_study_2015/DBR-circular-non-tapered/DBR-circular-non-tapered-d0.600/resonance_run_2016-07-21/'
%SUBDIR2='DATA/taper_study_2016/resonance_run_2016-07-26/'
%'block_holes_2012-03-24_hw@BC1/0.34/33_24/book0/resonance_run_2016-07-21/'
%'block_holes_2012-03-24_hw@BC1/0.34/33_24/no_taper_4/resonance_run_2016-07-21/'
%'cylinder_holes_2012-03-24_hw@BC2/0.34/33_24/book0/resonance_run_2016-07-21/'
%'cylinder_holes_2012-03-24_hw@BC2/0.34/33_24/no_taper_4/resonance_run_2016-07-21/'

%cd(fullfile(MAINDIR, SUBDIR))

%cd('block_holes_2012-03-24_hw@BC1/0.34/33_24/book0/resonance_run_2016-07-21/')
%x_energy = 'xaid01_energy.prn';
%x_epsilon = 'x4id01.prn';
%y_energy = 'ybid01_energy.prn';
%y_epsilon = 'y5id01.prn';
%z_energy = 'zcid01_energy.prn';
%z_epsilon = 'z6id01.prn';
%thesis_plotPillarSnapshots_function(x_energy, x_epsilon, y_energy, y_epsilon, z_energy, z_epsilon);

%  cd('block_holes_2012-03-24_hw@BC1/0.34/33_24/no_taper_4/resonance_run_2016-07-21/')
