function s = fileToCellArray(infile)
  % function s = fileToCellArray(infile)
  %
  % Create a cell array from a textfile.
  %
  % * strips whitespace before and after lines.
  % * skips empty lines.
  % * skips lines starting with % or #.

  s = {};
  fid = fopen(infile);
  tline = fgetl(fid);
  while ischar(tline)
      tline = strtrim(tline);
      if ~isempty(tline) && ~strcmp(tline(1),'%') && ~strcmp(tline(1),'#')
        s{end+1} = tline;
      end
      tline = fgetl(fid);
  end
  fclose(fid);

end
