function LUT = createEpsilonShiftLookupTable(outfile, value_list, value_old, value_new, varargin)
  % function LUT = createEpsilonShiftLookupTable(outfile, value_list, value_old, value_new, varargin)
  %
  % Creates an epsilon lookup table for use with calculateModeVolume() for example.
  % This is a simple .prn file with two columns, the first one being the source epsilon values and the second one the new epsilon values.
  % 
  % This function creates a table where each input epsilon is associated with zero, except for "value_old", which is associated with "value_new - value_old".
  %
  % Example:
  % >> LUT = createEpsilonShiftLookupTable('/tmp/foo.out', [1,2,3,2.5,2,4], 2.2, 22, 'interpret_as_refractive_index', true, 'exact_match', false)
  % LUT =
  %   1.00000     0.00000
  %   4.00000   479.16000
  %   6.25000     0.00000
  %   9.00000     0.00000
  %  16.00000     0.00000

  % create parser
  p = inputParser();
  p = inputParserWrapper(p, 'addRequired', 'outfile', @ischar);
  p = inputParserWrapper(p, 'addRequired', 'value_list', @isnumeric);
  p = inputParserWrapper(p, 'addRequired', 'value_old', @isnumeric);
  p = inputParserWrapper(p, 'addRequired', 'value_new', @isnumeric);
  p = inputParserWrapper(p, 'addParamValue', 'interpret_as_refractive_index', false, @islogical);
  p = inputParserWrapper(p, 'addParamValue', 'exact_match', true, @islogical);  
  p = inputParserWrapper(p, 'parse', outfile, value_list, value_old, value_new, varargin{:});
  
  % turn into column vector and remove duplicates
  value_list = unique(value_list(:));
  
  % convert from index to epsilon if necessary
  if p.Results.interpret_as_refractive_index
    value_list = value_list.^2;
    value_old = value_old.^2;
    value_new = value_new.^2;
  end
  
  % initialize lookup table
  LUT = [value_list, zeros(size(value_list))];
  
  % locate source value matching value_old
  if p.Results.exact_match
    match = find(value_old==value_list);
  else
    [match, values, abs_err, sub_indices, minerr] = closestInd(value_list, value_old);
  end

  % error out if failed to find one and only one match
  if length(match)~=1
    value_list
    match
    error('Failed to properly match value_old = %f in value_list.', value_old);
  end
  
  % change the target value for the matched source value
  LUT(match, 2) = value_new - value_old;

  % write table to a .prn file
  header_arg = {'epsilon', 'delta_epsilon'};
  writePrnFile(outfile, header_arg, LUT);

  % deprecated code:
  % TODO: Until we use interp1-based solutions instead of lookup_in_table(), the first column needs to have .3f precision, so we use a custom writer.
  %writePrnFile(outfile, header_arg, LUT, 'precision', '%.3f');
  %fid = fopen(outfile, 'w');
  %fprintf(fid, 'epsilon delta_epsilon\n');
  %for idx = 1:size(LUT, 1)
    %fprintf(fid, '%.3f %f\n', LUT(idx, 1), LUT(idx, 2));
  %end
  %fclose(fid);
  
end
