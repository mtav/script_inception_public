function [epsilon, X, Y, Z, structured_entries] = prnToh5_epsilon(inpfile_list, varargin)
  % function [epsilon, X, Y, Z, structured_entries] = prnToh5_epsilon(inpfile_list, varargin)
  %
  % Convert epsilon .prn slices into an .h5 and a .vtk file.
  %
  % Usage:
  %  prnToh5_epsilon({'epsilon_snaphots.inp'})
  %  prnToh5_epsilon({'epsilon_snaphots.inp'}, 'foo.h5')
  %  prnToh5_epsilon({'epsilon_snaphots.inp'}, '', 'overwrite', true, 'show_figure', 'false')
  %
  % Arguments:
  %   Required:
  %     inpfile_list : List of input files of the form {'file1.inp','file2.inp',...}
  %  Optional:
  %    h5file : The .h5 output file. Also used as base for the .vtk output filename. If an empty string is passed, the filename will be automatically generated using the basename of the first element from inpfile_list. Default: ''
  %  Parameter-value pairs:
  %    'snap_plane' : Direction of the snapshots ('x', 'y', 'z' or 'auto'). If set to 'auto', it chooses the direction with the most snapshots. Default = 'auto'
  %    'show_figure' : If true, show Matlab slice plots of the data. Default: true
  %    'overwrite' : If true, overwrite existing .h5 and .vtk files without asking for confirmation. Default: false
  %
  % Return values:
  %   * epsilon : An Ny*Nx*Nz "meshgrid" of the epsilon values.
  %   * X : An Ny*Nx*Nz "meshgrid" of the X values.
  %   * Y : An Ny*Nx*Nz "meshgrid" of the Y values.
  %   * Z : An Ny*Nx*Nz "meshgrid" of the Z values.
  %   * structured_entries : The "BFDTD structure" corresponding to the inpfile_list entries.
  %
  % TODO: Create proper .vtu, .vts or .vti files.
  % TODO: Extend to frequency/energy snapshots and use all snapshots (planned via VTK(python or C++) .vts/.vtu files).
  % TODO: We should use x/y,y/z,z/x pairs from the snapshots to add them to the grid and only use the .inp file for the third coordinate. This would work around any additional bugs in BFDTD and make the code more robust. Eventual goal is .vtu for this reason as well. Data can be added at arbitrary positions (but makes analysis harder).
  %
  %%% Note about stored dimensions:
  % for all: size(epsilon) = Ny, Nx, Nz
  % for h5tovtk to lead to correct X,Y,Z axes, we need to h5write in this order: Nz, Ny, Nx
  % for X snapshots: size(esnap_data) = Nz, Ny -> needs to be transposed
  % for Y snapshots: size(esnap_data) = Nz, Nx -> needs to be transposed
  % for Z snapshots: size(esnap_data) = Ny, Nx
  %
  %%% Note about BFDTD-weirdness:
  % When creating a snapshot plane covering the whole geometry, the data output does not seem to cover the final edge of the mesh.
  % But when using a partial snapshot starting a little bit after the first edge, it does cover the final edge of the mesh.
  % This is a bug as confirmed by Chris Railton. It is fixed in "BFDTD 2014".
  % This script works with both versions.

  % create parser
  p = inputParser();
  p = inputParserWrapper(p, 'addRequired', 'inpfile_list', @iscellstr);
  p = inputParserWrapper(p, 'addOptional', 'h5file', '', @ischar);
  p = inputParserWrapper(p, 'addParamValue', 'snap_plane', 'auto', @(x) any(validatestring(x, {'x','y','z','auto'})));
  p = inputParserWrapper(p, 'addParamValue', 'show_figure', true, @islogical);
  p = inputParserWrapper(p, 'addParamValue', 'overwrite', false, @islogical);
  p = inputParserWrapper(p, 'parse', inpfile_list, varargin{:});
    
  if isempty(p.Results.h5file)
    [path_str, name_str, ext_str] = fileparts(p.Results.inpfile_list{1});
    h5file = [path_str, name_str, '.h5'];
  else
    h5file = p.Results.h5file;
  end
  
  % read BFDTD input files
  [inpEntries, structured_entries] = GEO_INP_reader(inpfile_list);
  
  % detect slicing direction automatically
  slicing_info = BFDTD_getSlicingInfo(structured_entries, 'SnapshotType', p.Results.snap_plane);
  [snap_plane, Nsnaps, slicing_direction_index, snap_type] = BFDTD_getSlicingInfo(structured_entries, 'SnapshotType', p.Results.snap_plane);

  % convert snap_plane='x','y','z' to 1,2,3
  slicing_direction_index = (snap_plane - double('x')) + 1;

  if slicing_direction_index == 1
    Nsnaps = length(structured_entries.epsilon_snapshots_X);
  elseif slicing_direction_index == 2
    Nsnaps = length(structured_entries.epsilon_snapshots_Y);
  else
    Nsnaps = length(structured_entries.epsilon_snapshots_Z);
  end
  
  % prepare a meshgrid
  xmesh = [0; cumsum(structured_entries.xmesh)];
  ymesh = [0; cumsum(structured_entries.ymesh)];
  zmesh = [0; cumsum(structured_entries.zmesh)];
  [X, Y, Z] = meshgrid(xmesh, ymesh, zmesh);

  % create array to store data from the snapshots
  epsilon = zeros(size(X));

  id_string = structured_entries.flag.id;
  
  for numID = 1:Nsnaps
    % get filename
    [ esnap, alphaID, pair ] = numID_to_alphaID_TimeSnapshot(numID, snap_plane, id_string, 1);
    
    % read in data
    [esnap_header, esnap_data, esnap_u, esnap_v] = readPrnFile(esnap);
    
    if size(esnap_data, 3) ~= 1
      error('This does not appear to be a standard epsilon snapshot with just two coordinate columns and one material column.');
    end
    
    if slicing_direction_index == 1
    
      % get x position and index
      x_current = structured_entries.epsilon_snapshots_X(numID).P1(slicing_direction_index);
      [x_current_closest_err, x_current_idx] = min(abs(xmesh - x_current));

      % determine range into which to write
      P1 = structured_entries.epsilon_snapshots_X(numID).P1;
      P2 = structured_entries.epsilon_snapshots_X(numID).P2;
      
      Ymin = P1(2);
      Ymax = P2(2);
      Zmin = P1(3);
      Zmax = P2(3);

      snapshot_data_range_Y = esnap_u;
      snapshot_data_range_Z = esnap_v;
      
      Ymin = max(Ymin, snapshot_data_range_Y(1));
      Ymax = min(Ymax, snapshot_data_range_Y(end));
      Zmin = max(Zmin, snapshot_data_range_Z(1));
      Zmax = min(Zmax, snapshot_data_range_Z(end));

      [ind_ymin, val, abs_err] = closestInd(ymesh, Ymin);
      [ind_ymax, val, abs_err] = closestInd(ymesh, Ymax);
      [ind_zmin, val, abs_err] = closestInd(zmesh, Zmin);
      [ind_zmax, val, abs_err] = closestInd(zmesh, Zmax);

      % put data into the prepared arrays
      epsilon(ind_ymin:ind_ymax, x_current_idx, ind_zmin:ind_zmax) = esnap_data';
      
    elseif slicing_direction_index == 2
    
      % get y position and index
      y_current = structured_entries.epsilon_snapshots_Y(numID).P1(slicing_direction_index);
      [y_current_closest, y_current_idx] = min(abs(ymesh - y_current));
      
      % determine range into which to write
      P1 = structured_entries.epsilon_snapshots_Y(numID).P1;
      P2 = structured_entries.epsilon_snapshots_Y(numID).P2;

      Xmin = P1(1);
      Xmax = P2(1);
      Zmin = P1(3);
      Zmax = P2(3);
      
      snapshot_data_range_X = esnap_u;
      snapshot_data_range_Z = esnap_v;
      
      Xmin = max(Xmin, snapshot_data_range_X(1));
      Xmax = min(Xmax, snapshot_data_range_X(end));
      Zmin = max(Zmin, snapshot_data_range_Z(1));
      Zmax = min(Zmax, snapshot_data_range_Z(end));
      
      [ind_xmin, val, abs_err] = closestInd(xmesh, Xmin);
      [ind_xmax, val, abs_err] = closestInd(xmesh, Xmax);
      [ind_zmin, val, abs_err] = closestInd(zmesh, Zmin);
      [ind_zmax, val, abs_err] = closestInd(zmesh, Zmax);
            
      % put data into the prepared arrays
      epsilon(y_current_idx, ind_xmin:ind_xmax, ind_zmin:ind_zmax) = esnap_data';
      
    elseif slicing_direction_index == 3
    
      % get z position and index
      z_current = structured_entries.epsilon_snapshots_Z(numID).P1(slicing_direction_index);
      [z_current_closest, z_current_idx] = min(abs(zmesh-z_current));
      
      % determine range into which to write
      P1 = structured_entries.epsilon_snapshots_Z(numID).P1;
      P2 = structured_entries.epsilon_snapshots_Z(numID).P2;
      
      Xmin = P1(1);
      Xmax = P2(1);
      Ymin = P1(2);
      Ymax = P2(2);

      snapshot_data_range_X = esnap_u;
      snapshot_data_range_Y = esnap_v;
      
      Xmin = max(Xmin, snapshot_data_range_X(1));
      Xmax = min(Xmax, snapshot_data_range_X(end));
      Ymin = max(Ymin, snapshot_data_range_Y(1));
      Ymax = min(Ymax, snapshot_data_range_Y(end));

      [ind_xmin, val, abs_err] = closestInd(xmesh, Xmin);
      [ind_xmax, val, abs_err] = closestInd(xmesh, Xmax);
      [ind_ymin, val, abs_err] = closestInd(ymesh, Ymin);
      [ind_ymax, val, abs_err] = closestInd(ymesh, Ymax);

      % put data into the prepared arrays
      epsilon(ind_ymin:ind_ymax, ind_xmin:ind_xmax, z_current_idx) = esnap_data;
      
    end
    
  end

  % plot in matlab to check before writing to .h5
  if p.Results.show_figure
    figure;

    subplot(1,2,1);
    contourslice(X, Y, Z, epsilon, [xmesh(floor(length(xmesh)/2))],[ymesh(floor(length(ymesh)/2))],[zmesh(floor(length(zmesh)/2))]);
    colormap jet; colorbar;
    xlabel('x'); ylabel('y'); zlabel('z');

    subplot(1,2,2);
    slice(X, Y, Z, epsilon, [xmesh(floor(length(xmesh)/2))],[ymesh(floor(length(ymesh)/2))],[zmesh(floor(length(zmesh)/2))]);
    colormap jet; colorbar;
    xlabel('x'); ylabel('y'); zlabel('z');
  end

  % create .h5 file
  h5file_location = GetFullPath(h5file);
  if exist(h5file_location, 'file')
    if p.Results.overwrite
      delete(h5file_location);
    else
      %h5file_location = which(h5file);
      %if isempty(h5file_location)
        %h5file_location = GetFullPath(h5file);
      %end
      qstring = ['Overwrite ', h5file_location, ' ?'];
      choice = questdlg(qstring, 'File already exists. Overwrite?', 'Yes', 'No', 'No');
      
      switch choice
        case 'Yes'
          delete(h5file_location);
        otherwise
          return;
      end
    end
  end

  % We need to re-arrange the dimensions to get the correct output in VTK using h5tovtk.
  epsilon_for_h5_writing = permute(epsilon, [3,1,2]);

  disp(['Creating ', h5file_location]);
  h5create(h5file_location, '/epsilon', size(epsilon_for_h5_writing));
  h5write(h5file_location, '/epsilon', epsilon_for_h5_writing);

  disp('...and the corresponding vtk file.');
  command = ['h5tovtk ', h5file_location];
  [status,cmdout] = system(command,'-echo');

  disp('DONE');
end
