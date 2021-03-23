function FIB_infos_struct = FIB_infos()
  % Returns infos about the FEI Strata FIB201.
  %
  % Usage:
  %   FIB_infos_struct = FIB_infos()
  
  FIB_infos_struct = struct();
  FIB_infos_struct.valid_pixel_range_X = [0, 4095];
  FIB_infos_struct.valid_pixel_range_Y = [280, 3816];
  
  FIB_infos_struct.Npixels_X = diff(FIB_infos_struct.valid_pixel_range_X) + 1;
  FIB_infos_struct.Npixels_Y = diff(FIB_infos_struct.valid_pixel_range_Y) + 1;
  
  FIB_infos_struct.HFW_at_mag1_in_mum = 304000;

  FIB_infos_struct.standard_magnifications = [244,
    500,
    1000,
    2000,
    5000,
    10000,
    20000,
    50000,
    100000,
    200000];

    A = [1 8;
      4 12;
      11 15;
      70 25;
      150 35;
      350 55;
      1000 80;
      2700 120;
      6600 270;
      11500 500];
    
    beamCurrent_pA = A(:,1);
    beamDiameter_nm = A(:,2);
    beamDiameter_mum = beamDiameter_nm.*1e-3;
    
    FIB_infos_struct.beamInfos = table(beamCurrent_pA, beamDiameter_nm, beamDiameter_mum);

end
