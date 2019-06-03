function [ pillar_type, n_type, radius, N_bottom, N_top, basename ] = getDataFromDirname(DIR)
  % get pillar data
  % this function is specific to Andrew's micropillars
  
  [ folder, basename, ext ] = fileparts(DIR);
  infos = regexp(basename, '_', 'split');
  pillar_type = infos(2);
  n_type = str2num(char(infos(3)));
  radius = str2num(char(infos(4)))/10;
  
  if strcmp(pillar_type,'M2754')
    N_bottom = 33;
    N_top = 26;
  elseif strcmp(pillar_type,'M3687')
    N_bottom = 40;
    N_top = 36;
  else
    error('Unidentified pillar!');
  end
end
