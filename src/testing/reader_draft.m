% test with:
% [ entries ] = reader_draft('test.inp'); for i=1:length(entries);fprintf('%s\n',entries{i}.name);end;
function [ entries ] = reader_draft(filename)
  entries = {};

  % read the whole file as one string
  fulltext = fileread(filename);

  % remove comments
  pattern_stripcomments = '\*\*(?!name=).*\n';
  cleantext =  regexprep(fulltext, pattern_stripcomments, '\n', 'lineanchors', 'dotexceptnewline', 'warnings');

  % extract blocks
  pattern_objects = '^(?<type>\w+)\s*(?<nameblob>[^\{\}]+)?\{(?<data>[^\{\}]*?)\}';
  [tokens_blocks match_blocks names_blocks] =  regexp(cleantext, pattern_objects, 'tokens', 'match', 'names', 'lineanchors', 'warnings');

  % process blocks
  %disp(['length(names_blocks) = ', num2str(length(names_blocks))]);
  for i = 1:length(names_blocks)

    type = names_blocks(:,i).type;
    nameblob = names_blocks(:,i).nameblob;
    
    name = '';
    if strcmpi(nameblob,'') == 0
      pattern_nameblob = '\*\*name=(?<name>.*)';
      [tokens_nameblob match_nameblob names_nameblob] =  regexp(nameblob, pattern_nameblob, 'tokens', 'match', 'names', 'lineanchors', 'warnings');
      if length(names_nameblob.name) > 0
        name = strtrim(names_nameblob.name);
      end
    end
    
    data = names_blocks(:,i).data;
    % disp(['===>type = ',type]);

    dataV = [];
    % remove empty lines
    lines = strread(data,'%s','delimiter','\n');
    cellFlag = 0;
    for L = 1:length(lines)
      if ~length(lines{L})
        continue;
      end

      num_val = str2num(lines{L});
      %L
      %num_val
            
      str_val = strtrim(lines{L}); % trim string
      str_val = str_val(str_val ~= '"');% remove double quotes

      % TODO: Check if this can't be simplified, or if it's even necessary.
      if cellFlag
        if length(num_val)  %% num_val is num
          dataV{length(dataV)+1} = num_val;
        else           %% num_val is not num
          dataV{length(dataV)+1} = str_val;
        end
      else
         if length(num_val)  %% num_val is num
          dataV = [dataV,num_val];
        else           %% num_val is not num
          cellFlag = 1;
          dataV = num2cell(dataV);
          dataV{length(dataV)+1} = str_val;
        end
      end
    end % end of loop through lines

    entry.name = name;
    entry.type = type;
    entry.data = dataV';
    entries{length(entries)+1} = entry;
  end % end of loop through blocks

end
