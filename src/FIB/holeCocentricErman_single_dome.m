% This function creates a stream file for a single dome
% folder : folder to save to
% rep : Repetitions (ex: 1,3,5 or 16)
% mag : Magnification (ex: 10000 or 20000)
% r_inner : inner radius in mum (ex: 0, 2, 2.8 or 4.2)
% r_outer : outer radius in mum (ex: 2, 2.8 or 4.2)
% minDwell : minimum dwell time in mus (ex:20 or 150)

function holeCocentricErman_single_dome(folder,rep,mag,r_inner,r_outer,minDwell)
  if exist('folder','var')==0
    folder = uigetdir(pwd(),'folder');
  end
  if ~(exist(folder,'dir'))
    error(['dir not found: ',folder]);
  end

  %%%%%%%%PARAMETERS%%%%%%%%%%%%%%%%%%%%%%%%%%%
  Step=1;  % The distance in pixels between each spiral ring.

  writeToFile=1;

  maxDwell=7000;
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  [res, HFW] = getResolution(mag);
  if (r_outer/1e3>HFW/2)
    error('Feature is too big for this magnification level..');
  end

  R_outer=round(r_outer/res/Step); % Radius in pixels.
  R_inner=round(r_inner/res/Step); % Radius in pixels.

  pxPerRing=round(2*pi*R_outer);
  numRings=R_outer-R_inner+1;

  rvec=R_inner:R_outer;

  dwell=round((1-sin(acos(rvec/max(rvec))))*(maxDwell-minDwell)+minDwell);
  plot(dwell)
  dwell=repmat(dwell,pxPerRing,1);
  dwell=dwell(:);

  rad=repmat(rvec,pxPerRing,1);
  rad=rad(:)';

  theta=repmat(linspace(0,2*pi,pxPerRing),1,numRings);
  x = round(rad.*cos(theta))*Step;
  y = round(rad.*sin(theta))*Step;

  c=[x',y'];
  [mixed,k]=unique(c,'rows');
  kk=sort(k);
  v=c(kk,:)';
  dwell=dwell(kk)';
  % lineLength(coordinates)
  x=v(1,:);
  y=v(2,:);

  x=x+2048-round((min(x)+max(x))/2);
  y=y+2048-round((min(y)+max(y))/2);

  figure;
  % maxInd=length(x);
  % ind=(maxInd-40000:10:maxInd);
  % scatter3(x(ind),y(ind),dwell(ind));
  % title([num2str(length(x)),' Points']);
  % axis tight;
  surfMask(x,y,dwell,1)

  if writeToFile
    % Write to file.
    % folder=uigetdir();
    filename = [folder,filesep,'holeCC_mag',num2str(mag),'_r',num2str(r_outer),'um_',num2str(minDwell),'_',num2str(maxDwell),'.str'];
    disp(['Writing to ',filename])
    fid=fopen(filename,'w');
    fprintf(fid,'s\r\n%i\r\n%i\r\n',rep,length(x));
    fprintf(fid,'%i %i %i\r\n',[dwell;x;y]);
    fclose(fid);
  end
end
