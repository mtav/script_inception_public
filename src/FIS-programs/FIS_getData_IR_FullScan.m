function data = FIS_getData_IR_FullScan(logfile)
  % default return data
  data = struct();
  data.Position = [];
  data.Lambda = [];
  data.Intensity = [];
  
  measurement_types = {'Sample', 'Mirror', 'DarkBackground', 'NosampleBackground'};
  
  % load logfile info
  FIS_info = FIS_readLogFile(logfile);
  % data.metadata.FIS_info = FIS_info;
  
  % position data
  res = FIS_info.Spatial_Resolution_mm;
  Xini = FIS_info.Initial_Position_mm(1);
  Xend = FIS_info.Final_position_mm(1);
  Yini = FIS_info.Initial_Position_mm(2);
  Yend = FIS_info.Final_position_mm(2);
  x_position = Xini:res:Xend;
  y_position = Yini:res:Yend;
  if length(x_position)==1
      x_position(end+1) = Xend; % for dark background measurements, where only 1-2 positions are measured to save time
  end
  if length(y_position)==1
      y_position(end+1) = Yend; % for dark background measurements, where only 1-2 positions are measured to save time
  end
  
  data.x_position = x_position;
  data.y_position = y_position;
  
  [data.X, data.Y, data.Lambda] = meshgrid(data.x_position, data.y_position, FIS_getW_IR());
  
  FOLDER = dirname(logfile);
  
  FIS_data_files = struct();
  FIS_data_files.(measurement_types{1}).files = {};
  FIS_data_files.(measurement_types{1}).FIS_info = FIS_info;
  FIS_data_files.(measurement_types{1}).logfile = logfile;
  FIS_data_files.(measurement_types{1}).logfile_full = fullfile(pwd(), logfile);
  
  % get data files
  for pos_idx = 1:length(data.y_position)
    dataFile = sprintf('SampleY%d.txt', round(1000*data.y_position(pos_idx)));
    dataFile = fullfile(FOLDER, dataFile);
    if ~exist(dataFile, 'file')
      warning('File not found!: %s', dataFile);
      if ~java.io.File(f).exists()
        % cf: https://stackoverflow.com/questions/3938687/matlab-exist-returns-0-for-a-file-that-definitely-exists
        error('File not found!: %s', dataFile);
      end
    end
    FIS_data_files.(measurement_types{1}).files{end+1} = dataFile;
  end
  data.metadata.FIS_data_files = FIS_data_files;
  
  % load data
  data.Intensity = NaN * ones(length(x_position), length(y_position), length(data.Lambda));
  
  dataFileList = FIS_data_files.(measurement_types{1}).files;
  for pos_idx = 1:length(data.y_position)
    D = load(dataFileList{pos_idx});
    D = D';
    data.Intensity(:, pos_idx, :) = D(:,:);
  end
  
end
