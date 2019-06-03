function [ entries, structured_entries ] = GEO_INP_reader(file_list)
  % function [ entries, structured_entries ] = GEO_INP_reader(file_list)
  % creates entries + structured_entries from file_list
  %
  % TODO: parallelepiped support... (but what should really be done is a common parsing library used by all interfaces: C++, Matlab/Octave, Python, etc)
  % TODO: Make it return [ structured_entries, entries ] + maybe get read of "entries" return value.
  
  entries = {};
  structured_entries = FDTDstructure();
  
  for idx = 1:length(file_list)
    filename = file_list{idx};
    
    [DIR, NAME, EXT] = fileparts (filename);
    
    if strcmpi(EXT, '.in')
      error('.in file passed');
    end
    
    % disp(['Processing ', filename]);
    [ entries, structured_entries ] = single_GEO_INP_reader(filename, entries, structured_entries);
  end

end % end of function
