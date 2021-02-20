function mag = getMagFromScreenSizeInMicrons(ScreenSizeInMicrons)
  % function mag = getMagFromScreenSizeInMicrons(ScreenSizeInMicrons)  
  FIB_infos_struct = FIB_infos();
  mag = FIB_infos_struct.HFW_at_mag1_in_mum ./ ScreenSizeInMicrons;
end
