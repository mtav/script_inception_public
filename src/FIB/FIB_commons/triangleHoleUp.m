function [dwell_vector,X,Y] = triangleHoleUp(beamCurrent,res,dwell,x_center,y_center,x_size,y_size)
  % size of circles in nm as a function of the beamcurrent
  spotSizes = [1 8;
  4 12;
  11 15;
  70 25;
  150 35;
  350 55;
  1000 80;
  2700 120;
  6600 270;
  11500 500;
  ];
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  rep=1;
  beamCurrent=1; %Beam current.
  % vertical overlap of circles as a proportion of their diameter
  overlap=0.50;
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  
  % size of a circle in mum
  spotSize = spotSizes(find(spotSizes==beamCurrent),2)*1e-3;
  
  % vertical stepping distance
  BeamStep_Y = max(round((spotSize-spotSize*overlap)/res),1);
  % horizontal stepping distance
  BeamStep_X = BeamStep_Y;
  
  W_pxl = round(x_size/res);
  H_pxl = round(y_size/res);
  
  Xp = 1:BeamStep_X:W_pxl;
  
  dwell_vector = [];
  X = [];
  Y = [];
  
  for m = 1:length(Xp);
    L_pxl = H_pxl - abs(Xp(m)-0.5*W_pxl)*(2*H_pxl/W_pxl);
    Yp = 1:BeamStep_Y:L_pxl;
    if (mod(m,2)==0)
      Y = [Y, Yp];
    else
      Y = [Y, fliplr(Yp)];
    end
    X = [X, Xp(m)*ones(1,length(Yp))];
  end
  
  % place at desired position
  Sx = 2048+round(x_center/res); % shift centre in pixel
  Sy = 1980+round(y_center/res); % shift centre in pixel
  
  X = round(X+Sx-W_pxl/2);
  Y = round(Y+Sy);
  dwell_vector = dwell*ones(1,length(X));
end
