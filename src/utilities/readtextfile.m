function tab = readtextfile(filename)
  % Read a text file into a matrix with one row per input line
  % and with a fixed number of columns, set by the longest line.
  % Each string is padded with NUL (ASCII 0) characters
  %

  % open the file for reading
  ip = fopen(filename,'rt');          % 'rt' means read text
  if (ip < 0)
      error('could not open file');   % just abort if error
  end;
  % find length of longest line
  max=0;                              % record length of longest string
  cnt=0;                              % record number of strings
  s = fgetl(ip);                      % get a line
  while (ischar(s))                   % while not end of file
     cnt = cnt+1;
     if (length(s) > max)           % keep record of longest
          max = length(s);
     end;
      s = fgetl(ip);                  % get next line
  end;
  % rewind the file to the beginning
  max=56;
  frewind(ip);
  % create an empty matrix of appropriate size
  tab=char(zeros(cnt,max));         % fill with ASCII zeros
  % load the strings for real
  cnt=0;
  s = fgetl(ip);
  while (ischar(s))
     cnt = cnt+1;
     if length(s) ~= 0
         tab(cnt,1:length(s)) = s;      % slot into table
     end
     s = fgetl(ip);
  end;
  % close the file and return
  fclose(ip);
end
