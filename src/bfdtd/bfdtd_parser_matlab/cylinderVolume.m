function volume = cylinderVolume(cylinder_structure)
  volume = ((pi*cylinder_structure.outer_radius.^2) - (pi*cylinder_structure.inner_radius.^2)) * cylinder_structure.height;
end
