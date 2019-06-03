function ret = getDefectProperties(geofile, defect_name)
  % quickly hacked up function to extract defect properties.
  % TODO: Optimize GEO_INP_reader instead (matlab+octave) + maybe add options to search for defect only, etc
  
  ret.defect_found = false;
  
  [DIR, NAME, EXT] = fileparts (geofile);
  if ~strcmpi(EXT, '.geo')
    error('Invalid extension: %s -> %s', geofile, EXT);
  end
  if ~exist(geofile, 'file')
    error('File not found: %s', geofile);
  end
  
  fulltext = fileread(geofile);
  
  % remove comments
  pattern_stripcomments = '\*\*(?!name=).*\n';
  cleantext =  regexprep(fulltext, pattern_stripcomments, '\n', 'lineanchors', 'dotexceptnewline', 'warnings');
  
  % TODO: reduce code duplication between here and single_GEO_INP_reader()...
  %% extract blocks
  %pattern_objects = '^(?<type>\w+)\s*(?<nameblob>[^\{\}]+)?\{(?<data>[^\{\}]*?)\}';
  %[tokens_blocks, match_blocks, names_blocks] =  regexp(cleantext, pattern_objects, 'tokens', 'match', 'names', 'lineanchors');
  
  % extract blocks
  pattern_objects = '^(?<type>\w+)\s*(?<nameblob>[^\{\}]+)?\{(?<data>[^\{\}]*?)\}';
  if inoctave()
    [tokens_blocks, match_blocks, names_blocks] =  regexp(cleantext, pattern_objects, 'tokens', 'match', 'names', 'lineanchors');
    % this is slow!
    names_blocks = ScalarStructureToStructArray(names_blocks);
  else
    [tokens_blocks, match_blocks, names_blocks] =  regexp(cleantext, pattern_objects, 'tokens', 'match', 'names', 'lineanchors', 'warnings');
  end
  
  %names_blocks
  %length_names_blocks = getNumberOfEntries(names_blocks)
  
  % process blocks
  %disp(['length_names_blocks = ', num2str(length_names_blocks)]);
  for i = 1:length(names_blocks)
    %[type, nameblob, data] = getTokenValues(names_blocks, i);
    type = names_blocks(:,i).type;
    nameblob = names_blocks(:,i).nameblob;
    
    name = '';
    if strcmpi(nameblob,'') == 0
      pattern_nameblob = '\*\*name=(?<name>.*)';
      if inoctave()
        [tokens_nameblob match_nameblob names_nameblob] =  regexp(nameblob, pattern_nameblob, 'tokens', 'match', 'names', 'lineanchors');
      else
        [tokens_nameblob match_nameblob names_nameblob] =  regexp(nameblob, pattern_nameblob, 'tokens', 'match', 'names', 'lineanchors', 'warnings');
      end
      if length(names_nameblob.name) > 0
        name = strtrim(names_nameblob.name);
      end
    end
    
    if strcmpi(name, defect_name)
      ret.defect_found = true;
      break
    end
  end
  
  if ~ret.defect_found
    return
  end
  
  %%name
  %%type
  %%nameblob
  %%data
  
  %dataV = [];
  %% remove empty lines
  %lines = strread(data,'%s','delimiter','\n');
  
  %%cellFlag = 1;
  
  %for L = 1:length(lines)
    %if ~length(lines{L})
      %continue;
    %end
  
    %% num_val will be an empty [] if lines{L} is string
    %num_val = str2num(lines{L});
    %%L
    %%num_val
          
    %str_val = strtrim(lines{L}); % trim string
    %str_val = str_val(str_val ~= '"');% remove double quotes
  
    %% TODO: Check if this can't be simplified, or if it's even necessary.
    %%if cellFlag
      %if length(num_val) %% num_val is num
        %dataV{length(dataV)+1} = num_val;
      %else %% num_val is not num
        %dataV{length(dataV)+1} = str_val;
      %end
    %%else
      %%if length(num_val) %% num_val is num
        %%dataV = [dataV,num_val];
      %%else %% num_val is not num
        %%cellFlag = 1;
        %%dataV = num2cell(dataV);
        %%dataV{length(dataV)+1} = str_val;
      %%end
    %%end
  %end % end of loop through lines
  
  %entry.name = name;
  %entry.type = type;
  %entry.data = dataV';
  %%ret.entry = entry;
  entry.name = name;
  entry.type = type;
  entry.data = strsplit_custom(strtrim(names_blocks(:,i).data));
  %entries{length(entries)+1} = entry;
  
  switch upper(entry.type)
    case {'SPHERE'}
      ret.object = bfdtd_add_sphere(entry);
      ret.point_in_object = @(x,y,z) point_in_sphere(x, y, z, ret.object);
      ret.volume = sphereVolume(ret.object);
      
    case {'BLOCK'}
      ret.object = bfdtd_add_block(entry);
      ret.point_in_object = @(x,y,z) point_in_block(x, y, z, ret.object);
      ret.volume = blockVolume(ret.object);
    case {'CYLINDER'}
      ret.object = bfdtd_add_cylinder(entry);
      ret.point_in_object = @(x,y,z) point_in_cylinder(x, y, z, ret.object);
      ret.volume = cylinderVolume(ret.object);
    otherwise
      error('Unknown type.');
  end % end of switch
  
  ret.printInfo = @(prefix) printStructure(ret.object, prefix);
  ret.type = type;
    
