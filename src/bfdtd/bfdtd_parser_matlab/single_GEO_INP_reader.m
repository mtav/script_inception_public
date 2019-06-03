function [ entries, structured_entries ] = single_GEO_INP_reader(filename, entries, structured_entries, varargin)
  % function [ entries, structured_entries ] = single_GEO_INP_reader(filename, entries, structured_entries)
  %
  % fprintf('    single_GEO_INP_reader: processing: %s\n', filename);
  % TODO: Make it return [ structured_entries, entries ] + maybe get read of "entries" return value.
  %
  % TODO: data should be split by spaces, not by newlines, as this is most likely how BFDTD parses it. (make sure python parser does the same! and check bfdtd source code! (bris2meep C version))
  % TODO: str2num conversion should be done inside object-specific data readers, not before
  % TODO: optimize speed
  % TODO: allow searching by name (defect info extraction), with exit as soon as found, i.e. make getDefectProperties() obsolete/simplified
  % TODO: stop when "end" is read, as done by BFDTD
  
  % creates entries + structured_entries from filename
  
  %%%%%%%%%%%%%
  % parse args
  p = inputParser();
  p = inputParserWrapper(p, 'addRequired', 'filename', @ischar);
  p = inputParserWrapper(p, 'addRequired', 'entries', @iscell);
  p = inputParserWrapper(p, 'addRequired', 'structured_entries', @isstruct);
  p = inputParserWrapper(p, 'addParamValue', 'loadGeometry', true, @islogical);
  p = inputParserWrapper(p, 'parse', filename, entries, structured_entries, varargin{:});
  %%%%%%%%%%%%%
  
  if ~p.Results.loadGeometry
    [DIR, NAME, EXT] = fileparts (filename);
    if strcmpi(EXT, '.geo')
      return;
    end
  end
  
  %=====================================================================
  % define structures (TODO: switch to octave+matlab compatible classes)
  %=====================================================================
  time_snapshots = getTimeSnapshotStructure(0);
  epsilon_snapshots = getTimeSnapshotStructure(0);
  frequency_snapshots = getFrequencySnapshotStructure(0);
  getFrequencySnapshotStructure(0);
  
  time_snapshots_X = getTimeSnapshotStructure(0);
  time_snapshots_Y = getTimeSnapshotStructure(0);
  time_snapshots_Z = getTimeSnapshotStructure(0);
  epsilon_snapshots_X = getTimeSnapshotStructure(0);
  epsilon_snapshots_Y = getTimeSnapshotStructure(0);
  epsilon_snapshots_Z = getTimeSnapshotStructure(0);
  frequency_snapshots_X = getFrequencySnapshotStructure(0);
  frequency_snapshots_Y = getFrequencySnapshotStructure(0);
  frequency_snapshots_Z = getFrequencySnapshotStructure(0);
  
  all_snapshots = getGenericSnapshotStructure(0);
  
  excitations = struct(...
    'name', {}, ...
    'current_source', {},...
    'P1', {},...
    'P2', {},...
    'E', {},...
    'H', {},...
    'type', {},...
    'time_constant', {},...
    'amplitude', {},...
    'time_offset', {},...
    'frequency', {},...
    'param1', {},...
    'param2', {},...
    'template_filename', {},...
    'template_source_plane', {},...
    'template_target_plane', {},...
    'template_direction', {},...
    'template_rotation', {});
  
  boundaries = struct('name',{},'type',{},'position',{});
  box = struct('name',{},'lower',{},'upper',{});
  probe_list = struct('name',{},'position',{},'step',{},'E',{},'H',{},'J',{},'pow',{});
  
  block_list = getBlockStructure(0);
  sphere_list = getSphereStructure(0);
  cylinder_list = getCylinderStructure(0);
  rotation_list = getRotationStructure(0);
  
  % xmesh = [];
  % ymesh = [];
  % zmesh = [];
  % flag = [];
  % boundaries = [];
  %=====================================================================
  
  % ask for input file if not given
  if exist('filename','var') == 0
    disp('filename not given');
    [file,path] = uigetfile({'*.geo *.inp'},'Select a GEO or INP file');
    filename = [path,file];
  end
  
  % raise error in file not found
  existFileOutsideLoadPath(filename, true);
    
  % read the whole file as one string
  fulltext = fileread(filename);
  
  % remove comments
  pattern_stripcomments = '\*\*(?!name=).*\n';
  % does not seem to work anymore on Matlab 2013 and 2015?! (at least on BC3) :/
  cleantext =  regexprep(fulltext, pattern_stripcomments, '\n', 'lineanchors', 'dotexceptnewline', 'warnings');
  
  % extract blocks
  pattern_objects = '^(?<type>\w+)\s*(?<nameblob>[^\{\}]+)?\{(?<data>[^\{\}]*?)\}';
  if inoctave()
    [tokens_blocks, match_blocks, names_blocks] =  regexp(cleantext, pattern_objects, 'tokens', 'match', 'names', 'lineanchors');
    % this is slow!
    names_blocks = ScalarStructureToStructArray(names_blocks);
  else
    [tokens_blocks, match_blocks, names_blocks] =  regexp(cleantext, pattern_objects, 'tokens', 'match', 'names', 'lineanchors', 'warnings');
  end
  
  % process blocks
  %length_names_blocks = getNumberOfEntries(names_blocks);
  %disp(['length(names_blocks) = ', num2str(length(names_blocks))]);
  %disp(['length_names_blocks = ', num2str(length_names_blocks)]);
  
  for i = 1:length(names_blocks)
  
  %for i = 1:length_names_blocks
    % [type, nameblob, data] = getTokenValues(names_blocks, i);
    type = names_blocks(:,i).type;
    nameblob = names_blocks(:,i).nameblob;
  
    % extract object name if present
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
    
    % create data var for convenience, contains object data, excluding comments
    %data = names_blocks(:,i).data;
    
    % disp(['===>type = ',type]);
  
    %% deprecated complex data post-processing...
    %dataV = [];
    %% remove empty lines
    %lines = strread(data, '%s', 'delimiter', '\n')
    
    %%cellFlag = 1;
    
    %for L = 1:length(lines)
      %if ~length(lines{L})
        %continue; % empty line
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
    
    entry.name = name;
    entry.type = type;
    entry.data = strsplit_custom(strtrim(names_blocks(:,i).data));
    entries{length(entries)+1} = entry;
  
    switch upper(entry.type)
      case {'FREQUENCY_SNAPSHOT','SNAPSHOT'}
        % disp('Adding snapshot...');
        snapshot = add_snapshot(entry);
        all_snapshots = [ all_snapshots, snapshot ];
        if strcmpi(entry.type,'FREQUENCY_SNAPSHOT')
          snapshot = add_frequency_snapshot(entry);
          frequency_snapshots = [ frequency_snapshots snapshot ];
          if snapshot.plane == 1
            frequency_snapshots_X = [ frequency_snapshots_X snapshot ];
          elseif snapshot.plane == 2
            frequency_snapshots_Y = [ frequency_snapshots_Y snapshot ];
          else
            frequency_snapshots_Z = [ frequency_snapshots_Z snapshot ];
          end
        elseif strcmpi(entry.type,'SNAPSHOT')
          snapshot = add_time_snapshot(entry);
          % all time snapshots are stored as time snapshots, including "epsilon snapshots"
          time_snapshots = [ time_snapshots, snapshot ];
          if snapshot.plane == 1
              time_snapshots_X = [ time_snapshots_X snapshot ];
          elseif snapshot.plane == 2
              time_snapshots_Y = [ time_snapshots_Y snapshot ];
          else
              time_snapshots_Z = [ time_snapshots_Z snapshot ];
          end
          % additionally, we store epsilon snapshots separately for convenience
          if snapshot.eps == 1
            epsilon_snapshots = [ epsilon_snapshots snapshot ];
            if snapshot.plane == 1
              epsilon_snapshots_X = [ epsilon_snapshots_X snapshot ];
            elseif snapshot.plane == 2
              epsilon_snapshots_Y = [ epsilon_snapshots_Y snapshot ];
            else
              epsilon_snapshots_Z = [ epsilon_snapshots_Z snapshot ];
            end
          end
        else
          error('Sense, it makes none.');
        end
      case {'EXCITATION'}
        current_excitation = add_excitation(entry);
        excitations = [ excitations, current_excitation ];
      case {'XMESH'}
        structured_entries.xmesh = str2num_check_array(entry.data);
      case {'YMESH'}
        structured_entries.ymesh = str2num_check_array(entry.data);
      case {'ZMESH'}
        structured_entries.zmesh = str2num_check_array(entry.data);
      case {'FLAG'}
        structured_entries.flag = add_flag(entry);
      case {'BOUNDARY'}
        structured_entries.boundaries = add_boundary(entry);
      case {'PROBE'}
        probe = add_probe(entry);
        probe_list = [ probe_list probe ];
      case {'BOX'}
        structured_entries.box = add_box(entry);
      case {'SPHERE'}
        sphere = bfdtd_add_sphere(entry);
        sphere_list = [ sphere_list, sphere ];
        structured_entries.geometry_object_list{end+1} = sphere;
      case {'BLOCK'}
        block = bfdtd_add_block(entry);
        block_list = [ block_list, block ];
        structured_entries.geometry_object_list{end+1} = block;
      case {'CYLINDER'}
        cylinder = bfdtd_add_cylinder(entry);
        cylinder_list = [ cylinder_list, cylinder ];
        structured_entries.geometry_object_list{end+1} = cylinder;
      case {'ROTATION'}
        rotation = add_rotation(entry);
        rotation_list = [ rotation_list, rotation ];
        structured_entries.geometry_object_list{end+1} = rotation;
      otherwise
        % disp('Unknown type.');
    end % end of switch
  
  end %end of loop through blocks
  
  structured_entries.all_snapshots = [ structured_entries.all_snapshots, all_snapshots ];
  structured_entries.time_snapshots =  [structured_entries.time_snapshots, time_snapshots];
  structured_entries.epsilon_snapshots =  [structured_entries.epsilon_snapshots, epsilon_snapshots];
  structured_entries.frequency_snapshots =  [structured_entries.frequency_snapshots, frequency_snapshots];
  
  structured_entries.time_snapshots_X =  [structured_entries.time_snapshots_X, time_snapshots_X];
  structured_entries.time_snapshots_Y =  [structured_entries.time_snapshots_Y, time_snapshots_Y];
  structured_entries.time_snapshots_Z =  [structured_entries.time_snapshots_Z, time_snapshots_Z];
  
  structured_entries.epsilon_snapshots_X =  [structured_entries.epsilon_snapshots_X, epsilon_snapshots_X];
  structured_entries.epsilon_snapshots_Y =  [structured_entries.epsilon_snapshots_Y, epsilon_snapshots_Y];
  structured_entries.epsilon_snapshots_Z =  [structured_entries.epsilon_snapshots_Z, epsilon_snapshots_Z];
  
  structured_entries.frequency_snapshots_X =  [structured_entries.frequency_snapshots_X, frequency_snapshots_X];
  structured_entries.frequency_snapshots_Y =  [structured_entries.frequency_snapshots_Y, frequency_snapshots_Y];
  structured_entries.frequency_snapshots_Z =  [structured_entries.frequency_snapshots_Z, frequency_snapshots_Z];
  
  structured_entries.excitations =  [structured_entries.excitations, excitations];
  structured_entries.sphere_list =  [structured_entries.sphere_list, sphere_list];
  structured_entries.block_list =  [structured_entries.block_list, block_list];
  structured_entries.cylinder_list =  [structured_entries.cylinder_list, cylinder_list];
  structured_entries.rotation_list =  [structured_entries.rotation_list, rotation_list];
  structured_entries.probe_list =  [structured_entries.probe_list, probe_list];
  %structured_entries.geometry_object_list =  [structured_entries.geometry_object_list, geometry_object_list];
