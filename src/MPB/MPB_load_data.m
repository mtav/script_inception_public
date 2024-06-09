function s = MPB_load_data(infile)
  %%%%% Designed to read data from .dat files generated using:
  %% mpb CTLFILE > OUTFILE
  %% grep freq OUTFILE > DATFILE
  
  if ~exist('infile', 'var')
    [infile_name, infile_dir] = uigetfile('*.dat');
    infile = fullfile(infile_dir, infile_name);
  end
  
  s = struct();
  s.infile = infile;
  [s.infile_dir, s.infile_base, s.infile_ext] = fileparts(s.infile);
  
  data = readmatrix(s.infile, 'Range', [2,2]);
  
  s.kindex = data(:,1);
  s.kindex_fixed = 1:size(data, 1);
  s.k1 = data(:,2);
  s.k2 = data(:,3);
  s.k3 = data(:,4);
  s.kmag = data(:,5);
  
  for i = 6:size(data,2)
    fn = data(:,i);
    s.fn(:,i-5) = fn(:);
  end
end