end

%% deprecated
%function [type, nameblob, data] = getTokenValues(names_blocks, entry_index)
%%function val = getTokenValue(names_blocks, field_name, entry_index)
  %% special function to deal with the different types returned by regexp in Octave and Matlab
  %%entry_index=1
  %%field_index=1
  %%field_name='type'
  %% octave:
  %%tokens_blocks{entry_index}{field_index}
  %%val = getfield(names_blocks, field_name){entry_index}
  %type = names_blocks.type{entry_index};
  %nameblob = names_blocks.nameblob{entry_index};
  %data = names_blocks.data{entry_index};
  
  %% matlab:
%end

%% deprecated
%function N = getNumberOfEntries(names_blocks)
  %% octave:
  %N = length(names_blocks.type);
  %% matlab:
%end

%% deprecated
%function sphere = add_sphere(entry)
  %sphere.name = entry.name;
  %entry.data = cell2mat(entry.data);
  %idx = 1;
  %sphere.center = entry.data(idx:idx+2); idx = idx+3;
  %sphere.outer_radius = entry.data(idx); idx = idx+1;
  %sphere.inner_radius = entry.data(idx); idx = idx+1;
  %sphere.permittivity = entry.data(idx); idx = idx+1;
  %sphere.conductivity = entry.data(idx); idx = idx+1;
%end

%function block = add_block(entry)
  %block.name = entry.name;
  %entry.data = cell2mat(entry.data);
  %idx = 1;
  %block.lower = entry.data(idx:idx+2); idx = idx+3;
  %block.upper = entry.data(idx:idx+2); idx = idx+3;
  %block.permittivity = entry.data(idx); idx = idx+1;
  %block.conductivity = entry.data(idx); idx = idx+1;
%end

%function cylinder = add_cylinder(entry)
  %cylinder.name = entry.name;
  %entry.data = cell2mat(entry.data);
  %idx = 1;
  %cylinder.center = entry.data(idx:idx+2); idx = idx+3;
  %cylinder.inner_radius = entry.data(idx); idx = idx+1;
  %cylinder.outer_radius = entry.data(idx); idx = idx+1;
  %cylinder.height = entry.data(idx); idx = idx+1;
  %cylinder.permittivity = entry.data(idx); idx = idx+1;
  %cylinder.conductivity = entry.data(idx); idx = idx+1;
  %if length(entry.data)>=idx; cylinder.angle = entry.data(idx); else cylinder.angle = 0; end; idx = idx+1;
%end
