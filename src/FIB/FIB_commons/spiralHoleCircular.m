function [dwell_vector,X,Y] = spiralHoleCircular(beamCurrent,res,dwell,x_center,y_center,x_size,y_size)
  %%%%%%%%Input-PARAMTERS%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %dwell_vector time (us) - try 800.
  %radius Width of the square (um).
  %s shift first hole centre to centre cavity = cavity length(um).

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  radius = 0.5*x_size;
  
  if (radius>4096*res/2)
     error('Feature is too big for this magnification level..');
  end

  R=radius/res; % Radius in pixels.
  % R=radius;

  Sx = round(x_center/res); % shift centre in pixel
  Sy = round(y_center/res); % shift centre in pixel
  
  numPoints = 2*pi*R^2;

  % numPoints
  t = linspace(0,2*pi*R,numPoints);

  X = round(1/(2*pi)*t.*cos(t));
  Y = round(1/(2*pi)*t.*sin(t));

  X = X-min(X)+2048-round(R);
  Y = Y-min(Y)+1980-round(R);

  c = [X',Y'];
  [mixed,k] = unique(c,'rows');
  kk = sort(k);
  coordinates = c(kk,:)';
  % lineLength(coordinates)
  X = coordinates(1,:);
  Y = coordinates(2,:);

  shiftXfirst = 2048+Sx;
  shiftYfirst = 2060+Sy;

  X = shiftXfirst+X-round((min(X)+max(X))/2);
  Y = shiftYfirst+Y-round((min(Y)+max(Y))/2);
  dwell_vector = dwell*ones(1,length(X));
end
