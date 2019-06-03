function ret = filefun(func, infile)
  % function ret = filefun(func, infile)
  %
  % Apply function to each line from a text file.
  %
  % * strips whitespace before and after lines.
  % * skips empty lines.
  % * skips lines starting with % or #.
  %
  % Example usage:
  %    ret = filefun(@calculateModeVolume_RCD111, 'dirlist.txt');
  %
  % TODO: Add support for multiple arguments by using s{:} and making fileToCellArray() split up based on a given separator (optionally)
  
  s = fileToCellArray(infile);
  ret = cellfun(func, s, 'UniformOutput', false);
end
