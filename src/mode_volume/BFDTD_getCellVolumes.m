function [dV, dX, dY, dZ] = BFDTD_getCellVolumes(xmesh, ymesh, zmesh)
  dx = diffCentered(xmesh);
  dy = diffCentered(ymesh);
  dz = diffCentered(zmesh);
  [dX, dY, dZ] = meshgrid(dx, dy, dz);
  dV = dX .* dY.* dZ;
end
