function spiralRing()
projectName='r2';
% projectName='29Oct10KXSm_206_800_150pA_m0.5';
% folder=['ANONYMIZED\MyMatlab\myPhotonicsPackage\FIB\',projectName,'\'];
folder=['J:\cluster\ANONYMIZED\',projectName,'\'];
mkdir(folder);

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

scanType='s';  %  CAnbe 'v' or 'h' or 's'

%sr=0.42; %The sputter rate µm3/nC 
mag=36000;
rep=1;
bC=150; %Beam current.
overlap=0.5;
%depth=1000; %depth of trench (nm)

hc=0.285

R=[hc*2,hc*4,hc*6,hc*8,hc*10]
r=[hc,hc*3,hc*5,hc*7,hc*9]

R0=4;  %  radius of Bigger circle in um
r0=3.4;  %  radius of Smaller circle in um
R1=1;  %  radius of Bigger circle in um
r1=0.4;  %  radius of Smaller circle in um
R2=6;  %  radius of Bigger circle in um
r2=4.4;  %  radius of Smaller circle in um

spotSize=spotSizes(find(spotSizes==bC),2)*1e-3;

HFW=304000/mag; % Width of the horizontal scan-Horizontal Field Width-(um) 
reso=HFW/4096; % size of each pixel (um).
BeamStep=round((spotSize-spotSize/2*overlap)/reso);

Rsq0=(R0/reso)^2;
rsq0=(r0/reso)^2;
Rsq1=(R1/reso)^2;
rsq1=(r1/reso)^2;
Rsq2=(R2/reso)^2;
rsq2=(r2/reso)^2;

Rsq=(R/reso).^2
rsq=(r/reso).^2

if (2.5*max(R)>HFW)
    disp('R is too big to fit to the screen')
    return;
end

Q1=zeros(3335,3900);

cy=size(Q1,1)/2;
cx=size(Q1,2)/2;

for m=1:size(Q1,1)
    for n=1:size(Q1,2)
        distsq=(m-cy)^2+(n-cx)^2;
        %distsq=(n-cx)^2;
        
        
       for idx=1:length(R)
            if (distsq<Rsq(idx) && distsq>rsq(idx))
                Q1(m,n)=1;
            end
       end
    
    end
end

imagesc(Q1)
pause(1)

%% Crop from top
        numCropCellsV=0;
        o=1;
        while (sum(Q1(o,:))==0)
            o=o+1;            
        end
        Q1=Q1(o:end,:);
        numCropCellsV=o-1;
%% Crop from bottom
        o=size(Q1,1);
        while (sum(Q1(o,:))==0)
            o=o-1;            
        end
        Q1=Q1(1:o,:);
%% Crop from left
        numCropCellsH=0;
        o=1;
        while (sum(Q1(:,o))==0)
            o=o+1;            
        end
        Q1=Q1(:,o:end);
        numCropCellsH=o-1;

%% Crop from right
        o=size(Q1,2);
        while (sum(Q1(:,o))==0)
            o=o-1;            
        end
        Q1=Q1(:,1:o);
[X,Y]=imageToEtchPath(Q1,BeamStep,0,'rough',0);

X=X+numCropCellsH;
Y=Y+numCropCellsH;

save([folder,projectName,'.mat'],'X','Y');

clf
plot(X,Y);
