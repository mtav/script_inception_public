function holeSpiral(outfile)
  %%%%%%%%PARAMTERS%%%%%%%%%%%%%%%%%%%%%%%%%%%
  dwell=800; % Dwell time (us).
  mag=5000; % Magnification.
  rep=10; % Repetitions.
  r=2;  % Width of the square (um).
  N=15;  % Number of rotations of the spiral
  % numPoints=10000; %  METHOD 0: total number of pixels to be etched.
  c=14;  % METHOD 1: A constant defining number of points of the smallest circle.
  % % e=1.7;   % Ellipticity.  Measure of how elliptical the feture is.

  % The equation is:
  % r0: r position of central point
  % rstep: radius step size
  
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  [res, HFW] = getResolution(mag);
  if (r>HFW/2)
    'Feature is too big for this magnification level..' 
    return;
  end
  R = r/res; % Radius in pixels.
  numPoints = 2*pi*R*N;

  t = [];
  %METHOD 0
    t=linspace(0,2*N*pi,numPoints);
  %METHOD 1
   %for i=1:N
       %t=[t,2*pi*linspace(i-1,i,i*c)];
   %end
  %METHOD 2
   %v=fliplr(10-logspace(log10(1),1,260))/9;
   %t=2*N*pi*v;
  %%%%%%%%%%%%%%%%%%%%%%%%%%%
  maxt = max(t);
  x = round(R/maxt*t.*cos(t));
  y = round(R/maxt*t.*sin(t));

  x = x-min(x)+2048-round(R);
  y = y-min(y)+280+2048-round(R);

  c = [x',y'];
  [mixed,k] = unique(c,'rows');
  kk = sort(k);
  coordinates = c(kk,:)';
  
  writeStrFile(outfile, coordinates(1,:), coordinates(2,:), dwell*ones(size(coordinates(1,:))), rep);
end
