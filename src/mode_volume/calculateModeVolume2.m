function ret = calculateModeVolume2(ret, varargin)
  % TODO: -use trapz+cumtrapz
  % TODO: store selection specific info elsewhere? (for easier comparisons to default)
  % TODO: improve logging params: allow boolean or filename
  % TODO: try to use boolean masks instead of double to reduce memory usage
  % TODO: for convergence plots, it would be more efficient to pass the defect mask instead of always recalculating it. Alternative: check if mask is stored in "ret".
  % TODO: store all computed datasets, since they use up RAM during function call, so might as well store them? + can be cleared via ret=rmfield(ret,'y');
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %%%%% create parser
  p = inputParser();
  p = inputParserWrapper(p, 'addRequired', 'ret', @isstruct);
  p = inputParserWrapper(p, 'addParamValue', 'refractive_index_defect', NaN, @isnumeric);
  %p = inputParserWrapper(p, 'addParamValue', 'integration_sphere_centre', [NaN, NaN, NaN], @(x) isnumeric(x) && length(x)==3);
  %p = inputParserWrapper(p, 'addParamValue', 'integration_sphere_radius', NaN, @(x) isnumeric(x) && length(x)==1);
  %p = inputParserWrapper(p, 'addParamValue', 'norm_function', @norm, @(x) isa(x, 'function_handle'));
  p = inputParserWrapper(p, 'addParamValue', 'mask_function', false, @(x) isa(x, 'function_handle') || (islogical(x) && ~x ) );
  p = inputParserWrapper(p, 'addParamValue', 'geofile', '', @ischar);
  p = inputParserWrapper(p, 'addParamValue', 'defect_name', 'defect', @ischar);
  p = inputParserWrapper(p, 'addParamValue', 'verbosity', 1, @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'log', false, @(x) islogical(x) || (ischar(x) && ~isempty(x)) );
  p = inputParserWrapper(p, 'parse', ret, varargin{:});
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %%%%% additional input processing
  
  %%%%%%%%%%%%
  %%% code from old calculateModeVolume() script:
  % TODO: reduce code duplication from old calculateModeVolume() script
  
  % verbosity handling
  if p.Results.verbosity > 0
    stdout_fid = 1;
  else
    stdout_fid = -1;
  end
  
  % logfile handling (diary() replaced by disp_and_log() for more control)
  if ischar(p.Results.log) && ~isempty(p.Results.log)
    logfile = p.Results.log;
  elseif islogical(p.Results.log) && p.Results.log
    logfile = sprintf('mode-volume-run_%02d.txt', ret.info.snap_time_number_fsnap);
  else
    logfile = '';
  end
  if ~isempty(logfile)
    if p.Results.verbosity > 0
      disp(['logfile = ', logfile]);
    end
    logfile_fid = fopen(logfile,'w');
  else
    logfile_fid = -1;
  end
  
  % get defect from geofile if specified
  % TODO: could use list of objects later for very detailed and complex energy distribution info (less needed when 3D vis is used)
  if isfield(ret.info, 'defect_properties');
    ret.info = rmfield(ret.info, 'defect_properties');
  end
  ret.info.defect_properties.defect_found = false;
  if ~isempty(p.Results.geofile)
    disp_and_log([stdout_fid, logfile_fid], 'geofile specified, attempting defect detection...');
    ret.info.defect_properties = getDefectProperties(p.Results.geofile, p.Results.defect_name);
    if ret.info.defect_properties.defect_found
      disp_and_log([stdout_fid, logfile_fid], 'defect found');
    else
      disp_and_log([stdout_fid, logfile_fid], 'defect not found');
    end
  end
  
  % set ret.MV.refractive_index_defect
  ret.MV.refractive_index_defect = p.Results.refractive_index_defect;
  if isnan(ret.MV.refractive_index_defect)
    if ret.info.defect_properties.defect_found
      ret.MV.refractive_index_defect = sqrt(ret.info.defect_properties.object.permittivity);
    else
      ret.MV.refractive_index_defect = 1;
    end
  end
  disp_and_log([stdout_fid, logfile_fid], 'Setting ret.MV.refractive_index_defect = %f ( permittivity = %f )', ret.MV.refractive_index_defect, ret.MV.refractive_index_defect.^2);
  %%%%%%%%%%%%
  
  if numel(ret.info.frequency_set)~=1
    error('Number of frequencies is not exactly 1.');
  end
  
  wavelength_mum = get_c0() ./ ret.info.frequency_set(1);
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %%%%%%%%%% start calculations
  
  %%%%% preliminaries
  
  % get field indices
  % TODO: some getter functions for these common operations? and/or use named tables for data...
  idx_material = find(strcmpi('material', ret.data.header));
  idx_Exmod = find(strcmpi('Exmod', ret.data.header));
  idx_Eymod = find(strcmpi('Eymod', ret.data.header));
  idx_Ezmod = find(strcmpi('Ezmod', ret.data.header));
  
  % compute Emod2 amd EnergyDensity datasets
  if ~isfield(ret.data, 'Emod2') || ~isfield(ret.data, 'EnergyDensity')
    ret = addModeVolumeData(ret);
  end
  
  % compute Energy dataset
  Energy = (ret.data.EnergyDensity .* ret.data.dV);
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %%%%% create selection mask
  if isa(p.Results.mask_function, 'function_handle')
    selection_mask = p.Results.mask_function(ret.data.X, ret.data.Y, ret.data.Z);
  else
    selection_mask = true(size(ret.data.X));
  end
  
  %%%%% create defect mask
  if ret.info.defect_properties.defect_found
    % TODO: fix case where BFDTD finds point outside, but I find point inside...
    % TODO: optimize by using existing defect mask?: if isfield(ret.data, 'defect_mask')...
    defect_mask = ret.info.defect_properties.point_in_object(ret.data.X, ret.data.Y, ret.data.Z);
    defect_mask = defect_mask .* (ret.data.D(:, :, :, idx_material) == ret.info.defect_properties.object.permittivity);
  else
    defect_mask = false(size(ret.data.X));
  end
  
  %%%%% store masks for debugging
  ret.data.defect_mask = defect_mask;
  ret.data.selection_mask = selection_mask;
  
  %%%%% integrate + extract maxima info
  ret.MV.info_full                 = calculateModeVolume_getFundamentalInfo(ret.data.X, ret.data.Y, ret.data.Z,...
                                       ret.data.D(:, :, :, idx_material),...
                                       ret.data.Emod2,...
                                       ret.data.dV);
  
  ret.MV.info_defect               = calculateModeVolume_getFundamentalInfo(ret.data.X, ret.data.Y, ret.data.Z,...
                                       defect_mask .* ret.data.D(:, :, :, idx_material),...
                                       defect_mask .* ret.data.Emod2,...
                                       defect_mask .* ret.data.dV);
  
  ret.MV.info_selection            = calculateModeVolume_getFundamentalInfo(ret.data.X, ret.data.Y, ret.data.Z,...
                                       selection_mask .* ret.data.D(:, :, :, idx_material),...
                                       selection_mask .* ret.data.Emod2,...
                                       selection_mask .* ret.data.dV);
  
  ret.MV.info_selection_and_defect = calculateModeVolume_getFundamentalInfo(ret.data.X, ret.data.Y, ret.data.Z,...
                                       selection_mask .* defect_mask .* ret.data.D(:, :, :, idx_material),...
                                       selection_mask .* defect_mask .* ret.data.Emod2,...
                                       selection_mask .* defect_mask .* ret.data.dV);
  
  %%%%% create MV info structures
  ret.MV.MV_MaximumEnergyDensity_nfixed = createMVstruct(ret.MV.info_selection.TotalEnergy,...
                                                         ret.MV.info_selection.MaximumEnergyDensity.EnergyDensity,...
                                                         wavelength_mum,...
                                                         ret.MV.refractive_index_defect);
  
  ret.MV.MV_MaximumEnergyDensity_nlocal = createMVstruct(ret.MV.info_selection.TotalEnergy,...
                                                         ret.MV.info_selection.MaximumEnergyDensity.EnergyDensity,...
                                                         wavelength_mum,...
                                                         ret.MV.info_selection.MaximumEnergyDensity.refractive_index);
  
  ret.MV.MV_MaximumEmod2_nfixed = createMVstruct(ret.MV.info_selection.TotalEnergy,...
                                                         ret.MV.info_selection.MaximumEmod2.EnergyDensity,...
                                                         wavelength_mum,...
                                                         ret.MV.refractive_index_defect);
  
  ret.MV.MV_MaximumEmod2_nlocal = createMVstruct(ret.MV.info_selection.TotalEnergy,...
                                                         ret.MV.info_selection.MaximumEmod2.EnergyDensity,...
                                                         wavelength_mum,...
                                                         ret.MV.info_selection.MaximumEmod2.refractive_index);
  
  ret.MV.MV_MaximumEnergyDensity_nfixed_defect = createMVstruct(ret.MV.info_selection.TotalEnergy,...
                                                         ret.MV.info_selection_and_defect.MaximumEnergyDensity.EnergyDensity,...
                                                         wavelength_mum,...
                                                         ret.MV.refractive_index_defect);
  
  ret.MV.MV_MaximumEnergyDensity_nlocal_defect = createMVstruct(ret.MV.info_selection.TotalEnergy,...
                                                         ret.MV.info_selection_and_defect.MaximumEnergyDensity.EnergyDensity,...
                                                         wavelength_mum,...
                                                         ret.MV.info_selection_and_defect.MaximumEnergyDensity.refractive_index);
  
  ret.MV.MV_MaximumEmod2_nfixed_defect = createMVstruct(ret.MV.info_selection.TotalEnergy,...
                                                         ret.MV.info_selection_and_defect.MaximumEmod2.EnergyDensity,...
                                                         wavelength_mum,...
                                                         ret.MV.refractive_index_defect);
  
  ret.MV.MV_MaximumEmod2_nlocal_defect = createMVstruct(ret.MV.info_selection.TotalEnergy,...
                                                         ret.MV.info_selection_and_defect.MaximumEmod2.EnergyDensity,...
                                                         wavelength_mum,...
                                                         ret.MV.info_selection_and_defect.MaximumEmod2.refractive_index);
  
  %%%%% compute per-material info
  ret.MV.materials.epsilon = unique(ret.data.D(:, :, :, idx_material));
  ret.MV.materials.volume = [];
  ret.MV.materials.energy = [];
  for epsilon_idx = 1:numel(ret.MV.materials.epsilon)
    epsilon_val = ret.MV.materials.epsilon(epsilon_idx);
    epsilon_mask = (ret.data.D(:, :, :, idx_material) == epsilon_val);
    ret.MV.materials.volume(epsilon_idx) = sumFlat(ret.data.dV(epsilon_mask));
    ret.MV.materials.energy(epsilon_idx) = sumFlat(Energy(epsilon_mask));
  end
  
  %%%%% display results
  
  disp_and_log([stdout_fid, logfile_fid], '\n=== Detailed information ===\n');
  disp_and_log([stdout_fid, logfile_fid], printStructure(ret));
  
  disp_and_log([stdout_fid, logfile_fid], '\n=== Material information ===\n');
  for epsilon_idx = 1:numel(ret.MV.materials.epsilon)
    disp_and_log([stdout_fid, logfile_fid], '  epsilon = %.4f <=> index = %.2f', ret.MV.materials.epsilon(epsilon_idx), sqrt(ret.MV.materials.epsilon(epsilon_idx)));
    disp_and_log([stdout_fid, logfile_fid], '    volume (mum^3) = %E = %.2f %% of total volume', ret.MV.materials.volume(epsilon_idx), 100*ret.MV.materials.volume(epsilon_idx) ./ sumFlat(ret.MV.materials.volume));
    disp_and_log([stdout_fid, logfile_fid], '    energy (J) = %E = %.2f %% of total energy', ret.MV.materials.energy(epsilon_idx), 100*ret.MV.materials.energy(epsilon_idx) ./ sumFlat(ret.MV.materials.energy));
  end
  
  if ret.info.defect_properties.defect_found
    disp_and_log([stdout_fid, logfile_fid], '\n=== Defect information ===\n');
    disp_and_log([stdout_fid, logfile_fid], '  epsilon = %.4f <=> index = %.2f', ret.info.defect_properties.object.permittivity, sqrt(ret.info.defect_properties.object.permittivity));
    disp_and_log([stdout_fid, logfile_fid], '    volume (mum^3) = %E = %.2f %% of total volume', ret.MV.info_defect.TotalVolume_Mesh, 100*ret.MV.info_defect.TotalVolume_Mesh ./ ret.MV.info_full.TotalVolume_Mesh);
    disp_and_log([stdout_fid, logfile_fid], '    energy (J) = %E = %.2f %% of total energy', ret.MV.info_defect.TotalEnergy, 100*ret.MV.info_defect.TotalEnergy ./ ret.MV.info_full.TotalEnergy);
  end
  disp_and_log([stdout_fid, logfile_fid], '\n=== Summary (using data in selection and local index) ===\n');
  disp_and_log([stdout_fid, logfile_fid], 'Total energy: %f', ret.MV.info_selection.TotalEnergy);
  disp_and_log([stdout_fid, logfile_fid], 'Wavelength (mum): %f', wavelength_mum);
  
  disp_and_log([stdout_fid, logfile_fid], '\nMode volume using max(EnergyDensity) anywhere:\n');
  printSummary(stdout_fid, logfile_fid, ret.MV.info_selection.MaximumEnergyDensity, ret.MV.MV_MaximumEnergyDensity_nlocal       );
  
  disp_and_log([stdout_fid, logfile_fid], '\nMode volume using max(|E|^2) anywhere:\n');
  printSummary(stdout_fid, logfile_fid, ret.MV.info_selection.MaximumEmod2,         ret.MV.MV_MaximumEmod2_nlocal               );
  
  disp_and_log([stdout_fid, logfile_fid], '\nMode volume using max(EnergyDensity or |E|^2) in defect:\n');
  printSummary(stdout_fid, logfile_fid, ret.MV.info_selection_and_defect.MaximumEnergyDensity, ret.MV.MV_MaximumEnergyDensity_nlocal_defect);
  
  if logfile_fid >= 0
    % close logfile
    fclose(logfile_fid);
  end
  
