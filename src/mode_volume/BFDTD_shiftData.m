function ret = BFDTD_shiftData(ret, shift)
  % shifts the data in a BFDTD volumetric data structure, so that x=x-shift(1), y=y-shift(2), z=z-shift(3)
  ret.data.X = ret.data.X - shift(1);
  ret.data.Y = ret.data.Y - shift(2);
  ret.data.Z = ret.data.Z - shift(3);
  
  % .. todo:: these should really be updated using the index values and make a vector form available
  % .. todo:: or maybe have a general update function recalculating maxima, etc based on shift
  % .. todo:: or shift during load... (but annoying if data was saved to .mat after load)
  ret.MV.info_full.MaximumEmod2.x = ret.MV.info_full.MaximumEmod2.x - shift(1);
  ret.MV.info_full.MaximumEmod2.y = ret.MV.info_full.MaximumEmod2.y - shift(2);
  ret.MV.info_full.MaximumEmod2.z = ret.MV.info_full.MaximumEmod2.z - shift(3);
  
  ret.info.defect_properties.object.center = ret.info.defect_properties.object.center - shift;
  
end
