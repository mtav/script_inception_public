function mymesh = getTaperedMesh_Direct(delta_0, ratio, N)
  % mymesh = getTaperedMesh_Direct(delta_0, ratio, N)
  mymesh = [];
  for i = 0:N
    mymesh(end+1) = getPositionAtN(delta_0, i, ratio);
  end
end
