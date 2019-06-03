function ratio = getAlphaToReachPosition(delta_0, Delta_X, N)
  % the equation to solve is:
  % [1] * ratio^(N+1) + [-1 - Delta_X/delta_0)] * ratio^1 + [Delta_X/delta_0] * ratio^0 = 0
  %
  % IMPORTANT: There might not always be a real positive >1 solution, especially if N*delta_0 > Delta_X.
  % In the case of multiple solutions, you can use selectRatio(ratio_list, err, ratio_max).
  
  if N==0
    ratio = 1;
  else
    coeffs = [1, zeros(1, N-1), -1 - Delta_X/delta_0, Delta_X/delta_0]
    ratio = roots(coeffs);
  end
end
