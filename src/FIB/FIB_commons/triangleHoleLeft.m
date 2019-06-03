function [dwell_vector,X,Y] = triangleHoleLeft(beamCurrent,res,dwell,x_center,y_center,x_size,y_size)
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
  
  Yp = 1:BeamStep_Y:H_pxl;
  
  dwell_vector = [];
  X = [];
  Y = [];
  
  for m = 1:length(Yp);
    L_pxl = W_pxl - abs(Yp(m)-0.5*H_pxl)*(2*W_pxl/H_pxl);
    Xp = -L_pxl:BeamStep_X:-1;
    if (mod(m,2)==0)
      X = [X, Xp];
    else
      X = [X, fliplr(Xp)];
    end
    Y = [Y, Yp(m)*ones(1,length(Xp))];
  end
  
  % place at desired position
  Sx = 2048+round(x_center/res); % shift centre in pixel
  Sy = 1980+round(y_center/res); % shift centre in pixel
  
  X = round(X+Sx);
  Y = round(Y+Sy-H_pxl/2);
  dwell_vector = dwell*ones(1,length(X));
end
