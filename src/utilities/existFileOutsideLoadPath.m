function [file_found, details] = existFileOutsideLoadPath(filename, raise_error)
  % Checks if filename exists and is a file,
  % but also whether or not it was accidentally found in the Octave/Matlab search path.

  if ~exist('raise_error', 'var')
    raise_error = false;
  end

  % default return values
  file_found = false;
  details.error_message = '';
  details.file_in_path = false;
  details.file_in_path_location = '';
  details.file_fullpath = '';  
  
  % exit if file not found
  if ~exist(filename, 'file')
    file_found = false;
    details.error_message = ['File not found: ', filename];
    if raise_error
      error(details.error_message);
    end
    return;
  end
  
  % check that file is not accidentally a file on the Matlab/Octave path
  details.file_in_path_location = which(filename);
  %if inoctave()
    %details.file_in_path_location = file_in_loadpath(filename, 'all');
  %end
  if ~isempty(details.file_in_path_location)
    details.file_fullpath = GetFullPath(filename);
    if ~strcmp(details.file_in_path_location, details.file_fullpath)
      file_found = false;
      details.error_message = ['File found in load path at ', details.file_in_path_location, ', but requested file was ', details.file_fullpath, '. If this is the file you want, please specify the full path or change directory.'];
      if raise_error
        error(details.error_message);
      end
      return;
    end
  end

  file_found = true;
end
