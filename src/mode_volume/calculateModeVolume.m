function ret = calculateModeVolume(inpfile_list, varargin)
  % SPAGHETTI CODE!!!
  %
  % function ret = calculateModeVolume(inpfile_list, varargin)
  %
  % Example:
  %  calculateModeVolume({'epsilon_snaphots.inp','frequency_snapshots.inp'}, 'eps_folder', '../epsilon', 'snap_plane', 'x', 'refractive_index_defect', 1.5)
  %
  % Required argument:
  %  inpfile_list : List of input files of the form {'file1.inp','file2.inp',...}
  %
  % Optional arguments:
  %  fsnap_folder : folder containing the .prn files for frequency snapshots. Default = '.'
  %  eps_folder : folder containing the .prn files for epsilon snapshots. Default = '.'
  %  snap_plane : direction of the snapshots ('x','y' or 'z'). Default = 'z'
  %  snap_time_number : the number of the snapshot (i.e. 02 in zaaid02.prn for example). Default = biggest number for which snapshots are available.
  %  refractive_index_defect : refractive index used to normalize the mode volume (usually refractive index of the defect/cavity). Default = 1.
  %  is_half_sim : if set to true, the calculated mode volume will be multiplied by 2. Set to 'false' by default.
  %  numID_list : List of numIDs of snapshots to allow selecting specific ones. However the chosen 'snap_plane' direction is still used for filtering, so a snapshot must be in the snap_plane direction and in numID_list to be selected! If not specified or empty, it defaults to a list of all numIDs.
  %  justCheck : If true, the command only lists details about the snapshots that would be used to calculate the mode volume and does nothing else. Default = false.
  %  mode_index : Index of the mode for which to calculate the mode volume. Default = 1.
  %  Nmodes : Total number of modes for which mode volume snapshots are available. Default = 1. (designed for snapshots created as follows: {(z1,f1), (z1,f2), (z2,f1), (z2,f2), (z3,f1), (z3,f2)})
  %  logfile_bool : If true log calculation info to a file in the fsnap_folder, else don't log. Default = false.
  %  incorrectAlgorithm_bool : If true, use the incorrect mode volume calculation used in JQE paper. Only re-implemented for comparison purposes. Should always be left false otherwise! Default = false
  %  logfile : Specify the name of the file to log to, if logfile_bool is true. If set to an empty string, a default name will be used. Default = ''
  %  integration_sphere: Specify a spherical volume over which to integrate. Format: [xc,yc,zc,radius] where (xc,yc,zc) is the sphere centre and "radius" its radius. If radius<0, the whole volume is used. Default = '[0,0,0,-1]'
  %  epsilon_lookup_table: Specify a file containing a lookup table to use for epsilon values. The file should be in the .prn format with 2 columns.
  %
  % Return value:
  % A structure *ret* of the following form is returned:
  %  ret.allFilesFound
  %  ret.TotalEnergy
  %  ret.MaximumEnergyDensity
  %  ret.MV_MaximumEnergyDensity_nfixed
  %  ret.MV_MaximumEnergyDensity_nlocal
  %  ret.MV_MaximumE2_nfixed
  %  ret.MV_MaximumE2_nlocal
  %  ret.Lambda_mum
  %  ret.f0_MHz
  %  ret.first
  %  ret.snap_time_number
  %  ret.repetition
  %  ret.Niterations
  %  ret.refractive_index_defect
  %  ret.box
  %
  % Octave compatible: Yes (last test: 2016-04-22)
  % Matlab compatible: ??? (last test: ????-??-??)
  %
  % NOTE: Missing epsilon generating .inp files can be created using bfdtd_tool.py.
  % Example: bfdtd_tool.py -i qedc3_2_05.in --outdir . --basename qedc3_2_05_epsilon FreqToEps
  %
  % TODO: Left/right/trapezoidal integration, interpolation? Use Matlab methods... (or numpy/scipy later) (Matlab: trapz() and integral())
  % TODO: Fix block integration
  % TODO: Add support for split MV processing (part_1/part_2 folders) (Note: Maybe we could use searchpaths. But that's hazardous...)
  % TODO: Add option to save energy snapshots
  % TODO: Add option to calculate MV for all available snap_time_number values?
  % TODO: Create GUI. -> will probably be done in python/C++
  % TODO: Finish Python version.
  % TODO: Cleanup.
  % TODO: Add a way to load/save config files.
  % TODO: Validate using theoretical functions with known integral. -> cf: testing/mode_volume_validation.*
  % TODO: auto-save option of snapshots + maybe vtk generation
  % TODO: Only read in box from .geo file instead of all objects to reduce loading time. (Reducing the loading time is another todo... Python seems to do it faster already.)
  % TODO: Evaluate MV error based on mesh size, timestep, etc. Same for Q factor and then give corresponding error on coupling strength.
  % TODO: Auto-determine snapshot direction... (will not be needed once we just use all available data...)
  % TODO: Improve max snapshot time determination in case of multidir sims (never do those again!)... ex: part_1 up to 16 and part_2 up to 4...
  % TODO: Add option to raise error during just check runs when missing files?
  % TODO: justCheck should include snapshot order check (no negative thickness)... (again: not needed once we just use all...)
  % TODO: Add option to loop through all snap_time_number values to more easily check change in time...
  % TODO: Add command + args to logfile? (same for any other logging functions) + maybe git commit hash? -> should make debugging/reproduction easier
  % TODO: Calculate concentration factors? (i.e. energy percentage as a function of epsilon)
  % TODO: URGENT: calcMV: create 3D data array in mesh format and then calculate mode volume and other crap... -> will make vis, processing, etc a lot easier!!! (calcMV: another result of using shitty existing code as a starting point...)
  % TODO: Add convergence checks: vs increasing integration volume + energy at edges vs total energy/max energy
  % TODO: improve return structure (Veff is same no matter what normalization is used (fixed or local))
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %%%%% create parser
  p = inputParser();
  p = inputParserWrapper(p, 'addRequired', 'inpfile_list', @iscellstr);
  p = inputParserWrapper(p, 'addParamValue', 'fsnap_folder', '.', @ischar);
  p = inputParserWrapper(p, 'addParamValue', 'eps_folder', '.', @ischar);
  p = inputParserWrapper(p, 'addParamValue', 'snap_plane', 'z', @(x) any(validatestring(x, {'x','y','z'})));
  p = inputParserWrapper(p, 'addParamValue', 'snap_time_number', NaN, @isnumeric); % if not given, we use getLastSnapTimeNumber()
  p = inputParserWrapper(p, 'addParamValue', 'refractive_index_defect', NaN, @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'is_half_sim', false, @islogical);
  p = inputParserWrapper(p, 'addParamValue', 'numID_list', [], @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'justCheck', false, @islogical);
  
  p = inputParserWrapper(p, 'addParamValue', 'pre_2008_BFDTD_version', false, @islogical);
  
  p = inputParserWrapper(p, 'addParamValue', 'mode_index', 1, @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'Nmodes', 1, @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'incorrectAlgorithm_bool', false, @islogical); % Incorrect mode volume calculation used in JQE paper. Only re-implemented for comparison purposes. Should always be left false otherwise!
  p = inputParserWrapper(p, 'addParamValue', 'logfile_bool', false, @islogical);
  p = inputParserWrapper(p, 'addParamValue', 'logfile', '', @ischar);
  p = inputParserWrapper(p, 'addParamValue', 'integration_direction', 0, @(x) isnumeric(x) && size(x)==1 && any(x==[-1,0,1]));
  
  p = inputParserWrapper(p, 'addParamValue', 'integration_sphere', [0,0,0,-1], @(x) isnumeric(x) && length(x)==4);
  p = inputParserWrapper(p, 'addParamValue', 'norm_function', @norm, @(x) isa(x, 'function_handle'));
  
  p = inputParserWrapper(p, 'addParamValue', 'epsilon_lookup_table', '', @ischar);
  p = inputParserWrapper(p, 'addParamValue', 'verbosity', 1, @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'geofile', '', @ischar);
  p = inputParserWrapper(p, 'addParamValue', 'defect_name', 'defect', @ischar);
  p = inputParserWrapper(p, 'addParamValue', 'workdir', '', @ischar);
  
  p = inputParserWrapper(p, 'parse', inpfile_list, varargin{:});

  %p.Results.norm_function([1,2,3])
  %ret = struct();
  %return

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %%%%% misc init ops
  
  % define a custom function, so it can be re-used easily for other workdirs (useful together with filefun() for example)
  ret.custom_function = @(x) calculateModeVolume(p.Results.inpfile_list, ...
                                                  'fsnap_folder', p.Results.fsnap_folder, ...
                                                  'eps_folder', p.Results.eps_folder, ...
                                                  'snap_plane', p.Results.snap_plane, ...
                                                  'snap_time_number', p.Results.snap_time_number, ...
                                                  'refractive_index_defect', p.Results.refractive_index_defect, ...
                                                  'is_half_sim', p.Results.is_half_sim, ...
                                                  'numID_list', p.Results.numID_list, ...
                                                  'justCheck', p.Results.justCheck, ...
                                                  'pre_2008_BFDTD_version', p.Results.pre_2008_BFDTD_version, ...
                                                  'mode_index', p.Results.mode_index, ...
                                                  'Nmodes', p.Results.Nmodes, ...
                                                  'logfile_bool', p.Results.logfile_bool, ...
                                                  'incorrectAlgorithm_bool', p.Results.incorrectAlgorithm_bool, ...
                                                  'logfile', p.Results.logfile, ...
                                                  'integration_direction', p.Results.integration_direction, ...
                                                  'integration_sphere', p.Results.integration_sphere, ...
                                                  'epsilon_lookup_table', p.Results.epsilon_lookup_table, ...
                                                  'verbosity', p.Results.verbosity, ...
                                                  'geofile', p.Results.geofile, ...
                                                  'defect_name', p.Results.defect_name, ...
                                                  'workdir', x);

  % change to workdir if specified
  ORIGDIR = pwd();
  if ~isempty(p.Results.workdir)
    cd(p.Results.workdir);
  end
  ret.workdir = pwd();
  if p.Results.verbosity > 0
    fprintf(1, '=====> workdir = %s\n', ret.workdir);
  end

  % check if dirs exist
  if ~isdir(p.Results.fsnap_folder)
    error('p.Results.fsnap_folder = %s is not a valid directory', p.Results.fsnap_folder);
  end
  if ~isdir(p.Results.eps_folder)
    error('p.Results.eps_folder = %s is not a valid directory', p.Results.eps_folder);
  end

  % default return values
  ret.allFilesFound = true;
  
  ret.TotalEnergy = NaN;
  ret.MaximumEnergyDensity = struct();
  
  ret.TotalE2V = NaN;
  ret.MaximumE2 = struct();
  
  ret.Lambda_mum = NaN;
  ret.f0_MHz = NaN;
  ret.first = NaN;
  ret.snap_time_number = NaN;
  ret.repetition = NaN;
  ret.Niterations = NaN;
  ret.refractive_index_defect = NaN;
  ret.box = struct();
  
  ret.MV_MaximumEnergyDensity_nfixed = createMVstruct();
  ret.MV_MaximumEnergyDensity_nlocal = createMVstruct();
  ret.MV_MaximumE2_nfixed = createMVstruct();
  ret.MV_MaximumE2_nlocal = createMVstruct();
  
  ret.Nsnapshots = NaN;
  ret.commandArguments = p.Results;
  
  % per-material values
  ret.materials.epsilon = [];
  ret.materials.energy = [];
  ret.materials.volume = [];

  % define integration sphere parameters
  integration_sphere_centre = p.Results.integration_sphere(1:3);
  integration_sphere_radius = p.Results.integration_sphere(4);

  % verbosity handling
  if p.Results.verbosity > 0
    stdout_fid = 1;
  else
    stdout_fid = -1;
  end

  % logfile handling (diary() replaced by disp_and_log() for more control)
  if p.Results.logfile_bool
    if ~isempty(p.Results.logfile)
      logfile = p.Results.logfile;
    else
      logfile = sprintf('mode-volume-run_%d-%d_%02d.txt', p.Results.mode_index, p.Results.Nmodes, p.Results.snap_time_number);
      if p.Results.incorrectAlgorithm_bool
        logfile = sprintf('mode-volume-run_%d-%d_%02d.incorrectAlgorithm.txt', p.Results.mode_index, p.Results.Nmodes, p.Results.snap_time_number);
      end
    end  
    logfile = fullfile(p.Results.fsnap_folder, logfile);
    if p.Results.verbosity > 0
      disp(['logfile = ', logfile]);
    end
    logfile_fid = fopen(logfile,'w');
  else
    logfile_fid = -1;
  end

  % get defect from geofile if specified
  % TODO: could use list of objects later for very detailed and complex energy distribution info (less needed when 3D vis is used)
  ret.defect_properties.defect_found = false;
  if ~isempty(p.Results.geofile)
    disp_and_log([stdout_fid, logfile_fid], 'geofile specified, attempting defect detection...');
    ret.defect_properties = getDefectProperties(p.Results.geofile, p.Results.defect_name);
    if ret.defect_properties.defect_found
      disp_and_log([stdout_fid, logfile_fid], 'defect found');
    else
      disp_and_log([stdout_fid, logfile_fid], 'defect not found');
    end
  end

  % set ret.refractive_index_defect
  ret.refractive_index_defect = p.Results.refractive_index_defect;
  if isnan(ret.refractive_index_defect)
    if ret.defect_properties.defect_found
      ret.refractive_index_defect = sqrt(ret.defect_properties.object.permittivity);
    else
      ret.refractive_index_defect = 1;
    end
  end
  disp_and_log([stdout_fid, logfile_fid], 'Setting ret.refractive_index_defect = %f ( permittivity = %f )', ret.refractive_index_defect, ret.refractive_index_defect^2);
  
  % load epsilon lookup table if provided
  if p.Results.epsilon_lookup_table
    [TABLE_header, TABLE] = readPrnFile(p.Results.epsilon_lookup_table, 'verbosity', p.Results.verbosity);
  end

  % log some stuff
  disp_and_log([stdout_fid, logfile_fid], sprintf('fsnap_folder = %s', p.Results.fsnap_folder));
  disp_and_log([stdout_fid, logfile_fid], sprintf('eps_folder = %s', p.Results.eps_folder));
  disp_and_log([stdout_fid, logfile_fid], sprintf('snap_plane = %s', p.Results.snap_plane));
  
  % convert snap_plane='x','y','z' to 1,2,3
  snapDirInt = (p.Results.snap_plane - double('x')) + 1;

  % read the input files
  [ structured_entries, inpEntries ] = readBristolFDTD(inpfile_list);
  probe_ident = structured_entries.flag.id;
  ret.box = structured_entries.box;
  
  snap_time_number = p.Results.snap_time_number;

  Snaps = {};
  % TODO: Select snapshots by "name" in case there are non-mode-volume related snapshots. -> to be superseded by eventual new input format/objects?
  % TODO: Store values from snapshot on grid. Makes previous TODO unnecessary and general mode volume computations much easier. (.h5,.vts,.vtu formats)

  % define default numID_list if it is undefined or empty
  numID_list = p.Results.numID_list;
  if length(numID_list) == 0
    numID_list = 1:length(structured_entries.epsilon_snapshots);
  end
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %%%%% Get the necessary filenames, etc
  
  % We have to go through all snapshots since the "numbering/indexing" goes over X, Y and Z.
  for numID_esnap = 1:length(structured_entries.epsilon_snapshots)
    % if numID_esnap is in numID_list
    if length(find(numID_esnap==numID_list)) > 0
      esnap = structured_entries.epsilon_snapshots(numID_esnap);
      if esnap.plane == snapDirInt
        
        % This is for "multimode support", i.e. when more than 1 frequency was used for each frequency snapshot,
        % leading to N(epsilon snapshots)*N(mode frequencies) frequency snapshots in total.
        % numID_fsnap will be the freq_snap idx corresponding to the eps_snap idx numID_esnap.
        % p.Results.Nmodes = number of modes
        % p.Results.mode_index = mode we want to calculate the MV for
        % 1 <= numID_esnap <= N(epsilon snapshots)
        % 1 <= p.Results.mode_index <= N(mode frequencies)
        numID_fsnap = p.Results.mode_index + (numID_esnap-1)*p.Results.Nmodes;
        
        fsnap_frequency = structured_entries.frequency_snapshots(numID_fsnap).frequency;
        first = structured_entries.frequency_snapshots(numID_fsnap).first;
        repetition = structured_entries.frequency_snapshots(numID_fsnap).repetition;
        
        [ esnap_filename, esnap_alphaID, esnap_pair ] = numID_to_alphaID_TimeSnapshot(numID_esnap, p.Results.snap_plane, probe_ident, 1);

        % if snap_time_number has not been specified, we try to use the biggest working one.
        % TODO: URGENT: this should be outside the loop! Otherwise varying snap_time_number could be used!!!
        if isnan(snap_time_number)
          [ fsnap_filename, fsnap_alphaID, fsnap_pair ] = numID_to_alphaID_FrequencySnapshot(numID_fsnap, 'snap_plane', p.Results.snap_plane, 'probe_ident', probe_ident, 'snap_time_number', 0, 'pre_2008_BFDTD_version', p.Results.pre_2008_BFDTD_version);
          prefix = [p.Results.snap_plane, fsnap_alphaID, probe_ident];
          snap_time_number = getLastSnapTimeNumber(p.Results.fsnap_folder, prefix, 'probe_ident', probe_ident, 'pre_2008_BFDTD_version', p.Results.pre_2008_BFDTD_version);
          if snap_time_number < 0
            error(['Failed to automatically determine snap_time_number, most likely due to missing .prn files in fsnap_folder = "', p.Results.fsnap_folder, '"']);
          end
        end
        [ fsnap_filename, fsnap_alphaID, fsnap_pair ] = numID_to_alphaID_FrequencySnapshot(numID_fsnap, 'snap_plane', p.Results.snap_plane, 'probe_ident', probe_ident, 'snap_time_number', snap_time_number, 'pre_2008_BFDTD_version', p.Results.pre_2008_BFDTD_version);

        % Storing a ridiculous amount of info. TODO: fix?
        SnapEntry.pos = esnap.P2(esnap.plane); % NOTE: TODO: Why P2 instead of P1? What happens when P1[plane]!=P2[plane]?
        SnapEntry.epsFile = fullfile(p.Results.eps_folder, esnap_filename);
        SnapEntry.fsnapFile = fullfile(p.Results.fsnap_folder, fsnap_filename);
        SnapEntry.numID_esnap = numID_esnap;
        SnapEntry.numID_fsnap = numID_fsnap;
        SnapEntry.fsnap_frequency = fsnap_frequency;
        SnapEntry.first = first;
        SnapEntry.repetition = repetition;
        Snaps{end+1} = SnapEntry;
        
        if p.Results.justCheck
          disp_and_log([stdout_fid, logfile_fid], 'SnapEntry.pos = %f, esnap_filename = %s, fsnap_filename = %s, numID_esnap = %d, numID_fsnap = %d', SnapEntry.pos, esnap_filename, fsnap_filename, numID_esnap, numID_fsnap);
          if exist(SnapEntry.epsFile, 'file') == 0
            disp_and_log([stdout_fid, logfile_fid], 'WARNING: %s not found.', SnapEntry.epsFile);
            ret.allFilesFound = false;
          end
          if exist(SnapEntry.fsnapFile, 'file') == 0
            disp_and_log([stdout_fid, logfile_fid], 'WARNING: %s not found.', SnapEntry.fsnapFile);
            ret.allFilesFound = false;
          end
        end
        
      end
    end
  end
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %%%%% more preliminary ops
  
  if p.Results.justCheck
    disp_and_log([stdout_fid, logfile_fid], 'length(Snaps) = %d', length(Snaps));
    if logfile_fid >= 0
      fclose(logfile_fid);
    end
    return
  end
  
  if isempty(Snaps)
    error('No epsilon snapshots found in the snap_plane = %s direction. The input .inp files must provide both epsilon and frequency snapshots to be used to calculate the mode volume. Also check the value of the snap_plane argument.', p.Results.snap_plane);
  end
  
  mesh{1} = structured_entries.xmesh;
  mesh{2} = structured_entries.ymesh;
  mesh{3} = structured_entries.zmesh;

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %%%%% calculate the mode volume, preliminary ops
  
  % maximum energy density structure
  ret.MaximumEnergyDensity.value = -Inf; % to make sure we find a maximum, even if it is negative
  ret.MaximumEnergyDensity.epsilon = NaN;
  ret.MaximumEnergyDensity.Exmod = NaN;
  ret.MaximumEnergyDensity.Eymod = NaN;
  ret.MaximumEnergyDensity.Ezmod = NaN;
  ret.MaximumEnergyDensity.plane_index = NaN;
  ret.MaximumEnergyDensity.column_1_index = NaN;
  ret.MaximumEnergyDensity.column_2_index = NaN;
  ret.MaximumEnergyDensity.x = NaN;
  ret.MaximumEnergyDensity.y = NaN;
  ret.MaximumEnergyDensity.z = NaN;

  % maximum E2 structure
  ret.MaximumE2.value = -Inf; % to make sure we find a maximum, even if it is negative
  ret.MaximumE2.epsilon = NaN;
  ret.MaximumE2.Exmod = NaN;
  ret.MaximumE2.Eymod = NaN;
  ret.MaximumE2.Ezmod = NaN;
  ret.MaximumE2.plane_index = NaN;
  ret.MaximumE2.column_1_index = NaN;
  ret.MaximumE2.column_2_index = NaN;
  ret.MaximumE2.x = NaN;
  ret.MaximumE2.y = NaN;
  ret.MaximumE2.z = NaN;
  
  TotalEnergy = 0;
  TotalE2V = 0;
  TotalVolume = 0;
  
  m_max = length(Snaps);
  ret.Nsnapshots = m_max;
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %%%%% calculate the mode volume, main loop
  
  for m = 1:m_max
    % print progress info
    disp_and_log([stdout_fid, logfile_fid], 'm = %d/%d', m, m_max);
    disp_and_log([stdout_fid, logfile_fid], 'SnapEntry.pos = %f, esnap_filename = %s, fsnap_filename = %s, numID_esnap = %d, numID_fsnap = %d', Snaps{m}.pos, Snaps{m}.epsFile, Snaps{m}.fsnapFile, Snaps{m}.numID_esnap, Snaps{m}.numID_fsnap);
    
    % skip snapshots which are outside selected integration region
    if integration_sphere_radius >= 0
      if strcmp(p.Results.snap_plane,'x')
        % k->plane->x, j->col1->y, i->col2->z
        mindist = abs(Snaps{m}.pos - integration_sphere_centre(1));
      elseif strcmp(p.Results.snap_plane,'y')
        % k->plane->y, j->col1->x, i->col2->z
        mindist = abs(Snaps{m}.pos - integration_sphere_centre(2));
      else
        % k->plane->z, j->col1->x, i->col2->y
        mindist = abs(Snaps{m}.pos - integration_sphere_centre(3));
      end
      if mindist > integration_sphere_radius
        disp_and_log([stdout_fid, logfile_fid], 'Snapshot plane outside integration region. Skipping.');
        continue;
      end
    end
    
    % read in data
    [header_esnap, data_esnap, column_1_esnap, column_2_esnap] = readPrnFile(Snaps{m}.epsFile, 'verbosity', p.Results.verbosity);
    [header_fsnap, data_fsnap, ui_fsnap, uj_fsnap] = readPrnFile(Snaps{m}.fsnapFile, 'verbosity', p.Results.verbosity);
    
    %%% apply data modifiers
    
    % data modifier: lookup table
    % TODO: to be improved later using interp1* functions (for less discrete epsilon distributions, like in MEEP/MPB output), in which case two data_esnap arrays need to be created depending on usage (mask creation and value array).
    if p.Results.epsilon_lookup_table
      %data_esnap = lookup_in_table(TABLE, data_esnap);
      data_esnap = interp1Custom(TABLE(:,1), TABLE(:,2), data_esnap, 'nearest', 'extrap');
    end
    
    % data modifier: defect from geofile and refractive_index_defect
    if ret.defect_properties.defect_found && ~isnan(p.Results.refractive_index_defect)
      data_esnap = setPermittivityInObject(data_esnap, p.Results.snap_plane, p.Results.refractive_index_defect^2, ret.defect_properties);
    end
    
    % debug info
    if p.Results.verbosity > 5
      disp_and_log([stdout_fid, logfile_fid], ['==> size(data_fsnap) = ',num2str(size(data_fsnap))]);
      disp_and_log([stdout_fid, logfile_fid], ['==> size(ui_fsnap) = ',num2str(size(ui_fsnap))]);
      disp_and_log([stdout_fid, logfile_fid], ['==> size(uj_fsnap) = ',num2str(size(uj_fsnap))]);
      
      disp_and_log([stdout_fid, logfile_fid], ['==> size(data_esnap) = ',num2str(size(data_esnap))]);
      disp_and_log([stdout_fid, logfile_fid], ['==> size(column_1_esnap) = ',num2str(size(column_1_esnap))]);
      disp_and_log([stdout_fid, logfile_fid], ['==> size(column_2_esnap) = ',num2str(size(column_2_esnap))]);
    end
    
    if length(Snaps) <= 1
      disp_and_log([stdout_fid, logfile_fid], 'WARNING: You are only using one snapshot!!! setting thickness = 1');
      thickness = 1;
    else
      % TODO: Fix this hack. Causes problems at "edges" and is problematic if snapshots are not in the correct order.
      if p.Results.incorrectAlgorithm_bool
        if m == length(Snaps)
          thickness = abs(Snaps{m}.pos-Snaps{m-1}.pos);
        else
          thickness = abs(Snaps{m+1}.pos-Snaps{m}.pos);
        end
      else
        if m == 1
          thickness = (Snaps{2}.pos - Snaps{1}.pos)/2;
        elseif m == m_max
          thickness = (Snaps{m_max}.pos - Snaps{m_max-1}.pos)/2;        
        else
          thickness = (Snaps{m+1}.pos - Snaps{m-1}.pos)/2;
        end
      end
    end
    
    if thickness <= 0
      error(['Negative thickness found: thickness = ', num2str(thickness), ' Please check the order of your snapshots. Unordered snapshots not yet supported.']);
    end
    
    if p.Results.incorrectAlgorithm_bool
      % get indices which vary in a plane, i.e. the columns in a .prn file
      v = 1:3;
      ind = find(v~=snapDirInt);
      
      %length(column_1_esnap)
      %length(mesh{ind(1)})
      
      %length(column_2_esnap)
      %length(mesh{ind(2)})
      
      %size(data_fsnap)
      %size(data_esnap)
      
      % WIP: data_e/fsnap should only be defined once, after vi,vj have been defined. Fix this mess for clarity and robustness.
      % we should always take a "forward diff" -> requires adding missing mesh line
      % The "mesh" variables are already "diffs", i.e. list of cell sizes.
      if( length(column_1_esnap) == length(mesh{ind(1)}) ) % happens if full or bottom-left snapshot is taken
        % full snapshot
        vi = mesh{ind(1)};
        error('Full snapshot not supported with incorrect algorithm?');
      else
        % partial snapshot
        vi = diff(column_1_esnap);
        data_fsnap = data_fsnap(1:end-1, :, :);
        data_esnap = data_esnap(1:end-1, :, :);
      end
      
      if( length(column_2_esnap) == length(mesh{ind(2)}) ) % happens if full or bottom-left snapshot is taken
        % full snapshot
        vj = mesh{ind(2)};
        error('Full snapshot not supported with incorrect algorithm?');
      else
        % partial snapshot
        vj = diff(column_2_esnap);
        data_fsnap = data_fsnap(:, 1:end-1, :);
        data_esnap = data_esnap(:, 1:end-1, :);
      end
    else
      vi = [(column_1_esnap(2) - column_1_esnap(1))/2; (column_1_esnap(3:end) - column_1_esnap(1:end-2))/2; (column_1_esnap(end) - column_1_esnap(end-1))/2];
      vj = [(column_2_esnap(2) - column_2_esnap(1))/2; (column_2_esnap(3:end) - column_2_esnap(1:end-2))/2; (column_2_esnap(end) - column_2_esnap(end-1))/2];
    end
    
    %size(vi) % N1,1
    %size(vj) % N2,1
    
    areaM = vj*vi'; % N2,1 * 1,N1 = N2,N1
    
    % TODO: multiply by a binary matrix defining points inside sphere or other volume restriction
    integration_region = ones(size(areaM));
    if integration_sphere_radius >= 0
      for column_1_index = 1:length(column_1_esnap)
        for column_2_index = 1:length(column_2_esnap)
          if strcmp(p.Results.snap_plane,'x')
            % k->plane->x, j->col1->y, i->col2->z
            x = Snaps{m}.pos;
            y = column_1_esnap(column_1_index);
            z = column_2_esnap(column_2_index);
          elseif strcmp(p.Results.snap_plane,'y')
            % k->plane->y, j->col1->x, i->col2->z
            x = column_1_esnap(column_1_index);
            y = Snaps{m}.pos;
            z = column_2_esnap(column_2_index);
          else
            % k->plane->z, j->col1->x, i->col2->y
            x = column_1_esnap(column_1_index);
            y = column_2_esnap(column_2_index);
            z = Snaps{m}.pos;
          end
          if p.Results.norm_function([x,y,z] - integration_sphere_centre) > integration_sphere_radius
            integration_region(column_2_index, column_1_index) = 0;
          end
        end
      end
    end
    
    %size(areaM)
    %size(data_fsnap)
    %size(data_esnap)
    
    %vi = diff(column_1_esnap);
    %vj = diff(column_2_esnap);
    
    %vi = mesh{ind(1)};
    %vj = mesh{ind(2)};
    
    %disp_and_log([stdout_fid, logfile_fid], ['==> size(vi) = ',num2str(size(vi))]);
    %disp_and_log([stdout_fid, logfile_fid], ['==> size(vj) = ',num2str(size(vj))]);
    
    Exmod = data_fsnap(:,:,1);
    Eymod = data_fsnap(:,:,4);
    Ezmod = data_fsnap(:,:,7);
    
    E2 = (Exmod.^2+Eymod.^2+Ezmod.^2).*integration_region;
    energy_density = data_esnap.*E2;
    
    % hack for old incorrect system
    if p.Results.incorrectAlgorithm_bool
      [local_maximum_energy_density, local_maximum_energy_density_idx] = max(sum(sum(energy_density)));
      [local_maximum_E2, local_maximum_E2_idx] = max(sum(sum(E2)));
    else
      % values and indices of the maximum energy point in the current plane
      [local_maximum_energy_density, local_maximum_energy_density_idx] = max(energy_density(:));
      [local_maximum_E2, local_maximum_E2_idx] = max(E2(:));
    end
    
    %local_maximum_energy_density_all_indices = find(energy_density(:)==local_maximum_energy_density);
    %local_maximum_energy_density_list = [local_maximum_energy_density_list, local_maximum_energy_density];
    
    % TODO: another ugly complex bit, which would be a lot easier if conversion to a 3D matrix was done first...
    if ( local_maximum_energy_density > ret.MaximumEnergyDensity.value )
      ret.MaximumEnergyDensity.value = local_maximum_energy_density;
      [I, J] = ind2sub(size(energy_density), local_maximum_energy_density_idx);
      ret.MaximumEnergyDensity.plane_index = m;
      ret.MaximumEnergyDensity.column_1_index = J;
      ret.MaximumEnergyDensity.column_2_index = I;
      if strcmp(p.Results.snap_plane,'x')
        % k->plane->x, j->col1->y, i->col2->z
        ret.MaximumEnergyDensity.x = Snaps{m}.pos;
        ret.MaximumEnergyDensity.y = column_1_esnap(ret.MaximumEnergyDensity.column_1_index);
        ret.MaximumEnergyDensity.z = column_2_esnap(ret.MaximumEnergyDensity.column_2_index);
      elseif strcmp(p.Results.snap_plane,'y')
        % k->plane->y, j->col1->x, i->col2->z
        ret.MaximumEnergyDensity.x = column_1_esnap(ret.MaximumEnergyDensity.column_1_index);
        ret.MaximumEnergyDensity.y = Snaps{m}.pos;
        ret.MaximumEnergyDensity.z = column_2_esnap(ret.MaximumEnergyDensity.column_2_index);
      else
        % k->plane->z, j->col1->x, i->col2->y
        ret.MaximumEnergyDensity.x = column_1_esnap(ret.MaximumEnergyDensity.column_1_index);
        ret.MaximumEnergyDensity.y = column_2_esnap(ret.MaximumEnergyDensity.column_2_index);
        ret.MaximumEnergyDensity.z = Snaps{m}.pos;
      end
      ret.MaximumEnergyDensity.epsilon = data_esnap(I,J);
      ret.MaximumEnergyDensity.Exmod = Exmod(I,J);
      ret.MaximumEnergyDensity.Eymod = Eymod(I,J);
      ret.MaximumEnergyDensity.Ezmod = Ezmod(I,J);
    end

    if ( local_maximum_E2 > ret.MaximumE2.value )
      ret.MaximumE2.value = local_maximum_E2;
      [I, J] = ind2sub(size(E2), local_maximum_E2_idx);
      ret.MaximumE2.plane_index = m;
      ret.MaximumE2.column_1_index = J;
      ret.MaximumE2.column_2_index = I;
      if strcmp(p.Results.snap_plane,'x')
        % k->plane->x, j->col1->y, i->col2->z
        ret.MaximumE2.x = Snaps{m}.pos;
        ret.MaximumE2.y = column_1_esnap(ret.MaximumE2.column_1_index);
        ret.MaximumE2.z = column_2_esnap(ret.MaximumE2.column_2_index);
      elseif strcmp(p.Results.snap_plane,'y')
        % k->plane->y, j->col1->x, i->col2->z
        ret.MaximumE2.x = column_1_esnap(ret.MaximumE2.column_1_index);
        ret.MaximumE2.y = Snaps{m}.pos;
        ret.MaximumE2.z = column_2_esnap(ret.MaximumE2.column_2_index);
      else
        % k->plane->z, j->col1->x, i->col2->y
        ret.MaximumE2.x = column_1_esnap(ret.MaximumE2.column_1_index);
        ret.MaximumE2.y = column_2_esnap(ret.MaximumE2.column_2_index);
        ret.MaximumE2.z = Snaps{m}.pos;
      end
      ret.MaximumE2.epsilon = data_esnap(I,J);
      ret.MaximumE2.Exmod = Exmod(I,J);
      ret.MaximumE2.Eymod = Eymod(I,J);
      ret.MaximumE2.Ezmod = Ezmod(I,J);
    end
    
    %disp_and_log([stdout_fid, logfile_fid], ['==> size(energy_density) = ',num2str(size(energy_density))]);
    %disp_and_log([stdout_fid, logfile_fid], ['==> size(areaM) = ',num2str(size(areaM))]);
    %disp_and_log([stdout_fid, logfile_fid], ['==> size(thickness) = ',num2str(size(thickness))]);
    
    current_TotalEnergy = sum(sum(energy_density.*areaM*thickness));
    current_TotalE2V = sum(sum(E2.*areaM*thickness));
    current_TotalVolume = sum(sum(integration_region.*areaM*thickness));
    
    % hack for old incorrect system
    %if p.Results.incorrectAlgorithm_bool
      %current_TotalEnergy = current_TotalEnergy/local_maximum_energy_density;
    %end
    
    TotalEnergy = TotalEnergy + current_TotalEnergy;
    TotalE2V = TotalE2V + current_TotalE2V;
    TotalVolume = TotalVolume + current_TotalVolume;
    
    % per-material handling
    unique_epsilon_list = unique(data_esnap);
    for eps_idx = 1:length(unique_epsilon_list)
      eps_val = unique_epsilon_list(eps_idx);
      eps_match_idx = find(ret.materials.epsilon == eps_val);
      if length(eps_match_idx) > 1; error('error in epsilon list building'); end;
      if isempty(eps_match_idx)
        ret.materials.epsilon(end+1) = eps_val;
        ret.materials.energy(end+1) = 0;
        ret.materials.volume(end+1) = 0;
        eps_match_idx = length(ret.materials.epsilon);
      end
      eps_mask = data_esnap == eps_val; % TODO: to be improved later using lookup_in_table and/or interp1* functions (for less discrete epsilon distributions, like in MEEP/MPB output)
      ret.materials.energy(eps_match_idx) = ret.materials.energy(eps_match_idx) + sum(sum(eps_mask.*energy_density.*areaM*thickness));
      ret.materials.volume(eps_match_idx) = ret.materials.volume(eps_match_idx) + sum(sum(eps_mask.*integration_region.*areaM*thickness));
    end
    
    % TODO: defect handling
    
  end
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %%%%% set return values
  
  % hack for half-sims
  if p.Results.is_half_sim
    ret.TotalEnergy = 2*TotalEnergy;
    ret.TotalE2V = 2*TotalE2V;
    ret.TotalVolume = 2*TotalVolume;
  else
    ret.TotalEnergy = TotalEnergy;
    ret.TotalE2V = TotalE2V;
    ret.TotalVolume = TotalVolume;
  end

  % misc assignments
  ret.first = Snaps{1}.first;
  ret.snap_time_number = snap_time_number;
  ret.repetition = Snaps{1}.repetition;
  ret.Niterations = ret.first + ret.snap_time_number*ret.repetition;
  ret.f0_MHz = Snaps{1}.fsnap_frequency;
  ret.Lambda_mum = get_c0()/ret.f0_MHz;
    
  % sim size from box
  size_x_box = ret.box.upper(1) - ret.box.lower(1);
  size_y_box = ret.box.upper(2) - ret.box.lower(2);
  size_z_box = ret.box.upper(3) - ret.box.lower(3);

  % sim size from mesh
  size_x_mesh = sum(structured_entries.xmesh);
  size_y_mesh = sum(structured_entries.ymesh);
  size_z_mesh = sum(structured_entries.zmesh);

  % create MV info structures
  %MV_MaximumEnergyDensity = ret.TotalEnergy / ret.MaximumEnergyDensity.value;
  %MV_MaximumE2 = ret.TotalEnergy / ( ret.MaximumE2.epsilon * ret.MaximumE2.value );
  
  ret.MV_MaximumEnergyDensity_nfixed = createMVstruct(ret.TotalEnergy, ret.MaximumEnergyDensity.value, ret.Lambda_mum, ret.refractive_index_defect);
  ret.MV_MaximumEnergyDensity_nlocal = createMVstruct(ret.TotalEnergy, ret.MaximumEnergyDensity.value, ret.Lambda_mum, sqrt(ret.MaximumEnergyDensity.epsilon));
  ret.MV_MaximumE2_nfixed = createMVstruct(ret.TotalEnergy, ( ret.MaximumE2.epsilon * ret.MaximumE2.value ), ret.Lambda_mum, ret.refractive_index_defect);
  ret.MV_MaximumE2_nlocal = createMVstruct(ret.TotalEnergy, ( ret.MaximumE2.epsilon * ret.MaximumE2.value ), ret.Lambda_mum, sqrt(ret.MaximumE2.epsilon));
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %%%%% output info
  
  % incorrect algorithm warning
  disp_and_log([stdout_fid, logfile_fid], '');
  if p.Results.incorrectAlgorithm_bool
    disp_and_log([stdout_fid, logfile_fid], 'WARNING: Incorrect algorithm used!!!' );
    disp_and_log([stdout_fid, logfile_fid], '');
  end
  
  % main output
  disp_and_log([stdout_fid, logfile_fid], ['General info:']);
  
  disp_and_log([stdout_fid, logfile_fid], ['  incorrectAlgorithm_bool = ', num2str(p.Results.incorrectAlgorithm_bool)]);
  disp_and_log([stdout_fid, logfile_fid], ['  Nsnapshots = ', num2str(ret.Nsnapshots)]);
  disp_and_log([stdout_fid, logfile_fid], ['  epsilon_lookup_table = ', p.Results.epsilon_lookup_table]);
  
  disp_and_log([stdout_fid, logfile_fid], sprintf('  Niterations = %d + %d*%d = %d', ret.first, ret.snap_time_number, ret.repetition, ret.Niterations) );
  disp_and_log([stdout_fid, logfile_fid], ['  f0_MHz = ', num2str(ret.f0_MHz)]);
  disp_and_log([stdout_fid, logfile_fid], ['  Lambda_mum = ', num2str(ret.Lambda_mum)]);
  disp_and_log([stdout_fid, logfile_fid], ['  refractive_index_defect = ', num2str(ret.refractive_index_defect)]);
  disp_and_log([stdout_fid, logfile_fid], ['  TotalEnergy = ', num2str(ret.TotalEnergy)]);
  disp_and_log([stdout_fid, logfile_fid], ['  TotalE2V = ', num2str(ret.TotalE2V)]);
  disp_and_log([stdout_fid, logfile_fid], ['MaximumEnergyDensity:']);
  disp_and_log([stdout_fid, logfile_fid], ['  value = ', num2str(ret.MaximumEnergyDensity.value)]);
  disp_and_log([stdout_fid, logfile_fid], ['  epsilon = ', num2str(ret.MaximumEnergyDensity.epsilon)]);
  disp_and_log([stdout_fid, logfile_fid], ['  Exmod = ', num2str(ret.MaximumEnergyDensity.Exmod)]);
  disp_and_log([stdout_fid, logfile_fid], ['  Eymod = ', num2str(ret.MaximumEnergyDensity.Eymod)]);
  disp_and_log([stdout_fid, logfile_fid], ['  Ezmod = ', num2str(ret.MaximumEnergyDensity.Ezmod)]);
  disp_and_log([stdout_fid, logfile_fid], ['  plane_index = ', num2str(ret.MaximumEnergyDensity.plane_index)]);
  disp_and_log([stdout_fid, logfile_fid], ['  column_1_index = ', num2str(ret.MaximumEnergyDensity.column_1_index)]);
  disp_and_log([stdout_fid, logfile_fid], ['  column_2_index = ', num2str(ret.MaximumEnergyDensity.column_2_index)]);
  disp_and_log([stdout_fid, logfile_fid], ['  x (mum) = ', num2str(ret.MaximumEnergyDensity.x)]);
  disp_and_log([stdout_fid, logfile_fid], ['  y (mum) = ', num2str(ret.MaximumEnergyDensity.y)]);
  disp_and_log([stdout_fid, logfile_fid], ['  z (mum) = ', num2str(ret.MaximumEnergyDensity.z)]);
  disp_and_log([stdout_fid, logfile_fid], ['  x/size_x_mesh = ', num2str(ret.MaximumEnergyDensity.x/size_x_mesh)]);
  disp_and_log([stdout_fid, logfile_fid], ['  y/size_y_mesh = ', num2str(ret.MaximumEnergyDensity.y/size_y_mesh)]);
  disp_and_log([stdout_fid, logfile_fid], ['  z/size_z_mesh = ', num2str(ret.MaximumEnergyDensity.z/size_z_mesh)]);
  disp_and_log([stdout_fid, logfile_fid], ['MaximumE2:']);
  disp_and_log([stdout_fid, logfile_fid], ['  value = ', num2str(ret.MaximumE2.value)]);
  disp_and_log([stdout_fid, logfile_fid], ['  epsilon = ', num2str(ret.MaximumE2.epsilon)]);
  disp_and_log([stdout_fid, logfile_fid], ['  Exmod = ', num2str(ret.MaximumE2.Exmod)]);
  disp_and_log([stdout_fid, logfile_fid], ['  Eymod = ', num2str(ret.MaximumE2.Eymod)]);
  disp_and_log([stdout_fid, logfile_fid], ['  Ezmod = ', num2str(ret.MaximumE2.Ezmod)]);
  disp_and_log([stdout_fid, logfile_fid], ['  plane_index = ', num2str(ret.MaximumE2.plane_index)]);
  disp_and_log([stdout_fid, logfile_fid], ['  column_1_index = ', num2str(ret.MaximumE2.column_1_index)]);
  disp_and_log([stdout_fid, logfile_fid], ['  column_2_index = ', num2str(ret.MaximumE2.column_2_index)]);
  disp_and_log([stdout_fid, logfile_fid], ['  x (mum) = ', num2str(ret.MaximumE2.x)]);
  disp_and_log([stdout_fid, logfile_fid], ['  y (mum) = ', num2str(ret.MaximumE2.y)]);
  disp_and_log([stdout_fid, logfile_fid], ['  z (mum) = ', num2str(ret.MaximumE2.z)]);
  disp_and_log([stdout_fid, logfile_fid], ['  x/size_x_mesh = ', num2str(ret.MaximumE2.x/size_x_mesh)]);
  disp_and_log([stdout_fid, logfile_fid], ['  y/size_y_mesh = ', num2str(ret.MaximumE2.y/size_y_mesh)]);
  disp_and_log([stdout_fid, logfile_fid], ['  z/size_z_mesh = ', num2str(ret.MaximumE2.z/size_z_mesh)]);
  disp_and_log([stdout_fid, logfile_fid], ['Box size, based on box (Only valid if you read in a .geo file defining it.):']);
  disp_and_log([stdout_fid, logfile_fid], ['  size_x_box (mum) = ', num2str(size_x_box)]);
  disp_and_log([stdout_fid, logfile_fid], ['  size_y_box (mum) = ', num2str(size_y_box)]);
  disp_and_log([stdout_fid, logfile_fid], ['  size_z_box (mum) = ', num2str(size_z_box)]);
  disp_and_log([stdout_fid, logfile_fid], ['Box size, based on mesh:']);
  disp_and_log([stdout_fid, logfile_fid], ['  size_x_mesh (mum) = ', num2str(size_x_mesh)]);
  disp_and_log([stdout_fid, logfile_fid], ['  size_y_mesh (mum) = ', num2str(size_y_mesh)]);
  disp_and_log([stdout_fid, logfile_fid], ['  size_z_mesh (mum) = ', num2str(size_z_mesh)]);
  disp_and_log([stdout_fid, logfile_fid], ['Volumes:']);
  disp_and_log([stdout_fid, logfile_fid], '  Box volume (mum^3) = size_x_box*size_y_box*size_z_box = %f', size_x_box*size_y_box*size_z_box);
  disp_and_log([stdout_fid, logfile_fid], '  Box volume (mum^3) = size_x_mesh*size_y_mesh*size_z_mesh = %f', size_x_mesh*size_y_mesh*size_z_mesh);
  disp_and_log([stdout_fid, logfile_fid], '  Integration volume (mum^3) = TotalVolume = %f', ret.TotalVolume);

  disp_and_log([stdout_fid, logfile_fid], ['Material information:']);
  for eps_idx = 1:length(ret.materials.epsilon)
    disp_and_log([stdout_fid, logfile_fid], '  epsilon = %.4f <=> index = %.2f', ret.materials.epsilon(eps_idx), sqrt(ret.materials.epsilon(eps_idx)));
    disp_and_log([stdout_fid, logfile_fid], '    volume (mum^3) = %f = %.2f %% of total volume', ret.materials.volume(eps_idx), 100*ret.materials.volume(eps_idx)/ret.TotalVolume);
    disp_and_log([stdout_fid, logfile_fid], '    energy (J) = %f = %.2f %% of total energy', ret.materials.energy(eps_idx), 100*ret.materials.energy(eps_idx)/ret.TotalEnergy);
  end

  disp_and_log([stdout_fid, logfile_fid], ['Defect information:']);
  if ret.defect_properties.defect_found
    disp_and_log([stdout_fid, logfile_fid], ['  Original info from geofile = %s :'], p.Results.geofile);
    disp_and_log([stdout_fid, logfile_fid], ret.defect_properties.printInfo('    '));
    disp_and_log([stdout_fid, logfile_fid], ['  Volume and energy information (using new refractive_index_defect if specified):']);
    %disp_and_log([stdout_fid, logfile_fid], '  epsilon = %.4f <=> index = %.2f', ret.defect.epsilon, sqrt(ret.defect.epsilon));
    %disp_and_log([stdout_fid, logfile_fid], '    volume (mum^3) = %f = %.2f %% of total volume', ret.defect.volume, 100*ret.defect.volume/ret.TotalVolume);
    %disp_and_log([stdout_fid, logfile_fid], '    energy (J) = %f = %.2f %% of total energy', ret.defect.energy, 100*ret.defect.energy/ret.TotalEnergy);
  else
    disp_and_log([stdout_fid, logfile_fid], ['  defect not found']);
  end
  
  disp_and_log([stdout_fid, logfile_fid], ['Mode volume information:']);
  disp_and_log([stdout_fid, logfile_fid], ['  Mode volume using max(EnergyDensity) and fixed refractive index:']);
  dispMVstruct([stdout_fid, logfile_fid], ret.MV_MaximumEnergyDensity_nfixed, '    ');
  disp_and_log([stdout_fid, logfile_fid], ['  Mode volume using max(EnergyDensity) and local refractive index:']);
  dispMVstruct([stdout_fid, logfile_fid], ret.MV_MaximumEnergyDensity_nlocal, '    ');
  disp_and_log([stdout_fid, logfile_fid], ['  Mode volume using max(E^2) and fixed refractive index:']);
  dispMVstruct([stdout_fid, logfile_fid], ret.MV_MaximumE2_nfixed, '    ');
  disp_and_log([stdout_fid, logfile_fid], ['  Mode volume using max(E^2) and local refractive index:']);
  dispMVstruct([stdout_fid, logfile_fid], ret.MV_MaximumE2_nlocal, '    ');
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %%%%% final pre-return operations
  
  % close logfile
  if logfile_fid >= 0
    fclose(logfile_fid);
  end

  % Save the return structure too for easier data re-use. Other formats could be added later if needed.
  if p.Results.logfile_bool
    % quick hack to save ret
    %saveable_ret = ret;
    %saveable_ret.custom_function = 'cannot be saved';
    saveable_ret = rmfield(ret, 'custom_function');
    save([logfile, '.struct'], 'saveable_ret');
    %save('-mat7-binary', [logfile, '.struct'], 'saveable_ret');
    %save('-ascii', [logfile, '.struct'], 'saveable_ret');
  end
  
  % change back to original dir
  cd(ORIGDIR);

end
