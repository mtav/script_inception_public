clear all;
clc;

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

projectName='Dave';

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5
mag=200000;
dwell=10000;
rep=1;
bC=1; %Beam current.
overlap=0.5;

%Shaded  Region
WShaded=50;  % Width of the trench in nm
TrenchWidth=100; % Widht of the grating in nm.

numGrating=7; %#Grating
numRep=numGrating+1; %#Trench
W=(numRep*WShaded+(numRep-1)*TrenchWidth)*1e-3 %X total length um
H=0.04;   %Y grating length
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

spotSize=spotSizes(find(spotSizes==bC),2)*1e-3;

[res, HFW] = getResolution(mag);
xRealMax=HFW
yRealMax=262350/mag

BeamStep=max(round((spotSize-spotSize*overlap)/res),1);

wShaded=round(WShaded*1e-3/res);
trenchWidth=round(TrenchWidth*1e-3/res);

h=round(H/res);

xp=1:BeamStep:wShaded;
yp=1:BeamStep:h;
ypFlip=fliplr(yp);
onesVec=ones(1,length(yp));

x=[];
y=[];

for m=1:length(xp)
    
    x=[x,xp(m)*onesVec];
    if (mod(m,2)==0)
        y=[y,yp];
        
    else
         y=[y,ypFlip];
    end

end

lenx=length(x);  % Number of points in each grating
numGratInPar=floor(4.5e5/lenx);  % The number of gratings in each mask which combines to form thewhole structure


xx=x;
for m=1:numRep-1
	xx=xx+trenchWidth+wShaded;
	x=[x,xx];
end

numFlip=floor((numRep)/2);

yy=y;

y=[y,fliplr(y)];
y=repmat(y,1,numFlip);

if (mod(numFlip,2)==0)
    y=[y,yy];
end



sW=4096;
sH=4096-280;


% x=round(x+sW/2-w/2);
y=round(y+sH/2-h/2);

clf
hold on
colorvec=['r','b','k','g','c','m'];

lpar=lenx*numGratInPar;
numPar=numRep/numGratInPar;
for m=1:numPar+1
    
    xpar=x((m-1)*lpar+1:min(m*lpar,length(x)));
    ypar=y((m-1)*lpar+1:min(m*lpar,length(x)));
    
    plot(xpar,ypar,colorvec(mod(m,length(colorvec))+1))
    
    fid=fopen(['Grating_v1_',num2str(m),'_',projectName,'_',num2str(mag),'X_Dwell',num2str(dwell),'_Rep.',num2str(rep),'_NumOfGrating',num2str(numGrating),'_LengthY',num2str(H),'_LengthX',num2str(W),'_OL',num2str(overlap),'_Current',num2str(bC),'.str'],'w+');
    fprintf(fid,'s\r\n%i\r\n%i\r\n',rep,length(xpar));
    fprintf(fid,[num2str(dwell),' %i %i\r\n'],[xpar;ypar]);
    fclose(fid);
    
end




hold on

spotR=spotSize/res/2;
for m=1:length(yy)
    rectangle('Position',[x(m)-spotR,y(m),spotSize/res,spotSize/res],'Curvature',[1,1])
end

axis equal
