%%%%%
% checking functions

function check_results = checkMeshUpUp(mymesh, delta_0, delta_max, ratio_max, Delta_X, err)
  % TODO: make the check work for all possible cases, i.e. up-up, down-down, up-down, down-up (and maybe even check against those (requires external limits))
  %
  % mesh notations:
  %   position:        x0----------x1---------x2--------........----------x(end-1)----------x(end)
  %   thickness: d0----------d1---------d2---------d3---........d(end-1)------------d(end)----------d(right)
  %   ratio:           a0----------a1---------a2--------........----------a(end-1)----------a(end)
  %
  
  if length(mymesh) == 0
    error('mesh is empty');
  end
  
  %%% preparations
  
  % [d1,...,d(end)]
  disp('checkMeshUpUp: delta')
  delta = diff(mymesh)
  disp('checkMeshUpUp: delta_max - delta')
  delta_max - delta
  
  % [a1,...,a(end-1)]
  [direct_ratio, normalized_ratio] = getThicknessRatios(mymesh)

  %%% required
  
  % required for pass (5 boolean tests):
  %   reach start edge:
  %     x(0) == 0
  check_results.required.start_edge_reached = (mymesh(1) == 0);
  %   reach end edge:
  %     x(end) == Delta_X
  check_results.required.end_edge_reached = (mymesh(end) == Delta_X);
  %   do not exceed maximum thickness:
  %     delta(i=0:end) <= delta_max
  check_results.required.less_than_delta_max = all(delta <= delta_max+err);
  %   do not exceed maximum ratio:
  %     1/ratio_max <= ratio(i=1:end-1) <= ratio_max
  check_results.required.less_than_ratio_max = all( (1/(ratio_max+err) <= direct_ratio) & (direct_ratio <= (ratio_max+err)) );
  %   do not exceed maximum ratio at left edge (but going under 1/ratio_max is acceptable):
  %     delta(1) <= ratio*delta_0
  check_results.required.less_than_ratio_max_at_start = (delta(1) <= ratio_max*delta_0);
  
  % increasing thcknesses only (up-up case only)
  check_results.required.thickness_increasing_only = checkMeshDeltaIncreasesOnly(mymesh, err);
  
  check_results.required.pass = check_results.required.start_edge_reached && check_results.required.end_edge_reached && check_results.required.less_than_delta_max && check_results.required.less_than_ratio_max && check_results.required.less_than_ratio_max_at_start && check_results.required.thickness_increasing_only;
  
  %%% optional

  % optional (1 boolean test + 2 triple-case tests):
  %   delta_0 <= delta(i=0:end)
  check_results.optional.greater_than_delta_0 = all( delta_0 <= delta );
  %
  % edge ranges:
  %  d0/a     d0    a*d0
  %    |       |     |
  % 0  1   1   2  2  2   BAD
  %
  %   ratio(i=0) = a0 = d1/d0 regions:
  %     (0) < 1/ratio_max <= (1) < 1 <= (2) <= ratio_max:
  %
  %      0) d1 < d0/a
  %      1) d0/a <= d1 < d0
  %      2) d0 <= d1 <= a*d0
  %
  if delta(1) < delta_0/ratio_max
    check_results.optional.start_edge_category = 0;
  elseif (delta_0/ratio_max <= delta(1)) && (delta(1) < delta_0)
    check_results.optional.start_edge_category = 1;
  else % delta_0 <= delta(1) <= ratio_max*delta_0
    check_results.optional.start_edge_category = 2;
  end
  
  %
  % dmax/a     dmax
  %    |         |
  % 0  1    1    2    BAD
  %
  %   ratio(i=end) = a(end) = d(right)/d(end) ~ delta_max/d(end) regions:
  %     (2) = 1 < (1) <= ratio_max < (0):
  %     
  %     0) d(end) < delta_max/ratio_max
  %     1) delta_max/ratio_max <= d(end) < delta_max
  %     2) d(end) == delta_max
  %
  if delta(end) < delta_max/ratio_max
    check_results.optional.end_edge_category = 0;
  elseif (delta_max/ratio_max <= delta(end)) && (delta(end) < delta_max)
    check_results.optional.end_edge_category = 1;
  else delta(end) == delta_max
    check_results.optional.end_edge_category = 2;
  end
    
end

function ret = checkMeshDeltaIncreasesOnly(mymesh, err)
  ret = true;
  thickness = diff(mymesh);
  for idx = 2:length(thickness)
    if thickness(idx) - thickness(idx-1) < -err
      ret = false;
      return;
    end
  end
end

function ret = checkMeshDeltaDecreasesOnly(mymesh, err)
  ret = true;
  thickness = diff(mymesh);
  for idx = 2:length(thickness)
    if thickness(idx) - thickness(idx-1) > err
      ret = false;
      return;
    end
  end
end
