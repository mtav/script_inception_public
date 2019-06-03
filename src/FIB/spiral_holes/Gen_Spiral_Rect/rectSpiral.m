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

%%%%%%%%PARAMTERS%%%%%%%%%%%%%%%%%%%%%%%%%%%
dwell=4800; % Dwell time (us).
mag=5000; % Magnification.
bC=1; %Beam current.
overlap=0.25;

spotSize=spotSizes(find(spotSizes==bC),2)*1e-3;
lineSep=spotSize*(2-overlap)/2;  % Seperation of consecutive spiral circles (um).

w=1;  % Width of the square (um).
h=1;  % Width of the square (um).
  
rep=10; % Repetitions.
innerToOuter=0; % Direction of etch.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%55

HFW=304000/mag; % Width of the horizontal scan (um).
res=HFW/4096; % size of each pixel (um).

W=round(w/res);  % Width in pixels.
H=round(h/res);  % Heigth in pixels.
L=round(lineSep/res);  % Line seperation in pixels.

if (L==0)
    L=1;
    display('Seperation too small using highest resolution')
end

yc=0;

xl=W+L;
yl=H+L;

offsetX=2048-round(W/2);
offsetY=1908-round(H/2);

x=offsetX*ones(1,H);
y=offsetY+(H-1:-1:0);

while(xl>L && yl>L)  
    %Go to right xl
    xl=xl-L;
    x=[x,(x(end)+1:x(end)+xl-1)];
    y=[y,y(end)*ones(1,xl-1)];
    %Go down yl
    yl=yl-L;
    x=[x,x(end)*ones(1,yl-1)];
    y=[y,(y(end)+1:y(end)+yl-1)];
    %Go left xl - L
    xl=xl-L;
    x=[x,(x(end)-1:-1:x(end)-xl+1)];
    y=[y,y(end)*ones(1,xl-1)];
    %Go up yl-L
    yl=yl-L;
    x=[x,x(end)*ones(1,yl-1)];
    y=[y,(y(end)-1:-1:y(end)-yl+1)];
	%Set xl=xl-2L yl=yl-2L
end



M=[x;y];
if (innerToOuter)
    M=fliplr(M);
end

figure(1)

for i=1:100:length(x)
     plot(M(1,1:i)*res,M(2,1:i)*res);
     pause(.1)
end

plot(M(1,:),M(2,:));


%Write to file.
%folder='ANONYMIZED\MyMatlab\myPhotonicsPackage\FIB\';
%fid=fopen([folder,'sqSp_mag',num2str(mag),'_w',num2str(w),'_h',num2str(h),'.str'],'w+');
%fprintf(fid,'s\r\n%i\r\n%i\r\n',rep,length(x));
%fprintf(fid,[num2str(dwell),' %i %i\r\n'],M);
%fclose(fid);
