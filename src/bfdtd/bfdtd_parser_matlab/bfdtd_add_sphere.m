function sphere = bfdtd_add_sphere(entry)
  sphere = getSphereStructure(1);
  sphere.name = entry.name;
  idx = 1;
  sphere.center = str2num_check_array(entry.data, idx, idx+2); idx = idx+3;
  sphere.outer_radius = getNumber(entry.data, idx); idx = idx+1;
  sphere.inner_radius = getNumber(entry.data, idx); idx = idx+1;
  sphere.permittivity = getNumber(entry.data, idx); idx = idx+1;
  sphere.conductivity = getNumber(entry.data, idx); idx = idx+1;
end
