function v = versionArray()
  version_string = version();
  version_cell_array = strsplit_custom(version_string, '.');
  v = [];
  for idx = 1:length(version_cell_array)
    v(end+1) = str2num(version_cell_array{idx});
  end
end
