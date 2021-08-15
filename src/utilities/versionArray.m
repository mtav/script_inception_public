function v = versionArray()
  version_string = version();
  version_cell_array = strsplit_custom(version_string, {'.', '~'});
  v = [];
  N = min(length(version_cell_array), 3);
  for idx = 1:N
    v(end+1) = str2num(version_cell_array{idx});
  end
end
