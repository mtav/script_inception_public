function [dwell_vector,X,Y] = ZigZagHoleRectangular(beamCurrent,res,dwell,x_center_mum,y_center_mum,x_size_mum,y_size_mum)
  % size of circles in nm as a function of the beamcurrent (diametro of spot)
  spotSizes=[1 8;
  4 12;
  11 15;
  70 25;
  150 35;
  350 55;
  1000 80;
  2700 120;
  6600 270;
  11500 500;
  ];
  
  %projectName='trial9';
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5
  %mag=200000;
  %dwell=20000;
  % rep=1;
  % beamCurrent=1; %Beam current.
  
  % vertical overlap of circles as a proportion of their diameter
  overlap=0.50;
  
  % horizontal distance between circles in nm
  %trenchWidth=150;  % nm
  %trenchWidth=0;  % nm
  
  % width and height of the whole structure in mum
  %W=1.25; %mum
  %H=0.5; %mum
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  
  % size of a circle in mum
  spotSize = spotSizes(find(spotSizes==beamCurrent),2)*1e-3
  %spotSize = 0.500
    
  % vertical stepping distance
  BeamStep_Y = max(round((spotSize-spotSize*overlap)/res),1) % => minimum beamStep = 1 (pxl?)
  %'BeamStep_Y'
  %round((spotSize-spotSize*overlap)/res)
  %1
  %BeamStep_Y
  
  % horizontal stepping distance
  %BeamStep_X = round((spotSize+trenchWidth*1e-3)/res);
  BeamStep_X = BeamStep_Y;
   
  W_pxl = round(x_size_mum/res);
  H_pxl = round(y_size_mum/res);
  
  %xp=[1,1+BeamStep_X,1+(1+2)*BeamStep_X,1+(1+2+3)*BeamStep_X]
  Xp = 1:BeamStep_X:W_pxl;
  Yp = 1:BeamStep_Y:H_pxl;
  
  %'lengths'
  %length(xp)
  %length(yp)
  %return
  
  XpFlip = fliplr(Xp);
  onesVec = ones(1,length(Xp));
  
  dwell_vector = [];
  X = [];
  Y = [];
  
  N = length(Yp);
  for m=1:N
    %disp(['m = ',num2str(m/N)]);
    Y = [Y,Yp(m)*onesVec];
    if (mod(m,2)==0)
      X = [X,Xp];
    else
      X = [X,XpFlip];
    end
  end
  
  Sx = 2048+round(x_center_mum/res); % shift centre in pixel
  Sy = 1980+round(y_center_mum/res); % shift centre in pixel
  
  X = round(X+Sx-W_pxl/2);
  Y = round(Y+Sy-H_pxl/2);
  dwell_vector = dwell*ones(1,length(X));
  
  %filename = ['snake_',projectName,'_',num2str(mag),'X_dwell',num2str(dwell),'_rep',num2str(rep),'.str'];
  %disp(['Writing to ',filename]);
  %fid=fopen(filename,'w+');
  %fprintf(fid,'s\r\n%i\r\n%i\r\n',rep,length(x));
  %fprintf(fid,[num2str(dwell),' %i %i\r\n'],[x;y]);
  %fclose(fid);
  
  % clf
  %disp('Plotting lines...');
  %figure;
  %subplot(2,1,1);
  %plot(x,y,'.');
  %subplot(2,1,2);
  %plot(res*x,res*y,'.');
  
  %hold on;
  
  %disp('Plotting circles...');
  %spotR=spotSize/res/2;
  %for m=1:length(x)
    %subplot(2,1,1)
    %rectangle('Position',[x(m)-spotR,y(m)-spotR,spotSize/res,spotSize/res],'Curvature',[1,1])
    %subplot(2,1,2)
    %rectangle('Position',res*[x(m)-spotR,y(m)-spotR,spotSize/res,spotSize/res],'Curvature',[1,1])
  %end
end
