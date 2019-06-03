function [dwell_vector,X,Y] = spiralHoleRectangular(beamCurrent,res,dwell,x_center,y_center,x_size,y_size)
  spotSizes=[1 8;
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
  
  %%%%%%%%PARAMTERS%%%%%%%%%%%%%%%%%%%%%%%%%%%
  overlap = 0.25;
  spotSize = spotSizes(find(spotSizes==beamCurrent),2)*1e-3;
  lineSep = spotSize*(2-overlap)/2;  % Seperation of consecutive spiral circles (um).
  innerToOuter = 0; % Direction of etch.
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%55
  W = round(x_size/res);  % Width in pixels.
  H = round(y_size/res);  % Heigth in pixels.
  L = round(lineSep/res);  % Line seperation in pixels.
  
  if ( L == 0 )
    L = 1;
    display('Separation too small using highest resolution')
  end
  
  xl = W + L;
  yl = H + L;
  
  Sx = 2048+round(x_center/res); % shift centre in pixel
  Sy = 1980+round(y_center/res); % shift centre in pixel

  offsetX = Sx-round(W/2);
  offsetY = Sy-round(H/2); %TODO: Use functions/global vars to get constants like 1908 and 2048

  X = offsetX*ones(1,H);
  Y = offsetY+(H-1:-1:0);
  
  while(xl>L && yl>L)  
    %Go to right xl
    xl = xl-L;
    X = [X,(X(end)+1:X(end)+xl-1)];
    Y = [Y,Y(end)*ones(1,xl-1)];
    %Go down yl
    yl = yl-L;
    X = [X,X(end)*ones(1,yl-1)];
    Y = [Y,(Y(end)+1:Y(end)+yl-1)];
    %Go left xl - L
    xl = xl-L;
    X = [X,(X(end)-1:-1:X(end)-xl+1)];
    Y = [Y,Y(end)*ones(1,xl-1)];
    %Go up yl-L
    yl = yl-L;
    X = [X,X(end)*ones(1,yl-1)];
    Y = [Y,(Y(end)-1:-1:Y(end)-yl+1)];
    %Set xl=xl-2L yl=yl-2L
  end
  
  if (innerToOuter)
    X = fliplr(X);
    Y = fliplr(Y);
  end
  dwell_vector = repmat(dwell,size(X,1),size(X,2));
end
