function cylinder = bfdtd_add_cylinder(entry)
  cylinder = getCylinderStructure(1);
  cylinder.name = entry.name;
  cylinder.center = str2num_check_array(entry.data, 1, 3);
  cylinder.inner_radius = str2num_check(entry.data{4});
  cylinder.outer_radius = str2num_check(entry.data{5});
  cylinder.height = str2num_check(entry.data{6});
  cylinder.permittivity = str2num_check(entry.data{7});
  cylinder.conductivity = str2num_check(entry.data{8});
  cylinder.angle = getNumber(entry.data, 9, 0);
end
