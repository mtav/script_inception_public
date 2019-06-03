clear all
fileID=fopen('sphere_ellip60_uphalf1.gwl','w');
format1='%.3f %.3f %.3f %.3f\n';
format2='%.3f %.3f %.3f %.3f\n';
format3='Write\n';

%power compensation L=(1+k*z)*L0
k=0.0076*2;
L0=50;

co=0.6 % make ellipsoid 

d=100; %diameter
r0=d/2;
voxelX=0.25; %0.5;
voxelZ=4*voxelX; %1.5;
overlap=0.5;

% use spherical coordinates
% first half
%
deltaX=voxelX*(1-overlap);
deltaR=0.2;
deltaP=6 ;

r=r0;
fprintf(fileID,format3);
for i=1:r0/deltaR+1
    phi=0;
    theta=0;
%     deltaT=deltaX/r/(360/deltaP);
    deltaT=asin(deltaX/r)/(360/deltaP);
    for j=1:(pi/2/deltaT+1)
        
        x(j)=r*sin(theta)*cos(phi*2*pi/360);
        y(j)=r*sin(theta)*sin(phi*2*pi/360);
        z(j)=r*cos(theta);
        
        
        phi=phi+deltaP;
        theta=theta+deltaT;
        
    end
    for j=1:2:length(x)-2
        L1=(1+k*(z(j)+d/2)*co)*L0;
        L2=(1+k*(z(j+1)+d/2)*co)*L0; 
            line=[x(j) y(j) (z(j)+d/2)*co L1; x(j+1) y(j+1) (z(j+1)+d/2)*co L2];
            fprintf(fileID,format1,line');
            
    end
    fprintf(fileID,format3);
    clear ('x','y','z')
    r=r-deltaR;
%     deltaT=deltaT+0.1;
end
fclose(fileID);

fileID=fopen('sphere_ellip60_uphalf4.gwl','w');
% second half

r=0;
for i=1:r0/deltaR+1
    phi=0;
    theta=pi/2;
    deltaT=asin(deltaX/r)/(360/deltaP);
    for j=1:(pi/2/deltaT+1)
        
        x(j)=r*sin(theta)*cos(phi*2*pi/360);
        y(j)=r*sin(theta)*sin(phi*2*pi/360);
        z(j)=r*cos(theta);
        
        phi=phi+deltaP;
        theta=theta+deltaT;
        
    end
    for j=1:2:length(x)-2
        L1=(1+k*(z(j)+d/2)*co)*L0;
        L2=(1+k*(z(j+1)+d/2)*co)*L0;
            line=[x(j) y(j) (z(j)+d/2)*co L1; x(j+1) y(j+1) (z(j+1)+d/2)*co L2];
            fprintf(fileID,format1,line');
            
    end
    fprintf(fileID,format3);
     clear ('x','y','z')
    r=r+deltaR;
%     deltaT=deltaT+0.1;
end
%}

% use polar coordinates
%{
deltaZ=voxelZ*(1-overlap);
deltaR=voxelX*(1-overlap);
deltaT=5;


% upper half
z=d/2:-deltaZ:0;
r1=sqrt(r0^2-z.*z);
r1(1)=0.5;

for i=1:length(r1)
    r=0;
    t=0;
    for j=1:r1(i)/(deltaR/(360/deltaT))
        
            x(j)=r*cos(t*2*pi/360);
            y(j)=r*sin(t*2*pi/360);
            
            r=r+deltaR/(360/deltaT);
            t=t+deltaT;
            
    end
    for j=1:length(x)-1
            line=[x(j) y(j) (z(j)+d/2)*co; x(j+1) y(j+1) (z(j)+d/2)*co];
            fprintf(fileID,format1,line');
            fprintf(fileID,format3);
     end
end

% lower half
clear ('z','r1');
z=0:-deltaZ:-d/2;
r1=sqrt(r0^2-z.*z);
% r1(1)=0.1;

for i=1:length(r1)
    r=0;
    t=0;
    for j=1:r1(i)/(deltaR/(360/deltaT))
        
            x(j)=r*cos(t*2*pi/360);
            y(j)=r*sin(t*2*pi/360);
            
            r=r+deltaR/(360/deltaT);
            t=t+deltaT;
            
    end
    for j=1:length(x)-1
            line=[x(j) y(j) (z(j)+d/2)*co; x(j+1) y(j+1) (z(j)+d/2)*co];
            fprintf(fileID,format1,line');
            fprintf(fileID,format3);
    end
     clear ('x','y')
end
%}
fclose(fileID);