function [dwell_vector,X,Y] = circleSection(beamCurrent, res, dwell, circleCentro2D_mum, circleRadius_mum, rectW_mum)
  % function [dwell_vector,X,Y] = circleSection(beamCurrent, res, dwell, circleCentro2D_mum, circleRadius_mum, rectW_mum)
  
  % size of circles in nm as a function of the beamcurrent
  spotSizes_nm=[1 8;
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
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5
  %mag=200000;
  %dwell=20000;
  %rep=1;
  %beamCurrent=1; %Beam current.
  
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
  spotSize_mum = spotSizes_nm(find(spotSizes_nm==beamCurrent),2)*1e-3;
  %spotSize_mum = 0.500
    
  % vertical stepping distance
  BeamStep_Y_pxl = max(round( ((1-overlap)*spotSize_mum)/res ),1);
  %'BeamStep_Y_pxl'
  %round((spotSize_mum-spotSize_mum*overlap)/res)
  %1
  %BeamStep_Y_pxl
  
  % horizontal stepping distance
  %BeamStep_X_pxl = round((spotSize_mum+trenchWidth*1e-3)/res);
  BeamStep_X_pxl = BeamStep_Y_pxl;
   
  W_pxl = round(2*circleRadius_mum/res);
  H_pxl = round(rectW_mum/res);
  
  %BeamStep_X_pxl = 0.1
  
  Ncircles = floor((circleRadius_mum/res)/BeamStep_X_pxl)
  
  %circleCentro2D_mum
  %circleRadius_mum
  %rectW_mum
  
  dwell_vector = [];
  X = [];
  Y = [];
  
  %BeamStep_X_pxl = 0.1
  disp('========================')
  Ncircles
  res
  BeamStep_X_pxl

  %currentRadius_pxl = Ncircles*BeamStep_X_pxl
  %alpha_start = asin(H_pxl/currentRadius_pxl)
  %alpha_end = pi - alpha_start
  %L_mum = currentRadius_pxl*(alpha_end-alpha_start)
  %L_pxl = L_mum/res
  %Npoints = L_pxl/BeamStep_X_pxl

  disp('========================')
  %return
  for m = 1:Ncircles
    %m = Ncircles
    currentRadius_pxl = m*BeamStep_X_pxl
    alpha_start = asin(H_pxl/currentRadius_pxl)
    if ( isreal(alpha_start) )
      alpha_end = pi - alpha_start
      L_pxl = currentRadius_pxl*(alpha_end-alpha_start)
      %L_pxl = L_mum/res
      Npoints = L_pxl/BeamStep_X_pxl
      %BeamStep_X_pxl

      %Npoints = 500
      %alpha_start = 0
      %alpha_end = pi
      angles = linspace(alpha_start, alpha_end, Npoints);

      if (mod(m,2)==0) % positive direction
        X = [X,(currentRadius_pxl).*cos(angles)];
        Y = [Y,(currentRadius_pxl).*sin(angles)];
      else % negative direction
        X = [X,(currentRadius_pxl).*cos(fliplr(angles))];
        Y = [Y,(currentRadius_pxl).*sin(fliplr(angles))];
      end
    end
  
  end
  
  Sx = 2048+round(circleCentro2D_mum(1)/res); % shift centre in pixel
  Sy = 1980+round(circleCentro2D_mum(2)/res); % shift centre in pixel
  
  X = round(X+Sx);
  Y = round(Y+Sy);
  dwell_vector = dwell*ones(1,length(X));
  
  length(X)
  
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
  %spotR=spotSize_mum/res/2;
  %for m=1:length(x)
    %subplot(2,1,1)
    %rectangle('Position',[x(m)-spotR,y(m)-spotR,spotSize_mum/res,spotSize_mum/res],'Curvature',[1,1])
    %subplot(2,1,2)
    %rectangle('Position',res*[x(m)-spotR,y(m)-spotR,spotSize_mum/res,spotSize_mum/res],'Curvature',[1,1])
  %end
end
