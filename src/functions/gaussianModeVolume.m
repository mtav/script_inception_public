function Veff = gaussianModeVolume(rx_list, ry_list, rz_list, alpha)
  % returns:
  % Veff = int(int(int( f(x,y,z), x, -rx, rx), y, -ry, ry), z, -rz, rz);
  % where f(x,y,z) is a 3D gaussian:
  % f(x,y,z) = exp(-alpha*(x^2+y^2+z^2))
  
  func_gaussian3D = @(x,y,z) exp(-alpha.*(x.^2+y.^2+z.^2));
  func_Veff = @(rx,ry,rz) integral3(func_gaussian3D, -rx, rx, -ry, ry, -rz, rz);
  
  Veff = arrayfun(func_Veff, rx_list, ry_list, rz_list);
  
end
