function holeSpiralErman_single_ring(outfile, rep, mag, r_inner, r_outer)
  % This function creates a stream file for a single ring hole
  % outfile : file to save to
  % rep : Repetitions (ex: 1,3,5 or 16)
  % mag : Magnification (ex: 10000 or 20000)
  % r_inner : inner radius in mum (ex: 0, 2, 2.8 or 4.2)
  % r_outer : outer radius in mum (ex: 2, 2.8 or 4.2)

  if exist('outfile','var')==0; error('No outfile specified.'); end;
  if exist('rep','var')==0; rep = 30; end;
  if exist('mag','var')==0; mag = 10000; end;
  if exist('r_inner','var')==0; r_inner = 0; end;
  if exist('r_outer','var')==0; r_outer = 0.3; end;

  %%%%%%%%PARAMETERS%%%%%%%%%%%%%%%%%%%%%%%%%%%
  dwell=800; % Dwell time (us).
  Step=1;  % The distance in pixels between each spiral ring.
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  [res, HFW] = getResolution(mag);
  if (r_outer/1e3>HFW/2)
    error('Feature is too big for this magnification level..')
  end

  R_outer = r_outer/res/Step; % Radius in pixels.
  R_inner = r_inner/res/Step; % Radius in pixels.
  numPoints = 2*pi*(R_outer^2-R_inner^2);
  t = [];
  t = linspace(2*R_inner*pi,2*R_outer*pi,numPoints);
  x = round(1/2/pi*t.*cos(t)*Step);
  y = round(1/2/pi*t.*sin(t)*Step);
  c = [x',y'];
  [mixed,k] = unique(c,'rows');
  kk = sort(k);
  coordinates = c(kk,:)';
  x = coordinates(1,:);
  y = coordinates(2,:);
  x = x+2048-round((min(x)+max(x))/2);
  y = y+2048-round((min(y)+max(y))/2);

  writeStrFile(outfile, x, y, dwell*ones(size(x)), rep);
end
