function [resolution_mum_per_pxl, HFW_mum, FIB_infos_struct] = getResolution(mag)
  % Usage:
  %   [res, HFW, FIB_infos_struct] = getResolution(mag)
  %
  % Valid pixel ranges:
  %   X: 0-4095 -> width: 4096 pixels
  %   Y: 280-3816 -> height: 3537 pixels

  FIB_infos_struct = FIB_infos();
  
  HFW_mum = FIB_infos_struct.HFW_at_mag1_in_mum ./ mag; % Width of the horizontal scan (mum).
  resolution_mum_per_pxl = HFW_mum ./ FIB_infos_struct.Npixels_X; % size of each pixel (mum/pxl).
  
  FIB_infos_struct.mag = mag;
  FIB_infos_struct.resolution_mum_per_pxl = resolution_mum_per_pxl;
  
  FIB_infos_struct.size_X_mum = HFW_mum;
  FIB_infos_struct.size_Y_mum = FIB_infos_struct.Npixels_Y .* FIB_infos_struct.resolution_mum_per_pxl;
  
end
