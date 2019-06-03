function surfMask(x,y,dwell,beamStep)
  %beamStep is to get a better plot instead of spikes

  if nargin == 0
    [x, y, dwell, rep, numP] = readStrFile;
    beamStep = 1
  end

  if nargin<4
    beamStep = 1;
  end

  x = x/beamStep;
  y = y/beamStep;

  if length(dwell)==1
    dwell = dwell*ones(1,length(x));
  end
  A = zeros(max(x)-min(x),max(y)-min(y));
  xp = x-min(x)+1;
  yp = y-min(y)+1;

  % dwell = -dwell+max(dwell);
  tic()
  for m=1:length(xp)
    A(xp(m),yp(m))=dwell(m);
  end
  toc()

  % A=A(:,1:round(size(A,2)/2));
  % surf((A)); shading interp

  % imagesc(A)
  % plot3(x,y,dwell);
  % A
  %~ subplot(2,1,1)
  surf(padarray(A,10)); shading interp
  set(gca,'ZDir','reverse')
  axis equal
  view(-31,80)
  %~ subplot(2,1,2)
  %~ surf(padarray(A,10)); shading interp
  %~ set(gca,'ZDir','reverse')
  %~ axis equal
  %~ view(-31,80)
end
