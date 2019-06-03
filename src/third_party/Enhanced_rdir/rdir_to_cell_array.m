function ret = rdir_to_cell_array(rdir_output)
  % converts rdir output to a cell array
  % TODO: There might be a better way to do this, else a general get by field tool would be useful?
  %
  % example:
  %   rdir_output = rdir(['*/part_*', '/*.inp']);
  %   ret = rdir_to_cell_array(rdir_output);
  
  ret = {};
  for i = 1:length(rdir_output)
    ret{i} = rdir_output(i).name;
  end
end
