function  ret = lookup_in_table(TABLE, val, varargin)
  % lookup table for a function from 1 dimension to Ndims dimensions, where TABLE is of size (Nvals, 1 + Ndims)
  
  p = inputParser();
  p = inputParserWrapper(p, 'addRequired', 'TABLE', @isnumeric);
  p = inputParserWrapper(p, 'addRequired', 'val', @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'exit_on_error', true, @islogical);
  p = inputParserWrapper(p, 'parse', TABLE, val, varargin{:});
  
  if size(TABLE, 1) < 1 || size(TABLE, 2)<2
    TABLE
    error('Table must have at least 1 row and 2 columns.');
  end
  
  % create a return array
  ret = NaN*ones([size(val), size(TABLE,2)-1]);
  
  for idx_val = 1:numel(val)
    sub_indices = ind2sub_array(size(val), idx_val);
    sub_indices = num2cell(sub_indices);

    i1 = find(TABLE(:,1)==val(idx_val));

    if length(i1)==1
      ret(sub_indices{:},:) = TABLE(i1,2:end);
    else
    
      if p.Results.exit_on_error
        TABLE
        if length(i1)==0
          error('Value %f not found in table.', val(idx_val));
        else
          error('Multiple entries found for value %f in table.', val(idx_val));
        end
      end
      
    end
    
  end
  
end
