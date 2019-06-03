function N = getNToReachPosition(delta_0, Delta_X, ratio)
  N = (log((Delta_X/delta_0)*(ratio-1) + ratio)/log(ratio)) - 1;
end
