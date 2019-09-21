function [x_all, y_all, dwell_all, rep, numPoints] = readStrFile(filename_cellarray, magnitude)
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %
  %       UNIVERSITY OF BRISTOL
  %
  %       Original author: Erman Engin
  %
  % Modified by Mike Taverne
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % This function reads and plots a mask file (stream file, usual extension: .str).
  %
  % Usage:
  %   [x, y, dwell, rep, numPoints] = readStrFile(filename_cellarray, magnitude)
  %
  % magnitude is optional. If given a second plot in mum will be created.
  % TODO: Add support for filelists.
  % TODO: Use in readStrFile().
  %
  % This script makes the old "surfMask()" obsolete.
  
  if (nargin==0)
    [FileName,PathName,FilterIndex] = uigetfile('*.str','',pwd());
    filename=[PathName,filesep,FileName];
    filename_cellarray = {filename};
  end
  
  if ischar(filename_cellarray)
    filename_cellarray = {filename_cellarray};
  end
  
  % default values
  x_all = [];
  y_all = [];
  dwell_all = [];
  
  figure; hold on;
  
  for idx=1:length(filename_cellarray)
    % default values
    x = [];
    y = [];
    dwell = [];
    rep = 0;
    numPoints = 0;
    
    filename = char(filename_cellarray(idx));
    disp(['Processing : ',filename]);
    
    try
      fid = fopen(filename);
      dummy = fgets(fid);
      rep = str2num(fgets(fid));
      numPoints = str2num(fgets(fid));
      M = fscanf(fid, '%f %f %f', [3 inf]);
      fclose(fid);
    catch
      disp(['Error opening file ', filename]);
      fclose(fid);
    end
    
    if size(M, 1) < 3
      disp('WARNING: Empty streamfile');
    else
      dwell = M(1, :);
      x = M(2, :);
      y = M(3, :);
    end
    
    estimateMaskDuration(x, y, dwell, rep);
    
    if exist('magnitude','var') == 1
      plotFIBstream(x, y, dwell, magnitude);
    else
      plotFIBstream(x, y, dwell);
    end
    x_all = [x_all, x];
    y_all = [y_all, y];
    dwell_all = [dwell_all, dwell];
    
  end
end
