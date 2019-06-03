function holeSpiralErman(outfile)
  %%%%%%%%PARAMTERS%%%%%%%%%%%%%%%%%%%%%%%%%%%
  dwell=100; % Dwell time (0.1us).
  mag=10000; % Magnification.
  rep=30; % Repetitions.
  direction=0;  % 0 for inner to outer, 1 for outer to inner.
  Step=1;  % The distance in pixels between each spiral ring.
  r_outer=0.3;  
  r_inner=0;  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  [res, HFW] = getResolution(mag);
  if (r_outer/1e3>HFW/2)
    'Feature is too big for this magnification level..' 
    return;
  end

  R_outer = r_outer/res/Step; % Radius in pixels.
  R_inner = r_inner/res/Step; % Radius in pixels.
  numPoints = 4*pi*(R_outer^2-R_inner^2);
  t = [];
  t = linspace(2*R_inner*pi,2*R_outer*pi,numPoints);
  x = round(1/2/pi*t.*cos(t));
  y = round(1/2/pi*t.*sin(t));
  c = [x',y'];
  [mixed,k]=unique(c,'rows');
  kk=sort(k);
  coordinates=c(kk,:)';
  x = coordinates(1,:)*Step;
  y = coordinates(2,:)*Step;
  x = x+2048-round((min(x)+max(x))/2);
  y = y+2048-round((min(y)+max(y))/2);
  dirStr='ItoO';
  if direction
      x=fliplr(x);
      y=fliplr(y);
      dirStr='OtoI';
  end

  writeStrFile(outfile, x, y, dwell*ones(size(x)), rep);
end
