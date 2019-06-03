function block = bfdtd_add_block(entry)
  block = getBlockStructure(1);
  block.name = entry.name;
  XL = str2num_check(entry.data{1});
  YL = str2num_check(entry.data{2});
  ZL = str2num_check(entry.data{3});
  block.lower = [XL, YL, ZL];

  XU = str2num_check(entry.data{4});
  YU = str2num_check(entry.data{5});
  ZU = str2num_check(entry.data{6});
  block.upper = [XU, YU, ZU];
  block.permittivity = str2num_check(entry.data{7});
  block.conductivity = str2num_check(entry.data{8});
  
  block.center = (block.upper + block.lower)/2;
end
