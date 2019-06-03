function [basename_str, path_str, basename_str_with_suffix] = basename(NAME, SUFFIX)
  % function [basename_str, path_str, basename_str_with_suffix] = basename(NAME, SUFFIX)
  %
  % DESCRIPTION
  %        Returns NAME with any leading directory components removed.  If specified, also remove a trailing SUFFIX.
  %
  % Based on the GNU/Linux "basename" command, but also optionally returns the path and basename with suffix.
  
  [path_str, name_str, ext_str] = fileparts(NAME);
  basename_str_with_suffix = [name_str, ext_str];
  
  if exist('SUFFIX','var') == 1
    basename_str = regexprep(basename_str_with_suffix, [SUFFIX,'$'],''); % TODO: Why not build it using name_str + SUFFIX? Anyway, works for now...
  else
    basename_str = basename_str_with_suffix;
  end
  
end
