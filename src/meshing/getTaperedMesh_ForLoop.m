function mymesh = getTaperedMesh_ForLoop(delta_0, ratio, N)
  % get the corresponding mesh
  mymesh = [0];
  s = delta_0;
  for i = 1:N
      s = ratio*s;
      mymesh(end+1) = mymesh(end) + s;
  end
end
