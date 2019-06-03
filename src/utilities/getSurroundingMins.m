function [ idx_min_left, idx_min_right ] = getSurroundingMins(y,i)

  ref = y(i);
  idx_min_left = 1;
  for idx = i:-1:1
    if y(idx)>ref
      idx_min_left = idx+1;
      break;
    end
    ref = y(idx);
  end
  
  ref = y(i);
  idx_min_right = length(y);
  for idx = i:1:length(y)
    if y(idx)>ref
      idx_min_right = idx-1;
      break;
    end
    ref = y(idx);
  end
  
end
