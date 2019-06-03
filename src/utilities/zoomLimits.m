function new_limits = zoomLimits(limits, zoom)
  % simple script to scale limits up or down assymetrically
  % examples:
  %   >> zoomLimits([1,2], [0.5,0.5])
  %     ans = 1.2500    1.7500
  %   >> zoomLimits([1,2], [0.5,1])
  %     ans = 1.2500    2.0000
  %   >> zoomLimits([1,2], [1,0.5])
  %     ans = 1.0000    1.7500
  
  N_limits = length(limits);
  if mod(N_limits, 2) ~= 0
    error('limits must have an even number of elements.');
  end
  
  N_zoom = length(zoom);
  if mod(N_zoom, 2) ~= 0
    error('zoom must have an even number of elements.');
  end
  
  new_limits = [];
  for idx = 1:2:N_limits
    L = limits(idx:idx+1);
    Z = zoom(idx:idx+1);
    m = mean(L);
    new_limits(idx:idx+1) = m + Z .* (L - m);
  end
  
end
