clear all
% fileID=fopen('I-PL_capsule.gwl','w');
% fileID=fopen('I-PG_capsule.gwl','w');
format1='%.3f %.3f %.3f %.3f\n';
format2='%.3f %.3f %.3f %.3f\n';
format3='Write\n';

outfile1 = 'outfile1.matlab.gwl';
outfile2 = 'outfile2.matlab.gwl';
outfile3 = 'outfile3.matlab.gwl';
outfile4 = 'outfile4.matlab.gwl';

%power compensation L=(1+k*z)*L0
k=0.0152; 
L0=50; %35; %IP-L

IPX=0; % IPX:0 (IP-L) or IPX:1 (IP-G)
d=10; %diameter
t=3; %thickness
co=0.6; %eliptical coordinate
hole=2.5; %hole on top radius

r0=d/2;

voxelX=0.3;
voxelZ=4*voxelX;
overlap=0.5;

% use spherical coordinates



if IPX
    % use spherical coordinates
% first half
%
deltaX=voxelX*(1-overlap);
deltaR=0.2;
deltaP=6 ;

fileID=fopen(outfile1,'w');
r=r0;
for i=1:t/deltaR
    phi=0;
    theta=0+asin(hole/r0);
    deltaT=deltaX/r/(360/deltaP);
    
    for j=1:((pi/2-asin(hole/r0))/deltaT+1)
        
        x(j)=r*sin(theta)*cos(phi*2*pi/360);
        y(j)=r*sin(theta)*sin(phi*2*pi/360);
        z(j)=r*cos(theta);
        
        phi=phi+deltaP;
        theta=theta+deltaT;
        
    end
    for j=1:length(x)-1
        L1=(1+k*(z(j)+d/2))*L0;
        L2=(1+k*(z(j+1)+d/2))*L0;
            line=[x(j) y(j) (z(j)+d/2)*co L1; x(j+1) y(j+1) (z(j+1)+d/2)*co L2];
            fprintf(fileID,format1,line');
           
    end
     fprintf(fileID,format3);
    clear ('x','y','z')
    r=r-deltaR;
%     deltaT=deltaT+0.1;
end
fclose(fileID);
% second half

fileID=fopen(outfile2,'w');
r=r0-t;
for i=1:t/deltaR+1
    phi=0;
    theta=pi/2;
    deltaT=deltaX/r/(360/deltaP);
    for j=1:(pi/2/deltaT+1)
        
        x(j)=r*sin(theta)*cos(phi*2*pi/360);
        y(j)=r*sin(theta)*sin(phi*2*pi/360);
        z(j)=r*cos(theta);
        
        phi=phi+deltaP;
        theta=theta+deltaT;
        
    end
    for j=1:length(x)-1
         L1=(1+k*(z(j)+d/2))*L0;
        L2=(1+k*(z(j+1)+d/2))*L0;
            line=[x(j) y(j) (z(j)+d/2)*co L1; x(j+1) y(j+1) (z(j+1)+d/2)*co L2];
            fprintf(fileID,format1,line');
           
    end
     fprintf(fileID,format3);
     clear ('x','y','z')
    r=r+deltaR;
%     deltaT=deltaT+0.1;
end
fclose(fileID);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
else

% second half
deltaX=voxelX*(1-overlap);
deltaR=0.2;
deltaP=6 ;

fileID=fopen(outfile3,'w');
r=r0;
for i=1:t/deltaR
    phi=0;
    theta=pi;
    deltaT=deltaX/r/(360/deltaP);
    for j=1:(pi/2/deltaT+1)
        
        x(j)=r*sin(theta)*cos(phi*2*pi/360);
        y(j)=r*sin(theta)*sin(phi*2*pi/360);
        z(j)=r*cos(theta);
        
        phi=phi+deltaP;
        theta=theta-deltaT;
        
    end
    for j=1:length(x)-1
         L1=(1+k*(z(j)+d/2))*L0;
        L2=(1+k*(z(j+1)+d/2))*L0;
            line=[x(j) y(j) (z(j)+d/2)*co L1; x(j+1) y(j+1) (z(j+1)+d/2)*co L2];
            fprintf(fileID,format1,line');
            
    end
    fprintf(fileID,format3);
     clear ('x','y','z')
    r=r-deltaR;
%     deltaT=deltaT+0.1;
end
fclose(fileID);
%}

% upper half
%
first = true;
fileID=fopen(outfile4,'w');
r=r0;
for i=1:t/deltaR
    phi=0;
    theta=pi/2; 
    deltaT=deltaX/r/(360/deltaP);
    
    if first
      theta
      hole
      r0
      deltaT
      Lfoo = length(1:((theta-asin(hole/r0))/deltaT+1))
      first = false;
    end
    
    disp(['Lfoo = ', num2str(Lfoo)]);
    for j=1:((theta-asin(hole/r0))/deltaT+1) % make hole on top
    
    %j
    %class(Lfoo)
        if j >= Lfoo - 3
          disp(['j = ', num2str(j), ' theta = ', num2str(theta)]);
        end
        
        x(j)=r*sin(theta)*cos(phi*2*pi/360);
        y(j)=r*sin(theta)*sin(phi*2*pi/360);
        z(j)=r*cos(theta);
        
        phi=phi+deltaP;
        theta=theta-deltaT;
        
    end
    for j=1:length(x)-1
        L1=(1+k*(z(j)+d/2))*L0;
        L2=(1+k*(z(j+1)+d/2))*L0;
            line=[x(j) y(j) (z(j)+d/2)*co L1; x(j+1) y(j+1) (z(j+1)+d/2)*co L2];
            fprintf(fileID,format1,line');
            
    end
    fprintf(fileID,format3);
    clear ('x','y','z')
    r=r-deltaR;
%     deltaT=deltaT+0.1;
end
fclose(fileID);

end

% fclose(fileID);
