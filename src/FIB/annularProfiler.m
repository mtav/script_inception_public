% This function converts a given vector, profile to a concentric etch mask.
% folder : folder to save to
% rep : Repetitions (ex: 1,3,5 or 16)
% mag : Magnification (ex: 10000 or 20000)
% r_inner_mum : inner radius in mum (ex: 0, 2, 2.8 or 4.2)
% r_outer_mum : outer radius in mum (ex: 2, 2.8 or 4.2)
% prefix : prefix used in filename (ex: 'ERMAN')
% direction : 0 for inner to outer 1 for outer to inner.
% profile_type : 'dome', 'sawtooth', 'dome + ring', 'dome + angular ring', anything else => user-defined profile
% profile : user-defined profile, vector holding dwell times.

% hang your PC with:
% annularProfiler(getenv('TESTDIR'),1,40000,2,4,'_prefix_',0,'dome + angular ring',[],1)

function annularProfiler(folder,rep,mag,r_inner_mum,r_outer_mum,prefix,direction,profile_type,profile,interRingDistancePxl)
  if exist('folder','var')==0
    folder = uigetdir(pwd(),'folder');
  end
  if ~(exist(folder,'dir'))
    error(['dir not found: ',folder]);
  end
  
  %%%%%%%%PARAMETERS%%%%%%%%%%%%%%%%%%%%%%%%%%% 
  %interRingDistancePxl = 1;  % The distance in pixels between each spiral ring.

  [res, HFW] = getResolution(mag);
  if (r_outer_mum/1e3>HFW/2)
    error('Feature is too big for this magnification level..');
  end
  disp(['Resolution = ',num2str(res),' mum/pxl'])
  R_outer_pxl = round(r_outer_mum/res); % Radius in pixels.
  R_inner_pxl = round(r_inner_mum/res); % Radius in pixels.

  ring_Width = 2.1; %um  
  Ring_Width = round(ring_Width/res); %in pixels.

  ringDwell = 3400;             %unit: 0.1us
  domeMaxDwell = 3200;
  domeMinDwell = 50;

  writeToFile = 1;
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  rvec = (R_inner_pxl+1):interRingDistancePxl:R_outer_pxl;
  
  if strcmpi(profile_type,'dome')
    %% DOME
    pf = [prefix,'_dome'];
    profile = 500*(1-sin(acos(rvec/max(rvec))));
  elseif strcmpi(profile_type,'sawtooth')
    %% SAWTOOTH
    pf = [prefix,'_swt'];
    profile = 500*(0.5*sawtooth(rvec/8/pi)+0.5);
  elseif strcmpi(profile_type,'dome + ring')
    %% DOME+RING
    pf = [prefix,'_dmr'];
    profile = domeMaxDwell*(1-sin(acos(rvec/max(rvec))))+domeMinDwell;
    profile = [profile,ringDwell*ones(1,Ring_Width)];
  elseif strcmpi(profile_type,'dome + angular ring')
    %% DOME+ANGULAR RING
    pf = [prefix,'_dmar'];
    profile = domeMaxDwell*(1-sin(acos(rvec/max(rvec))))+domeMinDwell;
    profile = [profile,(Ring_Width:-1:0)/Ring_Width*ringDwell];
  else
    disp('Using user-defined profile');
    pf = [prefix,'_custom'];
  end
      
  Rad_pxl = length(profile); % Radius in pixels.
  rvec_new = 1:Rad_pxl;
  pxPerRing = round(8*pi*Rad_pxl);
  rad = repmat(rvec_new,pxPerRing,1);
  rad = rad(:)';
  
  %% PLOT
  figure;
  plot(rvec_new*res*interRingDistancePxl,profile)
  set(gca,'YDir','reverse')
  %~ pause(.3)
  prefix = pf;
  
  dwell = round(profile);
  figure;
  plot(rvec_new*res*interRingDistancePxl,dwell)
  dwell = repmat(dwell,pxPerRing,1);
  dwell = dwell(:);

  size(linspace(0,2*pi,pxPerRing))
  size(Rad_pxl)
  pxPerRing
  Rad_pxl
  nnz(profile)
  pxPerRing*nnz(profile)
  if pxPerRing*nnz(profile)>1e6
    disp('WARNING: NOT ENOUGH MEMORY. Exiting');
    return
  end
  theta = repmat(linspace(0,2*pi,pxPerRing),1,Rad_pxl);
  x = round(rad.*cos(theta));
  y = round(rad.*sin(theta));

  %% REMOVE POINTS HAVING MINIMUM DWELL
  ind = find(dwell ~=  0);
  x = x(ind);
  y = y(ind);
  dwell = dwell(ind);

  if length(x)<1e5
    %% METHOD 1
    c = [x',y'];
    [mixed,k] = unique(c,'rows');
    kk = sort(k);
    v = c(kk,:)';
    dwell = dwell(kk)';
    % lineLength(coordinates)
    x = v(1,:);
    y = v(2,:);
  else
    %% METHOD 2 IF NOT ENOUGH MEMORY USE THIS METHOD
    disp('WARNING: Using low memory method');
    disp('Dauxrigante...')
    stackSize = 1e5;
    cc = ceil(length(x)/stackSize);
    xn = [];
    yn = [];
    dwellN = [];
    for m = 1:cc
      ind = (m-1)*stackSize+1:min(m*stackSize,length(x));
      c = [x(ind)',y(ind)'];
      dwellT = dwell(ind);
      [mixed,k] = unique(c,'rows');
      kk = sort(k);
      v = c(kk,:)';
      dwellT = dwellT(kk);
      % lineLength(coordinates)
      xn = [xn,v(1,:)];
      yn = [yn,v(2,:)];  
      dwellN = [dwellN;dwellT];
    end

    c = [xn',yn'];
    [mixed,k] = unique(c,'rows');
    kk = sort(k);
    v = c(kk,:)';
    x = v(1,:);
    y = v(2,:);
    dwell = dwellN(kk)';
  end

  x = x+2048-round((min(x)+max(x))/2);
  y = y+2048-round((min(y)+max(y))/2);

  figure;
  % maxInd = length(x);
  % ind = (maxInd-40000:10:maxInd);
  % scatter3(x(ind),y(ind),dwell(ind));
  %
  % plot3(x,y,dwell);
  % set(gca,'YDir','reverse')
  % title([num2str(length(x)),' Points']);
  % axis tight;
  surfMask(x,y,dwell,1);

  figure;
  plot(x,y);
  axis([0 4096 0 4096]);

  if writeToFile
    % Write to file.
    % folder = uigetdir();
    mkdir(folder);
    filename = [folder,filesep,prefix,'_holeCC_r',num2str(length(profile)),'px_',datestr(now,'yyyymmdd_HHMMSS'),'.str'];
    %~ filename = [folder,filesep,prefix,'_holeCC_r',num2str(length(profile)),'px_',datestr(now,'yyyymmdd_HHMMSS'),'.str'];
    %~ rep
    %~ mag
    %~ r_inner_mum
    %~ r_outer_mum
    %~ prefix
    %~ direction
    %~ profile_type
    %~ profile
    %~ ringDwell
    %~ domeMaxDwell
    %~ domeMinDwell

    disp(['length(x) = ',num2str(length(x))])
    disp(['Writing to ',filename])
    fid = fopen(filename,'w');
    fprintf(fid,'s\r\n%i\r\n%i\r\n',rep,length(x));
    if ~direction
      fprintf(fid,'%i %i %i\r\n',[dwell;x;y]);
    else
      fprintf(fid,'%i %i %i\r\n',fliplr([dwell;x;y]));
    end
    fclose(fid);
  end
end
