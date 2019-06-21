function FIS_info = FIS_readLogFile(logfile)
  % extract structured data from an FIS log file
  
  FIS_info = struct();
  [fid, message] = fopen(logfile, 'r');
  if fid == -1
    error(message);
  end
  FIS_info.prefix = fgetl(fid);
  
  while true
    L = fgetl(fid);
    if isnumeric(L)
      break;
    end
    [name, value, valid_field_name] = getNameValuePair(L);
    %if isnumeric(value)
      %fprintf(1, '%s = %.2f\n', valid_field_name, value);
    %else
      %fprintf(1, '%s = %s\n', valid_field_name, value);
    %end
    FIS_info.(valid_field_name) = value;
  end
  fclose(fid);
end

function [name, value, valid_field_name] = getNameValuePair(L)
  % Get name and value from a string of the form 'name : value'.
  % "valid_field_name" can be used as a structure fieldname.
  
  % split, strip and replace only exist in Matlab 2016 and later.
  
  %a = split(L, ':');
  a = strsplit(L, ':');
  %name = strip(a{1});
  name = strtrim(a{1});
  %[value, tf] = str2num(strip(a{2}));
  [value, tf] = str2num(strtrim(a{2}));
  if tf == 0
    %value = strip(a{2});
    value = strtrim(a{2});
  end
  C = {' ', '-','(',')', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'};
  % valid_field_name = replace(name, C, '_');
  valid_field_name = name;
  for idx=1:length(C)
    valid_field_name = strrep(valid_field_name, C{idx}, '_');
  end

  % valid_field_name = strip(valid_field_name, '_');
  % valid_field_name = strtrim(valid_field_name, '_');
   valid_field_name = regexprep(valid_field_name, '^_+', '');
   valid_field_name = regexprep(valid_field_name, '_+$', '');

end
