function [x, status] = str2num_check_array(data, index_min, index_max)
  % TODO: could pass an index list... and merge with getNumber/String... Just make sure discontinuous index lists work properly!!! (with alloc for speed)
  % TODO: Should return number of entries read to update data index (push/pop system would be helpful...)
  
  if ~exist('index_min', 'var')
    index_min = 1;
  end
  if ~exist('index_max', 'var')
    index_max = length(data);
  end
  
  N = index_max-index_min+1;
  x = zeros(1, N);
  for idx = 1:N
    [x(idx), status] = str2num_check(data{index_min+(idx-1)});
  end
end
