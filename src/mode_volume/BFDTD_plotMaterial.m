function BFDTD_plotMaterial(ret, limits)

  SX = ret.MV.info_full.MaximumEmod2.x;
  SY = ret.MV.info_full.MaximumEmod2.y;
  SZ = ret.MV.info_full.MaximumEmod2.z;
  %if ~exist('SX', 'var')
    %SX = mean(getRange(X));
  %end
  %if ~exist('SY', 'var')
    %SY = mean(getRange(Y));
  %end
  %if ~exist('SZ', 'var')
    %SZ = mean(getRange(Z));
  %end
  plotVolumetricData(ret.data.X,ret.data.Y,ret.data.Z, ret.data.D(:,:,:,1), SX, SY, SZ);
  plot3_xline(SX,'y--');
  plot3_yline(SY,'y--');
  plot3_zline(SZ,'y--');
  xlim([limits(1),limits(2)]);
  ylim([limits(3),limits(4)]);
  zlim([limits(5),limits(6)]);
  plot3_xline(SX,'y--');
  plot3_yline(SY,'y--');
  plot3_zline(SZ,'y--');
end
