function N = getNToReachThickness(delta_0, delta_max, ratio)
  % IMPORTANT: It is not always possible to reach a given thickness once delta_0, delta_max, ratio have been fixed.
  N = log(delta_max/delta_0)/log(ratio);
end
