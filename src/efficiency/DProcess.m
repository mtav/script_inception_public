function DProcess(folder,inputFileList)
  % folder=uigetdir();
  %folder='J:\optics\Erman\Optimal vertical emission oPC cavities(optL3)\48nm_half\65400';
  %folder='J:\optics\Erman\qedc3_3_0525b_6_30_1';
  
  % get list of snapshot files
  % NOTE: Adapt here as necessary
  XFsnapFiles = dir([folder,filesep,'x*00.prn']);
  YFsnapFiles = dir([folder,filesep,'y*00.prn']);
  ZFsnapFiles = dir([folder,filesep,'z*00.prn']);
  
  % show number of X,Y,Z snapshots
  length(XFsnapFiles)
  length(YFsnapFiles)
  length(ZFsnapFiles)
  
  % get .inp filename
  % [InpFileName,InpPathName] = uigetfile('*.inp','Select INP file','J:\optics\Erman\Optimal vertical emission oPC cavities(optL3)\48nm_half\65400');
  inpfile = dir([folder,filesep,'*.inp']);
  inpfile
  inpfile = [folder,filesep,inpfile(1).name];
  
  % get inp entries
  inpEntries = GEO_INP_reader({inpfile});
  
  % prepare the following:
  % XSnaps: list of XSnapEntry objects
  % XSnapEntry.fileName: filename
  % XSnapEntry.pos: X position in mum
  % same for Y and Z
  XSnaps = {}; YSnaps = {}; ZSnaps = {};
  for m = 1:length(inpEntries)
    if strcmp(lower(inpEntries{m}.type),'frequency_snapshot')
      % Find out which plane it is
      data = inpEntries{m}.data;
      if cell2mat(data(8))==cell2mat(data(11))
        snapNo=length(XSnaps)+1;
        XSnapEntry.fileName=XFsnapFiles(snapNo).name;
        XSnapEntry.pos=cell2mat(data(8));
        XSnaps{snapNo}=XSnapEntry;  
      elseif cell2mat(data(9))==cell2mat(data(12))
        snapNo=length(YSnaps)+1;
        YSnapEntry.fileName=YFsnapFiles(snapNo).name;
        YSnapEntry.pos=cell2mat(data(9));
        YSnaps{snapNo}=YSnapEntry;
      elseif cell2mat(data(10))==cell2mat(data(13))
        snapNo=length(ZSnaps)+1;
        ZSnapEntry.fileName=ZFsnapFiles(snapNo).name;
        ZSnapEntry.pos=cell2mat(data(10));
        ZSnaps{snapNo}=ZSnapEntry;
      end
    end
  end
    
  % select the .prn files for the calculation box
  % NOTE 1: You must select 1*X,2*Y and 2*Z snapshots for things to work correctly. This is because the structure is assumed to have an X-symmetry.
  % NOTE 2: They should be so that the 2 Y snapshots are not on the same Y-line and the 2 Z snapshots are not on the same Z-line.
  % NOTE 3: output is Y- by default
  %[prnFileNames,prnPathName] = uigetfile('*.prn','Select 6 PRN files',folder,'MultiSelect','on');
  
  prnPathName = ['.',filesep];
  
  %inputFileList = {'triangle_pillar_1_1.inp','triangle_pillar_1_1.geo'}
  PrnFileNameList_xm = findPrnByName(inputFileList,'Box frequency snapshot X-')
  PrnFileNameList_xp = findPrnByName(inputFileList,'Box frequency snapshot X+')
  PrnFileNameList_ym = findPrnByName(inputFileList,'Box frequency snapshot Y-')
  PrnFileNameList_yp = findPrnByName(inputFileList,'Box frequency snapshot Y+')
  PrnFileNameList_zm = findPrnByName(inputFileList,'Box frequency snapshot Z-')
  PrnFileNameList_zp = findPrnByName(inputFileList,'Box frequency snapshot Z+')


  PrnFileNameList_xm = findPrnByName(inputFileList,'Efficiency box frequency snapshot X-')
  PrnFileNameList_xp = findPrnByName(inputFileList,'Efficiency box frequency snapshot X+')
  PrnFileNameList_ym = findPrnByName(inputFileList,'Efficiency box frequency snapshot Y-')
  PrnFileNameList_yp = findPrnByName(inputFileList,'Efficiency box frequency snapshot Y+')
  PrnFileNameList_zm = findPrnByName(inputFileList,'Efficiency box frequency snapshot Z-')
  PrnFileNameList_zp = findPrnByName(inputFileList,'Efficiency box frequency snapshot Z+')

  
  
  %return

  prnFileNames = [PrnFileNameList_xm,PrnFileNameList_xp,PrnFileNameList_ym,PrnFileNameList_yp,PrnFileNameList_zm,PrnFileNameList_zp]
  %prnFileNames = sort(prnFileNames);
  
  % The limits of the surrounding box.
  xLimits=[];
  yLimits=[];
  zLimits=[];

  % Store the X position of the chosen X snapshots in xLimits. Same for Y and Z.
  for n = 1:6
    n
    prnFileName = prnFileNames{n};
    plane = prnFileName(1)-119; % trick to get 1,2,3 from x,y,z
  
    if plane == 1
      for m = 1:length(XSnaps)
        if strcmp(prnFileName,XSnaps{m}.fileName)
          break;
        end 
      end
      XSnaps{m}.pos
      xLimits(length(xLimits)+1) = XSnaps{m}.pos;
    elseif plane == 2
      for m = 1:length(YSnaps)
        if strcmp(prnFileName,YSnaps{m}.fileName)
          break;
        end 
      end
      yLimits(length(yLimits)+1) = YSnaps{m}.pos;
    elseif plane == 3
      for m = 1:length(ZSnaps)
        if strcmp(prnFileName,ZSnaps{m}.fileName)
          break;
        end 
      end
      zLimits(length(zLimits)+1) = ZSnaps{m}.pos;
    end
  end
  
  % show the unordered limits
  xLimits
  yLimits
  zLimits
  
  % add missing x limit (because only one X snapshot was chosen)
  %xLimits = [xLimits,1e20];
  
  % sort limits
  xLimits = sort(xLimits);
  yLimits = sort(yLimits);
  zLimits = sort(zLimits);
  
  Res = [];
  for m = 1:6
    % create new figure
    figure;
  
    % get plane in 1,2,3 format
    [prnFileNameDir,prnFileNameBaseName] = fileparts(prnFileNames{m});
    plane = prnFileNameBaseName(1)-119; % trick to get 1,2,3 from x,y,z
    
    % read .prn file
    % It will create a 3D plot of col(3) vs ( col(1), col(2) )
    % ui will be the list of unique values in column 1 and of size NX
    % uj will be the list of unique values in column 2 and of size NY
    % data will then also be of size (NY, NX, N_data_columns)
    [header,data,ui,uj] = readPrnFile([prnPathName,prnFileNames{m}]);

    % show NX and NY
    'length of ui and uj'
    length(ui)
    length(uj)

    % plot Exmod
    subplot(2,3,1);
    imagesc(ui,uj,data(:,:,1)')
    colorbar;
    title('ui,uj,data(:,:,1)''');
    
    % get integration limits (as indexes!) and prepare colNames according to the snapshot direction
    if plane == 1
      minui = min(find(ui>yLimits(1)));
      maxui = max(find(ui<=yLimits(2)));
      
      minuj = min(find(uj>zLimits(1)));
      maxuj = max(find(uj<=zLimits(2)));
      
      colNames = {'Eyre','Eyim','Hzre','Hzim','Ezre','Ezim','Hyre','Hyim'};
      
    elseif plane == 2
      minui = min(find(ui>xLimits(1)));
      maxui = max(find(ui<=xLimits(2)));
      
      minuj = min(find(uj>zLimits(1)));
      maxuj = max(find(uj<=zLimits(2))); 
      
      colNames = {'Exre','Exim','Hzre','Hzim','Ezre','Ezim','Hxre','Hxim'};
      
    elseif plane == 3
      minui = min(find(ui>xLimits(1)));
      maxui = max(find(ui<=xLimits(2)));
      
      minuj = min(find(uj>yLimits(1)));
      maxuj = max(find(uj<=yLimits(2)));
      
      colNames = {'Exre','Exim','Hyre','Hyim','Eyre','Eyim','Hxre','Hxim'};
      
    end
    
    % quick hack (TODO: do it correctly)
    if minui==1
      minui=2
    end
    if minuj==1
      minuj=2
    end
    
    % crop data
    data = data(minuj:maxuj,minui:maxui,:);
    
    % plot cropped data
    subplot(2,3,2);
    imagesc(data(:,:,1)')
    colorbar;
    title('data(:,:,1)''');
    
    % colIndices = zeros(1,length(colNames));

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
  
    % calculate the poynting vector (PFD will be of size(NY,NX))
    PFD = 0.5*real((Fields(:,:,1)+i*Fields(:,:,2)).*conj(Fields(:,:,3)+i*Fields(:,:,4))-(Fields(:,:,5)+i*Fields(:,:,6)).*conj(Fields(:,:,7)+i*Fields(:,:,8)));
    
    % show the size of PFD
    'size(PFD)'
    size(PFD)
    
    % plot the poynting field (vertical X, horizontal Y for Z plane for example)
    subplot(2,3,3);
    imagesc(PFD')
    colorbar;
    title('PFD''');

    % show NX,NY
    'length of ui and uj'
    length(ui)
    length(uj)
    
    % show "i limits"
    minui
    maxui

    % show "j limits"
    minuj
    maxuj

    % get part of ui,uj over which we will integrate
    uiL = ui(max(1,minui-1):maxui);
    ujL = uj(max(1,minuj-1):maxuj);
    
    % show number of elements over which we will integrate
    length(uiL)
    length(ujL)
    
    % create differential surface (dS) matrix
    % TODO: Take into account direction of the plane
    AreaM = repmat(diff(ujL),1,length(uiL)-1).*repmat(diff(uiL)',length(ujL)-1,1);
    
    % plot dS
    subplot(2,3,4);
    imagesc(AreaM')
    colorbar;
    title('AreaM''');
    
    % integrate poynting field over area
    Res(m) = sum(sum(PFD.*AreaM));
    
    % plot poynting*dS
    subplot(2,3,5);
    imagesc((PFD.*AreaM)')
    colorbar;
    title('(PFD.*AreaM)''');
    
  end
  
  % calculate efficiency and show it
  for i=1:6
    disp([prnFileNames{i},' -> Res(',num2str(i),') = ',num2str(Res(i))])
  end
  total = -Res(1)+Res(2)-Res(3)+Res(4)-Res(5)+Res(6);
  disp(['sum(Res) = ',num2str(total)]);
  
  
  Res(2)/total
  
end