end

function printSummary(stdout_fid, logfile_fid, max_info, MV_structure)
  disp_and_log([stdout_fid, logfile_fid], '  epsilon = %f', max_info.epsilon);
  disp_and_log([stdout_fid, logfile_fid], '  refractive index: n = %f', max_info.refractive_index);
  disp_and_log([stdout_fid, logfile_fid], '  |E|^2 = %E', max_info.Emod2);
  disp_and_log([stdout_fid, logfile_fid], '  epsilon*|E|^2 = %E', max_info.EnergyDensity);
  disp_and_log([stdout_fid, logfile_fid], '  mode volume: Veff = %f', MV_structure.mode_volume_mum3);
  disp_and_log([stdout_fid, logfile_fid], '  normalized mode volume: Vn1 = Veff / ((lambda/n)^3): %E', MV_structure.normalized_mode_volume_1);
end

% old code
    %mask = getVolumetricMask(ret, p.Results.integration_sphere_centre, p.Results.integration_sphere_radius);
    %xmin = p.Results.integration_sphere_centre(1) - p.Results.integration_sphere_radius;
    %xmax = p.Results.integration_sphere_centre(1) + p.Results.integration_sphere_radius;
    %ymin = p.Results.integration_sphere_centre(2) - p.Results.integration_sphere_radius;
    %ymax = p.Results.integration_sphere_centre(2) + p.Results.integration_sphere_radius;
    %zmin = p.Results.integration_sphere_centre(3) - p.Results.integration_sphere_radius;
    %zmax = p.Results.integration_sphere_centre(3) + p.Results.integration_sphere_radius;
    %limits = [xmin,xmax,ymin, ymax,zmin,zmax];
    %[Nx,Ny,Nz,Nv] = subvolume(ret.data.X, ret.data.Y, ret.data.Z, ret.data.X, limits);
    %% create mask
    %mask = zeros(size(ret.data.X));
    %for linear_index = 1:numel(ret.data.X)
      %x = ret.data.X(linear_index);
      %y = ret.data.Y(linear_index);
      %z = ret.data.Z(linear_index);
      %if p.Results.norm_function([x;y;z] - p.Results.integration_sphere_centre(:)) <= p.Results.integration_sphere_radius
        %mask(linear_index) = 1;
      %end
    %end

  %if ~isfield(ret.data, 'material')  || ~isfield(ret.data, 'Emod2') || ~isfield(ret.data, 'EnergyDensity')
  %ret.data.material = ret.data.D(:,:,:, idx_material);

  %if any(isnan(p.Results.integration_sphere_centre)) || any(isnan(p.Results.integration_sphere_radius))

  %ret = createMVstruct(TotalEnergy, MaximumEnergyDensity, wavelength_mum, refractive_index_defect)
  
  %ret.MV.MV_MaximumEnergyDensity_nfixed = createMVstruct(Etot, maxEnergyDensity, wavelength_mum, ret.MV.refractive_index_defect);
  %ret = createMVstruct(TotalEnergy, MaximumEnergyDensity, wavelength_mum, refractive_index_defect)
  
  %ret.MV.info_selection.TotalEnergy
  
  %ret.MV.info_selection.MaximumEmod2.EnergyDensity
  %ret.MV.info_selection.MaximumEnergyDensity.EnergyDensity
  %ret.MV.info_defect.MaximumEmod2.EnergyDensity
  %ret.MV.info_defect.MaximumEnergyDensity.EnergyDensity
  
  
  
  %wavelength_mum
  
  %ret.MV.info_selection.MaximumEmod2.refractive_index
  %ret.MV.info_selection.MaximumEnergyDensity.refractive_index
  %ret.MV.info_defect.MaximumEmod2.refractive_index
  %ret.MV.info_defect.MaximumEnergyDensity.refractive_index
  %ret.MV.refractive_index_defect
  
  %return
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %%%%%% integration
  %if ~is_function_handle(p.Results.mask_function)
    %% integrate over whole volume
    %nonzeros_idx = find(ret.data.EnergyDensity);
    %ret.MV.TotalIntegrationVolume = sum(ret.data.dV(nonzeros_idx));
    %ret.MV.TotalMeshVolume = sum(ret.data.dV(:));
    %ret.MV.TotalEnergy = sum(Energy(:));
    
    %% get maxima info
    %[ret.MV.MaximumEnergyDensity.value, ret.MV.MaximumEnergyDensity.linear_index] = max(ret.data.EnergyDensity(:));
    %[ret.MV.MaximumE2.value, ret.MV.MaximumE2.linear_index] = max(ret.data.Emod2(:));
    %[ret.MV.MaximumEnergyDensity_in_defect.value, ret.MV.MaximumEnergyDensity_in_defect.linear_index] = max(ret.data.EnergyDensity(:));
    %[ret.MV.MaximumE2_in_defect.value, ret.MV.MaximumE2_in_defect.linear_index] = max(ret.data.Emod2(:));
    
  %else
    %mask = p.Results.mask_function(ret.data.X, ret.data.Y, ret.data.Z);
    %nonzeros_idx = find(mask .* ret.data.EnergyDensity);
    %ret.MV.TotalIntegrationVolume = sum(ret.data.dV(nonzeros_idx));
    %ret.MV.TotalMeshVolume = sum( (mask .* ret.data.dV)(:) );
    %ret.MV.TotalEnergy = sum( (mask .* Energy)(:) );
    
    %% get maxima info
    %[ret.MV.MaximumEnergyDensity.value, ret.MV.MaximumEnergyDensity.linear_index] = max( (mask .* ret.data.EnergyDensity)(:) );
    %[ret.MV.MaximumE2.value, ret.MV.MaximumE2.linear_index] = max( (mask .* ret.data.Emod2)(:) );
    %[ret.MV.MaximumEnergyDensity.value, ret.MV.MaximumEnergyDensity.linear_index] = max( (mask .* defect_mask .* ret.data.EnergyDensity)(:) );
    %[ret.MV.MaximumE2.value, ret.MV.MaximumE2.linear_index] = max( (mask .* ret.data.Emod2)(:) );
  %end
  
  %% get maxima locations
  %ret.MV.MaximumE2.x = ret.data.X(ret.MV.MaximumE2.linear_index);
  %ret.MV.MaximumE2.y = ret.data.Y(ret.MV.MaximumE2.linear_index);
  %ret.MV.MaximumE2.z = ret.data.Z(ret.MV.MaximumE2.linear_index);
  %[ret.MV.MaximumE2.y_index, ret.MV.MaximumE2.x_index, ret.MV.MaximumE2.z_index] = ind2sub(size(ret.data.X), ret.MV.MaximumE2.linear_index);
  
  %ret.MV.MaximumEnergyDensity.x = ret.data.X(ret.MV.MaximumEnergyDensity.linear_index);
  %ret.MV.MaximumEnergyDensity.y = ret.data.Y(ret.MV.MaximumEnergyDensity.linear_index);
  %ret.MV.MaximumEnergyDensity.z = ret.data.Z(ret.MV.MaximumEnergyDensity.linear_index);
  %[ret.MV.MaximumEnergyDensity.y_index, ret.MV.MaximumEnergyDensity.x_index, ret.MV.MaximumEnergyDensity.z_index] = ind2sub(size(ret.data.X), ret.MV.MaximumEnergyDensity.linear_index);
  
  %% get maxima epsilon values
  %ret.MV.MaximumEnergyDensity.epsilon = ret.data.D(ret.MV.MaximumEnergyDensity.y_index, ret.MV.MaximumEnergyDensity.x_index, ret.MV.MaximumEnergyDensity.z_index, idx_material);
  %ret.MV.MaximumE2.epsilon = ret.data.D(ret.MV.MaximumE2.y_index, ret.MV.MaximumE2.x_index, ret.MV.MaximumE2.z_index, idx_material);
  
  %% calculate mode volumes
  %if ret.MV.MaximumEnergyDensity.value ~= 0
    %MV_MaximumEnergyDensity = ret.MV.TotalEnergy ./ ret.MV.MaximumEnergyDensity.value;
  %else
    %MV_MaximumEnergyDensity = NaN;
  %end
  %if ( ret.MV.MaximumE2.epsilon * ret.MV.MaximumE2.value ) ~= 0
    %MV_MaximumE2 = ret.MV.TotalEnergy ./ ( ret.MV.MaximumE2.epsilon * ret.MV.MaximumE2.value );
  %else
    %MV_MaximumE2 = NaN;
  %end
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %% create MV info structures
  
  %ret.MV.MV_MaximumEnergyDensity_nfixed = createMVstruct(MV_MaximumEnergyDensity, wavelength_mum, ret.MV.refractive_index_defect);
  %ret.MV.MV_MaximumEnergyDensity_nlocal = createMVstruct(MV_MaximumEnergyDensity, wavelength_mum, sqrt(ret.MV.MaximumEnergyDensity.epsilon));
  
  %ret.MV.MV_MaximumE2_nfixed = createMVstruct(MV_MaximumE2, wavelength_mum, ret.MV.refractive_index_defect);
  %ret.MV.MV_MaximumE2_nlocal = createMVstruct(MV_MaximumE2, wavelength_mum, sqrt(ret.MV.MaximumE2.epsilon));
  
  %ret.MV.MV_MaximumE2_nfixed = createMVstruct(MV_MaximumE2, wavelength_mum, ret.MV.refractive_index_defect);
  %ret.MV.MV_MaximumE2_nlocal = createMVstruct(MV_MaximumE2, wavelength_mum, sqrt(ret.MV.MaximumE2.epsilon));
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