end

%deprecated
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

%deprecated
%function N = getNumberOfEntries(names_blocks)
  %% octave:
  %N = length(names_blocks.type);
  %% matlab:
%end

function ret = getRotationStructure(N)
  T = cell(1, N);
  T(:) = {'ROTATION'};
  f = cell(1, N);
  f(:) = {-1};
  ret = struct('type', T, 'name', f, 'axis_point', f, 'axis_direction', f, 'angle_degrees', f);
end

function flag = add_flag(entry)
  flag.name = entry.name;
  flag.iMethod = str2num_check(entry.data{1});
  flag.propCons = str2num_check(entry.data{2});
  flag.flagOne = str2num_check(entry.data{3});
  flag.flagTwo = str2num_check(entry.data{4});
  flag.numSteps = str2num_check(entry.data{5});
  flag.stabFactor = str2num_check(entry.data{6});
  flag.id = getString(entry.data, 7, '_id_');
end

function boundaries = add_boundary(entry)
  boundaries.name = entry.name;
  for i = 1:6
    boundaries(i).type = str2num_check(entry.data{4*(i-1)+1});
    a = str2num_check(entry.data{4*(i-1)+2});
    b = str2num_check(entry.data{4*(i-1)+3});
    c = str2num_check(entry.data{4*(i-1)+4});
    boundaries(i).position = [a,b,c];
  end
