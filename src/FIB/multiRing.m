% This function converts a given vector, profile to a concentric etch mask.
% folder : folder to save to
% rep_vec : Repetitions (ex: 1,3,5 or 16)
% mag : Magnification (ex: 10000 or 20000)
% r_inner_mum : inner radius in mum (ex: 0, 2, 2.8 or 4.2)
% r_outer_mum : outer radius in mum (ex: 2, 2.8 or 4.2)
% prefix : prefix used in filename (ex: 'ERMAN')
% direction : 0 for inner to outer 1 for outer to inner.
% profile_type : 'dome', 'sawtooth', 'dome + ring', 'dome + angular ring', anything else => user-defined profile
% profile : user-defined profile, vector holding dwell times.

% hang your PC with:
% annularProfiler(getenv('TESTDIR'),1,40000,2,4,'_prefix_',0,'dome + angular ring',[],1)

function filename_cellarray = multiRing(folder,mag,prefix,direction,interRingDistancePxl)
  % ex: b=multiRing('TESTDIR/str_ring',36000,'ring',1,1)

  filename_cellarray = {};

  if exist('folder','var')==0
    folder = uigetdir(pwd(),'folder');
  end
  if ~(exist(folder,'dir'))
    error(['dir not found: ',folder]);
  end
  
  %%%%%%%%PARAMETERS%%%%%%%%%%%%%%%%%%%%%%%%%%% 
  %interRingDistancePxl = 1;  % The distance in pixels between each spiral ring.

  h=0.040;
  c=0.080;
  t=0.011667;
  w=0.080;
  R=[h,h+w+c+t,h+w*2+c*2+t*3,h+w*3+c*3+t*6,h+w*4+c*4+t*10,h+w*5+c*5+t*15,h+w*6+c*6+t*21];
  r=[0,h+w,h+w*2+c+t,h+w*3+c*2+t*3,h+w*4+c*3+t*6,h+w*5+c*4+t*10,h+w*6+c*5+t*15];
  rep_vec=1:length(R);

%  R=[h+w*6+c*6+t*21];
%  r=[h+w*6+c*5+t*15];

  r_outer_mum = max([max(r),max(R)]);

  [res, HFW] = getResolution(mag);
  if (r_outer_mum/1e3>HFW/2)
    error('Feature is too big for this magnification level..');
  end
  disp(['Resolution = ',num2str(res),' mum/pxl']);
  
  r_pxl = round(r/res);
  R_pxl = round(R/res);
  R_outer_pxl = round(r_outer_mum/res); % Radius in pixels.
  
  ring_Width = 2.1; %um
  Ring_Width = round(ring_Width/res); %in pixels.

  ringDwell = 2400; %unit: 0.1us
  domeMaxDwell = 3200;
  domeMinDwell = 50;

  writeToFile = 1;
  AllInOne = 1; % separate stream files or only one?
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  rvec = 1:interRingDistancePxl:R_outer_pxl;
  
  pf = [prefix];
  
  for idx=1:length(R)
    profile = [zeros(1,r_pxl(idx)),ones(1,R_pxl(idx)-r_pxl(idx))];
    profile = ringDwell*profile;
    Rad_pxl = length(profile); % Radius in pixels.
    rvec_new = 1:Rad_pxl;
    pxPerRing = round(2*pi*Rad_pxl);
    % todo: reduce nb of points by using find on profile to extract
    % non-zero values
    rad = repmat(rvec_new,pxPerRing,1);
    rad = rad(:)'; % make vector horizontal (xdim=1)

    %% PLOT
    %figure;
    %plot(rvec_new*res*interRingDistancePxl,profile)
    %set(gca,'YDir','reverse')
    %~ pause(.3)
    prefix = pf;

    dwell = round(profile);
    %figure;
    %plot(rvec_new*res*interRingDistancePxl,dwell)
    dwell = repmat(dwell,pxPerRing,1);
    dwell = dwell(:);

    if pxPerRing*nnz(profile)>1e6
      size(linspace(0,2*pi,pxPerRing))
      size(Rad_pxl)
      pxPerRing
      Rad_pxl
      nnz(profile)
      pxPerRing*nnz(profile)
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
      disp('Dauxrigante...');
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

    %figure;
    % maxInd = length(x);
    % ind = (maxInd-40000:10:maxInd);
    % scatter3(x(ind),y(ind),dwell(ind));
    %
    % plot3(x,y,dwell);
    % set(gca,'YDir','reverse')
    % title([num2str(length(x)),' Points']);
    % axis tight;
    %surfMask(x,y,dwell,1);

    %figure;
    %plot(x,y);
    %axis([0 4096 0 4096]);
    
    dwell_vec{idx} = dwell;
    x_vec{idx} = x;
    y_vec{idx} = y;

  end

  % writing
  mkdir(folder);
  if AllInOne
    dwell=[];
    x=[];
    y=[];
    for idx=1:length(R)
      dwell = [dwell, repmat(dwell_vec{idx},1,rep_vec(idx))];
      x = [x, repmat(x_vec{idx},1,rep_vec(idx))];
      y = [y, repmat(y_vec{idx},1,rep_vec(idx))];
    end
    rep=1;
    % folder = uigetdir();
    filename = [folder,filesep,prefix,'.str'];
    %~ filename = [folder,filesep,prefix,'_holeCC_r',num2str(length(profile)),'px_',datestr(now,'yyyymmdd_HHMMSS'),'.str'];
    disp(['length(x) = ',num2str(length(x))]);
    disp(['Writing to ',filename]);
    fid = fopen(filename,'w');
    fprintf(fid,'s\r\n%i\r\n%i\r\n',rep,length(x));
    if ~direction
      fprintf(fid,'%i %i %i\r\n',[dwell;x;y]);
    else
      fprintf(fid,'%i %i %i\r\n',fliplr([dwell;x;y]));
    end
    fclose(fid);
    filename_cellarray{end+1} = filename;
  else
    for idx=1:length(R)
      dwell = dwell_vec{idx};
      x = x_vec{idx};
      y = y_vec{idx};
      % folder = uigetdir();
      filename = [folder,filesep,prefix,'.idx_',num2str(idx),'.rep_',num2str(rep_vec(idx)),'.str'];
      %~ filename = [folder,filesep,prefix,'_holeCC_r',num2str(length(profile)),'px_',datestr(now,'yyyymmdd_HHMMSS'),'.str'];
      disp(['length(x) = ',num2str(length(x))]);
      disp(['Writing to ',filename]);
      fid = fopen(filename,'w');
      fprintf(fid,'s\r\n%i\r\n%i\r\n',rep_vec(idx),length(x));
      if ~direction
        fprintf(fid,'%i %i %i\r\n',[dwell;x;y]);
      else
        fprintf(fid,'%i %i %i\r\n',fliplr([dwell;x;y]));
      end
      fclose(fid);
      filename_cellarray{end+1} = filename;
    end
  end
  
end
