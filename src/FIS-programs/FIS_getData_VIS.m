function data = FIS_getData_VIS(folder_name, measurement_type)
  % Create a meshgrid data structure with the fields Position, Lambda, Intensity based on the data files in "folder_name" of type "measurement_type".
  % This can then be used as follows:
  %   Sample = FIS_getData_VIS(folder_name, 'Sample');
  %   Mirror = FIS_getData_VIS(folder_name, 'Mirror');
  %   surf(Sample.Position, Sample.Lambda, Sample.Intensity./Mirror.Intensity); view(2); shading interp;
  
  data = struct();
  data.Position = [];
  data.Lambda = [];
  data.Intensity = [];
  
  if ~exist('folder_name', 'var')
    folder_name = uigetdir();
    if isnumeric(folder_name) && folder_name==0
      return
    end
  end
  
  FIS_data_files = FIS_getFiles(folder_name);
  data.metadata.folder_name = folder_name;
  data.metadata.folder_name_full = fullfile(pwd, folder_name);
  data.metadata.FIS_data_files = FIS_data_files;
  
  measurement_types = {'Sample', 'Mirror', 'DarkBackground', 'NosampleBackground'};
  available_measurement_types = {};
  for idx = 1:length(measurement_types)
    if isfield(FIS_data_files, measurement_types{idx})
      available_measurement_types{end+1} = measurement_types{idx};
    end
  end
  if length(available_measurement_types) <= 0
    errordlg('No data found in this directory.');
    return
  end
  if ~exist('measurement_type', 'var')
    [idx, tf] = listdlg('PromptString', 'Select measurement type', 'SelectionMode', 'single', 'ListString', available_measurement_types);
    if tf == 0
      return;
    else
      measurement_type = available_measurement_types{idx};
    end
  end
  
  data.metadata.measurement_type = measurement_type;
  %fprintf(1, 'folder_name = %s\n', folder_name);
  %fprintf(1, 'measurement_type = %s\n', measurement_type);
  
  if ~isfield(FIS_data_files, measurement_type)
    error('No %s files found in %s', measurement_type, folder_name);
    return
  end
  
  PREFIX = FIS_data_files.(measurement_type).FIS_info.prefix;
  position = FIS_data_files.(measurement_type).position;
  f = fullfile(folder_name, sprintf('%s%d.txt', PREFIX, round(1000*position(1))));
  data1D = load(f);
  lambda = data1D(:,1);
  [data.Position, data.Lambda] = meshgrid(position, lambda);
  data.Intensity = zeros(size(data.Position));
  
  for pos_idx = 1:length(position)
      f = fullfile(folder_name, sprintf('%s%d.txt', PREFIX, round(1000*position(pos_idx))));
      data1D = load(f);
      lambda = data1D(:,1);
      intensity = data1D(:,2);
      data.Intensity(:, pos_idx) = intensity(:);
  end
  
end
