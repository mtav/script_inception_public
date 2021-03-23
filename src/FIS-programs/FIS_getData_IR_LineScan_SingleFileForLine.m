function data = FIS_getData_IR_LineScan_SingleFileForLine(dataFile, logfile, Wfile)
  
  % default return data
  data = struct();
  data.Position = [];
  data.Lambda = [];
  data.Intensity = [];
  
  % select input file if not specified
  if ~exist('dataFile', 'var')
    [FileName_Sample, PathName_Sample] = uigetfile('*.txt','Select the Sample file');
    if isequal(FileName_Sample, 0)
      disp('User selected Cancel');
      return
    end
    dataFile = [PathName_Sample, FileName_Sample];
  end
  
  % determine logfile if not provided
  if ~exist('logfile', 'var')
    logfile = fullfile(dirname(dataFile), 'log.txt');
    if ~exist(logfile, 'file')
        d = dirname(logfile);
        filelist = dir(fullfile(d, '*log.txt'));
        if length(filelist)==1
            logfile = fullfile(filelist(1).folder, filelist(1).name);
            fprintf('Auto-determined logfile: %s\n', logfile);
        else
            filelist
            error('Failed to determine logfile.');
        end
    end
    FIS_info = FIS_readLogFile(logfile);
    Xres = FIS_info.Spatial_Resolution_mm;
    Xini = FIS_info.Initial_Position_mm(1);
    Xend = FIS_info.Final_position_mm(1);      
  end
  
  % default wavelength file if not specified
  if ~exist('Wfile', 'var')
    Wfile = fullfile(dirname(dataFile), 'W.txt');
  end
  
  % add metadata
  data.metadata.dataFile = dataFile;
  data.metadata.dataFile_full = fullfile(pwd(), dataFile);
  data.metadata.Wfile = Wfile;
  data.metadata.logfile = logfile;
  data.metadata.FIS_info = FIS_info;
  
  % debugging output
  fprintf('dataFile = %s\n', dataFile);
  
  % intensity data
  data.Intensity = load(dataFile);
  
  % wavelength data
  wavelength = load(Wfile);
  data.Lambda = unique(wavelength); % because data gets appended to W.txt on repeated measurements
  
  % position data
  Xposition = Xini:Xres:Xend;
  if length(Xposition)==1
      Xposition(end+1) = Xend; % for dark background measurements, where only 1-2 positions are measured to save time
  end
  
  % if the measurement was cancelled, truncate the position vector
  if length(Xposition) > size(data.Intensity, 2)
      Xposition = Xposition(1:size(data.Intensity, 2));
  end
  data.Position = Xposition;
  
  data.metadata.zrange = getRange(data.Intensity);
  
  % standardize to column vectors
  data.Position = data.Position(:);
  data.Lambda = data.Lambda(:);
end
