function result = dirname(path)
  % function result = dirname(path)
  %
  % If path ends with a "/", it returns path, but as a full path. (based on python's os.path.dirname() behaviour)
  % Else, it strips away any trailing /component and returns the full path containing /component.
  %
  % If dirname(path) exists, an absolute path is returned
  % Else, it just returns path without the final component
  %
  % TODO: improve doc
  
  curDir = pwd();
  [pathstr, name, ext] = fileparts(GetFullPath(path));
  if exist(pathstr, 'dir')
    cd(pathstr);
    result = pwd(); % full (absolute) path
  else
    result = pathstr;
  end
  cd(curDir); % get back to where you were
  
end
