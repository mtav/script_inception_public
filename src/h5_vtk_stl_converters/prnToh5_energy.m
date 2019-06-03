function epsilon = prnToh5_energy(inpfile_list, h5file, varargin)
  % .prn to .h5 prototype. Use at your own risk.

  % create parser
  p = inputParser();
  p = inputParserWrapper(p, 'addRequired', 'inpfile_list', @iscellstr);
  p = inputParserWrapper(p, 'addRequired', 'h5file', @ischar);
  %p = inputParserWrapper(p, 'addParamValue', 'fsnap_folder', '.', @isdir);
  %p = inputParserWrapper(p, 'addParamValue', 'eps_folder', '.', @isdir);
  %p = inputParserWrapper(p, 'addParamValue', 'snap_time_number', NaN, @isnumeric); % if not given, we use getLastSnapTimeNumber()
  %p = inputParserWrapper(p, 'addParamValue', 'refractive_index_defect', NaN, @isnumeric); % if not defined, we simply don't calculate the normalized mode volume
  %p = inputParserWrapper(p, 'addParamValue', 'is_half_sim', false, @islogical);
  %p = inputParserWrapper(p, 'addParamValue', 'numID_list', [], @isnumeric);
  %p = inputParserWrapper(p, 'addParamValue', 'justCheck', false, @islogical);
  %p = inputParserWrapper(p, 'addParamValue', 'BFDTD_version', '2013', @(x) any(validatestring(x, {'2003','2008','2013'})));
  %p = inputParserWrapper(p, 'addParamValue', 'mode_index', 1, @isnumeric);
  
  p = inputParserWrapper(p, 'addParamValue', 'snap_plane', 'auto', @(x) any(validatestring(x, {'x','y','z','auto'})));
  p = inputParserWrapper(p, 'parse', inpfile_list, h5file, varargin{:});

  p.Results

  % read BFDTD input files
  [inpEntries, structured_entries] = GEO_INP_reader(inpfile_list);
  
  % detect slicing direction automatically
  if strcmpi(p.Results.snap_plane, 'auto')
    snap_plane = BFDTD_getSlicingDirection(structured_entries);
  else
    snap_plane = p.Results.snap_plane;
  end

  % convert snap_plane='x','y','z' to 1,2,3
  slicing_direction_index = (snap_plane - double('x')) + 1

  if slicing_direction_index == 1
    Nsnaps = length(structured_entries.epsilon_snapshots_X)
  elseif slicing_direction_index == 2
    Nsnaps = length(structured_entries.epsilon_snapshots_Y)
  else
    Nsnaps = length(structured_entries.epsilon_snapshots_Z)
  end
  
  %return

  % prepare a meshgrid
  xmesh = cumsum(structured_entries.xmesh);
  ymesh = cumsum(structured_entries.ymesh);
  zmesh = cumsum(structured_entries.zmesh);

  %size(structured_entries.xmesh)
  %size(structured_entries.ymesh)
  %size(structured_entries.zmesh)

  [X, Y, Z] = meshgrid(xmesh, ymesh, zmesh);

  %Nsnaps = 51;
  %slicing_direction_index = 3;

  % create arrays to store data from the snapshots
  %size(X)
  %if slicing_direction_index == 2
    %epsilon = zeros(size(X), Nsnaps, size(Z));
    %energy =  zeros(size(X), Nsnaps, size(Z));
  %end

  epsilon = zeros(size(X));
  %energy =  zeros(size(X));

  %epsilon = zeros(200,200,199);
  %energy =  zeros(200,200,199);

  % for manual testing
  %numID = 51;
  %snap_time_number = 1;

  %snap_plane = 'z';
  %id_string = '_id_';
  %id_string = 'a';

  id_string = structured_entries.flag.id
  
  %snap_time_number = p.Results.snap_time_number;

  %% if snap_time_number has not been specified, we try to use the biggest working one.
  %if isnan(snap_time_number)
    %[ fsnap_filename, fsnap_alphaID, fsnap_pair ] = numID_to_alphaID_FrequencySnapshot(numID_fsnap, 'snap_plane', p.Results.snap_plane, 'probe_ident', probe_ident, 'snap_time_number', 0, 'BFDTD_version', p.Results.BFDTD_version);
    %prefix = [p.Results.snap_plane, fsnap_alphaID, probe_ident];
    %snap_time_number = getLastSnapTimeNumber(p.Results.fsnap_folder, prefix, 'probe_ident', probe_ident);
  %end


  for numID = 1:Nsnaps
    % get filenames
    [ esnap, alphaID, pair ] = numID_to_alphaID_TimeSnapshot(numID, snap_plane, id_string, 1);
    %[ fsnap, alphaID, pair ] = numID_to_alphaID_FrequencySnapshot(numID, 'snap_plane', snap_plane, 'probe_ident', id_string, 'snap_time_number', snap_time_number, 'BFDTD_version', '2003');
      
    % read in data
    [esnap_header, esnap_data, esnap_u, esnap_v] = readPrnFile(esnap);
    %[fsnap_header, fsnap_data, fsnap_u, fsnap_v] = readPrnFile(fsnap);
    
    % calculate energy snapshot
    %energy_current = esnap_data.*(fsnap_data(:,:,3).^2 + fsnap_data(:,:,6).^2 + fsnap_data(:,:,9).^2);

    if slicing_direction_index == 1
      % get y position
      %y_current = structured_entries.frequency_snapshots(numID).P1(slicing_direction_index);
      x_current = structured_entries.epsilon_snapshots_X(numID).P1(slicing_direction_index);
      [x_current_closest, x_current_idx] = min(abs(xmesh - x_current));
      
      % put data into the prepared arrays
      size(esnap_data)
      size(epsilon)
      x_current_idx
      epsilon(:, x_current_idx, :) = esnap_data';
      %energy(y_current_idx, :, :) = energy_current';
    elseif slicing_direction_index == 2
      % get y position
      %y_current = structured_entries.frequency_snapshots(numID).P1(slicing_direction_index);
      y_current = structured_entries.epsilon_snapshots_Y(numID).P1(slicing_direction_index);
      [y_current_closest, y_current_idx] = min(abs(ymesh - y_current));
      
      % put data into the prepared arrays
      size(esnap_data)
      size(epsilon)
      y_current_idx
      epsilon(y_current_idx, :, :) = esnap_data';
      %energy(y_current_idx, :, :) = energy_current';
    elseif slicing_direction_index == 3
      % get z position
      %z_current = structured_entries.frequency_snapshots(numID).P1(slicing_direction_index);
      z_current = structured_entries.epsilon_snapshots_Z(numID).P1(slicing_direction_index);
      [z_current_closest, z_current_idx] = min(abs(zmesh-z_current));
      
      % put data into the prepared arrays
      epsilon(:,:,z_current_idx) = esnap_data;
      %energy(:,:,z_current_idx) = energy_current;
    end
    
    % create energy .prn file (not efficient since it reloads data here)
    %createEnergySnapshot(esnap, fsnap, ['energy_', fsnap]);
  end

  % plot in matlab to check before writing to .h5
  figure;

  subplot(1,2,1);
  contourslice(X, Y, Z, epsilon, [xmesh(floor(length(xmesh)/2))],[ymesh(floor(length(ymesh)/2))],[zmesh(floor(length(zmesh)/2))]);
  %colormap hsv;
  colormap jet; colorbar;
  xlabel('x'); ylabel('y'); zlabel('z');

  subplot(1,2,2);
  %contourslice(X, Y, Z, energy, [xmesh(floor(length(xmesh)/2))],[ymesh(floor(length(ymesh)/2))],[zmesh(floor(length(zmesh)/2))]);
  slice(X, Y, Z, epsilon, [xmesh(floor(length(xmesh)/2))],[ymesh(floor(length(ymesh)/2))],[zmesh(floor(length(zmesh)/2))]);
  %colormap hsv;
  colormap jet; colorbar;
  xlabel('x'); ylabel('y'); zlabel('z');

  % create .h5 file
  %h5file='energy.h5';
  %h5file='epsilon.h5';
  
  pwd
  
  h5file = p.Results.h5file
  
  if exist(h5file, 'file')
    h5file_location = which(h5file);
    if isempty(h5file_location)
      h5file_location = GetFullPath(h5file);
    end
    qstring = ['Overwrite ', h5file_location, ' ?']
    choice = questdlg(qstring, 'File already exists. Overwrite?', 'Yes', 'No', 'No')
    
    switch choice
    case 'Yes'
      delete(h5file_location);
    otherwise
      return;
    end
  end

  %h5create(h5file, '/energy', size(energy));
  %h5write(h5file, '/energy', energy);

  %h5create(h5file, '/log_energy', size(energy));
  %h5write(h5file, '/log_energy', log(energy));

  %ret = epsilon


  % We need to re-arrange the dimensions to get the correct output in VTK using h5tovtk.
  epsilon_for_h5_writing = permute(epsilon,[3,1,2]);

  h5create(h5file, '/epsilon', size(epsilon_for_h5_writing));
  h5write(h5file, '/epsilon', epsilon_for_h5_writing);

  command = ['h5tovtk ', h5file];
  [status,cmdout] = system(command,'-echo');
  % To create the .vtk files:
  %  h5tovtk -o energy.v3.log_energy.vtk energy.v3.h5:log_energy
  %  h5tovtk -o energy.v3.epsilon.vtk energy.v3.h5:epsilon
  %  h5tovtk -o energy.v3.energy.vtk energy.v3.h5:energy

  % h5tovtk -d log_energy  -o log_energy.vtk energy.h5
  % h5tovtk -d epsilon  -o epsilon.vtk energy.h5
  % h5tovtk -d energy  -o energy.vtk energy.h5
  % h5tovtk -d log_energy  -o log_energy.vtk energy.h5 && h5tovtk -d epsilon  -o epsilon.vtk energy.h5 && h5tovtk -d energy  -o energy.vtk energy.h5
end
