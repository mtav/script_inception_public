clear all
fileID=fopen('sphere3_uphalf1.gwl','w');
format1='%.3f %.3f %.3f %.3f\n';
format2='%.3f %.3f %.3f %.3f\n';
format3='Write\n';

%power compensation L=(1+k*z)*L0
k0=0.0076*2;
L0=50;

d=25; %diameter
r0=d/2;
voxelX=0.275;
voxelZ=4*voxelX;
overlap=0.5;

% use spherical coordinates
% first half
%{
deltaX=voxelX*(1-overlap);
deltaR=0.2;
deltaP=6 ;

r=r0;
for i=1:r0/deltaR
    phi=0;
    theta=0;
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
            line=[x(j) y(j) z(j)+d/2 L1; x(j+1) y(j+1) z(j+1)+d/2 L2];
            fprintf(fileID,format1,line');
            fprintf(fileID,format3);
    end
    clear ('x','y','z')
    r=r-deltaR;
%     deltaT=deltaT+0.1;
end

% second half

r=0;
for i=1:r0/deltaR+1
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
            line=[x(j) y(j) z(j)+d/2 L1; x(j+1) y(j+1) z(j+1)+d/2 L2];
            fprintf(fileID,format1,line');
            fprintf(fileID,format3);
    end
     clear ('x','y','z')
    r=r+deltaR;
%     deltaT=deltaT+0.1;
end
%}

% use polar coordinates
%
deltaZ=voxelZ*(1-overlap);
deltaR=voxelX*(1-overlap);
deltaT=5;
deltaP=5;
% deltaT2 grid density
% upper half outside ring
phi=0:deltaP:90;
z=r0.*cos(phi*2*pi/360);
r1=sqrt(r0^2-z.*z);

for i=1:length(r1)
    r=r1(i)+2*deltaR;
    
    %outside ring
    for overlap=1:15 %overlap
    t=0;
    for k=1:2 %overwrite
    for j=1:360/deltaT+1
        
            x(j)=r*cos(t*2*pi/360);
            y(j)=r*sin(t*2*pi/360);        
            t=t+deltaT;
    end
    
    for j=1:length(x)-1
        L1=(1+k0*(z(i)+d/2))*L0;
        L2=(1+k0*(z(i)+d/2))*L0;
            line=[x(j) y(j) z(i)+d/2 L1; x(j+1) y(j+1) z(i)+d/2 L2];
            fprintf(fileID,format1,line');
            fprintf(fileID,format3);
    end
    t=deltaT/2;
    end
    r=r-deltaR;
    end
     clear ('x','y')
end
fclose(fileID);

fileID=fopen('sphere3_uphalf2.gwl','w');
%inside grid uphalf
phi=0:deltaP:90;
z=r0.*cos(phi*2*pi/360);
r1=sqrt(r0^2-z.*z);
for i=1:length(r1)
    r=r1(i)+deltaR;
    t1=90;
    t2=90;
    deltaT2=abs(asin(deltaR/r))*360/2/pi; %gap
    for j=1:180/deltaT2
            x1(j)=r*cos(t1*2*pi/360);
            y1(j)=r*sin(t1*2*pi/360);        
            x2(j)=r*cos(t2*2*pi/360);
            y2(j)=r*sin(t2*2*pi/360);
            t1=t1-deltaT2;
            t2=t2+deltaT2;
    end
    
    for j=1:length(x1)
        L1=(1+k0*(z(i)+d/2))*L0;
        L2=(1+k0*(z(i)+d/2))*L0;
            line=[x1(j) y1(j) z(i)+d/2 L1; x2(j) y2(j) z(i)+d/2 L2];
            fprintf(fileID,format1,line');
            fprintf(fileID,format3);
    end
%     r=r1(i);
clear ('x1','y1','x2','y2')
    t1=0;
    t2=0;
    for j=1:180/deltaT2
            x1(j)=r*cos(t1*2*pi/360);
            y1(j)=r*sin(t1*2*pi/360);        
            x2(j)=r*cos(t2*2*pi/360);
            y2(j)=r*sin(t2*2*pi/360);
            t1=t1-deltaT2;
            t2=t2+deltaT2;
    end
    
    for j=1:length(x1)
        L1=(1+k0*(z(i)+d/2))*L0;
        L2=(1+k0*(z(i)+d/2))*L0;
            line=[x1(j) y1(j) z(i)+d/2 L1; x2(j) y2(j) z(i)+d/2 L2];
            fprintf(fileID,format1,line');
            fprintf(fileID,format3);
    end
     clear ('x1','y1','x2','y2')
end
fclose(fileID);

fileID=fopen('sphere3_downhalf3.gwl','w');
%inside grid downhalf
phi=90+deltaP:deltaP:180;
z=r0.*cos(phi*2*pi/360);
r1=sqrt(r0^2-z.*z);
for i=1:length(r1)
    r=r1(i)+deltaR;
    t1=90;
    t2=90;
    deltaT2=abs(asin(deltaR/r))*360/2/pi; %gap
    for j=1:180/deltaT2
            x1(j)=r*cos(t1*2*pi/360);
            y1(j)=r*sin(t1*2*pi/360);        
            x2(j)=r*cos(t2*2*pi/360);
            y2(j)=r*sin(t2*2*pi/360);
            t1=t1-deltaT2;
            t2=t2+deltaT2;
    end
    
    for j=1:length(x1)
        L1=(1+k0*(z(i)+d/2))*L0;
        L2=(1+k0*(z(i)+d/2))*L0;
            line=[x1(j) y1(j) z(i)+d/2 L1; x2(j) y2(j) z(i)+d/2 L2];
            fprintf(fileID,format1,line');
            fprintf(fileID,format3);
    end
%     r=r1(i);
clear ('x1','y1','x2','y2')
    t1=0;
    t2=0;
    for j=1:180/deltaT2
            x1(j)=r*cos(t1*2*pi/360);
            y1(j)=r*sin(t1*2*pi/360);        
            x2(j)=r*cos(t2*2*pi/360);
            y2(j)=r*sin(t2*2*pi/360);
            t1=t1-deltaT2;
            t2=t2+deltaT2;
    end
    
    for j=1:length(x1)
        L1=(1+k0*(z(i)+d/2))*L0;
        L2=(1+k0*(z(i)+d/2))*L0;
            line=[x1(j) y1(j) z(i)+d/2 L1; x2(j) y2(j) z(i)+d/2 L2];
            fprintf(fileID,format1,line');
            fprintf(fileID,format3);
    end
     clear ('x1','y1','x2','y2')
end
fclose(fileID);

fileID=fopen('sphere3_downhalf4.gwl','w');
% lower half
clear ('z','r1','phi');
phi=90+deltaP:deltaP:180;
z=r0.*cos(phi*2*pi/360);
r1=sqrt(r0^2-z.*z);
% r1(1)=0.1;

for i=1:length(r1)
    r=r1(i)+2*deltaR;
    
    %outside ring
    for overlap=1:15 %overlap
    t=0;
    for k=1:2 %overwrite
    for j=1:360/deltaT+1
        
            x(j)=r*cos(t*2*pi/360);
            y(j)=r*sin(t*2*pi/360);        
            t=t+deltaT;
    end
    
    for j=1:length(x)-1
        L1=(1+k0*(z(i)+d/2))*L0;
        L2=(1+k0*(z(i)+d/2))*L0;
            line=[x(j) y(j) z(i)+d/2 L1; x(j+1) y(j+1) z(i)+d/2 L2];
            fprintf(fileID,format1,line');
            fprintf(fileID,format3);
    end
    t=deltaT/2;
    end
    r=r-deltaR;
    end
     clear ('x','y')
end
%}
fclose(fileID);