end

function box = add_box(entry)
  box.name = entry.name;
  [box.lower, status] = str2num_check_array(entry.data, 1, 3);
  [box.upper, status] = str2num_check_array(entry.data, 4, 6);
end

function rotation = add_rotation(entry)
  rotation = getRotationStructure(1);
  rotation.name = entry.name;
  idx = 1;
  rotation.axis_point = str2num_check_array(entry.data, idx, idx+2); idx = idx+3;
  rotation.axis_direction = str2num_check_array(entry.data, idx, idx+2); idx = idx+3;
  rotation.angle_degrees = getNumber(entry.data, idx); idx = idx+1;
end

function probe = add_probe(entry)
  probe.name = entry.name;
  idx = 1;
  probe.position = str2num_check_array(entry.data, idx, idx+2); idx = idx+3;
  probe.step = getNumber(entry.data, idx); idx = idx+1;
  probe.E = str2num_check_array(entry.data, idx, idx+2); idx = idx+3;
  probe.H = str2num_check_array(entry.data, idx, idx+2); idx = idx+3;
  probe.J = str2num_check_array(entry.data, idx, idx+2); idx = idx+3;
  probe.pow = getNumber(entry.data, idx); idx = idx+1;
end

% TODO: check necessity of those multiple snapshot adding functions.
function snapshot = add_frequency_snapshot(entry)
  snapshot.name = entry.name;
  idx = 1;
  snapshot.first = getNumber(entry.data, idx); idx = idx+1;
  snapshot.repetition = getNumber(entry.data, idx); idx = idx+1;
  snapshot.interpolate = getNumber(entry.data, idx); idx = idx+1;
  snapshot.real_dft = getNumber(entry.data, idx); idx = idx+1;
  snapshot.mod_only = getNumber(entry.data, idx); idx = idx+1;
  snapshot.mod_all = getNumber(entry.data, idx); idx = idx+1;
  snapshot.plane = getNumber(entry.data, idx); idx = idx+1;
  snapshot.P1 = str2num_check_array(entry.data, idx, idx+2); idx = idx+3;
  snapshot.P2 = str2num_check_array(entry.data, idx, idx+2); idx = idx+3;
  snapshot.frequency = getNumber(entry.data, idx); idx = idx+1;
  snapshot.starting_sample = getNumber(entry.data, idx); idx = idx+1;
  snapshot.E = str2num_check_array(entry.data, idx, idx+2); idx = idx+3;
  snapshot.H = str2num_check_array(entry.data, idx, idx+2); idx = idx+3;
  snapshot.J = str2num_check_array(entry.data, idx, idx+2); idx = idx+3;
  
  % add additional info for easier postprocessing (proper class+method setup would make this obsolete)
  snapshot = addSnapshotInfo(snapshot);
