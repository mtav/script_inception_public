function volume = sphereVolume(sphere_structure)
  volume = (4/3)*pi*(sphere_structure.outer_radius.^3) - (4/3)*pi*(sphere_structure.inner_radius.^3);
end
