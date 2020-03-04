function grating_calibration(a_um)

  if exist('a_um','var')==0
    a_um = 1000/600;
  end

  lambda_range_VIS = [0.340, 0.800];
  lambda_range_IR = [0.900, 1.700];

  subplot(1,2,1);
  grating_calibration_plot(a_um, lambda_range_VIS);
  subplot(1,2,2);
  grating_calibration_plot(a_um, lambda_range_IR);

end
