function FIS_data_files = FIS_getFiles(folder_name)
  % Find FIS data in directory "folder_name" and return the corresponding filenames in a structure.
  
  FIS_data_files =  struct();
  
  if ~exist('folder_name', 'var')
    folder_name = uigetdir();
  end
  
  %fprintf(1, 'folder_name = %s\n', folder_name);
  
  FIS_data_files.folder_name = folder_name;
  
  % find the log files:
  measurement_types = {'Sample', 'Mirror', 'DarkBackground', 'NosampleBackground'};
  for measurement_type = measurement_types
    L = dir(fullfile(folder_name, [measurement_type{:}, '*log.txt']));
    for idx = 1:length(L)
      [tokens, matches] = regexp(L(idx).name, [measurement_type{:}, '(.*?)log\.txt'],'tokens','match');
      FILENAME = tokens{1}{1};
      PREFIX = sprintf('%s%s', measurement_type{:}, FILENAME);
      logfile = fullfile(L(idx).folder, sprintf('%s%s', PREFIX, 'log.txt'));
      FIS_info = FIS_readLogFile(logfile);
      FIS_data_files.(measurement_type{:}).FIS_info = FIS_info;
      position = FIS_info.Initial_Position_mm:FIS_info.Spatial_Resolution_mm:FIS_info.Final_position_mm;
      FIS_data_files.(measurement_type{:}).position = position;
      FIS_data_files.(measurement_type{:}).files = {};
      for pos_idx = 1:length(position)
        f = fullfile(L(idx).folder, sprintf('%s%d.txt', PREFIX, round(1000*position(pos_idx))));
        if ~exist(f, 'file')
          error('File not found!: %s', f);
        end
        FIS_data_files.(measurement_type{:}).files{end+1} = f;
      end
    end
  end
  
end