end

function snapshot = add_time_snapshot(entry)
  snapshot.name = entry.name;
  idx = 1;
  snapshot.first = getNumber(entry.data, idx); idx = idx+1;
  snapshot.repetition = getNumber(entry.data, idx); idx = idx+1;
  snapshot.plane = getNumber(entry.data, idx); idx = idx+1;
  snapshot.P1 = str2num_check_array(entry.data, idx, idx+2); idx = idx+3;
  snapshot.P2 = str2num_check_array(entry.data, idx, idx+2); idx = idx+3;
  snapshot.E = str2num_check_array(entry.data, idx, idx+2); idx = idx+3;
  snapshot.H = str2num_check_array(entry.data, idx, idx+2); idx = idx+3;
  snapshot.J = str2num_check_array(entry.data, idx, idx+2); idx = idx+3;
  snapshot.power = getNumber(entry.data, idx); idx = idx+1;
  snapshot.eps = getNumber(entry.data, idx, 0); idx = idx+1;
  
  % add additional info for easier postprocessing (proper class+method setup would make this obsolete)
  snapshot = addSnapshotInfo(snapshot);
end

function snapshot = add_snapshot(entry)
  % to create a list of all snapshots together, usefulness dubious...
  if strcmpi(entry.type,'FREQUENCY_SNAPSHOT')
    snapshot = add_frequency_snapshot(entry);
    % add time_snapshot-only fields
    snapshot.power = -1;
    snapshot.eps = -1;
  elseif strcmpi(entry.type,'SNAPSHOT')
    snapshot = add_time_snapshot(entry);
    % add frequency_snapshot-only fields
    snapshot.interpolate = -1;
    snapshot.real_dft = -1;
    snapshot.mod_only = -1;
    snapshot.mod_all = -1;
    snapshot.frequency = -1;
    snapshot.starting_sample = -1;
  else
    error('Sense, it makes none.');
  end
end

function current_excitation = add_excitation(entry)
  current_excitation.name = entry.name;
  current_excitation.current_source = str2num_check(entry.data{1});
  current_excitation.P1 = str2num_check_array(entry.data, 2, 4);
  current_excitation.P2 = str2num_check_array(entry.data, 5, 7);
  current_excitation.E = str2num_check_array(entry.data, 8, 10);
  current_excitation.H = str2num_check_array(entry.data, 11, 13);
  current_excitation.type = str2num_check(entry.data{14});
  current_excitation.time_constant = str2num_check(entry.data{15});
  current_excitation.amplitude = str2num_check(entry.data{16});
  current_excitation.time_offset = str2num_check(entry.data{17});
  current_excitation.frequency = str2num_check(entry.data{18});
  current_excitation.param1 = str2num_check(entry.data{19});
  current_excitation.param2 = str2num_check(entry.data{20});
  current_excitation.template_filename = getString(entry.data, 21, 'template_filename');
  current_excitation.template_source_plane = getString(entry.data, 22, 'x');
  current_excitation.template_target_plane = getString(entry.data, 23, 'x');
  current_excitation.template_direction = getNumber(entry.data, 24, 0);
  current_excitation.template_rotation = getNumber(entry.data, 25, 0);
end
