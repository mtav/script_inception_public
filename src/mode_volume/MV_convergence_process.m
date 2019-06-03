function ret_new = MV_convergence_process(mesh_file, inpfile_list, outfile_basename, varargin)
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %%%%% create parser
  p = inputParser();
  p = inputParserWrapper(p, 'addRequired', 'mesh_file', @ischar);
  p = inputParserWrapper(p, 'addRequired', 'inpfile_list', @iscellstr);
  
  %p = inputParserWrapper(p, 'addRequired', 'fsnap_file', @ischar);
  %p = inputParserWrapper(p, 'addRequired', 'eps_file', @ischar);
  
  p = inputParserWrapper(p, 'addRequired', 'outfile_basename', @ischar);
  
  p = inputParserWrapper(p, 'addParamValue', 'N', 100, @isnumeric); % number of integration boxes to use
  p = inputParserWrapper(p, 'addParamValue', 'linear_volume', false, @islogical); % Increase integration volume linearly. If false, the radius is increased linearly.
  
  p = inputParserWrapper(p, 'addParamValue', 'refractive_index_defect', NaN, @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'DataSizeMax', 200e6, @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'numID_list', [], @(x) isnumeric(x) || iscell(x));
  p = inputParserWrapper(p, 'addParamValue', 'pre_2008_BFDTD_version', false, @islogical);
  p = inputParserWrapper(p, 'addParamValue', 'justCheck', false, @islogical);
  
  p = inputParserWrapper(p, 'addParamValue', 'snap_time_number_fsnap', NaN, @isnumeric); % if not given, it will be automatically determined
  
  p = inputParserWrapper(p, 'addParamValue', 'doSaveCSV', true, @islogical);
  p = inputParserWrapper(p, 'addParamValue', 'doPlot', true, @islogical);
  p = inputParserWrapper(p, 'addParamValue', 'doSavePlot', true, @islogical);
  p = inputParserWrapper(p, 'addParamValue', 'doSaveFinalLog', true, @islogical);
  
  p = inputParserWrapper(p, 'addParamValue', 'doLoop', true, @islogical);
  
  % defect infos
  p = inputParserWrapper(p, 'addParamValue', 'geofile', '', @ischar);
  p = inputParserWrapper(p, 'addParamValue', 'defect_name', 'defect', @ischar);
  
  p = inputParserWrapper(p, 'parse', mesh_file, inpfile_list, outfile_basename, varargin{:});
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  
  fprintf('=========> Processing %s \n', basename(outfile_basename));
  close all;
  
  % quick existence tests to save time
  if ~exist(mesh_file)
    error('File not found: %s', mesh_file);
  end
  for idx = 1:numel(inpfile_list)
    if ~exist(inpfile_list{idx})
      error('File not found: %s', inpfile_list{idx});
    end
  end
  
  %fsnap_dir = dirname(mesh_file);
  
  %inpfile_list = {eps_file, 'qedc3_2_05.inp'};
  %fsnap_file = fullfile(fsnap_dir, 'qedc3_2_05.inp');
  %inpfile_list = {eps_file, fsnap_file};
  
  % load and cd into workdir
  %cd(fsnap_dir);
  
  % define variables
  %eps_folder = dirname(eps_file);
  
  % TODO: this really needs to be improved...
  %last_snap_time_number = getLastSnapTimeNumber('.','yaa', 'probe_ident', 'a');
  %last_snap_time_number = getLastSnapTimeNumber('.','xaa', 'probe_ident', '_id_');
  
  %BFDTD_version = '2003'; % Should not matter for N<=51, but better to do it correctly.
  columns = {'material', 'Exmod', 'Eymod', 'Ezmod'};
  outfile_basename = [outfile_basename, '.MV_convergence'];
  
  % load data and do a first calculation
  %cd(dirname(mesh_file));
  fprintf('%s: pwd  = %s\n', basename(mfilename('fullpath')), pwd());
  ret_new = BFDTD_loadVolumetricData('mesh_file', mesh_file, 'inpfile_list', inpfile_list, 'columns', columns, 'justCheck', p.Results.justCheck, 'DataSizeMax', p.Results.DataSizeMax, 'pre_2008_BFDTD_version', p.Results.pre_2008_BFDTD_version, 'numID_list', p.Results.numID_list, 'loadGeometry', false, 'snap_time_number_fsnap', p.Results.snap_time_number_fsnap);
  
  % centro+radius info
  Cx = 0.5*(ret_new.info.frequency_snapshots.xmax + ret_new.info.frequency_snapshots.xmin);
  Cy = 0.5*(ret_new.info.frequency_snapshots.ymax + ret_new.info.frequency_snapshots.ymin);
  Cz = 0.5*(ret_new.info.frequency_snapshots.zmax + ret_new.info.frequency_snapshots.zmin);
  
  rx = 0.5*(ret_new.info.frequency_snapshots.xmax - ret_new.info.frequency_snapshots.xmin);
  ry = 0.5*(ret_new.info.frequency_snapshots.ymax - ret_new.info.frequency_snapshots.ymin);
  rz = 0.5*(ret_new.info.frequency_snapshots.zmax - ret_new.info.frequency_snapshots.zmin);
  
  centro = [Cx, Cy, Cz];
  Rmax = [rx, ry, rz];
  
  % storage variables
  ret_all = {};
  header = {};
  data = [];
  
  %alpha_volume_list = [];
  %alpha_radius_list = [];
  %rx = [];
  %ry = [];
  %rz = [];
  %VolumeRequested = [];
  
  if p.Results.justCheck
    return;
  end
  
  if ~exist(dirname(outfile_basename), 'dir')
    mkdir(dirname(outfile_basename));
  end
  
  if p.Results.doLoop
    
    %alpha_list = linspace(0, 1, 5000);
    
    %alpha_r = 0.1732/2
    %alpha_v = alpha_r^3
    
    %alpha_list = linspace(0, 1e-3);
    alpha_list = linspace(0, 1, p.Results.N);
    
    for idx = 1:numel(alpha_list)
      
      if p.Results.linear_volume
        alpha_volume = alpha_list(idx);
        alpha_radius = alpha_volume.^(1/3);
      else
        alpha_radius = alpha_list(idx);
        alpha_volume = alpha_radius.^3;
      end
      
      radius = alpha_radius.*Rmax;
      
      % store integration box info
      integration_box = struct();
      integration_box.idx = idx;
      integration_box.alpha = alpha_list(idx);
      integration_box.cx = centro(1);
      integration_box.cy = centro(2);
      integration_box.cz = centro(3);
      integration_box.rx = radius(1);
      integration_box.ry = radius(2);
      integration_box.rz = radius(3);
      integration_box.alpha_volume = alpha_volume;
      integration_box.alpha_radius = alpha_radius;
      integration_box.VolumeRequested = 8*radius(1)*radius(2)*radius(3);
      
      %alpha_volume_list(idx) = alpha_volume;
      %alpha_radius_list(idx) = alpha_radius;
      %rx(idx) = radius(1);
      %ry(idx) = radius(2);
      %rz(idx) = radius(3);
      %VolumeRequested(idx) = 8*radius(1)*radius(2)*radius(3);
      
      % linear volume
      %radius = (alpha_volume^(1/3))*Rmax;
      % linear radius
      %radius = alpha_radius*Rmax;
      
      progress = 100*idx./numel(alpha_list);
      fprintf('\n================> idx = %d/%d = %.2f%% ; alpha_volume = %f\n', idx, numel(alpha_list), progress, alpha_volume);
      
      ret_new = calculateModeVolume2(ret_new, 'refractive_index_defect', p.Results.refractive_index_defect, 'geofile', p.Results.geofile, 'defect_name', p.Results.defect_name,...
        'mask_function', @(X,Y,Z) getVolumetricMaskBox(X, Y, Z, centro, radius), 'verbosity', 0);
        
      ret_new.MV.integration_box = integration_box;
        
      ret_all{idx} = ret_new.MV;
      
      [header, row] = struct2prn(ret_new.MV);
      if isempty(data)
        data = row;
      else
        data = cat(1, data, row);
      end
      
      
      
    end
    
    if p.Results.doSaveCSV
      % save plot data
      %mkdir(dirname(outfile_basename));
      writePrnFile([outfile_basename, '.csv'], header, data, 'delimiter', ';', 'precision', '');
      
      % create and save figures
      if p.Results.doPlot
        %figure_handle = MV_convergence_plot_function(header, data, 'alpha_volume');
        %saveas_fig_and_png(figure_handle, [outfile_basename, '.alpha_volume']);
        %figure_handle = MV_convergence_plot_function(header, data, 'TotalIntegrationVolume');
        %saveas_fig_and_png(figure_handle, [outfile_basename, '.TotalIntegrationVolume']);
        %figure_handle = MV_convergence_plot_function(header, data, 'TotalMeshVolume');
        %saveas_fig_and_png(figure_handle, [outfile_basename, '.TotalMeshVolume']);
        
        %figure_handle = MV_convergence_analysis_function([outfile_basename, '.csv'], p.Results.doSavePlot);
        figure_handle = MV_convergence_analysis_function2([outfile_basename, '.csv'], p.Results.doSavePlot);
      end
      
    end
  end % if p.Results.doLoop
  
  % do a final calculation using all available data
  ret_new = calculateModeVolume2(ret_new, 'refractive_index_defect', p.Results.refractive_index_defect, 'geofile', p.Results.geofile, 'defect_name', p.Results.defect_name, 'log', GetFullPath([outfile_basename, '.final.log']));
  if p.Results.doSaveFinalLog
    disp('saving MV structure...');
    MV = ret_new.MV
    save([outfile_basename, '.MV.struct'], 'MV');
    disp('saving info structure...');
    try
      % Octave sometimes crashes here, so we just wrap it in a try statement... Error message:
      %    warning: save: wrong type argument 'function handle'
      %    error: save: error while writing '' to MAT file
      %    error: save: error while writing '' to MAT file
      %    error: save: error while writing 'info' to MAT file
      
      %ret_new_info = ret_new.info
      %save([outfile_basename, '.info.struct'], 'ret_new_info');
      save([outfile_basename, '.info.struct'], '-struct', 'ret_new', 'info');
    catch
      warning('Failed to save info structure as %s', [outfile_basename, '.info.struct']);
    end
    if inoctave()
      struct_levels_to_print(10, 'local');
    end
    diary_file = GetFullPath([outfile_basename, '.MV.log']); % Octave does not expand tilde? BUG?
    if exist(diary_file, 'file')
      delete(diary_file);
    end
    diary(diary_file);
    ret_new.info
    ret_new.MV
    diary off;
  end
  
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%% deprecated code:

  %TotalEnergy = [];
  %TotalIntegrationVolume = [];
  %TotalMeshVolume = [];
  
  %MaximumEnergyDensity.value = [];
  %MaximumE2.value = [];
  
  %MaximumEnergyDensity.epsilon = [];
  %MaximumE2.epsilon = [];
  
  %MV_MaximumE2_nfixed.mode_volume_mum3 = [];
  %MV_MaximumE2_nfixed.normalized_mode_volume_1 = [];
  
  %MV_MaximumE2_nlocal.mode_volume_mum3 = [];
  %MV_MaximumE2_nlocal.normalized_mode_volume_1 = [];
  
  %MV_MaximumEnergyDensity_nfixed.mode_volume_mum3 = [];
  %MV_MaximumEnergyDensity_nfixed.normalized_mode_volume_1 = [];
  
  %MV_MaximumEnergyDensity_nlocal.mode_volume_mum3 = [];
  %MV_MaximumEnergyDensity_nlocal.normalized_mode_volume_1 = [];

      %TotalEnergy(idx) = ret_all{idx}.TotalEnergy;
      %TotalIntegrationVolume(idx) = ret_all{idx}.TotalIntegrationVolume;
      %TotalMeshVolume(idx) = ret_all{idx}.TotalMeshVolume;
      
      %MaximumE2.value(idx) = ret_all{idx}.MaximumE2.value;
      %MaximumEnergyDensity.value(idx) = ret_all{idx}.MaximumEnergyDensity.value;
      
      %MaximumE2.epsilon(idx) = ret_all{idx}.MaximumE2.epsilon;
      %MaximumEnergyDensity.epsilon(idx) = ret_all{idx}.MaximumEnergyDensity.epsilon;
      
      %MV_MaximumE2_nfixed.mode_volume_mum3(idx) = ret_all{idx}.MV_MaximumE2_nfixed.mode_volume_mum3;
      %MV_MaximumE2_nfixed.normalized_mode_volume_1(idx) = ret_all{idx}.MV_MaximumE2_nfixed.normalized_mode_volume_1;
      
      %MV_MaximumE2_nlocal.mode_volume_mum3(idx) = ret_all{idx}.MV_MaximumE2_nlocal.mode_volume_mum3;
      %MV_MaximumE2_nlocal.normalized_mode_volume_1(idx) = ret_all{idx}.MV_MaximumE2_nlocal.normalized_mode_volume_1;
      
      %MV_MaximumEnergyDensity_nfixed.mode_volume_mum3(idx) = ret_all{idx}.MV_MaximumEnergyDensity_nfixed.mode_volume_mum3;
      %MV_MaximumEnergyDensity_nfixed.normalized_mode_volume_1(idx) = ret_all{idx}.MV_MaximumEnergyDensity_nfixed.normalized_mode_volume_1;
      
      %MV_MaximumEnergyDensity_nlocal.mode_volume_mum3(idx) = ret_all{idx}.MV_MaximumEnergyDensity_nlocal.mode_volume_mum3;
      %MV_MaximumEnergyDensity_nlocal.normalized_mode_volume_1(idx) = ret_all{idx}.MV_MaximumEnergyDensity_nlocal.normalized_mode_volume_1;

      %header = {'alpha_list', 'Veff', 'Vn1', 'TotalEnergy', 'TotalIntegrationVolume', 'TotalMeshVolume', 'MaximumEnergyDensity'};
      %data = [alpha_list(:), Veff(:), Vn1(:), TotalEnergy(:), TotalIntegrationVolume(:), TotalMeshVolume(:), MaximumEnergyDensity(:)];
      
      % TODO: Improve this madness
      %header = {'alpha_volume', 'alpha_radius', 'rx', 'ry', 'rz', 'VolumeRequested',...
                %'TotalEnergy', 'TotalIntegrationVolume', 'TotalMeshVolume',...
                %'MaxEnergy.value', 'MaxE2.value',...
                %'MaxEnergy.epsilon', 'MaxE2.epsilon',...
                %'MaxE2_nfixed.Veff', 'MaxE2_nfixed.Vn1',...
                %'MaxE2_nlocal.Veff', 'MaxE2_nlocal.Vn1',...
                %'MaxEnergy_nfixed.Veff', 'MaxEnergy_nfixed.Vn1',...
                %'MaxEnergy_nlocal.Veff', 'MaxEnergy_nlocal.Vn1'};
      %data = [alpha_volume_list(:), alpha_radius_list(:), rx(:), ry(:), rz(:), VolumeRequested(:),...
              %TotalEnergy(:), TotalIntegrationVolume(:), TotalMeshVolume(:),...
              %MaximumEnergyDensity.value(:), MaximumE2.value(:),...
              %MaximumEnergyDensity.epsilon(:), MaximumE2.epsilon(:),...
              %MV_MaximumE2_nfixed.mode_volume_mum3(:), MV_MaximumE2_nfixed.normalized_mode_volume_1(:),...
              %MV_MaximumE2_nlocal.mode_volume_mum3(:), MV_MaximumE2_nlocal.normalized_mode_volume_1(:),...
              %MV_MaximumEnergyDensity_nfixed.mode_volume_mum3(:), MV_MaximumEnergyDensity_nfixed.normalized_mode_volume_1(:),...
              %MV_MaximumEnergyDensity_nlocal.mode_volume_mum3(:), MV_MaximumEnergyDensity_nlocal.normalized_mode_volume_1(:)];
