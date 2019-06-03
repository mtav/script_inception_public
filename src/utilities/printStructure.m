function ret = printStructure(input_structure, varargin)
  % prints the contents of a structure
  % TODO: test on Matlab + how it compares to simpler alternatives like disp+diary
  % TODO: make output look nicer, maybe like standard Octave structure display
  
  % create parser
  p = inputParser();
  p = inputParserWrapper(p, 'addRequired', 'input_structure', @isstruct);
  p = inputParserWrapper(p, 'addParamValue', 'prefix', '', @ischar);
  p = inputParserWrapper(p, 'addParamValue', 'struct_prefix', '', @ischar);
  p = inputParserWrapper(p, 'addParamValue', 'use_struct_prefix', false, @islogical);
  p = inputParserWrapper(p, 'addParamValue', 'indented', true, @islogical);
  p = inputParserWrapper(p, 'addParamValue', 'sectioned', true, @islogical);
  p = inputParserWrapper(p, 'addParamValue', 'indent_char', '  ', @ischar);
  p = inputParserWrapper(p, 'addParamValue', 'indent_depth', 0, @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'warnings', false, @islogical);
  p = inputParserWrapper(p, 'parse', input_structure, varargin{:});
  
  key_list = fieldnames(input_structure);
  
  ret = '';
  
  indent_string = repmat(p.Results.indent_char, 1, p.Results.indent_depth);
  
  % create full prefix
  prefix_full = '';
  if p.Results.indented
    prefix_full = [prefix_full, indent_string];
  end
  prefix_full = [prefix_full, p.Results.prefix];
  if p.Results.use_struct_prefix
    prefix_full = [prefix_full, p.Results.struct_prefix];
  end
  
  % loop through fields/keys
  for idx = 1:numel(key_list)
    
    key = key_list{idx};
    value = getfield(input_structure, key);
    
    % structure cases
    if isstruct(value)
      
      struct_prefix = sprintf('%s%s.', p.Results.struct_prefix, key);
      
      if p.Results.sectioned
        ret = [ret, sprintf('\n%s%s:\n', prefix_full, key)];
      end
      
      value_string = printStructure(value,...
                    'prefix', p.Results.prefix,...
                    'struct_prefix', struct_prefix,...
                    'use_struct_prefix', p.Results.use_struct_prefix,...
                    'indented', p.Results.indented,...
                    'sectioned', p.Results.sectioned,...
                    'indent_char', p.Results.indent_char,...
                    'indent_depth', p.Results.indent_depth+1);
      ret = [ret, value_string];
      if idx < numel(key_list)
        ret = [ret, sprintf('\n')];
      end
      continue
    
    % non-structure cases
    elseif isnumeric(value) && isscalar(value)
      value_string = num2str(value);
    elseif islogical(value) && isscalar(value)
      % TODO: true/false strings, but support arrays?
      value_string = num2str(value);
    elseif ischar(value)
      value_string = value;
    elseif iscellstr(value)
      % TODO: create/find functions to do these basic things...
      value_string = '{';
      for idx_value = 1:numel(value)
        value_string = [value_string, value{idx_value}];
        if idx_value < numel(value)
          value_string = [value_string, ', '];
        end
      end
      value_string = [value_string, '}'];
    elseif isnumeric(value) && numel(value) < 10
      value_string = '[';
      for idx_value = 1:numel(value)
        value_string = [value_string, num2str(value(idx_value))];
        if idx_value < numel(value)
          value_string = [value_string, ', '];
        end
      end
      value_string = [value_string, ']'];
      
    % unhandled cases
    else
      if p.Results.warnings
        warning('Skipping %s%s of class %s and size %s', p.Results.struct_prefix, key, class(value), num2str(size(value)));
      end
      continue
    
    end
    
    % create key string
    key_string = [prefix_full, key];
    
    ret = [ret, key_string, ' = ', value_string];
    if idx < numel(key_list)
      ret = [ret, sprintf('\n')];
    end
    
  end
  
end
