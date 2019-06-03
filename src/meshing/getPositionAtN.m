function position = getPositionAtN(delta_0, N, ratio)
  position = ( (ratio^(N+1)-ratio)/(ratio-1) ) * delta_0;
end
