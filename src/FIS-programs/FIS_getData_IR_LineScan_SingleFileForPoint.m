function data = FIS_getData_IR_LineScan_SingleFileForPoint(logfile)

  % default return data
  data = struct();
  data.Position = [];
  data.Lambda = [];
  data.Intensity = [];
  
  % Sample/S
  % Mirror/M
  % DarkBackground/D (when the flip-mirror blocks the path to the sensor fibre)
  % NosampleBackground/N
  % TODO: add support for the various sample types
  % TODO: add support for non-horizontal scans
  measurement_types = {'Sample', 'Mirror', 'DarkBackground', 'NosampleBackground'};
  
  % load logfile info
  FIS_info = FIS_readLogFile(logfile);
  
  % position data
  Xres = FIS_info.Spatial_Resolution_mm;
  Xini = FIS_info.Initial_Position_mm(1);
  Xend = FIS_info.Final_position_mm(1);      
  Xposition = Xini:Xres:Xend;
  if length(Xposition)==1
      Xposition(end+1) = Xend; % for dark background measurements, where only 1-2 positions are measured to save time
  end
  data.Position = Xposition;
  
  FOLDER = dirname(logfile);
  
  FIS_data_files = struct();
  FIS_data_files.(measurement_types{1}).files = {};
  FIS_data_files.(measurement_types{1}).FIS_info = FIS_info;
  FIS_data_files.(measurement_types{1}).logfile = logfile;
  FIS_data_files.(measurement_types{1}).logfile_full = fullfile(pwd(), logfile);
  
  for pos_idx = 1:length(data.Position)
    dataFile = sprintf('S%dX6000Y.txt', round(1000*data.Position(pos_idx)));
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
  
  dataFileList = FIS_data_files.(measurement_types{1}).files;
  for pos_idx = 1:length(data.Position)
    D = load(dataFileList{pos_idx});
    if pos_idx == 1
      data.Lambda = D(:,1);
    end
    data.Intensity(:, pos_idx) = D(:,2);
  end
  
  % standardize to column vectors
  data.Position = data.Position(:);
  data.Lambda = data.Lambda(:);
end
