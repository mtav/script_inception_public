function calcPowerThroughPlane(prnFile, direction)
  % read .prn file
  % It will create a 3D plot of col(3) vs ( col(1), col(2) )
  % ui will be the list of unique values in column 1 and of size NX
  % uj will be the list of unique values in column 2 and of size NY
  % data will then also be of size (NY, NX, N_data_columns)
  [header,data,ui,uj] = readPrnFile(prnFile);

  % get integration limits (as indexes!) and prepare colNames according to the snapshot direction
  if direction == 1
    minui = min(find(ui>yLimits(1)));
    maxui = max(find(ui<=yLimits(2)));
    
    minuj = min(find(uj>zLimits(1)));
    maxuj = max(find(uj<=zLimits(2)));
    
    colNames = {'Eyre','Eyim','Hzre','Hzim','Ezre','Ezim','Hyre','Hyim'};
    
  elseif direction == 2
    minui = min(find(ui>xLimits(1)));
    maxui = max(find(ui<=xLimits(2)));
    
    minuj = min(find(uj>zLimits(1)));
    maxuj = max(find(uj<=zLimits(2))); 
    
    colNames = {'Exre','Exim','Hzre','Hzim','Ezre','Ezim','Hxre','Hxim'};
    
  elseif direction == 3
    minui = min(find(ui>xLimits(1)));
    maxui = max(find(ui<=xLimits(2)));
    
    minuj = min(find(uj>yLimits(1)));
    maxuj = max(find(uj<=yLimits(2)));
    
    colNames = {'Exre','Exim','Hyre','Hyim','Eyre','Eyim','Hxre','Hxim'};
    
  end

  % prepare Fields for the poynting vector calculation
  Fields = zeros([size(data,1),size(data,2),length(colNames)]);
  for n = 1:length(colNames)
    for o = 1:length(header)
      if strcmp(header{o},colNames{n})
        Fields(:,:,n) = data(:,:,o-2);
      end
    end
  end

  % define the imaginary number
  i = sqrt(-1);

  % create complex E vector
  % create complex H vector

  % calculate the poynting vector (PFD will be of size(NY,NX))
  PFD = 0.5*real((Fields(:,:,1)+i*Fields(:,:,2)).*conj(Fields(:,:,3)+i*Fields(:,:,4))-(Fields(:,:,5)+i*Fields(:,:,6)).*conj(Fields(:,:,7)+i*Fields(:,:,8)));

  P = 0.5*real(cross(E,conj(H)));

  % get part of ui,uj over which we will integrate
  uiL = ui(max(1,minui-1):maxui);
  ujL = uj(max(1,minuj-1):maxuj);
  
  % show number of elements over which we will integrate
  length(uiL)
  length(ujL)
  
  % create differential surface (dS) matrix
  % TODO: Take into account direction of the plane
  AreaM = repmat(diff(ujL),1,length(uiL)-1).*repmat(diff(uiL)',length(ujL)-1,1);

  % integrate poynting field over area
  Res(m) = sum(sum(PFD.*AreaM));
end
